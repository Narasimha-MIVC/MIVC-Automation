"""Module for execution of common portal functionalities such as login, log out, account switch etc
   File: CommonFunctionality.py
   Author: Kenash Kanakaraj @ Modified by Gopal
"""

import os
import sys
import time

#For console logs while executing ROBOT scripts
from robot.api.logger import console

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
import web_wrappers.selenium_wrappers as base
from mapMgr import mapMgr
from log import log
from selenium.webdriver import ActionChains

__author__ = "Kenash Kanakaraj"

mapMgr.create_maplist("PbxComponent")
mapDict = mapMgr.getMapDict()

_RETRY_COUNT = 3

class CommonFunctionality(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def open_url(self, url):
        """
        To open BOSS portal.
        :param url: URL of BOSS Page
        :return:
        """
        try:
            self._browser.go_to(url)
            log.mjLog.LogReporter("CommonFunctionality", "info", "Open URL successful")
        except Exception as e:
            raise e

    def client_login(self, username, password, **options):
        """Login for BOSS portal

        :param username: User email address
        :param password: user password
        :param options:
        :return:
        """
        try:
            print "Debug: enter client_log-in"
            status=False
            print "username %s" %username
            print "password %s" %password
            self.action_ele.clear_input_text("LoginUserName")
            self.action_ele.clear_input_text("LoginPassword")
            self.action_ele.input_text("LoginUserName", username)
            self.action_ele.input_text("LoginPassword", password)
            self.action_ele.click_element("LoginSubmit")
            time.sleep(2)
            status=True
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise err
        return status

    def client_login_BOSS(self, username, password, **options):
        """Login for BOSS portal

        :param username: User email address
        :param password: user password
        :param options:
        :return:
        """
        try:
            print "Debug: enter client_log-in"
            status=False
            print "username %s" %username
            print "password %s" %password
            self.action_ele.clear_input_text("LoginUserName1")
            self.action_ele.clear_input_text("LoginPassword1")
            self.action_ele.input_text("LoginUserName1", username)
            self.action_ele.input_text("LoginPassword1", password)
            self.action_ele.click_element("LoginSubmit1")
            time.sleep(2)
            status=True
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise err
        return status

    def close_browser(self):
        """Close the browser object

        :param driver: WebDriver object
        :return:
        """
        time.sleep(2)
        self._browser.quit()

    def switch_page(self, **params):
        """
        To switch to other pages based on given name
        :param params: name page which need to be switch
        :return:
        """
        try:
            self.action_ele.execute_javascript("scroll(250, 0)");
            print("IN COMMON SWITCH")
            print(params)
            getattr(self, "switch_page_" + params['page'])(params)
        except Exception as err:
            print(err.message)


    def switch_page_Phone_System(self, params):
        """
        switch to phone system page
        """
        self.action_ele.click_element("Phone_system_tab")
        self.action_ele.explicit_wait("call_recording")
        self.action_ele.click_element("call_recording")
