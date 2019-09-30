"""Module for synchronizing the hybrid connections
   File: synchronization.py
   Author: Prasanna, Priyanka
"""
import os
import sys
import time
import inspect

import stafenv

from web_wrappers import selenium_wrappers as base

__author__ = "Prasanna and Priyanka"


class Synchronization(object):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):

        # self._browser = args[0]
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def synchronize_ac_id_and_token(self, **params):

        try:
            self.action_ele.explicit_wait("std2_admin_system_hybrid_sync_ac_id")
            self.action_ele.input_text("std2_admin_system_hybrid_sync_ac_id", params["accountId"])

            self.action_ele.explicit_wait("std2_admin_system_hybrid_sync_ac_token")
            self.action_ele.input_text("std2_admin_system_hybrid_sync_ac_token", params["token"])

            # Now Synchronize
            self.action_ele.explicit_wait("std2_admin_system_hybrid_sync_now_button")
            self.action_ele.click_element("std2_admin_system_hybrid_sync_now_button")

        except Exception as e:
            print(e.message)
            return False

        return True

    def sync_data_between_STD2_Boss(self):
        """
        `Description:` This API will click on sync now button which will sync the data b/w D2 and Boss
        `parameter:` None
        `Created by:` Priyanka
        """
        # Steps:
        # 1. Click on Sync Now button
        # 2. return Synced or not

        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            synced=False
            self.action_ele.explicit_wait("std2_admin_system_hybrid_sync_now_button")
            self.action_ele.click_element("std2_admin_system_hybrid_sync_now_button")
            time.sleep(3)
            synced = True

        except (Exception) as err:
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return synced		