"""Module for creating and verifying
   File:
   Author: Prasanna
"""

import os
import sys
import time
import inspect

from web_wrappers import selenium_wrappers as base

__author__ = "Prasanna"


class Topology(object):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        # self._browser = args[0]
        self.action_ele = base.WebElementAction(self._browser)



