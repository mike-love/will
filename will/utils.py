# -*- coding: utf-8 -*-
from clint.textui import puts, indent
from clint.textui import colored
from HTMLParser import HTMLParser
from requests.auth import HTTPBasicAuth
import requests
import re
import json
import logging

class Bunch(dict):
    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__ = self

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self


# Via http://stackoverflow.com/a/925630
class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def html_to_text(html):
    # Do some light cleanup.
    html = html.replace("\n", "").replace("<br>", "\n").replace("<br/>", "\n").replace('<li>', "\n - ")
    # Strip the tags
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()


def is_admin(nick):
    from . import settings
    return settings.ADMINS == '*' or nick.lower() in settings.ADMINS


def show_valid(valid_str):
    puts(colored.green(u"✓ %s" % valid_str))


def warn(warn_string):
    puts(colored.yellow("! Warning: %s" % warn_string))


def error(err_string):
    puts(colored.red("ERROR: %s" % err_string))


def note(warn_string):
    puts(colored.cyan("- Note: %s" % warn_string))


def print_head():
        puts("""
      ___/-\___
  ___|_________|___
     |         |
     |--O---O--|
     |         |
     |         |
     |  \___/  |
     |_________|

      Will: Hi!
""")


def sizeof_fmt(num, suffix='B'):
    # http://stackoverflow.com/a/1094933
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def key_gen(name, key_len, key_check, appender=None):
    """ generate a key from the name parameter
        :param name: string from which to derive a project key;
            usually name or title
        :param key_len: maximum length of the key value
        :param key_check: callback to verify key is unique
        :param appender(optional) integer to append if the key is not
            unique
        :return key
    """
    tmp_key = (re.sub('[^A-Z]', '', name)[:key_len-len(str(appender or ''))] +
               str(appender or ''))

    if key_check:
        if key_check(tmp_key):
            tmp_key = key_gen(name, key_len, key_check,
                              appender=int(appender or 0)+1)
    return tmp_key


class _RESTClient(object):
    url_pat = re.compile('(?P<scheme>https?:\/\/)?(?P<base>[\da-z\.-]+\.[a-z\.]{2,6}[\/\w \.-]*)\/?$')

    def __init__(self, base_url):
        self.base = base_url
        self._sess = requests.Session()

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, usr_base):
        match = self.url_pat.match(usr_base.lower())
        if match:
            self._base = match.group('base')
            self.scheme = match.group('scheme') if match.group('scheme') else 'http://'
        else:
            # want to through an error eventually
            pass

    def _uri_join(self, fragment):
        base = '/'.join(frag for frag in (self.base.split('/') + fragment.split('/')) if frag)
        return ''.join([self.scheme, base])

    def request(self, method, endpoint, raise_for_status=True,
                params={}, cb=None, **kwargs):
        """internal method of making requests"""

        url = self._uri_join(endpoint)
        try:
            r = self._sess.request(method=method, url=url, params=params, **kwargs)
            if r.text:
               logging.debug('%(endpoint)s: \r\n %(resp)s' %{'endpoint': endpoint, 'resp': r.text})
            if raise_for_status:
                r.raise_for_status()
            if cb:
                return cb(r)
            else:

                return r
        except:
            raise

    def strip_data(self, response):
        if response.text:
            return response.json()
        else:
            raise AttributeError


class BasicRESTClient(_RESTClient):
    def __init__(self, base_url, username=None, password=None):

        super(SimpleRESTClient, self).__init__(base_url)

        if username and password:
            auth = HTTPBasicAuth(username, password)
        self._sess = requests.Session()
        self._sess.headers['Content-Type'] = 'application/json'
        self._sess.auth = auth

# TODO: Remove class
class _BasicRESTClient(_RESTClient):
    """ RESTClient with Basic HTTP auth"""

    def __init__(self, base_url, username=None, password=None):
        super(_BasicRESTClient, self).__init__(base_url)

        if username and password:
            auth = HTTPBasicAuth(username, password)
        self._sess = requests.Session()
        self._sess.headers['Content-Type'] = 'application/json'
        self._sess.auth = auth


# TODO: Remove class
class RESTClient(object):
    @staticmethod
    def client(auth, base_url, username=None, password=None):
        """ factory for rest client generation based on the require auth type
            :param auth:
            :param base_url:
            :param username:
            :param password:
            :return _RESTClient
        """

        if auth.lower() == 'basic':
            return _BasicRESTClient(base_url, username, password)
        else:
            return None
