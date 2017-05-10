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
    pass

