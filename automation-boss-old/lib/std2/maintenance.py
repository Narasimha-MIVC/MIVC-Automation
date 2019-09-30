"""
STD2 component functionalities
Author: Prasanna Tripathy
"""
import os
import sys
import time

import stafenv

from web_wrappers.selenium_wrappers import LocalBrowser
from web_wrappers import selenium_wrappers as base

from commonhandles import CommonHandles


####
# Start ...
# Topology page under Maintenance
# Maintenance -> Topology
####


class TopologyPage(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()

    def switch_page(self, page):
        # Switch to the Maintenance/Topology page
        self.action_ele.explicit_wait("std2_maintenance_topology")
        self.action_ele.click_element("std2_maintenance_topology")
        time.sleep(5)
####
# Topology page under Maintenance
# Maintenance -> Topology
# ... End
####

####
# Start ...
# Topology page under Maintenance
# Maintenance -> Topology
####


class Services(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)

    def switch_page(self, pages):
        # Switch to the Maintenance/Hybrid/Services page
        self.action_ele.explicit_wait("std2_maintenance_hybrid_services")
        self.action_ele.click_element("std2_maintenance_hybrid_services")
        time.sleep(5)


class Users(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)

    def switch_page(self, pages):
        # Switch to the Maintenance/Hybrid/Data/Users page
        self.action_ele.explicit_wait("std2_maintenance_hybrid_data_users")
        self.action_ele.click_element("std2_maintenance_hybrid_data_users")
        time.sleep(5)


class Data(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.users = Users(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Users": self.users.switch_page})

    def switch_page(self, pages):
        # Switch to the Maintenance page
        self.action_ele.explicit_wait("std2_maintenance_hybrid_data")
        self.action_ele.click_element("std2_maintenance_hybrid_data")
        time.sleep(5)

        # Check if required to traverse down the path
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun(pages[1:])
            else:
                raise AssertionError("The function is not defined")


class Hybrid(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.services = Services(browser)
        self.data = Data(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Services": self.services.switch_page,
                                  "Data": self.data.switch_page})

    def switch_page(self, pages):
        # Switch to the Maintenance page
        self.action_ele.explicit_wait("std2_maintenance_hybrid")
        self.action_ele.click_element("std2_maintenance_hybrid")
        time.sleep(5)

        # Check if required to traverse down the path
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun(pages[1:])
            else:
                raise AssertionError("The function is not defined")

####
# Topology page under Maintenance
# Maintenance -> Topology
# ... End
####


class MaintenancePage(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.topology = TopologyPage(browser)
        self.hybrid = Hybrid(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Topology": self.topology.switch_page,
                                  "Hybrid": self.hybrid.switch_page})

    def switch_page(self, pages):
        # Switch to the Maintenance page
        self.action_ele.explicit_wait("std2_maintenance")
        self.action_ele.click_element("std2_maintenance")
        time.sleep(5)

        # Check if required to traverse down the path
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun(pages[1:])
            else:
                raise AssertionError("The function is not defined")




