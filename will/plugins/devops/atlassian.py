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
        user_prof = self.get_hipchat_user(self, user_id)

        if user_prof.get('email'):
            tmp_un = user_prof['email'].split('@')[0]
            if self._is_valid_user(tmp_un):
                proj_admin = tmp_un
            else:
                proj_admin = settings.JIRA_USERNAME
        else:
            proj_admin = settings.JIRA_USERNAME


        self.reply(message, "ok creating project %s with %s as project lead" % project_name)

        try:
            r = self.create_jira_project(project_name,'mlove',
                    proj_template_key="com.pyxis.greenhopper.jira:gh-scrum-template")

            self.reply(message, "Created JIRA Project: %s - %s with ID: %s"
                   % (r['key'], project_name, r['id']))
        except:

            raise

    def _is_valid_user(self, userid):
        """checks if the user is a valid user"""
        if(self.get_jira_user(userid).get('email')):
            return True
        else:
            return False


