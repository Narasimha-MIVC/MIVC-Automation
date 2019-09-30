"""Module for execution of Add on Feature functionalities
   File: AddonFeature.py
   Author: Megha Bansal
"""

import os
import sys
import pdb
import time
import imaplib
import time, re
import email
import datetime
from time import gmtime, strftime
from collections import defaultdict
import inspect
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# For console logs while executing ROBOT scripts
from robot.api.logger import console
from lib import select_from_dropdown as SFD

# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
# import base
import web_wrappers.selenium_wrappers as base
from lib import wait_in_loop as WIL

from log import log
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

__author__ = ""

_RETRY_COUNT = 3


class AddonFeature(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 10

    def add_globaluser_mobility(self, params):
        """
        `Description:` To add global user to mobility via add on features page

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """

        self.action_ele.explicit_wait("CosmoMobility_Grid")
        self.action_ele.click_element("CosmoMobility_Add")
        self.action_ele.explicit_wait("Add_grid")
        self.action_ele.explicit_wait("Addgrid_checkbox")
        if params['gu_name']:
            self.action_ele.clear_input_text("Addgrid_Name")
            self.action_ele.input_text("Addgrid_Name", params['gu_name'])

        self.action_ele.click_element("Addgrid_checkbox")
        self.action_ele.click_element("Addgrid_Next")
        time.sleep(2)

        self.action_ele.explicit_wait("Summary")
        self.action_ele.explicit_wait("Requestedby")
        self.action_ele.select_from_dropdown_using_index("Requestedby", 1)
        self.action_ele.explicit_wait("Requestedsources")
        self.action_ele.select_from_dropdown_using_index("Requestedsources", 1)
        self.action_ele.click_element("Addgrid_Finish")

        for i in range(self.counter):
            try:
                # okbutton = self._browser.element_finder("Click_Ok")
                # if okbutton.is_displayed():
                isDisplayed = self.query_ele.element_displayed("Click_Ok")
                if isDisplayed:
                    break
                else:
                    time.sleep(5)
            except:
                self._browser._browser.refresh()

        verify_success = self.query_ele.text_present("Mobility has been activated")
        if verify_success == False:
            verify_success = self.query_ele.text_present("Order has been created")
            if verify_success == False:
                return verify_success
            else:
                return True
        else:
            return True

    def provision_scribe_feature_to_user(self, params):
        """
        `Description:` To provision Connect scribe for user via add on features page

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        self.action_ele.click_element('Scribe_Manage')
        self.action_ele.explicit_wait("CosmoMobility_Grid")
        self.action_ele.click_element("CosmoScribeGridbtnAdd")
        self.action_ele.explicit_wait("Add_grid")
        self.action_ele.explicit_wait("Addgrid_checkbox")
        if params['userName']:
            self.action_ele.clear_input_text("Addgrid_Name")
            self.action_ele.input_text("Addgrid_Name", params['userName'])

        self.action_ele.click_element("Addgrid_checkbox")
        self.action_ele.clear_input_text("Addgrid_Name")
        self.action_ele.click_element("Addgrid_Next")
        time.sleep(2)
        self.action_ele.click_element("Addgrid_Next")

        self.action_ele.explicit_wait("Summary")
        time.sleep(1)
        self.action_ele.explicit_wait("Requestedby")
        self.action_ele.select_from_dropdown_using_index("Requestedby", 1)
        self.action_ele.explicit_wait("Requestedsources")
        self.action_ele.select_from_dropdown_using_index("Requestedsources", 1)
        self.action_ele.click_element("Addgrid_Finish")

        for i in range(self.counter):
            try:
                # okbutton = self._browser.element_finder("Click_Ok")
                # if okbutton.is_displayed():
                isDisplayed = self.query_ele.element_displayed("Click_Ok")
                if isDisplayed:
                    break
                else:
                    time.sleep(5)
            except:
                self._browser._browser.refresh()

        verify_success = self.query_ele.text_present("MiCloud Connect Scribe has been activated")
        if verify_success == False:
            verify_success = self.query_ele.text_present("Order has been created")
            if verify_success == False:
                return verify_success
            else:
                self.action_ele.click_element("Click_Ok")
                return True
        else:
            self.action_ele.click_element("Click_Ok")
            return True
			
    def add_on_feature_activate_shoretel_connect_hybrid(self):
        """
        The API will manage the connect scribe hybrid page
        :return:
        Created by: Prasanna
        """
        try:
            self.action_ele.explicit_wait("Add_On_Feature_ShoreTel_Connect_Hybrid")
            self.action_ele.click_element("Add_On_Feature_ShoreTel_Connect_Hybrid")
        except Exception as e:
            print(e.message)
            return False

        return True

    def add_on_feature_manage_connect_scribe_hybrid(self, params):
        """
        The API will manage the connect scribe hybrid page
        :return:
        Created by: Prasanna
        """
        status = True

        try:
            # 1. Click on the Manage button on the Add-On Feature page for connect scribe Hybrid
            # 2. Add users
            WIL(self.action_ele.click_element, "Add_On_Feature_Connect_Scribe_Hybrid_Manage")

            WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add")

            if params['SelectAll']:
                WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add_Select_All")
            elif params['Users']:
                for user in params['Users']:
                    WIL(self.action_ele.clear_input_text, "Add_On_Feature_Scribe_Add_Grid_Input_FullName")
                    WIL(self.action_ele.input_text, "Add_On_Feature_Scribe_Add_Grid_Input_FullName", user)
                    # select the element from the data grid
                    element = WIL(self._browser.element_finder, "Add_On_Feature_Scribe_Add_Grid", return_value=True)
                    if element:
                        row = element.find_elements_by_tag_name("div")
                        if not row:
                            raise Exception("no user element selected on grid")
                        row[1].click()
                    else:
                        raise Exception("Required user element not found on grid")
                else:
                    WIL(self.action_ele.clear_input_text, "Add_On_Feature_Scribe_Add_Grid_Input_FullName")
            else:
                # select the first user from the grid
                element = WIL(self._browser.element_finder, "Add_On_Feature_Scribe_Add_Grid", return_value=True)
                if element:
                    row = element.find_element_by_tag_name("div")
                    if not row:
                        raise Exception("no user element selected on grid")
                    # row[1].click()
                    columns = row.find_elements_by_tag_name("div")
                    if columns:
                        params.update({'Users': [columns[1].text]})
                        columns[0].click()
                else:
                    raise Exception("Required user element not found on grid")

            WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add_Next")

            WIL(self.action_ele.select_from_dropdown_using_text,
                "Add_On_Feature_Scribe_Add_Next_Req_By", params["Req_By"])
            WIL(self.action_ele.select_from_dropdown_using_text,
                "Add_On_Feature_Scribe_Add_Next_Req_Src", params["Req_Src"])

            # click on Terms and Conditions link
            current_window_handle = self._browser._browser.current_window_handle
            time.sleep(5)
            WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add_Next_TC_Link")
            time.sleep(3)
            # update the window handle
            windows_handles = self._browser._browser.window_handles
            self._browser._browser.switch_to.window(windows_handles[-1])
            # Close the tab
            self._browser._browser.close()
            self._browser._browser.switch_to.window(current_window_handle)
            time.sleep(3)

            WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add_Next_TC_Accept")

            WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add_Next_Finish")
            time.sleep(20)
            WIL(self.action_ele.click_element, "Add_On_Feature_Scribe_Add_Next_Finish_OK")

            WIL(self.action_ele.explicit_wait, "Add_On_Feature_Scribe_Manage_Page")

        except Exception as e:
            print(e.message)
            status = False

        return status

    def add_on_feature_activate_and_manage_cloud_hybrid_fax(self, params):
        """
        The API will activate the cloud hybrid Fax
        :return:
        """

        status = True

        try:
            
            try:
                # Check if the activate button is available. Return True if the button is not available
                self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Activate", waittime=5)
                self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Activate")

                # click the OK button
                self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_OK")
                self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_OK")
            except Exception as e:
                print(e.message)

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Manage")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Manage")

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Add")

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add_Page")
            time.sleep(2)

            if params['SelectAll']:
                self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add_Select_All")
                self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Add_Select_All")
            elif params['Users']:
                self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add_Grid_Input_FullName")
                for user in params['Users']:
                    self.action_ele.clear_input_text("Add_On_Feature_Fax_Hybrid_Add_Grid_Input_FullName")
                    self.action_ele.input_text("Add_On_Feature_Fax_Hybrid_Add_Grid_Input_FullName", user)
                    # select the element from the data grid
                    element = self._browser.element_finder("Add_On_Feature_Fax_Hybrid_Add_Grid")
                    if element:
                        row = element.find_elements_by_tag_name("div")
                        if not row:
                            raise Exception("no user element selected on grid")
                        row[1].click()
                    else:
                        raise Exception("Required user element not found on grid")
                else:
                    self.action_ele.clear_input_text("Add_On_Feature_Fax_Hybrid_Add_Grid_Input_FullName")
            else:
                # select the first user from the grid
                element = self._browser.element_finder("Add_On_Feature_Fax_Hybrid_Add_Grid")
                if element:
                    row = element.find_elements_by_tag_name("div")
                    if not row:
                        raise Exception("no user element selected on grid")
                    row[1].click()
                else:
                    raise Exception("Required user element not found on grid")

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add_Next")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Add_Next")
            time.sleep(2)
            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add_Next")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Add_Next")

            if params['FaxNumberSelectAll']:
                self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Numbers_Select_All")
                self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Numbers_Select_All")
            elif params['FaxNumbers']:
                self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Numbers_Grid_Input_Number")
                for num in params['FaxNumbers']:
                    self.action_ele.clear_input_text("Add_On_Feature_Fax_Hybrid_Numbers_Grid_Input_Number")
                    self.action_ele.input_text("Add_On_Feature_Fax_Hybrid_Numbers_Grid_Input_Number", num)
                    # select the element from the data grid
                    element = self._browser.element_finder("Add_On_Feature_Fax_Hybrid_Numbers_Grid")
                    if element:
                        row = element.find_elements_by_tag_name("div")
                        if not row:
                            raise Exception("no user element selected on grid")
                        row[1].click()
                    else:
                        raise Exception("Required user element not found on grid")
                else:
                    self.action_ele.clear_input_text("Add_On_Feature_Fax_Hybrid_Numbers_Grid_Input_Number")
            else:
                # select the first user from the grid
                element = self._browser.element_finder("Add_On_Feature_Fax_Hybrid_Numbers_Grid")
                if element:
                    row = element.find_elements_by_tag_name("div")
                    if not row:
                        raise Exception("no user element selected on grid")
                    row[1].click()
                else:
                    raise Exception("Required user element not found on grid")

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Add_Next")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Add_Next")

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Numbers_Next_Req_By")
            self.action_ele.select_from_dropdown_using_text(
                "Add_On_Feature_Fax_Hybrid_Numbers_Next_Req_By", params["Req_By"])
            self.action_ele.select_from_dropdown_using_text(
                "Add_On_Feature_Fax_Hybrid_Numbers_Next_Req_Src", params["Req_Src"])

            # click on Terms and Conditions link
            current_window_handle = self._browser._browser.current_window_handle
            time.sleep(5)
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Numbers_Next_TC_Link")
            time.sleep(3)
            # update the window handle
            windows_handles = self._browser._browser.window_handles
            self._browser._browser.switch_to.window(windows_handles[-1])
            # Close the tab
            self._browser._browser.close()
            self._browser._browser.switch_to.window(current_window_handle)
            time.sleep(3)

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Numbers_Next_TC_Accept")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Numbers_Next_TC_Accept")
            time.sleep(3)

            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Numbers_Next_Finish")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Numbers_Next_Finish")

            time.sleep(20)
            self.action_ele.explicit_wait("Add_On_Feature_Fax_Hybrid_Numbers_Next_Finish_OK")
            self.action_ele.click_element("Add_On_Feature_Fax_Hybrid_Numbers_Next_Finish_OK")
            time.sleep(5)

        except Exception as e:
            print(e.message)
            status = False

        # return True irrespective of the result
        return status

    def activate_connect_archiving(self, params):
        """
        Function to activate the 'Connect Archiving' add on feature
        :param params:
        :return:
        """
        status = True
        try:
            # click on the activate button
            # self.action_ele.explicit_wait("Activate_Connect_Archiving")
            WIL(self.action_ele.click_element, "Activate_Connect_Archiving")
            # chose the options on Archive settings wizard
            self.action_ele.explicit_wait("Archive_Settings")
            if params['Option'] == 'All' or params['Option'] == 'MiCloud Connect IM Archive':
                self.action_ele.click_element("MiCloud_Connect_IM_Archive")
            if params['Option'] == 'All' or params['Option'] == 'MiCloud Connect Call Recording Archive':
                self.action_ele.click_element("MiCloud_Connect_Call_Recording_Archive")
            if params['Option'] == 'All' or params['Option'] == 'MiCloud Connect Collaboration Archive':
                self.action_ele.click_element("MiCloud_Connect_Collaboration_Archive")

            # Click on next button
            self.action_ele.explicit_wait("Select_Archive_Next")
            self.action_ele.click_element("Select_Archive_Next")

            # Fill the details on the summary page before clicking Finish
            self.action_ele.explicit_wait("Select_Archive_Finish")
            cur_date = datetime.date.today()
            self.action_ele.input_text("Activation_Date", cur_date.strftime('%m/%d/%Y'))
            if params['Location']:
                self.action_ele.select_from_dropdown_using_text("Archive_Location", params['Location'])
            else:
                self.action_ele.select_from_dropdown_using_index("Archive_Location", 1)
            if params['RequestedBy']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Requested_By', params['RequestedBy'], loop_count=40)
                #self.action_ele.select_from_dropdown_using_text("Requested_By", params['RequestedBy'])
            else:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                    'Requested_By', 1, loop_count=40)
                #self.action_ele.select_from_dropdown_using_index("Requested_By", -1)
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'Request_Sources', params['RequestSource'], loop_count=40)
            #self.action_ele.select_from_dropdown_using_text("Request_Sources", params['RequestSource'])
            if params['RequestSource'] == 'Case':
                self.action_ele.input_text("Case_Number", params['CaseNumber'])
            self.action_ele.click_element("Select_Archive_Finish")

            time.sleep(5)

        except Exception as e:
            print(e)
            status = False

        return status

    def activate_connect_call_recording(self, params):
        """
        The function to activate connect call recording
        :param params:
        :return: True / False
        """
        status = True
        try:
            # click on the activate button
            WIL(self.action_ele.explicit_wait, "Activate_Connect_Call_Recording")
            self.action_ele.click_element("Activate_Connect_Call_Recording")
            time.sleep(4)
            # Fill the details in the settings page
            self.action_ele.explicit_wait("Call_Recording_Setting_Page")
            element = self._browser.element_finder("Call_Recording_Setting_Page")
            if element.text != "Connect Call Recording Settings":
                raise Exception("Page not opened")
            if params['RequestedBy']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Requested_By', params['RequestedBy'], loop_count=40)
                #self.action_ele.select_from_dropdown_using_text("Requested_By", params['RequestedBy'])
            else:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                    'Requested_By', 1, loop_count=40)
                #self.action_ele.select_from_dropdown_using_index("Requested_By", -1)
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'Request_Sources', params['RequestSource'], loop_count=40)
            #self.action_ele.select_from_dropdown_using_text("Request_Sources", params['RequestSource'])
            if params['RequestSource'] == 'Case':
                self.action_ele.input_text("Case_Number", params['CaseNumber'])

            self.action_ele.click_element("Update_Call_Recording_OK")

        except Exception as e:
            print(e)
            return False
        return status

    def activate_add_on_feature(self, params):
        """
        Generic API to activate the add on features
        :param params:
        :return: True / False
        """
        from collections import defaultdict
        params = defaultdict(lambda: '', params)
        status = False
        try:
            if params['add_on_feature'] == 'Connect Archiving':
                status = self.activate_connect_archiving(params)
            elif params['add_on_feature'] == 'Connect Call Recording':
                status = self.activate_connect_call_recording(params)
            # Add elif conditions for other Add on features
            else:
                pass
        except Exception as e:
            print(e)
            return False
        return status