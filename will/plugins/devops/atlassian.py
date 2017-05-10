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

    @require_settings("JIRA_USERNAME", "JIRA_PASSWORD", "JIRA_SERVER")
    @respond_to("\bcreate \b(?P<project_type>.*)?\bproject\b (?P<project_name>.*).*$")
    def create_project(self, message, project_type, project_name):
        try:
            r = self.create_project(project_name)
        except:


            self.reply(message, "Created JIRA Project: %s - %s with ID: %s"
                       % r['key', project_name, r['id'])

