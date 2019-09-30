"""Module for actions on the Phone Users page"""

import os
import sys
import time
import datetime
from distutils.util import strtobool
from collections import defaultdict

#For console logs while executing ROBOT scripts
from robot.api.logger import console

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

#import base
import web_wrappers.selenium_wrappers as base
import log

class PhoneUsers(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def select_call_routing_for_user(self, user_email):
        """
        `Description:` Look for the user whose email address is provided, then click
                        on the Service/Phone Name column. Then select the
                        Call Routing tab.

        `:param params:` Email address of user.

        created by: V Milutinovic
        """
        try:
            self.action_ele.click_element("Phone_system_tab")
            self.action_ele.click_element("Users_link")

            canvasid = "au_datagrid_usersDataGrid"
            searchcolumnid = "headerRow_BusinessEmail"

            self.action_ele.explicit_wait(searchcolumnid)
            self.action_ele.input_text(searchcolumnid, user_email)
            self.action_ele.explicit_wait(canvasid)
            grid_table_row = self._browser.element_finder(canvasid)
            if grid_table_row:
                print grid_table_row

                # It is essential to wait for the element to load, even though we were waiting for the grid to load.
                self.action_ele.explicit_wait("MatchingServicePhoneName")
                elms = self._browser.elements_finder("MatchingServicePhoneName")
                elms[0].click()

                self.action_ele.explicit_wait("CallRouting_tab")
                self.action_ele.click_element("CallRouting_tab")

                # Make sure we are starting with default options for call routing.
                self.set_default_options_for_call_routing()
                return True

        except:
            raise AssertionError("Navigation Failed!!")

    def click_on_configure_main_settings(self):
        """
        `Description:` Click on Configure Main Settings

        `:param params:`

        created by: V Milutinovic
        """
        try:
            self.action_ele.explicit_wait("configureMainSettingsButtonId")

            matching_xpath = "configureMainSettingsButton"
            matching_buttons = self._browser.elements_finder(matching_xpath)
            if matching_buttons:
                print matching_buttons

                search_item = "Configure Main Settings"
                for button in matching_buttons:
                    name_list = button.text
                    if search_item == name_list:
                        time.sleep(1)
                        button.click()
                        return True
            return False

        except:
            raise AssertionError("Navigation Failed!!")

    def click_on_configure_phones_add(self):
        """
        `Description:` Click on Configure Phones -> Add

        `:param params:`

        created by: V Milutinovic
        """
        try:
            self.action_ele.explicit_wait("callRoutingAddNumbersHeader")

            matching_xpath = "configureMainSettingsButton"
            matching_buttons = self._browser.elements_finder(matching_xpath)
            if matching_buttons:
                print matching_buttons

                search_item = "Add"
                for button in matching_buttons:
                    name_list = button.text
                    if search_item == name_list:
                        time.sleep(1)
                        button.click()
                        return True
            return False

        except:
            raise AssertionError("Navigation Failed!!")

    def add_phone_for_call_routing(self, phone_number):
        """
        `Description:` Add a phone to call routing.

        `:param params:`

        created by: V Milutinovic
        """
        try:
            self.action_ele.explicit_wait("tblCallRoutingNumbers")
            self.action_ele.input_text("configurePhoneCallRoutingAddLabel", phone_number)
            self.action_ele.input_text("configurePhoneCallRoutingAddPhoneNumber", phone_number)

            # Click on "Press 1 to connect"
            self.action_ele.click_element('configurePhoneCallRoutingPressOne')

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')
            return True

        except:
            raise AssertionError("Navigation Failed!!")

    def add_second_phone_for_call_routing(self, phone_number):
        """
        `Description:` Add second phone to call routing.

        `:param params:` phone number

        created by: V Milutinovic
        """
        try:
            self.action_ele.explicit_wait("tblCallRoutingNumbers")
            self.action_ele.input_text("configurePhoneCallRoutingAddLabel2", phone_number)
            self.action_ele.input_text("configurePhoneCallRoutingAddPhoneNumber2", phone_number)

            # Click on "Press 1 to connect"
            self.action_ele.click_element('configurePhoneCallRoutingPressOne2')

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')
            return True

        except:
            raise AssertionError("Navigation Failed!!")

    def add_phone_to_call_routing(self, phone_number, phone_index):
        """
        `Description:` Adds a phone to Call Routing.

        `:param params:` phone number and index

        created by: V Milutinovic
        """
        try:
            result = self.click_on_configure_main_settings()
            if not result:
                return result

            result = self.click_on_configure_phones_add()
            if not result:
                return result

            if phone_index == "first":
                result = self.add_phone_for_call_routing(phone_number)
            else:
                result = self.add_second_phone_for_call_routing(phone_number)
            if not result:
                return result

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def configure_call_routing_options(self):
        """
        `Description:` Add phones to Call Routing.
        They have to be added one at the time, otherwise it would fail even when adding them manually. It seems like a bug in BOSS.
        It would be nice to create new users first and then add their phone numbers, rather than hard-coding extension numbers.

        `:param params:`

        created by: V Milutinovic
        """
        try:
            result = self.add_phone_to_call_routing("4001", "first")
            if not result:
                return result

            time.sleep(3)
            result = self.add_phone_to_call_routing("4002", "second")
            if not result:
                return result

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def find_and_click_matching_element(self, xpath, search_item):
        """
        `Description:` Looks for an element that matches xpath and text, and clicks on it if it finds it.

        `:param params:` xpath and text that need to match.

        created by: V Milutinovic
        """
        try:
            matching_buttons = self._browser.elements_finder(xpath)
            if matching_buttons:
                print matching_buttons

                for button in matching_buttons:
                    name_list = button.text
                    if search_item == name_list:
                        time.sleep(1)
                        button.click()
                        return True
            return False
        except:
            raise AssertionError("Failed to find matching element!!")

    def configure_always_forward_to_voicemail(self):
        """
        `Description: This function assumes that the Call Routing menu has been entered so make sure
        you have called the keyword "I open Call Routing for user" before calling this function`

        `:param None:

        created by: vuh
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("configureMainSettingsButtonId")
            self.action_ele.click_element('changeVoicemail')

            # Click on "Always forward my calls to" radio button
            element = self._browser.element_finder("alwaysForwardRadio")
            if element:
                element.click()
            else:
                return False

            # Select forwarding option
            self.action_ele.select_from_dropdown_using_text('alwaysForwardOptions', "voicemail")

            # click on Finish
            self.action_ele.click_element('availabilityRoutingWizard_finish')

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def always_forward_to_voicemail_configured(self):
        """
        `Description:` Check to see if always forward to voicemail has been configured

        `:param None:

        created by: vuh
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("availabilityRouting-content")
            time.sleep(3)
            self.action_ele.click_element('changeVoicemail')

            # Check if "Forward the call to" radio button is checked
            self.action_ele.explicit_wait("alwaysForwardRadio")
            element = self._browser.element_finder("alwaysForwardRadio")
            if element and not element.is_selected():
                console("Always forward was not selected")
                return False

            # Check voicemail option
            element = self._browser.element_finder("alwaysForwardOptions")
            if element and element.get_attribute('value') != "0": # voicemail value
                return False

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def configure_call_forwarding(self, default_values=False):
        """
        `Description:` Configure parameters in Find Me -> Call Forwarding.

        `:param params:

        created by: V Milutinovic
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("configureMainSettingsButtonId")
            self.action_ele.click_element('changeFindMe')

            # Click on Call Forwarding button
            self.action_ele.explicit_wait("availabilityRoutingWizard")
            result = self.find_and_click_matching_element("callRoutingButtons", "Call Forwarding")
            if not result:
                return result

            # Click on "Forward the call to" radio button
            element = self._browser.element_finder("forwardTheCallTo")
            if element:
                element.click()
            else:
                return False

            # Select voicemail option
            self.action_ele.select_from_dropdown_using_text('forwardTheCallToOptions', "voicemail")
            # select number of rings
            if default_values:
                self.action_ele.select_from_dropdown_using_text('ringsBeforeForwarding', "3")
            else:
                self.action_ele.select_from_dropdown_using_text('ringsBeforeForwarding', "5")
            # and if more than 8 calls forward to
            self.action_ele.select_from_dropdown_using_text('ifMoreThan8CallsForwardTo', "voicemail")

            # click on Finish
            self.action_ele.click_element('availabilityRoutingWizard_finish')

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def call_forwarding_configured(self):
        """
        `Description:` Verify call forwarding parameters are configured as expected.

        `:param params:

        created by: V Milutinovic
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("availabilityRouting-content")
            time.sleep(3)
            self.action_ele.click_element('changeFindMe')

            # Click on Call Forwarding button
            self.action_ele.explicit_wait("availabilityRoutingWizard")
            result = self.find_and_click_matching_element("callRoutingButtons", "Call Forwarding")
            if not result:
                console("failed to click on Call Forwarding option")
                return result

            # Check if "Forward the call to" radio button is checked
            self.action_ele.explicit_wait("forwardTheCallTo")
            element = self._browser.element_finder("forwardTheCallTo")
            if element and not element.is_selected():
                console("failed to click on Call Forwarding option")
                return False

            # Check voicemail option
            element = self._browser.element_finder("forwardTheCallToOptions")
            if element and element.get_attribute('value') != "0": # voicemail value
                return False

            # Check number of rings
            element = self._browser.element_finder("ringsBeforeForwarding")
            if element and element.get_attribute('value') != "4":
                return False

            # and if more than 8 calls forward to
            element = self._browser.element_finder("ifMoreThan8CallsForwardTo")
            if element and element.get_attribute('value') != "0": # voicemail value
                return False

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def configure_find_me_numbers(self, default_values=False):
        """
        `Description:` Configure Find Me numbers that will be used sequentially.

        `:param params:` Apply default values, if specified.

        created by: V Milutinovic
        """
        try:
            time.sleep(3)
            result = self.click_on_configure_main_settings()
            if not result:
                return result

            # Click on Next button
            nextButtonId = "callRoutingSettingsWizard_next"
            self.action_ele.explicit_wait(nextButtonId)
            self.action_ele.click_element(nextButtonId)
            time.sleep(1)

            # Click on next again in new window
            self.action_ele.explicit_wait(nextButtonId)
            self.action_ele.click_element(nextButtonId)
            time.sleep(1)

            # click on "Ring my Find Me numbers sequentially before playing my voicemail"
            elms = self._browser.elements_finder("cosmoCallRoutingFindMeContainer")
            # if elms and elms[1]:
            #     self.action_ele.explicit_wait("cosmoCallRoutingFindMeContainer")
            result = self.find_and_click_matching_element("ringMyFindMeNumbers", "Ring my Find Me numbers sequentially before playing my voicemail")
            if not result:
                return result

            # click on "Prompt the caller to record their name if caller ID is not available"
            self.action_ele.select_checkbox("promptCallerToRecordName")

            # Enter My Find Me numbers
            if default_values:
                self.action_ele.select_from_dropdown_using_text('myFindMeNumber1', "Select Number")
                self.action_ele.select_from_dropdown_using_text('myFindMeNumber2', "Select Number")
            else:
                self.action_ele.select_from_dropdown_using_text('myFindMeNumber1', "4001 - Press 1 to connect - Try for 3 rings")
                self.action_ele.select_from_dropdown_using_text('myFindMeNumber2', "4002 - Press 1 to connect - Try for 3 rings")

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')

            time.sleep(3)
            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def select_call_routing_for_filtered_user(self, user_email):
        """
        `Description:` Click on Call Routing tab for a selected user.

        `:param params:` Email address of user

        created by: V Milutinovic
        """
        try:
            self.action_ele.click_element("Phone_system_tab")
            self.action_ele.click_element("Users_link")

            canvasid = "au_datagrid_usersDataGrid"
            searchcolumnid = "headerRow_BusinessEmail"

            self.action_ele.explicit_wait(searchcolumnid)
            self.action_ele.input_text(searchcolumnid, user_email)
            self.action_ele.explicit_wait(canvasid)
            grid_table_row = self._browser.element_finder(canvasid)
            if grid_table_row:
                print grid_table_row

                self.action_ele.explicit_wait("SelectedMatchingServicePhoneName")
                elms = self._browser.elements_finder("SelectedMatchingServicePhoneName")
                elms[0].click()

                self.action_ele.explicit_wait("CallRouting_tab")
                self.action_ele.click_element("CallRouting_tab")
                return True

        except:
            raise AssertionError("Navigation Failed!!")

    def find_me_numbers_configured(self):
        """
        `Description:` To verify Find Me Numbers are configured

        `:param params:

        created by: V Milutinovic
        """
        try:
            # The changes are not refreshed in the form after changing routing settings.
            # Need to open call routing for the user again by walking through few menus to refresh content.
            self.select_call_routing_for_filtered_user("auser1@shoretel.com")
            self.click_on_configure_main_settings()

            self.action_ele.explicit_wait("availabilityRouting-content")
            time.sleep(3)

            # Check if "Forward the call to" radio button is checked
            self.action_ele.explicit_wait("findMeNumbersSettings")
            element = self._browser.element_finder("findMeNumbersSettings")
            if element:
                console("element" + element.text)

            text = element.text
            do_not_pick_up = "pick up, ring these numbers sequentially"
            if do_not_pick_up not in element.text:
                return False
            if "4001" not in element.text:
                return False
            if "4002" not in element.text:
                return False

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def select_prog_buttons_for_user(self, user_email):
        """
        `Description:` Look for the user whose email address is provided, then click
                        on the Service/Phone Name column. Then select the
                        Prog Buttons tab.

        `:param params:` Email address of user

        created by: V Milutinovic
        """
        try:
            self.action_ele.click_element("Phone_system_tab")
            self.action_ele.click_element("Users_link")

            canvasid = "au_datagrid_usersDataGrid"
            searchcolumnid = "headerRow_BusinessEmail"

            self.action_ele.explicit_wait(searchcolumnid)
            self.action_ele.input_text(searchcolumnid, user_email)
            self.action_ele.explicit_wait(canvasid)
            grid_table_row = self._browser.element_finder(canvasid)
            if grid_table_row:
                print grid_table_row

                # Wait for the element to load, even though we were waiting for the grid to load.
                self.action_ele.explicit_wait("MatchingServicePhoneName")
                elms = self._browser.elements_finder("MatchingServicePhoneName")
                elms[0].click()

                self.action_ele.explicit_wait("progButtonsTab")
                self.action_ele.click_element("progButtonsTab")
                return True

        except:
            raise AssertionError("Navigation Failed!!")

    def set_default_options_for_call_routing(self):
        """
        `Description:` This routine will make sure the default options are set for Call Routing
        before proceeding with the new configuration.

        `:param params:` none

        created by: V Milutinovic
        """
        try:
            # First set the default options in Call Forwarding
            self.configure_find_me_numbers(True)

            # Clear Find Me numbers.
            self.configure_call_forwarding(True)

            # Clear Configure Phones numbers
            self.clear_call_routing_configured_phones()
        except:
            raise AssertionError("Failed to set default values for Call Routing!!")

    def clear_call_routing_configured_phones(self):
        """
        `Description:` Clear the phones assigned in Call Routing, if there are any.

        `:param params:` none

        created by: V Milutinovic
        """
        try:
            time.sleep(3)
            result = self.click_on_configure_main_settings()
            if not result:
                return result

            elms2 = self._browser.elements_finder("deleteCallRoutingPhoneLink2")
            if elms2 and elms2[0]:
                elms2[0].click()

            elms1 = self._browser.elements_finder("deleteCallRoutingPhoneLink1")
            if elms1 and elms1[0]:
                elms1[0].click()

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')
            time.sleep(2)
            return True
        except:
            raise AssertionError("Failed to clear phones configured for Call Routing!!")

    def verify_phone_settings_sip_password(self, user_email):
        """
        `Description:` Look for the user whose email address is provided, then click
        on the Service/Phone Name column. Then select the Phone tab.
        `params:` Email address of user.
        Created by: Shilpa K N
        """

        try:
            canvasid = "au_datagrid_usersDataGrid"
            searchcolumnid = "headerRow_BusinessEmail"

            self.action_ele.explicit_wait(searchcolumnid)
            self.action_ele.input_text(searchcolumnid, user_email)

            self.action_ele.explicit_wait(canvasid)
            grid_table_row = self._browser.element_finder(canvasid)

            if grid_table_row:
                print grid_table_row  # It is essential to wait for the element to load, even though we were waiting for the grid to load.

            self.action_ele.explicit_wait("MatchingServicePhoneName")
            elms = self._browser.elements_finder("MatchingServicePhoneName")
            elms[0].click()

            stationLabelId = "Phone_tab_Station_Label"
            self.action_ele.explicit_wait(stationLabelId, 30)
            isSipPasswordPresent = self.assert_ele._is_text_present("Sip Password")
            if isSipPasswordPresent:
                return False
            else:
                return True

        except:
            raise AssertionError("Failed navigating to Phone Settings page of the user.")


    def configure_availablity_Settings(self, available_state="Available", Call_routing_condition="CallForwarding", Call_forward_condition="CallForwardAnotherNumber", PhNumber="5501", noofrings="5"):
        """
        `Description:` Configure call routing parameters.

        `:param params:available State, Call routing condition, Call Forward condition, Phone number , No of rings.

        created by: Maha
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.select_from_dropdown_using_text('CallRoutingTab_Availability', available_state)
            # Click on Find Me change button
            if Call_routing_condition== "SimultaneousRing":
                #self.action_ele.click_element('changeFindMe')
                # click on Finish
                self.action_ele.click_element('availabilityRoutingWizard_finish')

            elif Call_routing_condition== "CallForwarding":
                time.sleep(1)
                self.action_ele.click_element('changeVoicemail')


                if Call_forward_condition=="Keepringing":
                    # Click on "Forward the call to" radio button
                    element = self._browser.element_finder("KeepRinging")
                    if element:
                        element.click()
                    else:
                        return False

                    self.action_ele.click_element('availabilityRoutingWizard_finish')

                elif Call_forward_condition=="CallForwardVoicemail":
                    # Click on "Forward the call to" radio button
                    element = self._browser.element_finder("forwardTheCallTo")
                    if element:
                        element.click()
                    else:
                        return False
                    # Select voicemail option
                    self.action_ele.select_from_dropdown_using_text('forwardTheCallToOptions', "voicemail")
                    # select number of rings
                    self.action_ele.select_from_dropdown_using_text('ringsBeforeForwarding', noofrings)
                    time.sleep(1)
                    # and if more than 8 calls forward to
                    self.action_ele.select_from_dropdown_using_text('ifMoreThan8CallsForwardTo', "voicemail")
                    # click on Finish
                    self.action_ele.click_element('availabilityRoutingWizard_finish')

                elif Call_forward_condition=="CallForwardAnotherNumber":
                    # Click on "Forward the call to" radio button
                    element = self._browser.element_finder("forwardTheCallTo")
                    if element:
                        element.click()
                    else:
                        return False
                    # Select voicemail option
                    self.action_ele.select_from_dropdown_using_text('forwardTheCallToOptions', "another number")
                    time.sleep(1)
                    self.action_ele.input_text('ForwardcallinputNumber',PhNumber)
                    time.sleep(2)
                    # select number of rings
                    self.action_ele.select_from_dropdown_using_text('ringsBeforeForwarding', noofrings)
                    time.sleep(1)
                    # and if more than 8 calls forward to
                    self.action_ele.select_from_dropdown_using_text('ifMoreThan8CallsForwardTo', "voicemail")
                    # click on Finish
                    self.action_ele.click_element('availabilityRoutingWizard_finish')

                elif Call_forward_condition=="AlwaysForwardVoicemail":
                    # Click on "Forward the call to" radio button
                    element = self._browser.element_finder("AlwaysforwatdTo")
                    if element:
                        element.click()
                    else:
                        return False

                    self.action_ele.select_from_dropdown_using_text('AlwaysforwatdToOptions', "voicemail")
                    self.action_ele.click_element('availabilityRoutingWizard_finish')

                elif Call_forward_condition=="AlwaysForwarAnotherNumber":
                    # Click on "Forward the call to" radio button
                    element = self._browser.element_finder("AlwaysforwatdTo")
                    if element:
                        element.click()
                    else:
                        return False

                    self.action_ele.select_from_dropdown_using_text('AlwaysforwatdToOptions', "another number")
                    time.sleep(1)
                    self.action_ele.input_text('AlwaysforwatdinputNumber',PhNumber)
                    time.sleep(2)
                    self.action_ele.click_element('availabilityRoutingWizard_finish')

                elif Call_forward_condition == "DNDNeverForward":
                    element = self._browser.element_finder("dndneverforward")
                    if element:
                        element.click()
                    else:
                        return False
                    time.sleep(1)
                    self.action_ele.click_element('availabilityRoutingWizard_finish')

                elif Call_forward_condition == "DNDAlwaysVM":
                    self.action_ele.explicit_wait("dndalwaysvm")
                    time.sleep(1)
                    self.action_ele.click_element('dndalwaysvm')

                    self.action_ele.click_element('availabilityRoutingWizard_finish')
                else:
                    log("Please give the proper Call Forward Option")

            elif Call_routing_condition== "Findme":
                #self.action_ele.click_element('changeFindMe')
                # click on Finish
                self.action_ele.click_element('availabilityRoutingWizard_finish')

            elif Call_routing_condition== "VoicemailInteraction":
                #self.action_ele.click_element('changeFindMe')
                # click on Finish
                self.action_ele.click_element('availabilityRoutingWizard_finish')

            else:
                log("Please give the proper Call routing Option")

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def create_new_power_routing(self,rulename="prtest",prcondition="On_the_Phone",prforward="another_number", PhNumber="5501", deleteflag="0"):
        """
        `Description:` Create and delete the power routing

        `:param params:` Power routing Name , Pre condition , Forward rule, Phone Number, Delete flag

        created by: Maha
        """
        try:
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if deleteflag == "0":
                time.sleep(2)
                self.action_ele.explicit_wait("PowerRouting")
                self.action_ele.click_element('PowerRouting')
                self.action_ele.explicit_wait("CreateNewPowerRouting")
                self.action_ele.click_element('CreateNewPowerRouting')
                self.action_ele.explicit_wait("PowerRoutingRuleName")
                self.action_ele.input_text('PowerRoutingRuleName', rulename)

                if prcondition=="On_the_Phone":
                    self.action_ele.explicit_wait("PowerRoutingOnthePhone")
                    self.action_ele.click_element('PowerRoutingOnthePhone')
                    self.action_ele.explicit_wait("PowerRoutingAddButton")
                    self.action_ele.click_element('PowerRoutingAddButton')

                    if prforward=="another_number":
                        self.action_ele.explicit_wait("PowerRoutingForwordOption")
                        self.action_ele.click_element('PowerRoutingForwordOption')
                        self.action_ele.explicit_wait("PowerRoutingForwordPhNumber")
                        self.action_ele.input_text('PowerRoutingForwordPhNumber', PhNumber)

                    elif prforward=="voicemail" :
                            self.action_ele.explicit_wait("PowerRoutingForwordOptionvm")
                            self.action_ele.click_element('PowerRoutingForwordOptionvm')
                    else:
                        log("power routing forward selection is not proper")

                    self.action_ele.explicit_wait("PowerRoutingOKbutton")
                    self.action_ele.click_element('PowerRoutingOKbutton')
                    time.sleep(2)
                    self.action_ele.click_element('PowerRoutingEnable')
                    self.action_ele.click_element('PowerRoutingSave')
                    time.sleep(2)
                    self.action_ele.click_element('AvailabilityRoutingbtn')
                else:
                    log("power routing condition selection is not proper")

            elif deleteflag == "1":
                time.sleep(2)
                #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                self.action_ele.explicit_wait("PowerRouting")
                self.action_ele.click_element('PowerRouting')
                self.action_ele.explicit_wait("PowerRoutingDeleteButton")
                self.action_ele.click_element('PowerRoutingDeleteButton')
                self.action_ele.explicit_wait("Service_Void_Yes")
                time.sleep(1)
                self.action_ele.click_element('Service_Void_Yes')
                time.sleep(2)
                self.action_ele.click_element('PowerRoutingSave')
                time.sleep(2)
                self.action_ele.click_element('AvailabilityRoutingbtn')
            else:
                log("delete flag selection is selection is not proper")

            return True
        except:
            raise AssertionError("Failed to clear phones configured for Call Routing!!")

    def select_call_routing_using_extension(self, extension):
        """
        `Description:` Look for the user whose phone extension is provided, then click
                        on the Service/Phone Name column. Then select the
                        Call Routing tab.

        `:param params:` Extension of user.

        created by: Maha
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            time.sleep(2)
            self.action_ele.explicit_wait("Phone_system_tab")
            self.action_ele.click_element("Phone_system_tab")
            self.action_ele.click_element("Users_link")
            time.sleep(2)
            self.action_ele.explicit_wait("headerRowExtensionInput")
            self.action_ele.input_text("headerRowExtensionInput", extension)
            self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
            grid_table_row = self._browser.element_finder("au_datagrid_usersDataGrid")
            if grid_table_row:
                print grid_table_row

                # It is essential to wait for the element to load, even though we were waiting for the grid to load.
                self.action_ele.explicit_wait("MatchingServicePhoneName")
                elms = self._browser.elements_finder("MatchingServicePhoneName")
                elms[0].click()

                self.action_ele.explicit_wait("CallRouting_tab")
                self.action_ele.click_element("CallRouting_tab")

                # Make sure we are starting with default options for call routing.
                #self.set_default_options_for_call_routing()
                return True
            else:
                return False
        except Exception as e:
            print e.message
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            #raise AssertionError("Navigation Failed!!")
