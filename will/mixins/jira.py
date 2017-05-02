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

    def get_project(klass, jira_key=None):
        """ return specific project information using the key param, or
            return all projects

            :param jira_key: jira project key to create the issue in
            :param summary: issue summary
            :retun: json response object
        """

        endpoint = JIRA_PROJECT_ENDPOINT % {'id': (str(jira_key or ''))}
        self.log.info('Getting project %(jira_key)s from %(server)s' \
                       % {'jira_key': jira_key, 'server': self.app_root})

        return self.client.request("GET", endpoint)


    def get_project_keys(klass, user=default_user, password=default_pass):
        """get a list of project keys from jira
            :param user: (optional): user to use for authentication
            :param password: (optional): password of the user for
                authentication
            :return list of keys
        """
        key_list = (r.get('key') for r in klass.get_project(jira_key=None,
                                                            user=user,
                                                            password=password))

        klass.log.info('Fetched keylist from %(server)s'\
                       % {'server':klass.app_root})

        return key_list


    def get_issue(klass, proj_key, user=default_user, password=default_pass,
                  issue_id=None):

        """ get an issue from the jira project or return all issues for a
                project if no key is specified
            :param proj_key: jira project key to retrieve the issue in
            :param user: (optional): user to act as the submitter
            :param password: (optional): password of the user acting
                as submitter
            :param issue_id: (optional): issue key of a specific issue
                to retrieve
            :return: json response object
        """
        if issue_id:
            endpoint = JIRA_ISSUE_ENDPOINT % {'id': str(issue_id)}
            klass.log.info('Getting issue %(issueid)s from %(server)s' \
                    % {'issueid': issue_id, 'server': klass.app_root})

            return klass._jira_request("GET", endpoint, user, password)

        else:
            endpoint = JIRA_SEARCH_ENDPOINT
            params = "jql=project=\"%s\"" % proj_key
            klass.log.info('Geting issues for query: %(query)s from %s(server)' \
                            % {'query': params, 'server': klass.app_root})

            return klass._jira_paged_request("GET", endpoint, user, password,
                                             data_key='issues', params=params)

    def create_project(klass, proj_name, proj_key=None, proj_admin=None,
                       proj_type="software", user=default_user,
                       password=default_pass):

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
            proj_key = will_shared.key_gen(proj_name, 10,
                                           klass.get_project_keys())

        data = {"key": proj_key, "name": proj_name,
                "projectTypeKey": proj_type,
                "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                "lead": proj_admin}
        endpoint = JIRA_PROJECT_ENDPOINT %{'id':''}
        klass.log.info('Creating project: %(data)s' % {'data': data})
        api_resp = klass._jira_request("POST", endpoint, user,
                                       password, True, data=data)
        logging.info('Response: \r\n %(resp)s' %{'resp': api_resp})
        return api_resp

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
