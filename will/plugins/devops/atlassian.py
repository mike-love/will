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
import requests

class AtlassianPlugin(WillPlugin):

    @respond_to("create(?P<project_type>.*)?project(?P<project_name>.*)")
    def will_create_project(self, message, project_type, project_name):
        user_email = self.get_hipchat_user('@%s' % message.sender.nick).get('email')

        self.reply(message, "ok creating project %s with %s as project lead"
                   % (project_name, user_email))

        try:
            hc = self.create_hipchat_room(project_name, owner=user_email)
            self.reply(message, "created hipchat room %(room)s" %{'room': hc.get('name')})
        except:
            raise

        try:
            try:
                ur = self.get_jira_user(user_email.split('@')[0])

                proj_admin = user_email.split('@')[0]
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    proj_admin = settings.JIRA_USERNAME

                else:
                    raise
            logging.debug('Creating JIRA project %s with %s as admin/lead' % (project_name, proj_admin))
            j_resp = self.create_jira_project(proj_name=project_name, proj_admin=proj_admin,
                                              proj_template_key="com.pyxis.greenhopper.jira:gh-scrum-template")
            admin_role = self._get_jira_admin(self.get_jira_project_roles(j_resp['key']))

            logging.debug('Adding %(admin)s to role %(roleid)s for project %(j_key)s'
                          % {'admin': proj_admin, 'roleid': admin_role, 'j_key': j_resp['key']})

            jrole_resp = self.assign_jira_project_role(proj_admin, j_resp['key'], admin_role)

            self.reply(message, "Created JIRA Project: %s - %s with ID: %s"
                   % (j_resp['key'], project_name, j_resp['id']))
        except:

            raise

        try:
            # reuse the jira key if it's not already assigned in confluence
            if self.space_key_exists(j_resp['key']):
                space_key = None
            else:
                space_key = j_resp['key']

            try:
                ur = self.get_confluence_user(user_email.split('@')[0])
                proj_admin = user_email.split('@')[0]
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    proj_admin = settings.CONFLUENCE_USERNAME
                else:
                    raise

            context_element = {"jira-server": "6028ff00-2ed7-3998-8913-344d65267cba",
                        "jira-project": j_resp['id'], "name": project_name,
                        "spaceKey": space_key, "description":"",
                        "noPageTitlePrefix":"true", "alt_token":"undefined",
                        "jira-server-id": "6028ff00-2ed7-3998-8913-344d65267cba",
                        "project-key": j_resp['key'], "project-name": project_name,
                        "ContentPageTitle": project_name}

            logging.debug('Creating Confluence space %s with %s as admin/lead' % (project_name, proj_admin))
            c_resp = self.create_space(project_name, space_key=space_key,
                                       description="", space_admin=proj_admin,
                                       blueprint=True, context_element=context_element,
                                       blueprint_id="22dd1292-0487-406b-9c89-d342e6d7e8cd")

            self.reply(message, 'Created atlassian project %(name)s' % {'name': project_name})
        except:
            raise

    def _get_jira_admin(self, roles):
        """ get the jira admin role from a role api response """
        admin_url = roles.get('Administrators')

        if admin_url:
            return admin_url.split('/')[-1]
        else:
            raise

