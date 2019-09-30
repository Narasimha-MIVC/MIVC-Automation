"""Module for execution of AOB portal functionality
   File: AOB_Functionality.py
   Author: Saurabh Singh
"""

import os
import re
import sys
import time
import datetime
import random
# from time import gmtime, strftime
from collections import defaultdict
import inspect,re
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# For print logs while executing ROBOT scripts
from robot.api.logger import console

# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
#import base
import web_wrappers.selenium_wrappers as base

# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
__author__ = "Saurabh Singh"



_RETRY_COUNT = 3


class AobFunctionality(object):
    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 6  # for retries

    def aob_navigateto_locationanduser(self):
        """
        `Description:` Navigate to Location and User page from Welcome Page
                
        `return:` Status - False or True
                
        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            if self.query_ele.get_text("welcome") == "Welcome":
                print("AOB page opened")
                self._browser._browser.execute_script("window.scrollTo(0, 200);")
                time.sleep(1)
            btn = self._browser._browser.execute_script(
                'return document.querySelector("shor-button").shadowRoot.querySelector(".btn.btn-deepblue ")')
            if btn.text == "Start" or btn.text == "Resume":
                btn.click()
            # time.sleep(5)
            self.action_ele.explicit_wait("tansfer_img")
            if "Skip" in self._browser._browser.page_source:
                print(self.query_ele.get_text("skip_btn"))
                self.action_ele.click_element("skip_btn")
            else:
                print(self.query_ele.get_text("continue_button"))
                self.action_ele.click_element("continue_button")
            time.sleep(1)
            if "Got It" in self._browser._browser.page_source:
                self.action_ele.click_element("aob_tn_got_it_button")
            self.action_ele.explicit_wait("loc_user_btn")
            if self.query_ele.get_text("loc_user_text") == "Locations and Users":
                status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_navigate_to_transfer_requests(self):
        try:
            status = False
            self._browser._browser.execute_script("window.scrollTo(0, 200);")
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            btn = self.query_ele.get_value_execute_javascript(
                'document.querySelector("shor-button").shadowRoot.querySelector(".btn.btn-deepblue ")')

            if btn.text == "Start" or btn.text == "Resume":
                btn.click()

            self.action_ele.explicit_wait("tansfer_img")

            if self.query_ele.get_text("transfer_num_heading") == "Transfer Numbers":
                status = True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_click_transfer_button(self):
        try:
            if "Skip" in self._browser._browser.page_source:
                self.action_ele.click_element("transfer_button")
            else:
                self.action_ele.click_element("transfer_more_button")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_select_other_current_provider(self):
        try:
            self.action_ele.click_element("current_provider_button")
            self.action_ele.click_element("other_provider")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_set_provider_name(self, param):
        try:
            self.action_ele.input_text("other_provider_name", param)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_authorize_transfer_request(self):
        try:
            self.action_ele.click_element("transfer_request_authorization_checkbox_label")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_save_transfer_request(self):
        try:
            self.action_ele.click_element("aob_save_button")
            self.action_ele.click_element("transfer_request_gotit_button")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_goto_transfer_more(self):
        """
        `Description:` Navigate to Transfer more page from Welcome Page

        `return:` Status - False or True

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if self.query_ele.get_text("welcome") == "Welcome":
                print("AOB page opened")
                self._browser._browser.execute_script("window.scrollTo(0, 200);")
                time.sleep(1)
            btn = self.query_ele.get_value_execute_javascript(
                'document.querySelector("shor-button").shadowRoot.querySelector(".btn.btn-deepblue ")')
            if btn.text == "Start" or btn.text == "Resume":
                btn.click()
            # time.sleep(5)
            self.action_ele.explicit_wait("tansfer_img")
            status = True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_validate_location_activation_date(self, params):
        """
        `Description:` Validate the Location Activation Date on AOB page as well as Status in Location and User page
        
        `param params:` Supported status of location
        
        `return:` Status- True or False
        
        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            locations = self._browser.elements_finder("activation_text")
            text = locations[0].text
            loc_names = self._browser.elements_finder("loc_name")
            loc_name = loc_names[0].text
            for each in params:
                if each.lower() in text.lower():
                    status = True
                    break
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return loc_name, text, status

    def validate_geo_location_date(self, params, name):
        """
        `Description:` Validate Geo Location Date on Boss Page

        `:param params:` Date of location

        `:param name:` Name of Location for which date has to validate

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            params = params.split(" ")
            self.action_ele.input_text("loc_name_text", name)
            time.sleep(1)
            geo_date = self._browser.elements_finder("date")
            params = params[-1].split("/")
            geo_date = geo_date[0].text.split("/")
            for i in range(len(params)):
                if int(geo_date[i]) == int(params[i]):
                    status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_back_button(self):
        """
        `Description:` Go to Back page by pressing Back button - Used Java Script because of Shadow Root

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            btn = self.query_ele.get_value_execute_javascript(
                'document.querySelector("shor-button").shadowRoot.querySelector(".btn.btn-footer-back ")')
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", btn)
            time.sleep(1)
            if btn.text == "Back":
                btn.click()
            time.sleep(2)
            self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_page_title(self, param):
        """
        `Description:` Verify the page name.

        `:param param:` Name of Page

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            print(param)
            self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
            if param in self._browser._browser.page_source:
                status = True
            else:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_location_and_user_button(self):
        """
        `Description:` Verify the button "Start" or "Resume" which redirects to User page, is present or not

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            if self.query_ele.get_text("loc_user_btn") == "Start" or self.query_ele.get_text(
                    "loc_user_btn") == "Resume" or self.query_ele.get_text("loc_user_btn") == "Revisit":
                status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_user_page(self):
        """
        `Descrption:` Function will got User page for particular location from Location nad User page

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            revisit = self._browser.elements_finder('revisit_button')  # yet to be used
            all_buttons = self._browser.elements_finder(
                'aob_all_button')  # return all button present on Location and User page
            # if self.query_ele.get_text("loc_user_btn") == "Start" or self.query_ele.get_text("loc_user_btn") == "Resume" or self.query_ele.get_text("loc_user_btn") == "Revisit":
            if all_buttons[0].text == "Start" or all_buttons[0].text == "Resume":  # or all_buttons[0].text == "Revisit"
                self.action_ele.click_element("loc_user_btn")
                self.action_ele.explicit_wait("left_side_block")
            elif self.query_ele.get_text("revisit_button") == "Revisit":
                self.action_ele.click_element("revisit_button")
                # call revisit Function Yet to be written
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_create_user(self, params):
        """
        `Description:` This function used Java Script and Selenium function because of SHADOWROOT tag

        `:param params:` User detail like name, last name, email, extension and Phone number detail

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            time.sleep(2)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            firstName = self.query_ele.get_value_execute_javascript(
                'document.querySelectorAll("shor-textfield#firstName")')
            for each_name in range(len(firstName)):
                if firstName[each_name].is_displayed():
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self.query_ele.get_value_execute_javascript(
                        'document.querySelectorAll("shor-textfield#firstName")[{each_name}].shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    text1[0].clear()
                    text1[0].send_keys(params['firstName'])
                    status = True
                    break
                else:
                    pass
            time.sleep(1)

            lastName = self.query_ele.get_value_execute_javascript(
                'document.querySelectorAll("shor-textfield#lastName")')
            for each_name in range(len(lastName)):
                if lastName[each_name].is_displayed():
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self.query_ele.get_value_execute_javascript(
                        'document.querySelectorAll("shor-textfield#lastName")[{each_name}].shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    text1[0].clear()
                    text1[0].send_keys(params['lastName'])
                    status = True
                    break
                else:
                    pass
            time.sleep(1)

            extension = self.query_ele.get_value_execute_javascript(
                'document.querySelectorAll("shor-textfield#extension")')
            for each_name in range(len(extension)):
                if extension[each_name].is_displayed():
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self.query_ele.get_value_execute_javascript(
                        'document.querySelectorAll("shor-textfield#extension")[{each_name}]'
                        '.shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    text1[0].send_keys(Keys.CONTROL, 'a')
                    time.sleep(1)
                    # if params['extn']!="None":
                    text1[0].clear()
                    text1[0].send_keys(params['extn'])
                    status = True
                    break
                else:
                    pass
            time.sleep(1)

            email = self.query_ele.get_value_execute_javascript(
                'document.querySelectorAll("shor-textfield#useremail")')
            for each_name in range(len(email)):
                if email[each_name].is_displayed():
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self.query_ele.get_value_execute_javascript(
                        'document.querySelectorAll("shor-textfield#useremail")[{each_name}]'
                        '.shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    text1[0].clear()
                    text1[0].send_keys(params['email'])
                    time.sleep(1)
                    text1[0].send_keys(Keys.TAB)
                    status = True
                    break
                else:
                    pass
            time.sleep(1)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            buttons = self._browser.elements_finder("phone_buttons")
            for each in range(len(buttons)):
                if buttons[each].is_displayed():
                    #
                    if params['phone'] == "None" and buttons[each].text == "None":
                        buttons[each].click()
                        try:
                            if "Keep Number" in self._browser._browser.page_source:
                                self.action_ele.click_element("aob_keep_number_button")
                        except:
                            pass
                        print("None Button Click")
                        time.sleep(1)
                        status = True
                        break
                    elif params['phone'] == "Existing" and buttons[each].text == "Existing":
                        print("Existing button clicked")
                        buttons[each].click()
                        try:
                            if "Keep Number" in self._browser._browser.page_source:
                                self.action_ele.click_element("aob_keep_number_button")
                        except:
                            pass
                        drop = self._browser.elements_finder("drop_down_text")
                        for each in drop:
                            if each.is_displayed():
                                #
                                if params['number'] != "None":
                                    # Select(each).select_by_visible_text(params['number'])
                                    params['number'] = params['number'][1:]
                                    Select(each).select_by_value(params['number'])
                                    status = True
                                    break
                                elif params['number'] == "None":
                                    Select(each).select_by_index(1)
                                    status = True
                                else:
                                    pass
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def __aob_verify_user_field(self):
        """
        
        `Description:` Verify the all the user field value
                        This function used Java Script and Selenium function because of SHADOWROOT tag

        `:param params:` User detail

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            # params = defaultdict(lambda: '', params)
            time.sleep(2)

            firstName = self._browser._browser.execute_script(
                'return document.querySelectorAll("shor-textfield#firstName")')
            for each_name in range(len(firstName)):
                if firstName[each_name].is_displayed():
                    # import pdb;
                    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self.query_ele.get_value_execute_javascript(
                        'document.querySelectorAll("shor-textfield#firstName")[{each_name}].shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    fName = text1[0].text
                    break
                else:
                    pass
            time.sleep(1)

            lastName = self._browser._browser.execute_script(
                'return document.querySelectorAll("shor-textfield#lastName")')
            for each_name in range(len(lastName)):
                if lastName[each_name].is_displayed():
                    # import pdb;
                    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self._browser._browser.execute_script(
                        'return document.querySelectorAll("shor-textfield#lastName")[{each_name}].shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    lName = text1[0].text
                    break
                else:
                    pass
            time.sleep(1)

            email = self._browser._browser.execute_script(
                'return document.querySelectorAll("shor-textfield#useremail")')
            for each_name in range(len(email)):
                if email[each_name].is_displayed():
                    # import pdb;
                    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                    self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    text1 = self._browser._browser.execute_script(
                        'return document.querySelectorAll("shor-textfield#useremail")[{each_name}].shadowRoot.querySelectorAll("'
                        '.form-control ")'.format(each_name=each_name))
                    email_name = text1[0].text
                    break
                else:
                    pass
            time.sleep(1)

            buttons = self._browser.elements_finder("phone_buttons")
            for each in range(len(buttons)):
                if buttons[each].is_displayed():
                    #
                    if buttons[each].text == "Existing":
                        val = buttons[each].get_attribute("class")
                        if "active" in val:
                            print("Existing button is seleted")
                            button_status = "Yes"
                            break
                        else:
                            button_status = "No"

            drop = self._browser.elements_finder("drop_down_text")
            for each in drop:
                if each.is_displayed():
                    drop_down_value = Select(each).first_selected_option.text
                    break
            user_values = {}
            user_values['fName'] = fName
            user_values['lName'] = lName
            user_values['email'] = email_name
            user_values['drop'] = drop_down_value
            user_values['btn'] = button_status
            print(user_values)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return user_values

    def verify_message_displayed(self, error_message):
        """
        `Description:` verify the given error message is present on the screen

        `:param` error_message: Error Message

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            #
            error_message = error_message.replace('"', "")
            if error_message in self._browser._browser.page_source:
                print(error_message)
                return True
            else:
                return False
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def remove_popup(self, **params):
        """
        `Description:` To remove Error message popup on User creation page

        `:param` params['button']- Name of button which need to press

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            print(params)
            time.sleep(1)
            try:
                before_heading = self.query_ele.get_text("main_heading")
            except:
                pass
            if params['button'] == "Continue":
                self.action_ele.click_element("leave_button")
                time.sleep(1)
                status = True
            else:
                #
                buttons = self._browser.elements_finder("stay_on_page")
                for each in buttons:
                    if each.is_displayed() and each.text == "Stay on Page":
                        each.click()
                        after_heading = self.query_ele.get_text("main_heading")
                        if before_heading == after_heading:
                            status = True
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def user_page_verification(self):
        """
        `Description` Verify the count of user in each bundle at User page for perticual location.
                       This function will traverse to every bundle and verify the correct number of user

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            block = self._browser.elements_finder("left_side_block")
            if block[0].is_displayed():
                print("Left Hand Side Box is present")

            texts = self._browser.elements_finder("status_bar_text")
            self._browser._browser.execute_script("window.scrollTo(0, 64);")
            for each in texts:
                each.click()
                time.sleep(2)
                each = each.text.split(" ")
                user_count = self._browser.elements_finder("check_icon_for_user")
                print("tab : " + str(each[0]))
                print("User list: " + str(len(user_count)))
                if int(each[0]) == len(user_count):
                    print("Correct number of User Displayed")
                    status = True
                else:
                    status = False
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    break
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_save_and_logout_button(self):
        """
        `Description:` Press Save and Logout Button - Java Script and selenium function has been used because of Shadow Root

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            btn1 = self.query_ele.get_value_execute_javascript('document.querySelectorAll("shor-button")[1].shadowRoot.querySelector(".btn.btn-save-logout ")')
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", btn1)
            # self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            if btn1.text == "Save & Log Out":
                btn1.click()

            for i in range(4):
                ele = self._browser.elements_finder("header_image")
                if len(ele) > 0:  # checking lenght of ele element if its greater then 0 it measn it goes to home page else retry to wait
                    break
                else:
                    time.sleep(2)
            # self.action_ele.explicit_wait("header_image")
            # time.sleep(2)
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_logout_button(self):
        """
        `Description:` Press Save and Logout Button - Java Script and selenium function has been used because of Shadow Root

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            btn1 = self.query_ele.get_value_execute_javascript('document.querySelectorAll("shor-button")[1].shadowRoot.querySelector(".btn.btn-logout ")')
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", btn1)
            # self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            if btn1.text == "Log Out":
                btn1.click()

            for i in range(4):
                ele = self._browser.elements_finder("header_image")
                if len(ele) > 0:  # checking lenght of ele element if its greater then 0 it measn it goes to home page else retry to wait
                    break
                else:
                    time.sleep(2)
            # self.action_ele.explicit_wait("header_image")
            # time.sleep(2)
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_click_button(self, btn):
        """
        `Description:` This function will click "Cancel" and "Save" button

        `:param` btn:  Name of button which need to click

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            if btn == "Cancel":
                buttons = self._browser.elements_finder("cancel_button")
                for each in buttons:
                    if each.is_displayed():
                        each.click()
                        time.sleep(2)
                        break

            elif btn == "Save":
                buttons = self._browser.elements_finder("aob_save_button")
                for each in buttons:
                    if each.is_displayed():
                        each.click()
                        time.sleep(3)
                        block = self._browser.elements_finder("progress_bar")
                        print(block[0].is_displayed())
                        for i in range(self.counter):
                            if block[0].is_displayed():
                                time.sleep(3)
                                print("Extending Wait")
                            else:
                                print("Progress bar removed")
                                break
                        break

            elif btn == "Revisit":
                buttons = self._browser.elements_finder("aob_revisit")
                if len(buttons)>0:
                    buttons[0].click()

            elif btn == "Add User Type":
                self.action_ele.click_element("add_type_button")

            elif btn == "Continue":
                self.action_ele.click_element("continue_button")

            elif btn == "Got It":
                try:
                    self.action_ele.click_element("aob_tn_got_it_button")
                except:
                    pass

            elif btn.lower() == "Return Number".lower():
                try:
                    self.action_ele.click_element("aob_return_number_btn")
                except:
                    pass

            elif btn.lower() == "Keep Number".lower():
                try:
                    self.action_ele.click_element("aob_keep_number_btn")
                except:
                    pass

            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_user_field(self):
        """
        `Description:` To verify all user field are reset properly or not in user form.

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            names = self._browser.elements_finder("user_names")
            for each in names:
                if each.text == "New User 1":
                    each.click()
                    params = self.__aob_verify_user_field()
                    #
                    if params['fName'] == '' and params['lName'] == '' and params['email'] == '' and params[
                        'drop'] == 'Select' and params['btn'] == "Yes":
                        status = True
                        print("All field are reseted")
                    else:
                        print("All filed were not reseted properly")
                        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_location_label(self):
        """
        `Description:` Validate and check if the location are in sorted order or not.
                       This function wlll take button name as well as Location name to validate the sorted order.

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            location = []
            location2 = []
            #
            names = self._browser.elements_finder("location_labels")
            btn_names = self._browser.elements_finder("aob_all_button")
            for each in range(len(btn_names)):
                if btn_names[each].text == "Resume" or btn_names[each].text == "Start":
                    location.append(names[each].text)
                else:
                    location2.append(names[each].text)
            print(location)
            sorted_locations = sorted(location)
            sorted_locations2 = sorted(location2)
            if sorted_locations == location and sorted_locations2 == location2:
                status = True
                print("Location is in Sorted order")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_bundle_switch(self):
        """
        `Description:' Traverse through every bundle till the last and verify the its heading.

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            headings = self._browser.elements_finder("bundle_heading")
            for each in headings:
                each.click()
                time.sleep(1)
                print(each.text)
                heading_name = self.query_ele.get_text("main_heading")
                if each.text in heading_name:
                    status = True
            self._browser._browser.execute_script("window.scrollTo(0, 100);")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_click_next_bundle(self):
        """
        `Description:` Click on Next bundle on User page and validate the bundle heading example:
            self.action_ele.click_element("bundle_heading", index=0)
            self.action_ele.click_element("bundle_heading", index=1)
            self.action_ele.click_element("bundle_heading", value='Telephony')
            self.action_ele.click_element("bundle_heading", index=0,value='Elite')
            self.action_ele.click_element("bundle_heading_1")
            self.action_ele.click_element("bundle_heading_3")
            self.action_ele.click_element("bundle_heading_0")

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            headings = self._browser.elements_finder("bundle_heading")
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", headings[1])
            headings[1].click()
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_click_skip_user(self):
        """
        `Description:` Click on Skip user button.

        `return:` Status- True or False and Heading name before it clicks
                   (this will be use in some function to check if the what is the bundle name before clicking skip.)

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            #
            heading = self.query_ele.get_text("main_heading")
            names = self._browser.elements_finder("user_names")
            for each in names:
                if each.text == "New User 1":
                    each.click()
            time.sleep(1)
            headings = self._browser.elements_finder("left_side_block")
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", headings[-1])
            time.sleep(1)
            if "Continue" not in self._browser._browser.page_source:
                self.action_ele.click_element("skip_button")
            else:
                self.action_ele.click_element("skip_btn")
            time.sleep(1)
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status, heading

    def aob_check_bundle_name(self, name):
        """
        `Description:` Check the name of bundle and validate if it switches or not

        `:param` name: Name of bundle

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            #
            left_container = self._browser.elements_finder("left_side_block")
            if left_container[0].is_displayed():
                current_bundle = self.query_ele.get_text("main_heading")
                print(name)
                print(current_bundle)
                if name != current_bundle:
                    status = True
            else:
                if self.verify_page("Call handling for "):
                    status = True
                    print("User was on last bundle.")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_check_user_name(self, name, bundle_name):
        """
        `Description:` Check if Correct user is listed or not in AOB user creation page

        `:param`s name: Name of User

        `:param`s bundle_name: Name of bunlde (in case bundle switch happened)

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #
            user_names = self._browser.elements_finder("user_names")
            for each_name in user_names:
                if each_name.text == name:
                    status = True
                    break
            if status == False:
                bundle_heading = self._browser.elements_finder("aob_left_container_names")
                for each in bundle_heading:
                    if each.text in bundle_name:
                        each.click()
                        if name in self._browser._browser.page_source:
                            status = True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_help_url(self, **params):
        """
        `Description:` Navigating to Help url page.

        `:param` params:  Dictionary consiting User detail and URL to validate

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #
            # if params['user'] == '' and params['pwd'] == '':
            #     print("Please provide salesforce credentials")
            #     return False
            self.action_ele.click_element("aob_help_url")
            self.action_ele.switch_to_window(2)
            # if self._browser._browser.current_url != params['url']:
            # if self._browser._browser.current_url not in params['url']:
            #     user = self._browser.elements_finder("aob_help_page_user_name")
            #     if user[0].is_displayed():
            #         self.action_ele.input_text("aob_help_page_user_name", params['user'])
            #         self.action_ele.input_text("aob_help_page_password", params['pwd'])
            #         time.sleep(1)
            #         self.action_ele.click_element("aob_help_submit")
            #         self.action_ele.explicit_wait("aob_help_page_Search")
            #         time.sleep(1)
            #         page_url = self._browser._browser.current_url
            #         if page_url in params['url']:
            #             status = True
            #     else:
            #         status = False
            #         self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            # else:
            #     if self._browser._browser.current_url in params['url']:
            #         status = True
            page_url = self._browser._browser.current_url
            if page_url in params['url']:
                status = True
            self._browser._browser.close()
            self.action_ele.switch_to_window(1)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_clear_users_fields(self, params):
        """
        Description: Clear all  user fields
                     Shadow Root Function Selenium and Java Script is being used

        `:param`   params: Name of Field which need to be clear

        `return:` Return status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params == "FirstName":
                firstName = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#firstName")')
                for each_name in range(len(firstName)):
                    if firstName[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#firstName")[{each_name}].shadowRoot.querySelectorAll("'
                            '.form-control ")'.format(each_name=each_name))
                        text1[0].send_keys(Keys.CONTROL, 'a')
                        text1[0].send_keys(Keys.BACKSPACE)
                        status = True
                        break
                    else:
                        pass
                time.sleep(1)

            elif params == "LastName":
                lastName = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#lastName")')
                for each_name in range(len(lastName)):
                    if lastName[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#lastName")[{each_name}].shadowRoot.querySelectorAll("'
                            '.form-control ")'.format(each_name=each_name))
                        text1[0].send_keys(Keys.CONTROL, 'a')
                        text1[0].send_keys(Keys.BACKSPACE)
                        status = True
                        break
                    else:
                        pass
                time.sleep(1)

            elif params == "Extension":
                extension = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#extension")')
                for each_name in range(len(extension)):
                    if extension[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#extension")[{each_name}]'.format(
                                each_name=each_name))
                        # for each in range(len(text1.get_attribute('val'))):
                        text1.click()
                        text1.send_keys(Keys.CONTROL, 'a')
                        text1.send_keys(Keys.BACKSPACE)
                        text1.send_keys(Keys.TAB)
                        status = True
                        break
                    else:
                        pass
                time.sleep(1)

            elif params == "Email":
                #
                email = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#useremail")')
                for each_name in range(len(email)):
                    if email[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#useremail")[{each_name}].shadowRoot.querySelectorAll("'
                            '.form-control ")'.format(each_name=each_name))
                        e_name = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#useremail")[{each_name}].shadowRoot.querySelectorAll("'
                            '.form-control ")[0].value'.format(each_name=each_name))
                        for each in e_name:
                            text1[0].send_keys(Keys.CONTROL, 'a')
                            text1[0].send_keys(Keys.BACKSPACE)
                        status = True
                        break
                    else:
                        pass
                time.sleep(1)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_error_message(self, params, field):
        """
        `Description:` To validate the error message on AOB page while clearing fields
                        Shadow Root Function Selenium and Java Script is being used

        `:param` params: params- Error Message

        `:param`: filed- Name of field which has been cleared

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if field == "FirstName":
                firstName = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#firstName")')
                for each_name in range(len(firstName)):
                    if firstName[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#firstName")[{each_name}].shadowRoot.querySelectorAll("'
                            '.help-block")'.format(each_name=each_name))
                        print(text1[0].text)
                        print(params)
                        if text1[0].text == params:
                            return True
                        else:
                            pass
                time.sleep(1)
            elif field == "LastName":
                lastName = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#lastName")')
                for each_name in range(len(lastName)):
                    if lastName[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#lastName")[{each_name}].shadowRoot.querySelectorAll("'
                            '.help-block")'.format(each_name=each_name))
                        print(text1[0].text)
                        print(params)
                        if text1[0].text == params:
                            return True
                        else:
                            pass
                time.sleep(1)

            elif field == "Extension":
                extension = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#extension")')
                for each_name in range(len(extension)):
                    if extension[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#extension")[{each_name}].shadowRoot.querySelectorAll("'
                            '.help-block")'.format(each_name=each_name))
                        print(text1[0].text)
                        print(params)
                        if params in text1[0].text:
                            return True
                        else:
                            pass
                time.sleep(1)

            elif field == "Email":
                #
                email = self._browser._browser.execute_script(
                    'return document.querySelectorAll("shor-textfield#useremail")')
                for each_name in range(len(email)):
                    if email[each_name].is_displayed():
                        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        text1 = self.query_ele.get_value_execute_javascript(
                            'document.querySelectorAll("shor-textfield#useremail")[{each_name}].shadowRoot.querySelectorAll("'
                            '.help-block")'.format(each_name=each_name))
                        print("Actual_Message: "+str(text1[0].text))
                        print(params)
                        if text1[0].text == params:
                            return True
                        else:
                            pass
                time.sleep(1)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_created_user(self):
        """
        `Description:` Check if User is created in bundle or not.

        `return:` True- If created
                  False- If user is not created

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            #
            bundles = self._browser.elements_finder("left_side_block")
            bundles[0].click()  # forcefully cliking on first bundle
            user_num = self._browser.elements_finder("check_icon_for_user")
            if len(user_num) >= 1:
                user_num[0].click()
                status = True
            else:
                status = False
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_get_bundle_name(self):
        """
        `Description:` Get the current selected bundle name

        `return:` Bundle Name

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            bundle_name = self.query_ele.get_text("main_heading")
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status, bundle_name

    def aob_user_switch(self, params):
        """
        `Description:` Check if it switched to next user upon in same bundle upon clikcing Save button

        `params:` params: firstName, lastName and Bundle name of user dictionary

        `return:` True - On Success
                False- on Fails

        `created by:` Saurabh Singh
        """
        try:
            status = False
            status3 = False
            status2 = False
            status1 = False
            time.sleep(1)
            print(params)
            # status, bundle=self.aob_get_bundle_name()
            status1 = self.aob_check_user_name(params['firstName'] + " " + params['lastName'], params['bundle'])
            #
            time.sleep(1)
            current_bundle_name = self.query_ele.get_text("main_heading")
            if current_bundle_name == params['bundle']:
                status2 = True
            else:
                bundle_names = self._browser.elements_finder("bundle_heading")
                for each in bundle_names:
                    each.click()
                    current_bundle_name = self.query_ele.get_text("main_heading")
                    if current_bundle_name == params['bundle']:
                        status2 = True
            self._browser._browser.refresh()
            users = self._browser.elements_finder("user_names")
            for each in users:
                if each.text == "New User 1":
                    status3 = True
                    break
                else:
                    print("No User Left in bundle")
                    status3 = True
            if status2 and status3:
                status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_verify_user_inBoss(self, usermailid):
        """
        `Description:` Verify AOB User in Boss Portal User page

        `:param` usermailid: email id of user

        `return:` status

        `created by:` Saurabh Singh
        """
        try:
            status = False
            self._browser._browser.refresh()
            time.sleep(3)
            self.action_ele.explicit_wait('email_search')
            self.action_ele.input_text('email_search', usermailid)
            self.action_ele.explicit_wait("aob_user_link")
            user_list = self._browser.elements_finder("aob_user_link")
            if len(user_list) == 1:
                status = True
                print("User found")
            else:
                print("More then one or no user present")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_enables_disbale_drop_down(self, params):
        """
        `Description:` This function will enable or disable phone number dropdown box on user creation page based on user input

        `:param` params: name of button "Exiating" or "None"

        return:  Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            buttons = self._browser.elements_finder("phone_buttons")
            #
            for each in buttons:
                if each.is_displayed():
                    if params == each.text:
                        each.click()
                        break
            drop_down = self._browser.elements_finder("drop_down_text")
            for each in drop_down:
                if each.is_displayed():
                    if each.is_enabled() and params == "Existing":
                        status = True
                    elif params == "None":
                        if not each.is_enabled():
                            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_check_user_with_profile(self):
        """
         `Description:` Check if User is created with profile (phone number) in bundle or not.

         `return:` Status True or False

         `created by:` Saurabh Singh
         """
        try:
            status = False
            time.sleep(1)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            bundles = self._browser.elements_finder("left_side_block")
            for bundle in bundles:
                if status == False:
                    bundle.click()
                    user_num = self._browser.elements_finder("aob_get_phone_number")
                    for each in user_num:
                        if len(user_num) >= 1:
                            if each.text != "":
                                num = each.text
                                status = True
                                each.click()
                                break
                        else:
                            status = False
                else:
                    break
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status, num

    def aob_check_if_number_available(self, num):
        """
         `Description:` Check if Phone number becomes available or not after unassigned.

         `return:` Status True or False

         `created by:` Saurabh Singh
         """
        try:
            status = False
            time.sleep(1)
            xList = []
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            drop1 = self._browser.elements_finder("add_type_button")
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", drop1[0])
            drop = self._browser.elements_finder("get_all_number")
            for each in drop:
                if status == False:
                    if each.is_displayed():
                        xList = each.text.split("\n")
                        for i in xList:
                            if num == i.strip():
                                status = True
                                break
                else:
                    break
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_validate_location_status(self, params):
        """
        `Description:` Validate the Location Status in all available location on Location and User page
                       Takes input of location status

        `:param` params: location

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #
            location_status = self._browser.elements_finder("activation_text")
            all_button = self._browser.elements_finder("aob_all_button")
            for each in range(len(location_status)):
                if params['status'] in location_status[each].text:
                    if params['btn_name'] != "None":
                        if params['btn_name'] == all_button[each].text:  # if loc status and button both matched
                            status = True
                            break
                    else:
                        status = True
                        print("No Button is available for this location state")
                        break
            if status == False:
                print("Location Status is not present currently")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_create_multiple_user(self, params):
        """
        `Description:` Create multiple user - (Baically used to create all the user in particular bundle)

        `:param` params: User detail

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            console(params)
            block = self._browser.elements_finder("left_side_block")
            if block[0].is_displayed():
                print("Left Hand Side Container is present")
            texts = self._browser.elements_finder("bundle_user_count")
            self._browser._browser.execute_script("window.scrollTo(0, 64);")
            #
            time.sleep(2)
            count = texts[1].text.split(" ")
            for each in range(int(count[-1])):
                params['extn'] = random.randint(1000, 8999)
                params['email'] = str(random.randint(100, 8999)) + "_" + params[
                    'email']  # adding random number here because number of user availble to create is not certain
                self.aob_create_user(params)
                self.aob_click_button("Save")
            if params['bundle'] != self.query_ele.get_text("main_heading"):
                status = True
            if status == False:
                bundles = self._browser.elements_finder("bundle_heading")
                if bundles[-1].text in self.query_ele.get_text("main_heading"):
                    print("User was in last bundle")
                    status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_get_location_name(self):
        """
        `Description:` Fetch the current location name which is in progress from location and user page in AOB

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            time.sleep(2)
            #
            location_status = self._browser.elements_finder("location_labels")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return location_status[0].text

    def aob_get_intial_order_detail(self, name):
        """
        `Description:` Verify the Initial order sate in Order Page

        `:param` name: Location Name

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            self.action_ele.select_from_dropdown_using_text("aob_order_status", "Pending")
            time.sleep(1)
            self.action_ele.input_text("location_text_field", name)
            time.sleep(1)
            #
            self.action_ele.click_element("aob_order_id")
            self.action_ele.explicit_wait("save_button")
            self.action_ele.click_element("order_items")
            bundle_desc = self._browser.elements_finder("bundle_desc")
            bundle_quantity = self._browser.elements_finder("bundle_quantity")
            bundle = {}
            for i in range(len(bundle_desc) - 1):
                bundle[bundle_desc[i].text] = bundle_quantity[i].text
            console(bundle)
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status, bundle

    def aob_verify_inital_order(self, params):
        """
        Description: Verify the Initial order sate in AOB Page

        `:param` params: Intial order detail

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #
            bundle_heading = self._browser.elements_finder("bundle_heading")
            for each in bundle_heading:
                each.click()
                for i in params.keys():
                    if each.text in i:
                        count = self.query_ele.get_text("aob_status_text_for_user_count")
                        if "additional" not in count:
                            count = count.split(" ")
                            count = count[-1]
                        else:
                            count = count.split(" ")
                            count = count[2]
                        if params[i] == count:
                            status = True
                        else:
                            status = False
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_check_user_in_current_budnle(self):
        """
        `Description:` Check for current user in current bundle is available to create

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #
            count = self.query_ele.get_text("aob_status_text_for_user_count")
            if "additional" not in count:
                count = count.split(" ")
                lastcount = count[-1]
            else:
                count = count.split(" ")
                lastcount = count[2]
            if int(count[0]) < int(lastcount):
                status = True
            else:
                status = False
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_zoom_in_zoom_out(self):
        """
        `Description:` Zoom in and zoom out the screen

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            i = 100
            while i > 0:
                self.query_ele.get_value_execute_javascript('document.body.style.zoom="{size}%"'.format(size=i))
                time.sleep(1)  # Implemented wait to see the zoomin and zoom out properly
                i -= 25
            while i < 101:
                self.query_ele.get_value_execute_javascript('document.body.style.zoom="{size}%"'.format(size=i))
                time.sleep(1)  ##Implemented wait to see the zoomin and zoom out properly
                i += 25
                status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_check_aob_link(self):
        """
        `Description:` Check if AOB setup link is available on page or not

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            self.action_ele.click_element("Phone_system_tab")
            # status = self.query_ele.element_enabled("aob_setup_link")
            status = 'Mitel Easy Setup' in self._browser._browser.page_source
            if status:
                status = self.query_ele.element_enabled("aob_setup_link")
            else:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_verify_location_status(self, location):
        """
        `Description:` Verify the location status in Geo location Page

        `:param` location:Location name

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            self.action_ele.explicit_wait("geo_location_status")
            time.sleep(3)
            self.action_ele.select_from_dropdown_using_text("geo_location_status", "Pending")
            el = self._browser.elements_finder("geo_location_name_field")
            lis = []
            for each in range(len(el)):
                lis.append(el[each].text)
            if location in lis:
                print "Location is in Pending State"
                status = True
            else:
                print "Location is not in Pending State"
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_callhandling_setup(self, btn):
        """
        `Description:` Function to click on Setup or Don't Setup button

        `:param` btn: Button Name

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            time.sleep(2)
            if "Don't Set Up" in self._browser._browser.page_source or ("Continue" in self._browser._browser.page_source and "Set Up" in self._browser._browser.page_source):
                if btn.lower() == "Don't Set Up".lower():
                    if "Continue" in self._browser._browser.page_source:
                        self.action_ele.click_element("ch_continue")
                        status = True
                    else:
                        self.action_ele.click_element("ch_dont_Setup")
                        status = True

                elif btn.lower() == "Set Up".lower():
                    try:
                        self.action_ele.click_element("ch_setup")
                    except:
                        pass
                        #self.action_ele.click_element("aob_ch_page_button")
                    status = True

                elif btn.lower() == "Reset".lower() or btn.lower() == "Update".lower():
                    buttons = self._browser.elements_finder("aob_ch_page_button")
                    for each in buttons:
                        if btn.lower() == each.text.lower():
                            each.click()
                            status = True
                            break

                elif btn.lower() == "Reset Call Handling".lower() or btn.lower() == "Don't Reset".lower():
                    buttons = self._browser.elements_finder("aob_ch_reset_page_button")
                    for each in buttons:
                        if btn.lower() == each.text.lower():
                            each.click()
                            status = True
                            break

            elif btn.lower() == "Save".lower() or btn.lower() == "Cancel".lower():
                buttons = self._browser.elements_finder("aob_ch_page_button")
                for each in buttons:
                    if btn.lower() == each.text.lower():
                        each.click()
                        try:
                            self.action_ele.explicit_wait("aob_ch_icon_after_setup")
                        except:
                            self.action_ele.explicit_wait('aob_ch_business_hours_icon')
                        status = True
                        break

            elif btn.lower() == 'Revisit'.lower():
                self.action_ele.click_element('Revisit_button')
                status = True

            elif btn.lower() == 'New Voicemail'.lower():
                self.action_ele.click_element('New_Voicemail_button')
                status = True

            elif btn.lower() == 'Add'.lower():
                self.action_ele.click_element('CH_Add_button')
                status = True

            elif btn.lower() == 'Skip this step'.lower():
                self.action_ele.click_element('Skip_this_step_link')
                status = True
            elif btn.lower() == 'Confirm'.lower():
                self.action_ele.click_element('CH_confirm_button')
                status = True

            else:
                print("Call Handling setup is already completed.Kindly reset call handling to do it again.")
                return False

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_select_future_day(self):
        """
        `Description:` Enter Date into Activation page at Future date field

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            lables = self._browser.elements_finder("act_option")
            lables[1].click()
            date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%m/%d/%Y")
            self.action_ele.clear_input_text_new("aob_future_date_textbox")
            time.sleep(1)  # time take to enable text box and enter text
            self.action_ele.input_text("aob_future_date_textbox", date)
            #self.action_ele.click_element("act_heading")
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_save_and_finsih(self):
        """
        `Description:` This function will click "Save and  Finish" button on Activation Page in AOB
                        Shadowroot is found hence CSS value is being used.

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            btn1 = self._browser._browser.execute_script(
                'return document.querySelectorAll("shor-button")[0].shadowRoot.querySelector(".btn.btn-deepblue.width-127 ")')
            btn1.click()
            block = self._browser.elements_finder("progress_bar")
            for i in range(6):
                if not "Locations and Users" in self._browser._browser.page_source:
                    time.sleep(3)  # implemented for retries
                    print("Extending Wait")
                else:
                    print("Progress bar removed")
                    break

            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_create_all_user_in_location(self, params):
        """
        `Description:` Create all remaining user for particular location

        `:param` params: User Detail

        `return:` Status True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(1)
            import random
            console(params)
            #
            bundle_name = self._browser.elements_finder("aob_left_container_names")
            for each in range(len(bundle_name)):
                count = self.query_ele.get_text("aob_status_text_for_user_count")
                if "additional" not in count:
                    count = count.split(" ")
                    lastcount = count[-1]
                else:
                    count = count.split(" ")
                    lastcount = count[2]
                self._browser._browser.execute_script("window.scrollTo(0, 64);")
                lastcount = int(lastcount) - int(count[0])  # to get the count of remaining user
                for each in range(int(lastcount)):
                    params['extn'] = random.randint(1000, 8999)
                    params['email'] = str(random.randint(100, 8899)) + "_" + params['email']
                    self.aob_create_user(params)
                    self.aob_click_button("Save")
            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    ####################AOB Regression########################
    def aob_check_current_active_user(self):
        """
        `Description:`  This function will check if current active user is new user or not

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            active_users=self._browser.elements_finder("active_user_field")
            if len(active_users)==1 and "New User 1" in self._browser._browser.page_source:
                print("Current active user is new user.")
                status = True
            else:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_go_to_bundle(self,bundlename):
        """
        `Description:`  This function will go to specific bundle

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            bundles=self._browser.elements_finder("bundle_heading")
            for bundle in bundles:
                bundle.click()
                if bundlename == self.query_ele.get_text("main_heading"):
                    status = True
                    break
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_activate_icon_state(self,icon):
        """
        `Description:`  This function will check if status icon is enable or disable.

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if icon.lower() == "Activate".lower():
                element=self._browser.elements_finder("activate_icon")
            elif icon.lower() == "Call Handling".lower():
                element=self._browser.elements_finder("callhadnling_text")
            if "grey" in element[0].get_attribute('class'):
                status = True
            else:
                status = False
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_welcome_page_start_button_exists(self):
        try:
            btn = self._browser._browser.execute_script(
                'return document.querySelector("shor-button").shadowRoot.querySelector(".btn.btn-deepblue ")')
            if btn.text == "Start" or btn.text == "Resume":
                return True
            else:
                return False
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_element_exists(self, element):
        try:
            elements = self._browser.elements_finder(element)
            if len(elements) > 0:
                return True
            else:
                return False
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_click_element(self, element, sleep_seconds = 0):
        try:
            self.action_ele.click_element(element)
            
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
            
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_get_text(self, element):
        try:
            return self.query_ele.get_text(element)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_verify_text(self, text, regexp):
        try:
            match = re.match(regexp, text)
            if match:
                return True
            else:
                return False
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_call_handling_setup_selection(self,option):
        """
        `Description:`  This function will select phone number in Call hadling page

        `params:`  option: Name of button.

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            buttons= self._browser.elements_finder("aob_ch_button")
            for button in buttons:
                if option.lower() == button.text.lower():
                    button.click()
                    break
            else:
                status = False
                print("Button is not present.")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return status
            if option =="Existing":
                drop = self._browser.elements_finder("aob_ch_drop_down")
                for each in drop:
                    if each.is_displayed():
                        Select(each).select_by_index(1)
                        status = True
                        break
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            elif option =="New":
                for i in range(3):
                    if self._browser.element_finder("CH_Change_button").is_enabled():
                        status = True
                        print("New Number is generated")
                        break
                    else:
                        time.sleep(2)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def refresh_browser(self):
        """
        `Description:`  This function will refresh the browser

        `created by:` Saurabh Singh
        """
        try:
            self._browser._browser.refresh()
            time.sleep(3)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_check_call_handling_setup(self):
        """
        `Description:`  This function will chek if call handling feature is setted up or not

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            time.sleep(2)
            if "Reset" in self._browser._browser.page_source and "Update" in self._browser._browser.page_source:
                status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_get_first_available_number(self):
        """
        `Description:`  This function will fetch first available number from user. Return False if no number is available

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            #drop1 = self._browser.elements_finder("add_type_button")
            #self._browser._browser.execute_script("arguments[0].scrollIntoView();", drop1[0])
            drop = self._browser.elements_finder("get_all_number")
            for each in drop:
                if status == False:
                    if each.is_displayed():
                        self._browser._browser.execute_script("arguments[0].scrollIntoView();", each)
                        xList = each.text.split("\n")
                        number=xList[0].strip()
                else:
                    break
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status,number

    def aob_check_available_phone_number_in_call_handling_page(self,num):
        """
        `Description:`  This function will check if number is available on call handling page

        `params:`  num: Number which need to valdate

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            drop=self._browser.elements_finder("test") #test has xpath //select. Might have to modify later in AOB.map file if UI changes
            for each in drop:
                xList = each.text.split("\n")
                for x in xList:
                    if x.strip() == num.strip():
                        status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_configure_transfer_more_page(self,param):
        """
        `Description:`  This function will add phone numbers to tranfer more number page

        `params:`  num: Number which need to valdate

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            number=0  #save pervious number inorder to check if the same number has added before or not. If it is it will add 1 to number and add
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            try:
                if self._browser.element_finder("aob_transfer_button").is_displayed():
                    self.action_ele.click_element("aob_transfer_button")
            except:
                if self._browser.element_finder("aob_transfer_more_button").is_displayed():
                    self.action_ele.click_element("aob_transfer_more_button")
            time.sleep(1)
            el=self._browser.elements_finder("aob_cp_drop_down_box")
            if el[0].is_displayed():
                print("Transfer more page is opened")

            elements = self._browser.elements_finder("aob_current_provider")
            dropdown = self._browser.elements_finder("aob_cp_drop_down_box")
            for each in dropdown:
                if each.is_displayed():
                    if param["currentProvider"]!=None:
                        for each1 in elements:
                            if each1.text == param["currentProvider"]:
                                each1.click()
                                break
                    else:
                        elements[1].click()

            textfield = self._browser.elements_finder("aob_tn_text")
            for i in textfield:
                if i.is_displayed():
                    if number != int(param["numberRange"]):
                        i.send_keys(param["numberRange"])
                        #self.action_ele.input_text("aob_tn_text",param["numberRange"])
                    else:
                        param["numberRange"] = int(param["numberRange"])+1 #if number exist then this part will be executed
                        i.send_keys(param["numberRange"])
                        #self.action_ele.input_text("aob_tn_text_field", param["numberRange"])
                        number = param["numberRange"]
            self._browser._browser.execute_script("window.scrollTo(0, 200);")
            self.action_ele.click_element("aob_tn_check")
            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_verify_learn_more_url(self,params):
        """
        `Description:`  This function will verify the Learn More url on user page
        `params:`  num: Number which need to valdate

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.click_element("aob_learn_more")
            self.action_ele.switch_to_window(2)
            if self._browser._browser.current_url not in params['url']:
                status = False
            else:
                status = True
            self._browser._browser.close()
            self.action_ele.switch_to_window(1)
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_activationpage_calendar(self):
        """
        `Description:`  This function will verify if the calendar is present in page

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            calendar = self._browser.elements_finder("aob_activation_calendar")
            if calendar[0].is_displayed():
                status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_click_on_calendar(self):
        """
        `Description:`  This function will click on calendar

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            lables = self._browser.elements_finder("act_option")
            lables[1].click()
            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_calendar_enabled(self):
        """
        `Description:`  This function will verify if the calendar is enabled in page

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            calendar = self._browser.element_finder("aob_activation_calendar")
            if calendar.is_enabled():
                status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_transfer_number_is_created(self):
        """
        `Description:`  This function will check if any number is added in transfer page

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            tn_number = self._browser.elements_finder("aob_transfer_number_entry")
            if len(tn_number) > 1:
                status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_open_two_section(self):
        """
        `Description:`  This function will check if only one section can be opned at same time

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            all_drop_down_box = self._browser.elements_finder("aob_tn_text")
            tn_entry = self._browser.elements_finder("aob_transfer_number_entry")
            tn_entry[0].click()
            for each in range(len(all_drop_down_box)):
                if all_drop_down_box[each].is_displayed():
                    if len(tn_entry) > 1: #to check entries on transfer number page if entries are morethen one then this part will be executed
                        tn_entry[each+1].click()
                        if not all_drop_down_box[each].is_displayed():
                            status = True
                            break
                    else:
                        print("There are no two section present. Test case can not be executed")
                        status = False
                        break

        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_verify_phone_number_on_transfer_number_page(self,num):
        """
        `Description:`  This function will verify the given number presented on callhandling page.

         `params:` num- Number to be validated

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            number_list = self._browser.elements_finder("aob_transfer_page_number")[1:]
            for each in number_list:
                ch_num = re.sub('\(*\)*-* *','',str(each.text))
                if ch_num == num:
                    status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status,num

    def aob_activation_verify_temporary_link(self,linkText):
        """
        `Description:`  This function will verify if temporary number link is available on Activation page or not

         `params:` linkText- Link Text to verify

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            if linkText in self._browser._browser.page_source :
                links = self._browser.elements_finder("aob_temparory_number_link")
                for each_link in links:
                    if each_link.is_displayed() and each_link.text == linkText:
                        status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_activate_icon_visiblity(self,icon):
        """
        `Description:`  This function will check if status icon is presnet

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            element=self._browser.elements_finder("aob_icon")
            for each_element in element:
                if each_element.text.lower() == icon.lower() and each_element.is_displayed():
                    status = True
                    break
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_tab_click(self,tabName):
        """
        `Description:`  This function will click on Tab of Transfer Number and SetUp

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            tab_names = self._browser.elements_finder("aob_tabs")
            for each_tab in tab_names:
                if tabName.lower() == each_tab.text.lower():
                    each_tab.click()
                    status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_ch_setup_business_hour(self,params):
        """
        `Description:`  This function will configure bunisess hour for ch

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if not "Reset" in self._browser._browser.page_source:
                self.action_ele.click_element("aob_ch_business_hour_add")
                days = self._browser.elements_finder("aob_ch_business_hour_days")
                for each_day in params['days']:
                    for business_day in days:
                        if business_day.text.lower() == each_day.lower():
                            business_day.click()
                            break

                starttime = self._browser.element_finder("aob_ch_business_hour_start_time")
                starttime.send_keys(params['startTime'])

                endtime = self._browser.element_finder("aob_ch_business_hour_end_time")
                endtime.send_keys(params['endTime'])

                self.action_ele.click_element("aob_ch_business_hour_save_button")   #in future if cancel button test case comes add here and pass a flag frm variable file
            else:
                print("Business Hour is already setted up")
            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_ch_setup_operator_rings(self,params):
        """
        `Description:`  This function will configure rings number and clear ring number

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['clear'] == "Yes":
                self.action_ele.clear_input_text_new("aob_operator_number_rings")
                status = True
            else:
                self.action_ele.input_text("aob_operator_number_rings",params["ringNum"])
                if str(int(params["ringNum"])*4) in self.query_ele.get_text("aob_operator_ring_text"):
                    status = True

        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_delete_transfer_number_entry(self):
        """
        `Description:`  This function will clear transfer number entry also also verifies if entry is deleted

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            all_drop_down_box = self._browser.elements_finder("aob_tn_text")
            tn_entry = self._browser.elements_finder("aob_transfer_number_entry")
            tn_entry[1].click()
            delete_buttons = self._browser.elements_finder("aob_tn_delete_button")
            for button in delete_buttons:
                if button.is_displayed() and button.text == "Delete":
                    print("Delete button is present")
                    button.click()
                    break

            block = self._browser.elements_finder("progress_bar")   #code to wait till progress bar is displayed
            print(block[0].is_displayed())
            for i in range(self.counter):
                if block[0].is_displayed():
                    time.sleep(3)
                    print("Extending Wait")
                else:
                    print("Progress bar removed")
                    break
            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def get_dgrid_values(self,columnName, grid):
        """
        `Description:`  This function will get all the values from the grid

        `params:`  num: Number which need to valdate

        `return:`  Status - True or False

        `created by:` Saurabh Singh
        """
        try:
            status = False

            grid=self._browser.elements_finder(grid)
            dict={}
            for each in range(len(grid)):
                print grid[each].get_attribute("title")
                x=grid[each].get_attribute("title")
                dict[x]= []
                if x == columnName:
                    index=each+1
            print index
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            col_name=self._browser._map_converter("user_page_slick_grid")['BY_VALUE']
            #col_name=col_name+"["+str(index)+"]"
            #self._browser._browser.find_elements_by_xpath(col_name)
            vals= self._browser._browser.execute_script("return {grid_value}.getData().getItems()".format(grid_value = col_name))
            col= self._browser._browser.execute_script("return {grid_value}.getColumns()".format(grid_value = col_name))
            status = True
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status


#########################################################################################################################
        # def time_zone_change(self, timezone):
        #     """
        #     
        #     `Decription:` Change timezone of system
        #     `:param` timezone: Country time zone to be change
        #     `return:`
        #     """
        #     try:
        #         status = False
        #         subprocess.call('tzutil /s "%s"'%timezone)
        #         status = True
        #     except Exception, e:
        #         print(e)
        #     return status

        # def aob_check_no_tn_number(self, msg):
        #     """
        #     
        #     `Description:`Check for if Telephone Number if available or not.
        #     Function not used as of now. but might be useful in future to check if phone number available or not
        #     `:param` timezone:
        #     `return:`
        #     """
        #     try:
        #         status = False
        #         messages=self._browser.elements_finder("aob_no_number_message")
        #         for each in messages:
        #             if each.is_displayed():
        #                 if msg==each.text:
        #                     status=True
        #     except Exception, e:
        #         print(e)
        #     return status

    def check_currency_abbreviations(self, params):
        """
            `Description:` This function will return all list of available bundles that can be added in Add User Type
                           and check the currency abbrevations on add user type page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            bundle_list=[]
            charge_list=[]
            status=False
            bundle_names=self._browser.elements_finder('add_user_type_bundles')
            for bundle in bundle_names:
                if not bundle.is_displayed():
                    right_toggles=self._browser.elements_finder('right_arrow_toggle')
                    for toggle in right_toggles:
                        if toggle.is_displayed():
                            toggle.click()
                            break
                bundle_list.append(bundle.text)
                bundle.click()
                billing_types=self._browser.elements_finder('price_formatting_add_user_type')
                for billing_type in billing_types:
                    if billing_type.text == 'One-Time Setup Charge' or billing_type.text == 'Monthly Charge':
                        charges = self._browser.elements_finder('currency_charge')
                        for charge in charges:
                            if charge.is_displayed():
                                charge_list.append(charge.text[-3:])
            if set(charge_list).issubset(params):
                status = True
        except Exception, e:
            print(e)
        return status

    def select_option_on_call_handling_summary_page(self, option):
        """
            `Description:` This function will click on selected option on call handling summary page

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            status = False
            if option.lower() == 'Operator'.lower():
                self.action_ele.click_element('operator_CH_page')
                status = True
            elif option.lower() == 'Business Hours'.lower():
                try:
                    if self._browser.element_finder("aob_ch_business_hour"):
                        print("Business Hour is Already opened")
                        pass
                except:
                    self.action_ele.click_element('Business_hours_CH_page')
                status = True
            elif option.lower() == 'Live Answer'.lower():
                self.action_ele.click_element('live_answer_CH_page')
                status = True
            elif option.lower() == 'Take a Message'.lower():
                time.sleep(1)
                self.action_ele.click_element('take_message_CH_page')
                status = True
            elif option.lower() == 'Menu Greeting'.lower():
                self.action_ele.click_element('menu_greeting_CH_page')
                status = True
        except Exception, e:
            print(e)
        return status

    def aob_check_ch_tab_open(self, option):
        """
            `Description:` This function will check if tab is open or not in ch page

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Saurabh Singh
        """
        # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            status = False
            if option.lower() == 'Operator'.lower():
                pass
            elif option.lower() == 'Business Hours'.lower():
                if "Skip this step" in self._browser._browser.page_source:
                    status = True
                elif "Reset" in self._browser._browser.page_source:
                    status = True
                if "Save" in self._browser._browser.page_source:
                    status = True
                if "Add" in self._browser._browser.page_source:
                    status = True
            elif option.lower() == 'Live Answer'.lower():
                if "Ring Users" and "Number of Rings" in self._browser._browser.page_source:
                    status = True
                if "Add" in self._browser._browser.page_source:
                    status = True
            elif option.lower() == 'Take a Message'.lower():
                if "New Voicemail" in self._browser._browser.page_source:
                    status = True
                if "You can let callers press 2 to leave a message." in self._browser._browser.page_source:
                    status = True
            elif option.lower() == 'Menu Greeting'.lower():
                if "On-Hours: System greeting" in self._browser._browser.page_source:
                    status = True
                if "On-Hours: Custom greeting" in self._browser._browser.page_source:
                    status = True
                if "Replace" in self._browser._browser.page_source:
                    status = True
        except Exception, e:
            print(e)
        return status

    def add_user_as_an_operator(self, extn):
        """
            `Description:` This function will add user as an operator on call handling summary page

            `:param` extn: Extension of the user which need to be added as operator on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar

            `Modified By:` Saurabh Singh
        """
        #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            status = False
            try:
            #self.action_ele.explicit_wait('operator_add_button')
                self.action_ele.click_element('operator_add_button')
            except:
                self.action_ele.click_element('aob_ch_choose_button')
            self.action_ele.explicit_wait('operator_extn_box')
            self.action_ele.input_text('operator_extn_box', extn)
            self.action_ele.explicit_wait('filtered_extension')
            if extn in self.query_ele.get_text('filtered_extension'):
                self.action_ele.click_element('filtered_extension')
                status = True
            elif extn in self.query_ele.get_text('filtered_username'):
                self.action_ele.click_element('filtered_username')
                status = True
        except Exception, e:
            print(e)
        return status

    def aob_get_number_from_ch_page(self):
        """
            `Description:` This function will return number from call handling page

            `:return`:  True or False

            `created by:` Saurabh Singh

        """
        #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            number = self._browser.element_finder("aob_ch_get_selected_number")
            xList = number.text.split("\n")
            number =xList[0].strip()
        except Exception, e:
            print(e)
        return number

    def aob_select_bundle_type(self,params):
        """
        Description: aob_select_bundle_type - Iterates through the bundle types available and selects the type passed. Will add an additional user if the bundle is full.
        Param1: Name of the bundle type to be selected.
        Returns: Returns True if the bundle type is present and selected.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self._browser._browser.execute_script('window.scrollTo(0, 0);')
            self.action_ele.explicit_wait("bundle_user_types")
            type = self._browser.elements_finder("bundle_user_types")
            for each in range(len(type)):
                console(len(type))
                console("Inside For, params =" + params)
                console(type[each].text)
                if type[each].is_displayed():
                    console("First If")

                    if type[each].text == params:
                        console("Second if")
                        type[each].click()

                        #Checks if bundle is full
                        users = self._browser.elements_finder("user_names")
                        create = True
                        for user in users:
                            if user.text == "New User 1":
                                 create = False
                        #Adds additional User if bundle is full
                        if self._browser.elements_finder("add_user_button") and create:
                            self.action_ele.click_element("add_user_button")
                            time.sleep(1)
                            self.action_ele.click_element("add_user_confirm_button")
                            time.sleep(1)

                        return True

        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return False

    def aob_add_user_bundle(self,params):
        """
        Description: aob_add_user_bundle - Will add a empty user to the type of bundle passed.
        Param1: Bundle types(Courtesy, Voicemail Only, Telephony, Standard, Advanced, Essentials)
                Standard Education and Essential Education cannot be added inside AOB, will throw exception
        Returns: Returns True if successful, False if not.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params == "Standard Education" or params == "Essential Education":
                raise ValueError('Standard and Essential Education bundles must be added at time of contract creation')
            self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            self.action_ele.click_element("add_user_type")
            count = 0
            while count <=2:
                type = self._browser.elements_finder("bundle_types")
                count = count+1
                for each in range(len(type)):
                    if type[each].text == params:
                        type[each].click()
                        self.action_ele.click_element("bundle_add_button")
                        return True
                self.action_ele.click_element("bundle_types_next")
                self.action_ele.click_element("bundle_types_next")


        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return False

    def add_user_confirm_button(self):
        """
        Description: add_user_confirm_button - Clicks the confirm button that pops up when you add an additional user to a bundle.
        Returns: Returns True if the confirm button is found and pressed.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        button = self._browser.elements_finder("confirm_button")
        for each in range(len(button)):
            if button[each].is_displayed():
                # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                if button[each].text == "Confirm":
                    button[each].click()
                    return True

        return True

    def aob_change_user_number(self,index):
        """
        Description: aob_change_user_number - From the Add User/Edit User screen it will selected a number from the drop-down menu.
        Param1: Index number of the drop down list. First selected index(0) would be the current user number. Index(1)... etc would select other numbers from top to bottom.
        Returns: Returns True if a number is selected. Returns the phone number selected for the user.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            buttons=self._browser.elements_finder("phone_buttons")
            console("Phone index = " + index)
            time.sleep(1)
            for each in range(len(buttons)):
                if buttons[each].is_displayed():

                    if index == "None" and buttons[each].text == "None":
                        buttons[each].click()
                        console("None Button Click")
                        time.sleep(1)
                        return True, "None"
                    elif index != "None" and buttons[each].text == "Existing":
                        console("Existing button clicked")
                        buttons[each].click()
                        drop = self._browser.elements_finder("drop_down_text")
                        for number in drop:
                            if number.is_displayed():
                                Select(number).select_by_index(index)
                                time.sleep(1)
                                console("Selected Number:" + Select(number).first_selected_option.text)
                                return True, Select(number).first_selected_option.text
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return False

    #Iterate through bundles until user name is found
    def aob_find_user_bundle_type(self,name):
        """
        Description: aob_find_user_bundle_type - Checks in all bundles until it finds the user name passed.
        Param1: User name is it appears in the bundle.
        Returns: Returns True if the user is found in a bundle. Returns the bundle name the user was present in.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:

            self._browser._browser.execute_script('window.scrollTo(0, 0);')
            type = self._browser.elements_finder("bundle_user_types")
            console("Looking for Bundle")
            for each in range(len(type)):
                console("Checking: " + type[each].text)
                type[each].click()
                if self.aob_select_user(name):
                    console("User Found")
                    status = True
                    return status, type[each].text

        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return False

    def aob_select_user(self, name):
        """
        Description: aob_select_user - Selects an AOB User in the current bundle based on the name passed.
        Param1: User name is it appears in the bundle.
        Returns: Returns True if the user present and selected.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        self._browser._browser.execute_script('window.scrollTo(0, 0);')
        user_names = self._browser.elements_finder("user_names")
        for each_name in user_names:
            if each_name.text == name:
                each_name.click()
                return True
        return False

    def aob_check_user_number(self, number):
        """
        Description: aob_check_user_number - Verifying the current users number against the number passed.
        Param1: A phone number to check against the users current number. Also accepts Select or None for users without a number selected.
        Returns: Returns True if the phone number passed matches the currently selected number for a user.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        console("Verifying number :" + number)
        self._browser._browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        drop = self._browser.elements_finder("drop_down_text")
        for each in drop:
            selected_number = Select(each).first_selected_option.text
            if number == "None" and (selected_number == "Select" or selected_number == ""):
                console("Look for:" + number + " and verified.")
                return True
            elif selected_number == number:
                console("Looked for:" + number + " and Found:" + selected_number)
                return True

        return False

    def aob_navigateto_locationactivation(self):
        """
        Description: aob_navigateto_locationactivation - Clicks the Skip or Continue button on the Add User page so the Revisit button appears
                     then clicks the Revisit button to navigate to the location activation page.
        Returns: Returns True if the Revisit button is present and selected.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            status = False
            time.sleep(2)
            if self.query_ele.get_text("welcome") == "Welcome":
                self._browser._browser.execute_script("window.scrollTo(0, 200);")
                time.sleep(1)
            btn = self._browser._browser.execute_script(
                'return document.querySelector("shor-button").shadowRoot.querySelector(".btn.btn-deepblue ")')
            if btn.text == "Start" or btn.text == "Resume":
                btn.click()
            # time.sleep(5)
            self.action_ele.explicit_wait("tansfer_img")
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if "Skip" in self._browser._browser.page_source:
                console(self.query_ele.get_text("skip_btn"))
                self.action_ele.click_element("skip_btn")
            else:
                console(self.query_ele.get_text("continue_button"))
                self.action_ele.click_element("continue_button")
                time.sleep(1)
            if "Got It" in self._browser._browser.page_source:
                self.action_ele.click_element("aob_tn_got_it_button")

            button = self._browser.elements_finder("revisit_button1")
            for each in button:

                if each.text == "Revisit":
                    console("Clicking Revisit")
                    each.click()
                    time.sleep(4)
                    return True


            return False


        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_verify_activation(self):
        """
        Description: aob_verify_activation - Verifies that the activation is set to Activate Now.
        Returns: Returns True if the Activate Now button is selected by default.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            time.sleep(2)
            if self._browser.elements_finder("activation_calendar_not_present"):
                return True
            elif self._browser.elements_finder("activation_calendar_present"):
                return False

        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return False

    def verify_bundle_user_counter(self):
        """
        Description: verify_bundle_user_counter - Verifies that the bundle users counter is present and increasing as users are created.
        Returns: Returns True is the bundle is full and False if the bundle is not full.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            counter = self._browser.elements_finder("aob_status_text_for_user_count")
            for each in counter:
                console("Counter is:" + each.text)
                users = each.text.split(" ")
                count = users[0]
                total = users[2]

            if count == total:
                self.action_ele.click_element("location_save_logout")
                result = True
            else:
                result = False

            return result


        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False


    def verify_location_checkmark(self):
        """
        Description: verify_location_checkmark - Checks if the checkmark has appeared once all users in location are completed.
        Returns: True or False based on if the was present.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            time.sleep(3)
            checkmark = self._browser.elements_finder("location_checkmark_active")
            console("Before")
            for each in range(len(checkmark)):
                if checkmark[each].is_displayed():
                    result = True

                else:
                    result = False


            return result

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def click_users_continue_button(self):
        """
        Description: click_users_continue_button - Clicks the continue button on the Add User page to close the location.
        Returns: True or False based on if the button was found and clicked.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            self.actiresulton_ele.click_element("leave_button")
            return True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def verify_welcome_checkmark(self):
        """
        Description: verify_welcome_checkmark - Checks if the checkmark on the welcome screen has appeared once all locations are completed.
        Returns: True or False based on if the was present.
        Created by: Rarlitt
        Created date: 01/31/2018
        Modified by :
        Modified date:
        """
        try:
            time.sleep(3)
            checkmark = self._browser.elements_finder("aob_checkmark_active")
            console("Before")
            for each in range(len(checkmark)):
                if checkmark[each].is_displayed():
                    result = True

                else:
                    result = False
                result = False

            return result

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False
    
    def aob_get_number_from_ch_page(self):
        """
            `Description:` This function will return number from call handling page

            `:return`:  True or False

            `created by:` Saurabh Singh

        """
        #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            number = self._browser.element_finder("aob_ch_get_selected_number")
            xList = number.text.split("\n")
            number =xList[0].strip()
        except Exception, e:
            print(e)
        return number

    def aob_saveinner_button(self):
        """
        `Description:` Click Save button - Used Java Script because of Shadow Root

        `return:` Status- True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            time.sleep(1)
            
            btn = self._browser._browser.execute_script(
                'return document.querySelector("button").shadowRoot.querySelector(".btn.btn-deepblue ")')
            self._browser._browser.execute_script("arguments[0].scrollIntoView();", btn)
            time.sleep(1)
            if btn.text == "Save":
                status = True
                btn.click()
            
            time.sleep(2)
            self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_click_close_buttons(self):
        """
        `Description:` Click Close buttons 

        `return:` Status- True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            time.sleep(1)
            buttons = self._browser.elements_finder("aob_x_close_button")
            if len(buttons) == 0:
                return True
            for each in buttons:
                if each.is_displayed():
                    each.click()
                    status = True
            
            if not status:
                self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return status
                
            time.sleep(1)
            self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status
        
    def aob_add_button(self):
        """
        `Description:` Click Add button

        `return:` Status- True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            time.sleep(1)
            buttons = self._browser.elements_finder("add_button")
            for each in buttons:
                if each.is_displayed() and each.text == "Add":
                    each.click()
                    status = True
                    break #there is only one add button
             
            time.sleep(2)
            self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_verify_add_business_hours_widgets(self, active_days_list = ["Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat"], inactive_days_list = ["Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat"]):
        """
        `Description:` Verify Business Hours components in that section
        
        `:param` active_days_list: list of days that could be already selected state
        
        `:param` inactive_days_list: list of days that could not be selected
        
        `return:` Status- True or False
        
        `created by:` Alex Medina
        """
        try:
            status = False
            time.sleep(1)
            
            days_of_week = {
                "Sun" : 0,
                "Mon" : 0,
                "Tues" : 0,
                "Wed" : 0,
                "Thur" : 0,
                "Fri" : 0,
                "Sat" : 0
            }
            
            #check unselected days
            buttons = self._browser.elements_finder("aob_add_business_hours_days_button")
            for each in buttons:
                if each.is_displayed() and each.text in days_of_week:
                    if (each.text in inactive_days_list):
                        days_of_week[each.text] += 1
            
            #check selected days
            buttons = self._browser.elements_finder("aob_add_business_hours_days_active_button")
            for each in buttons:
                if each.is_displayed() and each.text in days_of_week:
                    if (each.text in active_days_list):
                        days_of_week[each.text] += 1
            
            days_valid = True
            for day in days_of_week:
                if days_of_week[day] != 1:
                    print("Add Business Hours screen has invalid days: " + day)
                    days_valid = False
            
            #check if the labels "Start Time" and "End Time" exist
            start_labels_valid = True
            if not self.aob_verify_message_displayed("Start Time"):
                start_labels_valid = False
                print("Start Time label is missing!")
            if not self.aob_verify_message_displayed("End Time"):
                start_labels_valid = False
                print("End Time label is missing!")
            
            #check start and end time input boxes exist
            iboxes = self._browser.elements_finder("aob_add_business_hours_time_input")
            number_of_boxes = 0
            for each in iboxes:
                if each.is_displayed():
                    number_of_boxes += 1
            input_boxes_valid = number_of_boxes == 2
            if not input_boxes_valid:
                print("a time input box was not found. Found: " + str(len(buttons)))
            
            #check if save button exists
            buttons = self._browser.elements_finder("aob_save_text_primary_button")
            save_button_valid = len(buttons) == 1
            if not save_button_valid:
                print("save button was not found!")
            
            #check if cancel button exists
            buttons = self._browser.elements_finder("aob_cancel_text_default_button")
            cancel_button_valid = len(buttons) == 1
            if not cancel_button_valid:
                print("cancel button was not found!")
            
            #check if the close button exists 
            buttons = self._browser.elements_finder("aob_x_close_add_business_hours_button") #"aob_x_close_button")
            close_buttons = 0
            #there are multiple ; so check if one is visible
            for each in buttons:
                if each.is_displayed():
                    close_buttons += 1
            close_button_valid = len(buttons) == 1 or close_buttons == 1
            if not close_button_valid:
                print("close button was not found! Found: " + str(len(buttons)))
            
            status = days_valid and start_labels_valid and input_boxes_valid and save_button_valid and cancel_button_valid and close_button_valid
            
            if not status:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status
    
    def aob_add_business_hours(self, day, start_time, end_time, correct_times, validate_times = False):
        """
        `Description:` Add Random Business Hours
        
        `:param` day: day of the week (i.e. Mon, Tues, Wed, Thur, Fri, Sat or Sun)
        
        `:param` start_time: starting time
        
        `:param` end_time: ending time
        
        `:param` correct_times: to correct start_time and end_time issues

        `:param` validate_times: validate start_time and end_time
        
        `return:` Status- True or False
        
        `created by:` Alex Medina
        """
        try:
            status = False
            time.sleep(1)

            print("aob_add_business_hours(" + day + ", " + start_time.strftime("%I:%M %p") + ": " + start_time.strftime("%H:%M") + ", " + end_time.strftime("%I:%M %p") + ": " + end_time.strftime("%H:%M") + ")")
            
            if correct_times:
                if start_time > end_time:
                    temp_time = start_time
                    start_time = end_time
                    end_time = temp_time
            #validate times
            if validate_times:
                times_valid = False
                if start_time < end_time:
                    times_valid = True
                if not times_valid:
                    print("start_time or end_time is not valid ")
                    return False
            
            #the UI has to be in the Business Hours section
            setup_msg = "You can set up your call handling to behave differently during"
            if not self.aob_verify_message_displayed(setup_msg):
                print(setup_msg + " is missing!")
                return False
            
            days_of_week = {
                "Sun" : 0,
                "Mon" : 0,
                "Tues" : 0,
                "Wed" : 0,
                "Thur" : 0,
                "Fri" : 0,
                "Sat" : 0
            }
            
            #validate the day passed is correct
            if not day in days_of_week:
                print("invalid day of the week passed: " + day)
                return False
            
            #click the add business hour button if needed
            add_time_msg = "Add Business Hours Time Period"
            if not self.aob_verify_message_displayed(add_time_msg):
                add_time_button = self._browser.elements_finder("add_button_default")
                add_button_valid = len(add_time_button) == 1
                if not add_button_valid:
                    print("Add button was not found!")
                    return False
                add_time_button[0].click()
                
            #verify you are in the add business hour section
            if not self.aob_verify_message_displayed(add_time_msg):
                print(add_time_msg + " is missing!")
                return False
            
            #find the day of the week button and click it
            #revise unselected days
            day_found = False
            buttons = self._browser.elements_finder("aob_add_business_hours_days_button")
            for each in buttons:
                if each.is_displayed() and each.text == day:
                    each.click()
                    day_found = True
                    break;
            
            #revise selected days
            buttons = self._browser.elements_finder("aob_add_business_hours_days_active_button")
            for each in buttons:
                if each.is_displayed() and each.text == day:
                    day_found = True
                #unselect this day
                if each.is_displayed() and each.text != day:
                    each.click()
            
            #was the day clicked?
            if not day_found:
                print("Day clickable button was not found!")
                return False
            
            #set the start time
            start_time_field = self._browser.elements_finder("aob_ch_business_hour_start_time")
            #TODO - for some reason this is not saving AM or PM, so start time is always in AM
            start_time_field[0].send_keys(start_time.strftime("%H:%M").lower())

            #set the end time
            end_time_field = self._browser.elements_finder("aob_ch_business_hour_end_time")
            #TODO - for some reason this is not saving AM or PM, so end time is always in PM
            end_time_field[0].send_keys(end_time.strftime("%H:%M").lower())
            
            #click the save button
            save_button = self._browser.elements_finder("aob_save_text_primary_button")
            save_button_valid = len(save_button) == 1
            if not save_button_valid:
                print("save button was not found!")
                return False
            save_button[0].click()
            
            time.sleep(1)
            
            return True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        except:
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)    
        return status

    def aob_update_button(self):
        """
        `Description:` Click Update button

        `return:` Status- True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            time.sleep(1)
            buttons = self._browser.elements_finder("aob_update_button")
            for each in buttons:
                if each.is_displayed() and each.text == "Update":
                    each.click()
                    status = True
                    break #there is only one update button
            
            if status == False:
                return status
            
            time.sleep(2)
            self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_add_random_business_hours(self):
        """
        `Description:` This function will add random business hours
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            
            #days-to-int dictionary
            days = [
                'Mon', 
                'Tues', 
                'Wed', 
                'Thur', 
                'Fri', 
                'Sat', 
                'Sun' ]
            days_short_dict = {
                'Mon' : 'Mon', 
                'Tues': 'Tue', 
                'Wed' : 'Wed', 
                'Thur': 'Thu', 
                'Fri' : 'Fri', 
                'Sat' : 'Sat', 
                'Sun' : 'Sun' }
            #random number of days
            number_of_days = random.randint(1, 7)
            random.shuffle(days)
            day_count = 0
            time_periods = {} #format: Mon  3:00 PM - 5:00 PM
            for day in days:
                day_count += 1
                if (day_count-1) >= number_of_days:
                    break
                
                #for now only use start_time < noon
                start_time = self.aob_generate_random_time(1, 11)
                
                duration_hrs = random.randint(1, 11)
                duration_mins = random.randint(1, 59)
                #for now only use end_time >= noon since aob_add_business_hours is not saving AM or PM
                extra_hr = 0
                if duration_mins + int(start_time.strftime("%M")) > 59:
                    extra_hr = 1
                if duration_hrs + extra_hr + int(start_time.strftime("%I")) < 12:
                        duration_hrs = 11
                
                delta_time = datetime.timedelta(hours=duration_hrs, minutes=duration_mins)
                end_time = (datetime.datetime.combine(datetime.date(1,1,1),start_time) + delta_time).time()
                cur_time_period = day
                #TODO aob_add_business_hours is not saving AM or PM, so start is in AM and end time in PM
                if start_time < end_time:
                    time_periods[day] = start_time.strftime("%I:%M %p") + " - " + end_time.strftime("%I:%M %p")
                else:
                    time_periods[day] = end_time.strftime("%I:%M %p") + " - " + start_time.strftime("%I:%M %p")
                
                add_period_status = self.aob_add_business_hours(day, start_time, end_time, True)
                time.sleep(1)
            
            #check if the time periods were entered
            periods_valid = True
            for period in time_periods:
                #TODO - don't use days_short_dict if standard days abbreviations are used everywhere
                period_formatted = days_short_dict[period]
                day_status = self.aob_verify_message_displayed(period_formatted, 1, 1000)
                time_period_formatted = time_periods[period]
                for x in range(1, 10):
                    time_period_formatted = time_period_formatted.replace("0" + str(x) + ":", str(x) + ":")
                
                period_status = self.aob_verify_message_displayed(time_period_formatted, 1, 10)
                if not day_status:
                    periods_valid = False
                if not period_status:
                    periods_valid = False
                if not day_status or not period_status:
                    print("time period not found after creation: " + period_formatted + " " + time_period_formatted)
            if not periods_valid:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return False
            
            set_business_hours_msg = "You haven't added any time periods yet"
            business_hours_not_set = self.aob_verify_message_displayed(set_business_hours_msg)
            if not business_hours_not_set:
                status = True
            
            return status
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error Found on page, Test Case Failed!!")
        except:
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error Found on page, Test Case Failed!!")
        return status

    def aob_add_multiple_business_hours(self, min_days = 2, max_days = 7):
        """
        `Description:` This function will add multiple business hours
        `return:` True or False
        `created by:` Alex Medina
        """
        try:
            status = False
            
            if min_days < 1 or max_days > 7:
                print("aob_add_multiple_business_hours invalid input - It only supports min_days = 2 and max_days = 7")
                return False
            
            #days-to-int dictionary
            days = [
                'Mon', 
                'Tues', 
                'Wed', 
                'Thur', 
                'Fri', 
                'Sat', 
                'Sun' ]
            days_short_dict = {
                'Mon' : 'Mon', 
                'Tues': 'Tue', 
                'Wed' : 'Wed', 
                'Thur': 'Thu', 
                'Fri' : 'Fri', 
                'Sat' : 'Sat', 
                'Sun' : 'Sun' }
            #random number of days
            number_of_days = random.randint(min_days, max_days)
            random.shuffle(days)
            day_count = 0
            time_periods = {} #format: Mon  3:00 PM - 5:00 PM
            start_time_periods = {
                1: "1:01",
                2: "2:02",
                3: "3:03",
                4: "4:04",
                5: "5:05",
                6: "6:06",
                7: "7:07"
            }
            end_time_periods = {
                1: "18:01",
                2: "12:02",
                3: "13:03",
                4: "14:04",
                5: "15:05",
                6: "16:06",
                7: "17:07"
            }
            
            for day in days:
                day_count += 1
                if (day_count-1) >= number_of_days:
                    break
                
                start_time = datetime.datetime.strptime(start_time_periods[day_count], "%H:%M").time()
                end_time = datetime.datetime.strptime(end_time_periods[day_count], "%H:%M").time()
                
                time_periods[day] = start_time.strftime("%I:%M %p") + " - " + end_time.strftime("%I:%M %p")
                
                add_period_status = self.aob_add_business_hours(day, start_time, end_time, True)
                time.sleep(1)
            
            #check if the time periods were entered
            periods_valid = True
            for period in time_periods:
                #TODO - don't use days_short_dict if standard days abbreviations are used everywhere
                period_formatted = days_short_dict[period]
                day_status = self.aob_verify_message_displayed(period_formatted, 1, 1000)
                time_period_formatted = time_periods[period]
                for x in range(1, 10):
                    time_period_formatted = time_period_formatted.replace("0" + str(x) + ":", str(x) + ":")
                
                period_status = self.aob_verify_message_displayed(time_period_formatted, 1, 10)
                if not day_status:
                    periods_valid = False
                if not period_status:
                    periods_valid = False
                if not day_status or not period_status:
                    print("time period not found after creation: " + period_formatted + " " + time_period_formatted)
            if not periods_valid:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return False
            
            set_business_hours_msg = "You haven't added any time periods yet"
            business_hours_not_set = self.aob_verify_message_displayed(set_business_hours_msg)
            if not business_hours_not_set:
                status = True
            
            return status
        except Exception, e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error Found on page, Test Case Failed!!")
        except:
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error Found on page, Test Case Failed!!")
        return status

    def aob_get_elements_count(self, param):
        """
        `Description:` This function will get the number of matches of element param
        `return:` integer count
        
        `created by:` Alex Medina
        """
        try:
            buttons = self._browser.elements_finder(param)
            return len(buttons)
        except Exception, e:
            print e
            raise AssertionError("Error Found on page, Test Case Failed!!")
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
    
    def aob_verify_business_hours_count_matches(self, param):
        """
        `Description:` This function will remove the business hours
        `return:` True or False
        
        `created by:` Alex Medina
        """
        try:
            status = False
            buttons = self._browser.elements_finder("aob_x_close_button")
            if len(buttons) == param:
                status = True
            if not status:
                print("found " + str(len(buttons)) + " matches of aob_x_close_button, instead of " + str(param))
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            
            return status
        except Exception, e:
            print e
            raise AssertionError("Error Found on page, Test Case Failed!!")
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
    
    def aob_remove_business_hours(self):
        """
        `Description:` This function will remove the business hours
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            business_hours_count = 0
            buttons = self._browser.elements_finder("aob_x_close_button")
            for each in buttons:
                if each.is_displayed():
                    business_hours_count += 1
            
            set_business_hours_msg = "You haven't added any time periods yet"
            all_business_hours_msg = "At all times"
            #this could be call before the save button is clicked
            if business_hours_count == 0:
                business_hours_not_set = self.aob_verify_message_displayed(all_business_hours_msg)
                if business_hours_not_set:
                    return business_hours_not_set
                else:
                    business_hours_not_set = self.aob_verify_message_displayed(set_business_hours_msg)
                    if business_hours_not_set:
                        return business_hours_not_set
            
            business_hours_removed = self.aob_click_close_buttons()
            if not business_hours_removed:
                print("aob_click_close_buttons failed")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return False
            
            business_hours_not_set = self.aob_verify_message_displayed(set_business_hours_msg)
            if business_hours_not_set:
                business_hours_not_set = self.aob_click_element("aob_save_text_deepblue_button", 3)
                #check if UI disallows saving with no business hours
                #NOTE: this behavior may change
                #TODO: remove the next lines IF we allow users to save without time periods
                warning_msg = "Atleast one time period is required"
                business_hours_not_set = self.aob_verify_message_displayed(warning_msg)
            if not business_hours_not_set:
                print("This message was not found after removing all the time periods: " + set_business_hours_msg)
            
            return business_hours_not_set
        except Exception, e:
            print e
            raise AssertionError("Error Found on page, Test Case Failed!!")
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_unselect_add_business_hours(self):
        """
        `Description:` This function will unselect the days in the add business hours section
        `return:` True or False
        `created by:` Alex Medina
        """
        try:
            status = True
            days_of_week = {
                "Sun" : 0,
                "Mon" : 0,
                "Tues" : 0,
                "Wed" : 0,
                "Thur" : 0,
                "Fri" : 0,
                "Sat" : 0
            }
            
            #check selected days
            buttons = self._browser.elements_finder("aob_add_business_hours_days_active_button")
            for each in buttons:
                if each.is_displayed() and each.text in days_of_week:
                    each.click()

            #check unselected days
            buttons = self._browser.elements_finder("aob_add_business_hours_days_button")
            for each in buttons:
                if each.is_displayed() and each.text in days_of_week:
                    days_of_week[each.text] += 1
            
            #validate days of the week buttons are indeed unselected
            for day in days_of_week:
                if days_of_week[day] != 1:
                    status = False
            
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_verify_message_displayed(self, error_message, min_number_of_occurrences=1, max_number_of_occurrences=1):
        """
        `Description:` verify the given error message is present on the screen

        `:param` error_message: Error Message
        `:param` min_number_of_occurrences: Minimum number of occurrences
        `:param` max_number_of_occurrences: Maximum number of occurrences
        
        `return:` Status- True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            error_message = error_message.replace('"', "")
            number_of_matches = self._browser._browser.page_source.count(error_message)
            if min_number_of_occurrences <= number_of_matches <= max_number_of_occurrences:
                status = True
            print(error_message + " : Matches found: " + str(number_of_matches))
            
            if not status:
                self._browser._browser.execute_script('window.scrollTo(document.body.scrollHeight,0);')
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            
            return status
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def aob_create_voicemail_only_user(self, params):
        """
        `Description:` To add voicemail only user in aob call handling page under take a message tab

        `:param` params: firstname, lastname, email and extention

        `:return`:  True or False

        `created by:` Immani Mahesh Kumar
        """
        try:
            params = defaultdict(lambda: '', params)
            status = self.aob_create_user(params)
            time.sleep(1)
            self.action_ele.click_element('voicemail_only_save_button')
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_check_box_is_checked(self,checkbox):
        """
            `Description:` Check whether the check box is selected or not

            `:param` checkbox: checkbox map entry

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:
            status = False
            if self._browser.element_finder(checkbox).is_selected():
                status = True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_select_number_on_transfer_page(self, transfer_num):
        """
           `Description:` This method will select a number on transfer request page

           `:param` transfer_num: Transfer number on which we have to select

           `:return`:  True or False

           `created by:` Immani Mahesh Kumar
        """
        try:
            status = False
            nums=self._browser.elements_finder('Transfer_num_entry')
            for num in nums:
                ph_num = num.text
                ph_num = ''.join(e for e in ph_num if e.isalnum())
                if ph_num == transfer_num:
                    num.click()
                    status = True
                    break
            else:
                print('Transfer number not found')
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def switch_back_to_boss_page_from_aob(self):
        """
          `Description:` This method will toggle to BOSS portal again from AOB

          `:return`:  True or False

          `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = False
            aob_window = self._browser._browser.current_window_handle
            time.sleep(1)
            windows_handles = self._browser._browser.window_handles
            self._browser._browser.switch_to.window(windows_handles[0])
            boss_window = self._browser._browser.current_window_handle
            if boss_window:
                status = True
            else:
                print("Switching back to BOSS page failed")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def aob_direct_login(self, username, password):
        """
           `Description:` This method will help to login to AOB page directly

           `:params:` AOB login details(AOB URL, Username and password)

           `:return`:  True or False

           `created by:` Immani Mahesh Kumar
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            username_textbox = self.query_ele.get_value_execute_javascript(
                'document.querySelector("shor-textfield#username").shadowRoot.querySelector(".form-control ")')
            username_textbox.send_keys(username)
            password_textbox = self.query_ele.get_value_execute_javascript(
                'document.querySelector("shor-textfield#password").shadowRoot.querySelector(".form-control ")')
            password_textbox.send_keys(password)
            btns = self.query_ele.get_value_execute_javascript(
                'document.querySelectorAll("shor-button")')
            for each_btn in range(len(btns)):
                if btns[each_btn].is_displayed():
                    text1 = self.query_ele.get_value_execute_javascript(
                        'document.querySelectorAll("shor-button")[{each_btn}].shadowRoot.querySelectorAll("'
                        '.btn.btn-deepblue")'.format(each_btn=each_btn))
                    if text1[0].text == 'Sign in':
                        text1[0].click()
                        break

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_all_options_in_dropdown(self, option_list):
        """
            `Description:` This keyword will take list and dropdown and verify all the options in a dropdown

           `:dropdown` : map entry of the dropdown

           `:option_list` : list of options to be verified in a list

           `:return`:  True or False

           `created by:` Immani Mahesh Kumar
        """
        try:
            status=False
            elements = self._browser.elements_finder("aob_current_provider")
            dropdown = self._browser.elements_finder("aob_cp_drop_down_box")
            dropdown_list=[]
            for each in dropdown:
                if each.is_displayed():
                    for each1 in elements:
                        entry=re.sub(' +',' ',each1.text)
                        dropdown_list.append(entry.strip())
            final_dropdown=list(set(dropdown_list))
            final_dropdown.sort()
            option_list.sort()
            common=list(set(final_dropdown).intersection(set(option_list)))
            if len(common)==len(option_list):
                status=True
            else:
                status=False

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status

    def verify_country_dropdown(self):
        """
        `Description:` This function will verify country dropdown for multi-country contract in transfer number page

        `:return`:  True or False

        `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = False
            country_exp=[]
            country_actual = ['Canada', 'United States', 'Australia']
            country_dropdown=self._browser.elements_finder("transfer_num_country_dropdown")
            for i in range(len(country_dropdown)):
                if country_dropdown[i].is_displayed():
                    break
            if country_dropdown[i]:
                transfer_num_country_dropdown=self._browser.elements_finder("transfer_num_country_dropdown")
                for each1 in transfer_num_country_dropdown:
                    if each1.is_displayed():
                        each1.click()
                        break
                country_id = self._browser.elements_finder("country_name")
                for country in country_id:
                    if country.is_displayed():
                        country_list = country.find_elements_by_tag_name('li')
                        for each in country_list:
                            country_exp.append(each.text)
            if set(country_exp).issubset(set(country_actual)):
                status = True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_button_is_present(self,button):
        """
            `Description:` This function will verify the button is present on screen or not (which is inside shadow root)

           `:return`:  True or False

           `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = False
            if button.replace(' ','').lower() == 'logout':
                logout_button = self._browser._browser.execute_script(
                    'return document.querySelector("shor-button[type=\'logout\']").shadowRoot.querySelector('
                    '".btn.btn-logout")')
                if logout_button:
                    status = True

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status









