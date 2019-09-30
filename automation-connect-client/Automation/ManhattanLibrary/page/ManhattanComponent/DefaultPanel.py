## Module: DefaultPanel
## File name: DefaultPanel.py
## Description: Displays default UI for Manhattan Client
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 18 AUG 2014  Jahnavi-844             Initial Version
###############################################################################
# Python modules
import sys
import os
import time
import re
import datetime
import autoit

from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class DefaultPanel:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)

    def invoke_peoplelist(self):
        """
           Click on people tab on the default page 
        """
        try:
            self.webAction.click_element("default_people_tab")
            time.sleep(1)
            self.assertElement.element_should_be_displayed("peoples_group")
            log.mjLog.LogReporter("DefaultPanel", "info", "Clicked on People tab")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "Error while clicking on People tab " +str(sys.exc_info()))
            raise

    def invoke_recent_tab(self):
        """
        invoke_recent_tab() : Click on Recent button
        Parameters: No parameter
        """
        try:
            self.webAction.click_element("default_recent_tab")
            self.assertElement.element_should_be_displayed("recent_all_tab")
            log.mjLog.LogReporter("DefaultPanel", "info", "invoke_recent_tab - Clicked on Recent tab")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "invoke_recent_tab"
                                                           " - Error while clicking on Recent tab " + str(sys.exc_info()))
            raise

    def invoke_voicemails_tab(self):
        """
        Author: UKumar
        invoke_voicemails_tab(): To Click on Voicemails tab in dashboard
        Parameters: No parameter
        """
        try:
            self.webAction.explicit_wait("default_voicemail_tab")
            self.webAction.click_element("default_voicemail_tab")
            self.webAction.explicit_wait("voicemail_all_tab")
            self.assertElement.page_should_contain_element("voicemail_all_tab")
            log.mjLog.LogReporter("DefaultPanel", "info", "invoke_voicemails_tab - Clicked on Voicemails tab")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "invoke_voicemails_tab"
                                " - Error while clicking on Voicemails tab " + str(sys.exc_info()))
            raise

    def invoke_messages_tab(self):
        """
        Author: UKumar
        invoke_messages_tab(): To Click on Messages tab in dashboard
        Parameters: No parameter
        """
        try:
            self.webAction.click_element("default_messages_tab")
            log.mjLog.LogReporter("DefaultPanel", "info", "invoke_messages_tab - Clicked on Messages tab")
            is_mt = BuiltIn().get_variable_value('${is_runtype_mt}')
            #If MT Installer is installed, TWD should open by clicking on messages tab
            if is_mt:
                log.mjLog.LogReporter("DefaultPanel", "info", "invoke_messages_tab - Opened TWD")
                return 1
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "invoke_messages_tab"
                                                           " - Error while clicking on Messages tab " + str(
                sys.exc_info()))

    def invoke_workgroups_tab(self):
        """
        Author: Indresh
        invoke_workgroups_tab(): To Click on workgroups tab in dashboard
        Parameters: No parameter
        """
        try:
            self.webAction.explicit_wait("default_WK_notify")
            self.webAction.click_element("default_WK_notify")
            log.mjLog.LogReporter("DefaultPanel", "info", "invoke_workgroups_tab - Clicked on workgroups tab")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "invoke_workgroups_tab"
                                                           " - Error while clicking on workgroups tab " + str(
                sys.exc_info()))

    def invoke_events_tab(self):
        '''
           Click on events tab on the default page 
        '''
        try:
            if self.queryElement.element_not_displayed("events_upcoming_tab"):
                self.webAction.click_element("default_events_tab")
                time.sleep(2)
                self.assertElement.element_should_be_displayed("events_upcoming_tab")
                self.assertElement.element_should_be_displayed("events_past_tab")
            log.mjLog.LogReporter("DefaultPanel", "info", "invoke_events_tab - Clicked on Events Tab")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "invoke_events_tab - Error while clicking the Events tab " +str(sys.exc_info()))
            raise
    
    def search_people_or_extension(self, searchItem, throwException = False):
        '''
            Enter the name or number in search bar
            check the contact exist  or not
            if exist show the details
        '''
        try:
            # if self.queryElement.element_displayed("extension_close_searching"):
            # croslist = self._browser.elements_finder("extension_close_searching")
            # if len(croslist) >=1:
                # self.webAction.click_element("extension_close_searching")
            # time.sleep(2)
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            time.sleep(2)            
            log.mjLog.LogReporter("DefaultPanel","debug","search_people_or_extension - Clicked on search button")
            self.webAction.input_text("default_search_input",searchItem)
            time.sleep(1)
            searchResultsList=self._browser.elements_finder("peoples_panel_customer_name")
            
            if len(searchResultsList)==0:
                if throwException==False:
                    return False
                else:
                    log.mjLog.LogReporter("DefaultPanel","info","search_people_or_extension - No contact found!")
                    raise AssertionError("No contact found")
            else:
                log.mjLog.LogReporter("DefaultPanel","info","search_people_or_extension - %s is available" %(searchItem))
                return searchResultsList[0]
        except:
            log.mjLog.LogReporter("DefaultPanel","error","search_people_or_extension-Error while searching people" +str(sys.exc_info()))
            raise
            
    def change_user_status(self,status, discardPopup=False):
        """
        change_user_status() - This method clicks on user status and changes user status
        """
        try:
            status = re.sub('\_',' ',status)
            count = 0
            if discardPopup and (not self.queryElement.element_not_displayed("FP_availability_alert_popup")):
                self.webAction.click_element("FP_availability_alert_popup_ok")
            self.webAction.click_element("default_user_telephony_color")
            self.webAction.explicit_wait("default_user_status_option")
            status_options = self._browser.elements_finder("default_user_status_option")
                        
            for option in status_options:
                status_check = option.text
                if status in status_check.lower():
                    option.click()
                    count = count + 1
                    break
            if count != 0:
                log.mjLog.LogReporter("DefaultPanel","info","change_user_status - User status changed to "+status_check)
            else:
                raise
        except:
            log.mjLog.LogReporter("DefaultPanel","error","change_user_status - Failed to change user status "+str(sys.exc_info()))
            raise
            
    def set_status_variable(self, customStatus, statusOption='', customMessage=''):
        """
        author:uttam
        set_status_variable() - This method enters custom message for the status
                         'Variable' and sets that status as users's presence status
        parameters: customStatus, option, customMessage
        """
        try:
            customStatus = re.sub('\_',' ',customStatus)
            customMessage = re.sub('\_', ' ', customMessage)
            
            statusList = self._browser.elements_finder("default_user_status_variableUL")
            if statusList[1].text=="Available" and statusList[2].text=="Busy" and\
             statusList[3].text=="Not Available" and statusList[4].text=="Cancel":
                for option in statusList:
                    if option.text == customStatus:
                        option.click()
                        log.mjLog.LogReporter("DefaultPanel","info","set_status_variable -"
                                              " clicked on "+customStatus)
            if customStatus != 'Cancel':
                self.assertElement.element_should_be_displayed("default_user_status_cancel")
                self.webAction.click_element("default_user_status_variableInput")
                self.webAction.input_text("default_user_status_variableInput", customMessage)
                if statusOption == "save":
                    self.webAction.press_key("default_user_status_variableInput", "ENTER")
                    log.mjLog.LogReporter("DefaultPanel","info","set_status_variable -"
                                          " custom status is set to "+customStatus)
                else:
                    self.webAction.click_element("default_user_status_cancel")
                    log.mjLog.LogReporter("DefaultPanel","info","set_status_variable -"
                                          " custom status is cancelled")
        except:
            log.mjLog.LogReporter("DefaultPanel","error","set_status_variable - "
                                  "Failed to set custom status "+str(sys.exc_info()))
            raise

    def check_user_telephony_presence(self, status, color):
        '''
           Author : Gautham
           check_user_telephony_presence() - Checks the user telephony presence (status and color) at the manhattan login
           parameter : status, color
        '''
        try:
            status = re.sub('\_', ' ', status)
            # New Changes
            '''if status=="Basic*Routing":
                status=status.replace(status,"available")  
                print("The Value of status is *********** ",status)'''
            # End of change
            for i in range(10):
                rgb = self._browser.element_finder("default_user_telephony_color").value_of_css_property("background-color")
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                item = self.queryElement._get_text("default_user_telephony_status")
                print("Print Colour ", color)
                if "#09cf94" in hex_color:
                    actual_color = "green"
                elif "#ffd500" in hex_color:
                    actual_color = "yellow"
                elif "#ff5550" in hex_color:
                    actual_color = "red"
                else:
                    actual_color = "None"
                if status in item.lower() and color == actual_color:
                    log.mjLog.LogReporter("DefaultPanel", "info",
                                          "check_user_telephony_presence - Status is " + item + " and colour is " + actual_color)
                    break
                else:
                    time.sleep(10)
                    log.mjLog.LogReporter("DefaultPanel", "info",
                                          "check_user_telephony_presence - status not changed in %s tries" % (i + 1))
            else:
                raise AssertionError("status and Color of status do not match!")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "check_user_telephony_presence - user status check failed" + str(sys.exc_info()))
            raise
            
    def get_group_name(self, groupName):
        """
        author:uttam
        get_group_name() - This method extracts group name from notification in dashboard
        parameters: groupName
        """
        try:
            groups = self._browser.elements_finder("default_draft_notify")
            desiredGroupDraftObject = ""
            draftNumber = 0
            for group in groups:
                if group.text == groupName:
                    desiredGroupDraftObject = group
                    draftNumber = draftNumber + 1
                    
            if draftNumber == 0:
                log.mjLog.LogReporter("DefaultPanel","info","get_group_name - no draft found for the draft name "+groupName)
                return "no"
            elif draftNumber == 1:
                log.mjLog.LogReporter("DefaultPanel","info","get_group_name - group name is "+desiredGroupDraftObject.text)
                return desiredGroupDraftObject
            else:
                log.mjLog.LogReporter("DefaultPanel","info","get_group_name - more than one drafts are there")
                raise AssertionError("More than one draft for same group")
            #self.name = self.queryelement.get_text("default_draft_notify_name")

        except:
            log.mjLog.LogReporter("DefaultPanel","error","get_group_name - Error"
                                  " while getting group name " +str(sys.exc_info()))
            raise
   
    def close_conversation(self,sender):
        '''
           Author : Modified by Upendra
           This API will close a particular senders conversation
           
        '''
        try:
            userlist=self._browser.elements_finder("default_im_users2")
            print("close conversation - userlist : ", userlist)
            close_buttons=self._browser.elements_finder("default_IM_chatclose1")
            icon=self._browser.elements_finder("default_im_users2")
            print("close conversation - close_buttons : ", close_buttons) 
            
            userindex = 0
            for user in userlist:
                user1=user.text
                if sender in user1:
                    print("Sender is found in user ************************************user value is : ",user)
                    print("Sender is found in user ************************************sender value is",sender)
                    print("Length of user list : ",len(userlist))
                    if len(userlist) > 1:
                        print("Length of user list > 1 is : ",len(userlist))                    
                        userindex = userlist.index(user)
                        print("User Index : ", userindex)
                    else:
                        print("Length of user list = 1 : ",len(userlist))                    
                        userindex = 0                    

                    print("user index is : ",userindex)    
                    print("Mouse hover starting **************************************")
                    time.sleep(3)
                    ActionChains(self._browser.get_current_browser()).move_to_element(user).perform()
                    #self.webAction.mouse_hover(user)
                    time.sleep(5)
                    print("Mouse hover successful **************************************")
            
            #Use Group location and click on Cross(X) button               
            close_buttons[userindex].click()
            print("##################closed################")
            #self.assertElement.page_should_not_contain_text(sender)
            log.mjLog.LogReporter("DefaultPanel","info","close_conversation -closed im conversation")
        except:
            log.mjLog.LogReporter("DefaultPanel","error","close_conversation - error in closing im conversation " +str(sys.exc_info()))
            raise

    def open_dialpad(self):
        """
        Author : Upendra
        Desc.  : open_dialpad - Open the dialpad on the Manhattan Client
        params : none
        """
        try:
            self.webAction.click_element("Dialpad_dialpad")
            log.mjLog.LogReporter("DefaultPanel", "info", "open_dialpad - Clicked on dial-pad")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "open_dialpad - Failed to click on dial-pad " + str(sys.exc_info()))
            raise
            
    def verify_dialpad(self):
        """
	    Author : Upendra
	    Desc.  : verify_dialpad - verify the dial-pad on the Manhattan Client
        params : none
        """
        try:
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verifying the dial-pad")        
            self.assertElement.element_should_be_displayed("Dialpad_num_one")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button one is present on the dial-pad")            
            self.assertElement.element_should_be_displayed("Dialpad_num_two")  
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button two is present on the dial-pad")            
            #self.assertElement.element_should_be_displayed("Dialpad_num_two_abc")
            #log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button two and \"abc\" are present on the dial-pad")            
            self.assertElement.element_should_be_displayed("Dialpad_num_three")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button three is present on the dial-pad")            
            #self.assertElement.element_should_be_displayed("Dialpad_num_three_def")
            #log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button three and \"def\" are present on the dial-pad")            
            self.assertElement.element_should_be_displayed("Dialpad_num_four")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button four is present on the dial-pad")
            self.assertElement.element_should_be_displayed("Dialpad_num_five")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button five are present on the dial-pad")            
            #self.assertElement.element_should_be_displayed("Dialpad_num_five_jkl")
            #log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button five and \"jkl\" are present on the dial-pad")            
            self.assertElement.element_should_be_displayed("Dialpad_num_six")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button six are present on the dial-pad")             
            #self.assertElement.element_should_be_displayed("Dialpad_num_six_mno")
            #log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button six and \"mno\" are present on the dial-pad")
            self.assertElement.element_should_be_displayed("Dialpad_num_eight")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button eight are present on the dial-pad")             
            #self.assertElement.element_should_be_displayed("Dialpad_num_eight_tuv")
            #log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button eight and \"tuv\" are present on the dial-pad") 
            self.assertElement.element_should_be_displayed("Dialpad_num_nine")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button nine are present on the dial-pad")             
            #self.assertElement.element_should_be_displayed("Dialpad_num_nine_wxyz")
            #log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button nine and \"wxyz\" are present on the dial-pad") 
            self.assertElement.element_should_be_displayed("Dialpad_num_zero")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button zero(0) is present on the dial-pad") 
            self.assertElement.element_should_be_displayed("Dialpad_num_asterix")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button asterix(*) is present on the dial-pad") 
            self.assertElement.element_should_be_displayed("Dialpad_num_hash")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified dial button hash(#) is present on the dial-pad")
            log.mjLog.LogReporter("DefaultPanel", "info", "verify_dialpad - verified the dial-pad")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "verify_dialpad"
                                  " - Failed to verify the dial-pad "+str(sys.exc_info()))
            raise

    def click_dialpad_numbers(self, dial):
        """
        Author: Upendra
        Description: To be able to click on the numbers on dial-pad
        params: one, two, three, four, five, six, seven, eight, nine
        Ex: click_dialpad_numbers dial=one
        """
        try:
            log.mjLog.LogReporter("DefaultPanel", "info", "click_dialpad_numbers - Click on dial-pad numbers")
            if dial == "one" or dial == "1":
                self.webAction.click_element("Dialpad_num_one")
            elif dial == "two" or dial == "2":
                self.webAction.click_element("Dialpad_num_two")
            elif dial == "three" or dial == "3":
                self.webAction.click_element("Dialpad_num_three")
            elif dial == "four" or dial == "4":
                self.webAction.click_element("Dialpad_num_four")
            elif dial == "five" or dial == "5":
                self.webAction.click_element("Dialpad_num_five")
            elif dial == "six" or dial == "6":
                self.webAction.click_element("Dialpad_num_six")
            elif dial == "seven" or dial == "7":
                self.webAction.click_element("Dialpad_num_seven")
            elif dial == "eight" or dial == "8":
                self.webAction.click_element("Dialpad_num_eight")
            elif dial == "nine" or dial == "9":
                self.webAction.click_element("Dialpad_num_nine")
            elif dial == "*":
                self.webAction.click_element("Dialpad_num_hash")
            elif dial == "#":
                self.webAction.click_element("Dialpad_num_asterix")
            elif dial == "0" or dial == "0":
                self.webAction.click_element("Dialpad_num_zero")
            else:
                log.mjLog.LogReporter("DefaultPanel", "error", "click_dialpad_numbers - incorrect parameter passed")
                raise AssertionError("Incorrect parameter passed")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "click_dialpad_numbers"
                                " - Failed to click on numbers on dial-pad " + str(sys.exc_info()))
            raise
            
    def ongoingcall_send_canned_response(self, response):
        """
        Author:Manoj
        ongoingcall_send_canned_response() - This method will types the own canned response im message while call in progress
        parameter : response (response to be send)
        """
        try:
            self.webAction.click_element("default_call_canned_resonse")
            time.sleep(1)
            self.webAction.click_element("default_canned_response_own_text")
            self.webAction.input_text("default_canned_response_own_text", response)
            time.sleep(1)
            self.webAction.press_key("default_canned_response_own_text", "ENTER")
            log.mjLog.LogReporter("DefaultPanel", "info", "ongoingcall_send_canned_response - clicked on send canned response")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "ongoingcall_send_canned_response - error in clicking on send canned response"
                                  " pressing Done button "+str(sys.exc_info()))
            raise

    def double_click_operator(self):
        """
        Author: kalyan
        double_click_operator() = Double click on incoming call to answers the call.
        change list: added log messages (UKumar: 26-Dec-2016)
        """
        try:
            List = self._browser.elements_finder("double_click_answers")
            held_count = 0
            for i in List:
                # Double Click to Answer the Call
                x = self._browser.get_current_browser()
                ActionChains(x).double_click(i).perform()
                time.sleep(3)
                self.assertElement.element_should_be_displayed("third_panel_call_end")
                log.mjLog.LogReporter("DefaultPanel", "info", "double_click_operator"
                                                              " - call is accepted by double click")
                # time.sleep(3)
                # Check if the contact card is opened for the active call.
                element1 = self.queryElement.get_text("answered_activeCallName")
                print("dashboard call name is:", element1.split('\n'))
                # time.sleep(3)
                element2 = self.queryElement.get_text("third_panel_new_contact")
                # time.sleep(3)
                if element2 in element1.split('\n'):
                    log.mjLog.LogReporter("DefaultPanel", "info", "double_click_operator"
                                                                  " - contact card has opened sucessfully")
                else:
                    raise AssertionError("contact card did not open")
                # Check if there is one active call in dashboard.
                element_active_call = self._browser.elements_finder("answered_activeCallName")
                if len(element_active_call) != 1:
                    raise AssertionError("Number of active calls in dashboard is more than one")
                else:
                    log.mjLog.LogReporter("DefaultPanel", "info", "double_click_operator"
                                                                  " - one active call is present in the dashboard")
                time.sleep(5)
                # Check the number of held calls in dashboard
                element_held = self._browser.elements_finder("held_call_in_dashboard")
                if (len(element_held) != held_count):
                    raise AssertionError("The number of held calls in dashboard is not as expected.")
                else:
                    log.mjLog.LogReporter("DefaultPanel", "info", "double_click_operator - "
                                                                  "As expected, the number of held calls is %s" % held_count)

                # increment the held call counter.
                held_count = held_count + 1

                # if (self.queryElement.element_not_displayed("double_click_answers")):
                # log.mjLog.LogReporter("DefaultPanel","error","double_click_operator - Call is answered by double clickinig on for Operator")
                # else:
                # raise AssertionError("Call is not answered by double click for Operator.")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "double_click_operator -"
                                                           " failed to answer call by double click " + str(
                sys.exc_info()))
            raise

    def double_click_nonoperator(self):

        """
        Author: kalyan
        double_click_nonoperator() = Double click on incoming call does not answers the call.

        """

        try:

            print("Double click answer the call for non operator")
            source = self._browser.element_finder("double_click_answers")
            x = self._browser.get_current_browser()
            time.sleep(1)
            # Double click on incoming call notification.
            ActionChains(x).double_click(source).perform()
            time.sleep(1)
            # Check that notification remains on dashboard.
            self.assertElement.element_should_be_displayed("double_click_answers")
            # Check that call hangup icon is not displayed.
            if (self.queryElement.element_not_displayed("third_panel_call_end")):
                print("Call is not answered by double click for Non Operator")
            else:
                print("Call is answered by double click for Non Operator.")
                raise AssertionError("Call is answered by double click for Non Operator")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "default_panel_answer_call - failed to answer call for non operaotor" + str(
                                      sys.exc_info()))
            raise

    def tab_check_PeoplePanel(self):
        '''
        author : kiran
        tab_check_PeoplePanel()
        '''
        try:
            self.assertElement.element_should_be_displayed("default_people_tab")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_people_check_open_tab- verified the people tab availability")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "tab_check_PeoplePanel - Failed to check people tab" + str(sys.exc_info()))
            raise

    def tab_check_RecentPanel(self):
        '''
        author : kiran
        tab_check_RecentPanel()
        '''
        try:
            self.assertElement.element_should_be_displayed("default_recent_tab")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "tab_check_RecentPanel- verified the Recent tab availability")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "tab_check_RecentPanel - Failed to check Recent tab" + str(sys.exc_info()))
            raise

    def tab_check_EventPanel(self):
        '''
        author : kiran
        tab_check_EventPanel()
        '''
        try:
            self.assertElement.element_should_be_displayed("default_events_tab")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "tab_check_EventPanel- verified the Event tab availability")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "tab_check_EventPanel - Failed to check Event tab" + str(sys.exc_info()))
            raise

    def tab_check_WorkgroupPanel(self):
        '''
        author : kiran
        tab_check_WorkgroupPanel()
        '''
        try:
            self.assertElement.element_should_be_displayed("default_WK_notify")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "tab_check_WorkgroupPanel- verified the WorkGroup tab availability")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "tab_check_WorkgroupPanel - Failed to check WorkGroup tab" + str(sys.exc_info()))
            raise

    def compress_uncompress_dashboard_comprs(self, params):
        '''
        author : kiran
        compress_uncompress_dashboard_comprs()
        '''
        try:
            if self.queryElement.element_not_displayed("default_compress_dashboard"):
                return False
            self.assertElement.element_should_be_displayed("default_compress_dashboard")
            if "pos" in params.keys():
                self.webAction.click_element("FP_compress_recBox")
                # this xpath checks the one row view which comes after compressing the dashboard view.
            else:
                self.webAction.click_element("default_compress_dashboard")
                # this xpath checks the one row view which comes after compressing the dashboard view.
            self.webAction.explicit_wait("FP_compress_one_row_view")
            log.mjLog.LogReporter("DefaultPanel", "info",
                                  "compress_uncompress_dashboard_comprs -compressing dashboard successful")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "compress_uncompress_dashboard_comprs - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def compress_uncompress_dashboard_UnComprs(self, params):
        '''
        author : kiran
        compress_uncompress_dashboard_UnComprs()
        '''
        try:
            if self.queryElement.element_not_displayed("default_uncompress_dashboard"):
                return False
            self.assertElement.element_should_be_displayed("default_uncompress_dashboard")
            if "pos" in params.keys():
                self.webAction.click_element("FP_compress_recBox")
            else:
                self.webAction.click_element("default_uncompress_dashboard")
            # this xpath checks the 3 row view which comes after uncompressing the dashboard view.
            RowNum = self._browser.elements_finder("FP_compress_three_row_view")
            if len(RowNum) >= 4:
                log.mjLog.LogReporter("DefaultPanel", "info", "compress_uncompress_dashboard_Check"
                                      " - dashboard has people, recent, and events tab in saparate row")
            else:
                raise AssertionError("tabs are not present in separate row")
            log.mjLog.LogReporter("DefaultPanel", "info",
                                  "compress_uncompress_dashboard_UnComprs - uncompressing dashboard successful")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "compress_uncompress_dashboard_UnComprs"
                                                           " - Failed to check routing slip" + str(sys.exc_info()))
            raise

    def compress_uncompress_dashboard_Check(self, params):
        '''
        author : kiran
        compress_uncompress_dashboard_Check()
        '''
        try:
            if params["mode"].lower() == "compressed":
                self.assertElement.element_should_be_displayed("default_uncompress_dashboard")
                self.assertElement.element_should_be_displayed("FP_compress_one_row_view")
                log.mjLog.LogReporter("DefaultPanel", "info",
                                      "compress_uncompress_dashboard_Check - compressed mode verified")
            elif params["mode"].lower() == "uncompressed":
                self.assertElement.element_should_be_displayed("default_compress_dashboard")
                RowNum = self._browser.elements_finder("FP_compress_three_row_view")
                if len(RowNum) >= 4:
                    log.mjLog.LogReporter("DefaultPanel", "info", "compress_uncompress_dashboard_Check"
                                          " - dashboard has people, recent, and events tab in saparate row")
                    log.mjLog.LogReporter("DefaultPanel", "info",
                                          "compress_uncompress_dashboard_Check - uncompressed mode verified")
                else:
                    raise AssertionError("tabs are not present in saparate row")
            else:
                raise AssertionError("Incorrect argument!")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "compress_uncompress_dashboard_Check"
                                                           " - Failed to check routing slip" + str(sys.exc_info()))
            raise

    def verify_contactCard_from_systemDirectory(self, params):
        '''
           author : kiran
           verify_contactCard_from_systemDirectory() - this API verifies the contact card name from third panel contcat name.
           ex1: verify_contactCard_from_systemDirectory
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info",
                                  "verify_contactCard_from_systemDirectory- it will verify contact card name with system directory contact name")
            contact = params["contact"].replace("*", ' ')
            if "search" in params.keys():
                self.search_people_or_extension(contact)
            contctList = self._browser.elements_finder("people_search")
            flag = 0
            print(len(contctList))
            for i in contctList:
                dir_contact = i.text.replace(" ", "").replace("\n", "")
                print(contact.replace(" ", ""), dir_contact)
                # time.sleep(2)
                if "search" in params.keys():
                    if contact.replace(" ", "") in dir_contact:
                        i.click()
                        time.sleep(1)
                        flag = 1
                        if "call" in params.keys():
                            x = self._browser.get_current_browser()
                            ActionChains(x).double_click(i).perform()
                        break
                elif contact.replace(" ", "") in dir_contact:
                    i.click()
                    flag = 1
                    if "call" in params.keys():
                        x = self._browser.get_current_browser()
                        ActionChains(x).double_click(i).perform()
                    break
            if flag == 0:
                raise
            time.sleep(1)
            thirdPcontct = self._browser.element_finder("third_panel_new_contact")
            print("*called*", thirdPcontct.text, contact)

            if thirdPcontct.text == contact:
                print("third panel contact name matched with system directory contact")
                self.assertElement._is_element_contains("third_panel_answer_call")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "verify_contactCard_from_systemDirectory- successfully verify the contact card name")
            else:
                print("contact name found in system directory is not matching with third panel contact card name")
                raise
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "verify_contactCard_from_systemDirectory- failed to verify the system directory contact name with third panel contact card name" + str(
                                      sys.exc_info()))
            raise

    def click_and_Hold_the_Call(self, params):
        '''
        author : kiran
        click_and_Hold_the_Callclick_and_Hold_the_Call()
        '''
        try:
            # here the name of the call is matching and dragging that perticular call and doing mouse hover to the searched contact(so that contexual menu should appear)...
            if params["option"] == "In_call":
                call_contact_list1 = self._browser.elements_finder("default_callee_name")
            elif params["option"] == "Outgoing_call":
                call_contact_list1 = self._browser.elements_finder("group_edit_draft")
            elif params["option"] == "voice_mail":
                call_contact_list1 = self._browser.elements_finder("default_client_pane_user")
            else:
                call_contact_list1 = self._browser.elements_finder("default_im_pane_user")
                print("click and hold", len(call_contact_list1))
            for i in call_contact_list1:
                print(i.text, params["callName"])
                if i.text.strip(' ') == params["callName"].replace("*", " "):
                    ActionChains(self._browser.get_current_browser()).move_to_element(i).perform()
                    ActionChains(self._browser.get_current_browser()).click_and_hold(i).perform()
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "click_and_Hold_the_Call- verified the call dashboard and required call has been dragged to contact")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "click_and_Hold_the_Call - Failed to drag the call" + str(sys.exc_info()))
            raise

    def HoverToContact_InCall(self, params):
        '''
        author : kiran
        HoverToContact_InCall()
        '''
        try:
            # here the name of the call is matching and dragging that perticular call and doing mouse hover to the searched contact(so that contexual menu should appear)...
            call_contact_list1 = self._browser.elements_finder("default_callee_name")
            if "searchItem" in params.keys():
                self.webAction.mouse_hover("SP_anchor_contact")
                call_contact_list2 = self._browser.elements_finder("default_callee_name")
                searchList = self._browser.element_finder("SP_anchor_contact")
                time.sleep(2)
                print(len(call_contact_list2))
                # verify the call dashboard increased by 1
                if "nodrag" in params.keys():
                    if (len(call_contact_list2) == len(call_contact_list1) + 1):
                        raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                        return False
                else:
                    if (len(call_contact_list2) != len(call_contact_list1) + 1):
                        raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                        return False
                if "release" in params.keys():
                    ActionChains(self._browser.get_current_browser()).release(searchList).perform()
            elif "directory" in params.keys():
                self.webAction.mouse_hover("first_panel_Event_draft_convr")
                call_contact_list2 = self._browser.elements_finder("default_callee_name")
                if (len(call_contact_list2) != len(call_contact_list1) + 1):
                    raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                    return False
            elif "GroupName" in params.keys():
                grouplist = self._browser.elements_finder("peoples_first_group")
                for i in grouplist:
                    if i.text.strip(' ') == params["GroupName"].replace("*", " "):
                        ActionChains(self._browser.get_current_browser()).move_to_element(i).perform()
                        # verify the call dashboard increased by 1
                        call_contact_list2 = self._browser.elements_finder("default_callee_name")
                        if (len(call_contact_list2) != len(call_contact_list1) + 1):
                            raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                            return False
                        if "release" in params.keys():
                            ActionChains(self._browser.get_current_browser()).release(i).perform()
            elif "GrpContact" in params.keys():
                grpContlist = self._browser.elements_finder("peoples_grp_customer_name")
                for i in grpContlist:
                    print("hover", i.text, params["GrpContact"])
                    if i.text.strip(' ') == params["GrpContact"].replace("*", " "):
                        print(".@@@@@inside the loop")
                        ActionChains(self._browser.get_current_browser()).move_to_element(i).perform()
                        # verify the call dashboard increased by 1
                        call_contact_list2 = self._browser.elements_finder("default_callee_name")
                        if (len(call_contact_list2) != len(call_contact_list1) + 1):
                            raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                            return False
                        if "release" in params.keys():
                            ActionChains(self._browser.get_current_browser()).release(i).perform()
            elif "FavContact" in params.keys():
                FavContlist = self._browser.elements_finder("SP_group_contact_list")
                for i in FavContlist:
                    print("hover", i.text, params["FavContact"])
                    if i.text == params["FavContact"].replace("*", " "):
                        ActionChains(self._browser.get_current_browser()).move_to_element(i).perform()
                        # verify the call dashboard increased by 1
                        call_contact_list2 = self._browser.elements_finder("default_callee_name")
                        if (len(call_contact_list2) != len(call_contact_list1) + 1):
                            raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                            return False
                        if "release" in params.keys():
                            ActionChains(self._browser.get_current_browser()).release(i).perform()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "HoverToContact_InCall- verified the call dashboard and required call has been dragged to contact")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "HoverToContact_InCall - Failed to drag the call" + str(sys.exc_info()))
            raise

    def HoverToContact_IncomingCall(self, params):
        '''
        author : kiran
        HoverToContact_IncomingCall()
        '''
        try:
            # here the name of the call is matching and dragging that perticular call and doing mouse hover to the searched contact(so that contexual menu should appear)...
            call_contact_list1 = self._browser.elements_finder("default_im_pane_user")
            print("length of list is : list1 : ", len(call_contact_list1))
            for l1 in call_contact_list1:
                print("list1 : ", l1.text)
            if "searchItem" in params.keys():
                self.webAction.mouse_hover("SP_anchor_contact")
                call_contact_list2 = self._browser.elements_finder("default_im_pane_user")
                for l2 in call_contact_list2:
                    print("list2 : ", l2.text)
                searchList = self._browser.element_finder("SP_anchor_contact")
                if "release" in params.keys():
                    ActionChains(self._browser.get_current_browser()).release(searchList).perform()
            elif "directory" in params.keys():
                self.webAction.mouse_hover("first_panel_Event_draft_convr")
                call_contact_list2 = self._browser.elements_finder("default_im_pane_user")
            if (len(call_contact_list2) != len(call_contact_list1) + 1):
                # raise AssertionError("after mouse hover the call dashboard did not increased by 1")
                raise
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "HoverToContact_IncomingCall - Failed to drag the call" + str(sys.exc_info()))
            raise

    def HoverToContact_OutGoingCall(self, params):
        '''
        author : kiran
        HoverToContact_OutGoingCall()
        '''
        try:
            # here the name of the call is matching and dragging that perticular call and doing mouse hover to the searched contact(so that contexual menu should appear)...
            call_contact_list1 = self._browser.elements_finder("group_edit_draft")
            if "searchItem" in params.keys():
                self.webAction.mouse_hover("SP_anchor_contact")
                call_contact_list2 = self._browser.elements_finder("group_edit_draft")
                searchList = self._browser.element_finder("SP_anchor_contact")
                if "release" in params.keys():
                    ActionChains(self._browser.get_current_browser()).release(searchList).perform()
            if (len(call_contact_list2) == len(call_contact_list1) + 1):
                raise AssertionError("after mouse hover the call dashboard is increased by 1")
                return False
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "HoverToContact_OutGoingCall - Failed to drag the call" + str(sys.exc_info()))
            raise

    def BlindTransfer_from_contexualMenu(self):
        '''
        author : kiran
        BlindTransfer_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the blind transfer option from contexual menu...
            self.assertElement._is_element_contains("SP_contexBlindT")
            self.webAction.click_element("SP_contexBlindT")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "BlindTransfer_from_contexualMenu- passed to bilnd transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "BlindTransfer_from_contexualMenu - Failed to bilnd transfer the call" + str(
                                      sys.exc_info()))
            raise

    def BlindConf_from_contexualMenu(self):
        '''
        author : kiran
        BlindConf_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the blind conference option from contexual menu...
            self.assertElement._is_element_contains("SP_contexBlindConfT")
            self.webAction.click_element("SP_contexBlindConfT")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "BlindConf_from_contexualMenu- passed to bilnd conference the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "BlindConf_from_contexualMenu - Failed to do bilnd conference the call" + str(
                                      sys.exc_info()))
            raise

    def ConsultTrans_from_contexualMenu(self):
        '''
        author : kiran
        ConsultTrans_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the consult transfer option from contexual menu...
            self.assertElement._is_element_contains("SP_contexConsultT")
            self.webAction.click_element("SP_contexConsultT")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "ConsultTrans_from_contexualMenu- passed to consult transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "ConsultTrans_from_contexualMenu - Failed to consult transfer the call" + str(
                                      sys.exc_info()))
            raise

    def InterCom_from_contexualMenu(self):
        '''
        author : kiran
        InterCom_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the intercom transfer option from contexual menu...
            self.assertElement._is_element_contains("SP_contexIntercomT")
            self.webAction.click_element("SP_contexIntercomT")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "InterCom_from_contexualMenu- passed to intercom conference transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "InterCom_from_contexualMenu - Failed to intercom conference transfer the call" + str(
                                      sys.exc_info()))
            raise

    def InterCom_conference_from_contexualMenu(self):
        '''
        author : kiran
        InterCom_conference_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the intercom conference option from contexual menu...
            self.assertElement._is_element_contains("SP_contexIntercomConf")
            self.webAction.click_element("SP_contexIntercomConf")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "InterCom_conference_from_contexualMenu- passed to intercom conference transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "InterCom_conference_from_contexualMenu - Failed to intercom conference transfer the call" + str(
                                      sys.exc_info()))
            raise

    def park_and_InterCom_from_contexualMenu(self):
        '''
        author : kiran
        park_and_InterCom_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the intercom conference option from contexual menu...
            self.assertElement._is_element_contains("SP_contexPark_and_Intercom")
            self.webAction.click_element("SP_contexPark_and_Intercom")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "park_and_InterCom_from_contexualMenu- passed to do park and intercom transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "park_and_InterCom_from_contexualMenu - Failed to park and intercom transfer the call" + str(
                                      sys.exc_info()))
            raise

    def Park_from_contexualMenu(self):
        '''
        author : kiran
        Park_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the Park transfer option from contexual menu...
            self.assertElement._is_element_contains("SP_contexParkT")
            parkList = self._browser.elements_finder("SP_contexParkT")
            parkList[0].click()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Park_from_contexualMenu- passed to Park transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "Park_from_contexualMenu - Failed to Park transfer the call" + str(sys.exc_info()))
            raise

    def WhisperT_from_contexualMenu(self):
        '''
        author : kiran
        WhisperT_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the Whisper transfer option from contexual menu...
            self.assertElement._is_element_contains("SP_contexWhisperT")
            self.webAction.click_element("SP_contexWhisperT")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "WhisperT_from_contexualMenu- passed to Whisper transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "WhisperT_from_contexualMenu - Failed to Whisper transfer the call" + str(
                                      sys.exc_info()))
            raise

    def ConsltConf_from_contexualMenu(self):
        '''
        author : kiran
        ConsltConf_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the consult conference option from contexual menu...
            self.assertElement._is_element_contains("SP_contexConsConf")
            self.webAction.click_element("SP_contexConsConf")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "ConsltConf_from_contexualMenu- passed to consult conference the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "ConsltConf_from_contexualMenu - Failed to consult conference the call" + str(
                                      sys.exc_info()))
            raise

    def MailBoxTransfer_from_contexualMenu(self):
        '''
        author : kiran
        MailBoxTransfer_from_contexualMenu()
        '''
        try:
            # here we are verify/selecting the mailbox transfer option from contexual menu...
            self.assertElement._is_element_contains("SP_contexTransMailbox")
            self.webAction.click_element("SP_contexTransMailbox")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "MailBoxTransfer_from_contexualMenu- passed to mailbox transfer the call")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "MailBoxTransfer_from_contexualMenu - Failed to mailbox transfer the call" + str(
                                      sys.exc_info()))
            raise

    def workgrp_iconColorCheck_inCompressed(self, params):
        '''
        author : kalyan
        workgrp_iconColorCheck_inCompressed()
        '''
        try:
            if params["color"] == "green":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inCompressed- verify workgroup icon color is green")
                self.assertElement._is_element_contains("FP_compressed_WG_green_color")
            elif params["color"] == "yellow":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inCompressed- verify workgroup icon color is yellow")
                self.assertElement._is_element_contains("FP_compressed_workgrp_yellow_color")
            elif params["color"] == "black":
                self.assertElement._is_element_contains("FP_compressed_wg_black_color")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inCompressed- Workgroup is not logged in")
                self.assertElement._is_element_contains("FP_compressed_wg_black_color")
            else:
                raise AssertionError("invalid parameters passed")
                return False
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "workgrp_iconColorCheck_inCompressed - Failed verify the whisper pageavaibility in call" + str(
                                      sys.exc_info()))
            raise

    def workgrp_iconColorCheck_inUnCompressed(self, params):
        '''
        author : kalyan
        workgrp_iconColorCheck_inUnCompressed()
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "workgrp_iconColorCheck_inUnCompressed- The dashboard is in uncompressed mode")
            time.sleep(2)
            if params["color"] == "green":
                self.assertElement._is_element_contains("FP_workgrp_green_color")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inUnCompressed- verify workgroup icon color is green")
            elif params["color"] == "yellow":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inUnCompressed- verify workgroup icon color is yellow")
                self.assertElement._is_element_contains("FP_workgrp_yellow_color")
                self.assertElement._is_element_contains("FP_wrkgrp_wrapup_text")
            elif params["color"] == "black":
                self.assertElement._is_element_contains("FP_wg_black_color")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inUnCompressed- Workgroup is not logged in")
                self.assertElement._is_element_contains("FP_wg_black_color")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgrp_iconColorCheck_inUnCompressed- successfully verified")
            else:
                raise AssertionError("invalid parameters passed")
                return False
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "workgrp_iconColorCheck_inCompressed - Failed verify the whisper pageavaibility in call" + str(
                                      sys.exc_info()))
            raise

    def Verify_contextual_Menu(self, is_present):
        '''
        author : kiran
        Verify_contextual_Menu()
        '''
        try:
            # here we are verify/selecting the intercom transfer option from contexual menu...
            menu_present = not self.queryElement.element_not_displayed("SP_contexBlindT")
            print("status of menu is:", menu_present)
            if is_present == 'yes':
                if menu_present == False:
                    raise
            elif is_present == 'No':
                if menu_present == True:
                    raise
            elif is_present == 'non_operator':
                if menu_present == False:
                    raise
                print("time is ....................", datetime.datetime.now())
                self.assertElement.page_should_not_contain_text("Consult Transfer")
                self.assertElement.page_should_not_contain_text("Intercom Transfer")
                self.assertElement.page_should_not_contain_text("Transfer Mailbox")
                self.assertElement.page_should_not_contain_text("Intercom Conference")
                self.assertElement.page_should_not_contain_text("Consult Conference")
                self.assertElement.page_should_not_contain_text("Park and Page")
                self.assertElement.page_should_not_contain_text("Park and Intercom")
                print("time is ....................", datetime.datetime.now())
                # self._browser.implicitly_wait(10)
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Verify_contextual_Menu- contexual menu has been verified")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "Verify_contextual_Menu - Failed to verify contexual menu " + str(sys.exc_info()))
            raise

    def click_verify_routing_slip_present(self, params):
        '''
        author : kiran
        click_verify_routing_slip_present()
        '''
        try:
            routInfoList = self._browser.elements_finder("FP_default_routing_slip_info")
            print("the length of routing slip info is :", len(routInfoList))
            if (params["count"]) == (len(routInfoList)):
                print("Number of Routing Slips displayed matched the expected number")
            elif len(routInfoList) >= 1:
                for i in routInfoList:
                    spl = i.text.split()
                    print(len(spl))
                    print("variables are:", params["caller"], spl[0], params["callee"], spl[2])
                    if (params["call_type"] == "simple_call"):
                        if (params["caller"] in spl[0]) and (params["callee"] in spl[2]):
                            log.mjLog.LogReporter("ManhattanComponent", "info", "click_verify_routing_slip"
                                                                                " - routing slip verified")
                            if params["is_present"] == "yes":
                                print("the routing slip opened for the call as expected.")
                                # else:
                                # return False
                        else:
                            if params["is_present"] == "no":
                                print("The routing slip not open for the call ened as expected.")
                            else:
                                return False
                    elif params["call_type"] == "parked_call":
                        print(spl)
                        print(params["caller"], spl[0], params["callee"], spl[2])
                        # if ("parked" == spl[1]) and (params["callee"] in spl[3]):
                        if (params["caller"] in i.text and params["callee"] in i.text):
                            print("....the parked call has been checked......")
                        else:
                            return False
                    elif params["call_type"] == "return_parked":
                        print(spl)
                        if ("Couldn't" == spl[0]) and ("unpark;" == spl[1]) and ("call" == spl[2]) and (
                            "returned" == spl[3]):
                            print(".....the parked hasbeen successfully returned back......")
                    elif params["call_type"] == "trnsefered_call":
                        print("........................", i.text)
                        if (params["caller"] in i.text and params["callee"] in i.text):
                            print("....the transfered call successfully...")
                        else:
                            return False
                    else:
                        return False
            else:
                return False
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "click_verify_routing_slip_present - Failed to check the routing slip" + str(
                                      sys.exc_info()))
            raise

    def click_verify_routing_slip_hide(self, params):
        '''
        author : kiran
        click_verify_routing_slip_hide()
        '''
        try:
            if params["hide"] == "no":
                self.webAction.click_element("first_panel_routing_slip")
                self.assertElement.element_should_be_displayed("FP_default_routing_slip_compress")
            elif params["hide"] == "yes":
                if "call" in params.keys() and params["call"] == "held":
                    self.assertElement.element_should_be_displayed("FP_default_routing_slip_show_info_when_OnHold")
                    self.webAction.click_element("FP_default_routing_slip_show_info_when_OnHold")
                else:
                    self.assertElement.element_should_be_displayed("FP_default_routing_slip_compress")
                    self.webAction.click_element("FP_default_routing_slip_compress")

                if self.queryElement.element_not_displayed("first_panel_routing_slip"):
                    print("routing slip has been hided")
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_verify_routing_slip_hide"
                                                                " - show/hide routing slip successfull")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "click_verify_routing_slip_hide - Failed to check routing slip" + str(sys.exc_info()))
            raise

    def click_verify_routing_slip_show(self, params):
        '''
        author : kiran
        click_verify_routing_slip_show()
        '''
        try:
            if params["show"] == "second_routingSlip":
                self.webAction.click_element("first_panel_routingSlip_hideInfo2")
                self.assertElement.element_should_be_displayed("first_panel_routingSlip_openInfo2")
            elif params["show"] == "third_routingSlip":
                self.webAction.click_element("first_panel_routingSlip_hideInfo3")
                self.assertElement.element_should_be_displayed("first_panel_routingSlip_openInfo3")
            else:
                self.webAction.click_element("FP_default_routing_slip_show_info")
                self.assertElement.element_should_be_displayed("first_panel_routing_slip")
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_verify_routing_slip_show"
                                                                " - show/hide routing slip successfull")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "click_verify_routing_slip_show - Failed to check routing slip" + str(sys.exc_info()))
            raise

    def end_call(self):
        '''
           ends call by clicking red color end button
        '''
        try:
            time.sleep(2)
            self.webAction.mouse_hover("default_call_section")
            time.sleep(2)
            self.assertElement.element_should_be_displayed("default_call_end_button")
            self.webAction.click_element("default_call_end_button")
            log.mjLog.LogReporter("DefaultPanel", "info", "Clicked on End button")
            self.queryElement.element_not_displayed("default_call_section")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "Error while ending the call from default panel " + str(sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_incomingCall(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_incomingCall()
        '''
        try:
            self.webAction.mouse_hover("FP_ringing_incomming_call")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            if "release" in params.keys():
                self.source_ele = self._browser.element_finder("FP_ringing_incomming_call")
                ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_incomingCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_ParkedCall(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_ParkedCall()
        '''
        try:
            self.webAction.mouse_hover("default_panel_voicemail1")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            self.source_ele = self._browser.element_finder("default_panel_voicemail1")
            ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_ParkedCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_ConfCall(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_ConfCall()
        '''
        try:
            self.webAction.mouse_hover("default_OutG_CallName")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            self.source_ele = self._browser.element_finder("default_OutG_CallName")
            ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_ConfCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_VMCall(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_VMCall()
        '''
        try:
            self.webAction.mouse_hover("default_panel_voicemail")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            self.source_ele = self._browser.element_finder("default_panel_voicemail")
            ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_VMCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_IM_notific(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_IM_notific()
        '''
        try:
            self.webAction.mouse_hover("default_IM_notification_hover1")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            self.source_ele = self._browser.element_finder("default_IM_notification_hover1")
            ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_IM_notific - Failed to verify" + str(
                                      sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_GRP_DRAFT(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_GRP_DRAFT()
        '''
        try:
            self.webAction.mouse_hover("default_GRPdraft_Notif")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            self.source_ele = self._browser.element_finder("default_GRPdraft_Notif")
            ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_GRP_DRAFT - Failed to verify" + str(
                                      sys.exc_info()))
            raise

    def blind_transfer_from_search_item_to_EVNT_NOTIF(self, params):
        '''
        author : kiran
        blind_transfer_from_search_item_to_EVNT_NOTIF()
        '''
        try:
            self.webAction.mouse_hover("event_DashB_notification")
            list = self._browser.elements_finder("SP_anchor_contact")
            if len(list) == 2:
                print("length of list has been increased after mouse hover", len(list))
            else:
                print("click and hold operation not allowed here and the length of contact will be remain same",
                      len(list))
            self.source_ele = self._browser.element_finder("event_DashB_notification")
            ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "blind_transfer_from_search_item_to_EVNT_NOTIF - Failed to verify" + str(
                                      sys.exc_info()))
            raise

    def select_people_view_compact(self):
        '''
        author : Indresh
        select_people_view_compact()
        '''
        try:
            if self.queryElement.element_not_displayed("peoples_gridIcon"):
                self.webAction.click_element("peoples_listIcon")
                time.sleep(0.5)
                self.webAction.click_element("FP_compact_view")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "select_people_view_SmallA - Failed to check routing slip" + str(sys.exc_info()))
            raise

    def select_people_view_list(self):
        '''
        author : Indresh
        select_people_view_list()
        '''
        try:
            if self.queryElement.element_not_displayed("peoples_listIcon"):
                self.webAction.click_element("peoples_gridIcon")
                time.sleep(0.5)
                self.webAction.click_element("FP_list_view")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "select_people_view_list - Failed to check routing slip" + str(sys.exc_info()))
            raise

    def transfer_call_by_dragNdrop_searchContact_to_inCall(self, params):
        '''
        author : kiran
        transfer_call_by_dragNdrop_searchContact_to_inCall()
        '''
        try:
            name = params["searchItem"]
            searchlist1 = self._browser.elements_finder("peoples_panel_customer_name_new")
            for i in searchlist1:
                if name in i.text:
                    ActionChains(self._browser.get_current_browser()).click_and_hold(i).perform()
                    list4 = self._browser.elements_finder("peoples_panel_customer_name_new")
                    self.webAction.mouse_hover("default_client_pane_user")
                    if len(list4) == len(searchlist1) + 1:
                        print("length of group name has been increased after mouse hover", len(list4))
                    else:
                        print("the contact name can not draggable....")
                        return False
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "transfer_call_by_dragNdrop_searchContact_to_inCall - Failed transfer the call" + str(
                                      sys.exc_info()))
            raise

    def transfer_call_by_dragNdrop_favCon_to_inCall(self, params):
        '''
        author : kiran
        transfer_call_by_dragNdrop_favCon_to_inCall()
        '''
        try:
            list = self._browser.elements_finder("people_filter_lastcontact")
            print("list value is:", list)
            for i in list:
                if (i.text.strip(' ') == params["searchItem"]):
                    ActionChains(self._browser.get_current_browser()).click_and_hold(i).perform()
                    self.webAction.mouse_hover("default_client_pane_user")
                    print("mouse hover success")
                    list2 = self._browser.elements_finder("people_filter_lastcontact")
                    if (len(list2) == len(list) + 1):
                        print("length of list2 has been increased after mouse hover", len(list2))
                    else:
                        raise AssertionError("the object is not draggable....")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "transfer_call_by_dragNdrop_favCon_to_inCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def transfer_call_by_dragNdrop_grpCon_to_inCall(self, params):
        '''
        author : kiran
        transfer_call_by_dragNdrop_grpCon_to_inCall()
        '''
        try:
            x = params["searchItem"]
            name = x.split("#")
            spl = name[1]
            contact = spl.split("*")
            Gcontact = " ".join(contact)
            grouplist1 = self._browser.elements_finder("peoples_first_group")
            Gcontactlist = self._browser.elements_finder("people_filter_lastcontact")
            for i in grouplist1:
                if i.text == name[0]:
                    for j in Gcontactlist:
                        print("the contacts are", Gcontact, j.text)
                        if j.text == Gcontact:
                            ActionChains(self._browser.get_current_browser()).click_and_hold(j).perform()
                            self.webAction.mouse_hover("default_client_pane_user")
                            list3 = self._browser.elements_finder("people_filter_lastcontact")
                            if len(list3) == len(Gcontactlist) + 1:
                                print("length of group Contact has been increased by 1 after mouse hover", len(list3))
                            else:
                                raise AssertionError("the contact length is not incresed after dragging...", len(list3),
                                                     len(Gcontactlist))
                                return False
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "transfer_call_by_dragNdrop_grpCon_to_inCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def transfer_call_by_dragNdrop_grpName_to_inCall(self, params):
        '''
        author : kiran
        transfer_call_by_dragNdrop_grpName_to_inCall()
        '''
        try:
            name = params["searchItem"]
            grouplist1 = self._browser.elements_finder("peoples_first_group")
            for i in grouplist1:
                if name in i.text:
                    ActionChains(self._browser.get_current_browser()).click_and_hold(i).perform()
                    list4 = self._browser.elements_finder("peoples_first_group")
                    self.webAction.mouse_hover("default_client_pane_user")
                    if len(list4) == len(grouplist1) + 1:
                        print("length of group name has been increased after mouse hover", len(list4))
                        return False
                    else:
                        print("the group name can not draggable....")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "transfer_call_by_dragNdrop_grpName_to_inCall - Failed to check routing slip" + str(
                                      sys.exc_info()))
            raise

    def verify_conference_call_users(self, userlist):

        """
        Author: kiran
        verify_conference_call_users() = verify the conference call users.

        """
        try:
            self.webAction.click_element("default_clicktogglecall")
            time.sleep(1)
            pos = 1
            for i in userlist:
                pos = str(pos)
                user_name = "default_call" + pos
                user_text = self.queryElement.get_text(user_name)
                if user_text in userlist:
                    conf_user_end = "first_panel_end_conference_call" + pos
                    self.assertElement.page_should_contain_element(conf_user_end)
                pos = int(pos) + 1
            self.webAction.click_element("default_clicktogglecallclose")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "failed to verify the conferenece call users" + str(sys.exc_info()))
            raise

    def end_any_call_from_conferenceCall(self, userlist):
        """
        Author: kiran
        end_any_call_from_conferenceCall() : end the call from conference call.
        """
        try:
            self.webAction.click_element("default_clicktogglecall")
            self.webAction.explicit_wait("default_call1")
            call_legs_ended = 0
            num_participants = self._browser.elements_finder("default_call_list")

            for user in userlist:
                end_call_button_list = self._browser.elements_finder("first_panel_end_conference_call")
                for i, participant in enumerate(num_participants):
                    if participant.text.strip() == user:
                        end_call_button_list[i].click()
                        log.mjLog.LogReporter("DefaultPanel", "info", "end_any_call_from_conferenceCall"
                                              " - ended the conferenece call with user %s" % user)
                        break
                else:
                    raise AssertionError("User not found!")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "end_any_call_from_conferenceCall - "
                                  "failed to end the conferenece call " + str(sys.exc_info()))
            raise

    def verify_recent_counter_badge(self, params):
        '''
           This API verify recent tab badge count
        '''
        try:
            if "tab" in params.keys():
                if params["tab"] == "voicemails":
                    if params["badgeNo"] == "0":
                        self.assertElement.element_should_not_be_displayed("first_panel_voicemail_badge_no")
                        log.mjLog.LogReporter("DefaultPanel", "info",
                                              "verify_recent_counter_badge - Recent counter badge has no entries")
                    else:
                        number = self.queryElement.get_text("first_panel_voicemail_badge_no")
                        if number == params["badgeNo"]:
                            log.mjLog.LogReporter("DefaultPanel", "info", "verify_recent_counter_badge"
                                                                          " - Recent counter badge no. is as expected")
                        else:
                            raise AssertionError("DefaultPanel", "error", "verify_recent_counter_badge"
                                                                          " - Recent counter badge is not as expected")
                elif params["tab"] == "messages":
                    if params["badgeNo"] == "0":
                        self.assertElement.element_should_not_be_displayed("first_panel_messages_badge_no")
                        log.mjLog.LogReporter("DefaultPanel", "info", "verify_recent_counter_badge"
                                                                      " - Messages counter badge has no entries")
                    else:
                        number = self.queryElement.get_text("first_panel_messages_badge_no")
                        if number == params["badgeNo"]:
                            log.mjLog.LogReporter("DefaultPanel", "info", "verify_recent_counter_badge"
                                                  " - Messages counter badge no. is as expected")
                        else:
                            raise AssertionError("DefaultPanel", "error", "verify_recent_counter_badge"
                                                 " - Messages counter badge is not as expected")
                elif params["tab"] == "recent":
                    if params["badgeNo"] == "0":
                        self.assertElement.element_should_not_be_displayed("first_panel_recent_badge_no")
                        log.mjLog.LogReporter("DefaultPanel", "info", "verify_recent_counter_badge"
                                                                      " - Recent counter badge has no entries")
                    else:
                        number = self.queryElement.get_text("first_panel_recent_badge_no")
                        if number == params["badgeNo"]:
                            log.mjLog.LogReporter("DefaultPanel", "info", "verify_recent_counter_badge"
                                                                          " - Recent counter badge no. is as expected")
                        else:
                            raise AssertionError("DefaultPanel", "error", "verify_recent_counter_badge"
                                                                          " - Recent counter badge is not as expected")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "Recent counter badge is not as expected " + str(sys.exc_info()))
            raise

    def delete_event_draft(self):
        """
        Author: UKumar
        delete_event_draft(): TO delete event draft
        Parameters: no parameter
        """
        try:
            self.webAction.click_element("FP_delete_event_draft")
            self.webAction.explicit_wait("TP_discard_changes_draft_button")
            self.webAction.click_element("TP_discard_changes_draft_button")
            log.mjLog.LogReporter("DefaultPanel", "info",
                                  "delete_event_draft - clicked on Discard My Changes button to delete draft")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "delete_event_draft - Failed to delete event draft " + str(sys.exc_info()))
            raise
    
#Sprint 4
    def initiate_verify_search(self, search_item):
        """
        Author: UKumar
        initiate_verify_search() : Initiates search for contacts by typing in search bar
        Parameters: search_item
        """
        try:
            ActionChains(self._browser.get_current_browser()).send_keys(search_item).perform()
            search_result = self._browser.elements_finder("peoples_panel_customer_name")
            if len(search_result) >= 1:
                log.mjLog.LogReporter("DefaultPanel", "info", "initiate_verify_search"
                                      " - search has been initiated.")
            else:
                raise AssertionError("Not able to type in search bar!")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "initiate_verify_search - Error: "+str(sys.exc_info()))
            raise
    def search_people_by_firstname(self, searchItem, throwException = False):
        '''
            Enter the name or number in search bar
            check the contact exist  or not
            if exist show the details
        '''
        try:
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            log.mjLog.LogReporter("DefaultPanel","debug","search_people_by_firstname - Clicked on search button")
            self.webAction.input_text("default_search_input",searchItem)
            self.webAction.explicit_wait("peoples_panel_customer_name")
            searchResultsList=self._browser.elements_finder("peoples_panel_customer_name")
            
            if len(searchResultsList)==0:
                if throwException==False:
                    return False
                else:
                    log.mjLog.LogReporter("DefaultPanel","info","search_people_by_firstname - No contact found!")
                    raise AssertionError("No contact found")
            elif len(searchResultsList) > 1:
                log.mjLog.LogReporter("DefaultPanel","info","search_people_by_firstname - More than one contact found")
                return searchResultsList
            else:
                log.mjLog.LogReporter("DefaultPanel","info","search_people_by_firstname - %s is available" %(searchItem))
                return searchResultsList[0]
        except:
            log.mjLog.LogReporter("DefaultPanel","error","search_people_by_firstname-Error while searching people" +str(sys.exc_info()))
            raise        

        
    def close_verify_search(self):
        """
        Author: UKumar
        close_verify_search() : Closes the search result by pressing ESCAPE
                                and verifies that it has been closed
        Parameters: no parameter
        """
        try:
            ActionChains(self._browser.get_current_browser()).send_keys(Keys.ESCAPE).perform()
            if self.queryElement.element_not_displayed("extension_close_searching"):
                log.mjLog.LogReporter("DefaultPanel", "info", "close_verify_search"
                                      " - search result closed.")
            else:               
                raise AssertionError("Search result not closed!")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error", "close_verify_search - Error: "+str(sys.exc_info()))
            raise
	
    def search_list_people_or_extension(self, searchItem):
        '''
            Enter the name or number in search bar
            check the contact exist  or not
            if exist show the details
        '''
        try:
            self.webAction.explicit_wait("default_name_number_search")
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            log.mjLog.LogReporter("DefaultPanel", "debug", "search_people_or_extension - Clicked on search button")
            self.webAction.input_text("default_search_input", searchItem)
            searchItem = searchItem + "_ "
            self.webAction.input_text("default_search_input", searchItem)
            self.webAction.input_text("default_search_input", searchItem)
            searchResultsList = self._browser.elements_finder("peoples_panel_customer_name")

            if len(searchResultsList) == 0:
                log.mjLog.LogReporter("DefaultPanel", "info", "search_people_or_extension - No contact found!")
                raise
            else:
                log.mjLog.LogReporter("DefaultPanel", "info", "search_people_or_extension - contacts found")
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "search_people_or_extension-Error while searching people" + str(sys.exc_info()))
            raise
