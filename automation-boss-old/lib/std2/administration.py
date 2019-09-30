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


#####
# Start: Pages under Administration->Users
#####
class UsersUsersPage(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)

    def switch_page(self):
        # Switch to the Users/Users page
        self.action_ele.explicit_wait("std2_admin_users_users")
        self.action_ele.click_element("std2_admin_users_users")
        time.sleep(5)


class UsersPage(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.users = UsersUsersPage(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Users": self.users.switch_page})

    def switch_page(self, page):
        # Switch to the Administration/Users page
        self.action_ele.explicit_wait("std2_admin_users")
        self.action_ele.click_element("std2_admin_users")
        time.sleep(5)

        # Check if required to traverse down the path
        if page:
            fun = self.page_methods.get(page[0], None)
            if fun:
                fun()
            else:
                raise AssertionError("The function is not defined")
#####
# End: Pages under Administration->Users
#####

#####
# Start: Pages under Administration->System
#####


class Synchronization(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)

    def switch_page(self):
        # Switch to the Administration/System/Hybrid/Synchronization page
        self.action_ele.explicit_wait("std2_admin_system_hybrid_sync")
        self.action_ele.click_element("std2_admin_system_hybrid_sync")
        time.sleep(5)


class Services(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()

    def switch_page(self):
        # Switch to the Administration/System/Hybrid/Services page
        self.action_ele.explicit_wait("std2_admin_system_hybrid_services")
        self.action_ele.click_element("std2_admin_system_hybrid_services")
        time.sleep(5)


class Hybrid(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.services = Services(browser)
        self.sync = Synchronization(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Services": self.services.switch_page,
                                  "Synchronization": self.sync.switch_page})

    def switch_page(self, pages):
        # Switch to the Administration/System/Hybrid page
        self.action_ele.explicit_wait("std2_admin_system_hybrid")
        self.action_ele.click_element("std2_admin_system_hybrid")
        time.sleep(5)

        # Check if required to traverse down the path
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun()
            else:
                raise AssertionError("The function is not defined")


class System(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.hybrid = Hybrid(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Hybrid": self.hybrid.switch_page})

    def switch_page(self, pages):
        # Switch to the Administration/System page
        self.action_ele.explicit_wait("std2_admin_system")
        self.action_ele.click_element("std2_admin_system")
        time.sleep(5)

        # Check if required to traverse down the path
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun(pages[1:])
            else:
                raise AssertionError("The function is not defined")
#####
# End: Pages under Administration->System
#####


class CallControlBCAPage(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()

    def switch_page(self):
        # Switch to the Features/CallControl/BCA Page
        self.action_ele.explicit_wait("std2_features_callcontrol_BCA")
        self.action_ele.click_element("std2_features_callcontrol_BCA")
        time.sleep(5)


class FeaturesCallControlPage(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.bca = CallControlBCAPage(browser)
        self.register_page_methods()
    
    def register_page_methods(self):
        self.page_methods.update({"BridgedCallAppearances": self.bca.switch_page})

    def switch_page(self, page):
        # Switch to the Administration/Features/CallControl page
        self.action_ele.explicit_wait("std2_features_call_control")
        self.action_ele.click_element("std2_features_call_control")
        #time.sleep(5)

        # Check if required to traverse down the path
        if page:
            fun = self.page_methods.get(page[0], None)
            if fun:
                fun()
            else:
                raise AssertionError("The function FeaturesCallControlPage->switchpage is not defined")


class FeaturesPage(CommonHandles):
    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.call_control = FeaturesCallControlPage(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"CallControl": self.call_control.switch_page})

    def switch_page(self, page):
        # Switch to the Administration/Users page
        self.action_ele.explicit_wait("std2_features")
        time.sleep(1)
        self.action_ele.click_element("std2_features")
        time.sleep(1)

        # Check if required to traverse down the path
        if page:
            fun = self.page_methods.get(page[0], None)
            if fun:
                fun(page[1:])
            else:
                raise AssertionError("The function featurepage->switchpage is not defined")

#####
# End: Pages under Administration->Features
#####


class AdministrationPage(CommonHandles):

    def __init__(self, browser):
        CommonHandles.__init__(self, browser)
        self.page_methods = dict()
        self.users = UsersPage(browser)
        self.features = FeaturesPage(browser)
        self.system = System(browser)
        self.register_page_methods()

    def register_page_methods(self):
        self.page_methods.update({"Users": self.users.switch_page,
                                  "System": self.system.switch_page,
                                  "Features": self.features.switch_page})

    def switch_page(self, pages):
        # Switch to the Administration page
        self._browser._browser.refresh()
        self.action_ele.explicit_wait("std2_admin")
        self.action_ele.click_element("std2_admin")
        time.sleep(5)

        # Check if required to traverse down the path
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun(pages[1:])
            else:
                raise AssertionError("The function is not defined")




