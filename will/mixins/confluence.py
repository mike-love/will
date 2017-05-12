import logging
import json
import re

from will import settings
from ..utils import RESTClient
from ..utils import key_gen


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
        log.error('Cannot find required settings in configuration provided')
        raise Exception('Parameter missing from configuration; CONFLUENCE requires CONFLUENCE_USERNAME, \
                CONFLUENCE_PASSWORD, and CONFLUENCE_SERVER.')

