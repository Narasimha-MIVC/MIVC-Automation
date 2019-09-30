"""Module for verifying the status of Maintenance -> Hybrid -> users
   File: services.py
   Author: Prasanna
"""
import os
import sys
import time
import inspect

import stafenv

from web_wrappers import selenium_wrappers as base

__author__ = "Prasanna"


class Users(object):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):

        # self._browser = args[0]
        self.action_elm = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)


