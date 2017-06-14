# coding: utf-8
from will.utils import show_valid, error, warn, print_head

from will.plugin import WillPlugin
from will.decorators import (respond_to, hear, randomly, route, rendered_template,
                                require_settings)
from will import settings
import requests
import random
GIPHY_KEY = 'dc6zaTOxFJmzC'

GIF_URL = 'http://api.giphy.com/v1/gifs/translate?s=%(search_string)s&api_key=%(api_key)s'

class GIPHYPlugin(WillPlugin):
    @require_settings('GIPHY_KEY')
    @hear("^gif me (?P<search_string>.*)")
    def gif_me(self, message, search_string):
        """
           gif me ___: use giphy to search for a GIF related to ___
        """
        url = GIF_URL % {"search_string": search_string,
                         'api_key': settings.GIPHY_KEY}
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                gif_return = r.json()['data']['images']['fixed_height']['url']
                self.reply(message,gif_return)
            else:
                self.reply(message, 'GIFY is not working right now; try again later')
        except:
            raise

