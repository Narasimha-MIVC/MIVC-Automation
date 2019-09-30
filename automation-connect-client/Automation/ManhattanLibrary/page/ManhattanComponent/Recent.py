## Module: Recent
## File name: Recent.py
## Description: This class contains APIs related to Recent panel
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date                Engineer              Description
##  ---------       --------------      -----------------------
## 19 MAY 2017          UKumar             Initial Version
###############################################################################

# Python Modules
import sys
from selenium.webdriver.common.action_chains import ActionChains
import time
from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class Recent:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)

    def verify_recent_panel(self, option):
        """
        Author: UKumar
        verify_recent_panel() - Verifies that second panel, Recent tab is opened or not
        Parameters: option
        """
        try:

            status = self.queryElement.element_not_displayed("Recent_all_tab")
            if not status and option == "present":
                log.mjLog.LogReporter("Recent", "info", " verify_recent_panel"
                                                             " - Recent panel is opened")
            elif not status and option == "absent":
                raise AssertionError("Recent panel is opened")
            elif status and option == "absent":
                log.mjLog.LogReporter("Recent", "info", " verify_recent_panel"
                                                             " - Recent panel is not opened")
            else:
                raise AssertionError("Recent panel is not opened")
        except:
            log.mjLog.LogReporter("Recent", "info", " verify_recent_panel -"
                                                         "failed to verify Recent panel " + str(sys.exc_info()))
            raise

    def call_double_click_recent_entry(self, name):
        """
        Author : UKumar
        call_double_click_recent_entry(): Double click on an entry in Recent to make call
        Parameter: name
        """
        try:
            contact_list = self._browser.elements_finder("recent_history_name")
            for contact in contact_list:
                if name in contact.text.strip():
                    ActionChains(self._browser.get_current_browser()).double_click(contact).perform()
                    log.mjLog.LogReporter("Recent", "info", "call_double_click_recent_entry - Double clicked on entry for making call")
                    break
        except:
            log.mjLog.LogReporter("Recent", "error",
                                  "call_double_click_recent_entry - failed to double click on recent entry" + str(sys.exc_info()))
            raise

    def call_click_number_recent_entry(self, name="noname"):
        """
        Author : UKumar
        call_click_number_recent_entry(): Click on a number in an entry in Recent to make call
        Parameter: name
        """
        try:            
            contact_list = self._browser.elements_finder("recent_history_name")
            time.sleep(1)            
            number_list = self._browser.elements_finder("recent_history_number")
            time.sleep(1)            
            first_number = self._browser.elements_finder("recent_history_first_number")
            time.sleep(1)           
            if name == "noname":                
                first_number[0].click()
            else:
                for i, contact in enumerate(contact_list):
                    if name in contact.text.strip():
                        number_list[i].click()
                        log.mjLog.LogReporter("Recent", "info", "call_click_number_recent_entry - clicked on number for making call")
                        break
        except:
            log.mjLog.LogReporter("Recent", "error", "call_click_number_recent_entry -"
                                                     " failed to click on number to make call " + str(sys.exc_info()))
            raise
