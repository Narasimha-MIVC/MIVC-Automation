## Module: Events
## File name: Events.py
## Description: This class contains event related APIs
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date                Engineer              Description
##  ---------       --------------      -----------------------
## 10 APRIL 2017        UKumar             Initial Version
###############################################################################

# Python Modules
import sys
import os
import time
import re
import autoit
import pyautogui

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class Events:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def click_new_event(self):
        """
        click_new_event() - This method clicks on new event under Events tab
        """
        try:
            self.webAction.explicit_wait("events_new_event_button")
            self.webAction.click_element("events_new_event_button")
            log.mjLog.LogReporter("Events", "info", "click_new_event - clicked on new event button")
        except:
            log.mjLog.LogReporter("Events", "error", "click_new_event - Failed to click on new event button "+str(sys.exc_info()))
            raise
            
    def enter_exchange_credentials(self, exchange_username, exchange_password):
        """
        Author: UKumar
        enter_exchange_credentials(): To Enter exchange credentials after opening Events tab if asked
        Parameters: exchange_username and exchange_password
        """
        try:
            self.webAction.input_text("event_exchange_username", exchange_username)
            self.webAction.input_text("event_exchange_password", exchange_password)
            self.webAction.click_element("event_exchange_submit")
            time.sleep(3)
            self.webAction.click_element("event_exchange_ok_button")
            log.mjLog.LogReporter("Events", "info", "enter_exchange_credentials"
                                " - exchange credentials enterd.")
        except:
            log.mjLog.LogReporter("Events", "error", "enter_exchange_credentials"
                        " - Failed to enter exchange credentials "+str(sys.exc_info()))
            raise
            
    def set_meeting_title(self,event):
        """
        set_meeting_title() - This method input a meeting title under new events
        """
        try:
            
            self.assertElement.element_should_be_displayed("event_form")
            self.webAction.input_text("events_meeting_title",event)
            time.sleep(2)            
            log.mjLog.LogReporter("Events","info","set_meeting_title - Meeting title added")
        except:
            log.mjLog.LogReporter("Events","error","set_meeting_title - Failed to input meeting title "+str(sys.exc_info()))
            raise
            
    def set_calendar_date(self,date):
        """
        set_calendar_date() - This method select a date in the new event calendar
        """
        try:
            count = 0
            self.webAction.click_element("events_calendar_widget")
            date_list=self._browser.elements_finder("events_select_date")
            for select_date in date_list:
                if select_date.text == date:
                    select_date.click()
                    count = count + 1
            #list=self._browser.elements_finder("events_start_date")
            #selected = self._browser.element_finder("events_start_date").value_of_css_property("eventedit-start-date")
            if count != 0:
                log.mjLog.LogReporter("Events","info","set_calendar_date - Date selected")
            else:
                raise AssertionError("Date not available")
        except:
            log.mjLog.LogReporter("Events","error","set_calendar_date - Failed to select a date "+str(sys.exc_info()))
            raise
            
    def set_meeting_time(self, time):
        """
        Author: UKumar
        set_meeting_time() - This method enters time for meeting
        Parameters: time (hhmm)
        """
        try:
            if time == "auto_update":
                content = self.queryElement.get_value("TP_get_time")
                #print("Content is : ", content)
                hour = content.strip().split(":")[0]
                minute = content.strip().split(":")[1]
                if int(minute) in range(0, 7):
                    minute = "0"+str(int(minute) + 3)
                else:
                     minute = str(int(minute) + 3)
                new_time =  hour+":"+minute
                #print("new_time:, ", new_time)
                self.webAction.input_text_basic('TP_get_time', new_time)
                log.mjLog.LogReporter("Events","info","set_meeting_time - meeting time entered")
                return new_time
            else:
                self.webAction.input_text_basic('TP_get_time', time)
                log.mjLog.LogReporter("Events","info","set_meeting_time - meeting time entered")
                return time
        except:
            log.mjLog.LogReporter("Events","error","set_meeting_time - Failed to input meeting time "+str(sys.exc_info()))
            raise

    def set_event_duration(self, duration):
       """
       Author: Aakash
       set_meeting_time() - This method enters duration for meeting
       Parameters: duration
       """
       try:
           hours = duration / 60
           minutes = duration % 60
           self.webAction.clear_input_text('TP_event_duration_hours')
           self.webAction.input_text_basic('TP_event_duration_hours', hours)
           self.webAction.input_text_basic('TP_event_duration_minutes', minutes)    
       except:
           raise Exception("Events","error","set_event_duration - Failed to input meeting duration "+str(sys.exc_info()))
            
    def events_add_meeting_time_details(self,params):
        '''
           Author: Surendra
           events_add_meeting_details() - This method set meeting title
           ex: events_add_meeting_details name=test
        
        '''
        try:
            log.mjLog.LogReporter("Events","info"," events_add_meeting_details- Adding meeting details")
            ctime=time.strftime("%H:%M")
            timelist=ctime.split(':')
            print("***********",timelist)
            if timelist[1] == "57":
                if timelist[0] == "24":
                    timelist[0] ="0"
                timelist[0] = int(timelist[0]) + int("1")
                timelist[1] = int("00")
            elif timelist[1] == "58":
                if timelist[0] == "24":
                    timelist[0] ="0"
                timelist[0] = int(timelist[0])+int("1")
                timelist[1] = int("01")
            elif timelist[1] == "59":
                if timelist[0] == "24":
                    timelist[0] ="0"
                timelist[0] = int(timelist[0])+int("1")
                timelist[1] = int("02")
            else:
                timelist[1] = int(timelist[1]) + int("3")
                print ("***********", timelist)
                    #stime=timelist.split(':')
            jointime = ''.join([str(jtime) for jtime in timelist])
            print("*******this is sury jointime :", jointime)
            content=self.queryElement.get_value("TP_get_time")
            self.webAction.input_text_basic('TP_get_time',jointime)
            log.mjLog.LogReporter("Events","info","events_add_meeting_details- Meeting title added successfully")    
        except:
            log.mjLog.LogReporter("Events","error","events_add_meeting_details - Failed to add meeting details"+str(sys.exc_info()))
            raise
            
    def add_user_organizers(self, user):
        """
        add_user_organizers() - This method add a user to organizers field under meeting type in events
        """
        try:
            self.webAction.input_text("events_organisers_in", user)
            time.sleep(3)
            #self.webAction.click_element("event_select_organizer_name1")
            list = self._browser.elements_finder("events_select_user")
            #list = self._browser.elements_finder("event_select_organizer_name1")
            
            count = 0
            for user_name in list:
                if user_name.text==user:
                    #time.sleep(2)
                    user_name.click()
                    #time.sleep(2)
                    count = count + 1
            if count !=0:
                log.mjLog.LogReporter("Events","info","add_user_organizers - User added to organizers field")
            else:
                raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("Events","error","add_user_organizers - Failed to add user to organizers field"+str(sys.exc_info()))
            raise

    def add_user_presenters(self,user):
        """
        add_user_presenters() - This method add a user to presenters field under meeting type in events
        """
        try:
            self.webAction.input_text("events_presenters_in",user)
            #self.webAction.input_text("new_event_presenter",user)
            time.sleep(2)
            #self.webAction.click_element("enent_presenters_drop_down")
            list = self._browser.elements_finder("events_select_user")
            count = 0
            for user_name in list:
                #print(user)
                #print("***********************")
                #time.sleep(2)
                if user_name.text==user:
                    user_name.click()
                    count = count + 1
                    break
                    
            if count !=0:
                log.mjLog.LogReporter("Events","info","add_user_presenters - User added to presenters field")
            else:
                raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("Events","error","add_user_presenters - Failed to add user to presenters field"+str(sys.exc_info()))
            raise
    
    def add_user_participants(self,params):
        """
        add_user_participants() - This method add a user to participants field under meeting type in events
        Change list : added re.sub("\*", " ", params[key]) in place of params[key] to pass first name and last name (UKumar: 30-Dec-2016)
        """
        try:
            for key in params.keys():
                if "user" in key:
                    self.webAction.input_text("events_participants_in", re.sub("\*", " ", params[key]))
                    time.sleep(1)
                    list1 = self._browser.elements_finder("events_select_user")
                    count = 0
                    for user_name in list1:
                        if user_name.text==re.sub("\*", " ", params[key]):
                            user_name.click()
                            count = count + 1
                            break
                    if count !=0:
                        log.mjLog.LogReporter("Events","info","add_user_participants - User added to participants field")
                    else:
                        raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("Events","error","add_user_participants - Failed to add user to participants field"+str(sys.exc_info()))
            raise
    
    def click_create_event_invite(self):
        """
        click_create_event_invite() - This method clicks on create event invite under new event
        """
        try:
            log.mjLog.LogReporter("Events","info","click_create_event_invite - Going to click on create event invite")
            self.webAction.click_element("events_create_invite")
            #self.webAction.click_element("events_create_invite2")
            log.mjLog.LogReporter("Events","info","click_create_event_invite - clicked on create event invite")
        except:
            log.mjLog.LogReporter("Events","error","click_create_event_invite - Failed to click on create event invite "+str(sys.exc_info()))
            raise

    def get_upcoming_event(self, event_name):
        """
        Author: UKumar
        get_upcoming_event() - Returns yes if given event found otherwise no
        Parameters: event_name
        """
        try:
            event_found = "no"
            for i in range(3):
                event_names = self._browser.elements_finder("event_events_name")
                for name in event_names:
                    print(name.text)
                    if name.text.split(" ")[0].strip().lower() == event_name:
                        event_found = "yes"
                        log.mjLog.LogReporter("Events", "info", "get_upcoming_event - event found")
                        break
                else:
                    log.mjLog.LogReporter("Events", "info",
                                          "get_upcoming_event - event not listed in %s try (ies) " % (i + 1))
                    time.sleep(2)
                if event_found == "yes":
                    break
            return event_found
        except:
            log.mjLog.LogReporter("Events", "error", "get_upcoming_event - Failed to click find any event "+str(sys.exc_info()))
            raise
            
    def verifying_event_details(self, params):
        """
        Author: Surendra
        verifying_event_details() - This API checks the presenters and participants
                    placeholders and various labels for events fields
        Parameters: label
        Change list: added break and change if count!=0 to count==1 (UKumar: 01-Dec-2016)
        """
        try:
            self.assertElement.page_should_contain_element("event_presenter_name")
            self.assertElement.page_should_contain_element("event_participant_name")
            
            labels = self._browser.elements_finder("event_fields_labels")
            count = 0
            label1 = params["label"][0].upper() + params["label"][1:].lower()
            for label in labels:
                if label1 == label.text:
                    count += 1
                    break
            if count == 1:
                log.mjLog.LogReporter("Events","info","verifying_event_details - label is present properly")
            else:
                log.mjLog.LogReporter("Events","error","verifying_event_details - label is not present properly")
                raise AssertionError("Label is not in proper case")
        except:
            log.mjLog.LogReporter("Events","error","verifying_event_details - Failed to check"
                                    " presenters/particepents text"+str(sys.exc_info()))
            raise
            
    def share_call_screen(self, params):
        """
        author:prashanth
        share_call_screen() - This API clicks on the screen share button in call
        change list: added if condition for share_option (UKumar: 26-Dec-2016)
        """
        try:
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if "share" in params.keys():
                time.sleep(2)
                self.webAction.click_element("events_share_button")
                time.sleep(1)
                if params["share_option"] == "share_full_screen":
                    self.webAction.click_element("event_share_full_screen")
                    time.sleep(14)
                    log.mjLog.LogReporter("Events", "info", "share_call_screen - clicked on share full screen")
                elif params["share_option"] == "share_area":
                    self.webAction.click_element("event_share_area")
                    time.sleep(14)
                    log.mjLog.LogReporter("Events", "info", "share_call_screen - clicked on share area")
                else:
                    self.webAction.click_element("event_share_window")
                    time.sleep(12) # wait for choose application to share window to appear
                    autoit.win_activate("Select an application to share")
                    autoit.control_send("[TITLE:Select an application to share]",
                                        "[NAME:runningApplistView]", "{RIGHT}")
                    log.mjLog.LogReporter("Events", "info", "share_call_screen - clicked on share window")
            if "accept" in params.keys():
                self.webAction.click_element("default_accept_share")
                log.mjLog.LogReporter("Events", "info", "share_call_screen - accepted screen share successfully")
        except:
            log.mjLog.LogReporter("Events","error","share_call_screen - clicked screen share failed" +str(sys.exc_info()))
            raise
    
    def accept_screen_share(self, join_when):
        """
        Author: UKumar
        accept_screen_share(): This API accept sharing either by pressing
            'green join button' in dashboard or by pressing 'View Screen Share'
            button (sharing started after chat)
        Parameters: join_when
        """
        try:
            if join_when == "green_join_button":
                self.assertElement.element_should_be_displayed("default_accept_share")
                self.assertElement.element_should_be_displayed("default_reject_share")
                self.assertElement.element_should_be_displayed("people_view_screen_share")
                self.assertElement.element_should_be_displayed("people_copy_clipboard")
                self.webAction.click_element("default_accept_share")
                log.mjLog.LogReporter("Events", "info", "accept_screen_share"
                    " - accepted screen share by pressing green join button")
            else:
                self.assertElement.element_should_be_displayed("people_view_screen_share")
                self.assertElement.element_should_be_displayed("people_copy_clipboard")
                self.webAction.click_element("people_view_screen_share")
                log.mjLog.LogReporter("Events", "info", "accept_screen_share"
                    " - accepted screen share by pressing View Screen Share button")
        except:
            log.mjLog.LogReporter("Events", "error", "accept_screen_share"
                " - failed to accept screen share " +str(sys.exc_info()))
            return False

    def toggle_more_settings(self):
        """
        toggle_more_settings() - This method expands meeting settings options
        """
        try:
            self.webAction.click_element("events_more_settings")
            log.mjLog.LogReporter("Events", "info", "toggle_more_settings - Meeting settings toggled")
        except:
            log.mjLog.LogReporter("Events", "error", "toggle_more_settings - Failed to toggle meeting settings "+str(sys.exc_info()))
            raise

    def set_dial_out_participant(self, join_audio):
        """
        Author: UKumar
        set_dial_out_participant() - This API selects either press one to join audio
                                     part radio button or automatically join audio part
                                     radio button according to the parameters
        Parameters: join_audio
        """
        try:
            self.webAction.click_element("event_dial_out_participant")
            if join_audio == "press_one":
                self.webAction.select_radio_button("event_press_one_join_audio")
                log.mjLog.LogReporter("Events", "info", "set_dial_out_participant -"
                    " Must press one to enter audio portion of the meeting radio button selected")
                     
            else:
                self.webAction.select_radio_button("event_automatic_join_audio")
                log.mjLog.LogReporter("Events", "info", "set_dial_out_participant -"
                " Participants are automatically added to the audio portion of the meeting radio button selected")
                    
        except:
            log.mjLog.LogReporter("Events", "error", "set_dial_out_participant - failed"
                                    " to select checkboxes "+str(sys.exc_info()))
            raise

    def verify_events_panel(self, option):
        """
        Author: UKumar
        verify_events_panel() - Verifies that second panel, Events tab is opened or not
        Parameters: option
        """
        try:

            status = self.queryElement.element_not_displayed("events_new_event_button")
            if not status and option == "present":
                log.mjLog.LogReporter("Events", "info", " verify_events_panel"
                                                             " - Events panel is opened")
            elif not status and option == "absent":
                raise AssertionError("Events panel is opened")
            elif status and option == "absent":
                log.mjLog.LogReporter("Events", "info", " verify_events_panel"
                                                             " - Events panel is not opened")
            else:
                raise AssertionError("Events panel is not opened")
        except:
            log.mjLog.LogReporter("Events", "info", " verify_events_panel -"
                                                         "failed to verify Events panel " + str(sys.exc_info()))
            raise
        
    def send_meeting_request_for_invite(self):
        """
        Author: UKumar
        send_meeting_request_for_invite() - This API clicks on send button in outlook to create meeting
        Parameters: no parameter
        """
        try:
            time.sleep(2)
            autoit.win_activate("[CLASS:rctrl_renwnd32]")
            log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite"
                                                    " - entering meeting location")
            time.sleep(5)
            #autoit.control_send("[CLASS:rctrl_renwnd32]", "REComboBox20W1", "")
            autoit.control_send("[CLASS:rctrl_renwnd32]", "REComboBox20W1", "any conference room")
            #time.sleep(2)
            log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite"
                                                    " - clicking on send button")
            autoit.control_click("[CLASS:rctrl_renwnd32]", "Button1")
            try:
                window_handle = autoit.win_wait("[TITLE:Microsoft Outlook; CLASS:#32770]", 5)
                log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite"
                                                        " - Attendees changed dialog box appeared")
            except Exception as e:
                window_handle = 0
                log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite"
                                                        " - Attendees changed dialog box did not appear")
            
            log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite "+str(window_handle))
            if window_handle == 1:
                autoit.win_activate("[CLASS:#32770]")
                time.sleep(3)
                autoit.control_click("[CLASS:#32770]", "Button3")
                log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite - Clicked on OK button")
            log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_invite"
                                                    " - successfully sent meeting request from outlook")
        except:
            log.mjLog.LogReporter("Events", "error", "send_meeting_request_for_invite - failed"
                                    " to send meeting request from outlook "+str(sys.exc_info()))
            raise
    
    def send_meeting_request_for_cancel(self):
        """
        Author: UKumar
        send_meeting_request_for_cancel() - This API sends the meeting cancel request from outlook
        Parameters: no parameter
        """
        try:
            # not implemented completely
            log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_cancel -"
                                    " going to sends the meeting cancel request from outlook")           
            time.sleep(3)
            # autoit.send("!{h}{c}")
            # time.sleep(7)
            # autoit.send("{ENTER}")
            # time.sleep(3)
            # autoit.control_click("[CLASS:rctrl_renwnd32]", "Button1")
            print("sending key hc message")
            autoit.control_send("[CLASS:rctrl_renwnd32]", "NetUIHWND2", "!{h}{c}")
            time.sleep(3)
            autoit.control_send("Microsoft Outlook", "&Yes", "{ENTER}")
            time.sleep(5)
            autoit.control_click("[CLASS:rctrl_renwnd32]", "Button1")
            print("event successfully deleted ")
            log.mjLog.LogReporter("Events", "info", "send_meeting_request_for_cancel -"
                                    " succefully sends the meeting cancel request from outlook")
        except:
            log.mjLog.LogReporter("Events", "error", "send_meeting_request_for_cancel - failed"
                                    " failed to sending the meeting cancel request from outlook"+str(sys.exc_info()))
            raise

    def play_recording_through_client(self, play_object):
        """
        Author: UKumar
        play_recording_through_client() - This API clicks on play buuton to play recording
        Parameters: play_object (object of play recording option)
        """
        try:
            play_object.click()
            time.sleep(3)
            self.webAction.click_element("event_play_recording_button")
            log.mjLog.LogReporter("Events", "info", "play_recording_through_client -"
                                    " clicked on play button to start playing recording")
        except:
            log.mjLog.LogReporter("Events", "error", "play_recording_through_client - failed"
                                    " to click on play button "+str(sys.exc_info()))
            raise

    def download_recording(self, download_object, download_path):
        """
        Author: UKumar
        download_recording() - This API clicks on play buuton to play recording
        Parameters: play_object (object of play recording option)
        """
        try:
            download_object.click()
            time.sleep(4) # wait for Save As dialog box to appear
            autoit.win_activate("Save As")
            time.sleep(2)
            autoit.control_send("[CLASS:#32770]", "Edit1", download_path)
            time.sleep(1)
            autoit.control_click("[CLASS:#32770]", "Button1")
            log.mjLog.LogReporter("Events", "info", "download_recording -"
                                    " recording downloaded")
        except:
            log.mjLog.LogReporter("Events", "error", "download_recording - failed"
                                    " to download recording "+str(sys.exc_info()))
            raise

    def handle_presenter_upgrade_popup(self):
        try:
            if autoit.win_exists("Mitel Presenter Update") == 1:
                autoit.win_activate("Mitel Presenter Update") 
                autoit.control_click("[TITLE:Mitel Presenter Update]", "[Text:Skip]")
        except:
            raise Exception("Error in handling upgrade popup")

    def screen_share_exo(self, share_option):
        """
        Author: UKumar
        screen_share_exo() - This API clicks on one of the three sharing options from exo client
        Parameters: share_option
        """
        try:
            time.sleep(2) # wait for sharing option buttons to get enabled
            exo_share_options = self._browser.elements_finder("event_exo_share_options")
            
            if share_option == "share_full_screen":
                exo_share_options[0].click()
                log.mjLog.LogReporter("Events", "info", "screen_share_exo - clicked on Share Full Screen")
            elif share_option == "share_area":
                exo_share_options[1].click()
                log.mjLog.LogReporter("Events", "info", "screen_share_exo - clicked on Share Area")
            else:
                exo_share_options[2].click()                
                log.mjLog.LogReporter("Events", "info", "screen_share_exo - clicked on Window Share")
        except:
            log.mjLog.LogReporter("Events", "error", "screen_share_exo - failed"
                                    " to click on sharing optins "+str(sys.exc_info()))
            raise

    def join_endo_conference_dialin(self, params):
        """
        Author: UKumar
        join_endo_conference_dialin() - For joining a meeting from endo client on external number
                                        or internal number through softphone or deskphone
        Parameters: join_on, joining_device
        """
        try:
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params["join_on"] == "internal_number":

                if params["joining_device"] == "deskphone":
                    self.webAction.explicit_wait("event_dial_me_in")
                    self.webAction.click_element("event_dial_me_in")
                    self.webAction.click_element("event_dial_me_in")
                    self.webAction.explicit_wait("default_recieve_call")
                    self.webAction.click_element("default_recieve_call")
                    log.mjLog.LogReporter("Events", "info", "join_endo_conference_dialin"
                                          " - joined event by dial in from deskphone on internal number")
                else:
                    self.webAction.explicit_wait("event_join_on_softphone")
                    self.webAction.click_element("event_join_on_softphone")
                    log.mjLog.LogReporter("Events", "info", "join_endo_conference_dialin"
                                          " - joined event by dial in from softphone on internal number")
            else:
                # Clicking on the same button will dial External number assigned on the profile page
                self.webAction.explicit_wait("event_dial_me_in")
                self.webAction.click_element("event_dial_me_in")
                log.mjLog.LogReporter("Events", "info", "join_endo_conference_dialin"
                                      " - clicked on dial-in button, call will be answered from external number")

        except:
            log.mjLog.LogReporter("Events", "error", "join_endo_conference_dialin - failed"
                                  " to join endo conference "+str(sys.exc_info()))
            raise

    def click_reload_conference(self):
        try:
            while self.queryElement.element_not_displayed("event_conference_loaded"):
                self.webAction.explicit_wait("event_reload_conference")
                self.webAction.click_element("event_reload_conference")
                time.sleep(4)
        except:
            log.mjLog.LogReporter("Events", "error", "click_reload_conference - failed" +str(sys.exc_info()))
            return False

    def join_endo_conference_chat(self):
        """
        Author: UKumar
        join_endo_conference_chat() - For joining a meeting in chat mode
        Parameters: no parameter
        """
        try:
            self.webAction.click_element("join_web_conf")
            self.webAction.click_element("join_web_conf")
            # Reloading a conference if the conference does not appear
            self.click_reload_conference()
            self.webAction.explicit_wait("event_conference_loaded")
            log.mjLog.LogReporter("Events", "info", "join_endo_conference_chat"
                                                    " - joined conference in chat mode")
        except:
            log.mjLog.LogReporter("Events", "error", "join_endo_conference_chat - failed"
                                                     " to join endo conference in chat mode" + str(sys.exc_info()))
            raise

    def join_via_exo_client(self, participant):
        """
        Author: UKumar
        join_via_exo_client(): To type the name and join the event from Exo client
        Parameters: participant
        """
        try:
            self.webAction.click_element("EXO_JOIN")
            self.webAction.input_text("EXO_JOIN", participant)
            self.webAction.press_key("EXO_JOIN", "RETURN")
            log.mjLog.LogReporter("Events", "info", "join_via_exo_client"
                                  " - typed name and press enter")
        except:
            log.mjLog.LogReporter("Events", "error", "join_via_exo_client"
                                                     " - failed to join from exo "+str(sys.exc_info()))
            raise

    def callme_from_endo(self, number):
        """
        Author: UKumar
        callme_from_endo(): To make a call using call me feature from endo client
        Parameters: participant
        """
        try:
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.webAction.click_element("event_join_on_external_number")
            self.webAction.input_text("event_callme_number_input", number)
            self.webAction.click_element("event_callme_button")
            self.click_reload_conference()
            log.mjLog.LogReporter("Events", "info", "callme_from_endo"
                                                    " - entered number and clicked on Call Me")
        except:
            log.mjLog.LogReporter("Events", "error", "callme_from_endo"
                                                     " - Failed to click on Call Me " + str(sys.exc_info()))
            raise

    def callme_from_exo(self, number):
        """
        Author: UKumar
        callme_from_exo(): To make a call using call me feature from exo client
        Parameters: participant
        """
        try:
            time.sleep(0.5)
            self.webAction.click_element("event_exo_callme_input")
            time.sleep(0.5)
            self.webAction.input_text("event_exo_callme_input", number)
            time.sleep(0.5)
            self.webAction.click_element("event_exo_callme_button")
            log.mjLog.LogReporter("Events", "info", "callme_from_exo"
                                                    " - entered number and clicked on Call Me")
        except:
            log.mjLog.LogReporter("Events", "error", "callme_from_exo"
                                                     " - Failed to click on Call Me " + str(sys.exc_info()))
            raise

    def verify_event_appeared(self, event_name):
        """
        Author: UKumar
        verify_event_appeared(): Verifies that given event is appearing in Upcoming tab or not
        Parameters: event_name
        """
        try:
            found = False
            for i in range(6):
                event_names = self._browser.elements_finder("event_events_name")
                for name in event_names:
                    if event_name == name.text.split(" ")[0].strip():
                        found = True
                        log.mjLog.LogReporter("Events", "info", "verify_event_appeared - event is appearing.")
                        break
                    else:
                        log.mjLog.LogReporter("Events", "info", "verify_event_appeared"
                                                            " - event not listed in %s try(ies) " % (i + 1))
                        time.sleep(4)
                if found:
                    break
            else:
                raise AssertionError("Meeting not displayed in Upcoming tab!")
        except:
            log.mjLog.LogReporter("Events", "error", "verify_event_appeared"
                                                     " - Failed to verify meeting appearance " + str(sys.exc_info()))
            raise Exception("Events", "error", "verify_event_appeared-Failed to verify meeting appearance ")
