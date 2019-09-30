"""Module for actions on the Personal Information page"""

import os
import sys
import time
import datetime
import inspect
from selenium.webdriver.support.ui import Select

# For console logs while executing ROBOT scripts
from robot.api.logger import console
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
import web_wrappers.selenium_wrappers as base

__author__ = "Kenash Kanakaraj"

class PersonalInformation(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 30

    def switch_tab(self, tab_name):
        """
        `Description:`  Switch to the selected tab

        `Param:` tabName

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            if tab_name == "Contact":
                tab_map = "pi_tab_contact"
            elif tab_name == "Roles and Permissions":
                tab_map = "pi_tab_roles"
            elif tab_name == "Notification Preferences":
                tab_map = "pi_tab_notifications"
            else:
                return status
            self.action_ele.click_element(tab_map + "_selector")
            self.action_ele.explicit_wait(tab_map)
            status = True
            return status

        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def verify_contact_tab(self):
        """
        `Description:` Verify the Contact tab

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        status = False
        try:
            self.assert_ele.page_should_contain_element("pi_tab_contact_MitelLogIn")
            self.action_ele.explicit_wait("pi_tab_contact_MitelLogIn", ec="text_to_be_present_in_element",
                                          msg_to_verify="Mitel Log In")
            self.assert_ele.page_should_contain_element("pi_tab_contact_username")
            self.assert_ele.page_should_contain_element("pi_tab_contact_lastLogin_label")
            self.assert_ele.page_should_contain_element("pi_tab_contact_lastLogin_display")
            self.assert_ele.page_should_contain_element("pi_tab_contact_changePasswordButton")
            self.assert_ele.page_should_contain_element("pi_tab_contact_ContactInformation")
            self.action_ele.explicit_wait("pi_tab_contact_ContactInformation", ec="text_to_be_present_in_element",
                                          msg_to_verify="Contact Information")
            self.action_ele.click_element("pi_tab_contact_firstName")
            self.action_ele.explicit_wait("pi_tab_contact_firstName_cancel")
            self.action_ele.click_element("pi_tab_contact_firstName_cancel")
            self.action_ele.click_element("pi_tab_contact_lastName")
            self.action_ele.explicit_wait("pi_tab_contact_lastName_cancel")
            self.action_ele.click_element("pi_tab_contact_lastName_cancel")
            self.action_ele.click_element("pi_tab_contact_title")
            self.action_ele.explicit_wait("pi_tab_contact_title_cancel")
            self.action_ele.click_element("pi_tab_contact_title_cancel")
            self.action_ele.click_element("pi_tab_contact_businessEmail")
            self.action_ele.explicit_wait("pi_tab_contact_businessEmail_cancel")
            self.action_ele.click_element("pi_tab_contact_businessEmail_cancel")
            self.action_ele.click_element("pi_tab_contact_personalEmail")
            self.action_ele.explicit_wait("pi_tab_contact_personalEmail_cancel")
            self.action_ele.click_element("pi_tab_contact_personalEmail_cancel")
            self.action_ele.click_element("pi_tab_contact_cellPhone")
            self.action_ele.explicit_wait("pi_tab_contact_cellPhone_cancel")
            self.action_ele.click_element("pi_tab_contact_cellPhone_cancel")
            self.action_ele.click_element("pi_tab_contact_homePhone")
            self.action_ele.explicit_wait("pi_tab_contact_homePhone_cancel")
            self.action_ele.click_element("pi_tab_contact_homePhone_cancel")
            self.action_ele.explicit_wait("pi_tab_contact_Location", ec="text_to_be_present_in_element",
                                          msg_to_verify="Location")
            self.action_ele.mouse_hover("pi_tab_contact_Location_help")
            tooltip = self.query_ele.get_element_attribute("pi_tab_contact_Location_help", "tooltip")
            if not tooltip or tooltip.strip() != "Please contact Mitel Support to change the location of a user":
                return status
            field = self._browser.elements_finder("pi_tab_contact_location_input")
            if len(field):
                return status
            self.action_ele.explicit_wait("pi_tab_contact_MyServices", ec="text_to_be_present_in_element",
                                          msg_to_verify="My Services")
            self.assert_ele.page_should_contain_element("pi_tab_contact_grid_filter_tn")
            self.assert_ele.page_should_contain_element("pi_tab_contact_grid_filter_serviceType")
            self.assert_ele.page_should_contain_element("pi_tab_contact_grid_filter_activationDate")
            self.action_ele.explicit_wait("pi_tab_contact_AddFeature", ec="text_to_be_present_in_element",
                                          msg_to_verify="Add a feature")
            self.assert_ele.page_should_contain_element("pi_tab_contact_profile")
            self.assert_ele.page_should_contain_element("pi_tab_contact_feature")
            self.assert_ele.page_should_contain_element("pi_tab_contact_activationDate")
            self.assert_ele.page_should_contain_element("pi_tab_contact_addFeatureButton")
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def verify_roles_permissions_tab(self):
        """
        `Description:` Verify the Roles and Permissions tab

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        status = False
        try:
            self.action_ele.explicit_wait("pi_tab_roles_MitelRoles", ec="text_to_be_present_in_element",
                                          msg_to_verify="Mitel Roles")
            self.assert_ele.page_should_contain_element("pi_tab_roles_roles")
            self.assert_ele.page_should_contain_element("pi_tab_roles_addRoleButton")
            self.assert_ele.page_should_contain_element("pi_tab_roles_rolesGrid")
            self.action_ele.explicit_wait("pi_tab_roles_MitelPermissions", ec="text_to_be_present_in_element",
                                          msg_to_verify="Mitel Permissions")
            rows = self._browser.elements_finder("pi_tab_roles_permissionsTable_rows")
            if not rows or not len(rows):
                return status
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def verify_notification_preferences_tab(self):
        """
        `Description:` Verify the Notification Preferences tab.

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        status = False
        try:
            print("NO AVAILABLE TESTS FOR THIS TAB")
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_role(self, role):
        """
        `Description:`  Add a role to the user

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            before_total = 0
            totals = self._browser.elements_finder("pi_tab_roles_slickgrid_totals")
            for total in totals:
                before_total = total.text
            before_rows = int("".join([i for i in before_total if i.isdigit()]))
            after_rows = before_rows + 1
            after_total = before_total.replace(str(before_rows), str(after_rows))
            if role == "Decision Maker":
                option = "pi_tab_roles_roles_dm"
                scope = "pi_tab_roles_rolesGrid_DM_"
            elif role == "Phone Manager":
                option = "pi_tab_roles_roles_pm"
                scope = "pi_tab_roles_rolesGrid_PM_"
            elif role == "Billing":
                option = "pi_tab_roles_roles_billing"
                scope = "pi_tab_roles_rolesGrid_B_"
            elif role == "Emergency":
                option = "pi_tab_roles_roles_emergency"
                scope = "pi_tab_roles_rolesGrid_E_"
            elif role == "Partner":
                option = "pi_tab_roles_roles_partner"
                scope = "pi_tab_roles_rolesGrid_P_"
            elif role == "Technical":
                option = "pi_tab_roles_roles_technical"
                scope = "pi_tab_roles_rolesGrid_T_"
            else:
                return status
            self.action_ele.click_element("pi_tab_roles_roles")
            self.action_ele.click_element(option)
            self.action_ele.click_element("pi_tab_roles_addRoleButton")
            self.action_ele.explicit_wait("pi_tab_roles_slickgrid_totals", ec="text_to_be_present_in_element",
                                          msg_to_verify=after_total)
            scope_account = self._browser.elements_finder(scope + "A")
            if not scope_account or not scope_account[0].is_selected() or not scope_account[0].is_enabled():
                return status
            scope_location = self._browser.elements_finder(scope + "L")
            if not scope_location:
                return status

            if role != "Decision Maker" and role != "Billing":
                if not scope_location[0].is_enabled():
                    return status
                self.action_ele.click_element(scope + "L")
                self.action_ele.explicit_wait("pi_tab_roles_roles_error", ec="text_to_be_present_in_element",
                                              msg_to_verify="One or more locations are not specified")
                scope_select = self._browser.elements_finder(scope + "L_select")
                if not scope_select or not scope_select[0].is_enabled():
                    return status
                time.sleep(2)
                self.action_ele.click_element(scope + "A")
            else:
                if scope_location[0].is_enabled():
                    return status
            cells = self._browser.elements_finder("pi_tab_roles_slickgrid_cells")
            for cell in cells:
                if cell.text == role:
                    status = True
                    break
            time.sleep(1)
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def change_role_location(self, role, location):
        """
        `Description:`  Changes the location of the role for the user

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            if role == "Decision Maker":
                scope = "pi_tab_roles_rolesGrid_DM_"
            elif role == "Phone Manager":
                scope = "pi_tab_roles_rolesGrid_PM_"
            elif role == "Billing":
                scope = "pi_tab_roles_rolesGrid_B_"
            elif role == "Emergency":
                scope = "pi_tab_roles_rolesGrid_E_"
            elif role == "Partner":
                scope = "pi_tab_roles_rolesGrid_P_"
            elif role == "Technical":
                scope = "pi_tab_roles_rolesGrid_T_"
            else:
                return status
            self.action_ele.click_element(scope + "L")
            time.sleep(1)
            scope_select = self._browser.elements_finder(scope + "L_select")
            if not scope_select or not scope_select[0].is_enabled():
                return status
            dropdown = Select(scope_select[0])
            dropdown.select_by_visible_text(location)
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def remove_role_location(self, role):
        """
        `Description:`  Removes the location of the role for the user and sets scope to account

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            if role == "Decision Maker":
                scope = "pi_tab_roles_rolesGrid_DM_"
            elif role == "Phone Manager":
                scope = "pi_tab_roles_rolesGrid_PM_"
            elif role == "Billing":
                scope = "pi_tab_roles_rolesGrid_B_"
            elif role == "Emergency":
                scope = "pi_tab_roles_rolesGrid_E_"
            elif role == "Partner":
                scope = "pi_tab_roles_rolesGrid_P_"
            elif role == "Technical":
                scope = "pi_tab_roles_rolesGrid_T_"
            else:
                return status
            self.change_role_location(role, "")
            self.action_ele.explicit_wait("pi_tab_roles_roles_error")
            self.action_ele.click_element(scope + "A")
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def delete_role(self, role):
        """
        `Description:`  Delete a role from the user

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            before_total = 0
            totals = self._browser.elements_finder("pi_tab_roles_slickgrid_totals")
            for total in totals:
                before_total = total.text
            before_rows = int("".join([i for i in before_total if i.isdigit()]))
            after_rows = before_rows - 1
            after_total = before_total.replace(str(before_rows), str(after_rows))
            if role == "Decision Maker":
                option = "pi_tab_roles_rolesGrid_DM_delete"
            elif role == "Phone Manager":
                option = "pi_tab_roles_rolesGrid_PM_delete"
            elif role == "Billing":
                option = "pi_tab_roles_rolesGrid_B_delete"
            elif role == "Emergency":
                option = "pi_tab_roles_rolesGrid_E_delete"
            elif role == "Partner":
                option = "pi_tab_roles_rolesGrid_P_delete"
            elif role == "Technical":
                option = "pi_tab_roles_rolesGrid_T_delete"
            else:
                return status
            self.action_ele.click_element(option)
            self.action_ele.explicit_wait("pi_tab_roles_slickgrid_totals", ec="text_to_be_present_in_element",
                                          msg_to_verify=after_total)
            cells = self._browser.elements_finder("pi_tab_roles_slickgrid_cells")
            for cell in cells:
                if cell.text == role:
                    return status
            status = True
            time.sleep(1)
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def change_user_data(self, field, value, action):
        """
        `Description:`  Change the user's data

        `Param1:`   field - name of field to change

        `Param2:`   value - value to change the field to

        `Param3:`   action - button to be clicked (submit/cancel)

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        print("value: " + value)
        status = False
        try:
            if field.lower() == "first name":
                base_selector = "pi_tab_contact_firstName"
            elif field.lower() == "last name":
                base_selector = "pi_tab_contact_lastName"
            elif field.lower() == "title":
                base_selector = "pi_tab_contact_title"
            elif field.lower() == "business email":
                base_selector = "pi_tab_contact_businessEmail"
            elif field.lower() == "personal email":
                base_selector = "pi_tab_contact_personalEmail"
            elif field.lower() == "mobile phone":
                base_selector = "pi_tab_contact_cellPhone"
            elif field.lower() == "home phone":
                base_selector = "pi_tab_contact_homePhone"
            elif field.lower() == "location":
                base_selector = "pi_tab_contact_location"
            else:
                return status
            if not action.lower() == "save" and not field.lower() == "cancel":
                return status

            required = False
            if required:
                required_selector = "pi_tab_contact_inputError"
            else:
                required_selector = ""
            status = self.input_in_place(base_selector, value, action.lower(), required_selector)
            return status
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def input_in_place(self, base_selector, new_value, action, required_selector):
        """
        `Description:`  Global function to make changes to edit-in-place type fields

        `Param1:`   base_selector - mapped xpath name of the display field

        `Param2:`   new_value - value to change the field to

        `Param3:`   action - button to be clicked (save/cancel)

        `Param4:`   required_selector - mapped xpath name of the invalid input message

        `Returns:` status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            input_selector = base_selector + "_input"
            submit_selector = base_selector + "_submit"
            cancel_selector = base_selector + "_cancel"

            self.action_ele.click_element(base_selector)
            self.action_ele.explicit_wait(input_selector)
            old_value = self.query_ele.get_value(input_selector)

            self.action_ele.input_text(input_selector, new_value)
            if action == "save" and new_value == "" and required_selector:
                self.action_ele.click_element(submit_selector)
                self.action_ele.explicit_wait(required_selector)
                self.action_ele.click_element(cancel_selector)
                status = True
                return status
            elif action == "save":
                verify_value = new_value
                self.action_ele.click_element(submit_selector)
            else:
                verify_value = old_value
                self.action_ele.click_element(cancel_selector)
            self.action_ele.explicit_wait(base_selector, ec="text_to_be_present_in_element",
                                          msg_to_verify=verify_value)
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_mobility_profile(self, params):
        """
        `Description:` To add mobility profile for a global user via personal information page

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        isDisplayed = False
        isGridPresent = False
        params = defaultdict(lambda: '', params)
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['gu_name']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['gu_name'])

        self.action_ele.click_element("gu_user_link")
        self.action_ele.explicit_wait("personservice_grid")
        self.action_ele.select_from_dropdown_using_index("profile",1)

        for i in range(self.counter):
            try:
                isEnabled = self.query_ele.element_enabled("feature")
                if isEnabled:
                    break
                else:
                    time.sleep(2)
            except:
                self._browser._browser.refresh()

        if params['feature_name']:
            self.action_ele.select_from_dropdown_using_text("feature", params['feature_name'])

        if params['activationDate']:
            if params['activationDate'] == "today":
                cur_date = datetime.date.today()
                self.action_ele.input_text("profile_activationDate", cur_date.strftime('%m/%d/%Y'))
            else:
                self.action_ele.input_text(
                    "profile_activationDate", params['activationDate'])

        self.action_ele.explicit_wait("Requestedby")
        self.action_ele.select_from_dropdown_using_index("Requestedby", 1)

        self.action_ele.explicit_wait("Requestedsources")
        self.action_ele.select_from_dropdown_using_index("Requestedsources", 1)

        self.action_ele.click_element("addButton")
        for i in range(self.counter):
            if "Processing, please wait.." in self._browser._browser.page_source:
                time.sleep(5)
            else:
                try:
                    # import pdb;
                    # pdb.Pdb(stdout=sys.__stdout__).set_trace()

                    isDisplayed = self.query_ele.element_displayed("okButton")
                    if isDisplayed:
                        verify_success = self.query_ele.text_present("Order has been created")
                        if verify_success == False:
                            return verify_success
                        else:
                            self.action_ele.click_element("okButton")
                            self.action_ele.click_element("personservice_refresh")
                            self.action_ele.explicit_wait("personservice_featurepresent")
                            self.action_ele.clear_input_text("personservice_productname")
                            time.sleep(1)
                            self.action_ele.input_text("personservice_productname", params['feature_name'])
                            verify_success = self.query_ele.element_displayed("personservice_featurepresent")
                            return verify_success
                    else:
                        self.action_ele.explicit_wait("personservice_featurepresent")
                        self.action_ele.clear_input_text("personservice_productname")
                        self.action_ele.input_text("personservice_productname", params['feature_name'])
                        verify_success = self.query_ele.element_displayed("personservice_featurepresent")
                        return verify_success

                except Exception, e:
                    print e

    def verify_globaluser_location(self,params):
        """
        `Description:` This Function will verify the location of global user
        `Param:`: Dictionary contains global user information (Name of the user and its country)
        `Returns:` status - True/False
        `Created by:` Megha Bansal
        """
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['username']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['username'])

        self.action_ele.click_element("gu_user_link")
        locationPresent = self.query_ele.text_present(params['country'] + "_GlobalLocation_")

        if locationPresent:
            return True
        else:
            return False
