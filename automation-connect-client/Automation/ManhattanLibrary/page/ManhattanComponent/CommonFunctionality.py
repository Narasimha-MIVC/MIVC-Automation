## Module: Login
## File name: Login.py
## Description: This class contains the common operations like login,logout etc
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 18 AUG 2014  Jahnavi-844             Initial Version
###############################################################################
# Python Modules
import sys
import time

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class CommonFunctionality:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.assertElement = AssertElement(self._browser)
        self.queryElement = QueryElement(self._browser)

    def first_time_user_login(self, hqIP):
        '''
        first_time_user_login() - when user login to MHClient has to give server IP
        parameter: choice
        ex: choice==yes means entering server and press login button
            choice==no 
        '''
        try:
            self.webAction.input_text("Login_Server_text", hqIP)
            # self.webAction.click_element("Login_Login_Button_server")
            time.sleep(5)
            # print("clicked login button")
            log.mjLog.LogReporter("CommonFunctionality", "info",
                                  "first_time_user_login - Successfully entered HQ Server IP Address")
        except:
            log.mjLog.LogReporter("CommonFunctionality", "info",
                                  "first_time_user_login - error while entering HQ Server IP Address" + str(
                                      sys.exc_info()))
            raise

    def login_ctrlf12(self, username, password, server, save_password, domain=""):
        """
        login_ctrlf12() : Enters user name, password, domain, server IP and save password for login to connect client
        Parameters: username, password, server, save_password and domain
        """
        try:
            self.webAction.input_text("Login_Email", username)
            self.webAction.input_text("Login_Password", password)
            time.sleep(2)
            self.webAction.click_element('Login_show_advanced_options')
            time.sleep(1)
            self.webAction.input_text("Login_ctrlf12_server", server)

            if save_password.lower() == "yes":
                self.webAction.select_checkbox("login_ctrlf12_save_pwd")
            # else:
            #     self.webAction.unselect_checkbox("login_ctrlf12_save_pwd")
            if domain:
                self.webAction.input_text("Login_ctrlf12_domain", domain)
            self.webAction.click_element("Login_Login_Button_server")
            log.mjLog.LogReporter("CommonFunctionality", "info", "login_ctrlf12 - Trying"
                                                                 " to login using %s and %s" % (username, password))
        except:
            log.mjLog.LogReporter("CommonFunctionality", "error", "login_ctrlf12 - Login"
                                                                  " Failed using %s and %s" % (username, password))
            raise

    def login(self, username, password, server_address):
        '''
            enter user name and password and click on login
        '''
        try:
            log.mjLog.LogReporter("CommonFunctionality", "info", "Login - Trying to login " \
                                                                 "using %s and %s" % (username, password))

            self.webAction.clear_input_text_new("Login_Email")
            self.webAction.double_click_element("Login_Email")
            self.webAction.input_text_basic("Login_Email", username)
            self.webAction.double_click_element("Login_Password")
            self.webAction.input_text_basic("Login_Password", password)
            self.webAction.explicit_wait('Login_show_advanced_options')
            self.webAction.click_element('Login_show_advanced_options')
            self.webAction.explicit_wait('Login_ctrlf12_server')
            self.webAction.double_click_element("Login_ctrlf12_server")
            self.webAction.input_text_basic("Login_ctrlf12_server", server_address)
            
            #click the login button
            self.webAction.click_element("Login_Login")
            log.mjLog.LogReporter("CommonFunctionality", "info", "login- Trying to login " \
                                                                 "using %s and %s" % (username, password))
        except:
            log.mjLog.LogReporter("CommonFunctionality", "error", "login - LoginFailed ",
                                  "using %s and %s" % (username, password))
            raise
