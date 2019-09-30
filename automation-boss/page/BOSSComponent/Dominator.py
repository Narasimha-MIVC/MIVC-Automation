"""
Class: Dominator
Description: Provides all methods for the DOMinator keywords
Created by: Jim Wendt
"""

import time
import inspect
import string
import collections
import web_wrappers.selenium_wrappers as base
from random import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from log import log

__author__ = "Jim Wendt"


class Dominator(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def update_random_values(self, values):
        """
        Description: Removes Unicode and randomizes Dictionary values using '{type}' or '{type|length}' format

        :Note: Always processes as string.

        :Example: 'First {rand_str|8}' or '1{rand_int|10}' or '{rand_all}@shoretell.com'

        :Param1 values: Dictionary of form values

        :Return: Dictionary containing randomized values

        Created by: Jim Wendt
        """
        try:
            values = self.__convert_from_unicode(values)
            for form in values:
                for field in values[form]:
                    value = values[form][field]

                    # Only randomize strings
                    if hasattr(value, "find") and value.find("{rand_") != -1:
                        # Get the randomizer string
                        s = value.find("{")
                        e = value.find("}") + 1
                        find_val = value[s:e]

                        # Get the randomizer values
                        parts = find_val.replace("{", "").replace("}", "").split("|")
                        min_char = 8
                        max_char = 8

                        # Override default length if specified
                        if len(parts) == 2:
                            min_char = int(parts[1])
                            max_char = int(parts[1])

                        # Get randomizer fill values
                        if parts[0] == "rand_int":
                            all_char = string.digits
                        elif parts[0] == "rand_str":
                            all_char = string.ascii_letters
                        else:
                            all_char = string.ascii_letters + string.digits

                        # Create the randomized value and replace the original value wit it
                        new_val = "".join(choice(all_char)for _ in range(randint(min_char, max_char)))
                        values[form][field] = value.replace(find_val, new_val)
            return values
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to randomize values")
            return False

    def validate_component_with_json(self, component_type, details, values):
        """
        Description: FUTURE: Currently only checks component for JavaScript errors

        :Param1 component_type: Component type (grid, form, wizard, edit-in-place, etc)

        :Param2 details: Dictionary of the component definitions

        :Param3 values: Dictionary of values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            # Verify no JavaScript errors have occurred
            self.assert_ele.page_should_not_contain_javascript_errors()

            # Verify field values comply with field details
            if component_type in ["form", "wizard"]:
                for key in values:
                    try:
                        field = details["fields"][key]
                        # Validate value base on field type
                        if field["type"] in ["text", "password", "textarea"]:
                            self.__validate_text_field(key, field, values[key])
                        elif field["type"] == "select-one":
                            self.__validate_select_one_field(key, field, values[key])
                        elif field["type"] == "checkbox":
                            self.__validate_checkbox_field(key, field, values[key])
                        elif field["type"] == "radio":
                            self.__validate_radio_field(key, field, values[key])
                        elif field["type"] == "time":
                            self.__validate_time_field(key, field, values[key])
                        elif field["type"] == "number":
                            self.__validate_number_field(key, field, values[key])
                        elif field["type"] == "date":
                            self.__validate_date_field(key, field, values[key])
                        else:
                            raise Exception("Field type of " + field["type"] + " is not currently available")
                    except:
                        raise Exception("Failure: Field " + key + " is missing")

            return True
        except Exception as e:
            print("Exception:", e, "Unable to validate component " + component_type)
            return status

    def verify_component_state_with_json(self, component, state):
        """
        Description: Verifies that the specified component is in the specified state

        :Param1 component: Dictionary of component definition

        :Param2 state: String containing the expected state (enabled/disabled/hidden/visible/found/missing)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            state = state.lower()

            # Confirm we have a valid component with locator
            if not type(component) == dict:
                self.__add_log_entry("error", "Failure: The component to verify has an invalid configuration")
                return status

            if "locator" not in component or component["locator"] == "":
                self.__add_log_entry("error", "Failure: The component does not have a locator")
                return status

            # Get the specified element
            element = self._browser.element_finder(component["locator"])

            if state == "enabled" and element.is_enabled():
                status = True
            elif state == "disabled" and element.is_displayed() and not element.is_enabled():
                status = True
            elif state == "hidden" and not element.is_displayed():
                status = True
            elif state == "visible" and element.is_displayed():
                status = True
            elif state == "found" and element is not None:
                status = True
            elif state == "missing" and element is None:
                status = True

            if status is not True:
                self.__add_log_entry("error", "Failure: The state " + state + " specified is not valid")

            return status
        except Exception as e:
            print("Exception:", e)
            return status

    def confirm_component_text_with_json(self, component, text, expect):
        """
        Description: Confirms that the specified component contains the specified text

        :Param1 component: Dictionary of component definition

        :Param2 text: String containing the text to be found in the component

        :Param3 expect: String that contains the expected result (does/does not)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            expect = expect.lower()
            # Confirm we have a valid component with locator
            if not type(component) == dict:
                self.__add_log_entry("error", "Failure: The component to verify has an invalid configuration")
                return status

            if "locator" not in component or component["locator"] == "":
                self.__add_log_entry("error", "Failure: The component does not have a locator")
                return status

            elements = self._browser.elements_finder(
                component["locator"] + "//*[contains(., '" + text + "')]"
            )

            if expect == "does" and len(elements) == 0:
                self.__add_log_entry("error", "Failure: The text (" + text + ") was not found")
                return status

            if expect == "does not" and not len(elements) == 0:
                self.__add_log_entry("error", "Failure: The text (" + text + ") was found")
                return status

            status = True
            return status
        except Exception as e:
            print("Exception:", e)
            return status

    def update_form_with_json(self, form, values):
        """
        Description: Updates form with the specified values

        :Param1 form: Dictionary of form definitions

        :Param2 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            self._browser.waitfor_ajax_complete()
            for key in values:
                time.sleep(.35)
                field_type = form["fields"][key]["type"]

                # Confirm field is found and not disabled
                field = self._browser.element_finder(form["fields"][key]["locator"])
                if not field:
                    raise Exception("Failure: Field " + key + " is missing")
                if not field_type == "radio" and not field.is_enabled():
                    raise Exception("Failure: Field " + key + " is disabled")

                # Change value base on field type
                # Text like fields
                if field_type in ["text", "file", "password", "textarea", "number", "date"]:
                    self.update_text_field(key, field, values[key])
                elif field_type == "select-one":
                    self.update_select_one_field(key, field, values[key])
                elif field_type == "checkbox":
                    self.update_checkbox_field(key, field, values[key])
                elif field_type == "radio":
                    self.update_radio_field(key, field, values[key])
                elif field_type == "time":
                    self.update_time_field(key, field, values[key])
                else:
                    raise Exception("Field type of " + field_type + " is not currently available")
            status = True
            return status

        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def update_field_with_json(self, field, value):
        """
        Description: Updates individual field with the specified value

        :Param1 field: Dictionary of field definition

        :Param2 value: String of field value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            key = field.keys()[0]

            # Confirm field is found and not disabled
            element = self._browser.element_finder(field["locator"])
            if not element:
                raise Exception("Failure: Field " + key + " is missing")
            if not field["type"] == "radio" and not element.is_enabled():
                raise Exception("Failure: Field " + key + " is disabled")

            # Change value base on field type
            if field["type"] in ["text", "file", "password", "textarea", "number", "date"]:
                self.update_text_field(key, element, value)
            elif field["type"] == "select-one":
                self.update_select_one_field(key, element, value)
            elif field["type"] == "checkbox":
                self.update_checkbox_field(key, element, value)
            elif field["type"] == "radio":
                self.update_radio_field(key, element, value)
            elif field["type"] == "time":
                self.update_time_field(key, element, value)
            else:
                raise Exception("Field type of " + field["type"] + " is not currently available")
            status = True
            return status

        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __validate_text_field(self, name, field, value):
        """
        Description: Validates text input field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            value = self.__convert_from_unicode(value)
            required = self.__convert_from_unicode(field["required"])
            minlength = self.__convert_from_unicode(field["minlength"])
            maxlength = self.__convert_from_unicode(field["maxlength"])
            rangelength = self.__convert_from_unicode(field["rangelength"])

            # Convert rangelength array
            if rangelength and type(rangelength) == list:
                minlength = rangelength[0]
                maxlength = rangelength[1]

            if required and not value:
                raise Exception("Error: Field " + name + " is required")
            if minlength and len(value) < minlength:
                raise Exception("Error: Field " + name + " value (" + value + ") is shorter than " + minlength)
            if maxlength and len(value) > maxlength:
                raise Exception("Error: Field " + name + " value (" + value + ") is longer than " + maxlength)

            status = True
            return status

        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to validate " + name + " with " + value)
            return status

    def update_text_field(self, name, field, value):
        """
        Description: Updates text input field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed new field value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            time.sleep(.2)
            field.send_keys(value)
            self.__add_log_entry("info", "Updated " + name + " to " + value)
            status = True
            return status
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to update " + name + " to " + value)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __validate_checkbox_field(self, name, field, value):
        """
        Description: Validates checkbox field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        return True

    def update_checkbox_field(self, name, field, value):
        """
        Description: Updates checkbox field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Boolean of checked

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            checked = self.__convert_to_boolean(field.get_attribute("checked"))

            if not self.__convert_to_boolean(value) == checked:
                field.click()
                self.__add_log_entry("info", "Updated checkbox " + name + " to " + str(value))
            status = True
            return status
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to update checkbox " + name + " to " + str(value))
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __validate_radio_field(self, name, field, value):
        """
        Description: Validates radio field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        return True

    def update_radio_field(self, name, field, value):
        """
        Description: Updates radio field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed new field value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            checked = self.__convert_to_boolean(field.get_attribute("checked"))
            if not self.__convert_to_boolean(value) == checked:
                field.click()
                self.__add_log_entry("info", "Updated radio " + name + " to " + str(value))
            status = True
            return status
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to update radio " + name + " to " + str(value))
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __validate_select_one_field(self, name, field, value):
        """
        Description: Validates select input field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        return True

    def update_select_one_field(self, name, field, select):
        """
        Description: Selects one value from a select input field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 select: Mixed description of how to identify the option to select

        :Return: Boolean of execution results

        Created by: Jim Wendt

            The single select value is broken into two parts separated by the pipe symbol
            select = 'select type' | 'select value'
            Examples:
                'text|Primary'     chooses the option with 'Primary' in the drop down
                'value|10552'      chooses the option that has a value of 10552
                'position|2'       chooses the second option in the drop down (1 based)

        """
        status = False
        try:
            config = select.split("|")
            if len(config) != 2:
                raise Exception("Failure: Value for " + name + " is not valid")
            if config[0] == "text":
                Select(field).select_by_visible_text(config[1])
            elif config[0] == "value":
                Select(field).select_by_value(config[1])
            elif config[0] == "position":
                loop = 1
                for option in Select(field).options:
                    if loop == int(config[1]):
                        Select(field).select_by_visible_text(option.text)
                        break
                    loop = loop + 1
            else:
                raise Exception("Failure: Input type of " + config[0] + " is not currently available")
            self.__add_log_entry("info", "Updated select " + name + " to " + select)
            status = True
            return status
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to update " + name + " to " + select)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __validate_time_field(self, name, field, value):
        """
        Description: Validates time field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        return True

    def update_time_field(self, name, field, value):
        """
        Description: Updates time field

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed new field value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            if value:
                parts = value.split("|")
                if len(parts) != 3 or not parts[2].lower() in ["am", "pm"]:
                    raise Exception("Failure: Value (" + value + " for " + name + " is not valid")
                field.send_keys(parts[0])
                field.send_keys(Keys.TAB)
                field.send_keys(parts[1])
                field.send_keys(Keys.TAB)
                field.send_keys(parts[2])
            else:
                field.set_value("")
            status = True
            return status
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "Unable to update time " + name + " to " + value)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __validate_number_field(self, name, field, value):
        """
        Description: Validates text field for numbers

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 value: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        return True

    def __validate_date_field(self, name, field, value):
        """
        Description: Validates text field for date

        :Param1 name: String of field name

        :Param2 field: Object of the field

        :Param3 select: Mixed field value to validate

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        return True

    def edit_in_place_with_json(self, page, values, action):
        """
        Description: Updates form with the specified values

        :Param1 page: Dictionary of edit in place field definitions

        :Param2 values: Dictionary of field values

        :Param3 action: String that contains the button action to perform(submit, cancel)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            self._browser.waitfor_ajax_complete()
            for key in values:
                field_type = page["fields"][key]["type"]
                field_locator = page["fields"][key]["locator"]

                # Confirm the display for the field is found and not disabled
                display = self._browser.element_finder(field_locator)
                if not display:
                    raise Exception("Failure: Field " + key + " is missing")
                if not field_type == "radio" and not display.is_enabled():
                    raise Exception("Failure: Field " + key + " is disabled")
                self.action_ele.click_element(field_locator)

                # Setup input element
                if field_type == "select-one":
                    input_locator = field_locator + "//form//select"
                else:
                    input_locator = field_locator + "//form//input"

                field = self._browser.element_finder(input_locator)
                self.action_ele.explicit_wait(input_locator)

                if field_type == "select-one":
                    old_value = Select(field).first_selected_option.text
                else:
                    old_value = self.query_ele.get_value(input_locator)

                # Setup other elements
                error_locator = field_locator + "//form//label[contains(@class, 'input-validation-error')]"
                submit_locator = field_locator + "//form//button[@type='submit']"
                cancel_locator = field_locator + "//form//button[@type='cancel']"

                # Change value base on field type
                # Text like fields
                if field_type in ["text", "file", "password", "textarea", "number", "date"]:
                    field.clear()
                    self.update_text_field(key, field, values[key])
                elif field_type == "select-one":
                    self.update_select_one_field(key, field, values[key])
                elif field_type == "checkbox":
                    self.update_checkbox_field(key, field, values[key])
                elif field_type == "radio":
                    self.update_radio_field(key, field, values[key])
                elif field_type == "time":
                    field.clear()
                    self.update_time_field(key, field, values[key])
                else:
                    raise Exception("Field type of " + field_type + " is not currently available")

                verify_value = old_value
                if action == "fail" and values[key] == "" and page["fields"][key]["required"]:
                    self.action_ele.click_element(submit_locator)
                    self.action_ele.explicit_wait(error_locator)
                    self.action_ele.click_element(cancel_locator)
                elif action == "save":
                    if field_type == "select-one":
                        verify_value = Select(field).first_selected_option.text
                    else:
                        verify_value = values[key]
                    self.action_ele.click_element(submit_locator)
                    self._browser.waitfor_ajax_complete()
                else:
                    verify_value = old_value
                    self.action_ele.click_element(cancel_locator)

                self.action_ele.explicit_wait(field_locator, ec="text_to_be_present_in_element",
                                              msg_to_verify=verify_value)
            status = True
            return status

        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def conclude_form_with_json(self, form, action, button):
        """
        Description: Finalizes form with the specified action and button

        :Param1 form: Dictionary of form definitions

        :Param2 action: String that contains the action to perform(fail, save)

        :Param3 button: String that contains the name of the button to click

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        action = action.lower()

        # Confirm the we are using an available button
        if not form["buttons"][button]:
            self.__add_log_entry("error", button + " for " + action + " is not available")
            return status

        # Confirm the button is configured correctly
        if not form["buttons"][button]["locator"]:
            self.__add_log_entry("error", button + " for " + action + " is not configured correctly")
            return status

        # Click the button
        try:
            self.action_ele.click_element(form["buttons"][button]["locator"])
        except Exception as e:
            print("Exception:", e)
            self.__add_log_entry("error", "The button was not able to be clicked")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

        # Handle explict expected view
        if form["buttons"][button]["expect"]:
            try:
                self.action_ele.explicit_wait(form["buttons"][button]["expect"])
                if action != "fail":
                    status = True
                return status
            except Exception as e:
                if action == "fail":
                    status = True
                    return status
                print("Exception:", e)
                self.__add_log_entry("error", "The expected view is not visible")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return status

        # Wait for Ajax to complete
        self._browser.waitfor_ajax_complete()

        # Handle closing the modal
        if form["modal_locator"]:
            try:
                self.action_ele.explicit_wait(form["modal_locator"], ec="invisibility_of_element_located")
                return True
            except Exception as e:
                if action == "fail":
                    status = True
                    return status
                print("Exception:", e)
                self.__add_log_entry("error", "The modal form was not closed")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return status

        # Notify that this button expected view has not been configured
        self.__add_log_entry("warning", "The button action was not able to be verified")
        status = True
        return status

    def click_grid_button_with_json(self, grid, button):
        """
        Description: Clicks the specified button and performs any validation required

        :Param1 details: Dictionary of grid definitions

        :Param2 button: String that contains the name of the button to click

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            self.action_ele.click_element(grid["buttons"][button]["locator"])
            if not grid["buttons"][button]["expect"]:
                self.__add_log_entry("warning", "The button action was not able to be verified")
            else:
                self.action_ele.explicit_wait(grid["buttons"][button]["expect"])
            status = True
            return status
        except Exception as e:
            print("Exception:", e, "Unable to click " + button + " for grid")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def delete_from_grid_with_json(self, button, grid, field, values):
        """
        Description: Filters the grid with the specified parameters and performs any validation required

        :Param1 button: String that contains the name of the button to click

        :Param2 grid: Dictionary of grid definitions

        :Param3 field: String that contains the name of the field to filter

        :Param4 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # Wait for the grid totals to be visible
            self.action_ele.explicit_wait(grid["totals_locator"])

            # Filter the grid with the passed value
            self.action_ele.input_text(grid["columns"][field]["filter"]["locator"], values[field])

            # Get the row count before the delete
            total_element = self._browser.element_finder(grid["totals_locator"])
            total_text = total_element.text
            before_rows = int("".join([i for i in total_text if i.isdigit()]))
            if before_rows < 1:
                self.__add_log_entry("error", "No rows are displayed")
                return status

            # Find and click the first checkbox corresponding with the filtered rows
            found = 0
            checkboxes = self._browser.elements_finder(
                grid["locator"] + "/descendant::div[contains(@class, 'slick-cell-checkboxsel')]//input")
            for checkbox in checkboxes:
                checkbox.click()
                found = found + 1
                break
            if found < 1:
                self.__add_log_entry("error", "No checkbox for " + field + " as " + values[field] + " is available")
                return status

            # Wait for the delete button and click it
            self.action_ele.explicit_wait(grid["buttons"][button]["locator"])
            self.action_ele.click_element(grid["buttons"][button]["locator"])

            # Wait for the confirmation modal and click yes
            self.handle_generic_confirmation_dialog("yes")

            # Wait for OK confirmation dialog
            self.handle_generic_confirmation_dialog("ok")


            # Filter the grid with the passed value
            self.action_ele.input_text(grid["columns"][field]["filter"]["locator"], values[field])

            # Get the row count after delete and confirm the number of found rows have been deleted
            after_rows = before_rows - found
            after_total = total_text.replace(str(before_rows), str(after_rows))
            self.action_ele.explicit_wait(grid["totals_locator"], ec="text_to_be_present_in_element",
                                          msg_to_verify=after_total)

            # Confirm the value is no longer in the grid if any rows are left
            if after_rows:
                cells = self._browser.elements_finder(grid["locator"] +
                                                      "/descendant::div[contains(@class, 'slick-cell')]")
                for cell in cells:
                    if cell.text == values[field]:
                        self.__add_log_entry("warning", "The grid still contains " + values[field])
            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to delete from grid with " + button)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def filter_grid_header_with_json(self, grid, field, values):
        """
        Description: Filters the grid header fields with the specified parameters

        :Param1 grid: Dictionary of grid definition

        :Param2 field: String that contains the name of the field to filter

        :Param3 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # Wait for the grid totals to be visible
            self.action_ele.explicit_wait(grid["totals_locator"])

            # Confirm field is found and not disabled
            field_type = grid["columns"][field]["filter"]["type"]
            element = self._browser.element_finder(grid["columns"][field]["filter"]["locator"])
            if not element:
                raise Exception("Failure: Field " + field + " is missing")
            if not field_type == "radio" and not element.is_enabled():
                raise Exception("Failure: Field " + field + " is disabled")

            # Change value base on field type
            if field_type in ["text", "file", "password", "textarea", "number", "date"]:
                self.update_text_field(field, element, values[field])
            elif field_type == "select-one":
                self.update_select_one_field(field, element, values[field])
            elif field_type == "checkbox":
                self.update_checkbox_field(field, element, values[field])
            elif field_type == "radio":
                self.update_radio_field(field, element, values[field])
            elif field_type == "time":
                self.update_time_field(field, element, values[field])
            else:
                raise Exception("Failure: Field type of " + field_type + " is not currently available")
            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to filter grid field " + field)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def filter_grid_with_json(self, grid, field, value):
        """
        Description: Filters the grid with the specified parameters

        :Param1 grid: Dictionary of grid definition

        :Param2 field: String that contains the name of the field to filter

        :Param3 value: String that contains the filter value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            value = value.lower()

            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # Wait for the grid totals to be visible
            self.action_ele.explicit_wait(grid["totals_locator"])

            # Change value base on field type
            if field in ["searchText", "multiSearchText"]:
                search_text = self._browser.element_finder(grid["filters"]["searchText"]["locator"])
                toggle_btn = self._browser.element_finder(grid["filters"]["toggleBtn"]["locator"])
                multi_search_text = self._browser.element_finder(grid["filters"]["multiSearchText"]["locator"])
                multi_search_button = self._browser.element_finder(grid["filters"]["multiSearchButton"]["locator"])
                # Not currently doing any action on save search checkbox
                # save_search = self._browser.element_finder(grid["filters"]["saveSearch"]["locator"])

                if field == "searchText":
                    if multi_search_text and multi_search_text.get_attribute("value"):
                        multi_search_text.clear()
                    if toggle_btn.get_attribute("checked"):
                        toggle_btn.click()
                    search_text.clear()
                    self.update_text_field("searchText", search_text, value)
                if field == "multiSearchText":
                    if search_text and search_text.get_attribute("value"):
                        search_text.clear()
                    if not toggle_btn.get_attribute("checked"):
                        toggle_btn.click()
                    self.action_ele.explicit_wait(grid["filters"]["multiSearchText"]["locator"])
                    multi_search_text.clear()
                    self.update_text_field("multiSearchText", multi_search_text, value)
                    multi_search_button.click()
            elif grid["filters"][field]["type"] == "select-one":
                # Click the button
                self.action_ele.click_element(grid["filters"][field]["locator"])
                # Click the option
                self.action_ele.click_element(grid["filters"][field][value]["locator"])
            else:
                self.__add_log_entry("error", "The filter for " + field + " does have a valid configuration")

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to filter grid field " + field)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def select_grid_row_with_json(self, grid, count):
        """
        Description: Filters the grid with the specified parameters and selects one or more rows

        :Param1 grid: Dictionary of grid definition

        :Param2 count: Mixed either all, none or an integer of the number of rows to select

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            found = 0
            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # Wait for the grid totals to be visible
            self.action_ele.explicit_wait(grid["totals_locator"])

            # Get the number of rows to select
            if type(count) == int or count.isdigit():
                count = int(count)
            elif type(count) in[str, unicode] and count.lower() == "no":
                count = 0
            elif type(count) in[str, unicode] and count.lower() == "all":
                count = 99999
            else:
                raise Exception("Failure: Unable to determine the number of rows to select")

            # Select the specified number of rows
            if count == 0:
                checkbox = self._browser.element_finder(grid["header_checkbox"])
                if not checkbox:
                    raise Exception("Failure: Unable to locate grid header checkbox")
                if checkbox.get_attribute("checked"):
                    checkbox.click()
                else:
                    checkbox.click()
                    checkbox = self._browser.element_finder(grid["header_checkbox"])
                    checkbox.click()
            elif count == 99999:
                checkbox = self._browser.element_finder(grid["header_checkbox"])
                if not checkbox:
                    raise Exception("Failure: Unable to locate grid header checkbox")
                if not checkbox.get_attribute("checked"):
                    checkbox.click()
                else:
                    checkbox.click()
                    checkbox = self._browser.element_finder(grid["header_checkbox"])
                    checkbox.click()
            else:
                # Find and click the number specified checkboxes
                checkboxes = self._browser.elements_finder(
                    grid["locator"] + "/descendant::div[contains(@class, 'slick-cell-checkboxsel')]//input")
                for checkbox in checkboxes:
                    checkbox.click()
                    found = found + 1
                    if found >= count:
                        break
                if not found == count:
                    self.__add_log_entry("error", "Only " + str(found) + " were able to be checked")
                    return status
            # Iterate through the buttons and validate their visibility for the number selected
            for button in grid["buttons"]:
                enabled_value = None
                element = self._browser.element_finder(grid["buttons"][button]["locator"])
                if count == 0:
                    enabled_value = grid["buttons"][button]["enabled"]["0"]
                elif count == 99999:
                    enabled_value = grid["buttons"][button]["enabled"]["all"]
                elif found == 1:
                    enabled_value = grid["buttons"][button]["enabled"]["1"]
                elif found >= 2:
                    enabled_value = grid["buttons"][button]["enabled"]["2+"]

                # Warn if the button expected value is empty
                if not grid["buttons"][button]["expect"]:
                    self.__add_log_entry("warning", "The " + button + " button action was not able to be verified")

                # Error if the enabled state of the button is not correct
                if enabled_value is not None and not bool(element.is_enabled()) == bool(enabled_value):
                    self.__add_log_entry("error", "The " + button + " button is not enabling/disabling correctly")
                    return status

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to select " + str(count) + " row(s) from grid")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def show_contextmenu_from_grid_with_json(self, grid, field, values):
        """
        Description: Choose the contextmenu item for the grid with the specified parameters and does validation required

        :Param1 item: String that contains the name of the context menu item to click

        :Param2 grid: Dictionary of grid definitions

        :Param3 field: String that contains the name of the field to filter

        :Param4 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # Wait for the grid totals to be visible
            self.action_ele.explicit_wait(grid["totals_locator"])

            # Test if any contextmenu items are available
            if not grid["context_locator"]:
                self.__add_log_entry("error", "There are no context menu items available for this grid")
                return status

            # Filter the grid with the passed value
            self.action_ele.input_text(grid["columns"][field]["filter"]["locator"], values[field])

            # Get the row count before the any action
            before_rows = self.__get_total_grid_rows(grid["totals_locator"])
            if before_rows < 1:
                self.__add_log_entry("error", "No rows are displayed")
                return status

            # Confirm the contextmenu locator and show it
            context_menu = self._browser.element_finder(grid["context_locator"])
            if not context_menu:
                self.__add_log_entry("error", "The context menu configuration for this grid is not valid")
                return status

            # Find and right click the first of the filtered rows to show the context menu
            column = int(grid["columns"][field]["number"]) + 1
            locator = grid["locator"]
            locator += "/descendant::div[contains(@class, 'slick-row')][not(contains(@class, 'slick-group'))]"
            locator += "[1]//div[contains(@class, 'slick-cell')]"
            self.action_ele.right_click(locator + "[" + str(column) + "]")
            self.action_ele.explicit_wait(grid["context_locator"])

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to show context menu for grid row " + field)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def choose_contextmenuitem_from_grid_with_json(self, contextitems, menu_item, expect):
        """
        Description: Choose the contextmenu item for the grid with the specified parameters and does validation required

        :Param1 contextitems: Dictionary of grid context menu definitions

        :Param2 menu_item: String that contains the name of the context menu item to click

        :Param3 expect: String that contains the expected result (can/can not)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            expect = expect.lower()
            menu_item = menu_item.lower()
            locator = contextitems[menu_item]["locator"]

            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # Lots of extra work here to identify if an item is disabled
            if expect == "can not":
                disabled = False
                item = self._browser.element_finder(locator)
                classes = item.get_attribute("class")
                if classes and classes.find("disabled") != -1:
                    disabled = True
                if item.is_enabled() and disabled is False:
                    self.__add_log_entry("error", "The menu item " + menu_item + " was not disabled")
                    raise Exception("Failure: Menu item " + menu_item + " should be disabled")
            else:
                # Validate and click the menu item
                self.action_ele.explicit_wait(locator)
                self.action_ele.click_element(locator)

                # Wait for the expected action or log error if none is specified
                if not contextitems[menu_item]["expect"]:
                    self.__add_log_entry("warning", "The menu action was not able to be verified")
                else:
                    self.action_ele.explicit_wait(contextitems[menu_item]["expect"])

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to " + expect + " choose context menu item " + menu_item)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def find_value_in_grid_rows_with_json(self, grid, value, expect):
        """
        Description: Find the specified value in the grid

        :Param1 grid: Dictionary of grid definitions

        :Param2 value: String that contains the value to find

        :Param3 expect: String that contains the expected result (can/cannot)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            expect = expect.lower()
            value = value.lower()

            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            # If no rows are found we can exit here
            total_rows = self.__get_total_grid_rows(grid["totals_locator"])
            if total_rows == 0:
                if expect == "can":
                    return status
                else:
                    status = True
                    return status

            # Search all cells for the specified value and return if value is found
            cells = self._browser.elements_finder(grid["locator"] + "/descendant::div[contains(@class, 'slick-cell')]")
            for cell in cells:
                if cell.text.lower() == value:
                    if expect == "can":
                        status = True
                        return status
                    if expect == "cannot":
                        return status

            # Value not found in grid
            if expect == "can":
                return status
            else:
                status = True
                return status

        except Exception as e:
            print("Exception:", e, "Unable to " + expect + " find " + value + " in grid")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def clear_all_grid_filters_with_json(self, grid):
        """
        Description: Clear both column heading and search filters

        :Param1 grid: Dictionary of grid definitions

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:

            # Clear column heading filters
            for column in grid["columns"]:
                element = self._browser.element_finder(grid["columns"][column]["filter"]["locator"])
                if element.get_attribute("value"):
                    element.clear()

            # Clear search filters
            for filter in grid["filters"]:
                if grid["filters"][filter]["type"] in ["text", "select-one"]:
                    element = self._browser.element_finder(grid["filters"][filter]["locator"])
                    if element.get_attribute("value"):
                        element.clear()

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to clear all grid filters")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def click_grid_cell_with_json(self, grid, item, column, value):
        """
        Description: Click the text or icon in the specified cell of the grid
        :Param1 grid: Dictionary of grid definitions
        :Param2 item: String that contains the element to click (text/icon)
        :Param3 column: String that contains the column to search
        :Param4 value: String that contains the value to find
        :Return: Boolean of execution results
        Created by: Jim Wendt
        """
        status = False
        try:
            item = item.lower()
            if "external" in grid["columns"][column]["cell"]:
                is_external = self.__convert_to_boolean(grid["columns"][column]["cell"]["external"])
            else:
                is_external = False
            is_clickable = self.__convert_to_boolean(grid["columns"][column]["cell"]["clickable"])
            expect = grid["columns"][column]["cell"]["expect"]
            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()
            # Verify we can click any cell for this column
            if not is_clickable:
                self.__add_log_entry("error", "The cell for " + column + " is configured as non-clickable")
                raise Exception("The cell for " + column + " is configured as non-clickable")
            # Verify we can click any cell for this column
            if not expect:
                self.__add_log_entry("warning", "The " + item + " click action was not able to be verified")
            # Get Column number so we know which cell to access
            column_number = grid["columns"][column]["number"]
            # Get all rows for search
            rows = self._browser.elements_finder(grid["locator"] + "/descendant::div[contains(@class, 'slick-row')]")
            # Find the cell containing the search value
            count = 0
            for row in rows:
                cells = row.find_elements_by_tag_name("div")
                # Remove any cells from list that don't contain the correct class
                for cell in cells:
                    if cell.get_attribute("class").find("slick-cell") == -1:
                        cells.remove(cell)
                # Get and compare cell value to search value
                cell_text = self.__convert_from_unicode(cells[column_number].text)
                if str(cell_text).lower() == str(value).lower():
                    count = 1
                    # Click on the text anchor for the found cell
                    if item == "text":
                        anchor = cells[column_number].find_elements_by_tag_name("a")
                        if anchor:
                            anchor[0].click()
                        else:
                            raise Exception("The cell for " + column + " does not have a clickable anchor")
                    # Click on the icon for the found cell
                    elif item == "icon":
                        icon = cells[column_number].find_elements_by_tag_name("span")
                        if icon and icon[0].get_attribute("class").find("ui-icon-image") != -1:
                            icon[0].click()
                    else:
                        raise Exception("The item to click must be text or icon - " + item + " was specified")
                    # Handle the expected page
                    if not is_external:
                        # Wait for Ajax to complete
                        self._browser.waitfor_ajax_complete()
                        # Wait for the expected page
                        if expect:
                            self.action_ele.explicit_wait(expect)
                        # Verify no JavaScript errors have occurred
                        self.assert_ele.page_should_not_contain_javascript_errors()
                    elif is_external and self.action_ele.window_handles_count() > 1:
                        self.action_ele.switch_to_window(1)
                        self.action_ele.explicit_wait(expect)
                        self.action_ele.close_window()
                        self.action_ele.switch_to_window(0)
            # We did not find any matching cell
            if count == 0:
                raise Exception("Unable to find a cell for " + column + " that contains " + value)
            status = True
            return status
        except Exception as e:
            print("Exception:", e, "Click grid cell has failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def wizard_go_to_step_with_json(self, wizard, button, step):
        """
        Description: Move to the specified wizard step using the specified button

        :Param1 wizard: Dictionary of wizard definitions

        :Param2 button: String that contains the name of the button item to click (next/back)

        :Param3 step: String that contains the expected step definition

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            # Click the selected button
            locator = wizard["buttons"][button]["locator"]
            self.action_ele.explicit_wait(locator)
            self.action_ele.click_element(locator)

            self._browser.waitfor_ajax_complete()

            # Confirm the expected step is displaayed
            locator = wizard["steps"][step]["locator"]
            self.action_ele.explicit_wait(locator)

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to go to " + step + " in wizard with " + button + " button")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def wizard_finalize_with_json(self, wizard, button, include):
        """
        Description: Finish/Cancel the wizard step using the specified button

        :Param1 wizard: Dictionary of wizard definitions

        :Param2 button: String that contains the name of the button item to click (finish/cancel)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            button = button.lower()

            # Click the selected button
            locator = wizard["buttons"][button]["locator"]
            self.action_ele.explicit_wait(locator)
            self.action_ele.click_element(locator)

            # Handle the confirmation dialog if required for yes and OK confirmations
            if include == "with":
                self.handle_generic_confirmation_dialog("yes")
                self.handle_generic_confirmation_dialog("ok")

            # Confirm expected
            self.action_ele.explicit_wait(wizard["buttons"][button]["expect"])

            # Verify no JavaScript errors have occurred
            self.assert_ele.page_should_not_contain_javascript_errors()

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to " + button + " the wizard")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def handle_generic_confirmation_dialog(self, button):
        """
        Description: Handles the generic confirmation dialog with the specified button

        :Param1 button: String that contains the name of the button to click

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        status = False
        try:
            button = button.lower()
            if button == "yes":
                locator = "//button[@id='fnMessageBox_Yes']"
            elif button == "ok":
                locator = "//button[@id='fnMessageBox_OK']"
            else:
                locator = "//button[@id='fnMessageBox_No']"

            # Wait for the confirmation modal and click the action button
            self.action_ele.explicit_wait(locator)
            time.sleep(1)
            self.action_ele.click_element(locator)

            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()

            self.action_ele.explicit_wait(locator, ec="invisibility_of_element_located")

            status = True
            return status

        except Exception as e:
            print("Exception:", e, "Unable to handle generic confirmation dialog")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def __get_total_grid_rows(self, locator):
        """
        Description: Gets the row count for slickgrids

        :Param1 locator: String XPath for the grid totals

        :Return: Integer of the totals rows

        Created by: Jim Wendt
        """
        try:
            self.action_ele.explicit_wait(locator)
            element = self._browser.element_finder(locator)
            text = element.text
            return int("".join([i for i in text if i.isdigit()]))
        except Exception as e:
            print("Exception:", e, "Unable to get total rows")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return None

    def __convert_from_unicode(self, data):
        """
        Description: Converts pass data from unicode to native values

        :Param1 value: Mixed that contains the value to test

        :Return: Boolean of passed value

        Created by: Jim Wendt
        """
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(self.__convert_from_unicode, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.__convert_from_unicode, data))
        else:
            return data

    def __convert_to_boolean(self, value):
        """
        Description: Return boolean for trusey/falsey values

        :Param1 value: Mixed that contains the value to test

        :Return: Boolean of passed value

        Created by: Jim Wendt
        """
        value = self.__convert_from_unicode(value)
        try:
            if type(value) == bool:
                return value
            elif type(value) == int:
                return value == 1
            elif hasattr(value, "lower") and value.lower() in ["true", "1", "yes"]:
                return True
            else:
                return False
        except Exception as e:
            print("Exception:", e, "Unable to convert to boolean")
            return None

    @staticmethod
    def __add_log_entry(level, message):
        """
        level:
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        """
        log.mjLog.LogReporter("Dominator", level, level.capitalize() + ": " + message)
