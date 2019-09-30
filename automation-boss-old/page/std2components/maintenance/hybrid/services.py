"""Module for verifying the status of Maintenance -> Hybrid -> Services
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
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def verify_hybrid_services_activation_status_and_active_users(self, hybrid_services_status):
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

            self.action_ele.explicit_wait("std2_maintenance_hybrid_services_title")
            page_title = self._browser.element_finder("std2_maintenance_hybrid_services_title")
            if page_title.text != "Services":
                raise Exception("The required page is not available")

            # get the table entries
            self.action_ele.explicit_wait("std2_maintenance_hybrid_services_table")
            grid_table = self._browser.element_finder("std2_maintenance_hybrid_services_table")
            if grid_table:
                # Get the rows
                grid_table_rows = grid_table.find_elements_by_tag_name('tr')
                if grid_table_rows and len(grid_table_rows) > 1:
                    for element in grid_table_rows[1:]:
                        status = False
                        columns = element.find_elements_by_tag_name("td")
                        if columns and total_services:
                            for val in hybrid_services_status.values():
                                if columns[0].text == val["name"]:
                                    if val["activated"]:
                                        if columns[1].find_element_by_tag_name("input").is_selected():
                                            status = True
                                    else:
                                        try:
                                            if columns[1].find_element_by_tag_name("input").is_selected():
                                                pass
                                        except:
                                            status = True
                                    if status:
                                        total_services = total_services - 1
                                        if not total_services:
                                            return status
                                    break
                            else:
                                return False

        except Exception as e:
            print(e.message)
            status = False

        return status

