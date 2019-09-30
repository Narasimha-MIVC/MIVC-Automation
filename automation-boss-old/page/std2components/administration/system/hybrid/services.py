"""Module for verifying the status of Hybrid Services
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


class Services(object):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        # self._browser = args[0]
        self.action_elm = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def verify_hybrid_services_status(self, hybrid_services_status):
        """
            `Description:` This API will verify the status of different hybrid services status
            `Param1:` hybrid_services_status: Expected status of the hybrid services
            `Created by:` Prasanna
        """
        # Steps:
        # 1. get the services info from the grid.
        # 2. verify the status of different hybrid services
        # 3. return status
        status = False

        total_services = len(hybrid_services_status.keys())

        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

            self.action_elm.explicit_wait("std2_admin_system_hybrid_services_title")
            page_title = self._browser.element_finder("std2_admin_system_hybrid_services_title")
            if page_title.text != "Hybrid Services":
                raise Exception("The required page is not available")

            # get the table entries
            self.action_elm.explicit_wait("std2_admin_system_hybrid_services_table")
            grid_table = self._browser.element_finder("std2_admin_system_hybrid_services_table")
            if grid_table:
                # Get the rows
                grid_table_rows = grid_table.find_elements_by_tag_name('tr')

                if grid_table_rows and len(grid_table_rows) > 1:
                    for element in grid_table_rows[1:]:
                        status = False
                        columns = element.find_elements_by_tag_name("td")
                        if columns and total_services:
                            for val in hybrid_services_status.values():
                                if columns[1].text == val["name"] and columns[2].text == val["status"]:
                                    status = True
                                    total_services = total_services - 1
                                    if not total_services: return status

        except Exception as e:
            print(e.message)

        return status

