## Module: Messages
## File name: Messages.py
## Description: This class contains APIs related to Messages tab
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 04 MAY 2015  UKumar             Initial Version
###############################################################################

# Python Modules
import sys
import os
import time
import re
import autoit
from selenium.webdriver.common.action_chains import ActionChains

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class Messages:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def send_IM(self, IM):
        """
        send_IM() - This method types message identified by IM and presses
                     Return button to send the message
        parameter : IM (message to be send)
        """
        try:
            self.webAction.click_element("third_panel_chatBox")
            self.webAction.input_text("third_panel_chatBox", IM)
            #time.sleep(2)
            self.webAction.press_key("third_panel_chatBox", "RETURN")
            log.mjLog.LogReporter("Messages", "info", "send_IM - IM typed and Return key pressed")
        except:
            log.mjLog.LogReporter("Messages", "error", "send_IM - error either in typing IM or in"
                                  " pressing Return button "+str(sys.exc_info()))
            raise
            
    def verify_im_received(self, im):
        """
        Author: UKumar
        verify_im_received(): Verifies the IM received
        Parameters: im
        """
        try:
            sender_list = self._browser.elements_finder("IM_sender_name")
            im_list = self._browser.elements_finder("IM_im")
            for im1 in im_list:
                if im1.text.strip() == im:
                    log.mjLog.LogReporter("Messages", "info", "verify_im_received - IM received")                   
                    im1.click()
                    break
            self.webAction.explicit_wait("third_panel_chatBox")
            log.mjLog.LogReporter("Messages", "info", "verify_im_received - third panel opened for chat")
        except:
            try:
                log.mjLog.LogReporter("Messages", "info","verify_im_received - checking second time")
                sender_list = self._browser.elements_finder("IM_sender_name")
                im_list = self._browser.elements_finder("IM_im")
                for im1 in im_list:
                    if im1.text.strip() == im:
                        log.mjLog.LogReporter("Messages", "info", "verify_im_received - IM received")                   
                        im1.click()
                        break
                self.webAction.explicit_wait("third_panel_chatBox")
                log.mjLog.LogReporter("Messages", "info", "verify_im_received - third panel opened for chat")
            except:
                log.mjLog.LogReporter("Messages", "error", "verify_im_received - Error: "+str(sys.exc_info()))
                raise

    def mark_as_read_im_conversation(self, im):
        """
        Author: Vijay Ravi
        marks IM conversation from Messages panel as read
        Parameters: im
        """
        try:
            im_list = self._browser.elements_finder("IM_im")
            for im1 in im_list:
                if im1.text.strip() == im:
                    log.mjLog.LogReporter("Messages", "info", "mark_as_read_im_conversation - IM received")
                    ActionChains(self._browser.get_current_browser()).context_click(im1).perform()
                    break
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{DOWN}")
            time.sleep(1)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{DOWN}")
            time.sleep(1)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{ENTER}")
            log.mjLog.LogReporter("Messages", "info", "mark_as_read_im_conversation - Im Conversation marked as read")
        except:
            log.mjLog.LogReporter("Messages", "error", "mark_as_read_im_conversation -"
                                                       " error in marking conversation as read" + str(sys.exc_info()))
            raise

    def remove_im_conversation(self, params):
        """
        Author: Vijay Ravi
        removes IM conversation from Messages panel
        Parameters: search_im_entry_by, message and username
        """
        try:
            if params["search_im_entry_by"] == "im":
                im = re.sub("\*", " ", params["message"])
                im_list = self._browser.elements_finder("IM_im")
                for im1 in im_list:
                    if im1.text.strip() == im:
                        log.mjLog.LogReporter("Messages", "info", "remove_im_conversation - IM received")
                        ActionChains(self._browser.get_current_browser()).context_click(im1).perform()
                        break
            else:
                participant_to_match = [value for key, value in params.items() if "username" in key]
                participant_list_from_chat_entry = self._browser.elements_finder("IM_read_sender_name")
                for participants in participant_list_from_chat_entry:
                    i = 0
                    for sender in participant_to_match:
                        if sender in participants.text.strip():
                            i += 1
                    if i == len(participants.text.strip().split(',')):
                        log.mjLog.LogReporter("Messages", "info", "remove_im_conversation - participants verified")
                        ActionChains(self._browser.get_current_browser()).context_click(participants).perform()
                        log.mjLog.LogReporter("Messages", "info", "remove_im_conversation - right click performed")
                        break

            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{DOWN}")
            time.sleep(1)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{ENTER}")
            log.mjLog.LogReporter("Messages", "info",
                                  "remove_im_conversation - Removed conversation from messages panel")
        except:
            log.mjLog.LogReporter("Messages", "error",
                                  "remove_im_conversation - error in removing conversation" + str(sys.exc_info()))
            raise

    def verify_open_chat_entry(self, params):
        """
        Author: UKUmar
        verify_open_chat_entry() - Verifies that a read chat entry is present in Messages tab and clicks on it
                                    participant name in chat
        Parameters: sender_name
        """
        try:
            participant_to_match = [value for key, value in params.items() if "sender_name" in key]
            participant_list_from_chat_entry = self._browser.elements_finder("IM_read_sender_name")
            for participants in participant_list_from_chat_entry:
                i = 0
                for sender in participant_to_match:
                    if sender in participants.text.strip():
                        i += 1
                if i == len(re.split("\W+", participants.text.strip())):
                    log.mjLog.LogReporter("Messages", "info", "verify_open_chat_entry - participants verified")
                    participants.click()
                    log.mjLog.LogReporter("Messages", "info", "verify_open_chat_entry - clicked on chat entry")
                    break
        except:
            log.mjLog.LogReporter("Messages", "error", "verify_open_chat_entry - Error " + str(sys.exc_info()))
            raise
