# coding: utf-8
from will.utils import show_valid, error, warn, print_head

from will.plugin import WillPlugin
from will.decorators import (respond_to, hear, randomly, route, rendered_template,
                             require_settings)

from will import settings
import logging
import random
import json
import re


class AtlassianPlugin(WillPlugin):

    @respond_to("create(?P<project_type>.*)?project(?P<project_name>.*)")
    def will_create_project(self, message, project_type, project_name):
        self.reply(message, "ok creting project %s" % project_name)
        try:
            r = self.create_project(project_name,'mlove')

            self.reply(message, "Created JIRA Project: %s - %s with ID: %s"
                   % (r['key'], project_name, r['id']))
        except:

            raise

    @respond_to("jira")
    def replytome(self,message):
        self.reply(message, 'JIRA!')
