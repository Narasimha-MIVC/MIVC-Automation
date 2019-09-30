## Module: ThirdPanel
## File name: ThirdPanel.py
## Description: This class contains APIs related to functionality in third panel
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer                  Description
##  ---------   ---------           -----------------------
## 13 AUG 2015  UKumar@horetel.com       Initial Version
###############################################################################

# Python Modules
import sys
import os
import time
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class ThirdPanel:
    
    def __init__(self, browser):
        
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def select_routeslip_entity(self, entityName):
        """
        Author: Uttam
        select_routeslip_entity() : This method selects entity from drop down
        Parameter: entity
        Extra Info: entity could be call, voicemail, messages or everything
        """
        try:
            self.webAction.click_element("default_recent")
            self.webAction.explicit_wait("TP_History_DDArrow")
            self.webAction.click_element("TP_History_DDArrow")
            entityList = self._browser.elements_finder("TP_History_DD_Li")
            for entity in entityList :
                if entity.text == entityName:
                    entity.click()
                    log.mjLog.LogReporter("ThirdPanel", "info", "select_routeslip_entity"
                                          " - %s selected" %entityName)
                    break
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "select_routeslip_entity"
                                  " - Failed to select "+entityName+" "+str(sys.exc_info()))
            raise AssertionError("error while selecting entity")
        
    def verify_call_route_slip(self, params):
        """
        Author: Uttam
        verify_call_route_slip() - To verify call routing slip
        Parameters: when, caller, receiver and callerExtn
        Extra Info. : when could be either ongoingCall afterCall
        """
        try:
            if params["when"] == "ongoingCall":
                self.webAction.click_element("TP_CallHistory_DuringCall")
                historyValues = self._browser.elements_finder("TP_Call_History_RS")
                print(historyValues)
                for h in historyValues:
                    print("VALUESSSSSS : ", h.text)
                #self.assertElement.values_should_be_equal(params["callerExtn"], historyValues[0].text)
                self.assertElement.values_should_be_equal("Active Call", historyValues[1].text)
                print("ACTIVE CALLLLLLLLLLLLLLLLLL")
                message = params["caller"]+" called "+params["receiver"]+"."
                self.assertElement.values_should_be_equal(message, historyValues[2].text.split("\n")[0])
                print("DONEEEEEEEEEEEEEE")
                self.webAction.click_element("TP_CallHistory_DuringCall")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_call_route_slip"
                                      " - call routing slip verified during ongoing call")
            else:
                print("Inside elseggggggggggggggggggggggg")
                self.webAction.click_element("TP_CallHistory_AfterCall")
                print("CLICKEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                historyValues = self._browser.elements_finder("TP_Call_History_RS")
                for h in historyValues:
                    print("VALUESSSSSS : ", h.text)
                #self.assertElement.values_should_be_equal(params["callerExtn"], historyValues[0].text)
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_call_route_slip - "
                                      "duration of call is : %s minutes" %(historyValues[1].text))
                
                message = params["caller"]+" called "+params["receiver"]+"."
                self.assertElement.values_should_be_equal(message, historyValues[2].text.split("\n")[0])
                if params["transferType"] == "none":
                    self.assertElement.values_should_be_equal("Call disconnected.", historyValues[2].text.split("\n")[1])
                    self.assertElement.values_should_be_equal("Call terminated.", historyValues[2].text.split("\n")[2])
                elif params["transferType"] == "blind":
                    message = "Call transferred from "+params["receiver"]+" to "+params["thirdParty"]+"."
                    self.assertElement.values_should_be_equal("Call disconnected.", historyValues[2].text.split("\n")[1])
                    self.assertElement.values_should_be_equal("Call disconnected.", historyValues[2].text.split("\n")[2])
                    self.assertElement.values_should_be_equal("Call terminated.", historyValues[2].text.split("\n")[3])
                    
                self.webAction.click_element("TP_CallHistory_AfterCall")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_call_route_slip"
                                      " - call routing slip verified after call")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_call_route_slip - "
                                  "Failed to verify call routing slip "+str(sys.exc_info()))
            raise AssertionError("error while verifying call routing slip")
        
    def verify_support_info(self):
        """
        Author: Uttam
        verify_support_info() - To verify GUID information under Support Info
        Parameters: No Parameter
        """
        try:
            element = self._browser.element_finder("call outgoing-call")
            print(element)
            ActionChains(self._browser.get_current_browser()).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
            print("AGAIN clicked")
            '''self.assertElement.element_should_be_displayed("TP_Info_Label")
            self.webAction.click_element("TP_Info_Label")
            guidInfo = self.queryElement.get_text("TP_RS_GUID_Info")
            self.webAction.click_element("TP_CallHistory_AfterCall")
            log.mjLog.LogReporter("ThirdPanel", "info", "verify_support_info"
                                  " - GUID info is %s" %guidInfo)'''
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_support_info"
                                  " - Failed to verify support info. "+str(sys.exc_info()))
            raise AssertionError("error while verifying support information")
        
    def verify_vm_info(self, sender, receiverList, openContactCard):
        """
        Author: Uttam
        verify_vm_info() - This method verifies voicemail history (not forwarded)
        Parameters: sender, receiverList
        """
        try:
            self.webAction.click_element("TP_VM_History")
            self.webAction.click_element("TP_VM_History_DownArrow")
            participantList = self._browser.elements_finder("TP_VM_History_Users")
            print("Asender an dreceiver  : ", sender, receiverList[0])
            for a in participantList:
                print("Values sre : ", a.text)
            
            length = len(receiverList)
            for receiver in receiverList:
                    for i in range(0, length):
                        if receiver==participantList[i].text:
                            log.mjLog.LogReporter("ThirdPanel", "info", "verify_vm_info"
                                                  " - recipient %s is present" %receiver)
                            
            self.assertElement.values_should_be_equal(sender, participantList[length].text)
            log.mjLog.LogReporter("ThirdPanel", "info", "verify_vm_info - sender"
                                  " is %s" %sender)
            if openContactCard != 'no':
                for participant in participantList:
                    if participant.text==openContactCard:
                        x = self._browser.get_current_browser()
                        ActionChains(x).double_click(participant).perform()
                        break
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_vm_info - Failed"
                                  " to verify VM information "+str(sys.exc_info()))
            raise AssertionError("error while verifying VM information")
			
    def verify_forwarded_vm_info(self, forward, sender, receiverList, forwardedToList, openContactCard):
        """
        Author: Uttam
        verify_forwarded_vm_info() - This method verifies voicemail history
        Parameters: forward, senderList, receiver and forwardedTo
        """
        try:
            self.webAction.click_element("TP_VM_History")
            self.webAction.click_element("TP_VM_History_DownArrow")
            participantList = self._browser.elements_finder("TP_VM_History_Users")
            
            if forward=="auto":
                self.assertElement.values_should_be_equal(forwardedToList[0], participantList[0].text)
                self.assertElement.values_should_be_equal(receiverList[0], participantList[1].text)
                self.assertElement.values_should_be_equal(sender, participantList[2].text)
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_forwarded_vm_info - sender"
                                     " is %s and receiver is %s and VM is forwarded "
                                     " to %s" %(sender, receiverList[0], forwardedToList[0]))
            else:
                length = len(forwardedToList)
                for f in forwardedToList:
                    for i in range(0, length):
                        if f==participantList[i].text:
                            log.mjLog.LogReporter("ThirdPanel", "info", "verify_forwarded_vm_info - forwarded party %s is present" %f)
                self.assertElement.values_should_be_equal(receiverList[0], participantList[length].text)
                self.assertElement.values_should_be_equal(sender, participantList[length+1].text)
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_forwarded_vm_info - sender is %s,"
                                      " receiver is %s and VM is forwarded to %s and %s" %(sender,\
                                      receiverList[0], forwardedToList[0], forwardedToList[1]))
            if openContactCard != 'no':
                for participant in participantList:
                    if participant.text==openContactCard:
                        x = self._browser.get_current_browser()
                        ActionChains(x).double_click(participant).perform()
                        break
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_forwarded_vm_info - Failed"
                                  " to verify VM information "+str(sys.exc_info()))
            raise AssertionError("error while verifying VM information")

    def send_cancel_group_vm(self, params):
        """
        Author: Uttam
        send_cancel_group_vm() - This method records a voicemail for group
                and presses Send or Cancel button according to parameters
        Parameters: option, recording_device and subject
        """
        try:
            if "subject" in params.keys():
                subject = re.sub("\*", " ", params["subject"])
                self.webAction.input_text("TP_GroupVM_Subject", subject)
            if params["recording_device"].lower() == "computer":
                self.webAction.click_element("vm_play_through_computer")
            else:
                self.webAction.click_element("third_panel_contact_card_vm_play_via_phone")
            time.sleep(2)
            self.webAction.click_element("TP_GroupVM_Record")
            time.sleep(8)  # This is for recording the voice-mail
            self.webAction.click_element("TP_GroupVM_StopRecord")
            time.sleep(8)  # wait for send button to become enable
            # self.webAction.explicit_wait("TP_SendGroup_VM") # not working
            self.assertElement.element_should_be_displayed("vm_cancel_button")
            self.assertElement.element_should_be_displayed("TP_SendGroup_VM")

            if "vm_type" in params.keys():
                self.verify_select_vm_type(params)
            if params["option"] == "send":
                self.webAction.click_element("TP_SendGroup_VM")
                log.mjLog.LogReporter("ThirdPanel", "info", "send_cancel_group_vm"
                                                            " - Clicked on Send button")
            else:
                self.webAction.click_element("TP_GroupVM_Cancel")
                log.mjLog.LogReporter("ThirdPanel", "info", "send_cancel_group_vm"
                                                            " - Clicked on Cancel button")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "send_cancel_group_vm"
                                                         " - Failed to send group VM " + str(sys.exc_info()))
            raise AssertionError("error while sending group voicemail")

    def play_vm_third_panel(self, playing_option, set_playing_device):
        """
        Author: Uttam
        play_vm_third_panel() - Play voicemail either via computer speaker or via phone
        Parameters: playing_option (via computer or phone) and set_playing_device
        """
        try:
            if playing_option == 'phone' and set_playing_device == 'yes':
                self.webAction.click_element("third_panel_contact_card_vm_play_via_phone")
            if playing_option == 'computer' and set_playing_device == 'yes':
                self.webAction.click_element("third_panel_contact_card_vm_play_via_device")
            self.webAction.click_element("recent_voicemail_play")
            log.mjLog.LogReporter("ThirdPanel", "info", "play_vm_third_panel - voicemail"
                                                        " played")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "play_vm_third_panel - Failed"
                                                         " to play vm " + str(sys.exc_info()))
            raise AssertionError("error while playing VM")
    
    def forward_voicemail_third_panel(self, params):
        """
        Author: UKumar
        forward_voicemail_third_panel() - Enters recipients and subject for
                                        forwarding the voicemail
        Parameters: recipients and subject(optional)
        """
        try:
            recipientlist = []
            for key in params.keys():
                if "recipient" in key:
                    recipientlist.append(params[key])

            for recipient in recipientlist:
                self.webAction.input_text("recent_vm_forward_to", recipient)
                time.sleep(3)
                self.webAction.click_element("people_grp_drop_drown_contact_name")
                time.sleep(1)
            if "subject" in params.keys():
                self.webAction.input_text("TP_GroupVM_Subject", params['subject'])
            log.mjLog.LogReporter("ThirdPanel", "info", "forward_voicemail_third_panel"
                                                        "- data entered for voicemail")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "forward_voicemail_third_panel"
                                                         " - Failed enter voicemail data " + str(sys.exc_info()))
            raise AssertionError("error while filling forward voicemail data")
    
    def record_voicemail(self, record_option):
        """
        Author: UKumar
        record_voicemail() - Records voicemail either via computer speaker or via phone
        Parameters: record_option (computer speaker or phone)
        """
        try:
            if record_option == 'computer':
                self.webAction.click_element("recent_voicemail_play_through_computer")
            else:
                self.webAction.click_element("recent_voicemail_play_through_phone")
            self.webAction.click_element("TP_GroupVM_Record")
            time.sleep(16) # wait for the recording
            self.webAction.click_element("TP_GroupVM_StopRecord")
            time.sleep(5) # wait for the send button to get enabled
            log.mjLog.LogReporter("ThirdPanel", "info", "record_voicemail - voicemail recorded")

        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "record_voicemail - Failed"
                                                         " to record voicemail " + str(sys.exc_info()))
            raise AssertionError("error while recording voicemail")
            
    def verify_select_vm_type(self, params):
        """
        Author: UKumar
        verify_select_vm_type() - Verifies that Urgent, Private and Reciept checkboxes are
                    enabled and selects one of them
        Parameters : vm_type
        """
        try:
            urgent = self.queryElement.get_value_execute_javascript("$('.message-prop')[0].firstChild.disabled")
            private = self.queryElement.get_value_execute_javascript("$('.message-prop')[1].firstChild.disabled")
            receipt = self.queryElement.get_value_execute_javascript("$('.message-prop')[2].firstChild.disabled")
            if not urgent and not private and not receipt:
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_select_vm_type"
                                                            " - vm types are enabled")
            else:
                raise AssertionError("vm types are disabled")
            vm_type_dict = {"urgent":"$('.message-prop')[0].firstChild.click()",
                            "private": "$('.message-prop')[1].firstChild.click()",
                            "receipt": "$('.message-prop')[2].firstChild.click()"
                            }
            if params["vm_type"] == "all":
                self.webAction.execute_javascript("$('.message-prop')[0].firstChild.click()")
                self.webAction.execute_javascript("$('.message-prop')[1].firstChild.click()")
                self.webAction.execute_javascript("$('.message-prop')[2].firstChild.click()")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_select_vm_type"
                                                    " - all vm type selected")
            elif params["vm_type"] == "none":
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_select_vm_type"
                                                    " - no vm type selected")
            else:
                self.webAction.execute_javascript(vm_type_dict[params["vm_type"].lower()])
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_select_vm_type"
                                                    " - vm type selected")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_select_vm_type - Failed to"
                                                         " check that vm types are enabled " + str(sys.exc_info()))

            raise AssertionError("error while checking vm type")
			
    def verify_vm_comp_info(self, params):
        """
        Author: Prashanth
        verify_vm_comp_info() - To verify the voicemail  in third panel using comp option
        Parameters: record, play_pause, pause and panel
        Ex: verify_vm_comp_info vociemail=1 pause-play=yes(optional) pause=yes(optional)
		change list: commented first line (UKumar: 1-Sep-2016)
                     added if-else condition inside else part (UKumar: 6-Sep-2016)
        """
        try:
            #self.webAction.click_element("Dashboard_IM_VM_Notification")
            if "record" in params.keys():
                self.webAction.click_element("recents_vm")
                self.webAction.explicit_wait("recents_voicemail_click")
                self.webAction.click_element("recents_voicemail_click")
                self.webAction.click_element("recent_voicemail_play")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on computer speakers & play  in selected vm in compoption ")
                if "pause_play" in params.keys():
                    self.webAction.click_element("recent_voicemail_pause")
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on pause button in compoption for pause-play(option) after play")
                    self.webAction.explicit_wait("recent_voicemail_play")
                    self.webAction.click_element("recent_voicemail_play")
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on play button in compoption for pause-play(option)after pause")
                if "pause" in params.keys():
                    self.webAction.click_element("recent_voicemail_pause")
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on pause button in compoption for pause(option) after play")
                    self.webAction.explicit_wait("recent_voicemail_play")
                           
                else:
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on play button in comp for voicemail")
                        
                #unread_vm[int(vmnumber)-1].click()        
            
            else:
                if "panel" in params.keys() and params["panel"] == "recent":
                    unread_vm=self._browser.elements_finder("recents_vm")
                else:
                    unread_vm=self._browser.elements_finder("TP_unread_vm")
                vmnumber= params["voicemail"]           
                unread_vm[int(vmnumber)-1].click()
                self.webAction.explicit_wait("recent_voicemail_play_through_computer")
                self.webAction.click_element("recent_voicemail_play_through_computer")
                time.sleep(2)
                self.webAction.click_element("recent_voicemail_play")
                time.sleep(3); # time for pause button to appear (explicit wait is not working)
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on computer speakers & play  in selected vm in compoption ")
                if "pause_play" in params.keys():
                    self.webAction.click_element("recent_voicemail_pause")
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on pause button in compoption for pause-play(option) after play")
                    self.webAction.explicit_wait("recent_voicemail_play")
                    self.webAction.click_element("recent_voicemail_play")
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on play button in compoption for pause-play(option)after pause")
                if "pause" in params.keys():
                    self.webAction.click_element("recent_voicemail_pause")
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on pause button in compoption for pause(option) after play")
                    #self.webAction.explicit_wait("recent_voicemail_play")
                           
                else:
                    log.mjLog.LogReporter("ThirdPanel","info","verify_vm_comp_info - clicked on play button in comp for voicemail")
                        
                #unread_vm[int(vmnumber)-1].click()        
        except:
            log.mjLog.LogReporter("ThirdPanel","error","verify_vm_comp_info "+str(sys.exc_info()))
            raise AssertionError("Error while playing unread voicemails via comp in third panel")	 
    
    def verify_vm_phone_info(self, params):
        """
        Author: Prashanth
        verify_vm_phone_info() - To verify the voicemail through phone option in third panel
        Parameters: 
        Ex: verify_vm_phone_info vociemail=1 pause_play=yes(optional) pause=yes(optional)
        """
        try:
            
            
            self.webAction.click_element("Recent_tab")
            if "again" in params.keys():
                self.webAction.click_element("Recent_tab")
                self.webAction.click_element("third_panel_minimize")
                
            self.webAction.click_element("Recent_dropdown")
            
            unread_vm=self._browser.elements_finder("recents_vm")
            print("#########unread_vm##########" , unread_vm )
            vmnumber = params["voicemail"]           
            time.sleep(3)
            self.webAction.click_element("Recent_dropdown_Everything")
            time.sleep(15)
            unread_vm[int(vmnumber)-1].click()
            
            self.webAction.explicit_wait("recent_voicemail_play_through_phone")
            self.webAction.click_element("recent_voicemail_play_through_phone")
            self.webAction.click_element("recent_voicemail_play")
            log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on computer speakers & play  in selected vm in phoneoption ")
            if "pause_play" in params.keys():
                self.webAction.click_element("recent_voicemail_pause")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on pausebutton in phoneoption for pause-play(option) after play")
                self.webAction.explicit_wait("recent_voicemail_play")
                self.webAction.click_element("recent_voicemail_play")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on playbutton in phoneoption for pause-play(option)after pause")
            if "pause" in params.keys():
                self.webAction.click_element("recent_voicemail_pause")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on pausebutton in phoneoption for pause(option) after play")
                self.webAction.explicit_wait("recent_voicemail_play")
                       
            else:
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on playbutton in phone for voicemail")
            unread_vm[int(vmnumber)-1].click()
            
        except:
            log.mjLog.LogReporter("Thirdpanel","error","verify_vm_phone_info "+str(sys.exc_info()))
            raise AssertionError("Error while playing unread voicemails via phone in third panel")	 
    
    def verify_vm_thirdpanel(self, params):
        """
        Author: Prashanth
        verify_vm_thirdpanel() - To verify the voicemail through phone option in third panel
        Parameters: 
        Ex: verify_vm_thirdpanel vociemail=1 pause_play=yes(optional) pause=yes(optional)
        """
        try:
            # vmnumber = params["voicemail"]           
            # self.webAction.click_element("Recent_dropdown")
            # time.sleep(3)
            # self.webAction.click_element("Recent_dropdown_Everything")
            # time.sleep(15)
            # unread_vm[int(vmnumber)-1].click()
            self.assertElement.element_should_be_displayed("peoples_panel_customer_name")
            self.assertElement.element_should_be_displayed("third_panel_messagefilter")
            self.webAction.click_element("third_panel_messagefilter")
            people_options = self._browser.elements_finder("third_panel_messagefiltergroup")
            print("**********The Value of Filter is **********  ",people_options)            
            for option in people_options:
                print("filter:")
                people_check = option.text
                #Actual=['Everything','Calls','Voicemails','Messages']
                print("option:"+people_check)
                if people_check == params["Filter"]:
                    option.click()
                    break
            unread_vm=self._browser.elements_finder("recents_vm")
            print("#########unread_vm##########" , unread_vm )
            vmnumber = params["voicemail"]           
            
            time.sleep(15)
            unread_vm[int(vmnumber)-1].click()
            self.webAction.explicit_wait("recent_voicemail_play_through_phone")
            self.webAction.click_element("recent_voicemail_play_through_phone")
            self.webAction.click_element("recent_voicemail_play")
            log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on computer speakers & play  in selected vm in phoneoption ")
            if "pause_play" in params.keys():
                self.webAction.click_element("recent_voicemail_pause")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on pausebutton in phoneoption for pause-play(option) after play")
                self.webAction.explicit_wait("recent_voicemail_play")
                self.webAction.click_element("recent_voicemail_play")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on playbutton in phoneoption for pause-play(option)after pause")
            if "pause" in params.keys():
                self.webAction.click_element("recent_voicemail_pause")
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on pausebutton in phoneoption for pause(option) after play")
                self.webAction.explicit_wait("recent_voicemail_play")
                       
            else:
                log.mjLog.LogReporter("ThirdPanel","info","verify_vm_phone_info - clicked on playbutton in phone for voicemail")
            unread_vm[int(vmnumber)-1].click()
            
        except:
            log.mjLog.LogReporter("Thirdpanel","error","verify_vm_phone_info "+str(sys.exc_info()))
            raise AssertionError("Error while playing unread voicemails via phone in third panel")

    def verify_manditory_contact_fields(self, params):
        '''
        Author: UKumar
        verify_manditory_contact_fields - Verifies manditory fields for contact creation
        Parameters: firstName, lastName, email, im, phoneNumber
        '''
        try:
            if "firstName" in params.keys():
                self.assertElement.element_should_be_displayed("TP_contact_FName_required")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_manditory_contact_fields"
                                        " - First Name is manditory field")
            if "lastName" in params.keys():
                self.assertElement.element_should_be_displayed("TP_contact_LName_required")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_manditory_contact_fields"
                                        " - Last Name is manditory field")
            if "email" in params.keys():
                self.assertElement.element_should_be_displayed("TP_contact_Email_required")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_manditory_contact_fields"
                                        " - Email is manditory field")
            if "im" in params.keys():
                self.assertElement.element_should_be_displayed("TP_contact_IM_required")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_manditory_contact_fields"
                                        " - IM is manditory field")
            if "phoneNumber" in params.keys():
                self.assertElement.element_should_be_displayed("TP_contact_PhoneNums_required")
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_manditory_contact_fields"
                                        " - Phone Number is manditory field")
        except:
            log.mjLog.LogReporter("ThirdPanel","error","verify_manditory_contact_fields - FAILED "+str(sys.exc_info()))
            raise AssertionError("Failed to verify manditory fields")
            
    def click_edit_contact_button(self):
        """
        Author: UKumar
        click_edit_contact_button() - To click on Edit Contact Button on third panel 
        Parameters: no parameter
        """
        try:
            self.webAction.click_element("third_panel_info")
            self.assertElement.page_should_contain_text("Hide Info")
            self.webAction.click_element("third_panel_edit_contact")
            self.webAction.explicit_wait("TP_edited_contact_save")
            self.assertElement.element_should_be_displayed("TP_edited_contact_save")
            log.mjLog.LogReporter("ThirdPanel", "info", "click_third_panel_info"
                                                                " - Clicked on Edit contact button successfully")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "click_third_panel_info"
                                                                 " - failed to click on Edit contact button")
            raise

    def blank_out_contact_fields(self, params):
        """
        Author: UKumar
        blank_out_contact_fields() - To set blank value in contact fields identified by params
        Parameters: title, dept, company, address, city
        """
        try:
            if "title" in params.keys():
                self.webAction.input_text("people_new_contact_job_title", "")
                log.mjLog.LogReporter("ThirdPanel", "info", "blank_out_contact_fields"
                                                            " - Job Title field is blank now")
            if "dept" in params.keys():
                self.webAction.input_text("people_new_contact_department", "")
                log.mjLog.LogReporter("ThirdPanel", "info", "blank_out_contact_fields"
                                                            " - Department field is blank now")
            if "company" in params.keys():
                self.webAction.input_text("people_new_contact_company_name", "")
                log.mjLog.LogReporter("ThirdPanel", "info", "blank_out_contact_fields"
                                                            " - Company field is blank now")
            if "address" in params.keys():
                self.webAction.input_text("people_new_contact_address", "")
                log.mjLog.LogReporter("ThirdPanel", "info", "blank_out_contact_fields"
                                                            " - Address field is blank now")
            if "city" in params.keys():
                self.webAction.input_text("people_new_contact_city", "")
                log.mjLog.LogReporter("ThirdPanel", "info", "blank_out_contact_fields"
                                                            " - City field is blank now")
            self.webAction.click_element("TP_edited_contact_save")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "blank_out_contact_fields"
                                                         " - failed to blank out contact fields")
            raise

    def verify_contact_info(self, **params):
        """
        Author: Uttam
        verify_contact_info() - This method verifies that contact information
                                is present or not
        Parameters: status and all contact related parameters according to need 
        change list: added if condition for city, state, zip and country(UKumar: 01-Aug-2016)
                    added if "im" in params.keys(): inside else part (UKumar: 23-Aug-2016)
        """
        try:
            self.webAction.explicit_wait("third_panel_info")
            self.webAction.click_element("third_panel_info")
            if params["status"] == "present":
                if "company" in params.keys():
                    self.assertElement.page_should_contain_text(params["company"])
                if "title" in params.keys():
                    self.assertElement.page_should_contain_text(params["title"])
                if "dept" in params.keys():
                    self.assertElement.page_should_contain_text(params["dept"])
                if "mobile" in params.keys():
                    # self.mobile = "("+params["mobile"][0:3]+") "+params["mobile"][3:6]+"-"+params["mobile"][6:-1]
                    self.mobile = "0" + params["mobile"]
                    self.assertElement.page_should_contain_text(self.mobile)
                if "pager" in params.keys():
                    # self.pager = "("+params["pager"][0:3]+") "+params["pager"][3:6]+"-"+params["pager"][6:-1]
                    self.pager = params["pager"]
                    self.assertElement.page_should_contain_text(self.pager)
                if "home" in params.keys():
                    # self.home = "("+params["home"][0:3]+") "+params["home"][3:6]+"-"+params["home"][6:-1]
                    self.home = "0" + params["home"]
                    self.assertElement.page_should_contain_text(self.home)
                if "assistant" in params.keys():
                    # self.assis = "("+params["assistant"][0:3]+") "+params["assistant"][3:6]+"-"+params["assistant"][6:-1]
                    self.assis = "0" + params["assistant"]
                    self.assertElement.page_should_contain_text(self.assis)
                if "fax" in params.keys():
                    # self.fax = "("+params["fax"][0:3]+") "+params["fax"][3:6]+"-"+params["fax"][6:-1]
                    self.fax = "0" + params["fax"]
                    self.assertElement.page_should_contain_text(self.fax)
                if "email" in params.keys():
                    self.assertElement.page_should_contain_text(params["email"])
                if "address" in params.keys():
                    self.assertElement.page_should_contain_text(params["address"])
                if "city" in params.keys():
                    self.assertElement.page_should_contain_text(params["city"])
                if "state" in params.keys():
                    self.assertElement.page_should_contain_text(params["state"])
                if "zip" in params.keys():
                    self.assertElement.page_should_contain_text(params["zip"])
                if "country" in params.keys():
                    self.assertElement.page_should_contain_text(params["country"])
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                              " user info verified, presnt")
            else:
                if "company" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["company"])
                    log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                                  " Company name not present")
                if "title" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["title"])
                    log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                                  " Job Title not present")
                if "dept" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["dept"])
                    log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                                  " Department not present")
                if "im" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["im"])
                self.webAction.click_element("third_panel_info")
                if "mobile" in params.keys():
                    self.mobile = "(" + params["mobile"][0:3] + ") " + params["mobile"][3:6] + "-" + params["mobile"][
                                                                                                     6:-1]
                    self.assertElement.page_should_not_contain_text(self.mobile)
                if "pager" in params.keys():
                    self.pager = "(" + params["pager"][0:3] + ") " + params["pager"][3:6] + "-" + params["pager"][6:-1]
                    self.assertElement.page_should_not_contain_text(self.pager)
                if "home" in params.keys():
                    self.home = "(" + params["home"][0:3] + ") " + params["home"][3:6] + "-" + params["home"][6:-1]
                    self.assertElement.page_should_not_contain_text(self.home)
                if "assistant" in params.keys():
                    self.assis = "(" + params["assistant"][0:3] + ") " + params["assistant"][3:6] + "-" + params[
                                                                                                              "assistant"][
                                                                                                          6:-1]
                    self.assertElement.page_should_not_contain_text(self.assis)
                if "fax" in params.keys():
                    self.fax = "(" + params["fax"][0:3] + ") " + params["fax"][3:6] + "-" + params["fax"][6:-1]
                    self.assertElement.page_should_not_contain_text(self.fax)
                if "email" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["email"])
                if "address" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["address"])
                    log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                                  " Address not present")
                if "city" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["city"])
                    log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                                  " City not present")
                if "state" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["state"])
                if "zip" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["zip"])
                if "country" in params.keys():
                    self.assertElement.page_should_not_contain_text(params["country"])
                log.mjLog.LogReporter("ThirdPanel", "info", "verify_contact_info -"
                                                              " user info verified, not presnt")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_contact_info - "
                                                           "failed to verify user info " + str(sys.exc_info()))
            raise
            
    def verify_element_availability_onpage(self,elementName):
        '''
           Check the element existance in the page by giving the element text
           change list: added regular expression for elementName (UKumar: 29-July-2016)
        '''
        try:
            elementName = re.sub("\*", " ", elementName)
            self.assertElement._page_contains(elementName)
            log.mjLog.LogReporter("ThirdPanel","info","verify_element_availability_onpage"
                                    " - "+elementName+" element available")
        except:
            log.mjLog.LogReporter("ThirdPanel","info","verify_element_availability_onpage"
                                " - "+elementName+" element not available"+str(sys.exc_info()))
            raise AssertionError("element is not available")

    def verify_element_non_availability_onpage(self,elementName):
        '''
           Check the element does not exist in the page
        '''
        try:
            if elementName=="TP_contact_address":
                if self.queryElement.element_not_displayed(elementName):
                    log.mjLog.LogReporter("ThirdPanel","info","verify_element_non_availability_onpage"
                                        " - "+elementName+" not available")
                else:
                    raise
            else:
                if self.queryElement.get_text(elementName)=="":
                    log.mjLog.LogReporter("ThirdPanel","info","verify_element_non_availability_onpage"
                                        " - "+elementName+" not available")
                else:
                    raise
        except:
          log.mjLog.LogReporter("ThirdPanel","info","verify_element_non_availability_onpage"
                                " - failed to verify element availablity "+str(sys.exc_info()))
          raise AssertionError("failed to verify element availablity")

    def check_presence_status_third_panel(self, status):
        """
        Author: Uttam
        check_presence_status_third_panel() - This method extracts presence status
                                    for a user in third panel(user details)
        Parameters: status
        """
        try:
            status = re.sub('\_', ' ', status)
            time.sleep(3)
            if (status.lower() == 'available'):
                self.assertElement.element_should_be_displayed("TP_icon_available")
            elif (status.lower() == 'in a meeting'):
                self.assertElement.element_should_be_displayed("TP_icon_in_a_meeting")
            elif (status.lower() == 'out of office'):
                self.assertElement.element_should_be_displayed("TP_icon_out_of_office")
            elif (status.lower() == 'vacation'):
                self.assertElement.element_should_be_displayed("TP_icon_vacation")
            elif (status.lower() == 'dnd' or status.lower() == 'do not disturb'):
                self.assertElement.element_should_be_displayed("TP_icon_dnd")
            elif (status.lower() == 'custom'):
                self.assertElement.element_should_be_displayed("TP_icon_custom")
            else:
                raise AssertionError("expected status are not matching. Status passed in params= "+ status.lower())
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "check_presence_status_third_panel"
                                                           " - failed to check status" + str(sys.exc_info()))
            raise
			
    def check_availability_status_third_panel(self, status):
        """
        Author: Rahul
        check_ringing_status_third_panel() - This method checks status
                                    for a user in third panel(user details)
        Parameters: color and status
        """
        try:
            status = re.sub('\_', ' ', status)
            time.sleep(2)
            actualStatus = self.queryElement._get_text("third_panel_statusText")
            log.mjLog.LogReporter("ThirdPanel", "info", "check_presence_status_third_panel - actualStatus %s " %actualStatus)

            if status.lower() == actualStatus.lower():
                log.mjLog.LogReporter("ThirdPanel", "info", "check_presence_status_third_panel"
                                                              " - Status is " + status )
            else:
                raise AssertionError("expected status are not matching")

        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "check_ringing_status_third_panel"
                                                           " - failed to check status " + str(sys.exc_info()))
            raise
