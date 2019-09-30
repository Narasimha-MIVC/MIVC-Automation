"""Module for creating and verifying BCA
   File: BCA_Operations.py
   Author: Prasanna
"""

import os
import sys
import time
import inspect

from web_wrappers import selenium_wrappers as base

__author__ = "Priyanka"


class BossExceptionHandle(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Error Info: %s" % self.msg


class Bca(object):
    """All D2 packages"""
    def __init__(self, *args, **kwargs):
        # self._browser = args[0]
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        
    def add_std2_bca_user(self, **params):
        try:
            status = False
            bca_user_name= params["user_name"]
            self.action_ele.click_element("add_bca_user_button")
            if params['user_name']:
                self.action_ele.explicit_wait("bca_user_Name")
                self.action_ele.clear_input_text("bca_user_Name")
                time.sleep(2)
                self.action_ele.input_text("bca_user_Name", params["user_name"])
            # bca_ph_num = self.query_ele.get_text('bca_user_Extension')
            bca_ph_num = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('bca_dn_attributes_DN')[0].value")
            print(bca_ph_num)
            if params['ph_num']:
                self.action_ele.input_text("bca_user_backup_Extension", params["ph_num"])
            else:
                raise BossExceptionHandle("Backup Extension field is empty")
            if params['enable_did']:
                self.action_ele.click_element("bca_user_did_enable")
                did_num=params['user_did']
                print(str(did_num))
                did_num=int(did_num)+1
                print(did_num)
                did_check = self.query_ele.get_value_execute_javascript(
                    "document.getElementsByName('bca_did_range_digits')[0].value")
                print(did_check)
                #did_num = int(did_num) + 3
                did = "+" + str(did_num)
                print(did)
                self.action_ele.input_text("bca_user_did_range", did)

            self.action_ele.click_element("save_user")
            time.sleep(1)
            status = True
        except (Exception, BossExceptionHandle) as err:
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return bca_ph_num,bca_user_name,status


    # verify one STD2 BCA user info
    def verify_std2_bca_user(self, FirstName):

        """
            `Description:` This function verifies the added/modified ST D2 USER
            `Param1:` FirstName: contain User's First name
            `Returns:` True / False
            `Created by:` Priyanka
        """
        # Assumption is that the control is already in Admin->User->Users page
        verified = True
        try:
            # Select the BCA from the Grid
            self.action_ele.click_element("user_search_box")
            self.action_ele.explicit_wait("search_bca_user_name")
            self.action_ele.input_text("search_bca_user_name", FirstName)
            time.sleep(1)
            self.action_ele.press_key("search_bca_user_name", "ENTER")
            # Retrieve the BCA info from the grid table. In this case only one
            self.action_ele.explicit_wait("Search_Grid_Canvas")
            grid_table = self._browser.elements_finder("Search_Grid_Canvas")
            print(len(grid_table))
            if len(grid_table) == 1:
                print("##########")
                # Get the fields
                columns = grid_table[0].find_elements_by_tag_name('td')
                time.sleep(1)
                print("Number of columns: %s" % str(len(columns)))

                # verify the columns
            if 0 != len(columns):
                print("First Name: %s" % self.query_ele.get_element_attribute("first_row_bca_user_name", "title"))
                print("Extension: %s" % self.query_ele.get_element_attribute("first_row_bca_user_extension", "title"))
                if ((self.query_ele.get_element_attribute("first_row_bca_user_name", "title")) != FirstName):
                    raise BossExceptionHandle("Verifying the std2 User info failed")

            else:
                raise BossExceptionHandle("No element found on the grid")

            self.action_ele.clear_input_text("search_bca_user_name")
            time.sleep(1)
            self.action_ele.press_key("search_bca_user_name", "ENTER")
            #self._browser.refresh_browser()
            self._browser._browser.refresh()
            time.sleep(1)

        except (Exception, BossExceptionHandle) as err:
            verified = False
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return verified
   # End of function -- verify_std2_bca user

# start of delete_std2_bca_user
    def delete_std2_bca_user(self, FirstName):
        deleted = False
        try:
                # Select the BCA from the Grid
                print(FirstName)
                # import pdb;
                # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                self.action_ele.click_element("user_search_box")
                self.action_ele.explicit_wait("search_bca_user_name")
                self.action_ele.input_text("search_bca_user_name", FirstName)
                time.sleep(1)
                self.action_ele.press_key("search_bca_user_name", "ENTER")
                # Retrieve the user info from the grid table. In this case only one
                self.action_ele.explicit_wait("Search_Grid_Canvas")
                grid_table_row = self._browser.element_finder("Search_Grid_Canvas")
                time.sleep(2)
                print(grid_table_row)
                if grid_table_row:
                    print("##########")
                    # Get the fields
                    columns = grid_table_row.find_elements_by_tag_name('td')

                    print("Number of columns: %s" % str(len(columns)))
                    print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name", "title"))

                    # verify the columns
                if (0 != len(columns) and (
                    (self.query_ele.get_element_attribute("first_row_bca_user_name", "title")) == FirstName)):
                    print("First Name: %s" % self.query_ele.get_element_attribute("first_row_bca_user_name", "title"))
                    self.action_ele.click_element("first_row_user_first_name")
                    deleted = True

                time.sleep(2)
                # Delete the selected User

                if deleted:
                    print("### Deleting the STD2 User")

                    self.action_ele.explicit_wait("Delete_std2_bca_user_Button")
                    self.action_ele.click_element("Delete_std2_bca_user_Button")
                    if (self._browser.elements_finder("user_confirmation_popup")):
                        self.action_ele.click_element("OK_confirmation_button")
                    deleted = True
                    time.sleep(2)

                self.action_ele.clear_input_text("search_bca_user_name")
                self.action_ele.press_key("search_bca_user_name", "ENTER")
                # Select the User from the Grid
                #self._browser.refresh_browser()
                self._browser._browser.refresh()
                time.sleep(1)

        except (Exception, BossExceptionHandle) as err:
            deleted = False
            print("Deleting the BCA User info failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return deleted

    # End of delete_std2_bca_user function

    def update_std2_bca_user(self, **params):

        """
            `Description:` This function update the added/modified ST D2 BCA USER
            `Param1:` FirstName: contain BCA User's First name
            `Returns:` True / False
            `Created by:` Priyanka
        """

        # Assumption is that the control is already in Admin->Feature->User->Users page
        updated = False
        bca_username = None
        try:
            # Select the BCA from the Grid
            self.action_ele.explicit_wait("user_search_box")
            self.action_ele.click_element("user_search_box")
            self.action_ele.explicit_wait("search_bca_user_name")
            self.action_ele.input_text("search_bca_user_name", params["User_Name"])
            time.sleep(1)
            self.action_ele.press_key("search_bca_user_name", "ENTER")
            # Retrieve the user info from the grid table. In this case only one
            self.action_ele.explicit_wait("Search_Grid_Canvas")
            grid_table_row = self._browser.element_finder("Search_Grid_Canvas")
            time.sleep(2)
            if grid_table_row:
                print("##########")
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('td')

                print("Number of columns: %s" % str(len(columns)))
                print("Bca User Name: %s" % self.query_ele.get_element_attribute("first_row_bca_user_name", "title"))

                # verify the columns
            if (0 != len(columns) and (
                (self.query_ele.get_element_attribute("first_row_bca_user_name", "title")) == params["User_Name"])):
                print("Bca User Name: %s" % self.query_ele.get_element_attribute("first_row_bca_user_name", "title"))
                self.action_ele.click_element("first_row_bca_user_name")

            time.sleep(2)
            # Update the selected User

            if params["UpdatedName"]:
                self.action_ele.explicit_wait("bca_user_Name")
                self.action_ele.input_text("bca_user_Name", params["UpdatedName"])
            if params["Extension"]:
                self.action_ele.explicit_wait("bca_user_Extension")
                #extn = "4" + params["Extension"]
                #print(extn)
                #self.action_ele.input_text("User_Extension", extn)
            if params["updateDid"]:
                self.action_ele.click_element("user_did_setting1")
                if(params["updateDid"]=="update"):
                    did_num = self.query_ele.get_value_execute_javascript(
                        "document.getElementsByName('bca_did_range_digits')[0].value")
                    did_num = int(did_num) + 1
                    did = "+" + str(did_num)
                    print(did)
                    self.action_ele.input_text("bca_user_did_range", did)
                elif(params["updateDid"]=="assign"):
                    #self.action_ele.click_element("user_did_setting")
                    self.action_ele.click_element("bca_user_did_enable")
                    did_num = int(params['didVal'])
                    did = "+" + str(did_num)
                    print(did)
                    self.action_ele.input_text("bca_user_did_range", did)

                else:
                    self.action_ele.click_element("bca_user_did_enable")
            self.action_ele.click_element("save_user")
            time.sleep(2)
            updated = True
            bca_username = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('bca_Description')[0].value")
            self.action_ele.clear_input_text("search_bca_user_name")
            time.sleep(1)
            self.action_ele.press_key("search_bca_user_name", "ENTER")
            #self._browser.refresh_browser()
            self._browser._browser.refresh()
            time.sleep(1)

        except (Exception, BossExceptionHandle) as err:
                updated = False
                print(err)
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return bca_username,updated
            # End of function -- update_std2_bca user

        # update STD2 bca user info