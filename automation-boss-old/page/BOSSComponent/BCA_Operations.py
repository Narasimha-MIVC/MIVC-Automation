"""Module for creating and verifying BCA
   File: BCA_Operations.py
   Author: Prasanna
   Modified by: Immani Mahesh Kumar
"""

import os
import sys
import time
from web_wrappers import selenium_wrappers as base
from mapMgr import mapMgr
import inspect

from lib import wait_in_loop as WIL
from lib import select_from_dropdown as SFD

__author__ = "Prasanna"

# import log
# from distutils.util import strtobool
from collections import defaultdict
# from selenium import webdriver
# For console logs while executing ROBOT scripts
# from robot.api.logger import console
# import autoit
# import re

# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

mapMgr.create_maplist("BossComponent")
mapDict = mapMgr.getMapDict()
mapList = mapMgr.getMapKeyList()


class BossExceptionHandle(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Error Info: %s" % self.msg


class BCAOperations(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.INDEX = 1

        self.Extension = list()  # variable to retain the values of the default extensions(test case id: BCA0012)
        self.element_to_deselect = None
        self.bca = list()    # list of BCAs created..will be used for clean up at the beginning of Test cases

    # START --- function "clean-up"
    def clean_bca_suite(self, cleanAll=False):
        """
            `Description:` The function is used to clean up all the class level variables used in test cases
            This clean up function can be extended
            `Returns:` True / False
            `Created by:` Prasanna
        """
        del self.Extension[:]
        self.element_to_deselect = None

        # Cleaning up the BCA / aBCA which are not yet been deleted
        self.wait('phone_system_nav')
        self.action_ele.click_element('phone_system_nav')
        self.action_ele.click_element("Bridged_Call_Appearances")
        if not cleanAll:
            for bcainfo in self.bca:
                self.delete_bca(bcainfo)
                del bcainfo   # delete the dictionary
                time.sleep(5)
            del self.bca[:]   # Clean up the list
        else:
            # Clean all the bca in the grid
            self.delete_all_bca()

        self.action_ele.click_element("Account_Home_Page")
        time.sleep(3)

    # END --- function "clean-up"

    # START -- Function "wait"
    def wait(self, locator, wait_time=0, **kwargs):
        """
            `Description:` waiting function for an API to return
            `Param1:` locator: element locator on the web page
            `Param2:` wait_time: amount of time to wait before a timeout exception is raised
            `Created by:` Prasanna
        """
        if wait_time:
            if kwargs:
                status = self.action_ele.explicit_wait(locator, wait_time, **kwargs)
            else:
                status = self.action_ele.explicit_wait(locator, wait_time)
        else:
            if kwargs:
                status = self.action_ele.explicit_wait(locator, waittime=120, **kwargs)
            else:
                status = self.action_ele.explicit_wait(locator, waittime=120)
        if not status:
            print("Time expired")
            raise BossExceptionHandle("%s not active/enabled" % locator)
        time.sleep(1)

    # END -- Function "wait"

    # Start -- Function "click_ok_button"
    def click_ok_button(self):
        """
            `Description:` This function verifies the page contents before clicking on OK button.
            In case of Error mesage it throws an exception
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        WIL(self.wait, "BCA_OK_Button")
        try:
            self._browser.element_finder("BCA_Save_Success_Page_Title")
        except Exception as error:
            print(error.message)
            status = False
        WIL(self.action_ele.click_element, "BCA_OK_Button")
        # time.sleep(2)
        return status
    # End -- Function "click_ok_button"

    # Start --- Function "retain_bca_info"
    def retain_bca_info(self, params, operation):
        """
            `Description:` This function retains the BCA info for clean up purpose
            `Param1:` params: BCA info
            `Param2:` operation: operation type - Add/ copy
            `Created by:` Prasanna
        """
        bcainfo = dict()
        bcainfo["AssociatedBCA"] = None
        bcainfo["ProfileName"] = None
        bcainfo["PhoneNumber"] = params["SelectPhoneNumber"]
        bcainfo["Extension"] = params["Extension"]

        if not params["AssociatedBCA"]:
            if operation == "Add":
                bcainfo["ProfileName"] = params["ProfileName"]
            elif operation == "Copy":
                bcainfo["ProfileName"] = params["BcaCopyProfileName"]
        else:
            bcainfo["AssociatedBCA"] = True
            bcainfo["AssociatedBCAProfile"] = params["AssociatedBCAProfile"]

        self.bca.append(bcainfo)

    # End --- Function "retain_bca_info"

    # Start --- Function "handle_save_operation"
    def handle_save_operation(self, params, len_list):
        """
            `Description:` Handling of the save button in case of add / copy / edit BCA operations
            `Param1:` params: BCA info
            `Param2:` len_list: length of the list of phone numbers
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        i = 1
        while True:
            WIL(self.wait, "BCA_Save_Button")
            WIL(self.action_ele.click_element, "BCA_Save_Button")
            time.sleep(2)
            status = self.click_ok_button()
            if status:
                break
            elif i >= len_list:
                # cancel the operation
                WIL(self.wait, "BCA_Cancel_Button")
                WIL(self.action_ele.click_element, "BCA_Cancel_Button")
                WIL(self.wait, "BCA_OK_Button")
                WIL(self.action_ele.click_element, "BCA_OK_Button")

            elif not status:
                if not params["AssociatedBCA"]:
                    WIL(self.wait, "BCA_PhoneNumber")
                    WIL(self.action_ele.select_from_dropdown_using_index, "BCA_PhoneNumber", i)

                    params['SelectPhoneNumber'] = WIL(self.query_ele.get_text_of_selected_dropdown_option,
                                                               "BCA_PhoneNumber", return_value=True).strip()
                else:
                    WIL(self.wait, "A_BCA_Profile")
                    WIL(self.action_ele.select_from_dropdown_using_index, "A_BCA_Profile", i)
                    params['AssociatedBCAProfile'] = WIL(self.query_ele.get_text_of_selected_dropdown_option,
                                                                  "A_BCA_Profile", return_value=True).split("- ")[1]
                    params['SelectPhoneNumber'] = WIL(
                        # (self.query_ele.get_text_of_selected_dropdown_option("A_BCA_Profile")).split(" x")[0]
                        self.query_ele.get_text_of_selected_dropdown_option,
                        "A_BCA_Profile", return_value=True).split(" -")[0]
                i += 1

        return status
    # End --- Function "handle_save_operation"

    # Start of function --- "add_copy_edit_bca"
    def add_copy_edit_bca(self, params, operation):
        """
            `Description:` This function does add / copy / edit BCA or aBCA
            `Param1:` params: BCA / aBCA info
            `Param2:` operation: type of operation-- Add / Copy / Edit
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        len_list = 0
        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:

            if not params["AssociatedBCA"]:

                # In case of Edit Radio buttons, Profile Name and Extension fields are disabled
                if operation != "Edit":
                    if not params["CreateBcaUsingProgButton"]:
                        # self.wait("BCA_Radio_Button")
                        WIL(self.action_ele.select_radio_button, "BCA_Radio_Button")
                    elif params["VerifyRadioButton"]:   # verifying if BCA radio button is present
                        try:
                            self.wait("BCA_Radio_Button", 4)
                        except (Exception, BossExceptionHandle) as e:
                            print(e)
                            # self.wait('BCA_Cancel_Button')
                            WIL(self.action_ele.click_element, 'BCA_Cancel_Button')
                            # time.sleep(2)
                            # self.wait('BCA_Yes_Button')
                            WIL(self.action_ele.click_element, 'BCA_Yes_Button')
                            return False

                    # self.wait("BCA_Profile_Name")
                    if operation == "Add":
                        WIL(self.action_ele.input_text, "BCA_Profile_Name", params["ProfileName"])
                    else:
                        # For copy operation a different name
                        WIL(self.action_ele.input_text, "BCA_Profile_Name", params["BcaCopyProfileName"])

                # self.wait("BCA_Location")
                # self.action_ele.select_from_dropdown_using_text("BCA_Location", params['Location'])
                WIL(self.action_ele.select_from_dropdown_using_index, "BCA_Location", 0)
                params['Location'] = WIL(self.query_ele.get_text_of_selected_dropdown_option,
                                                  "BCA_Location", return_value=True)

                # Before adding Phone Number check the location intended by the test case
                if params['AssignFromLocation'] != "Don't assign a number":
                    # self.wait("BCA_Assign_PhoneNumber")
                    WIL(self.action_ele.select_from_dropdown_using_text,
                                 "BCA_Assign_PhoneNumber", params['AssignFromLocation'])

                    # Add the phone number if the test case needs

                    if params['SelectPhoneNumber']:
                        print("Phone Number: %s" % params['SelectPhoneNumber'])
                        if params['VerifyGlobalNo']:
                            ph_nums = WIL(self.query_ele.get_text_list_from_dropdown,
                                                   'BCA_PhoneNumber', return_value=True)
                            if ph_nums and params['SelectPhoneNumber'] not in ph_nums:
                                # self.wait('BCA_Cancel_Button')
                                WIL(self.action_ele.click_element, 'BCA_Cancel_Button')
                                # self.wait("BCA_Yes_Button")
                                # time.sleep(1)
                                WIL(self.action_ele.click_element, 'BCA_Yes_Button')
                                WIL(self.wait, 'Add_BCA_Button')
                                return True
                            else:
                                raise BossExceptionHandle("No Phone numbers in the list")

                        # self.wait("BCA_PhoneNumber")
                        WIL(self.action_ele.select_from_dropdown_using_text,
                                     "BCA_PhoneNumber", params['SelectPhoneNumber'])
                    else:
                        # Select the second available phone number from the drop down
                        WIL(self.action_ele.select_from_dropdown_using_index, "BCA_PhoneNumber", 0)
                        ph_number_list = WIL(self.query_ele.get_text_list_from_dropdown,
                                                      "BCA_PhoneNumber", return_value=True)
                        len_list = len(ph_number_list)

                    params['SelectPhoneNumber'] = WIL(self.query_ele.get_text_of_selected_dropdown_option,
                                                               "BCA_PhoneNumber", return_value=True).strip()

                    time.sleep(1)

                # In Edit operation Extension field is disabled
                if operation != "Edit":
                    # self.wait("BCA_Extension")
                    extn = WIL(self.query_ele.get_value, "BCA_Extension", return_value=True)
                    # Retain the extension
                    self.Extension.append(extn)
                    params['Extension'] = extn

                # Set the outbound caller Id only if required by the test case
                if params['OutboundCallerID']:
                    # self.wait("BCA_OutboundCallerIds")
                    if params['VerifyGlobalNo']:
                        ph_nums = WIL(self.query_ele.get_text_list_from_dropdown,
                                               'BCA_OutboundCallerIds', return_value=True)
                        if ph_nums and params['OutboundCallerID'] not in ph_nums:
                            print("Global number is not in outbound caller list")
                            # self.wait('BCA_Cancel_Button')
                            WIL(self.action_ele.click_element, 'BCA_Cancel_Button')
                            # self.wait("BCA_Yes_Button")
                            # time.sleep(1)
                            WIL(self.action_ele.click_element, 'BCA_Yes_Button')
                            WIL(self.wait, 'Add_BCA_Button')
                            return True
                        else:
                            raise BossExceptionHandle("Global outbound caller id in the list!!")

                    if params['OutboundCallerID'] == "Default":
                        # Select from the drop down
                        WIL(self.action_ele.select_from_dropdown_using_index, "BCA_OutboundCallerIds", 0)
                    else:
                        WIL(self.action_ele.select_from_dropdown_using_text,
                                     "BCA_OutboundCallerIds", params['OutboundCallerID'])

                # START -- other options
                if params['OtherSettings']:
                    # self.wait("BCA_Show_More_Option")
                    WIL(self.action_ele.click_element, "BCA_Show_More_Option")

                    # self.wait("BCA_Privacy_Check_Box")
                    privacy = WIL(self.action_ele.check_checkbox, "BCA_Privacy_Check_Box", return_value=True)
                    if params['Privacy']:
                        if not privacy:
                            # self.wait("BCA_Privacy_Check_Box")
                            WIL(self.action_ele.select_checkbox, "BCA_Privacy_Check_Box")
                    else:
                        if privacy:
                            # self.wait("BCA_Privacy_Check_Box")
                            WIL(self.action_ele.unselect_checkbox, "BCA_Privacy_Check_Box")

                    # self.wait("BCA_CFBusy")
                    WIL(self.action_ele.select_from_dropdown_using_text,
                                 "BCA_CFBusy", params['CallForwardBusy'])
                    if params['CallForwardBusyExtn']:
                        # self.wait("BCA_CFBusy_Extn")
                        WIL(self.action_ele.input_text, "BCA_CFBusy_Extn", params['CallForwardBusyExtn'])

                    # self.wait("BCA_CFNoAnswer")
                    WIL(self.action_ele.select_from_dropdown_using_text,
                                 "BCA_CFNoAnswer", params['CallForwardNoAnswer'])
                    if params['CallForwardNoAnswerExtn']:
                        # self.wait("BCA_CFNoAnswer_Extn")
                        WIL(self.action_ele.input_text, "BCA_CFNoAnswer_Extn", params['CallForwardNoAnswerExtn'])

                    # self.wait("BCA_Conf_Option")
                    WIL(self.action_ele.select_from_dropdown_using_text,
                                 "BCA_Conf_Option", params['ConferencingOptions'])

                    if params['ConferencingOptions'] != 'Disable Conferencing':
                        # self.wait("BCA_Enable_Tone")
                        enable_tone = WIL(self.action_ele.check_checkbox, "BCA_Enable_Tone", return_value=True)
                        if params['EnableToneWhenPartiesJoinOrLeave']:
                            if not enable_tone:
                                # self.wait("BCA_Enable_Tone")
                                WIL(self.action_ele.select_checkbox, "BCA_Enable_Tone")
                        else:
                            if enable_tone:
                                # self.wait("BCA_Enable_Tone")
                                WIL(self.action_ele.unselect_checkbox, "BCA_Enable_Tone")

                # END -- Other Options
            else:
                if operation != "Copy":
                    if operation != "Edit":
                        if not params["CreateBcaUsingProgButton"]:
                            # self.wait("Associated_BCA")
                            WIL(self.action_ele.select_radio_button, "Associated_BCA")
                        elif params["VerifyRadioButton"]:  # verifying if SCA radio button is present
                            try:
                                self.wait("Associated_BCA", 4)
                            except (Exception, BossExceptionHandle) as e:
                                print(e)
                                # self.wait('BCA_Cancel_Button')
                                WIL(self.action_ele.click_element, 'BCA_Cancel_Button')
                                # time.sleep(2)
                                # self.wait('BCA_Yes_Button')
                                WIL(self.action_ele.click_element, 'BCA_Yes_Button')
                                return False
                        if params['AssociatedBCAExtn']:
                            # self.wait("A_BCA_Extn")
                            WIL(self.action_ele.input_text, "A_BCA_Extn", params['AssociatedBCAExtn'])

                    self.wait("A_BCA_Profile")

                    if params['AssociatedBCAProfile']:
                        text = params['AssociatedBCAProfile']
                        if params["SelectPhoneNumber"]:
                            if params["duplicate_aBCAProfile"]:
                                text = params["SelectPhoneNumber"] + " " + \
                                       "-" + " " + params['duplicate_aBCAProfile']
                                abca_profile_list = WIL(self.query_ele.get_text_list_from_dropdown,
                                                        "A_BCA_Profile", return_value=True)
                                for profile in abca_profile_list:
                                    if profile == text:
                                        print "Already assigned profile is present in the drop down list"
                                        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                                        status = False
                                        self.wait("BCA_Cancel_Button")
                                        self.action_ele.click_element("BCA_Cancel_Button")
                                        self.wait("BCA_Yes_Button")
                                        time.sleep(1)
                                        self.action_ele.click_element("BCA_Yes_Button")
                                        time.sleep(2)
                                        raise BossExceptionHandle("Already assigned profile should not list in the aBCA drop down list, but it is listed")
                                else:
                                    print "Already assigned profile was removed from the drop down list as expected"
                                    status = True
                                    # Press the cancel button
                                    self.wait("BCA_Cancel_Button")
                                    self.action_ele.click_element("BCA_Cancel_Button")
                                    self.wait("BCA_Yes_Button")
                                    time.sleep(1)
                                    self.action_ele.click_element("BCA_Yes_Button")
                                    time.sleep(2)
                                    return status
                            text = params["SelectPhoneNumber"] + " " + \
                                   "x" + params["SelectPhoneNumber"][-4:] + " " + \
                                   "-" + " " + params['AssociatedBCAProfile']
                        print(text)
                        WIL(self.action_ele.select_from_dropdown_using_text, "A_BCA_Profile", text)
                    else:
                        # select the profile from the drop down
                        WIL(self.action_ele.select_from_dropdown_using_index, "A_BCA_Profile", 0)
                        # time.sleep(1)
                        abca_profile_list = WIL(self.query_ele.get_text_list_from_dropdown,
                                                         "A_BCA_Profile", return_value=True)
                        len_list = len(abca_profile_list)

                    params['AssociatedBCAProfile'] = WIL(self.query_ele.get_text_of_selected_dropdown_option,
                                                                  "A_BCA_Profile", return_value=True).split("- ")[1]
                    # Get the phone number or the extension part of the profile name
                    ph_num = WIL(self.query_ele.get_text_of_selected_dropdown_option,
                                          "A_BCA_Profile", return_value=True).split(" -")[0]
                    # if " x" in ph_num:
                    #     ph_num = ph_num.split(" x")[0]
                    # else:
                    #     ph_num = ph_num.split("x")[1]
                    params['SelectPhoneNumber'] = ph_num

                    params['Extension'] = WIL(self.query_ele.get_value, "A_BCA_Extn", return_value=True)

            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if not self.handle_save_operation(params, len_list):
                raise BossExceptionHandle("operation could not be saved")

            # retain BCA / aBCA details
            self.retain_bca_info(params, operation)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status
    # End of function --- "add_copy_edit_bca"

    # Start of function --- "get_abca_profile_name"
    def get_abca_profile_name(self, name):

        """
            `Description:` The API gets a particular profile name from the list of profile on Add aBCA page
            `Param1:` name: partial name string of the user profile
            `Returns:` True / False, The profile name
            `Created by:` Prasanna
        """
        status = True
        abca_profile = None
        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            self.wait("Associated_BCA")
            self.action_ele.select_radio_button("Associated_BCA")

            self.wait("A_BCA_Profile")
            # Get the string that contains the profile name
            profile_list = self.query_ele.get_text_list_from_dropdown("A_BCA_Profile")
            for abca_profile in profile_list:
                if name in abca_profile:
                    break
            else:
                raise BossExceptionHandle("Associated BCA Profile name not found!")

            self.wait("BCA_Cancel_Button", ec="element_to_be_clickable")
            time.sleep(1)
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(3)

            self.wait("BCA_Cancel_Page_Info", ec="visibility_of_element_located")

            self.wait("BCA_Yes_Button", ec="element_to_be_clickable")
            time.sleep(1)
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(3)
            self.wait("Add_BCA_Button", ec="visibility_of_element_located")

        except (Exception, BossExceptionHandle) as err:
            status = False
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status, abca_profile

    # End of function --- "get_abca_profile_name"

    # Start of function --- "select_bca_from_grid"
    def select_bca_from_grid(self, bca_name):

        """
            `Description:` The function selects the required BCA from the grid
            `Param1:` bca_name: name of the required BCA
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = False
        try:
            # Select the BCA from the Grid
            self.wait("BCA_Grid_Header_Row_Name")
            self.action_ele.input_text("BCA_Grid_Header_Row_Name", bca_name)
            time.sleep(1)

            # Retrieve the BCA info from the grid table. In this case only one
            self.wait("BCA_Grid_Canvas")
            grid_table_row = self._browser.element_finder("BCA_Grid_Canvas")
            if grid_table_row:
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('div')
                print("Number of columns: %s" % str(len(columns)))

                # check if the element is found
                if 0 != len(columns):
                    print("Profile Name: %s" % columns[2].text)
                    if columns[2].text == bca_name:
                        columns[1].click()
                        self.element_to_deselect = columns[1]
                        status = True

            time.sleep(2)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status
    # End of function --- "select_bca_from_grid"

    # START - Function "create_bca"
    def create_bca(self, params):

        """
            `Description:` This function creates new bca
            `Param1:` params: Dictionary containing information to create a new BCA
            `Returns:` True / False
            `Created by:` Prasanna
        """
        added = True
        try:
            self.wait("Add_BCA_Button", ec="element_to_be_clickable")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            status = self.add_copy_edit_bca(params, "Add")
            if not status:
                raise BossExceptionHandle("Adding BCA / aBCA failed")

        except (Exception, BossExceptionHandle) as err:
            added = False
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return added

    # End of function --- "create_bca"

    # Start of function --- "copy_bca"
    def copy_bca(self, params):

        """
            `Description:` The function copies a bca
            `Param1:` params: Dictionary containing BCA / aBCA info
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page
        copied = True

        if not params["AssociatedBCA"]:
            bca_profile_name = params["ProfileName"] + " BCA"
        else:
            bca_profile_name = params["ProfileName"] + " aBCA"

        print("BCA Profile name: %s" % bca_profile_name)

        try:

            # Select the BCA from the grid
            if not self.select_bca_from_grid(bca_profile_name):
                raise BossExceptionHandle("Selecting the required BCA from the grid failed")

            # Click on the copy button
            self.wait("Copy_BCA_Button")
            self.action_ele.click_element("Copy_BCA_Button")

            # Copy the BCA
            status = self.add_copy_edit_bca(params, "Copy")
            if not status:
                raise BossExceptionHandle("BCA / aBCA Copy operation failed")

        except (Exception, BossExceptionHandle) as e:
            print(e)
            copied = False
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return copied
    # End of function --- "copy_bca"

    # Start of function --- "edit_bca"
    def edit_bca(self, params):

        """
            `Description:` The function edits a BCA / aBCA
            `Param1:` params: Dictionary containing BCA / aBCA info
            `Returns:` True / False
            `Created by:` Prasanna
        """

        import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        # Assumption is that the control is already in BCA page
        edited = True

        if not params["AssociatedBCA"]:
            bca_profile_name = params["ProfileName"] + " BCA"
        else:
            bca_profile_name = params["ProfileName"] + " aBCA"

        print("BCA Profile name: %s" % bca_profile_name)

        try:

            # Select the BCA from the grid
            if not self.select_bca_from_grid(bca_profile_name):
                raise BossExceptionHandle("Selecting the required BCA from the grid failed")

            # Click on the copy button
            self.wait("Edit_BCA_Button")
            self.action_ele.click_element("Edit_BCA_Button")

            # Copy the BCA
            status = self.add_copy_edit_bca(params, "Edit")
            if not status:
                raise BossExceptionHandle("BCA / aBCA Edit operation failed")

        except (Exception, BossExceptionHandle) as e:
            print(e)
            edited = False
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return edited

    # End of function --- "edit_bca"

    # verify one BCA info
    def verify_bca(self, params):

        """
            `Description:` This function verifies the added/modified BCA or aBCA
            `Param1:` params: Dictionary containing information about the BCA / aBCA
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page
        params = defaultdict(lambda: "", params)

        verified = True
        if not params["AssociatedBCA"]:
            bca_profile_name = params["ProfileName"]+" BCA"
            bca_extn = params["Extension"]
        else:
            bca_profile_name = params["AssociatedBCAProfile"] + " aBCA"
            bca_extn = params["AssociatedBCAExtn"]

        print("BCA Profile name: %s" % bca_profile_name)

        try:
            # Select the BCA from the Grid
            # self.wait("BCA_Grid_Header_Row_Name")
            # self.action_ele.input_text("BCA_Grid_Header_Row_Name", bca_profile_name)
            WIL(self.action_ele.input_text, "BCA_Grid_Header_Row_Name", bca_profile_name, loop_count=40)
            time.sleep(1)

            # Retrieve the BCA info from the grid table. In this case only one
            #self.wait("BCA_Grid_Canvas")
            grid_table_row = WIL(self._browser.element_finder, "BCA_Grid_Canvas", return_value=True, loop_count=40)
            if grid_table_row:
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('div')
                print("Number of columns: %s" % str(len(columns)))

                # verify the columns
                if 0 != len(columns):
                    print("Expected Profile Name: {0}, Actual Profile Name: {1}".format(bca_profile_name, columns[2].text))
                    print("Expected Extension: {0}, Actual Extension: {1}".format(bca_extn, columns[3].text))
                    print("Expected Location: {0}, Actual Location: {1}".format(params["Location"], columns[5].text))
                    # Modified By: Prasanna - The location may be different and better to remove the check for location
                    # if ((columns[2].text != bca_profile_name) or
                    #         (params["Location"] and (columns[5].text != params["Location"]))):
                    if columns[2].text != bca_profile_name:
                        raise BossExceptionHandle("Verifying the BCA info failed")

                    # A special case of validation of default extension (test case id: BCA0012)
                    if ((bca_extn == "Validate Default Extension")
                            and (int(self.Extension[1]) != int(self.Extension[0])+1)):
                        raise BossExceptionHandle("Verifying default extension failed")
                    elif bca_extn and (bca_extn != columns[3].text):
                        print(bca_extn, columns[3].text)
                        raise BossExceptionHandle("Verifying extension failed")

            else:
                raise BossExceptionHandle("No element found on the grid")

        except (Exception, BossExceptionHandle) as err:
            verified = False
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        del self.Extension[:]

        return verified

    # End of function -- verify_bca

    # Retrieve the user phone number
    def retrieve_phone_number(self, param):

        """
            `Description:` This function retrieves a user phone number
            `Param1:` param: Name of the user
            `Returns:` True / False
            `Created by:` Prasanna
        """

        phone_number = None
        info_found = False

        try:
            self.action_ele.click_element('phone_system_nav')
            self.action_ele.click_element("Users_link")
            time.sleep(2)

            # get the user row from the grid
            self.action_ele.input_text("User_Page_HeaderRow_FullName", param)
            # self.action_ele.input_text("email_search", param)
            time.sleep(2)

            # Get the user info table
            user_grid_table = self._browser.element_finder("User_Grid_Canvas")
            if user_grid_table:
                # Get the fields
                columns = user_grid_table.find_elements_by_tag_name('div')
                # verify the columns and get the phone number assigned to the user
                if 0 != len(columns):
                    phone_number = columns[4].text
                    info_found = True

        except (Exception, BossExceptionHandle) as err:
            print("Retrieving the User Phone info failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        # Reset
        self.action_ele.input_text("User_Page_HeaderRow_FullName", "")
        # self.action_ele.input_text("email_search", "")
        time.sleep(1)

        return info_found, phone_number

    # End of "retrieve_phone_number"

    def verify_phone_status(self, ph_numbers, status):

        """
            `Description:` The function verifies the status of phone numbers
            This function is referred by the API "verify_phone_number"
            `Param1:` ph_numbers: Phone numbers
            `Param2:` status: Expected status of the phone numbers
            `Returns:` True / False
            `Created by:` Prasanna
        """
        self.wait("Ph_Number_Text_Box")
        # if self._browser.location == 'US':
        if len(ph_numbers) > 1:
            self.action_ele.input_text("Ph_Number_Text_Box", ph_numbers[0][:11])
        else:
            self.action_ele.input_text("Ph_Number_Text_Box", ph_numbers[0])
        # elif self._browser.location == 'UK':
        #    pass
        # else:   # For Australia
        #    pass
        time.sleep(2)

        # Get all the rows
        self.wait("Ph_Number_Data_Grid")
        ph_number_data_grid = self._browser.element_finder("Ph_Number_Data_Grid")
        if not ph_number_data_grid:
            raise BossExceptionHandle("No Element found with the locator")

        rows = ph_number_data_grid.find_elements_by_tag_name("tr")
        if len(rows) < len(ph_numbers):
            print(len(rows))
            raise BossExceptionHandle("Number of rows in the grid less then expected !")

        for i in range(len(ph_numbers)):
            found = False
            for j in range(len(rows)):
                columns = rows[j].find_elements_by_tag_name("td")
                if not columns:
                    print(len(columns))
                    raise BossExceptionHandle("Number of columns in the grid not as expected!")
                if (columns[1].text == ph_numbers[i]) and (columns[8].text == status):
                    found = True
                    break

            if not found:
                raise BossExceptionHandle("Phone status unavailable")

        return True

    # START -- function "verify_phone_number"
    def verify_phone_number(self, params):

        """
            `Description:` The API verifies the status of phone numbers
            `Param1:` params: Dictionary containing the phone numbers and the expected status
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = False
        numbers = list()

        try:
            if params['numberRange']:
                extns = int(params['range'])
                temp = int(params['numberRange'])
                numbers = list()
                for i in range(extns):
                    # This is only for US.
                    if self._browser.location == 'US':
                        ph_number = str(temp + i)
                        numbers.append(ph_number[0]+" ("+ph_number[1:4]+") "+ph_number[4:7]+"-"+ph_number[7:])
                    elif self._browser.location == 'UK':
                        pass
                    else:  # For Australia
                        pass
            else:
                for i in range(len(self.bca)):
                    if self.bca[i]["PhoneNumber"]:
                        numbers.append(self.bca[i]["PhoneNumber"])
                print("### phone numbers: ", numbers)

            if len(numbers):
                status = self.verify_phone_status(numbers, params["state"])

        except (Exception, BossExceptionHandle) as err:
            status = False
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status

    # End -- function "verify_phone_number"

    # Start -- function "verify_geo_location"
    def verify_geo_location(self, param):

        """
            `Description:` The API verifies a geographic location
            `Param1:` param: Geographic Location name
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            self.wait("Geo_Loc_HeaderRow_Label")
            self.action_ele.input_text("Geo_Loc_HeaderRow_Label", param)
            time.sleep(5)

            # Get all the rows
            self.wait("Geo_Loc_Grid_Canvas")
            geo_loc_data_grid = self._browser.element_finder("Geo_Loc_Grid_Canvas")
            if not geo_loc_data_grid:
                raise BossExceptionHandle("No Element found with the locator")

            rows = geo_loc_data_grid.find_elements_by_tag_name("div")
            if not len(rows):
                print(len(rows))
                raise BossExceptionHandle("Number of rows in the grid less then expected !")

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status
    # End -- function "verify_geo_location"

    # Deleting a BCA
    def delete_bca(self, params):
        """
            `Description:` This API deletes a BCA / aBCA
            `Param1:` params: Information about the BCA / aBCA
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Check if the Params is an empty dictionary then return True
        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        if not bool(params):
            return True

        params = defaultdict(lambda: "", params)

        # Assumption is that the control is already in BCA page
        deleted = False
        if not params["AssociatedBCA"]:
            bca_profile_name = params["ProfileName"] + " BCA"
        else:
            bca_profile_name = params["AssociatedBCAProfile"] + " aBCA"

        print("BCA Profile name: %s" % bca_profile_name)

        try:
            # Select the BCA from the Grid
            #self.wait("BCA_Grid_Header_Row_Name")

            WIL(self.action_ele.input_text,"BCA_Grid_Header_Row_Name", bca_profile_name, loop_count=30)
            time.sleep(1)

            # Retrieve the BCA info from the grid table. In this case only one
            # self.wait("BCA_Grid_Canvas")
            # grid_table_row = self._browser.element_finder("BCA_Grid_Canvas")
            grid_table_row = WIL(self._browser.element_finder,"BCA_Grid_Canvas", loop_count=40, return_value=True)
            if grid_table_row:
                row = grid_table_row.find_element_by_tag_name('div')
                if row:
                    # Get the fields
                    columns = row.find_elements_by_tag_name('div')
                    print("Number of columns: %s" % str(len(columns)))

                    # check if the element is found
                    if 0 != len(columns) and columns[1].text == bca_profile_name:
                        print("Profile Name: %s" % columns[1].text)
                        columns[0].click()
                        deleted = True

            time.sleep(2)
            # Delete the selected BCA
            if deleted:
                print("### Deleting the BCA")

                self.wait("Delete_BCA_Button")
                self.action_ele.click_element("Delete_BCA_Button")

                # verify the text on the delete manage page
                text = "Warning: This action will delete the selected " \
                       "bridged call appearance and any programming buttons that use it."
                # Get the text wrapped in <p> tag and compare it for the validation
                self.wait("BCA_Actions_Manage_Popup_Info")
                value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
                if text != value:
                    print(value)
                    raise BossExceptionHandle("Text in the page not as expected")

                time.sleep(2)
                self.wait("BCA_Yes_Button")
                self.action_ele.click_element("BCA_Yes_Button")
                time.sleep(3)

                text = "Bridged call appearance successfully deleted."
                # Get the text wrapped in <p> tag and compare it for the validation
                self.wait("BCA_Actions_Manage_Popup_Info")
                value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
                if text != value:
                    print(value)
                    raise BossExceptionHandle("Text in the page not as expected")

                self.wait("BCA_OK_Button")
                self.action_ele.click_element("BCA_OK_Button")

            time.sleep(3)

            """
            # Now again verify that the BCA entry is actually deleted
            # Select the BCA from the Grid
            self.wait("BCA_Grid_Header_Row_Name")
            self.action_ele.input_text("BCA_Grid_Header_Row_Name", bca_profile_name)
            time.sleep(2)

            # Retrieve the BCA info from the grid table. In this case only one
            self.wait("BCA_Grid_Canvas")
            grid_table_row = self._browser.element_finder("BCA_Grid_Canvas")
            if grid_table_row:
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('div')
                print("Number of columns: %s" % str(len(columns)))
                # check if the element is found
                if 0 != len(columns) and columns[2].text == bca_profile_name:
                    print("The BCA entry is not deleted from the BCA grid")
                    raise BossExceptionHandle("BCA item is not deleted !")
            """
        except (Exception, BossExceptionHandle) as err:
            deleted = False
            print("Deleting the BCA info failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return deleted

    # End of "delete_bca"

    # Deleting all the created BCAs
    def delete_all_bca(self):
        """
            `Description:` This API deletes all BCAs and aBCAs
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page
        deleted = False

        try:

            while True:
                # Retrieve the BCAs info from the grid table. In this case only one
                self.wait("BCA_Grid_Canvas")
                grid_table = self._browser.element_finder("BCA_Grid_Canvas")

                if grid_table:
                    grid_table_rows = grid_table.find_elements_by_tag_name('div')
                else:
                    raise BossExceptionHandle("No Rows in the grid table")

                if grid_table_rows:
                    grid_table_rows[1].click()
                    deleted = True
                    time.sleep(2)
                    # Delete the selected BCA
                    if deleted:
                        print("### Deleting the BCA")

                        self.wait("Delete_BCA_Button")
                        self.action_ele.click_element("Delete_BCA_Button")

                        # verify the text on the delete manage page
                        text = "Warning: This action will delete the selected " \
                               "bridged call appearance and any programming buttons that use it."
                        # Get the text wrapped in <p> tag and compare it for the validation
                        self.wait("BCA_Actions_Manage_Popup_Info")
                        value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
                        if text != value:
                            print(value)
                            raise BossExceptionHandle("Text in the page not as expected")

                        time.sleep(2)
                        self.wait("BCA_Yes_Button")
                        self.action_ele.click_element("BCA_Yes_Button")
                        time.sleep(3)

                        text = "Bridged call appearance successfully deleted."
                        # Get the text wrapped in <p> tag and compare it for the validation
                        self.wait("BCA_Actions_Manage_Popup_Info")
                        value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
                        if text != value:
                            print(value)
                            raise BossExceptionHandle("Text in the page not as expected")

                        self.wait("BCA_OK_Button")
                        self.action_ele.click_element("BCA_OK_Button")

                        time.sleep(3)
                        deleted = False
                else:
                    break

        except (Exception, BossExceptionHandle) as err:
            deleted = False
            print("Deleting the BCA info failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return deleted

    # End of "delete_bca"

    # START -- "verify_deletion_of_bca"
    def verify_deletion_of_bca(self, params):
        """
            `Description:` This API verifies the deletion of a BCA / aBCA
            `Param1:` params: Information about the BCA / aBCA
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = False
        try:
            # Verify Delete button without selecting a BCA
            text = "To remove a bridged call appearance, click the check box next to it."
            self.wait("Delete_BCA_Button")
            self.action_ele.click_element("Delete_BCA_Button")
            # Get the text wrapped in <p> tag and compare it for the validation
            self.wait("BCA_Actions_Manage_Popup_Info")
            value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
            if text != value:
                print(value)
                raise BossExceptionHandle("Text in the page not as expected")

            self.wait("BCA_OK_Button")
            self.action_ele.click_element("BCA_OK_Button")

            # Now verify delete with a BCA info

            status = self.delete_bca(params)

        except (Exception, BossExceptionHandle) as err:
            print(err.message)

        return status

    # END -- "verify_deletion_of_bca"

    # Start -- function "verify_bca_m5portal_bread_crumb"
    def verify_bca_m5portal_bread_crumb(self, param):
        """
            `Description:` This API verifies the M5 Portal Bread Crumb
            ("bread crumb" is a series of information) on BCA Page
            Example:  Home -> Phone System -> BOSS_AUTO_68 -> Bridged Call Appearances
            `Param1:` param: The account name
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page

        status = True

        try:
            # Verify the M5 Portal Bread Crumb ("bread crumb" is a series of information) on BCA Page
            self.wait("M5Portal_Bread_Crumb")
            header = self._browser.element_finder("M5Portal_Bread_Crumb")
            links_list = header.find_elements_by_tag_name('li')
            if not len(links_list):
                raise BossExceptionHandle("Not found the required links on BCA page!")
            # verify the links
            if ((links_list[1].text != "Phone System")
                    or (links_list[2].text != param)
                    or (links_list[3].text != "Bridged Call Appearances")):
                print(links_list[1].text)
                print(links_list[2].text)
                print(links_list[3].text)
                raise BossExceptionHandle("Link names not matching!")

        except (Exception, BossExceptionHandle) as err:
            print(err)
            status = False

        return status

    # End -- function "verify_bca_M5Portal_Bread_Crumb"

    # Start -- Function "verify_bca_page_add_button"
    def verify_bca_page_add_button(self):
        """
            `Description:` This API verifies the add button on BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            # Verify Add button
            text = "Add Bridged Call Appearance"
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            # Get the displayed text from the BCA add management page and verify it
            self.wait("BCA_Add_Page_Title")
            value = self.query_ele.get_text("BCA_Add_Page_Title")
            if text != value:
                print(value)
                raise BossExceptionHandle("Text in the page not as expected")
            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(2)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(5)
        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False
        return status
    # End -- Function "verify_bca_page_add_button"

    # Start -- Function "verify_bca_page_copy_button"
    def verify_bca_page_copy_button(self):
        """
            `Description:` This API verifies the Copy button on BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            # Verify copy button
            text = "To copy a bridged call appearance, click the check box next to it."
            self.wait("Copy_BCA_Button")
            self.action_ele.click_element("Copy_BCA_Button")
            # Get the displayed text from the BCA copy management page and verify it
            self.wait("BCA_Actions_Manage_Popup_Info")
            value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
            if text != value:
                print(value)
                raise BossExceptionHandle("Text in the page not as expected")
            self.wait("BCA_OK_Button")
            self.action_ele.click_element("BCA_OK_Button")
            time.sleep(2)
        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False
        return status

    # Start -- Function "verify_bca_page_edit_button"
    def verify_bca_page_edit_button(self):
        """
            `Description:` This API verifies the Edit button on BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            # Verify Edit button
            text = "To edit a bridged call appearance, click the check box next to it."
            self.wait("Edit_BCA_Button")
            self.action_ele.click_element("Edit_BCA_Button")
            # Get the displayed text from the BCA Edit management page and verify it
            self.wait("BCA_Actions_Manage_Popup_Info")
            value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
            if text != value:
                print(value)
                raise BossExceptionHandle("Text in the page not as expected")
            self.wait("BCA_OK_Button")
            self.action_ele.click_element("BCA_OK_Button")
            time.sleep(2)
        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False
        return status
    # End -- Function "verify_bca_page_edit_button"

    # Start -- Function "verify_bca_page_delete_button"
    def verify_bca_page_delete_button(self):
        """
            `Description:` This API verifies the Delete button on BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            # Verify Delete button
            text = "To remove a bridged call appearance, click the check box next to it."
            self.wait("Delete_BCA_Button")
            self.action_ele.click_element("Delete_BCA_Button")
            # Get the displayed text from the BCA delete management page and verify it
            self.wait("BCA_Actions_Manage_Popup_Info")
            value = self.query_ele.get_text("BCA_Actions_Manage_Popup_Info")
            if text != value:
                print(value)
                raise BossExceptionHandle("Text in the page not as expected")
            self.wait("BCA_OK_Button")
            self.action_ele.click_element("BCA_OK_Button")
            time.sleep(2)
        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False
        return status
    # End -- Function "verify_bca_page_delete_button"

    # Verifying the BCA page UI for different buttons and tabs
    def verify_bca_page(self, param):
        """
            `Description:` This API verifies the complete BCA page
            `Param1:` param: operation types "copy" / "add" / "edit" / "delete"
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page

        status = True

        try:
            if param == "copy":
                # Verify the bca page copy button
                if not self.verify_bca_page_copy_button():
                    raise BossExceptionHandle("Copy Button Verification Failed")
            elif param == "add":
                # Verify the bca page add button
                if not self.verify_bca_page_add_button():
                    raise BossExceptionHandle("Add Button Verification Failed")
            elif param == "edit":
                # Verify the bca page edit button
                if not self.verify_bca_page_edit_button():
                    raise BossExceptionHandle("Edit Button Verification Failed")
            elif param == "delete":
                # Verify the bca page delete button
                if not self.verify_bca_page_delete_button():
                    raise BossExceptionHandle("Delete Button Verification Failed")
            else:
                # Verify the bca page M5 portal bread crumb
                if not self.verify_bca_m5portal_bread_crumb(param):
                    raise BossExceptionHandle("m5 portal bread crumb Verification Failed")

                # Verify the bca page add button
                if not self.verify_bca_page_add_button():
                    raise BossExceptionHandle("Add Button Verification Failed")

                # Verify the bca page copy button
                if not self.verify_bca_page_copy_button():
                    raise BossExceptionHandle("Copy Button Verification Failed")

                # Verify the bca page edit button
                if not self.verify_bca_page_edit_button():
                    raise BossExceptionHandle("Edit Button Verification Failed")

                # Verify the bca page delete button
                if not self.verify_bca_page_delete_button():
                    raise BossExceptionHandle("Delete Button Verification Failed")

                # Verify Name Header field
                self.wait("BCA_Header_Name_Field")
                element = self._browser.element_finder("BCA_Header_Name_Field")
                if not element:
                    raise BossExceptionHandle('Page does not contain "Name" header field')
                time.sleep(1)

                # Verify Extension Header field
                self.wait("BCA_Header_Extension_Field")
                element = self._browser.element_finder("BCA_Header_Extension_Field")
                if not element:
                    raise BossExceptionHandle('Page does not contain "Extension" header field')
                time.sleep(1)

                # Verify Status Header field
                self.wait("BCA_Header_Status_Field")
                element = self._browser.element_finder("BCA_Header_Status_Field")
                if not element:
                    raise BossExceptionHandle('Page does not contain "Status" header field')
                time.sleep(1)

                # Verify Location Header field
                self.wait("BCA_Header_Location_Field")
                element = self._browser.element_finder("BCA_Header_Location_Field")
                if not element:
                    raise BossExceptionHandle('Page does not contain "Location" header field')
                time.sleep(1)

        except (Exception, BossExceptionHandle) as err:
            status = False
            print("Verifying the BCA page failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status

    # End of function "verify_bca_page"

    # START - Function "verify_call_forward_busy_field_options"
    def verify_call_forward_busy_field_options(self):
        """
            `Description:` This API verifies the Call Forward Busy field on Add BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            self.wait("BCA_Show_More_Option")
            self.action_ele.click_element("BCA_Show_More_Option")

            self.wait("BCA_CFBusy")
            # First Check the default value for the Call Forward busy field
            cf_busy = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFBusy")
            if cf_busy != "8 calls":
                raise BossExceptionHandle("Default value for the select option of Call Forward Busy Incorrect !")

            # Then check all the options
            element = self._browser.element_finder("BCA_CFBusy")
            values = element.find_elements_by_tag_name('option')
            if len(values) < 1:
                raise BossExceptionHandle("No options in the CFBusy selection drop down!")

            calls_values = list(map((lambda x: str(x) + " calls" if x > 1 else str(x) + " call"), list(range(1, 25))))
            for i in range(0, 24):
                if calls_values[i] != values[i].text:
                    print("Expected Value: %s, Actual Value: %s" % (calls_values[i], values[i].text))
                    raise BossExceptionHandle("CFBusy selection drop down value does not match")
                print("Expected Value: %s, Actual Value: %s" % (calls_values[i], values[i].text))

            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(1)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End - Function "verify_call_forward_busy_field_options"

    # START - Function "verify_call_forward_no_answer_field_options"
    def verify_call_forward_no_answer_field_options(self):
        """
            `Description:` This API verifies the call forward no answer field on Add BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            self.wait("BCA_Show_More_Option")
            self.action_ele.click_element("BCA_Show_More_Option")

            self.wait("BCA_CFNoAnswer")
            # First Check the default value for the Call Forward No answer field
            cf_no_ans = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFNoAnswer")
            if cf_no_ans != "4 rings":
                raise BossExceptionHandle("Call Forward no answer default select option Incorrect !")

            # Then check all the options
            element = self._browser.element_finder("BCA_CFNoAnswer")
            values = element.find_elements_by_tag_name('option')
            if len(values) < 1:
                raise BossExceptionHandle("No options in the CFNo Answer selection drop down!")

            rings_values = list(map((lambda x: str(x) + " rings" if x > 1 else str(x) + " ring"), list(range(1, 21))))
            for i in range(0, 20):
                if rings_values[i] != values[i].text:
                    print("Expected Value: %s, Actual Value: %s" % (rings_values[i], values[i].text))
                    raise BossExceptionHandle("CFNo Answer selection drop down value does not match")
                print("Expected Value: %s, Actual Value: %s" % (rings_values[i], values[i].text))

            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(1)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End - Function "verify_call_forward_no_answer_field_options"

    # START - Function "verify_Conferencing_field_options"
    def verify_conferencing_field_options(self):
        """
            `Description:` This API verifies different conferencing field options on Add BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            self.wait("BCA_Show_More_Option")
            self.action_ele.click_element("BCA_Show_More_Option")

            self.wait("BCA_Conf_Option")
            # First Check the default value for the conferencing field
            conf_opt = self.query_ele.get_text_of_selected_dropdown_option("BCA_Conf_Option")
            if conf_opt != "Disable Conferencing":
                raise BossExceptionHandle("Conferencing default select option Incorrect !")

            # Then check all the options
            element = self._browser.element_finder("BCA_Conf_Option")
            values = element.find_elements_by_tag_name('option')
            if len(values) < 1:
                raise BossExceptionHandle("No options in the Conferencing selection drop down!")

            conf_options = ["Disable Conferencing",
                            "Enable, others may not join",
                            "Enable, others may join"]

            for i in range(3):
                if conf_options[i] != values[i].text:
                    print("Expected Value: %s, Actual Value: %s" % (conf_options[i], values[i].text))
                    raise BossExceptionHandle("Conferencing selection drop down value does not match")
                print("Expected Value: %s, Actual Value: %s" % (conf_options[i], values[i].text))

            # Verify the Label information
            text = "Bridged Call Appearances are set up to be private by default, " \
                   "so a BCA or aBCA user with a call in progress cannot be joined " \
                   "by other BCA users on the same extension. However, the default " \
                   "setting can be changed to allow others to join, and an override on " \
                   "the phone lets the owner of the call lock or unlock the conference " \
                   "regardless of the default."

            self.wait("BCA_Add_Conference_Option_Label")
            element = self._browser.element_finder("BCA_Add_Conference_Option_Label")
            if not element:
                raise BossExceptionHandle("Element Conference Options Label img not found")
            info = element.get_attribute("tooltip")
            if info != text:
                print(info)
                raise BossExceptionHandle("Conference Options Label text does not match")

            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(1)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End - Function "verify_Conferencing_field_options"

    # START - Function "verify_enable_tone_check_box"
    def verify_enable_tone_check_box(self):
        """
            `Description:` This function verifies the enable tone field on Add BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            self.wait("BCA_Show_More_Option")
            self.action_ele.click_element("BCA_Show_More_Option")

            # Validation -1  *** "Enable Tone" disabled for conference option "Disable Conferencing"
            self.wait("BCA_Conf_Option")

            # The default option for conference option is "Disable Conferencing".
            # In this case the Enable Tone will be disabled

            try:
                if self.wait("BCA_Enable_Tone", 10):
                    status = False
                    raise BossExceptionHandle("Enable tone enabled!")
            except (Exception, BossExceptionHandle) as error:
                if not status:
                    raise BossExceptionHandle('Enable Tone validation failed for Conf option is "Disable Conferencing"')

            # Now change the conferencing option to "Enable, others may not join"
            self.wait("BCA_Conf_Option")
            self.action_ele.select_from_dropdown_using_text("BCA_Conf_Option", "Enable, others may not join")

            # In this case the Enable Tone check box must be enabled. If not enabled Timeout Exception will be raised
            self.wait("BCA_Enable_Tone", 10)

            # Now again change the conferencing option to "Enable, others may join"
            self.wait("BCA_Conf_Option")
            self.action_ele.select_from_dropdown_using_text("BCA_Conf_Option", "Enable, others may join")

            # In this case the Enable Tone check box must be enabled. If not enabled Timeout Exception will be raised
            self.wait("BCA_Enable_Tone", 10)

            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(1)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End - Function "verify_enable_tone_check_box"

    # Start of function --- "verify_show_more_settings"
    def verify_show_more_settings(self):
        """
            `Description:` This API verifies all fields under show more settings link
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        try:
            self.wait("BCA_Show_More_Option")
            self.action_ele.click_element("BCA_Show_More_Option")

            # Check that the Privacy check box is enabled by default
            self.wait("BCA_Privacy_Check_Box")
            privacy = self.action_ele.check_checkbox("BCA_Privacy_Check_Box")
            if not privacy:
                raise BossExceptionHandle("Default Value for the Privacy Check box is not enabled")

            self.wait("BCA_CFBusy")
            cf_busy = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFBusy")
            # Check the default value for the Call Forward busy field
            if cf_busy != "8 calls":
                raise BossExceptionHandle("Default value for the select option of Call Forward Busy Incorrect !")

            # # Check that the CF Busy Extn field is enabled as the default
            # if not self.wait("CallForwardBusyExtn", 10):
            #     raise BossExceptionHandle("CF Busy Extn field not enabled !")
            self.wait("BCA_CFNoAnswer")
            cf_no_answer = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFNoAnswer")
            # Check the default value for the Call Forward No Answer field
            if cf_no_answer != "4 rings":
                raise BossExceptionHandle("Default value for the select option of CF No Answer Incorrect !")

            # # Check that the CF No Answer Extn field is enabled as the default
            # if not self.wait("BCA_CFNoAnswer_Extn"):
            #     raise BossExceptionHandle("CF No Answer Extn field not enabled !")
            self.wait("BCA_Conf_Option")
            conf_option = self.query_ele.get_text_of_selected_dropdown_option("BCA_Conf_Option")
            # Check the default option for Conferencing Options
            if conf_option != 'Disable Conferencing':
                raise BossExceptionHandle("Default option for the Conferencing Options is not correct")

            # Check that the "Enable tone when parties join or leave" check box is disabled
            try:
                if self.wait("BCA_Enable_Tone", 10):
                    status = False
                    raise BossExceptionHandle("Enable tone when parties join or leave check box is enabled!")
            except (Exception, BossExceptionHandle) as error:
                if not status:
                    raise BossExceptionHandle("Enable Tone validation failed")

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End of function --- "verify_show_more_settings"

    # Start of function --- "verify_add_bca_page_show_more_settings"
    def verify_add_bca_page_show_more_settings(self):
        """
            `Description:` This API verifies the show more settings link on add BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            if not self.verify_show_more_settings():
                raise BossExceptionHandle("Verify Show more settings failed")

        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False

        return status

    # End of function --- "verify_add_bca_page_show_more_settings"

    # START - Function "verify_add_bca_page"
    def verify_add_bca_page(self):
        """
            `Description:` This API verifies the complete Add BCA operation page
            In this case it verifies all the default values
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True

        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            self.wait("BCA_Radio_Button")
            self.action_ele.select_radio_button("BCA_Radio_Button")

            self.wait("BCA_Profile_Name")
            profile_name = self.query_ele.get_text("BCA_Profile_Name")
            # check that the default Name field value is blank
            if profile_name:
                raise BossExceptionHandle("Default Name Field value is not blank")

            self.wait("BCA_Extension")
            extn = self._browser.element_finder("BCA_Extension")
            # check that the default Extension field value is not blank
            if extn:
                if not extn.get_attribute("value"):
                    raise BossExceptionHandle("Default Extension Field value is blank")
            print("Default Extension Field Value: %s" % extn.get_attribute("value"))
            self.wait("BCA_Location")
            location = self.query_ele.get_text_of_selected_dropdown_option("BCA_Location")
            # Check the default select option of the drop down for Location
            if location != "Select Location ...":
                raise BossExceptionHandle("Default select option for Location drop down Incorrect")

            self.wait("BCA_Assign_PhoneNumber")
            ph_number = self.query_ele.get_text_of_selected_dropdown_option("BCA_Assign_PhoneNumber")
            # Check the default select option of the drop down for Phone Number
            if ph_number != "Don't assign a number":
                raise BossExceptionHandle("Default select option for Phone Number drop down Incorrect")

            # Check that the Phone Number Select field is not enabled as the default
            try:
                if self.wait("BCA_PhoneNumber", 10):
                    status = False
                    raise BossExceptionHandle("Phone Number Select field enabled !")
            except:
                if not status:
                    raise BossExceptionHandle("Phone Number Select field validation failed !")

            # Check that the Outbound Caller Id field is not enabled as the default
            try:
                if self.wait("BCA_OutboundCallerIds", 10):
                    status = False
                    raise BossExceptionHandle("Outbound Caller Id field enabled !")
            except:
                if not status:
                    raise BossExceptionHandle("Outbound caller Id field validation failed")

            # START -- other options

            self.wait("BCA_Show_More_Option")
            self.action_ele.click_element("BCA_Show_More_Option")

            # Check that the Privacy check box is enabled by default
            self.wait("BCA_Privacy_Check_Box")
            privacy = self.action_ele.check_checkbox("BCA_Privacy_Check_Box")
            if not privacy:
                raise BossExceptionHandle("Default Value for the Privacy Check box is not enabled")

            self.wait("BCA_CFBusy")
            cf_busy = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFBusy")
            # Check the default value for the Call Forward busy field
            if cf_busy != "8 calls":
                raise BossExceptionHandle("Default value for the select option of Call Forward Busy Incorrect !")

            # # Check that the CF Busy Extn field is enabled as the default
            # if not self.wait("CallForwardBusyExtn", 10):
            #     raise BossExceptionHandle("CF Busy Extn field not enabled !")
            self.wait("BCA_CFNoAnswer")
            cf_no_answer = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFNoAnswer")
            # Check the default value for the Call Forward No Answer field
            if cf_no_answer != "4 rings":
                raise BossExceptionHandle("Default value for the select option of CF No Answer Incorrect !")

            # # Check that the CF No Answer Extn field is enabled as the default
            # if not self.wait("BCA_CFNoAnswer_Extn"):
            #     raise BossExceptionHandle("CF No Answer Extn field not enabled !")
            self.wait("BCA_Conf_Option")
            conf_option = self.query_ele.get_text_of_selected_dropdown_option("BCA_Conf_Option")
            # Check the default option for Conferencing Options
            if conf_option != 'Disable Conferencing':
                raise BossExceptionHandle("Default option for the Conferencing Options is not correct")

            # Check that the "Enable tone when parties join or leave" check box is disabled
            try:
                if self.wait("BCA_Enable_Tone", 10):
                    status = False
                    raise BossExceptionHandle("Enable tone when parties join or leave check box is enabled!")
            except:
                if not status:
                    raise BossExceptionHandle("Enable Tone validation failed")

            # END -- Other Options

            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(1)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as err:
            status = False
            print("Verifying Add BCA page failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status

    # End of function --- "verify_add_bca_page"

    # Start of function --- "verify_add_bca_page_show_less_settings"
    def verify_add_bca_page_show_less_settings(self):
        """
            `Description:` This function verifies the show less settings link on Add BCA page
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        try:
            self.wait("Add_BCA_Button")
            self.action_ele.click_element("Add_BCA_Button")
            time.sleep(1)

            if not self.verify_show_more_settings():
                raise BossExceptionHandle("Verify Show more settings failed")

            self.wait("BCA_Show_Less_Option")
            self.action_ele.click_element("BCA_Show_Less_Option")

            # Cancel the operation
            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(1)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False

        return status
    # End of function --- "verify_add_bca_page_show_less_settings"

    # Start of function --- "verify_copy_bca_page"
    def verify_copy_bca_page(self, params):
        """
            `Description:` This API verifies the Copy BCA page
            `Param1:` params: BCA / aBCA Profile name
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page
        verified = True
        if not params["AssociatedBCA"]:
            bca_profile_name = params["ProfileName"] + " BCA"
        else:
            bca_profile_name = params["AssociatedBCAProfile"] + " aBCA"

        print("BCA Profile name: %s" % bca_profile_name)

        try:

            # Select the BCA from the grid
            if not self.select_bca_from_grid(bca_profile_name):
                raise BossExceptionHandle("Selecting the required BCA from the grid failed")

            # Click on the copy button
            self.wait("Copy_BCA_Button")
            self.action_ele.click_element("Copy_BCA_Button")

            if not params["AssociatedBCA"]:
                # Get the copy page title
                page_title = "Copy Bridged Call Appearance"
                self.wait("BCA_Copy_Page_Title")
                if page_title != self.query_ele.get_text("BCA_Copy_Page_Title"):
                    raise BossExceptionHandle("The page title does not match")

                # Press the cancel button
                self.wait("BCA_Cancel_Button")
                self.action_ele.click_element("BCA_Cancel_Button")

                self.wait("BCA_Yes_Button")
                self.action_ele.click_element("BCA_Yes_Button")
            else:
                self.wait("BCA_OK_Button")
                self.action_ele.click_element("BCA_OK_Button")

            time.sleep(2)

            # De select the BCA from the grid
            self.select_bca_from_grid(bca_profile_name)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            verified = False

        return verified
    # End of function --- "verify_copy_bca_page"

    # Start of function --- "verify_bca_edit_page"
    def verify_bca_edit_page(self, params):
        """
            `Description:` This function verifies the Edit BCA page
            `Param1:` param: BCA / aBCA profile name
            `Returns:` True / False
            `Created by:` Prasanna
        """
        # Assumption is that the control is already in BCA page
        verified = True
        if not params["AssociatedBCA"]:
            bca_profile_name = params["ProfileName"] + " BCA"
        else:
            bca_profile_name = params["AssociatedBCAProfile"] + " aBCA"
            print(bca_profile_name)

        print("BCA Profile name: %s" % bca_profile_name)

        try:

            # Select the BCA from the grid
            if not self.select_bca_from_grid(bca_profile_name):
                raise BossExceptionHandle("Selecting the required BCA from the grid failed")

            # Click on the copy button
            self.wait("Edit_BCA_Button")
            self.action_ele.click_element("Edit_BCA_Button")

            # Verify the Edit page title
            page_title = "Edit Bridged Call Appearance"
            self.wait("BCA_Edit_Page_Title")
            if page_title != self.query_ele.get_text("BCA_Edit_Page_Title"):
                raise BossExceptionHandle("Page title does not match")

            # Verify that the Type "BCA" radio button is disabled
            try:
                element = self._browser.element_finder("BCA_Radio_Button")
                if element.is_enabled():
                    raise BossExceptionHandle("The BCA radio button is enabled!!!")
            except BossExceptionHandle as e:  # Error case
                raise Exception
            except Exception as e:
                print(e)

            # Verify that the Type "aBCA" radio button is disabled
            try:
                element = self._browser.element_finder("Associated_BCA")
                if element.is_enabled():
                    raise BossExceptionHandle("The aBCA radio button is enabled!!!")
            except BossExceptionHandle as e:   # Error case
                raise Exception
            except Exception as e:
                print(e)

            # Verify that the extension field is disabled
            try:
                element = self._browser.element_finder("BCA_Extension")
                if element.is_enabled():
                    raise BossExceptionHandle("The Exception field is enabled!!!")
            except BossExceptionHandle as e:   # Error case
                raise Exception
            except Exception as e:
                print(e)

            if params["AssociatedBCA"]:

                if params["SelectPhoneNumber"]:
                    # if 'x' not in params["SelectPhoneNumber"]:
                    #     bca_profile_name = params["SelectPhoneNumber"] + " x" + \
                    #                        params["SelectPhoneNumber"][-4:] + " - " + \
                    #                        params["AssociatedBCAProfile"]
                    # else:
                    #     bca_profile_name = params["SelectPhoneNumber"] + " - " + \
                    #                        params["AssociatedBCAProfile"]
                    bca_profile_name = params["SelectPhoneNumber"] + " - " + \
                                       params["AssociatedBCAProfile"]
                    print(bca_profile_name)
                    # verify the aBCA profile name
                    self.wait("BCA_Associated_Profile_Name")
                    profile_name = self.query_ele.get_text_of_selected_dropdown_option("BCA_Associated_Profile_Name")
                    if profile_name != bca_profile_name:
                        print(profile_name)
                        raise BossExceptionHandle("Profile name does not match")
            else:
                # Verify that the "Name" field is disabled
                try:
                    element = self._browser.element_finder("BCA_Profile_Name")
                    if element.is_enabled():
                        raise BossExceptionHandle("The Profile name field is enabled!!!")
                except BossExceptionHandle as e:  # Error case
                    raise Exception
                except Exception as e:
                    print(e)

                # verify that the location field is editable and check the existing value
                self.wait("BCA_Location")
                location_name = self.query_ele.get_text_of_selected_dropdown_option("BCA_Location")
                if location_name != params["Location"]:
                    raise BossExceptionHandle("The Location name does not match")

                # Verify that the Phone number select location is editable
                self.wait("BCA_Assign_PhoneNumber")
                val = self.query_ele.get_text_of_selected_dropdown_option("BCA_Assign_PhoneNumber")
                print("Select location type value: {}".format(val))

                # Verify that the Phone number field is editable
                self.wait("BCA_PhoneNumber")
                val = self.query_ele.get_text_of_selected_dropdown_option("BCA_PhoneNumber")
                print("Phone number value: {}".format(val))

                if params["OtherSettings"]:

                    self.wait("BCA_Show_More_Option")
                    self.action_ele.click_element("BCA_Show_More_Option")

                    # Check that the Privacy check box is enabled by default
                    self.wait("BCA_Privacy_Check_Box")
                    privacy = self.action_ele.check_checkbox("BCA_Privacy_Check_Box")
                    if privacy != params["Privacy"]:
                        raise BossExceptionHandle("Privacy Check box value not matching!")

                    # verify the call forward busy field
                    self.wait("BCA_CFBusy")
                    cfb = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFBusy")
                    if cfb != params["CallForwardBusy"]:
                        raise BossExceptionHandle("Call Forward Busy Value does not match!")

                    # verify call forward no answer field
                    self.wait("BCA_CFNoAnswer")
                    cf_no_ans = self.query_ele.get_text_of_selected_dropdown_option("BCA_CFNoAnswer")
                    if cf_no_ans != params["CallForwardNoAnswer"]:
                        raise BossExceptionHandle("Call Forward No Answer Value does not match!")

                    # verify the Conferencing Options
                    self.wait("BCA_Conf_Option")
                    conf_option = self.query_ele.get_text_of_selected_dropdown_option("BCA_Conf_Option")
                    if conf_option != params["ConferencingOptions"]:
                        raise BossExceptionHandle("Conferencing Options does not match!")

            # Press the cancel button
            self.wait("BCA_Cancel_Button")
            self.action_ele.click_element("BCA_Cancel_Button")
            time.sleep(5)
            self.wait("BCA_Yes_Button")
            self.action_ele.click_element("BCA_Yes_Button")
            time.sleep(2)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            verified = False

        return verified

    # End of function --- "verify_bca_edit_page"

    # Start of function --- "select_and_verify_user_on_phone_system_users"
    def select_and_verify_user_on_phone_system_users(self, user_name, params = None):
        """
            `Description:` This API will select and verify different fields on the Phone system -> user page
            `Param1:` user_name: Name of the user
            `Param2:` params: information regarding different fields which need to be verified
            `Returns:` True / False
            `Created by:` Prasanna
        """
        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        info_found = False
        try:
            # get the user row from the grid
            self.wait("User_Page_HeaderRow_FullName")
            self.action_ele.input_text("User_Page_HeaderRow_FullName", user_name)
            time.sleep(2)

            # Get the user info table
            user_grid_table = self._browser.element_finder("User_Grid_Canvas")
            if user_grid_table:
                print("Getting the fields")
                # Get the fields
                columns = user_grid_table.find_elements_by_tag_name('div')
                # verify the columns and get the phone number assigned to the user
                # if 0 != len(columns) and columns[2].text == user_name:
                if 0 != len(columns) and columns[2].text.lower() == user_name.lower():
                    print("The field got selected")
                    info_found = True

            if info_found:
                link = columns[3].find_elements_by_tag_name('a')
                link[0].click()
                time.sleep(2)

            # Check if verification required
            if params:
                # check if SCA info verification required
                if params["ScaInfo"]:
                    info = '"Shared Call Appearance" allows other administrative ' \
                           'staff to manage this user\'s calls on their IP Phones using ' \
                           'an associated Bridged Call Appearance (aBCA). Contact your ' \
                           'administrator or Mitel Support to enable or disable this feature.'

                self.action_ele.mouse_hover("User_Ph_Setting_Sca_Info")
                elm = self._browser.element_finder("User_Ph_Setting_Sca_Info")
                if not elm or elm.get_attribute('tooltip') != info:
                    raise BossExceptionHandle("SCA info verification failed!!!")

        except (Exception, BossExceptionHandle) as err:
            info_found = False
            print("Selecting the User failed")
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return info_found
    # End of function --- "select_and_verify_user_on_phone_system_users"

    # Start of function --- "select_ph_settings_on_phone_system_users"
    def select_ph_settings_on_phone_system_users(self, user_name):
        """
            `Description:` This function selects the phone settings on the Phone system -> user page
            `Param1:` user_name: Name of the user
            `Returns:` True / False
            `Created by:` Prasanna
        """
        info_found = False
        try:
            # get the user row from the grid
            self.wait("User_Page_HeaderRow_FullName")
            self.action_ele.input_text("User_Page_HeaderRow_FullName", user_name)
            time.sleep(2)

            # Get the user info table
            user_grid_table = self._browser.element_finder("User_Grid_Canvas")
            if user_grid_table:
                print("Getting the fields")
                # Get the fields
                columns = user_grid_table.find_elements_by_tag_name('div')
                # verify the columns and get the phone number assigned to the user
                if 0 != len(columns) and columns[2].text == user_name:
                    print("The field got selected")
                    info_found = True

            if info_found:
                link = columns[3].find_elements_by_tag_name('a')
                if not len(link):  # if the log in user is not "staff user"
                    link = columns[2].find_elements_by_tag_name('a')
                if not len(link):
                    raise BossExceptionHandle("Link not found")
                link[0].click()
                time.sleep(2)

        except (Exception, BossExceptionHandle) as err:
            print("Selecting the User Phone Settings failed")
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return info_found
    # End of function --- "select_ph_settings_on_phone_system_users"

    # Start of function --- "select_user_ph_number_on_personal_info_page"
    def select_user_ph_number_on_personal_info_page(self, ph_number):
        """
            `Description:` The function selects a phone number on user's personal information page
            `Param1:` ph_number: Phone number
            `Returns:` True / False
            `Created by:` Prasanna
        """
        status = True
        try:
            # verify that we are on user's personal information page
            self.wait("M5Portal_Bread_Crumb")
            header = self._browser.element_finder("M5Portal_Bread_Crumb")
            links_list = header.find_elements_by_tag_name('li')
            if not len(links_list):
                raise BossExceptionHandle("Not found the required links on page!")
            # verify the links
            if ((links_list[1].text != "Home")
                or (links_list[2].text != "Settings")
                or (links_list[3].text != "Personal Information")):
                print(links_list[1].text)
                print(links_list[2].text)
                print(links_list[3].text)
                raise BossExceptionHandle("Link names not matching!")

            self.wait("User_Personal_Info_headerRow_FormattedTN")
            self.action_ele.input_text("User_Personal_Info_headerRow_FormattedTN", ph_number)
            grid_element = self._browser.element_finder("User_Grid_Canvas")
            if not grid_element:
                raise BossExceptionHandle("user phone number grid element not found!")
            ph_number_list = grid_element.find_elements_by_tag_name('div')
            if not ph_number_list:
                raise BossExceptionHandle("Phone numbers not found in the grind")
            # Get the phone number link from the first element from the list
            columns = ph_number_list[0].find_elements_by_tag_name('div')
            if not columns:
                raise BossExceptionHandle("Fields not found!")
            if columns[0].text != ph_number:
                raise BossExceptionHandle("required phone number not found!")
            columns[0].click()

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End of function --- "select_user_ph_number_on_personal_info_page"

    # Start of function --- "select_line_on_program_button_page"
    def select_line_on_program_button_page(self, button_box):

        """
        `Description:` The function finds a line on a button page
        `Param1:` button_box: button box name
        `Returns:` Line number
        `Created by:` Prasanna
        """

        line_no = None
        # file_path = r"../../map/BossComponent/User_Phone_Programming.map"
        file_path = r"../../../automation-boss/map/BossComponent/User_Phone_Programming.map"
        line = None
        line_function = None
        index = None
        locator_list = list()

        # Open the file in "r" mode
        with open(file_path, 'r') as fd:
            content = fd.readlines()

        # change the value of the locator depending on button_box
        if button_box == "IP Phone":
            tab_str = "tab-ipPhone"
        elif button_box == "Button Box 1":
            tab_str = "tabs-buttonBox1"
        elif button_box == "Button Box 2":
            tab_str = "tabs-buttonBox2"
        elif button_box == "Button Box 3":
            tab_str = "tabs-buttonBox3"
        else:
            tab_str = "tabs-buttonBox4"

        for i in range(len(content)):
            if "User_Ph_Prog_Button_Line_Base" in content[i]:
                line = content[i].split("==")[1]
                locator_list.append(content[i].split("==")[0].replace("_Base", ""))
            if "User_Ph_Prog_Button_Rows_Select_Function_Base" in content[i]:
                line_function = content[i].split("==")[1]
                locator_list.append(content[i].split("==")[0].replace("_Base", ""))

        import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        if not line or not line_function:
            raise BossExceptionHandle("Required lines not found in the file")

        line = line.replace("tabs-", tab_str)
        line_function = line_function.replace("tabs-", tab_str)
        temp_line = locator_list[0]
        temp_line_function = locator_list[1]

        # checking the availability of the line
        for num in range(2, 26):
            status = False
            div = "div[" + str(num) + "]"
            line1 = line.replace("div[*]", div)
            line_function1 = line_function.replace("div[*]", div)
            locator_list[0] = temp_line + "==" + line1
            locator_list[1] = temp_line_function + "==" + line_function1
            if button_box == "IP Phone":
                if 3 <= num <= 14:
                    status = True
            else:
                status = True

            if status:
                index = self.update_map_manager(locator_list, index)
                try:
                    self.wait("User_Ph_Prog_Button_Line")
                    self.action_ele.click_element("User_Ph_Prog_Button_Line")
                    time.sleep(2)
                    self.wait("User_Ph_Prog_Button_Rows_Select_Function")
                    value = \
                        self.query_ele.get_text_of_selected_dropdown_option("User_Ph_Prog_Button_Rows_Select_Function")
                except (Exception, BossExceptionHandle) as e:
                    print(e)
                    return None

                if ((button_box == "IP Phones" and value == "Call Appearance") or
                        (button_box != "IP Phones" and value == "Unused")):
                    line_no = num
                    break

        # remove the locators from the map manager key list
        self.update_map_manager(None, index)

        # replace the file with the changed content
        print("#### Line No: %d" % line_no)
        return line_no
    # End of function --- "select_line_on_program_button_page"

    def select_button_box_on_program_buttons_page(self, button_box):

        """
        `Description:` The function selects one of the program button boxes
        `Param1:` button_box: button box name
        `Returns:` Line number
        `Created by:` Prasanna
        """
        status = False
        try:
            self.wait("User_Phone_Settings_Prog_Button_Types")
            elements = self._browser.element_finder("User_Phone_Settings_Prog_Button_Types")
            if not elements:
                raise BossExceptionHandle("program button types grid not found!")
            prog_button_list = elements.find_elements_by_tag_name('h3')
            if not prog_button_list:
                raise BossExceptionHandle("No Program Button Types available!")
            print("Length of prog_button_list: %s" % len(prog_button_list))
            for i in range(len(prog_button_list)):
                if prog_button_list[i].text == button_box:
                    print("Button Name: %s" % prog_button_list[i].text)
                    button = prog_button_list[i]
                    break
            else:
                raise BossExceptionHandle("Failure in Programing buttons")
            time.sleep(3)
            button.click()
            time.sleep(5)

            # # Select telephony from the drop down
            # self.wait("User_Ph_Prog_Button_Rows_Select_Type")
            # self.action_ele.select_from_dropdown_using_text("User_Ph_Prog_Button_Rows_Select_Type", "Telephony")
            #
            # # Select Function from the drop down
            # self.wait("User_Ph_Prog_Button_Rows_Select_Function")
            # self.action_ele.select_from_dropdown_using_text("User_Ph_Prog_Button_Rows_Select_Function",
            #                                                 "Bridged Call Appearance")
            #
            # # Select the BCA
            # self.wait("User_Ph_Prog_Button_Rows_Select_BCA")
            # self.action_ele.select_from_dropdown_using_text("User_Ph_Prog_Button_Rows_Select_BCA",
            #                                                 "5440 : TestBCA1")
            status = True
        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False

        return status

    # Start of function --- "select_program_buttons_on_phone_settings_page"
    def select_program_buttons_on_phone_settings_page(self):

        """
        `Description:` The function finds the program buttons on the phone settings page and clicks
        `Returns:` Line number
        `Created by:` Prasanna
        """
        status = True
        try:
            # verify that we are on Phone settings page
            self.wait("M5Portal_Bread_Crumb")
            header = self._browser.element_finder("M5Portal_Bread_Crumb")
            links_list = header.find_elements_by_tag_name('li')
            if not len(links_list):
                raise BossExceptionHandle("Not found the required links on page!")
            # verify the links
            if ((links_list[1].text != "Home")
                or (links_list[2].text != "Settings")
                or (links_list[3].text != "Phone Settings")):
                print(links_list[1].text)
                print(links_list[2].text)
                print(links_list[3].text)
                raise BossExceptionHandle("Link names not matching!")

            self.wait("User_Phone_Settings_Prog_Buttons")
            self.action_ele.click_element("User_Phone_Settings_Prog_Buttons")
            time.sleep(1)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status
    # End of function --- "select_program_buttons_on_phone_settings_page"

    # Start of API --- "get_available_program_button_line"
    def get_available_program_button_line(self, username, button_box):

        """
        `Description:` The API will get an available program button line on the required button box
        `Param1:` username: Phone user
        `Param2:` button_box: button box name
        `Returns:` Available Line number
        `Created by:` Prasanna
        """
        import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        line_no = None
        try:

            # Step1. Select the user phone settings on users grid
            if not self.select_ph_settings_on_phone_system_users(username):
                raise BossExceptionHandle("User Phone Settings selection failed")

            # Step2. Select the Program Buttons Page
            if not self.select_program_buttons_on_phone_settings_page():
                raise BossExceptionHandle("Failed clicking the program buttons link")

            # Step3. Select any of the Button Box
            if not self.select_button_box_on_program_buttons_page(button_box):
                raise BossExceptionHandle("Selecting a Button Box failed!")

            # Step4. Select any Line
            line_no = self.select_line_on_program_button_page(button_box)
            if not line_no:
                raise BossExceptionHandle("No button available for the button box")

        except (Exception, BossExceptionHandle) as e:
            print(e)

        return line_no

    # End of API --- "get_available_program_button_line"

    # Start of API --- "move_to_line_on_prog_button_page"
    def move_to_line_on_prog_button_page(self, username, button_box):

        """
        `Description:` The function will move to a particular line on program button box
        `Param1:` username: Phone user
        `Param2:` button_box: button box name
        `Returns:` True / False
        `Created by:` Prasanna
        """
        status = True
        try:

            # Step1. Select the user phone settings on users grid
            if not self.select_ph_settings_on_phone_system_users(username):
                raise BossExceptionHandle("User Phone Settings selection failed")

            # Step2. Select the Program Buttons Page
            if not self.select_program_buttons_on_phone_settings_page():
                raise BossExceptionHandle("Failed clicking the program buttons link")

            # Step3. Select any of the Button Box
            if not self.select_button_box_on_program_buttons_page(button_box):
                raise BossExceptionHandle("Selecting a Button Box failed!")

            # Step4. Select the required Line
            self.wait("User_Ph_Prog_Button_Line")
            self.action_ele.click_element("User_Ph_Prog_Button_Line")
            time.sleep(2)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False

        return status
    # End of API ---- "move_to_line_on_prog_button_page"

    # Start of function --- "update_map_manager"
    def update_map_manager(self, locator_list, index=None):

        """
        `Description:` The function will update the map manager with updated button box line locator
        `Param1:` locator_list: list of updated locators
        `Param2:` index: map list index- required to delete the old data in the map list
        `Returns:` The index on the map list where the update happens
        `Created by:` Prasanna
        """
        map_dict = {}
        map_key_list = []

        if index:
            del(mapList[index])

        if locator_list:
            for line in locator_list:
                elements = line.split('==')
                if len(elements) >= 2:
                    # Remove \n and leading and trailing spaces from value and then save
                    value_parts = [ele.strip() for ele in elements[1].split('#')]
                    key = elements[0].strip()

                    map_key_list.append(key)
                    map_dict[key] = {
                        "ELEMENT_TYPE": value_parts[0],
                        "BY_TYPE": value_parts[1],
                        "BY_VALUE": value_parts[2]
                    }

            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            mapDict.update(map_dict)

            # check any old occurrence of the same key list
            if map_key_list not in mapList:
                mapList.append(map_key_list)

            return mapList.index(map_key_list)
        else:
            return None
    # End of function --- "update_map_manager"

    # Start of function --- "regenerate_programming_page_element_locators"
    def regenerate_programming_page_element_locators(self, username, button_box, line_no=None):

        """
        `Description:` The API will regenerate the element locator strings in the map file for the
        programming button page

        Rules:
        1. In the map file "User_Phone_Programming.map"
           there must be Base locator string so that the actual locator string can be regenerated
        2. "_Base" must be the suffix for the base string. Ex: "Prog_Button_Rows_Select_Type_Base"
        3. The actual locator string must follow the base string in the map file. Ex: "Prog_Button_Rows_Select_Type"
        4. So in the Map file it should look like
           Prog_Button_Rows_Select_Type_Base ==
                                select#xpath#//*[@id="tabs-"]/div/div[*]/div/div[2]/div[2]/div/div[2]/select[1]
           Prog_Button_Rows_Select_Type ==
                                any string  (does not matter since this will be replaced during regeneration)
        `Param1:` username: The Phone user name
        `Param2:` button_box: The name of the button box
        `Param3:` line_no: The available line on the programming button box page
        `Returns:` True / False
        `Created by:` Prasanna
        """
        print("#### In function: %s" % "regenerate_programming_page_element_locators")
        import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        file_path = r"../../../automation-boss/map/BossComponent/User_Phone_Programming.map"

        # Call the API to get an available line on the button box page
        if not line_no:
            line_no = self.get_available_program_button_line(username, button_box)
            if not line_no:
                print("No available line on the button box!!!")
                return False, None

        # change the value of the locator depending on button_box
        if button_box == "IP Phone":
            tab_str = "tab-ipPhone"
            bca_button_str = "prog_button_0"
        elif button_box == "Button Box 1":
            tab_str = "tabs-buttonBox1"
            bca_button_str = "prog_button_1"
        elif button_box == "Button Box 2":
            tab_str = "tabs-buttonBox2"
            bca_button_str = "prog_button_2"
        elif button_box == "Button Box 3":
            tab_str = "tabs-buttonBox3"
            bca_button_str = "prog_button_3"
        else:
            tab_str = "tabs-buttonBox4"
            bca_button_str = "prog_button_4"

        # Open the file in "r" mode
        with open(file_path, 'r') as fd:
            content = fd.readlines()

        line = list()
        locator_list = list()

        for i in range(len(content)):
            if "_Base" in content[i]:
                line.append(content[i].split("==")[1])  # Get the mutable part of the element locator base string
                # Create the list of locators
                locator_list.append(content[i].split("==")[0].replace("_Base", ""))

        if not len(line):
            print("Lines not found in the map file")
            return False, None

        div = "div[" + str(line_no) + "]"
        for i in range(len(line)):
            if "tabs-" in line[i]:
                line[i] = line[i].replace("tabs-", tab_str)
            if "div[*]" in line[i]:
                line[i] = line[i].replace("div[*]", div)
            # @Modified by: Prasanna (because of changes in programming button page)
            if "user_prog_button_0_button_*" in line[i]:
                num = line_no - 2
                temp_str = "button_" + str(num)
                line[i] = line[i].replace("prog_button_0", bca_button_str)
                line[i] = line[i].replace("button_*", temp_str)
            locator_list[i] = locator_list[i] + "==" + line[i]

        print("&&&& Locator List: %s" % locator_list)

        # Parse the content and update the mapMgr with the locators
        if not self.update_map_manager(locator_list, None):
            print("map manager update is not successful")
            return False, None

        self.action_ele.click_element('user_phone_settings')
        self.action_ele.click_element('user_prog_button')
        if line_no:
            self.action_ele.explicit_wait('User_Ph_Prog_Button_' + str(line_no) + '_IP_Phones')
            self.action_ele.click_element('User_Ph_Prog_Button_' + str(line_no) + '_IP_Phones')

        return True, line_no
    # End of function --- "regenerate_programming_page_element_locators"

    # Start of API --- "select_type_and_function_on_program_page"
    def select_type_and_function_on_program_page(self, params):

        """
        `Description:` The API select the type, function, Long label and Short label on the program page
        `Param1:` params: type, function, Long label and Short label
        `Returns:` True / False
        `Created by:` Prasanna
        """
        print("In Function: %s" % "select_type_and_function_on_program_page")

        try:

            import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params["SelectFunction"]:
                self.wait("User_Ph_Prog_Button_Rows_Select_Function")
                self.action_ele.select_from_dropdown_using_text("User_Ph_Prog_Button_Rows_Select_Function",
                                                                params["SelectFunction"])

            if params["SelectLongLabel"]:
                self.wait("User_Ph_Prog_Button_Rows_Input_LongLabel")
                self.action_ele.input_text("User_Ph_Prog_Button_Rows_Input_LongLabel", params["SelectLongLabel"])

            if params["SelectShortLabel"]:
                self.wait("User_Ph_Prog_Button_Rows_Input_ShortLabel")
                self.action_ele.input_text("User_Ph_Prog_Button_Rows_Input_ShortLabel", params["SelectShortLabel"])

        except (Exception, BossExceptionHandle) as e:
            print(e)
            return False

        # replace the file with the changed content
        return True
    # End of API --- "select_type_and_function_on_program_page"

    # Start of function --- "select_bca_on_prog_buttons_page"
    def select_bca_on_prog_buttons_page(self, params):

        """
        `Description:` The function finds and selects the BCA on
        Phone System -> Users -> User -> Phone number -> Prog Buttons  page UI
        `Param1:` params: BCA info
        `Returns:` True / False, Program button Line number
        `Created by:` Prasanna
        """
        status = True

        try:

            import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            # Step1. Select the Function to be Bridged Call Appearance
            if not self.select_type_and_function_on_program_page(params):
                raise BossExceptionHandle("BCA could not be selected")

            # Step2. Select from the Target section the required BCA in the Bridged Call Appearance drop down
            if params["SelectBCA"]:
                self.wait("User_Ph_Prog_Button_Select_Bca")
                # for i in range(len(self.bca)):
                #     if params["ProfileName"] in self.bca[i]["ProfileName"]:
                #         bca_name = self.bca[i]["Extension"] + " : " + self.bca[i]["ProfileName"]
                # 1. get all select options
                bca_names = self.query_ele.get_text_list_from_dropdown("User_Ph_Prog_Button_Select_Bca")
                # 2. find profile name matching (partial)
                bca_name = list(filter((lambda x: params["ProfileName"] in x), bca_names))
                # 3. select the option on index
                self.action_ele.select_from_dropdown_using_index(
                    "User_Ph_Prog_Button_Select_Bca", bca_names.index(bca_name[0]))

            # step3. Select call stack position
            if params["SelectCallStackPosition"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Call_Stack_Pos")
                self.action_ele.select_from_dropdown_using_text("User_Ph_Prog_Button_Select_Bca_Call_Stack_Pos",
                                                                params["SelectCallStackPosition"])
            # step4. Select the option for Delay Before Audibly Ringing
            if params["SelectDelayBeforeAudiblyRing"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Delay_Before_Audibly_Ring")
                self.action_ele.select_from_dropdown_using_text(
                    "User_Ph_Prog_Button_Select_Bca_Delay_Before_Audibly_Ring",
                    params["SelectDelayBeforeAudiblyRing"]
                )

            # step5. Select the option for Show Caller Id Alert
            if params["SelectShowCallerIDAlert"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Show_Caller_Id_Alert")
                self.action_ele.select_from_dropdown_using_text(
                    "User_Ph_Prog_Button_Select_Bca_Show_Caller_Id_Alert",
                    params["SelectShowCallerIDAlert"]
                )

            # step6. Select Auto Answer option
            if params["SelectAutoAnswer"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Allow_Auto_Answer")
                self.action_ele.select_from_dropdown_using_text(
                    "User_Ph_Prog_Button_Select_Bca_Allow_Auto_Answer",
                    params["SelectAutoAnswer"]
                )

            # step7. Select No connected call action
            if params["SelectNoconnectedcallactionAnswerOnly"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Answer_Only")
                self.action_ele.click_element("User_Ph_Prog_Button_Select_Bca_Answer_Only")
            elif params["SelectNoconnectedcallactionDialTone"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Dial_Tone")
                self.action_ele.click_element("User_Ph_Prog_Button_Select_Bca_Dial_Tone")
            elif params["SelectNoconnectedcallactionDialExtn"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Dial_Extn")
                self.action_ele.click_element("User_Ph_Prog_Button_Select_Bca_Dial_Extn")
                if params["SelectNoconnectedcallactionDialExtnInput"]:
                    self.wait("User_Ph_Prog_Button_Select_Bca_Dial_Extn_Input")
                    self.action_ele.input_text("User_Ph_Prog_Button_Select_Bca_Dial_Extn_Input",
                                               params["SelectNoconnectedcallactionDialExtnInput"])
                    if params["SelectNoconnectedcallactionDialExtnSearch"]:
                        self.wait("User_Ph_Prog_Button_Select_Bca_Dial_Extn_Search")
                        self.action_ele.click_element("User_Ph_Prog_Button_Select_Bca_Dial_Extn_Search")
            elif params["SelectNoconnectedcallactionDialExternal"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Dial_External")
                self.action_ele.click_element("User_Ph_Prog_Button_Select_Bca_Dial_External")
                if params["SelectNoconnectedcallactionDialExternalInput"]:
                    self.wait("User_Ph_Prog_Button_Select_Bca_Dial_External_Input")
                    self.action_ele.input_text("User_Ph_Prog_Button_Select_Bca_Dial_External_Input",
                                               params["SelectNoconnectedcallactionDialExternalInput"])

            time.sleep(3)

            # step-8. Save or reset the BCA
            if params["SelectBcaSaveButton"]:
                WIL(self.action_ele.click_element, "User_Ph_Prog_Button_Select_Bca_Save_Button")
                WIL(self.wait, "BCA_OK_Button", {'ec': "text_to_be_present_in_element", 'msg_to_verify': "OK"})
                time.sleep(2)
                self.action_ele.click_element("BCA_OK_Button")
                time.sleep(2)
                # verify that "Bridged Call Appearance" appears on the function field of the button line
                text = WIL(self.query_ele.get_text, "User_Ph_Prog_Button_Line_Verify_Function", return_value=True)
                print(text)
                if "Bridged Call Appearance" not in text:
                    raise BossExceptionHandle("The Program line Label not matching!")

            elif params["SelectBcaResetButton"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Reset_Button")
                self.action_ele.click_element("User_Ph_Prog_Button_Select_Bca_Reset_Button")

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)
        return status
    # End of function --- "select_bca_on_prog_buttons_page"





    # Start of function --- "enable_shared_call_appearance"
    def enable_shared_call_appearance(self, params):

        """
        `Description:` TThe function enables the SCA with the required phone extension
        `Param1:` params: sca enable or disable flag and phone number
        `Returns:` True / False
        `Created by:` Prasanna
        """
        status = True
        extn = None
        try:
            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.wait("User_Ph_Settings_Sca_Enable")
            self.action_ele.click_element("User_Ph_Settings_Sca_Enable")
            time.sleep(1)
            self.action_ele.select_from_dropdown_using_text("User_Ph_Settings_Sca_Enable", params["ScaEnableFlag"])
            time.sleep(3)

            # enter the extension
            if params["ScaEnableFlag"] == "Enabled":
                if params["ScaExtn"]:
                    self.wait("User_Ph_Settings_Sca_Enable_Extn")
                    self.action_ele.input_text("User_Ph_Settings_Sca_Enable_Extn", params["ScaExtn"])
                time.sleep(2)

            # Click on Save / Cancel button
            if params["ScaSaveOrCancel"] == "submit":
                self.wait("User_Ph_Setting_Sca_Submit")
                self.action_ele.click_element("User_Ph_Setting_Sca_Submit")

                time.sleep(3)
                self.wait("BCA_OK_Button")
                self.action_ele.click_element("BCA_OK_Button")
                time.sleep(5)
                self.wait("BCA_OK_Button")
                self.action_ele.click_element("BCA_OK_Button")

                time.sleep(5)
            else:
                self.wait("User_Ph_Setting_Sca_Cancel")
                self.action_ele.click_element("User_Ph_Setting_Sca_Cancel")

            extn = self.query_ele.get_text("User_Ph_Settings_Sca_Extn_Label")
            print("SCA Extension: %s" % extn)
            self.Extension.append(extn)

            time.sleep(2)

        except (Exception, BossExceptionHandle) as e:
            print(e)
            status = False

        return status, extn

    # End of function --- "enable_shared_call_appearance"

    # Start of function --- "enable_sca"
    def enable_sca(self, params):

        """
        `Description:` The API enables an SCA on phone settings page of an user
        `Param1:` params: User name and phone number
        `Returns:` True / False
        `Created by:` Prasanna
        """
        status = True
        extn = None
        try:
            # select the user phone settings on users grid
            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if not self.select_and_verify_user_on_phone_system_users(params["ScaUserName"]):
                raise BossExceptionHandle("User selection failed")

            # enable shared call appearance
            status, extn = self.enable_shared_call_appearance(params)
            if not status:
                raise BossExceptionHandle("Enabling the SCA on phone settings page failed")

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        bca = {"ProfileName": params["ScaUserName"],
               "Extension": extn}

        self.bca.append(bca)


        return status, extn

    # End of function --- "enable_sca"

    # Start of function --- "find_entry_on_phone_number_page"
    def find_entry_on_phone_number_page(self, params):

        """
         `Description:` The API finds an entry on the phone number page
         `Param1:` params: Information about the element
         `Returns:` True / False
         `Created by:` Prasanna
         'Modified by:' Palla Surya Kumar
         """
        status = True
        phone_number_state = None
        index = 0
        try:
            # wait till the page is download successfully
            ph_numbers_grid = WIL(self._browser.element_finder, "Grid_Canvas", return_value=True)
            if not ph_numbers_grid:
                raise BossExceptionHandle("Grid canvas not selected in the Grid")

            for i in range(10):
                rows = ph_numbers_grid.find_elements_by_tag_name("div")
                if rows:
                    break
                time.sleep(5)
            else:
                raise BossExceptionHandle("No Row selected in the Grid")

            time.sleep(1)

            # Filter the grid rows
            if params['PhNum']:
                WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Number", params["PhNum"], loop_count=40)
                time.sleep(1)
            if params["Destination"]:
                WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Destination", params["Destination"], loop_count=40)
                time.sleep(1)
            if params["DestType"]:
                # WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Dest_type", params["DestType"])
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Ph_System_Ph_Numbers_Dest_type', params["DestType"], loop_count=40)
            if params["Type"]:
                # WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Type", params["Type"])
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Ph_System_Ph_Numbers_Type', params["Type"], loop_count=40)

            time.sleep(2)

            # Get the row from the grid
            if not params['Expected_status']:  # Checking the negative scenario when no element is selected
                ph_numbers_grid = WIL(self._browser.element_finder, "Grid_Canvas", default_loop_count=2,
                                      delay_in_sec=5, return_value=True)
                if ph_numbers_grid:
                    raise BossExceptionHandle("rows selected !!!")
                else:
                    return True
            else:
                ph_numbers_grid = WIL(self._browser.element_finder, "Grid_Canvas", delay_in_sec=10, return_value=True)
            if not ph_numbers_grid:
                raise BossExceptionHandle("Grid canvas not selected in the Grid")

            for i in range(10):
                rows = ph_numbers_grid.find_elements_by_tag_name("div")
                if rows:
                    break
                time.sleep(5)
            else:
                raise BossExceptionHandle("No Row selected in the Grid")

            time.sleep(1)

            for i in range(len(rows)):
                fields = WIL(rows[i].find_elements_by_tag_name, "div", return_value=True)
                if not fields:
                    raise BossExceptionHandle("No element selected!")
                # Check phone number, Destination type and phone number state
                if params['PhNum']:
                    ph_number = params['PhNum']
                else:
                    if params["Destination"]:
                        for index in range(len(self.bca)):
                            if params["Destination"] == self.bca[index]["ProfileName"]:
                                break
                        else:
                            raise BossExceptionHandle("BCA not added previously!")
                        ph_number = self.bca[index]["PhoneNumber"]
                    else:
                        ph_number = self.bca[i]["PhoneNumber"]  # selecting the ph numbers sequentially

                print(fields[1].text)
                print(fields[3].text)
                print(fields[7].text)
                print(fields[8].text)

                # Modified by: Prasanna
                # if (ph_number == fields[1].text and ((not params["Status"]) or params["Status"] == fields[3].text) and
                #     ((not params["DestType"]) or params["DestType"] == fields[7].text) and
                #     ((not params["Destination"]) or (params["Destination"] in fields[8].text))):
                #     break
                if (ph_number == fields[1].text and
                        ((not params["DestType"]) or params["DestType"] == fields[7].text) and
                        ((not params["Destination"]) or (params["Destination"] in fields[8].text))):
                    phone_number_state = fields[3].text
                    break
            else:
                raise BossExceptionHandle("Required Element not found!")

            fields[1].click()

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        # Reset the entry based on Destination / Phone number / Destination Type field
        if params["Destination"]:
            WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Destination", "")
        if params['PhNum']:
            WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Number", "")
        if params["DestType"]:
            WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Dest_type", "All")
        if params["Type"]:
            WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Type", "All")

        return status, phone_number_state

    # End of function --- "find_entry_on_phone_number_page"

    # Start of API --- "get_phone_number_with_required_status"
    def get_phone_number_with_required_status(self, status, _type="Domestic", location=None, country=None, destination="-"):

        """
        `Description:` The API finds a phone number on the phone number page with required status
        `Param1:` status: Phone status
        `Param2:` _type: Phone type
        `Returns:` Phone number
        `Created by:` Prasanna
        'Modified by:' Palla Surya Kumar
        """
        ph_num = None
        rows = None
        try:

            # Modified by Prasanna: provision to check for both available and pending state
            for loop_count in range(2):
                print(status)
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Ph_System_Ph_Numbers_Status', status, loop_count=40)
                # WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Status", status)
                WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Destination", destination)
                if country:
                    WIL(self.action_ele.select_from_dropdown_using_text, "PhoneSystem_CountryCode", country)
                # for i in range(10):
                #     list_types = WIL(self.query_ele.get_text_list_from_dropdown, "Ph_System_Ph_Numbers_Type", return_value=True)
                #     if _type in list_types:
                #         WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Type", _type)
                #         break
                #     time.sleep(5)
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Ph_System_Ph_Numbers_Type', _type, loop_count=40)
                if location:
                    WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Location", location)

                ph_numbers_grid = WIL(self._browser.element_finder, "Grid_Canvas", delay_in_sec=5, return_value=True)
                if not ph_numbers_grid:
                    raise BossExceptionHandle("No grid elements selected in the Grid")

                try:
                    rows = WIL(ph_numbers_grid.find_element_by_tag_name, "div", delay_in_sec=2, return_value=True)
                    break
                except:
                    status = "Pending port in" if status == "Available" else "Available"
                    continue

            if not rows:
                raise BossExceptionHandle("No rows selected in the Grid")

            # Take the first phone number from the list
            fields = WIL(rows.find_elements_by_tag_name, "div", return_value=True)
            if not fields:
                raise BossExceptionHandle("No element selected!")

            ph_num = fields[1].text
            fields[0].click()

            # Reset the status column
            WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Numbers_Status", "All")
            WIL(self.action_ele.input_text, "Ph_System_Ph_Numbers_Destination", "")
            WIL(self.action_ele.select_from_dropdown_using_text, "PhoneSystem_CountryCode", "All")

        except (Exception, BossExceptionHandle) as e:
            print(e)

        return ph_num

    # End of API --- "get_phone_number_with_required_status"

    # Start of API --- "assign_ph_number_to_bca"
    def assign_ph_number_to_bca(self, ph_status, bca_name, _type="Domestic"):

        """
        `Description:` The API finds a phone number on the phone number page
        and assigns it to a BCA
        `Param1:` ph_status: Phone status
        `Param2:` bca_name: bca name
        `Param3:` _type: Phone type
        `Returns:` Status, Phone number
        `Created by:` Prasanna
        """
        # step1 - find an available phone number
        # step2 - click on assign
        # Step3 - Select an already created BCA
        # Step4 - Assign the phone number to BCA
        status = True
        ph_number = None

        try:

            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

            ph_number = self.get_phone_number_with_required_status(ph_status, _type)
            if not ph_number:
                raise BossExceptionHandle("Required Phone number not found")

            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Assign")
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_Bca")
            time.sleep(1)
            WIL(self.action_ele.select_from_dropdown_using_text, "Ph_System_Ph_Number_Op_Destination", bca_name)
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Save_Button")

            # Click on OK button
            WIL(self.wait, "BCA_OK_Button", ec="text_to_be_present_in_element", msg_to_verify="OK")
            # time.sleep(1)
            WIL(self.action_ele.click_element, "BCA_OK_Button")
            time.sleep(3)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        # Retain the bca and phone number info
        bca_info = dict()
        bca_info["ProfileName"] = bca_name
        bca_info["PhoneNumber"] = ph_number
        self.bca.append(bca_info)

        return status, ph_number
    # End of function --- "assign_ph_number_to_bca"

    # Start of API --- "assign_ph_number_to_user"
    def assign_ph_number_to_user(self, ph_status, _type="Domestic"):

        """
        `Description:` The API finds a phone number on the phone number page
        and assigns it to an user
        `Param1:` ph_status: Phone status
        `Param2:` _type: Phone type
        `Returns:` Status, Phone number
        `Created by:` Prasanna
        """
        # step1 - find an available phone number
        # step2 - click on assign
        # Step3 - Select an user
        # Step4 - Assign the phone number to the user
        status = True
        ph_number = None

        try:

            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            ph_number = self.get_phone_number_with_required_status(ph_status, _type)
            if not ph_number:
                raise BossExceptionHandle("Required Phone number not found")

            # step2 - click on assign
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Assign")

            # Step3 - Select destination type as User
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_User", loop_count=40)

            # Step4 - Assign the phone number to user
            # WIL(self.action_ele.select_from_dropdown_using_index, "Ph_System_Ph_Number_Op_Destination", 1)
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                'Ph_System_Ph_Number_Op_Destination', 1, loop_count=40)

            # Save the changes
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Save_Button")

            # Click on OK button
            WIL(self.wait, "BCA_OK_Button", {"ec":"text_to_be_present_in_element", "msg_to_verify":"OK"}, loop_count=40)
            WIL(self.action_ele.click_element, "BCA_OK_Button")
            time.sleep(3)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)

        return status, ph_number
    # End of function --- "assign_ph_number_to_user"

    # Start of function --- "verify_bca_on_required_prog_button_line"
    def verify_bca_on_required_prog_button_line(self, params):

        """
        `Description:` The API will verify a BCA on a program button line
        `Param1:` params: program button and BCA info
        `Returns:` True / False
        `Created by:` Prasanna
        """
        status = True
        try:

            # Modified by Prasanna: The element "SelectType" has been removed from the page
            # Step1. verify the type
            # if params["SelectType"]:
            #     self.wait("User_Ph_Prog_Button_Rows_Select_Type")
            #     text = self.query_ele.get_text_of_selected_dropdown_option("User_Ph_Prog_Button_Rows_Select_Type")
            #     if params["SelectType"] != text:
            #         raise BossExceptionHandle("Button Type not matching!")

            if params["SelectFunction"]:
                self.wait("User_Ph_Prog_Button_Rows_Select_Function")
                text = self.query_ele.get_text_of_selected_dropdown_option("User_Ph_Prog_Button_Rows_Select_Function")
                if params["SelectFunction"] != text:
                    raise BossExceptionHandle("Button Function not matching!")

            if (params["SelectType"] == "All" and
                    (params["SelectFunction"] == "Call Appearance" or params["SelectFunction"] == "Unused")):
                return True

            if params["SelectLongLabel"]:
                pass

            if params["SelectShortLabel"]:
                pass

            # Step2. Select from the Target section the required BCA in the Bridged Call Appearance drop down
            if params["SelectBCA"]:
                self.wait("User_Ph_Prog_Button_Select_Bca")
                bca_name = None
                for i in range(len(self.bca)):
                    if params["ProfileName"] in self.bca[i]["ProfileName"]:
                        bca_name = self.bca[i]["Extension"] + " : " + self.bca[i]["ProfileName"]
                text = self.query_ele.get_text_of_selected_dropdown_option("User_Ph_Prog_Button_Select_Bca")
                if bca_name and bca_name != text:
                    raise BossExceptionHandle("BCA name not matching!")

            # step3. Select call stack position
            if params["SelectCallStackPosition"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Call_Stack_Pos")
                text = self.query_ele.get_text_of_selected_dropdown_option("User_Ph_Prog_Button_Select_Bca_Call_Stack_Pos")
                if params["SelectCallStackPosition"] != text:
                    raise BossExceptionHandle("Call stack position not matching!")

            # step4. Select the option for Delay Before Audibly Ringing
            if params["SelectDelayBeforeAudiblyRing"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Delay_Before_Audibly_Ring")
                text = self.query_ele.get_text_of_selected_dropdown_option(
                    "User_Ph_Prog_Button_Select_Bca_Delay_Before_Audibly_Ring")
                if params["SelectDelayBeforeAudiblyRing"] != text:
                    raise BossExceptionHandle("DelayBeforeAudiblyRing not matching!")

            # step5. Select the option for Show Caller Id Alert
            if params["SelectShowCallerIDAlert"]:
                self.wait("User_Ph_Prog_Button_Select_Bca_Show_Caller_Id_Alert")
                text = self.query_ele.get_text_of_selected_dropdown_option(
                    "User_Ph_Prog_Button_Select_Bca_Show_Caller_Id_Alert")
                if params["SelectShowCallerIDAlert"] != text:
                    raise BossExceptionHandle("ShowCallerIDAlert not matching!")

            # step6. Select Auto Answer option
            if params["SelectAutoAnswer"]:
                pass
            # step7. Select No connected call action
            if params["SelectNoconnectedcallactionAnswerOnly"]:
                pass
            elif params["SelectNoconnectedcallactionDialTone"]:
                pass
            elif params["SelectNoconnectedcallactionDialExtn"]:
                pass
            elif params["SelectNoconnectedcallactionDialExternal"]:
                pass

            time.sleep(2)

        except (Exception, BossExceptionHandle) as e:
            status = False
            print(e)
        return status
    # End of function --- "verify_bca_on_required_prog_button_line"

    def click_profiles_element (self):

        status = True

        try:
            self.wait("OperationsPrimaryPartitionsProfiles")
            self.action_ele.click_element("OperationsPrimaryPartitionsProfiles")

        except (Exception, BossExceptionHandle) as e:
            status = False
            print e

        return status

    # Start of function --- "elements_on_primary_partition_profile_page"
    def elements_on_primary_partition_profile_page(self, params):

        """
        `Description:` The API find an element on a primary partition profile page
        `Param1:` params: Element information
        `Returns:` True / False
        `Created by:` Prasanna
        """
        status = True

        try:
            self.wait("OperationsPrimaryPartitionsProfiles")
            self.action_ele.click_element("OperationsPrimaryPartitionsProfiles")

            self.wait("PrimaryPartitionFirstName")
            self.action_ele.input_text("PrimaryPartitionFirstName", params["FirstName"])

            if params["Extension"]:
                self.wait("PrimaryPartitionExtension")
                self.action_ele.input_text("PrimaryPartitionExtension", params["Extension"])
            elif params["PhoneNumber"]:
                self.wait("PrimaryPartitionPhoneNumber")
                self.action_ele.input_text("PrimaryPartitionPhoneNumber", params["PhoneNumber"])

            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

            # Get the row from the grid
            profile_grid = self._browser.element_finder("Grid_Canvas")
            if not profile_grid:
                raise BossExceptionHandle("Grid canvas not selected in the Grid")
            fields = profile_grid.find_elements_by_tag_name("div")
            if not fields:
                raise BossExceptionHandle("No element selected!")

            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

            if (params["FirstName"]) and fields[2].text != params["FirstName"]:
                raise BossExceptionHandle("Fields are not matching")
            elif params["Extension"]:
                if fields[5].text != params["Extension"]:
                    raise BossExceptionHandle("Fields are not matching")
            elif (params["PhoneNumber"]) and fields[7].text != params["PhoneNumber"]:
                    raise BossExceptionHandle("Fields are not matching")

            fields[1].click()

            # Reset the filtered fields
            self.wait("PrimaryPartitionFirstName")
            self.action_ele.input_text("PrimaryPartitionFirstName", "")

            self.wait("PrimaryPartitionPhoneNumber")
            self.action_ele.input_text("PrimaryPartitionPhoneNumber", "")

            self.wait("PrimaryPartitionExtension")
            self.action_ele.input_text("PrimaryPartitionExtension", "")

        except (Exception, BossExceptionHandle) as e:
            status = False
            print e

        return status

    ##########################################################
    ####
    # Start - - Mahesh
    ####
    ##########################################################
    def create_bca_from_programmable_button_page(self, params):
        """
        `Description:` The API creates a BCA on a program button page
        `Param1:` params: BCA info
        `Returns:` True / False
        `Created by:` Mahesh
        """
        status = True
        try:
            self.select_type_and_function_on_program_page(params)
            self.wait("User_Ph_Prog_Button_Create_BCA")
            self.action_ele.click_element('User_Ph_Prog_Button_Create_BCA')
            self.wait("BCA_Profile_Name")
            if not self.add_copy_edit_bca(params, "Add"):
                raise BossExceptionHandle("Create BCA from programmable button failed!!")

        except Exception, e:
            print(e.message)
            status = False

        return status

    ##########################################################
    ####
    # End - - Mahesh
    ####
    ##########################################################

    ##########################################################
    ####
    # Start - - Vasuja
    # old name of the function - "change_destination_type_of_TN_from_BCA"
    ####
    ##########################################################
    def edit_dnis_on_phone_numbers_page(self, param):
        """
        `Description:` Edit a phone number on 'Phone System--> Phone Numbers' page
        `Param:` Type of destination. Eg; Auto Attendant, Hunt Group, Bridged Call Appearance, Unassign
        `Returns:` status - True / False
        `Created by:` Vasuja
        'Modified By' Palla Surya Kumar
        """
        # Assumption is that the control is already in Phone System--> Phone Numbers page
        from collections import defaultdict
        param = defaultdict(lambda: '', param)
        status = True

        try:

            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_TN_edit")

            if param["auto_Attendant"]:
                # change the destination type to Auto Attendant
                WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_AutoAttendant")
                time.sleep(1)
                WIL(self.action_ele.select_from_dropdown_using_text,
                             "Ph_System_Ph_Number_Op_Destination", param['auto_Attendant'])
                time.sleep(1)

            elif param["hunt_Group"]:
                # change the destination type to Hunt Group
                WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_HuntGroup")
                time.sleep(1)
                WIL(self.action_ele.select_from_dropdown_using_text,
                             "Ph_System_Ph_Number_Op_Destination", param['hunt_Group'])
                time.sleep(1)

            elif param["bridged_Call_Appearance_name"]:
                # change the destination type to Bridged Call Appearance
                WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_Bca")
                time.sleep(1)
                WIL(self.action_ele.select_from_dropdown_using_text,
                             "Ph_System_Ph_Number_Op_Destination", param['bridged_Call_Appearance_name'])
                time.sleep(1)
            elif param["Unassign"]:
                # change the destination type to Unassign
                WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_Unassign")
                time.sleep(2)
            elif param["User"]:

                WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_User")

                time.sleep(1)
                WIL(self.action_ele.select_from_dropdown_using_index, "Ph_System_Ph_Number_Op_Destination", 1)
                time.sleep(1)
                param["User"] = \
                    WIL(self.query_ele.get_text_of_selected_dropdown_option,
                        "Ph_System_Ph_Number_Op_Destination", return_value=True)
            # Save the changes
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Save_Button")
            time.sleep(1)
            try:
                WIL(self._browser.element_finder, "PhoneSystem_Edit_Save_Success_Msg", loop_count=40)
                print("Message 'The phone number was assigned successfully' is displayed")
                WIL(self.wait, "BCA_OK_Button", {'ec': "text_to_be_present_in_element", 'msg_to_verify': "OK"})
                WIL(self.action_ele.click_element, "BCA_OK_Button", loop_count=40)
                self._browser._browser.refresh()
            except Exception:
                WIL(self.action_ele.click_element, "BCA_OK_Button")
                WIL(self.action_ele.click_element, "PhoneSystem_Edit_Cancel_Button")
                WIL(self.action_ele.click_element, "BCA_Yes_Button")
                time.sleep(4)
                raise BossExceptionHandle("message on page not as required!")

        except (Exception, BossExceptionHandle) as err:
            status = False
            print("Could not change destination type")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        time.sleep(4)
        return status

        # End of function "change_destination_type"

    ##########################################################
    ####
    # End - - Vasuja
    ####
    ##########################################################
