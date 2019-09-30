## Module: Voicemails
## File name: Voicemails.py
## Description: This class contains voicemail related APIs
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date                Engineer              Description
##  ---------       --------------      -----------------------
## 03 APRIL 2017        UKumar             Initial Version
###############################################################################

# Python Modules
import sys
import os
import time
from selenium.webdriver.common.action_chains import ActionChains

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class Voicemails:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def reply_voicemail(self, params):
        """
        Author: Uttam
        reply_voicemail() - This method records a voicemail via telephone in
              reply to a received voicemail, and replies that to sender back
        Parameter: subject
        """
        try:
            self.webAction.click_element("vm_reply_button")
            if params["subject"] != "default":
                self.webAction.input_text("vm_subject_field", params["subject"])

            if params["recording_device"] == "phone":
                self.webAction.click_element("vm_play_through_phone")
            else:
                self.webAction.click_element("vm_play_through_computer")

            if params["vm_type"] == "none":
                log.mjLog.LogReporter("Voicemails", "info", "verify_select_vm_type"
                                                    " - no vm type selected")
            else:
                self.verify_select_vm_type(params["vm_type"])
            
            self.webAction.click_element("vm_start_record_button")
            time.sleep(10) # This is for recording the voice-mail
            self.webAction.click_element("vm_stop_record_button")
            time.sleep(3) # wait for Send button to enable
            
            self.assertElement.element_should_be_displayed("vm_cancel_button")
            self.assertElement.element_should_be_displayed("vm_send_button")
            self.webAction.click_element("vm_send_button")
            log.mjLog.LogReporter("Voicemails", "info", "reply_voicemail"
                                  " - Clicked on Send button")
        except:
            log.mjLog.LogReporter("Voicemails", "error", "reply_voicemail - error"
                                  " while replying to voicemail "+str(sys.exc_info()))
            raise
            
    def forward_voicemail(self, toList, params):
        """
        Author: Uttam
        forward_voicemail() - This method records a voicemail via speaker to
              forward to a received voicemail, and forwards to third user
        Parameter: subject
        """
        try:
            self.webAction.click_element("recent_vm_forward")
            for recipient in toList:
                self.webAction.click_element("recent_vm_forward_to")
                self.webAction.input_text("recent_vm_forward_to", recipient)
                time.sleep(3)
                self.webAction.click_element("people_grp_drop_drown_contact_name")
                time.sleep(1)

            if params["subject"] != "default":
                self.webAction.input_text("vm_subject_field", params["subject"])

            if params["recording_device"] == "phone":
                self.webAction.click_element("vm_play_through_phone")
            else:
                self.webAction.click_element("vm_play_through_computer")

            if params["vm_type"] == "none":
                log.mjLog.LogReporter("Voicemails", "info", "verify_select_vm_type"
                                                    " - no vm type selected")
            else:
                self.verify_select_vm_type(params["vm_type"])
            
            self.webAction.click_element("vm_start_record_button")
            time.sleep(10) # This is for recording the voice-mail
            self.webAction.click_element("vm_stop_record_button")
            time.sleep(5) # wait for Send button to enable
            
            self.assertElement.element_should_be_displayed("vm_cancel_button")
            self.assertElement.element_should_be_displayed("vm_send_button")
            self.webAction.click_element("vm_send_button")
            log.mjLog.LogReporter("Voicemails", "info", "reply_voicemail"
                                  " - Clicked on Send button")
        except:
            log.mjLog.LogReporter("Voicemails", "error", "reply_voicemail - error"
                                  " while replying to voicemail "+str(sys.exc_info()))
            raise

    def delete_read_vm(self, vm_sender):
        """
        Author: Uttam
        delete_read_vm() - This method deletes read voicemails
        Parameter: sender
        """
        try:
            unreadVMs = self._browser.elements_finder("recent_vm_read")
            senderList = self._browser.elements_finder("recent_vm_sender_read")
            if self.queryElement.element_not_displayed("recent_vm_delete"):
                for vm in unreadVMs:
                    for sender in senderList:
                        if sender.text == vm_sender:
                            sender.click()
                            break
            self.webAction.click_element("recent_vm_delete")
            log.mjLog.LogReporter("Voicemails", "info", "delete_read_vm - "
                                                          "delete button clicked for read vm")
        except:
            log.mjLog.LogReporter("Voicemails", "error", "delete_read_vm - "
                                                           "failed to delete read vm " + str(sys.exc_info()))
            raise

    def delete_unread_vm(self, vm_sender):
        """
        Author: Uttam
        delete_unread_vm() - This method deletes unread voicemails
        Parameter: sender
        """
        try:
            # self.webAction.click_element("Recent_all_tab")
            unreadVMs = self._browser.elements_finder("recent_voicemail_unread")
            senderList = self._browser.elements_finder("recent_vm_sender_unread")

            if self.queryElement.element_not_displayed("recent_vm_delete"):
                for vm in unreadVMs:
                    for sender in senderList:
                        if sender.text == vm_sender:
                            sender.click()
                            break
            self.webAction.click_element("recent_vm_delete")
            log.mjLog.LogReporter("Voicemails", "info", "delete_unread_vm - "
                                                        "delete button clicked for unread vm")
        except:
            log.mjLog.LogReporter("Voicemails", "error", "delete_unread_vm - "
                                                         "failed to delete unread vm " + str(sys.exc_info()))
            raise

    def save_vm(self, sender, vm_to_save):
        """
        Author: UKumar
        save_vm() - To save the heard or unheard voicemail
        Parameters: sender and vm_to_save
        """
        try:
            if vm_to_save == "heard":
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_read")
            else:
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_unread")

            for vm_sender in vm_sender_list:
                if vm_sender.text.strip() == sender:
                    log.mjLog.LogReporter("Voicemails", "info", "save_vm - voicemail found")
                    break
            else:
                raise AssertionError("No voicemail found from sender %s!" % sender)
            self.webAction.click_element("vm_first_in_list")
            self.webAction.explicit_wait("vm_save_button")
            self.webAction.click_element("vm_save_button")
            self.webAction.explicit_wait("vm_saved")
            self.assertElement.element_should_be_displayed("vm_saved")
            self.webAction.click_element("vm_saved_folder")
            time.sleep(4)
            if vm_to_save == "heard":
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_read")
            else:
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_unread")
            for vm_sender in vm_sender_list:
                if vm_sender.text.strip() == sender:
                    log.mjLog.LogReporter("Voicemails", "info", "save_vm - voicemail found in Saved folder")
                    break
            else:
                raise AssertionError("No voicemail found in saved folder from sender %s!" % sender)
        except:
            log.mjLog.LogReporter("Voicemails", "error", "save_vm - failed to save vm " + str(sys.exc_info()))
            raise

    def unsave_vm(self, sender, vm_to_save):
        """
        Author: UKumar
        unsave_vm() - To unsave the heard or unheard voicemail
        Parameters: sender and vm_to_save
        """
        try:
            self.webAction.click_element("vm_saved_folder")
            if vm_to_save == "heard":
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_read")
            else:
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_unread")

            for vm_sender in vm_sender_list:
                if vm_sender.text.strip() == sender:
                    log.mjLog.LogReporter("Voicemails", "info", "save_vm - voicemail found")
                    break
            else:
                raise AssertionError("No voicemail found from sender %s!" % sender)
            self.webAction.click_element("vm_first_in_list")
            self.webAction.explicit_wait("vm_unsave_button")
            self.webAction.click_element("vm_unsave_button")
            time.sleep(2)
            if vm_to_save == "heard":
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_read")
            else:
                vm_sender_list = self._browser.elements_finder("recent_vm_sender_unread")
            for vm_sender in vm_sender_list:
                if vm_sender.text.strip() == sender:
                    raise AssertionError("Voicemail still found in Saved folder!")
            else:
                log.mjLog.LogReporter("Voicemails", "info", "save_vm - voicemail unsaved")
        except:
            log.mjLog.LogReporter("Voicemails", "error", "unsave_vm - failed to unsave vm " + str(sys.exc_info()))
            raise
