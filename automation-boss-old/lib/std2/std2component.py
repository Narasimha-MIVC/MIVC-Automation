"""
STD2 component functionalities
Author: Prasanna Tripathy
"""
import os
import sys
import time

import stafenv

from web_wrappers.selenium_wrappers import LocalBrowser
from page.std2components import STD2Pages

from commonhandles import CommonHandles

# import from individual pages
from administration import AdministrationPage as admin
from maintenance import MaintenancePage as maintenance


class Std2Component(CommonHandles, STD2Pages):

    def __init__(self, *args, **kwargs):

        self._browser = args[0]
        CommonHandles.__init__(self, self._browser)
        self.page_methods = dict()
        # Initializing the page objects
        STD2Pages.__init__(self, self._browser)
        # each page objects
        self.admin = admin(self._browser)
        self.maintenance = maintenance(self._browser)
        # Registering the methods to navigate inside each page
        self.register_page_methods()

    def register_page_methods(self):
        """
        The method will populate the methods to navigate to each page
        """
        self.page_methods.update({"Administration": self.admin.switch_page,
                                  "Maintenance": self.maintenance.switch_page})

    def switch_to_page(self, page_path):
        pages = page_path.split('/')
        if pages:
            fun = self.page_methods.get(pages[0], None)
            if fun:
                fun(pages[1:])
            else:
                raise AssertionError("The function is not defined")


    def refresh_browser(self):
        """
        `Description:`  This function will refresh the browser
        """
        try:
            self._browser._browser.refresh()
            time.sleep(3)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

