## Module: WorkGroup
## File name: WorkGroup.py
## Description: This class contains workgroup related APIs
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 11 FEB 2015  Uttam-858             Initial Version
###############################################################################

# Python Modules
import sys

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class WorkGroup:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def check_wk_notification(self, present):
        """
        Author: Uttam
        check_wk_notification() : This method checks for WorkGroup
                                  notification in dashboard
        Parameter: present
        Extra Info: present=yes for present
                    present=no for absent
        """
        try:
            if present == "yes":
                self.webAction.explicit_wait("default_WK_notify")
                self.assertElement.page_should_contain_element("default_WK_notify")
                log.mjLog.LogReporter("WorkGroup", "info", "check_wk_notification"
                                      " - WorkGroup notification is present")
            else:
                if self.queryElement.element_not_displayed("default_WK_notify"):
                    log.mjLog.LogReporter("WorkGroup", "info", "check_wk_notification"
                                          " - WorkGroup notification is not present")
        except:
            log.mjLog.LogReporter("WorkGroup", "error", "check_wk_notification"
                                  " - Failed to check WK notification "+str(sys.exc_info()))
            raise AssertionError("error while checking workgroup notification")
        
    def check_wk_attributes(self, **params):
        """
        Author: Uttam
        check_wk_attributes() - This method checks various
                                attributes of a workGroup
        Parameters: workGroupName
        """
        try:
            if self.queryElement.element_not_displayed("WK_Login_button"):
                return False
            self.assertElement.page_should_contain_element("WK_Login_button")
            self.webAction.click_element("WK_Login_button")
            self.assertElement.page_should_contain_text(params["workGroupName"])
            log.mjLog.LogReporter("WorkGroup", "info", "check_wk_attributes"
                                  " - WorkGroup attributes checked")
        except:
            log.mjLog.LogReporter("WorkGroup", "error", "check_wk_attributes"
                                  " - Failed to check WK attributes "+str(sys.exc_info()))
            raise AssertionError("error while checking workgroup attributes")

    def check_call_attributes(self):
        """
        Author: Uttam
        check_call_attributes() - This method clicks on queued calls
                                  and checks for various attributes
        Parameters:
        """
        try:
            self.webAction.click_element("WK_name_calls")
            self.webAction.click_element("WK_name_wait_button")
            self.assertElement.page_should_contain_text(callerName)
            self.assertElement.page_should_not_contain_text(callerExt)
            log.mjLog.LogReporter("WorkGroup", "info", "check_call_attributes"
                                  " - call attributes checked")
        except:
            log.mjLog.LogReporter("WorkGroup", "error", "check_call_attributes"
                                  " - Failed to check call attributes "+str(sys.exc_info()))
            raise AssertionError("error while checking call attributes in WK")
        
    def handle_call_vms(self):
        """
        Author: Uttam
        handle_call_vms() - This method checks various
                                attributes of a workGroup
        Parameters: 
        """
        try:
           
            log.mjLog.LogReporter("WorkGroup", "info", "handle_call_vms"
                                  " - WorkGroup attributes checked")
        except:
            log.mjLog.LogReporter("WorkGroup", "error", "handle_call_vms"
                                  " - Failed to check WK attributes "+str(sys.exc_info()))
            raise AssertionError("error while checking workgroup attributes")
            
    def check_wk_attributes_logout(self):
        """
        author:kalyan
        check_wk_attributes_logout() - This method checks various attributes of a workGroup and logging out the workgroup
        Parameters: workGroupName
        """
        try:
            if self.queryElement.element_not_displayed("WK_logout_button"):
                return False
            self.assertElement.page_should_contain_element("WK_logout_button")
            self.webAction.click_element("WK_logout_button")
            log.mjLog.LogReporter("WorkGroup", "info", "check_wk_attributes"
                                  " - WorkGroup attributes checked and workgroup is logged out")
        except:
            log.mjLog.LogReporter("WorkGroup", "error", "check_wk_attributes"
                                  " - Failed to check WK attributes and workgroup is not logged out "+str(sys.exc_info()))
            raise AssertionError("error while checking workgroup attributes and workgroup log out")
