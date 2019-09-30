## Module: WorkGroup
## File name: WorkGroup.py
## Description: This class contains workgroup related APIs
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 11 FEB 2015  Uttam-858             Initial Version
###############################################################################

# Python Modules
import sys
import os
import time
import re

from log import log
from WebElementAction import WebElementAction
from QueryElement import QueryElement
from AssertElement import AssertElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime


class MpvGroup:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    # APIs for MPV test sets
    
    def configure_video_conference(self,params):
        '''
           Author: Kiran
           configure_video_conference() - To configure video conference inside preferences         
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","configure_video_conference- To configure video conference inside preferences ")
            if "user_name" in params.keys():
                if self.queryElement.element_not_displayed("preferences_ac_clear_MPV_credential"):
                    self.webAction.input_text("preferences_MPV_username",params["user_name"])
                else:
                    self.webAction.click_element("preferences_ac_clear_MPV_credential")
                    self.webAction.input_text("preferences_MPV_username",params["user_name"])
            if "password" in params.keys():
                self.webAction.input_text("preferences_MPV_password",params["password"])
        # verify green save tab
            if "color_check" in params.keys():
                rgb = self._browser.element_finder("preferences_account_save_MPV").value_of_css_property("background-color")
                r,g,b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print(">..", hex_color)
                if "#09c994" not in hex_color:
                    raise
                self.webAction.click_element("preferences_account_save_MPV")
                rgb = self._browser.element_finder("preferences_account_save_MPV").value_of_css_property("background-color")
                r,g,b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print(hex_color)
            else:
                self.webAction.click_element("preferences_account_save_MPV")
            time.sleep(6)
            if "empty_credential" in params.keys():
                self.assertElement.page_should_contain_element("preferences_account_loginName_error")
                self.assertElement.page_should_contain_element("preferences_account__loginPass_error")  
            else:
                pass
            log.mjLog.LogReporter("ManhattanComponent","info","configure_video_conference- success To configure video conference inside preferences ")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","configure_video_conference- unable To configure video conference inside preferences"+str(sys.exc_info()))
            raise    
            
    def configure_video_conference_empaty(self):
        '''
           Author: Kiran
           configure_video_conference_empaty() - To configure video conference as empaty inside preferences         
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","configure_video_conference_empaty- To configure video conference as empaty inside preferences ")
            if self.queryElement.element_not_displayed("preferences_ac_clear_MPV_credential"):
                self.webAction.click_element("preferences_account_save_MPV")
            else:
                self.webAction.click_element("preferences_ac_clear_MPV_credential")
                self.webAction.explicit_wait("preferences_account_save_MPV")
                self.webAction.click_element("preferences_account_save_MPV")
            log.mjLog.LogReporter("ManhattanComponent","info","configure_video_conference_empaty- success To configure video conference inside preferences ")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","configure_video_conference_empaty- unable To configure video conference inside preferences"+str(sys.exc_info()))
            raise
            
    def add_participants_in_MPV_event(self,params):
        """
        add_participants_in_MPV_event() - This method add a user to participants in video meeting
        """
        try:
            for key in params.keys():
                if "user" in key:
                    participant = params[key].replace("*", " ")
                    print("...###33", participant)                    
                    self.webAction.input_text("events_MPV_participants_in",participant)
                    time.sleep(3)
                    self.webAction.explicit_wait("events_MPV_participants_users")
                    list = self._browser.elements_finder("events_MPV_participants_users")
                    count = 0
                    for user_name in list:
                        print(".....", user_name.text, participant)
                        if user_name.text == participant:
                            user_name.click()
                            count = count + 1
                    if count !=0:
                        log.mjLog.LogReporter("PeopleGroup","info","add_participants_in_MPV_event - User added to participants field")
                    else:
                        raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","add_participants_in_MPV_event - Failed to add user to participants field"+str(sys.exc_info()))
            raise
    
    def save_MPV_event_From_draft(self, draftName):
        '''
           Author: Kiran
           save_MPV_event_From_draft() - To save the MPV event from the draft       
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","save_MPV_event_From_draft- To save the MPV event from the draft")
            # open the draft notification
            self.defaultPanel.search_people_or_extension("a")
            contctList = self._browser.elements_finder("people_search")
            contctList[0].click()
            draftNames = self._browser.elements_finder("default_contact_draftNames1")
            for name in draftNames:
                print(".the draft info is.",name.text,draftName)
                # if name.text in draftName:
                if draftName in name.text.strip(' '):
                    print("..........",name.text,draftName)
                    name.click()
                    time.sleep(3)
                    break                
            self.webAction.explicit_wait("events_create_invite")
            self.webAction.click_element("events_create_invite")
            log.mjLog.LogReporter("ManhattanComponent","info","save_MPV_event_From_draft- success save the MPV event from the draft")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","save_MPV_event_From_draft- unable To save the MPV event from the draft"+str(sys.exc_info()))
            raise
    
    def save_MPV_meeting_duration(self, meeting_duration):
        '''
           Author: Kiran
           save_MPV_meeting_duration() - To save the MPV meeting duration      
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","save_MPV_meeting_duration- To save the MPV meeting duration")
            # edit the meeting time duration details 
            m_duration = meeting_duration.split("*")
            print("m duration is :.", m_duration, len(m_duration))
            if len(m_duration) == 2:           
                if m_duration[1] == "hour":
                    self.webAction.input_text("event_MPV_hour",m_duration[0])
                    self.webAction.input_text("event_MPV_minute","0")
                elif m_duration[1] == "minute":
                    self.webAction.input_text("event_MPV_hour","0")
                    self.webAction.input_text("event_MPV_minute",m_duration[0])
                else:
                    raise
            else:
                if m_duration[1] == "hour" and m_duration[3] == "minute":
                    self.webAction.input_text("event_MPV_hour",m_duration[0])
                    self.webAction.input_text("event_MPV_minute",m_duration[2])
                else:
                    AssertionError("invalid argument passed")
                    raise
            log.mjLog.LogReporter("ManhattanComponent","info","save_MPV_meeting_duration- success To save the MPV meeting duration")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","save_MPV_meeting_duration- unable To save the MPV meeting duration"+str(sys.exc_info()))
            raise
            
    def save_MPV_meeting_date(self, meeting_date):
        '''
           Author: Kiran
           save_MPV_meeting_date() - To save the MPV meeting date   
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","save_MPV_meeting_date- To save the MPV meeting date")
            # update the mpv meeting date
            #current_date = datetime.now()
            current_date = self.webAction.get_text("event_MPV_date",new_date)
            #Read the current date form the start date.    
            print("todays date is", current_date)
            chang_date = meeting_date.replace('*', ' ')
            chang_date = chang_date.split(' ')
            if (chang_date[1] == "day"):
                day = int(chang_date[0])
                if day == '0' :
                    return
                else:
                    new_date = datetime.datetime.strptime(current_date, "%m/%d/%y")
                    # new_date = current_date + timedelta(days=day)
                    print("the modified date is", new_date)
                    new_date = new_date.strftime('%m/%d/%Y')
                    print("formatted date is", new_date)
            # sending control_a_delete for delete the existing date
                    self.webAction.click_element("event_MPV_date") 
                    ActionChains(self._browser.get_current_browser()).send_keys(Keys.CONTROL).send_keys('a').send_keys(Keys.DELETE).perform()
                    ActionChains(self._browser.get_current_browser()).send_keys(Keys.CONTROL).send_keys('a').send_keys(Keys.DELETE).perform()
                    self.webAction.input_text("event_MPV_date",new_date)         
            else :
                self.webAction.input_text("event_MPV_date1",meeting_date)
            log.mjLog.LogReporter("ManhattanComponent","info","save_MPV_meeting_date- success To save the MPV meeting date")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","save_MPV_meeting_date- unable To save the MPV meeting date"+str(sys.exc_info()))
            raise  
    
    def verify_MPV_parameters(self, params):
        '''
           Author: Kiran
           verify_MPV_parameters() - To verify the MPV event fields  
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","verify_MPV_parameters- To verify the MPV event fields ")
            # select edit option
            event_name = params["event_name"]
            organizer = params["organizer"].replace('*',' ')
            evntName = self.queryElement.get_text("event_verify_MPV_event_name") 
            print("event name is :", evntName)
            if event_name in evntName:
                pass
            else:
                raise
            self.assertElement.element_should_contain_text("event_verify_MPV_organizer",organizer) 
            contactlist = []
            if "contact1" in params.keys(): 
                for key in params.keys():
                        if "contact" in key:                       
                            contactlist.append(params[key].replace('*',' '))
                for i in range(0, len(contactlist)): 
                    print("presenter is", contactlist[i])
                    self.assertElement.element_should_contain_text("event_verify_MPV_presenter",contactlist[i]) 
                    log.mjLog.LogReporter("ManhattanComponent","info","verify_MPV_parameters- success To verify the MPV event fields ")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","verify_MPV_parameters- unable To verify the MPV event fields "+str(sys.exc_info()))
            raise 

    
    def edit_MPV_meeting(self):
        '''
           Author: Kiran
           edit_MPV_meeting() - To edit the MPV meeting
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","edit_MPV_meeting- To edit the MPV meeting")
            # select edit option
            self.webAction.explicit_wait("event_edit_MPV_event")
            self.webAction.click_element("event_edit_MPV_event")
            log.mjLog.LogReporter("ManhattanComponent","info","edit_MPV_meeting- success To edit the MPV meeting")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","edit_MPV_meeting- unable To edit the MPV meeting"+str(sys.exc_info()))
            raise  
                
    def cancel_MPV_meeting(self):
        '''
           Author: Kiran
           cancel_MPV_meeting() - To cancel the MPV meeting
        '''
        try:           
            log.mjLog.LogReporter("ManhattanComponent","info","cancel_MPV_meeting- To cancel the MPV meeting")
            # select edit option
            self.webAction.explicit_wait("event_cancel_MPV_meeting")
            self.webAction.click_element("event_cancel_MPV_meeting")
            time.sleep(3)
            self.webAction.click_element("event_cancel_MPV_meeting_confirm")
            log.mjLog.LogReporter("ManhattanComponent","info","cancel_MPV_meeting- success To cancel the MPV meeting")		
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","cancel_MPV_meeting- unable To cancel the MPV meeting"+str(sys.exc_info()))
            raise 
        
    def join_MPV_meeting(self):
        """
        Author: kiran
        join_MPV_meeting() - This API joins the video meeting
        Parameter: 
        Ex: join_MPV_meeting event_name=mpv1
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "join_MPV_meeting -"
                                    " going to join the video meeting")
            self.webAction.explicit_wait("event_join_MPV_meeting")
            self.webAction.click_element("event_join_MPV_meeting")
            log.mjLog.LogReporter("ManhattanComponent", "info", "join_MPV_meeting -"
                                    " succefully joins the video meeting")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "join_MPV_meeting - failed"
                                    " failed This API joins the video meeting"+str(sys.exc_info()))
            raise    
    
    def verify_event_radio_button(self, params):
        """
        Author: kiran
        verify_event_radio_button() - This API verify the event radio button
        Parameter: 
        Ex: verify_event_radio_button verify=colaboration_enabled/colaboration_disabled
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_event_radio_button -"
                                    " going to verify the selected radio button")
            x = self._browser.get_current_browser()
            Cstatus = x.find_element_by_xpath(".//input[@id='eventedit-collaborationButton']").is_selected()
            Vstatus = x.find_element_by_xpath(".//input[@id='eventedit-videoButton']").is_selected()
            print("the radio button value is:", Cstatus, Vstatus)
            if params["verify"] == "colaboration_enabled" and Cstatus is not True:
                raise
            elif params["verify"] == "colaboration_disabled" and Cstatus is True:
                raise
            if params["verify"] == "video_enabled" and Vstatus is not True:
                raise
            elif params["verify"] == "video_disabled" and Vstatus is True:
                raise
            else:
                print("the radio button is selected as expected")
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_event_radio_button -"
                                    " succefull to verify the selected radio button")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_event_radio_button - failed"
                                    " failed to verify the selected radio button"+str(sys.exc_info()))
            raise    
    
    def verify_meeting_name(self, params):
        """
        Author: kiran
        verify_meeting_name() - This API verify only the meeting name is displayed in upcoming tab
        Parameter: 
        Ex: verify_meeting_name event_name=mpv1
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_meeting_name -"
                                    " going to verify the meeting name")
            self.webAction.explicit_wait("event_click_modify")
            events_name = self._browser.elements_finder("event_click_modify")
            count = 0
            print("total events are", len(events_name))
            for name in events_name:
                if params["event_name"] in name.text :                
                    print("the MPV event name is avaialble in upcoming tab", name.text)
                    count = count + 1
                    break
                else:
                    pass
            if count != 1:
                raise
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_meeting_name -"
                                    " succefully verified the meeting name")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_meeting_name - failed"
                                    " failed verify the meeting name"+str(sys.exc_info()))
            raise
            
    def verify_meeting_name_and_date(self, params):
        """
        Author: kiran
        verify_meeting_name_and_date() - This API verify the meeting name and date is displayed in upcoming tab
        Parameter: 
        Ex: verify_meeting_name_and_date event_name=mpv1
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_meeting_name_and_date -"
                                    " going to verify the meeting name and date")           
            
            xpath_element= self._browser._map_converter("MP_event_info")
            xpath_value_orig = xpath_element["BY_VALUE"]
            MPV_event_info = self._browser.elements_finder("MP_event_info")
            print(MPV_event_info)
            print(xpath_value_orig)
            for i in range(1, len(MPV_event_info)):
                MPV_xpath = xpath_value_orig + "[" + str(i) + "]"
                print("this is i" , MPV_xpath)
            # for i in MPV_event_info:
                # print(i.text)
       
            # events_name = self._browser.elements_finder("event_click_modify")
            
            # count = 0
            # print("total events are", len(events_name))
            # for name in events_name:
                # if params["event_name"] in name.text :                
                    # print("the MPV event name is avaialble in upcoming tab", name.text)
                    # count = count + 1
                    # break
                # else:
                    # pass
            # if count != 1:
                # raise
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_meeting_name_and_date -"
                                    " succefully verified the meeting name and date")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_meeting_name_and_date - failed"
                                    " failed verify the meeting name and date"+str(sys.exc_info()))
            raise