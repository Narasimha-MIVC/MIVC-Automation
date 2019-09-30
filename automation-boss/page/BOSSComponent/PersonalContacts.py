"""Module for actions on the Personal Contacts page"""

import os
import sys
import time
import inspect

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
import web_wrappers.selenium_wrappers as base
from Navigation import Navigation

__author__ = "Jim Wendt"


class PersonalContacts(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

        self.navigation = Navigation(self._browser)

    def navigate_to_personal_contacts(self):
        """
        `Description:` Navigate to Personal Contacts page

        `Param:`  None

        `Returns:`  status - True/False

        `Created by:` Jim Wendt
        """
        status = False
        try:
            self.navigation.navigate_to_page("Personal Contacts")
            status = True
            return status
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_personal_contact_required_fail(self):
        """
        `Description:` Add Personal Contact without required fields and confirm error

        `:param` None

        `:return:` status - True/False

         `Created by:` Jim Wendt
        """
        status = False
        try:
            self.action_ele.click_element("pc_add_contact")
            self.action_ele.explicit_wait("pc_add_contact_modal")
            self.action_ele.click_element("pc_add_contact_form_firstname_input")
            self.action_ele.click_element("pc_add_contact_form_ok")
            self.action_ele.explicit_wait("pc_add_contact_form_firstname_error")
            self.action_ele.click_element("pc_add_contact_form_cancel")
            status = True
            return status
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_personal_contact_success(self, **params):
        """
        `Description:` Add Personal Contact with required fields and confirm saved

        `:param` params:

        `Returns:` status - True/False

         `Created by:` Jim Wendt
        """
        status = False
        try:
            before_total = 0
            totals = self._browser.elements_finder("pc_slickgrid_totals")
            for total in totals:
                before_total = total.text
            before_rows = int("".join([i for i in before_total if i.isdigit()]))
            after_rows = before_rows + 1
            after_total = before_total.replace(str(before_rows), str(after_rows))
            self.action_ele.click_element("pc_add_contact")
            self.action_ele.explicit_wait("pc_add_contact_modal")
            self.action_ele.select_from_dropdown_using_text("pc_add_contact_form_group_select", params["group"])
            self.action_ele.input_text("pc_add_contact_form_firstname_input", params["firstName"])
            self.action_ele.input_text("pc_add_contact_form_lastname_input", params["lastName"])
            self.action_ele.input_text("pc_add_contact_form_companyname_input", params["companyName"])
            self.action_ele.input_text("pc_add_contact_form_departmentname_input", params["departmentName"])
            self.action_ele.input_text("pc_add_contact_form_workphone_input", params["workPhone"])
            self.action_ele.input_text("pc_add_contact_form_cellphone_input", params["cellPhone"])
            self.action_ele.input_text("pc_add_contact_form_pagerphone_input", params["pagerPhone"])
            self.action_ele.input_text("pc_add_contact_form_homephone_input", params["homePhone"])
            self.action_ele.input_text("pc_add_contact_form_faxphone_input", params["faxPhone"])
            self.action_ele.select_from_dropdown_using_text("pc_add_contact_form_default_select", params["default"])
            self.action_ele.input_text("pc_add_contact_form_email_input", params["email"])
            self.action_ele.input_text("pc_add_contact_form_im_input", params["im"])
            time.sleep(1)
            self.action_ele.click_element("pc_add_contact_form_ok")
            self.action_ele.explicit_wait("pc_slickgrid_totals", ec="text_to_be_present_in_element",
                                          msg_to_verify=after_total)
            self.action_ele.input_text("pc_grid_filter_deptname", params["departmentName"])
            time.sleep(1)
            cells = self._browser.elements_finder("pc_slickgrid_cells")
            for cell in cells:
                if cell.text == params["departmentName"]:
                    status = True
                    break
            return status

        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def delete_personal_contact(self, **params):
        """
        `Description:` Delete Personal Contact and confirm deleted

        `:param` params:

        `Returns:` status - True/False

         `Created by:` Jim Wendt
        """
        status = False
        try:
            before_total = 0
            totals = self._browser.elements_finder("pc_slickgrid_totals")
            for total in totals:
                before_total = total.text
            before_rows = int("".join([i for i in before_total if i.isdigit()]))
            self.action_ele.input_text("pc_grid_filter_deptname", params["departmentName"])
            found = 0
            checkboxes = self._browser.elements_finder("pc_grid_row_checkboxes")
            for checkbox in checkboxes:
                checkbox.click()
                found = found + 1
            if found < 1:
                return status
            self.action_ele.click_element("pc_grid_toolbar_delete")
            time.sleep(1)
            self.action_ele.explicit_wait("pc_delete_confirmation_title")
            self.action_ele.click_element("pc_delete_confirmation_yes")
            after_rows = before_rows - found
            after_total = before_total.replace(str(before_rows), str(after_rows))
            self.action_ele.explicit_wait("pc_slickgrid_totals", ec="text_to_be_present_in_element",
                                          msg_to_verify=after_total)
            cells = self._browser.elements_finder("pc_slickgrid_cells")
            for cell in cells:
                if cell.text == params["departmentName"]:
                    return status
            status = True
            return status

        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def verify_grid_toolbar_update_state(self, **params):
        """
        `Description:` Add Personal Contact with required fields and confirm saved

        `:param` params:

        `Returns:` status - True/False

         `Created by:` Jim Wendt
        """
        status = False
        try:
            self.action_ele.input_text("pc_grid_filter_deptname", params["departmentName"])
            update_button = self._browser.elements_finder("pc_grid_toolbar_update")[0]
            if update_button.is_enabled():
                return status
            checkboxes = self._browser.elements_finder("pc_grid_row_checkboxes")
            for checkbox in checkboxes:
                checkbox.click()
            if update_button.is_enabled():
                return status
            status = True
            return status

        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def edit_personal_contact(self, **params):
        """
        `Description:` Edit Personal Contact and confirm saved

        `:param` params:

        `Returns:` status - True/False

         `Created by:` Jim Wendt
        """
        status = False
        try:
            self.action_ele.click_element("pc_grid_toolbar_update")
            self.action_ele.explicit_wait("pc_add_contact_modal")
            # self.action_ele.select_from_dropdown_using_text("pc_add_contact_form_group_select", params["group"])
            self.action_ele.input_text("pc_add_contact_form_firstname_input", params["firstName"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_lastname_input", params["lastName"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_companyname_input", params["companyName"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_departmentname_input", params["departmentName"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_workphone_input", params["workPhone"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_cellphone_input", params["cellPhone"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_pagerphone_input", params["pagerPhone"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_homephone_input", params["homePhone"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_faxphone_input", params["faxPhone"] + "XXX")
            # self.action_ele.select_from_dropdown_using_text("pc_add_contact_form_default_select", params["default"])
            self.action_ele.input_text("pc_add_contact_form_email_input", params["email"] + "XXX")
            self.action_ele.input_text("pc_add_contact_form_im_input", params["im"] + "XXX")
            time.sleep(1)
            self.action_ele.click_element("pc_add_contact_form_ok")
            self.action_ele.explicit_wait("pc_slickgrid_totals", ec="text_to_be_present_in_element",
                                          msg_to_verify=1)
            self.action_ele.input_text("pc_grid_filter_deptname", params["departmentName"] + "XXX")
            found = 0
            checkboxes = self._browser.elements_finder("pc_grid_row_checkboxes")
            for checkbox in checkboxes:
                checkbox.click()
                found = found + 1
            if found < 1:
                return status
            time.sleep(1)
            cells = self._browser.elements_finder("pc_slickgrid_cells")
            for cell in cells:
                if cell.text == params["departmentName"]:
                    status = True
                    break
            return status

        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status
