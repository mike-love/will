# coding: utf-8
from will.utils import show_valid, error, warn, print_head, key_gen

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
        user_prof = self.get_hipchat_user(message.sender.nick)

        if user_prof.get('email'):
            tmp_un = user_prof['email'].split('@')[0]
            if self._is_valid_user(tmp_un):
                logging.debug('Could not find user %(user)s in %(server)s'
                              % {'user': tmp_un, 'server': settings.JIRA_SERVER})

                proj_admin = tmp_un
            else:
                proj_admin = settings.JIRA_USERNAME
        else:
            proj_admin = settings.JIRA_USERNAME


        self.reply(message, "ok creating project %s with %s as project lead"
                   % (project_name, proj_admin))

        try:
            hc = self.create_hipchat_room(project_name, owner='dummy@example.com')
            self.reply(message, "created hipchat room %(room)s" %{'room': hc.get('name')})
        except:
            raise

        try:
            j_resp = self.create_jira_project(proj_name=project_name, proj_admin=proj_admin,
                                              proj_template_key="com.pyxis.greenhopper.jira:gh-scrum-template")

            self.reply(message, "Created JIRA Project: %s - %s with ID: %s"
                   % (j_resp['key'], project_name, j_resp['id']))
        except:

            raise

        try:
            # reuse the jira key if it's not already assigned in confluence
            space_key = j_resp['key']

            context_element = {"jira-server": "6028ff00-2ed7-3998-8913-344d65267cba",
                        "jira-project": j_resp['id'], "name": project_name,
                        "spaceKey": space_key, "description":"",
                        "noPageTitlePrefix":"true", "alt_token":"undefined",
                        "jira-server-id": "6028ff00-2ed7-3998-8913-344d65267cba",
                        "project-key": j_resp['key'], "project-name": project_name,
                        "ContentPageTitle": project_name}

            c_resp = self.create_space(project_name, space_key=space_key,
                                       space_admin=proj_admin, description="",
                                       blueprint=True, context_element=context_element,
                                       blueprint_id="22dd1292-0487-406b-9c89-d342e6d7e8cd")
            self.reply(message, 'Created atlassian project %(name)s' % {'name': project_name})
        except:
            raise



    def _is_valid_user(self, userid):
        """checks if the user is a valid user"""
        if(self.get_jira_user(userid).get('email')):
            return True
        else:
            return False


