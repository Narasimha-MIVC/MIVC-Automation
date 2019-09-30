## Module: Settings
## File name: Settings.py
## Description: This class contains APIs for Settings Window
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 05 MAY 2017  UKumar             Initial Version
###############################################################################

# Python Modules
import sys
import os
import time
import re

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class Settings:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def configure_outlook_options(self, params):
        """
        Author: Uttam
        configure_outlook_options() : To configure various options under contacts in Outlook tab
        Parameter: present
        """
        try:
            if "donot_open_outlook" in params.keys():
                if params["donot_open_outlook"].lower() == "check":
                    self.webAction.select_checkbox("PR_outlook_donot_open_outlook")
                    self.assertElement.element_should_be_selected("PR_outlook_donot_open_outlook")
                    log.mjLog.LogReporter("Settings", "info", "configure_outlook_options"
                        " - 'Do not open Outlook when adding contact to Connect' checkbox is checked")
                else:
                    self.webAction.unselect_checkbox("PR_outlook_donot_open_outlook")
                    self.assertElement.element_should_not_be_selected("PR_outlook_donot_open_outlook")
                    log.mjLog.LogReporter("Settings", "info", "configure_outlook_options"
                        " - 'Do not open Outlook when adding contact to Connect' checkbox is unchecked")
        except:
            log.mjLog.LogReporter("Settings", "error", "configure_outlook_options"
                                  " - Failed to set contacts options "+str(sys.exc_info()))
            raise

    def add_canned_message_whitespaces(self, message):
        '''
        Author: Upendra modified by Uttam (12-AUG-2015)
        add_canned_message_whitespaces() - To add a blank-space and canned message with white spaces  
        Parameters : message
        '''
        try:
            log.mjLog.LogReporter("Settings", "info", "add_canned_message_whitespaces"
                                                          " - To add a canned message")
            # self.webAction.explicit_wait("preferences_im")
            #self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            time.sleep(2)
            self.webAction.click_element("preferences_im")
            time.sleep(2)
            if message == "blankspace" or message == "blank":
                messageListBefore = self._browser.elements_finder("preferences_response_list")
                numberOfMsgBeforeAddition = len(messageListBefore)
                self.webAction.input_text("preferences_input_canned_response", " ")
                self.webAction.click_element("preferences_add_canned_response_button")
                messageListAfter = self._browser.elements_finder("preferences_response_list")
                numberOfMsgAfterAddition = len(messageListAfter)
                if numberOfMsgBeforeAddition == numberOfMsgAfterAddition:
                    log.mjLog.LogReporter("Settings", "info", "add_canned_message_whitespaces"
                                                                  " - no message added")
            else:
                self.webAction.clear_input_text("preferences_input_canned_response")
                # commented below block because of functionality change
                # if (self.queryElement.element_enabled("preferences_add_canned_response_button")):
                # raise AssertionError("Settings","error","Enabled")

                message = "    " + str(message) + "    "
                # self.webAction.explicit_wait("preferences_input_canned_response")
                self.webAction.input_text("preferences_input_canned_response", message)
                # self.webAction.explicit_wait("preferences_add_canned_response_button")
                self.webAction.click_element("preferences_add_canned_response_button")
                time.sleep(3)
                messageList = self._browser.elements_finder("preferences_response_list")
                for msg in messageList:
                    can_message = msg.text
                    print("Length of the message after adding in canned messages is ", len(can_message))
                    log.mjLog.LogReporter("Settings", "info", "add_canned_message_whitespaces "
                                                                  "- White spaces have been removed before adding")
                    break

                message = message.strip()
                self.assertElement.page_should_contain_text(message)
                log.mjLog.LogReporter("Settings", "info", "add_canned_message_whitespaces - message added")
        except:
            log.mjLog.LogReporter("Settings", "error", "add_canned_message_whitespaces - "
                                "Failed to add canned message with white spaces " + str(sys.exc_info()))
            raise

    def add_canned_message_without_option(self, message):
        '''
           Author: Vishwas
           add_canned_message() - To add a canned message in IM tab

        '''
        try:
            log.mjLog.LogReporter("Settings", "info", "add_canned_message - To add a canned message")
            self.webAction.click_element("preferences_im")
            self.webAction.explicit_wait("preferences_input_canned_response")
            self.webAction.input_text("preferences_input_canned_response", message)
            self.webAction.explicit_wait("preferences_add_canned_button")
            self.webAction.click_element("preferences_add_canned_button")
            time.sleep(2)
            self.assertElement.page_should_contain_text(message)

            # Commented because of rework
            # canned_response=self.queryElement.get_text("preferences_latest_canned_response")
            # if(canned_response==message):
            #    log.mjLog.LogReporter("Settings","info","add_canned_message- canned response added is at the top of the list")
            # else:
            #    raise AssertionError("canned response added is not listed at the top")
            log.mjLog.LogReporter("Settings", "info", "add_canned_message- message added")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "add_canned_message- Failed to add canned message" + str(sys.exc_info()))
            raise AssertionError("Settings", "error", "Error while adding canned message")
            
    def click_preference_call_routing(self):
        """
        click_preference_call_routing() - This method clicks on preferences call routing button
        """
        try:
            #self.webAction.click_element("preferences_notifications") 
            time.sleep(4)
            self.webAction.click_element("preferences_call_routing")
            log.mjLog.LogReporter("Settings","info","click_preference_call_routing - call routing button clicked")
        except:
            log.mjLog.LogReporter("Settings","error","click_preference_call_routing - error while clicking call routing button "+str(sys.exc_info()))
            raise

    def verify_preferences_call_routing(self):
        """
        verify_preferences_call_routing() - This method verifies all the elements in call routing preferences window
        """
        try:
            self.assertElement.element_should_be_displayed("preferences_availability_routing")
            self.assertElement.element_should_be_displayed("preferences_power_routing")
            log.mjLog.LogReporter("Settings","info","verify_preferences_call_routing - verified call routing page elements")
        except:
            log.mjLog.LogReporter("Settings","error","verify_preferences_call_routing - error while verifying call routing page elements "+str(sys.exc_info()))
            raise AssertionError("Failed to verify Call Routing page")
    
    def verify_preferences_power_routing(self):
        """
        Author : Ankit modified by manoj, modified by Uttam
        verify_preferences_power_routing() - This method verifies all the elements in call routing preferences window
        """
        try:
            time.sleep(3)
            self.webAction.click_element("preferences_power_routing")
            self.assertElement.page_should_contain_text("My Power Rules")
            self.assertElement.page_should_contain_text("Takes effect before availability routing")
            log.mjLog.LogReporter("Settings","info","verify_preferences_power_routing - verified power routing page elements")
        except:
            log.mjLog.LogReporter("Settings","error","verify_preferences_power_routing - error while verifying power routing page elements "+str(sys.exc_info()))
            raise
            
    def click_create_new_power_rule(self):
        """
        click_create_new_power_rule() - This method clicks on new power rule
        """
        try:
            log.mjLog.LogReporter("Settings","info","click_create_new_power_rule - clicked on create new power rule")
            time.sleep(5)
            self.webAction.click_element("preferences_create_power_rule")
            #time.sleep(5)
            log.mjLog.LogReporter("Settings","info","click_create_new_power_rule - clicked on create new power rule")
        except:
            log.mjLog.LogReporter("Settings","error","click_create_new_power_rule - Failed to click on create new power rule "+str(sys.exc_info()))
            raise
    
    def enter_rule_name(self,ruleName):
        """
        enter_rule_name() - Enter a rule name
        """
        try:
            log.mjLog.LogReporter("Settings","info","enter_rule_name -Going to write Rule-name")
            time.sleep(3)
            self.webAction.click_element("preferences_power_routing_rule")
            time.sleep(3)
            self.webAction.input_text("preferences_power_routing_rule",ruleName)
            log.mjLog.LogReporter("Settings","info","enter_rule_name - Rule name entered successfully")
        except:
            log.mjLog.LogReporter("Settings","error","enter_rule_name - Failed to enter a rule name "+str(sys.exc_info()))	
            raise AssertionError("error while typing a rule name")    
        
    def click_number_matches(self):
        """
        click_number_matches() - This method clicks on number matches
        """
        try:
            self.webAction.click_element("preferences_number_matches")
            log.mjLog.LogReporter("Settings","info","click_number_matches - clicked on number matches")
        except:
            log.mjLog.LogReporter("Settings","error","click_number_matches - Failed to click on number matches "+str(sys.exc_info()))
            raise
            
    def click_my_availabilty(self):
        """
        click_my_availabilty() - This method clicks on my availabilty option in power routing
        """
        try:
            self.webAction.click_element("preferences_power_routing_availability_button")
            log.mjLog.LogReporter("Settings","info","click_my_availabilty - clicked on my availability option")
        except:
            log.mjLog.LogReporter("Settings","error","click_my_availabilty - Failed to click on my availability "+str(sys.exc_info()))
            raise

    def click_on_the_phone(self):
        """
        click_on_the_phone() - This method clicks on (on the phone) option in power routing
        """
        try:
            self.webAction.click_element("preferences_on_phone_button")
            log.mjLog.LogReporter("Settings", "info", "click_on_the_phone - clicked on (on the phone) option")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "click_on_the_phone - Failed to click on (on the phone) " + str(sys.exc_info()))
            raise
            
    def click_forward_call_button(self):
        """
        click_forward_call_button() - This method clicks on forward call button
        """
        try:
            log.mjLog.LogReporter("Settings","info","click_forward_call_button - clicked on forward call button")
            time.sleep(5)
            self.webAction.click_element("preferences_callRouting_PR_forword")
            log.mjLog.LogReporter("Settings","info","click_forward_call_button - clicked on forward call button")
        except:
            log.mjLog.LogReporter("Settings","error","click_forward_call_button - Failed to click on forward call button "+str(sys.exc_info()))
            raise

    def choose_forward_call(self, option, ringtone=''):
        """
        Author: Uttam
        choose_forward_call() - This method chooses the options for forwording call
        Parameters: option,  ringtone
        """
        try:
            self.webAction.select_radio_button("preferences_callRouting_PR_forward_radioDrop")
            self.webAction.select_from_dropdown_using_text("preferences_callRouting_PR_forward_dropdown",\
                                                               option)
            if option == "play ringtone":
                self.webAction.select_from_dropdown_using_text("preferences_callRouting_PR_forward_radioDrop_playRing",\
                                                               ringtone)
                log.mjLog.LogReporter("Settings","info","choose_forward_call -"
                                      " ringtone "+ringtone+" is selected")
            log.mjLog.LogReporter("Settings","info","choose_forward_call -"
                                  " "+option+" is selected")
        except:
            log.mjLog.LogReporter("Settings","error","choose_forward_call - "
                                  "Failed to select option "+str(sys.exc_info()))
            raise
    
    def add_user_forward_callto(self, params):
        '''
           Author : Prashanth
           verify the user firstname,extension,Double click on contact which is autosuggested
           parameter = searchItem
        '''
        try:
            
            self.webAction.select_radio_button("preferences_callRouting_PR_forward_radioText")
            if not self.queryElement.element_not_displayed("preferences_callRouting_PR_forward_text_rem"):
                self.webAction.click_element("preferences_callRouting_PR_forward_text_rem")
            
                       
            self.webAction.input_text("preferences_callRouting_PR_forward_text",\
                                      params["optionOrText"])
                                      
            time.sleep(3)
            
            firstNameList=self._browser.elements_finder("pref_BR_incCall_DDFCT_usrList")
            '''for names in firstNameList:
                fullname = names.text.split("\n")[0]
                exter = names.text.split("\n")[1]'''            
        
            firstNames = []
            for key in params.keys():
                if "firstName" in key:
                    firstNames.append(params[key])
            for t in firstNames:
                print("first Names: ", t)
        
            extensions = []
            for key in params.keys():
                if "extension" in key:
                    extensions.append(params[key])
                    
            for i in extensions:
                print("extensions: ", i)
            
            externals = []
            for key in params.keys():
                if "external" in key:
                    extensions.append(params[key])
            for j in extensions:
                print("extensions: ", j)
            
            
            #code for checking the name ,extension,external & selecting the user                   
            if params["type"] == "name":    
                for name in firstNames:
                    print("names inside test to check: " )
                    for names in firstNameList:
                        fullname = names.text.split("\n")[0]
                        exter = names.text.split("\n")[1]
                        #print ("names appearing in UI :" )
                        print("full name is :" + fullname)
                        Name = re.sub('\#',' ',name)
                        print("Name is :" + Name)
                        if (fullname == Name):
                            print("inside last name loop:")
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - user is verified - done")
                            break
                              
                        
                for external in externals:
                    print("first external inside loop : ")
                    for names in firstNameList:
                        fullname = names.text.split("\n")[0]
                        exter = names.text.split("\n")[1]
                        print ("Inside for Loop of external :")
                        if (exter == external):
                            print("inside external loop:")
                            time.sleep(3)
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - External number is verified - done")
                            break        
                
                for extension in extensions:
                    print("first extension inside loop : ")
                    for names in firstNameList:
                        fullname = names.text.split("\n")[0]
                        exter = names.text.split("\n")[1]
                        print("exter is : ",exter)
                        #print ("Inside for Loop of extension :")
                        if (exter == extension):
                            print("inside extension loop:")
                            time.sleep(3)
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - Extension number is verified - done")
                            break
                               
                for names in firstNameList:
                    fullname = names.text.split("\n")[0]
                    exter = names.text.split("\n")[1]
                    Name = re.sub('\#',' ',params["nameToAdd"])
                    if (fullname == Name ):
                        names.click()
                        time.sleep(3)
                        break
                
            #code for checking the external number,user & selecting the external                       
            elif params["type"] == "external":
                for external in externals:
                    print("first external inside loop : ")
                    for names in firstNameList:
                        fullname = names.text.split("\n")[0]
                        exter = names.text.split("\n")[1]
                        print ("Inside for Loop of external :")
                        if (exter == external):
                            print("inside external loop:")
                            time.sleep(3)
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - External number is verified - done")
                            break
                for name in firstNames:
                    print("names inside test to check: ")    
                    for names in firstNameList:
                        fullname = names.text.split("\n")[0]
                        exter = names.text.split("\n")[1]
                        print ("names appearing in UI :")
                        print("full name is :" + fullname)
                        Name = re.sub('\#',' ',name)
                        print("Name is :" + Name)
                        if (fullname == Name):
                            print("inside last name loop:")
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - user is verified - done")
                            break        
                            
                for names in firstNameList:
                    fullname = names.text.split("\n")[0]
                    exter = names.text.split("\n")[1]
                    if (exter == params["externalToAdd"]):
                        names.click()
                        time.sleep(3)
                        break

            #code for checking the extension,user & selecting the extension    
            elif params["type"] == "extension":
                for extension in extensions:
                    print("first extension inside loop : ")
                    for names in firstNameList:
                        print("names",names)
                        fullname = names.text.split("\n")[0]
                        print("fullname:",fullname)
                        exter = names.text.split("\n")[1]
                        print("exter",exter)
                        print ("Inside for Loop of extension :")
                        if (exter == extension):
                            print("inside extension loop:")
                            time.sleep(3)
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - Extension number is verified - done")
                            break
                for name in firstNames:
                    print("names inside test to check: ")    
                    for names in firstNameList:
                        fullname = names.text.split("\n")[0]
                        exter = names.text.split("\n")[1]
                        print ("names appearing in UI :")
                        print("full name is :" + fullname)
                        Name = re.sub('\#',' ',name)
                        print("Name is :" + Name)
                        if (fullname == Name):
                            print("inside last name loop:")
                            log.mjLog.LogReporter("Settings", "info","add_user_forward_callto - user is verified - done")
                            break         
                
                for names in firstNameList:
                    fullname = names.text.split("\n")[0]
                    exter = names.text.split("\n")[1]
                    if (exter == params["extensionToAdd"]):
                        names.click()
                        time.sleep(3)
                        break
            
            
            elif params["type"] == "none" :
                print("No type")
                self.webAction.click_element("preferences_callRouting_PR_forward_text")
                #break
                    
        except:
            log.mjLog.LogReporter("Settings","error","add_user_forward_callto- Error while clicking "+str(sys.exc_info()))
            raise AssertionError("failed to configure Forward call to option")
            
    def add_my_availabilty(self,text):
        """
        add_my_availabilty() - Add my availability details
        """
        try:
            if (text=="available"):
                self.webAction.click_element("preferences_power_routing_available")
            elif (text=="inameeting"):
                self.webAction.click_element("preferences_power_routing_inameeting")
            elif (text=="outofoffice"):
                self.webAction.click_element("preferences_power_routing_outofoffice")
            elif (text=="vacation"):
                self.webAction.click_element("preferences_power_routing_vacation")
            elif (text=="variable"):
                self.webAction.click_element("preferences_power_routing_variable")
            elif (text=="dnd"):
                self.webAction.click_element("preferences_power_routing_dnd")
            else:
                raise AssertionError("parameter not allowed !!!")
            log.mjLog.LogReporter("Settings","info","add_my_availabilty - Added my availabilty details ")
        except:
            log.mjLog.LogReporter("Settings","error","add_my_availabilty - Failed to add my availabilty details "+str(sys.exc_info()))
            raise

    def click_number_matches(self):
        """
        click_number_matches() - This method clicks on number matches
        """
        try:
            self.webAction.click_element("preferences_number_matches")
            log.mjLog.LogReporter("Settings", "info", "click_number_matches - clicked on number matches")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "click_number_matches - Failed to click on number matches " + str(sys.exc_info()))
            raise

    def add_number_matches(self, opt, name, number, text):
        """
        Author: Gautham modified by Uttam
        add_number_matches() - Add number details on number matches
        Parameters: opt and text
        Ex: add_number_matches opt=0 text=234
        """
        try:
            # self.webAction.click_element("preferences_number_matches_arrow")
            # match_list=self._browser.elements_finder("preferences_number_matches_drop_down")
            # opt=int(opt)
            # match_list[opt].click()
            number_dict = {"0": "The number is", "1": "The number is any internal number",
                           "2": "The number is an internal extension starting with",
                           "3": "The number is any external number",
                           "4": "The number is an external number starting with",
                           "5": "The number is private", "6": "The number is out of area/unknown"}
            self.webAction.select_from_dropdown_using_text("preferences_number_matches_drop_down", number_dict[opt])
            if opt == "0" or opt == "2" or opt == "3" or opt == "4":

                self.webAction.explicit_wait("preferences_number_matches_input_text")
                self.webAction.input_text("preferences_number_matches_input_text", text)

                time.sleep(2)
                if self.queryElement.element_not_displayed("pref_number_matches_input_suggesList"):
                    log.mjLog.LogReporter("Settings", "info", "add_number_matches - NO user is "
                                                                 "coming up as a match")
                else:
                    if name != ' ' and number != '':
                        numbersList = self._browser.elements_finder("pref_number_matches_input_suggesList_numbers")
                        formattedNumber = "(" + number[0:3] + ") " + number[3:6] + "-" + number[6:len(number)]
                        for self.number in numbersList:
                            if formattedNumber in self.number.text:
                                self.number.click()
                                break
                        log.mjLog.LogReporter("Settings", "info", "add_number_matches - Added number"
                                                                     " details on number matches")
                    elif name == ' ' and number == '':
                        log.mjLog.LogReporter("Settings", "info", "add_number_matches - Added number %s" % (text))
                    elif name != '' and number == '':
                        usersList = self._browser.elements_finder("pref_number_matches_input_suggesList_names")
                        for user in usersList:
                            if name in user.text:
                                user.click()
                                log.mjLog.LogReporter("Settings", "info", "add_number_matches - Added number"
                                                                             " details on number matches based on first name and last name")
                                break
                            else:
                                log.mjLog.LogReporter("Settings", "info", "add_number_matches - User not found")
                    else:
                        numbersList = self._browser.elements_finder("pref_number_matches_input_suggesList_numbers")
                        for self.number in numbersList:
                            if number in self.number.text:
                                log.mjLog.LogReporter("Settings", "info", "add_number_matches - %s is "
                                                                             "coming up as a match" % (number))
                                break
        except:
            log.mjLog.LogReporter("Settings", "error", "add_number_matches - Failed to add "
                                                          "number details " + str(sys.exc_info()))
            raise

    def click_on_edit_rule(self, ruleName):
        """
        click_on_edit_rule() - This method clicks on edit rule in power routing
        """
        try:
            log.mjLog.LogReporter("Settings", "info", "click_on_edit_rule - Entered clicked on edit rule")
            rule_list = self._browser.elements_finder("preferences_rule_name")
            edit_list = self._browser.elements_finder("preferences_edit_rule")
            log.mjLog.LogReporter("Settings", "info", "click_on_edit_rule - rule list")
            for rule in rule_list:
                str = rule.text
                str_list = str.split('\n')
                if str_list[0] == ruleName:
                    position = rule_list.index(rule)
            edit_list[position].click()
            log.mjLog.LogReporter("Settings", "info", "click_on_edit_rule - clicked on edit rule")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "click_on_edit_rule - Failed to click on edit rule " + str(sys.exc_info()))
            raise
            
    def check_rule_error(self, tabName):
        """
        author:uttam
        check_rule_error() - This method checks the errors occured during creation of rules
        parameters: tabName (name of the part under which you want to check the error)
        """
        try:
            if tabName == "timeisDay":
                status = self.queryElement.element_not_displayed("preferences_callR_PR_time_timeError")
                if status is True:
                    log.mjLog.LogReporter("Settings","info","check_rule_error -"
                                          " No error in creating rule")
                else:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "'One of the Day must be selected' error is there")
            elif tabName == "noCondition":
                status = self.queryElement.element_not_displayed("preferences_callR_PR_condiotionError")
                if status is True:
                    log.mjLog.LogReporter("Settings","info","check_rule_error -"
                                          " No error in creating rule")
                else:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "'Missing conditions for this rule' error is there")
            elif tabName == "timeisTime":
                status = self.queryElement.element_not_displayed("preferences_callR_PR_time_timeError")
                if status is False:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "'The from time must be before the to time' error is there")
            elif tabName == "my_availability":
                status = self.queryElement.element_not_displayed("preferences_callR_PR_mayAvailError")
                if status is False:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "'You must select atleast one availability state' error is there")
            elif tabName == "forward_call_to":
                status = self.queryElement.element_not_displayed("preferences_callRouting_PR_forwardError")
                if status is False:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "'You are not allowed to forward call' error is there")
            elif tabName == "number_matches":
                status = self.queryElement.element_not_displayed("preferences_number_matches_error")
                if status is False:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "'Invalid Number' error is there")
            else:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
                status = self.queryElement.element_not_displayed("preferences_power_routing_rule_err")
                print(status)
                if status is False:
                    log.mjLog.LogReporter("Settings","info","check_rule_error - "
                                          "error is there, check your rule name")
        except:
            log.mjLog.LogReporter("Settings","error","check_rule_error - Failed to"
                                  " create rule "+str(sys.exc_info()))
            raise

    def save_rule(self):
        """
        save_rule() - Save the rule
        """
        try:
            self.webAction.click_element("preferences_edit_save_rule")
            log.mjLog.LogReporter("Settings", "info", "save_rule - Clicked on save rule button ")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "save_rule - Failed to click on save rule button " + str(sys.exc_info()))
            raise
            
    def remove_rule_option(self,option):
        """
        remove_rule_option() - This method removes an option from the rule
        """
        try:
            if option=="number_matches":
                self.webAction.click_element("preferences_number_matches_remove_button")
            elif option=="dialed_number":
                self.webAction.click_element("preferences_dialled_number_remove_button")
            elif option=="my_availability":
                self.webAction.click_element("preferences_power_routing_availability_remove_button")
            elif option=="on_the_phone":
                self.webAction.click_element("preferences_on_phone_remove_button")
            elif option=="time_is":
                self.webAction.click_element("preferences_time_is_remove_button")
            else:
                raise AssertionError("wrong arguments passed")
            log.mjLog.LogReporter("Settings","info","remove_rule_option - An option is removed from the rule")
        except:
            log.mjLog.LogReporter("Settings","error","remove_rule_option - Failed to remove an option from thhe rule "+str(sys.exc_info()))
            raise
            
    def check_incoming_IM(self,check):
        """
        check_incoming_IM() - To check if IM notification check box is selected or unselected
        """
        try:
            option=self.webAction.check_checkbox("preferences_notifications_incoming_im")
            if check=="positive":
                if option:
                    log.mjLog.LogReporter("Settings","info","check_incoming_IM - Incoming IM notification option is selected")
                else:
                    raise AssertionError("Settings","error","check_incoming_IM - Incoming IM notification option is unselected")
            elif check=="negative":
                if not option:
                    log.mjLog.LogReporter("Settings","info","check_incoming_IM - Incoming IM notification option is unselected")
                else:
                    raise AssertionError("Settings","error","check_incoming_IM - Incoming IM notification option is selected")
            else:
                raise AssertionError("Wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("Settings","error","check_incoming_IM - Failed to check popup notification options"+str(sys.exc_info()))
            raise

    def check_incoming_voiceMail(self,check):
        """
        check_incoming_voiceMail() - To check if voice mail notification check box is selected or unselected
        """
        try:
            option=self.webAction.check_checkbox("preferences_notifications_incoming_voicemail")
            if check=="positive":
                if option:
                    log.mjLog.LogReporter("Settings","info","check_incoming_voiceMail - Incoming voice mail check box is selected")
                else:
                    raise AssertionError("Settings","error","check_incoming_voiceMail - Incoming voice mail check box is unselected")
            elif check=="negative":
                if not option:
                    log.mjLog.LogReporter("Settings","info","check_incoming_voiceMail - Incoming voice mail check box is unselected")
                else:
                    raise AssertionError("Settings","error","check_incoming_voiceMail - Incoming voice mail check box is selected")
            else:
                raise AssertionError("Wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("Settings","error","check_incoming_voiceMail - Failed to check popup notification options"+str(sys.exc_info()))
            raise
            
    def check_uncheck_incoming_IM(self,check):
        """
        check_uncheck_incoming_IM() - This method select or unselect incoming IM notification 
                                      option under Notifications
        change list: second if condition added inside if check=="true" (UKumar: 27-July-2016) 
        """
        try:
            if check=="true":
                if not self.queryElement.verify_checkbox("preferences_notifications_incoming_im"):
                    self.webAction.select_checkbox("preferences_notifications_incoming_im")
                if not self.queryElement.verify_checkbox("preferences_notifications_show_im_content"):
                    self.webAction.select_checkbox("preferences_notifications_show_im_content")
                    log.mjLog.LogReporter("Settings", "info", "check_uncheck_incoming_IM "
                                          "- Incoming IM selected")
            elif check=="false":
                self.webAction.unselect_checkbox("preferences_notifications_incoming_im")
                log.mjLog.LogReporter("Settings", "info", "check_uncheck_incoming_IM "
                                      "- Incoming IM unselected")
            else:
                raise AssertionError("Wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("Settings", "error", "check_uncheck_incoming_IM "
                                  "- Failed to click on incoming IM "+str(sys.exc_info()))
            raise

    def check_uncheck_incoming_voiceMail(self,check):
        """
        check_uncheck_incoming_voiceMail() - This method select or unselect incoming Voice Mail notification 
                                            option under Notifications
        """
        try:
            if check=="true":
                self.webAction.select_checkbox("preferences_notifications_incoming_voicemail")
                log.mjLog.LogReporter("Settings","info","check_uncheck_incoming_voiceMail - Incoming Voice Mail selected")
            elif check=="false":
                self.webAction.unselect_checkbox("preferences_notifications_incoming_voicemail")
                log.mjLog.LogReporter("Settings","info","check_uncheck_incoming_voiceMail - Incoming Voice Mail unselected")
            else:
                raise AssertionError("Wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("Settings","error","check_uncheck_incoming_voiceMail - Failed to click on incoming Voice Mail "+str(sys.exc_info()))
            raise
            
    def click_notifications_tab(self):
        """
        click_notifications_tab() - This method clicks on notifications tab
        """
        try:
            self.webAction.click_element("preferences_notifications")
            log.mjLog.LogReporter("Settings","info","click_notifications_tab - clicked on notifications tab")
        except:
            log.mjLog.LogReporter("Settings","error","click_notifications_tab - Failed to click on notifications tab "+str(sys.exc_info()))
            raise

    def click_notifications_popup(self):
        """
        click_notifications_popup() - This method clicks on popup tab under notifications
        """
        try:
            self.webAction.click_element("preferences_notifications_popup")
            log.mjLog.LogReporter("Settings","info","click_notifications_popup - clicked on popup tab")
        except:
            log.mjLog.LogReporter("Settings","error","click_notifications_popup - Failed to click on popup tab "+str(sys.exc_info()))
            raise
            
    def check_uncheck_close_contact_card(self,params):
        '''
           Author : Prashanth
           check_uncheck_close_contact_card()-Check/uncheck close contact card checkbox
           parameter: option
           ex: check_uncheck_close_contact_card
        '''
        try:
            if "click" in params.keys():
                log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Checking/unchecking close contact card")
                self.webAction.explicit_wait("preferences_telephony")
                self.webAction.click_element("preferences_telephony")
                print("###########telephony tab opened#############")
                self.webAction.explicit_wait("preferences_close_contact")
                time.sleep(2)
                self.assertElement.element_should_be_displayed("preferences_close_contact")
                self.assertElement.page_should_contain_text("Close contact card after call ends")
                print("#########verified the close contact card##########")
                
                if "tabcheck" in params.keys():    
                    print("#######entered tabcheck#####")
                    self.webAction.explicit_wait("preferences_notifications")
                    print("########notification presenet###########")
                    self.webAction.click_element("preferences_notifications")
                    print("########clicked on notification###########")
                    
                    time.sleep(2)
                    
                    self.webAction.click_element("preferences_telephony1")
                    print("########clicked on telephony from notifications###########")
                    self.webAction.explicit_wait("preferences_close_contact")
                    time.sleep(2)
                    self.assertElement.element_should_be_displayed("preferences_close_contact")
                    self.assertElement.page_should_contain_text("Close contact card after call ends")
                
                if params["option"] == "check":
                    self.webAction.select_checkbox("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card-Close contact card is checked as expected")
                
                elif params["option"] == "uncheck":
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- trying to unselect checkbox")
                    self.webAction.unselect_checkbox("preferences_close_contact")
                    #self.webAction.click_element("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Close contact card option is unchecked")
                
                elif params["option"] == "checked":
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- trying to verify whether box is checked")
                    #self.assertElement.element_should_be_selected("preferences_close_contact")
                    if self.queryElement.verify_checkbox("preferences_close_contact") is False:
                        print("********** Entered in to If loop false*******")
                        self.webAction.click_element("preferences_close_contact")
                        time.sleep(5)
                    #self.assertElement.element_should_be_selected("preferences_close_contact")
                    print("****************this is Sury************")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Close contact card is checked")
                
                elif params["option"] == "unchecked":
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- trying to verify whether box is checked")
                    self.assertElement.element_should_not_be_selected("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Close contact card is checked")
                
                else:
                    raise AssertionError("Wrong argument passed")
                    
                    
            else:
                if params["option"] == "check":
                    self.webAction.select_checkbox("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card-Close contact card is checked as expected")
                
                if params["option"] == "uncheck":
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- trying to unselect checkbox")
                    self.assertElement.page_should_contain_text("Close contact card after call ends")
                    print("#########Entered without click loop##########")
                    self.assertElement.element_should_be_displayed("preferences_close_contact")
                    self.webAction.unselect_checkbox("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Close contact card option is unchecked")
                
                elif params["option"] == "checked":
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- trying to verify whether box is checked")
                    self.assertElement.element_should_be_selected("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Close contact card is checked")
                
                elif params["option"] == "unchecked":
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- trying to verify whether box is checked")
                    self.assertElement.element_should_not_be_selected("preferences_close_contact")
                    log.mjLog.LogReporter("Settings","info","check_uncheck_close_contact_card- Close contact card is checked")
                
                else:
                    raise AssertionError("Wrong argument passed")
            
            if "close" in params.keys():
                print("############entered  close if###############")
                self.webAction.click_element("preferences_close_window")
                print("############window closed###############")
            
        except:
            log.mjLog.LogReporter("Settings","error","check_uncheck_close_contact_card- Failed"+str(sys.exc_info()))
            raise
            
    def set_Forevent_sounds(self,eventName):
        """
        Author: Uttam
        set_Forevent_sounds() - This method selects an event identified
                                by eventName from 'For event' drop down
        Parameter: eventName
        Extra Info.: instead of actual event name you have to pass number for events
                     1 for new voicemail, 2 for call from an internal number 
        """
        try:
            event_name = {"1":"new voicemail", "2":"call from an internal number",
                          "3":"call from an external number",
                          "4":"new IM message initiating a new conversation",
                          "5":"new IM message initiating an existing conversation",
                          "6":"monitored call",
                          "7":"shared line all"}
            self.webAction.select_from_dropdown_using_text("preferences_notif_sounds_forEveDD",\
                                                           event_name[eventName])
            log.mjLog.LogReporter("Settings","info","set_Forevent_sounds - event"
                                  " "+event_name[eventName]+" is selected")
        except:
            log.mjLog.LogReporter("Settings","error","set_Forevent_sounds - "
                                  "failed to select event "+str(sys.exc_info()))
            raise
            
    def configure_alert_sound(self, params):
        """
        Author: Uttam
        configure_alert_sound() - This method selects audio alert ON or OFF
                                and selects sound for Audio Alert ON
        Parameter: alert and alertSound 
        """
        try:
            if params["alert"]=="off":
                self.webAction.click_element("preferences_notif_sounds_NAA_radio")
            else:
                self.webAction.click_element("preferences_notif_sounds_PA_radio")
             
            if "alertSound" in params.keys():
                self.webAction.select_from_dropdown_using_text("preferences_notif_sounds_soundsDD",\
                                                               params["alertSound"])
                log.mjLog.LogReporter("Settings","info","configure_alert_sound - '%s' selected" %params["alertSound"])
        except:
            log.mjLog.LogReporter("Settings","error","configure_alert_sound - "
                                  "failed to select event "+str(sys.exc_info()))
            raise
            
    def verify_entity_notify(self, tabName):
        """
        author:uttam
        verify_entity_notify() - This method clicks on the tab identified by 'tabName'
                                and verifies the entities present under that tab
        parameter : tabName
        """
        try:
            if tabName == "Voicemail":
                self.webAction.click_element("preferences_notifications_voicemail")
                self.assertElement.element_should_be_displayed("preferences_notif_voicemail_notifyWin")
                log.mjLog.LogReporter("Settings", "info", "verify_entity_notify - Voicemail tab clicked")
            elif tabName == "Sounds":
                self.webAction.click_element("preferences_notifications_sounds")
                self.assertElement.element_should_be_displayed("preferences_notif_sounds_window")
                log.mjLog.LogReporter("Settings", "info", "verify_entity_notify - Sounds tab clicked")
            else:
                self.webAction.click_element("preferences_notifications_popup")
                self.assertElement.element_should_be_displayed("preferences_notifications_incoming_im")
                self.assertElement.element_should_be_displayed("preferences_notifications_incoming_voicemail")
                log.mjLog.LogReporter("Settings", "info", "verify_entity_notify - Popup tab clicked")
        except:
            log.mjLog.LogReporter("Settings", "error", "verify_entity_notify - unable"
                                  " to click on tab "+tabName+" "+str(sys.exc_info()))
            raise
            
    def add_user_to_blocked_list(self, usernames):
        """
        add_user_to_blocked_list() - This method types the username in the contactbox
                                     and clicks on the popup appeared for username typed
                                     to add the user to blocked list
        parameters: usernames (list of usernames)
        """
        try:
            self.webAction.click_element("preferences_IM_BlockNotif_contact")
            for username in usernames:
                userlist = self._browser.elements_finder("third_panel_blocklist_name")
                if len(userlist) == 0:
                    log.mjLog.LogReporter("Settings","info","add_user_to_blocked_list - user is not blocked")
                    self.webAction.input_text("preferences_IM_BlockNotif_contact", username)
                    time.sleep(3)
                    self.webAction.click_element("preferences_IM_BlockNotif_contact_suggesstion")
                    time.sleep(5)
                    self.webAction.click_element("preferences_IM_BlockNotif_contact")
                    self.webAction.click_element("preferences_notifications")
                    self.webAction.click_element("preferences_im")
                    time.sleep(3)
                    self.webAction.click_element("preferences_IM_BlockNotif")
                    time.sleep(2)
                    log.mjLog.LogReporter("Settings", "info", "add_user_to_blocked_list - user"
                              " selected from suggestion list")
                else:
                    name=self.queryElement.get_text("third_panel_blocklist_name")
                    if name==username:
                        print("user is already blocked")
                        log.mjLog.LogReporter("Settings","info","user is already blocked")
        except:
            log.mjLog.LogReporter("Settings", "error", "add_user_to_blocked_list - error"
                                  " while selecting user from suggestion list "+str(sys.exc_info()))
            raise

    def verify_preferences_basic_routing_change_panels(self, option):
        """
        Author: manoj
        verify_basic_routing_rule_not_present() - This method verifies if  a particular basic routing rule is not present
        """
        try:
            log.mjLog.LogReporter("Settings", "info",
                                  "verify_preferences_basic_routing_change_panels -going to click on basic routing change panel")
            if (option == "simulring"):
                self.webAction.click_element("preferences_basic_change_simulring_button")
                time.sleep(1)
                self.assertElement.page_should_contain_text("Simultaneous Ring")
            elif (option == "inc_call"):
                self.webAction.click_element("preferences_basic_change_inc_call_button")
                time.sleep(1)
                self.assertElement.page_should_contain_text("Incoming Call Forwarding")
            elif (option == "find_me"):
                self.webAction.click_element("preferences_basic_change_findme_button")
                time.sleep(1)
                self.assertElement.page_should_contain_text("FindMe")
            elif (option == "vm_greeting"):
                self.webAction.click_element("preferences_basic_change_vm_greeting_button")
                time.sleep(1)
                self.assertElement.page_should_contain_text("Voicemail Greeting: Recording & Playback")
            elif (option == "interacting_greeting1"):
                self.webAction.click_element("preferences_basic_change_greeting_only_btn")
                time.sleep(1)
                self.assertElement.page_should_contain_text("Greeting Options When")
            elif (option == "interacting_greeting2"):
                self.webAction.click_element("preferences_basic_change_operator_button")
                time.sleep(1)
                self.assertElement.page_should_contain_text("Interacting with Greeting")
            else:
                raise AssertionError("Invalid option passed")
            log.mjLog.LogReporter("Settings", "info",
                                  "verify_preferences_basic_routing_change_panels - verified basic routing rule change option")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "verify_preferences_basic_routing_change_panels - Failed to verify basic routing rule change option panels " + str(
                                      sys.exc_info()))
            raise

    def close_preferences_window(self):
        '''
           Author: Gautham
           close_preferences_window() - Close preferences window opened

        '''
        try:
            log.mjLog.LogReporter("Settings", "info", "close_preferences_window- Close preferences window opened")
            self.webAction.click_element("preferences_close_window")
            log.mjLog.LogReporter("Settings", "info",
                                  "close_preferences_window- Preferences window closed successfully")
        except:
            log.mjLog.LogReporter("Settings", "error",
                                  "close_preferences_window- Failed to close preferences window" + str(sys.exc_info()))
            raise

    def check_uncheck_routing_slip(self, params):
        '''
           Author : Prashanth
           check_uncheck_routing_slip()-Check/uncheck close contact card checkbox
           parameter: option
           ex: check_uncheck_routing_slip

           change list: removed if statement (Karthik: Aug 19-2016)
        '''
        try:
            self.webAction.explicit_wait("preferences_close_contact")
            time.sleep(2)
            self.assertElement.element_should_be_displayed("preferences_close_contact")
            self.assertElement.page_should_contain_text("Close contact card after call ends")

            flag = self.queryElement.verify_checkbox("Routing_Slip_click")
            if not flag:
                self.webAction.click_element("Routing_Slip_click")

            if "tabcheck" in params.keys():
                self.webAction.explicit_wait("preferences_notifications")
                self.webAction.click_element("preferences_notifications")
                time.sleep(2)
        except:
            log.mjLog.LogReporter("Settings", "error", "check_uncheck_routing_slip"
                                                          " - Failed to check/click on routing slip " + str(
                sys.exc_info()))
            raise AssertionError("Failed to Click")

    def add_or_remove_select_number_in_findme_panel(self, params):
        """
        Author : Indresh
        add_or_remove_select_number_in_findme_panel() - adds find me numbers in Findme panel
        """
        try:
            self.webAction.click_element("pref_select_number1_in_findme")
            time.sleep(2)
            self.webAction.click_element("pref_select_number1_radio_button")
            self.webAction.explicit_wait("pref_remove_selected_number")
            self.webAction.click_element("pref_remove_selected_number")
            button_remove_final = self._browser.get_current_browser().find_element_by_xpath("//div[@id='findme-numbers-basic-section']/div[@id='findme1-input']/st-userphone/div/div/div/p/st-button/button[@id='btn_remove_final']")
            if button_remove_final.is_displayed():
                self.webAction.click_element("pref_remove_button_final")
                time.sleep(2)
                self.webAction.explicit_wait("pref_select_number1_in_findme")
                self.webAction.click_element("pref_select_number1_in_findme")
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_or_remove_select_number_in_findme_panel")
            time.sleep(2)
            self.webAction.click_element("pref_select_number1_radio_button")
            self.webAction.input_text_basic("pref_select_number1_add_label", params["labelName"])
            self.webAction.input_text_basic("pref_select_number1_add_number", params["number"])
            time.sleep(2)
            self.webAction.click_element("pref_use_selected_number_button")
            time.sleep(2)
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_or_remove_select_number_in_findme_panel"
                                                            " - added as selected number")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_or_remove_select_number_in_findme_panel"
                                                                 " - failed to click on selected number " + str(
                sys.exc_info()))
            raise        
