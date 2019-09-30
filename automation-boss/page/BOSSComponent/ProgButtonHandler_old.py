"""Module for creating and verifying Emergency hunt group
   File: VCFEHandler.py
   Author: Rahul
"""

import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict

from selenium import webdriver
#For console logs while executing ROBOT scripts
from robot.api.logger import console


#import base
import web_wrappers.selenium_wrappers as base
import log

from CommonFunctionality import CommonFunctionality
__author__ = "Rahul"





#login to BOSS portal
class ProgButtonHandler(object):
    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.common_functionality = CommonFunctionality(self._browser)

    def add_programmable_buttons(self, params):
        """
        `Description:` For adding program buttons handler

        `:param` params:  Dictionary contains programmable button information

        `:return:`

        `Created by:` Kenash K
        """
        try:
            # Navigate to the buttons tab.
            self.common_functionality.switch_page_users()
            self.action_ele.input_text('email_search', params['user_email'])
            self.action_ele.click_element('user_phone_settings')
            self.action_ele.click_element('user_prog_button')

            # Defaults for button 2. The existing tests are all using button #2.
            #type = 'user_select_prog_button_type'
            function_button = 'user_select_prog_button_function'
            long_label = 'user_prog_button_long_label'
            short_label = 'user_prog_button_short_label'
            call_action_param = params.get('callaction', '')
            if not call_action_param:
                extension_button = 'user_select_prog_button_extension'
            else:
                # of course, different xpath for extension if call_action field is present
                extension_button = 'user_select_prog_button_extension_with_call_action'
            call_action = 'user_select_prog_button_call_action'
            digits_field = 'user_prog_button_digits'

            button_number = params.get('button', '')
            button_number = str(button_number)
            # If button number is specified. If not, use button #2.
            if button_number:
                self.action_ele.explicit_wait('User_Ph_Prog_Button_' + button_number + '_IP_Phones')
                self.action_ele.click_element('User_Ph_Prog_Button_' + button_number + '_IP_Phones')
                if button_number != "2":
                    type = 'user_select_prog_button_' + button_number + '_type'
                    function_button = 'user_select_prog_button_' + button_number + '_function'
                    long_label = 'user_prog_button_' + button_number + '_long_label'
                    short_label = 'user_prog_button_' + button_number + '_short_label'
                    if not call_action_param:
                        extension_button = 'user_select_prog_button_' + button_number + '_extension'
                    else:
                        extension_button = 'user_select_prog_button_' + button_number + '_extension_with_call_action'
                    call_action = 'user_select_prog_button_' + button_number + '_call_action'
                    digits_field = 'user_prog_button_' + button_number + '_digits'

            if not button_number:
                self.action_ele.explicit_wait('user_silent_coach')
                self.action_ele.click_element('user_silent_coach')

            # Clear the button first
            #self.unassign_button(type, function_button)

            # Set the button type, if specified.
            #specified_type = params.get('type', '')
            #if specified_type:
            #    self.action_ele.explicit_wait(type)
            #    self.action_ele.select_from_dropdown_using_text(type, specified_type)

            # Set the function.
            self.action_ele.explicit_wait(function_button)
            self.action_ele.select_from_dropdown_using_text(function_button,
                                                            params['function'])
            # Set labels.
            self.action_ele.input_text(long_label,
                                       params['longlabel'])
            self.action_ele.input_text(short_label,
                                       params['shortlabel'])
            # Set extension, if specified.
            extension_param = params.get('extension', '')
            if extension_param:
                self.action_ele.input_text(extension_button, extension_param)

            # Set call action.
            if call_action_param:
                self.action_ele.explicit_wait(call_action)
                self.action_ele.select_from_dropdown_using_text(call_action,  call_action_param)

            # Set digits, if specified.
            digits_param = params.get('digits', '')
            if digits_param:
                self.action_ele.explicit_wait(digits_field)
                self.action_ele.input_text(digits_field, digits_param)

            # Click on save and then on the OK button.
            self.action_ele.explicit_wait('user_prog_button_save')
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            self.action_ele.click_element('user_prog_button_save')
            self.action_ele.explicit_wait("fnMessageBox_OK")
            # Wait for Ajax to complete
            self._browser.waitfor_ajax_complete()
            time.sleep(3)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.click_element("fnMessageBox_OK")
        except Exception, e:
            print(e)
            raise AssertionError("Could not properly program buttons")


    def verify_programmed_button(self, params):
        """
        `Description:` To verify the button has been programmed as per input paramaters.

        `:param` params:  button settings that were specified as input.

        `:return:`

        `Created by:` Vlad Milutinovic
        """
        try:
            # Set default field IDs if 'button' parameter is not specified in input.
            function_field = 'user_select_prog_button_function'
            long_label_field = 'user_prog_button_long_label'
            short_label_field = 'user_prog_button_short_label'
            call_action_param = params.get('callaction', '')
            if not call_action_param:
                extension_field = 'user_select_prog_button_extension'
            else:
                # different xpath for extension if call_action field is present
                extension_field = 'user_select_prog_button_extension_with_call_action'
            call_action_field = 'user_select_prog_button_call_action'
            digits_field = 'user_prog_button_digits'

            # Check if button number is specified. If so, set the field IDs/xpaths appropriately.
            button_number = params.get('button', '')
            button_number = str(button_number)
            if button_number:
                self.action_ele.explicit_wait('User_Ph_Prog_Button_' + button_number + '_IP_Phones')
                self.action_ele.click_element('User_Ph_Prog_Button_' + button_number + '_IP_Phones')
                # The original field IDs are used in case of button #2 so the old test cases are not broken.
                # For other numbers the IDs need to be set.
                if button_number != "2":
                    function_field = 'user_select_prog_button_' + button_number + '_function'
                    long_label_field = 'user_prog_button_' + button_number + '_long_label'
                    short_label_field = 'user_prog_button_' + button_number + '_short_label'
                    if not call_action_param:
                        extension_field = 'user_select_prog_button_' + button_number + '_extension'
                    else:
                        extension_field = 'user_select_prog_button_' + button_number + '_extension_with_call_action'
                    call_action_field = 'user_select_prog_button_' + button_number + '_call_action'
                    digits_field = 'user_prog_button_' + button_number + '_digits'

            # Check the 'function' parameter.
            selected_function = self.query_ele.get_text_of_selected_dropdown_option(function_field)
            if not selected_function or selected_function != params['function']:
                return False

            # Check long label.
            long_label_value = self._browser.element_finder(long_label_field)
            if not long_label_value or long_label_value.get_attribute('value') != params['longlabel']:
                return False

            # Check short label.
            short_label_value = self._browser.element_finder(short_label_field)
            if not short_label_value or short_label_value.get_attribute('value') != params['shortlabel']:
                return False

            # Check 'extension' in case it is provided in input.
            extension_param = params.get('extension', '')
            if extension_param:
                extension_value = self._browser.element_finder(extension_field)
                if not extension_value or not extension_value.get_attribute('value').startswith(extension_param):
                    return False

            # Check 'call action' in case it is specified in input.
            if call_action_param:
                call_action_value = self.query_ele.get_text_of_selected_dropdown_option(call_action_field)
                if not call_action_value or call_action_value != call_action_param:
                    return False

            # Check 'digits' in case it is specified in input.
            digits_param = params.get('digits', '')
            if digits_param:
                digits_value = self._browser.element_finder(digits_field)
                if not digits_value or digits_value.get_attribute('value') != digits_param:
                    return False

            return True

        except Exception, e:
            print(e)
            raise AssertionError("Could not verify that the buttons are properly programmed")

    def unassign_button(self, type, function_button):
        """
        `Description:` To clear the button by setting the function to 'Unused' and saving the changes.
                       Used to make sure the button is unassigned before attempting to program it.

        `:param` params:  button type id and function id.

        `:return:`

        `Created by:` Vlad Milutinovic
        """
        try:
            # Set the type to All.
            self.action_ele.explicit_wait(type)
            self.action_ele.select_from_dropdown_using_text(type, 'All')
            self.action_ele.explicit_wait(function_button)
            # Set the function to 'Unused'.
            self.action_ele.select_from_dropdown_using_text(function_button, 'Unused')
            # Save and click on OK.
            self.action_ele.click_element('user_prog_button_save')
            time.sleep(2)
            self.action_ele.explicit_wait("fnMessageBox_OK")
            time.sleep(2)
            self.action_ele.click_element("fnMessageBox_OK")
        except Exception, e:
            print(e)
            raise AssertionError("Could not unassign buttons")
