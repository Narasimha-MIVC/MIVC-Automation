"""Module for creating and verifying BCA
   File: BCA_Operations.py
   Author: Prasanna
"""
import os
import sys
import time
import inspect

import stafenv

from web_wrappers import selenium_wrappers as base


__author__ = "Prasanna"


class _Users(object):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        # self._browser = args[0]
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def get_single_user_info_from_user_grid(self, user_info):
        """
            `Description:` This API will return a user info from the user grid
            `Param1:` user_info: a dictionary to capture the user information
            `Created by:` Prasanna
        """
        # Steps:
        # 1. get the first user info from the grid. (we are already in users page)
        # 2. update the user_info parameter
        # 3. return status
        status = False

        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

            self.action_ele.explicit_wait("std2_admin_users_users_grid")
            grid_table = self._browser.element_finder("std2_admin_users_users_grid")
            if grid_table:
                # Get the rows
                grid_table_rows = grid_table.find_elements_by_tag_name('tr')

                if grid_table_rows and len(grid_table_rows) > 1:
                    columns = grid_table_rows[1].find_elements_by_tag_name("td")
                    if columns:
                        status = True
                        user_info.update({"FIRST NAME": columns[1].text,
                                          "LAST NAME": columns[2].text,
                                          "EXTENSION": columns[3].text})

        except Exception as e:
            print(e.message)

        return status

    
    def add_new_std2user(self, Firstname, isdidenable):
        status = False
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.explicit_wait("add_user_button")
            self.action_ele.click_element("add_user_button")
            self.action_ele.explicit_wait("USER_First_Name")
            self.action_ele.input_text("USER_First_Name", Firstname)
            Lastname="st"
            self.action_ele.input_text("user_Last_Name", Lastname)
            #user_info.update({"lastname",LastName})
            #ph_num = self.query_ele.get_text("User_Extension")
            ph_num = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_dn_DN')[0].value")
            print(ph_num)
            client_user_name = Firstname + "@sco.com"
            self.action_ele.input_text("client_user_name", client_user_name)
            if(isdidenable):
                self.action_ele.click_element("user_did_enable")
                did_num=self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_did_range_digits')[0].value")
                did_num=int(did_num)+3
                did="+" + str(did_num)
                print(did)
                self.action_ele.input_text("user_did_range", did)
            self.action_ele.click_element("save_user")
            time.sleep(3)
            status = True
        except (Exception) as err:
            print(err)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return  ph_num,Firstname,Lastname,status
# end of add_std2_user

 # Deletion of  one STD2 user

    def delete_std2_user(self,FirstName):
        deleted= False
        try:
            #self._browser.refresh_browser()
            self._browser._browser.refresh()
            # Select the BCA from the Grid
            self.action_ele.click_element("user_search_box")
            self.action_ele.explicit_wait("search_user_first_name")
            self.action_ele.input_text("search_user_first_name", FirstName)
            time.sleep(1)
            self.action_ele.press_key("search_user_first_name", "ENTER")
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
            if 0 != len(columns) and \
                    ((self.query_ele.get_element_attribute("first_row_user_first_name", "title")) == FirstName):
                print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name", "title"))
                self.action_ele.click_element("first_row_user_first_name")
                deleted = True

            time.sleep(2)
            # Delete the selected User

            if deleted:
                print("### Deleting the STD2 User")

                self.action_ele.explicit_wait("Delete_std2_user_Button")
                self.action_ele.click_element("Delete_std2_user_Button")
                if self._browser.elements_finder("user_confirmation_popup"):
                    self.action_ele.click_element("OK_confirmation_button")
                deleted = True
                time.sleep(2)

            self.action_ele.clear_input_text("search_user_first_name")
            time.sleep(1)
            self.action_ele.press_key("search_user_first_name", "ENTER")
            # self._browser.refresh_browser()
            self._browser._browser.refresh()
            time.sleep(1)

        except Exception as err:
            deleted = False
            print("Deleting the User info failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return deleted

# End of delete_std2_user function

# verify one STD2 user info

    def verify_std2_user(self, FirstName):

        """
            `Description:` This function verifies the added/modified ST D2 USER
            `Param1:` FirstName: contain User's First name
            `Returns:` True / False
            `Created by:` Priyanka
        """

        # Assumption is that the control is already in Admin->User->Users page
        verified = True
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()

            # Select the User from the Grid
            self.action_ele.click_element("user_search_box")
            self.action_ele.explicit_wait("search_user_first_name")
            self.action_ele.input_text("search_user_first_name", FirstName)
            time.sleep(1)
            self.action_ele.press_key("search_user_first_name", "ENTER")
            if self._browser.elements_finder("user_confirmation_popup"):
                self.action_ele.click_element("OK_confirmation_button")
            # Retrieve the user info from the grid table. In this case only one
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
                print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name","title"))
                print("Last Name: %s" % self.query_ele.get_element_attribute("first_row_user_last_name","title"))
                print("Extension: %s" % self.query_ele.get_element_attribute("first_row_user_extension","title"))
                if (self.query_ele.get_element_attribute("first_row_user_first_name","title")) != FirstName:
                    raise Exception("Verifying the std2 User info failed")

            else:
                raise Exception("No element found on the grid")

            self.action_ele.clear_input_text("search_user_first_name")
            time.sleep(1)
            self.action_ele.press_key("search_user_first_name", "ENTER")
            # self._browser.refresh_browser()
            self._browser._browser.refresh()
            time.sleep(1)
        except Exception as err:
            verified = False
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return verified
    # End of function -- verify_std2 user

    # verify one STD2 user info

    def update_std2_user(self, **params):

        """
            `Description:` This function update the added/modified ST D2 USER
            `Param1:` FirstName: contain User's First name
            `Returns:` True / False
            `Created by:` Priyanka
        """

        # Assumption is that the control is already in Admin->User->Users page
        updated = False
        ph_num = None
        new_name = None
        user_email = None

        try:
            # Select the BCA from the Grid
            self.action_ele.explicit_wait("user_search_box")
            self.action_ele.click_element("user_search_box")
            self.action_ele.explicit_wait("search_user_first_name")
            self.action_ele.input_text("search_user_first_name", params["User_FirstName"])
            time.sleep(1)
            self.action_ele.press_key("search_user_first_name", "ENTER")
            # Retrieve the user info from the grid table. In this case only one
            self.action_ele.explicit_wait("Search_Grid_Canvas")
            grid_table_row = self._browser.element_finder("Search_Grid_Canvas")
            time.sleep(2)
            if grid_table_row:
                print("##########")
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('td')

                print("Number of columns: %s" % str(len(columns)))
                print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name", "title"))

                # verify the columns
                if (0 != len(columns) and
                        ((self.query_ele.get_element_attribute("first_row_user_first_name", "title")) ==
                             params["User_FirstName"])):
                    print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name", "title"))
                    self.action_ele.click_element("first_row_user_first_name")

            time.sleep(2)
            # Update the selected User

            if params["UpdatedFirstName"]:
                self.action_ele.explicit_wait("USER_First_Name")
                self.action_ele.input_text("USER_First_Name", params["UpdatedFirstName"])
            if params["UpdatedLastName"]:
                self.action_ele.explicit_wait("user_Last_Name")
                self.action_ele.input_text("user_Last_Name", params["UpdatedLastName"])
            if params["Extension"]:
                self.action_ele.explicit_wait("User_Extension")
                #extn = "4" + params["Extension"]
                #print(extn)
                #self.action_ele.input_text("User_Extension", extn)
            if params["Email"]:
                self.action_ele.explicit_wait("USER_First_Name")
                email = params["Email"] + "@sco.com"
                self.action_ele.input_text("USER_First_Name", email)
            if params["updateDid"]:
                self.action_ele.click_element("user_did_setting1")
                if params["updateDid"]=="update":
                    did_num = self.query_ele.get_value_execute_javascript(
                        "document.getElementsByName('user_did_range_digits')[0].value")
                    did_num = int(did_num) + 1
                    did = "+" + str(did_num)
                    print(did)
                    self.action_ele.input_text("user_did_range", did)
                else:
                    self.action_ele.click_element("user_did_enable")
            self.action_ele.click_element("save_user")
            time.sleep(2)
            updated = True
            fname = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_FirstName')[0].value")
            lname = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_LastName')[0].value")
            new_name = fname + " " + lname
            print (new_name)
            ph_num = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_dn_DN')[0].value")
            print(ph_num)
            user_email = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_EmailAddress')[0].value")
            print(user_email)
        except Exception as err:
                updated = False
                print(err.message)
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return ph_num, new_name, user_email, updated
    # End of function -- update_std2 user

    # update STD2 user info

    def retrieve_std2_user_did(self , first_name):
        status = False
        did_num = None
        try:
            self.action_ele.explicit_wait("user_search_box")
            self.action_ele.click_element("user_search_box")
            self.action_ele.explicit_wait("search_user_first_name")
            self.action_ele.input_text("search_user_first_name", first_name)
            time.sleep(1)
            self.action_ele.press_key("search_user_first_name", "ENTER")
            # Retrieve the user info from the grid table. In this case only one
            self.action_ele.explicit_wait("Search_Grid_Canvas")
            grid_table_row = self._browser.element_finder("Search_Grid_Canvas")
            time.sleep(2)
            if grid_table_row:
                print("##########")
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('td')

                print("Number of columns: %s" % str(len(columns)))
                print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name", "title"))

                # verify the columns
            if (0 != len(columns) and (
                        (self.query_ele.get_element_attribute("first_row_user_first_name", "title"))
                        == first_name)):
                print("First Name: %s" % self.query_ele.get_element_attribute("first_row_user_first_name", "title"))
                self.action_ele.click_element("first_row_user_first_name")
            time.sleep(2)
            # collect the did of the user
            self.action_ele.click_element("user_did_setting1")
            did_num = self.query_ele.get_value_execute_javascript(
                "document.getElementsByName('user_did_range_digits')[0].value")
            did_num = int(did_num)
            print(did_num)
            did_num = str(did_num)
            print(did_num)
            status = True
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return did_num, status
