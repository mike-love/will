import logging
import json
import re

from will import settings
from ..utils import RESTClient
from ..utils import key_gen

JIRA_ISSUE_ENDPOINT = "/rest/api/2/issue/%(id)s"
JIRA_PROJECT_ENDPOINT = "/rest/api/2/project/%(id)s"
JIRA_SEARCH_ENDPOINT = "/rest/api/2/search/"
JIRA_PROJ_ROLES_ENDPOINT = "/rest/api/2/project/%(id)s/role/%(roleid)s"

class _JIRAMixin(object):
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

        self.client = RESTClient.client('basic', self.app_root,
                                    self.default_user, self.default_pass)

    def get_project(self, jira_key=None):
        """ return specific project information using the key param, or
            return all projects

            :param jira_key: jira project key to create the issue in
            :param summary: issue summary
            :retun: json response object
        """

        endpoint = JIRA_PROJECT_ENDPOINT % {'id': (str(jira_key or ''))}
        self.log.info('Getting project %(jira_key)s from %(server)s' \
                       % {'jira_key': jira_key, 'server': self.app_root})

        return self.client.request("GET", endpoint, cb=self.client.strip_data)


    def get_project_keys(self):
        """get a list of project keys from jira
            :return list of keys
        """
        key_list = (r.get('key') for r in self.get_project(jira_key=None))

        self.log.info('Fetched keylist from %(server)s' % {'server':self.app_root})

        return key_list


    def get_issue(self, proj_key, issue_id=None):

        """ get an issue from the jira project or return all issues for a
                project if no key is specified
            :param proj_key: jira project key to retrieve the issue in
            :param issue_id: (optional): issue key of a specific issue
                to retrieve
            :return: json response object
        """
        if issue_id:
            return self._get_one_issue(issue_id)
        else:
            return self_get_one_issue(issue_id)

    def _get_one_issue(self, issue_id):

            endpoint = JIRA_ISSUE_ENDPOINT % {'id': str(issue_id)}
            self.log.info('Getting issue %(issueid)s from %(server)s' \
                    % {'issueid': issue_id, 'server': self.app_root})

            return self.client.request("GET", endpoint)

    def _get_many_issues(self):

        endpoint = JIRA_SEARCH_ENDPOINT
        params = "jql=project=\"%s\"" % proj_key
        klass.log.info('Geting issues for query: %(query)s from %s(server)' \
                        % {'query': params, 'server': klass.app_root})

        return self._jira_paged_request("GET", endpoint, user, password,
                                         data_key='issues', params=params)

    def get_project_roles(self, proj_key):
        """ retrieve roles available for a specific project
            param proj_key: jira project to retrieve the roles from
            :return: json response object
            :JIRA URI: /rest/api/2/project/%(id)s/role/%(roleid)s
        """

        endpoint = JIRA_PROJ_ROLES_ENDPOINT % {'id':proj_key, 'roleid':''}
        self.log.info('Getting project roles for %(proj_key)s from %(server)s' \
                % {'proj_key': proj_key, 'server': self.app_root})

        return self.client.request("GET",endpoint, cb=self.client.strip_data)

    def create_project(self, proj_name, proj_key=None, proj_admin=None,
                       proj_type="software"):

        """create a project with the provided project name
            :param proj_name: name of the project
            :param proj_key: (optional) pre-defined jira project key; if not
                provided one will be generated from the project name
            :param proj_admin: (optional)jira username of the user to assign
                as the admin on the project
            :param proj_type: (optional) jira project type to create
            :param user: (optional): user to act as the submitter
            :param password: (optional): password of the user acting
                as submitter
            :return: json response object
        """

        if proj_key is None:
            # Jira keys are maxed at 10 chars
            proj_key = key_gen(proj_name, 10, self.get_project_keys())

        data = {"key": proj_key, "name": proj_name,
                "projectTypeKey": proj_type,
                "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                "lead": proj_admin}

        endpoint = JIRA_PROJECT_ENDPOINT %{'id':''}
        self.log.debug('Creating project: %(data)s' % {'data': data})

        return self.client.request("POST", endpoint,
                                   cb=self.client.strip_data, data=data)


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

    def assign_project_role(self, user, proj_key, roleid):
        """ assign a specific role to a user
            :param user: user to assign the role to
            :param proj_key: project key the user will recieve the role for
            :param roleid: role id to assign to the user
            :return json response
            :JIRA URI: /rest/api/2/project/%(id)s/role/%(roleid)s
        """
        endpoint = JIRA_PROJ_ROLES_ENDPOINT % {'id': proj_key, 'roleid': roleid}

        self.client.request("POST", JIRA_PROJ_ROLES_ENDPOINT)

JIRAMixin = _JIRAMixin()
