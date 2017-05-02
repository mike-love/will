import logging
import json
import re

from will import settings
from ..utils import RESTClient

JIRA_ISSUE_ENDPOINT = "/rest/api/2/issue/%(id)s"
JIRA_PROJECT_ENDPOINT = "/rest/api/2/project/%(id)s"
JIRA_SEARCH_ENDPOINT = "/rest/api/2/search/"

class JIRAMixin(object):
    log = logging.getLogger(__name__)
    try:
        log.debug('Attempting to get mixin settings from configuraiton')
        default_user = settings.JIRA_USERNAME
        default_pass = settings.JIRA_PASSWORD
        app_root = settings.JIRA_SERVER
    except AttributeError:
        log.error('Cannot find required settings in configuration provided')
        raise Exception('Parameter missing from configuration; JIRA requires JIRA_USERNAME, \
                JIRA_PASSWORD, and JIRA_SERVER.')

    def __init__(self, auth='basic'):
        self.client = RESTClient.client(auth)

    def get_project(klass, jira_key=None, user=default_user,
                    password=default_pass):
        """ return specific project information using the key param, or
            return all projects

            :param jira_key: jira project key to create the issue in
            :param summary: issue summary
            :param user: (optional): user to act as the submitter
            :param password: (optional): password of the user acting as
                submitter
            :retun: json response object
        """

        endpoint = JIRA_PROJECT_ENDPOINT % {'id': (str(jira_key or ''))}
        klass.log.info('Getting project %(jira_key)s from %(server)s' \
                       % {'jira_key': jira_key, 'server': klass.app_root})

        return klass._jira_request("GET", endpoint, user, password)

    def create_issue(self, jira_key, summary, description=None, priority=None,
                     issue_type='task'):

        """ create an issue in the specified space
            :param jira_key: jira project key to create the issue in
            :param summary: issue summary
            :param description: (optional): issue description
            :param priority: (optional): issue priority
            :param issue_type: (optional): issue type to create
            :return: json response object
            {"fields": {
                project":{
                    "key": "TEST"
                },
                "summary": "REST ye merry gentlemen.",
                "description": "Creating of an issue using project
                                 and issue type names using the REST API",
                "issuetype": {
                    "name": "Bug"
                }
            }}
        """

        project = {"key": jira_key}
        issuetype = {"name": issue_type}
        data = {"fields": {"project": project, "summary": summary,
                "description": description, "issuetype": issuetype}}


        klass.log.info('Creating issue: %(data)s' % {'data': data})

        return self.client.request("POST", JIRA_ISSUE_ENDPOINT, data=data)
