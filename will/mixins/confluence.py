import logging
import json
import re

from will import settings
from ..utils import RESTClient
from ..utils import key_gen

CONFLUENCE_SPACE_ENDPOINT = "/rest/api/space/{id}"
CONFLUENCE_USER_ENDPOINT = "/rest/api/user"
CONFLUENCE_BLUEPRINT_ENDPOINT = "/rest/create-dialog/1.0/space-blueprint/create-space"

class ConfluenceMixin(object):
    log = logging.getLogger(__name__)

    try:
        log.debug('Attempting to get mixin settings from configuraiton')
        default_user = settings.CONFLUENCE_USERNAME
        default_pass = settings.CONFLUENCE_PASSWORD
        app_root = settings.CONFLUENCE_SERVER

        client = RESTClient.client('basic', app_root,
                                        default_user, default_pass)
    except AttributeError:
        log.error('Parameter(s) missing from configuration; \
        CONFLUENCE requires CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD, \
        and CONFLUENCE_SERVER.')

    def get_space(self, space_key=None):
        """ return information about a specific space
            :param space_key: confluence space key
            :return:
        """

        endpoint = CONFLUENCE_SPACE_ENDPOINT % {'id': str(space_key or '')}
        self.log.info('Getting space with %(key)s from server %(server)'
                      % {'key': space_key, 'server': self.app_root})

        return self.client.request("GET", endpoint)

    def get_space_keys(self, space_name=None):
        """ return space keys; if a space_name is not provided all keys are
                returned
            :param: space_name: (optional) name of the space whose key will
                be returned
            :param user: (optional): user to act as the submitter
            :param password: (optional): password of the user acting
            :return: list of keys
        """

        if space_name:
            pass
        else:
            key_list = [r.get('key') for r in self.get_space(space_key=None)]

        return key_list

    def get_confluence_user(self, user_name):
        """ return information about a specific user; if no user is provided
            all user data will be returned
            :param user_name: confluence username of the user to retrieve
            :return: json object
        """
        endpoint = CONFLUENCE_USER_ENDPOINT
        params = {'username': user_name}

        self.log.info('Getting user %(user)s from server %(server)'
                      % {'user': user_name, 'server': self.app_root})


        return self.client.request("GET", endpoint)

    def create_space(self, space_name, space_key=None, description=None,
                     space_admin=None, blueprint=False, **kwargs):

        """
            :param space_name: name of the space to create
            :param space_key: (optional) pre-defined confluence spacke key; if
                not provided one will be generated from the space name
            :param space_admin: (optional) confluence username of the user to
                assign as the admin in the space
            :param blueprint: (optional) confluence blueprint to use as the
                template for the space; if true, context_element, and
                blueprint_id must be provided as a keyword arg
            :return: json response object

        """

        if space_key is None:
            # Confluence keys are maxed at 255 chars
            space_key = utils.key_gen(space_name, 255,
                                            self.get_space_keys())


        if blueprint and kwargs.get('context_element'):
            # do blueprint things


            data = {"spaceKey": space_key, "name": project_name,
                    "description": description,
                    "spaceBlueprintId": kwargs.get('blueprint_id'),
                    "context": kwargs.get('context_element')}

            endpoint = CONFLUENCE_BLUEPRINT_ENDPOINT
        else:

            data = {"key": space_key, "name": project_name}

            pass

        return self.request("POST", endpoint=endpoint, data=data)

