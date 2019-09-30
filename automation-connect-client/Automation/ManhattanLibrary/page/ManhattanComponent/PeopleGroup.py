## Module: Login
## File name: Login.py
## Description: This class contains the people and group list
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
## 18 AUG 2014  Jahnavi-844             Initial Version
###############################################################################
# Python Modules
import sys
import os
import time
import re
import autoit
import zipfile
from datetime import datetime,date

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement
from robot.api.logger import console

class PeopleGroup:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)
        
    def open_own_user_detail(self):
        '''
           Author: Gautham
           open_own_user_detail() - Open own user panel from first panel
           parameters:
           ex: open_own_user_detail
        
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup","info","open_own_user_detail- Opening own user panel")           
            self.webAction.click_element("default_own_name")
            log.mjLog.LogReporter("PeopleGroup","info","open_own_user_detail- Own user panel opened successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","open_own_user_detail- Failed to open own user detail panel"+str(sys.exc_info()))
            raise
            
    def search_people_match_name(self,searchName,matchName,find):
        '''
           Author: Gautham
           Search the person from dashboard by giving a name or number
        '''
        try:
            log.mjLog.LogReporter("People_Group","info","search_people_match_name - Search the person from dashbord by giving a name or number")
            time.sleep(3)
            self.webAction.click_element("default_name_number_search")
            log.mjLog.LogReporter("People_Group","debug","search_people_match_name : Clicked on search button")
            self.webAction.input_text("default_search_input",searchName)
            time.sleep(3)
            if find == "no":
                self.assertElement.page_should_not_contain_text(matchName)            
                log.mjLog.LogReporter("People_Group","info","search_people_match_name - "+matchName+ " not available in dashbord")            
            else:
                self.assertElement.page_should_contain_text(matchName)
                log.mjLog.LogReporter("People_Group","info","search_people_match_name - "+matchName+" available in dashbord")
            
            self.webAction.click_element("default_people_tab") 
        except:
            log.mjLog.LogReporter("People_Group","error","search_people_match_name - Error while searching people on dashboard "+str(sys.exc_info()))
            raise

    def verify_contactCard_from_favoriteList(self, params):
        '''
           author : kiran
           verify_contactCard_from_favoriteList() - this API verifies the contact name of from fav list to third panel contcat name
           ex1: verify_contactCard_from_favoriteList
        '''
        try:
            favlist = self._browser.elements_finder("SP_group_contact_list")
            flag = 0
            for i in favlist:
                if i.text == params["contact"]:
                    i.click()
                    flag = 1
                    break
            if flag == 0:
                print("contact not found in favorite list")
                raise
            thirdPcontct = self._browser.element_finder("third_panel_new_contact")
            if thirdPcontct.text == params["contact"]:
                print("third panel contact name matched with favorite list contact")
                self.assertElement._is_element_contains("third_panel_answer_call")
            else:
                print("contact not found in third panel")
                raise
            log.mjLog.LogReporter("PeopleGroup", "info",
                                  "verify_contactCard_from_favoriteList- successfully called the contact")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "verify_contactCard_from_favoriteList- failed to call the contact" + str(
                                      sys.exc_info()))
            raise

    def verify_contactCard_from_CallDashboard(self, params):
        '''
           author : kiran
           verify_contactCard_from_CallDashboard() - this API verifies the contact name of from call lists to third panel contcat name
           ex1: verify_contactCard_from_CallDashboard
        '''
        try:
            calllist = self._browser.elements_finder("default_OutG_CallName")
            flag = 0
            for i in calllist:
                print(i.text, params["contact"])
                if (i.text.strip() in params["contact"].replace("*", " ")):
                    i.click()
                    flag = 1
                    break
            if flag == 0:
                print("contact name not found in call list")
                raise
            time.sleep(2)
            thirdPcontct = self._browser.element_finder("third_panel_new_contact")
            if thirdPcontct.text in params["contact"].replace("*", ' '):
                print("third panel contact name matched with dashboard call name")
                self.assertElement._is_element_contains("third_panel_answer_call")
            else:
                print("third panel contact name not matched with dashboard call name")
                raise
            log.mjLog.LogReporter("PeopleGroup", "info",
                                  "verify_contactCard_from_CallDashboard- contact card has been verified")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "verify_contactCard_from_CallDashboard- failed to verify the contact" + str(
                                      sys.exc_info()))
            raise

    def verify_contactCard_from_GrpContact(self, params):
        '''
           author : kiran
           verify_contactCard_from_GrpContact() - this API verifies the contact name of from group contcat name
           ex1: verify_contactCard_from_GrpContact
        '''
        try:
            contllist = self._browser.elements_finder("SP_group_contact_list")
            flag = 0
            for i in contllist:
                print(i.text, params["contact"])
                if i.text == params["contact"]:
                    i.click()
                    flag = 1
                    break
            if flag == 0:
                print("contact not found in group list")
                raise
            thirdPcontct = self._browser.element_finder("third_panel_new_contact")
            print(thirdPcontct.text, params["contact"])
            if thirdPcontct.text == params["contact"]:
                print("third panel contact name matched with dashboard call name")
                self.assertElement._is_element_contains("third_panel_answer_call")
            else:
                print("third panel contact name matched with dashboard call name")
                raise
            log.mjLog.LogReporter("PeopleGroup", "info",
                                  "verify_contactCard_from_GrpContact- contact card has been verified")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "verify_contactCard_from_GrpContact- failed to verify the contact" + str(
                                      sys.exc_info()))
            raise
            
    def add_new_group_button(self):
        '''
           click on the add new button which is on the bottom of the page
        '''
        try:
            autoit.win_activate("Mitel Connect")            
            self.webAction.click_element("peoples_add_button")
            time.sleep(3)
            self.webAction.click_element("add_new_group")            
            #self.assertElement.element_should_be_displayed("group_form")
            # autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            # autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            # autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{ENTER}")
            log.mjLog.LogReporter("PeopleGroup","info","add_new_group_button - creating new group")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","add_new_group_button -Error while creating the new group"+str(sys.exc_info()))
            raise
            
    def group_tab(self):
        '''
           click on the group tab
           displays the list of groups
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup","info","group_tab - going to select the group tab")
            self.webAction.click_element("peoples_group")
            log.mjLog.LogReporter("PeopleGroup","info","group_tab - selected group tab")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","group_tab- Error while selecting group tab "+str(sys.exc_info()))
            raise

    def display_grouplist(self, params):
        '''
           Author : Iswarya
           Display all the groups
           Change list: added logic for verifying all the groups instead of one group (UKumar: 23-June-2016)
        '''
        try:
            log.mjLog.LogReporter("People_Group", "info", "Display entire people group list")
            groupNamesList = []
            count = 0
            for key in params.keys():
                if "groupName" in key:
                    groupNamesList.append(params[key])
            grpArr = self._browser.elements_finder("peoples_grp")
            for group in groupNamesList:
                for grp in grpArr:
                    if group == grp.text:
                        count = count + 1
            if count == len(groupNamesList):
                log.mjLog.LogReporter("People_Group", "info", "display_grouplist - all contact groups are listed")
            else:
                raise ArithmeticError("all the groups are not listed")
        except:
            log.mjLog.LogReporter("People_Group", "error", "display_grouplist"
                                                           " - failed to display group list " + str(sys.exc_info()))
            raise
    
    def get_group_list(self):
        '''
        Author: UKumar
        get_group_list() - This method returns list of all the groups under People tab
        Parameter: no parameter
        '''
        try:
            groupList = self._browser.elements_finder("peoples_first_group")
            #groupList = self._browser.get_current_browser().find_elements_by_class_name("groupitem")
            if groupList:
                log.mjLog.LogReporter("PeopleGroup", "info", "get_group_list - group list found")
                return groupList
            else:
                log.mjLog.LogReporter("PeopleGroup", "info", "get_group_list - no group found")
                return False
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "get_group_list - Error while finding groups"
                                  " "+str(sys.exc_info()))
            raise
            
    def group_select(self,groupName):
        '''
        Author: modified by Akash
        group_select() - This method selects a group by giving groupName
        Parameter: groupName
        '''
        try:
            self.webAction.click_element("peoples_group")
            groupList = self._browser.elements_finder("peoples_first_group")
            for group in groupList:
                if groupName == group.text.strip():
                    edit_group_map = self._browser._map_converter("edit_group")
                    edit_group_xpath = '.' + edit_group_map["BY_VALUE"]
                    groupname = group.find_element_by_xpath(edit_group_xpath)                
                    groupname.click()
                    log.mjLog.LogReporter("PeopleGroup", "info", "group_select - Selected the group "+groupName)
                    break
            else:
                return False
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "group_select"
                                                          " - Error while selecting group "+str(sys.exc_info()))
            raise
            
    def verify_group_option(self, params):
        """
        Author: UKumar
        verify_group_option(): Verifies that all the group options are present
        parameters: contacts
        """
        try:
            if ("option" in params.keys()) and (params["option"] == "meetingWithGroup"):
                self.assertElement.element_should_be_displayed("TP_MeetingWithGroup")
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_group_option"
                                                             " - Meeting with Group options verified")
            self.assertElement.element_should_be_displayed("TP_StartGroupchat")
            self.assertElement.element_should_be_displayed("TP_Group_VM")
            self.assertElement.element_should_be_displayed("third_panel_edit_group")
            log.mjLog.LogReporter("PeopleGroup", "info", "verify_group_option - "
                                  "Group chat, Group VM options & edit button verified")
            contacts = []
            for key in params.keys():
                if "contact" in key:
                    contacts.append(params[key])
            
            contacts_list=self._browser.elements_finder("TP_GroupUsers")
            for contact in contacts:
                for member in contacts_list:
                    if member.text==contact:
                        log.mjLog.LogReporter("PeopleGroup","info","verify_group_option - The user is part of group")
                        break
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "verify_group_option - Error"
                                  " while verifying group options "+(str(sys.exc_info())))
            raise AssertionError("failed to verify group options")
            
    def select_group_option(self, params):
        """
        Author : Uttam
        select_group_option() - This method clicks on any of the three
                        options present on third panel of a contact group
        Parameters : option
        """
        try:
            if params["option"] == "groupChat" :
                self.webAction.click_element("TP_StartGroupchat")
                log.mjLog.LogReporter("PeopleGroup", "info", "select_group_option - "
                                      "clicked on Start Group Chat")
                if "groupCall" in params.keys():  
                    self.webAction.click_element("third_panel_answer_call")
                    log.mjLog.LogReporter("PeopleGroup", "info", "select_group_option - "
                                      "clicked on group call icon")
            elif params["option"] == "meetingWithGroup" :
                self.webAction.click_element("TP_MeetingWithGroup")
                log.mjLog.LogReporter("PeopleGroup", "info", "select_group_option - "
                                      "clicked on Schedule Meeting With Group")
            else:
                self.webAction.click_element("TP_Group_VM")
                log.mjLog.LogReporter("PeopleGroup", "info", "select_group_option - "
                                      "clicked on Send Group Voiemail")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "select_group_option - Error in"
                                  " clicking on %s %s" %(params["option"], str(sys.exc_info())))
            raise

    def open_edit(self):
        '''
          Author: Gautham
          open_edit() - Clicks on edit button for group
          parameters: panel
        '''
        try:
            time.sleep(2)
            self.webAction.click_element("third_panel_edit_group")
            log.mjLog.LogReporter("PeopleGroup", "info", "open_edit - edit button clicked")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", " open_edit - edit button not clicked " + str(sys.exc_info()))
            raise

    def delete_contact(self):
        """
        Author: bparihar
        delete_group() - This method identifies a contact and deletes that
        Parameters: none
        """
        try:
            self.webAction.click_element("third_panel_info")
            userList = self._browser.get_current_browser().find_elements_by_class_name("contactCardContactPointsButton")
            if len(userList) != 0:
                self.webAction.click_element("third_panel_delete_contact")
                self.webAction.click_element("third_panel_delete_contact_yes")
            return True
        except:
            log.mjLog.LogReporter("PeopleGroup","error"," delete_group - Error while clicking on delete button "+str(sys.exc_info()))
            raise
    
    def delete_group(self, params):
        """
        Author: Unknown modified by Uttam
        delete_group() - This method identifies a group and deletes that
        Parameters: groupName and option
        """
        try:
            self.webAction.click_element("peoples_group")
            time.sleep(2) # to wait for groups to appear
            if self.group_select(params["groupName"]) != False:                
                self.webAction.click_element("third_panel_edit_group")
                self.webAction.click_element("TP_delete_group")
                self.webAction.explicit_wait("TP_delete_discard")
                self.webAction.explicit_wait("TP_detele_confirm")
                if "option" in params and params["option"] == "cancel":
                     self.webAction.click_element("TP_delete_discard")
                else:
                     self.webAction.click_element("TP_detele_confirm")
                log.mjLog.LogReporter("PeopleGroup","info"," delete_group - "
                                      "clicked on Delete button to delete the group")
            else:
                log.mjLog.LogReporter("PeopleGroup","info"," delete_group - "
                                      "No Such Group Present")
                return False

        except:
            log.mjLog.LogReporter("PeopleGroup","error"," delete_group - Error while"
                                  " clicking on delete button "+str(sys.exc_info()))
            raise

    def add_contact_number(self, locator, box, type, num):
        '''
           Author: Gautham
           To add contact number to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_number - Adding contact number")
            # Select the option from last dropdown
            elements = self._browser.elements_finder(locator)
            (elements[-1]).click()
            
            boxes = self._browser.elements_finder(box)
            boxes[-1].send_keys(num)
            
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_number - contact number added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_contact_number - Adding contact number failed " + str(sys.exc_info()))
            raise AssertionError("add_contact_number - Error in adding contact number")

    def add_contactedit_number(self, option, box, type, num):
        '''
           Author: Gautham
           To edit contact number in contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contactedit_number - editing contact number")
            time.sleep(2)  # to wait for phone number textbox to apper, explicit_wait is not working
            # self.webAction.select_from_dropdown_using_text(option,type)
            self.webAction.input_text(box, num)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contactedit_number - contact number edited successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_contactedit_number - editing contact number failed " + str(sys.exc_info()))
            raise AssertionError("add_contactedit_number - Error in editing contact number")

    def add_contact_details(self, params):
        '''
           Author: Gautham Modified by Uttam
           To add contact with details like first name, middle name
           last name, company name, department, business, mobile, pager, home number
           Change list: added if condition inside elif params["cancel"] == "closeform" (UKumar: 09-Dec-2016)
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_details - Adding a contact with given details")
            time.sleep(2)
            #del params['component_id']
            for key in params.keys():
                if "first_name" in key:
                    self.webAction.click_element("people_new_contact_first_name")
                    # time.sleep(6)
                    self.add_first_name(params["first_name"])
                elif "middle_name" in key:
                    self.add_middle_name(params["middle_name"])
                elif "last_name" in key:
                    self.add_last_name(params["last_name"])
                elif "company" in key:
                    self.add_company(params["company"])
                elif "department" in key:
                    self.add_department(params["department"])
                elif "email" in key:
                    self.webAction.click_element("people_new_contact_email")
                    self.add_email(params["email"])
                elif "IM" in key:
                    self.add_im(params["IM"])
                elif "title" in key:
                    self.add_job_title(params["title"])
                elif "address" in key:
                    self.add_address(params["address"])
                elif "city" in key:
                    self.add_city(params["city"])
                elif "state" in key:
                    self.add_state(params["state"])
                elif "zip" in key:
                    self.add_zip(params["zip"])
                elif "country" in key:
                    self.add_country(params["country"])
                elif "company" not in key:
                    self.add_company()
                elif "department" not in key:
                    self.add_department()
                elif "title" not in key:
                    self.add_job_title()
                elif "address" not in key:
                    self.add_address()
                else:
                    # raise AssertionError("PeopleGroup","error","add_contact_details - error in passing parameters")
                    log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_details - no parameter passed")
                time.sleep(2)
            if "cancel" in params.keys():
                if params["cancel"] == "yes":
                    time.sleep(2)
                    self.webAction.click_element("TP_conatct_delete")
                    time.sleep(5)
                    log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_details - Contact cancelled")
                elif params["cancel"] == "closeform":
                    self.webAction.click_element("TP_contact_form_close")
                    if "option" in params.keys() and params["option"] == "discard_my_changes":
                        self.webAction.click_element("TP_contact_Edit_cancel_discardChanges")
                        log.mjLog.LogReporter("PeopleGroup", "info",
                                              "add_contact_details - form cancelled and clicked on Discard My Changes")
                    else:
                        self.webAction.click_element("TP_contact_Edit_cancel_cancel")
                        log.mjLog.LogReporter("PeopleGroup", "info",
                                              "add_contact_details - form cancelled and clicked on Cancel")
                elif params["cancel"] == "editcontact":
                    time.sleep(2)
                    self.webAction.click_element("third_panel_contact_delete_yes")
                    time.sleep(5)
                    log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_details - Edit Contact cancelled")
                elif params["cancel"] == "othertab":
                    time.sleep(5)
                    # self.defaultPanel.invoke_events_tab() this line is incorrect
                    time.sleep(3)
                    self.webAction.click_element("default_draft_notify_name")
                else:
                    log.mjLog.LogReporter("PeopleGroup", "info",
                                          "add_contact_details - Contact neither cancelled nor saved")
            else:
                self.webAction.click_element("third_panel_contact_save")
                log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_details - save contact button pressed")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_contact_details - Failed to add contact " + str(sys.exc_info()))
            raise AssertionError("Failed to add contact details")

    def add_first_name(self, value):
        '''
           Author: Gautham
           To add first name to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_first_name - Adding first name")
            self.webAction.input_text("people_new_contact_first_name", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_first_name - First name added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_first_name - Adding first name failed " + str(sys.exc_info()))
            raise

    def add_middle_name(self, value):
        '''
           Author: Gautham
           To add middle name to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_middle_name - Adding middle name")
            self.webAction.input_text("people_new_contact_middle_name", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_middle_name - Middle name added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_middle_name - Adding middle name failed " + str(sys.exc_info()))
            raise

    def add_last_name(self, value):
        '''
           Author: Gautham
           To add last name to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_last_name - Adding last name")
            self.webAction.input_text("people_new_contact_last_name", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_last_name - Last name added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_last_name - Adding last name failed " + str(sys.exc_info()))
            raise

    def add_email(self, value):
        '''
           Author: Gautham
           To email to contact
           change list: added if condition to enter space (UKumar, 19-July-2016)
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_email - Adding email")
            if value == "blank":
                self.webAction.input_text("people_new_contact_email", " ")
            else:
                self.webAction.input_text("people_new_contact_email", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_email - email added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_email - Adding email failed " + str(sys.exc_info()))
            raise

    def add_im(self, value):
        '''
           Author: Gautham
           To add IM details contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_IM - Adding IM details")
            self.webAction.input_text("people_new_contact_im", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_IM - IM details added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_IM - Adding IM details failed " + str(sys.exc_info()))
            raise

    def add_job_title(self, value=''):
        '''
           Author: Gautham
           To add job title to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_job_title - Adding job title")
            self.webAction.input_text("people_new_contact_job_title", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_job_title - job title added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_job_title - Adding job title failed " + str(sys.exc_info()))
            raise

    def add_department(self, value=''):
        '''
           Author: Gautham
           To add department to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_department - Adding department name")
            self.webAction.input_text("people_new_contact_department", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_department - department name added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_department - Adding department name failed " + str(sys.exc_info()))
            raise

    def add_company(self, value=''):
        '''
           Author: Gautham Modified by Utttam
           To add company to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_company - Adding company")
            self.webAction.input_text("people_new_contact_company_name", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_company - Company name added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "add_company - Adding company name failed " + str(sys.exc_info()))
            raise

    def add_address(self, value=''):
        '''
           Author: Gautham
           To add address to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_address - Adding address")
            self.webAction.input_text("people_new_contact_address", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_address - address added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_address - Adding address failed " + str(sys.exc_info()))
            raise

    def add_city(self, value):
        '''
           Author: Gautham
           To add city to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_city - Adding city")
            self.webAction.input_text("people_new_contact_city", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_city - city added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_city - Adding city failed " + str(sys.exc_info()))
            raise

    def add_state(self, value):
        '''
           Author: Gautham
           To add state to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_state - Adding state")
            self.webAction.input_text("people_new_contact_state", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_state - state added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_state - Adding state failed " + str(sys.exc_info()))
            raise

    def add_zip(self, value):
        '''
           Author: Gautham
           To add zip to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_zip - Adding zip")
            self.webAction.input_text("people_new_contact_zip", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_zip - zip added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_zip - Adding zip failed " + str(sys.exc_info()))
            raise

    def add_country(self, value):
        '''
           Author: Gautham
           To add country to contact
        '''
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "add_country - Adding country")
            self.webAction.input_text("people_new_contact_country", value)
            log.mjLog.LogReporter("PeopleGroup", "info", "add_country - country added successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_country - Adding country failed " + str(sys.exc_info()))
            raise

    def telephony_third_panel_chm_status(self, params):

        '''
         author : Yogesh
         third_panel_chm_status() : list out of chm status with contact name of selected group
         parameter: groupName
         ex: groupName=Bingo 
             display { contact_list: color}= {barabara:green}
         status    green=available, gray=not available, red=in meeting or out of office or offline  
        '''
        try:
            rgb = self._browser.elements_finder("third_panel_chm_status")
            # rgb = self._browser.elements_finder("third_panel_group_contact_chm_status")
            len1 = len(rgb)
            print("len1", len1)
            if len1 == 0:
                log.mjLog.LogReporter("PeopleGroup", "info", "telephony_third_panel_chm_status - no contacts found")
                return False
            else:
                color_code = []
                clr1 = []
            for rgb_color in rgb:
                ccolor = rgb_color.value_of_css_property("background-color")
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', ccolor).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                color_code.append(hex_color)
            for clr in color_code:
                if "#09cf94" in clr:
                    clr1.append("Green")
                elif "#d9d9d9" in clr:
                    clr1.append("Gray")
                elif "#ff5550" in clr:
                    clr1.append("red")
                elif "#ffd500" in clr:
                    clr1.append("yellow")
                else:
                    log.mjLog.LogReporter("PeopleGroup", "info", " telephony_third_panel_chm_status - empty list")
            if "verifycolor" in params.keys():
                if params["verifycolor"] in clr1:
                    log.mjLog.LogReporter("PeopleGroup", "info", "telephony_third_panel_chm_status : color verified ")
                else:
                    raise Exception(" PeopleGroup", "info",
                                         "telephony_third_panel_chm_status : color not verified ")

            c_list = self._browser.elements_finder("third_panel_contact_list")
            # c_list=self._browser.elements_finder("third_panel_group_contact_chm_status")
            contact_list = []
            for clist in c_list:
                con = self.queryElement.get_text("third_panel_group_contact_chm_status")
                contact_list.append(clist.text)

                dict_list = {}
            for contact, color in zip(contact_list, clr1):
                dict_list[contact] = color

                print("list of telephony status with name:", dict_list)
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "telephony_third_panel_chm_status : contact list with status ")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", " telephony_third_panel_chm_status " + str(sys.exc_info()))
            raise

    def display_person_detailinfo(self):
        '''
          click on contact and details be displayed on third page
        '''
        try:
            self.webAction.click_element("TP_EVENT_INFO")
            self.assertElement.page_should_contain_text("work")
            self.assertElement.page_should_contain_text("mobile")
            self.assertElement.page_should_contain_text("pager")
            self.assertElement.page_should_contain_text("home")
            self.assertElement.page_should_contain_text("fax")
            self.assertElement.page_should_not_contain_text("IM")    
        except:
            log.mjLog.LogReporter("PeopleGroup","error","display_person_detailinfo - Error while clicking on the person name"+str(sys.exc_info()))
            raise

    def click_favorite_button(self, peopleName, option):
        """
        Author: Uttam
        click_favorite_button() - This method clicks on favorite button for
                a given user for adding/deleting it to/from Favorite group
        Parameters: peopleName and option
        Change List: user.text is replaced from user.text.strip()
        """
        try:
            userList = self._browser.elements_finder("peoples_firstname")
            
            log.mjLog.LogReporter("PeopleGroup", "info", "click_favorite_button -"
                                  " length of user list ",len(userList))            
            if option == "add":
                favoriteButtonList = self._browser.elements_finder("peoples_favorite")
            else:
                favoriteButtonList = self._browser.elements_finder("peoples_favorite_on")
                
            lengthUserList=len(userList)
            lengthFavoriteButtonList=len(favoriteButtonList)
            difference=lengthUserList-lengthFavoriteButtonList
             
            if len(userList) == 1:
                favoriteButtonList[0].click()
            else:
                for user in userList:
                    if (user.text.strip()==peopleName):
                        indexUser=userList.index(user)
                favIndex=indexUser-difference
                if favIndex < 0:
                    favIndex = 0
				#favoriteButtonList[favIndex].mouse_hover()            
                favoriteButtonList[favIndex].click()
                if option == "add":
                    log.mjLog.LogReporter("PeopleGroup", "info", "click_favorite_button -"
										  " favorite button clicked for adding the user")
                else:
                    log.mjLog.LogReporter("PeopleGroup", "info", "click_favorite_button -"
										  " favorite button clicked for deleting the user")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "click_favorite_button - "
                                  "error while clicking favorite button "+str(sys.exc_info()))
            raise
            
    def open_contact_from_favourites(self, name):
        """
        Author: Prashanth
        open_contact_from_favourites() - This method clicks on a user entry in favourites to open contact card of a user
        Parameter: name
        """
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "open_contact_from_favourites"
                                  " - Selecting person from the favourites")
            time.sleep(2)
            favoriteList = self._browser.elements_finder("peoples_search_name_group")
            
            for fav in favoriteList:
                if name in fav.text:
                    fav.click()
                    log.mjLog.LogReporter("PeopleGroup", "info", "open_contact_from_favourites"
                                                                 " - clicked on user")
                    break
            else:
                raise AssertionError("user doesn't exist in favourites")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "open_contact_from_favourites - "
                                  "Error while clicking user"
                                  " "+str(sys.exc_info()))
            raise
            
    def check_favorite_button(self, peopleName):
        """
        Author: Uttam
        check_favorite_button() - This method checks the presence of favorite
                                  symbol for the person identified by peopleName  
        Parameters : peopleName
        Change List: groupName parameter removed
        """
        try:
            indexUser = -1
            userList = self._browser.get_current_browser().find_elements_by_class_name("first-name")
            if userList:
                for user in userList:
                    if user.text==peopleName:
                        log.mjLog.LogReporter("PeopleGroup","info","check_favorite_button"
                                              " - user is present in Favorites")
                        indexUser=userList.index(user)
                        break
                    else:
                        log.mjLog.LogReporter("PeopleGroup","info","check_favorite_button"
                                          " - user is "+str(user.text)) 
                star = self._browser.elements_finder("second_people_fav_icon")                
                if indexUser == -1:
                    log.mjLog.LogReporter("PeopleGroup","info","check_favorite_button"
                                          " - user is not Favorite")
                    return "false"
                else: 
                    imageURL = star[indexUser].value_of_css_property("background-image")
                    imageName = imageURL.split("/")[-1].strip(")")
                    if imageName == "Icons_Buttons_Favorite_On.png":
                        log.mjLog.LogReporter("PeopleGroup","info","check_favorite_button"
                                          " - user is Favorite")
                    return "true"
            else:
                log.mjLog.LogReporter("PeopleGroup","info","check_favorite_button"
                                      " - no user is present in Favorites")
                return "no user"
                                          
        except:
            log.mjLog.LogReporter("PeopleGroup","error","check_favorite_button - error"
                                  " while checking favorite button "+str(sys.exc_info()))
            raise

    def check_favorite_symbol_from_search(self, peopleName):
        """
        Author: UKumar
        check_favorite_symbol_from_search() - This method checks the presence of favorite
                                  button and symbol is not present for the person identified by peopleName
        Parameters : peopleName and groupName(optional)
        """
        try:
            indexUser = -1
            userList = self._browser.get_current_browser().find_elements_by_class_name("contact-item")
            for user in userList:
                if user.text == peopleName:
                    indexUser = userList.index(user)
                    break

            star = userList[indexUser].find_elements_by_tag_name("button")

            if len(star) == 0:
                log.mjLog.LogReporter("PeopleGroup", "info", "check_favorite_symbol_from_search"
                                                             " - favorite button is not present")
                return False
            else:
                log.mjLog.LogReporter("PeopleGroup", "info", "check_favorite_symbol_from_search"
                                                             " - favorite button is present")

                imageURL = star[0].value_of_css_property("background-image")
                imageName = imageURL.split("/")[-1].strip(")")
                if imageName == "Icons_Buttons_Favorite.png":
                    log.mjLog.LogReporter("PeopleGroup", "info", "check_favorite_symbol_from_search"
                                                                 " - user is not Favorite")
                else:
                    log.mjLog.LogReporter("PeopleGroup", "info", "check_favorite_symbol_from_search"
                                                                 " - user is Favorite")
                return True
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "check_favorite_symbol_from_search - error"
                                                          " while checking favorite button " + str(sys.exc_info()))
            raise
    
    def close_panel(self,panel):
        '''
          Author: Gautham modified by Uttam
          close_panel() - close the second panel, second panel for search or
                            third panel of Manhattan client
          parameters: panel
        '''
        try: 
            if panel == "second":
                self.webAction.click_element("peoples_second_panel_minimized_button")
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel - "
                                    "closed the second panel successfully")
            elif panel == "second_search":
                self.webAction.click_element("peoples_second_panel_search_close")
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel - second panel"
                                    " for search result closed successfully")
            elif panel == "third":
                self.webAction.click_element("peoples_close_third_panel_min")
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel- "
                                    "closed the third panel successfully")
            elif panel == "thirdclose":
                self.webAction.click_element("TP_contact_form_close")
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel- "
                                    "closed the third panel successfully")
            elif panel == "groupDraft":
                self.webAction.click_element("TP_Group_Form_Close")
                self.webAction.explicit_wait("TP_Group_Form_Close_Yes")
                self.webAction.click_element("TP_Group_Form_Close_Yes")
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel- closed the third panel successfully")
            elif panel == "screen_share":
                self.webAction.click_element("TP_share_minimize")
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel- "
                                                             "Screen share panel minimized")
            else:
                log.mjLog.LogReporter("PeopleGroup", "info", "close_panel- Wrong panel type")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "close_panel - "
                                "problem in closing the panel "+str(sys.exc_info()))
            raise
            
    def call_by_pressing_enter(self, username):
        """
        Author: Uttam
        call_by_pressing_enter() - This method selects a user identified by
            username by pressing down arrow key and presses ENTER key on that user
        Parameter: username
        """
        try:
            userList = self._browser.get_current_browser().find_elements_by_class_name("contactAnchor")
            self.press_up_down_arrow("down")
            
            for user in userList:
                formattedName = user.text.split("\n")
                full_name = formattedName[1].strip() # if user has only first name
                if len(formattedName) >= 3:
                    full_name = formattedName[1].strip() + " " + formattedName[2] # if user has first name and last name both
                if full_name == username:
                    ActionChains(self._browser.get_current_browser()).send_keys(Keys.ENTER).perform()
                    log.mjLog.LogReporter("PeopleGroup", "info", "call_by_pressing_enter -"
                                          " "+username+" selected and ENTER pressed")
                    break
                else:
                    self.press_up_down_arrow("down")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "call_by_pressing_enter"
                                  " - Error while either selecting user or pressing"
                                  " ENTER "+str(sys.exc_info()))
            raise
            
    def call_contact_by_double_click_people(self,searchItem):
        '''
           Author : Iswarya
           Double click on contact to make a call
           parameter = searchItem
        '''
        try:
            peopleList=self._browser.elements_finder("peoples_panel_customer_name")
            #peopleList=self._browser.elements_finder("people_full_name")
            print(peopleList)
            for name in peopleList:
                print("*********************")
                personName=name.text
                print(name.text)
                print(personName)
                personName = personName.replace(' ', '')
                time.sleep(5)
                if (personName==searchItem):
                    print("********")
                    x = self._browser.get_current_browser()
                    time.sleep(3)
                    #self.webAction.double_click_element(name)
                    ActionChains(x).double_click(name).perform()
                    #self.webAction.click_element("default_doubleclick")
                    #time.sleep(6)
                    log.mjLog.LogReporter("PeopleGroup","info","call_contact_by_double_click - "+personName+" done")
                    break;
        except:
            log.mjLog.LogReporter("PeopleGroup","error","Error while call_contact_by_double_click "+str(sys.exc_info()))
            raise
            
    def call_contact_by_double_click(self,searchItem):
        '''
           Author : Iswarya
           Double click on contact to make a call
           parameter = searchItem
        '''
        try:
            peopleList=self._browser.elements_finder("peoples_panel_customer_name")
            for name in peopleList:
                person_name_lit = map(str, name.text.split("\n"))
                personName = " ".join(map(str.strip, person_name_lit))
                if (personName==searchItem):
                    x = self._browser.get_current_browser()
                    ActionChains(x).double_click(name).perform()
                    log.mjLog.LogReporter("PeopleGroup","info","call_contact_by_double_click - "+personName+" done")
                    break
        except:
            try:
                log.mjLog.LogReporter("PeopleGroup","info","call_contact_by_double_click - Clicking Second Time")
                peopleList=self._browser.elements_finder("peoples_panel_customer_name")
                for name in peopleList:
                    person_name_lit = map(str, name.text.split("\n"))
                    personName = " ".join(map(str.strip, person_name_lit))
                    if (personName==searchItem):
                        x = self._browser.get_current_browser()
                        ActionChains(x).double_click(name).perform()
                        log.mjLog.LogReporter("PeopleGroup","info","call_contact_by_double_click - "+personName+" done")
                        break
            except:
                log.mjLog.LogReporter("PeopleGroup","error","Error while call_contact_by_double_click "+str(sys.exc_info()))
                raise

    def verify_INCALL(self, params):
        """
        author:prashanth
        verify_INCALL() - This method verifies the call in dashbaord & the contact card of the user who is in call
        parameter : user=user1 callprogress=yes callend=yes
        """
        try:
            if "callprogress" in params.keys() and params["callprogress"] != '':
                self.assertElement.element_should_be_displayed("first_panel_end_call")
                self.assertElement.page_should_contain_text(params["user"])
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call in progress")

            elif "click" in params.keys() and params["click"] != '':
                # self.webAction.click_element("default_client_pane_user1")
                self.webAction.click_element("default_client_pane_timer1")
            elif "callhold" in params.keys() and params["callhold"] != '':
                self.assertElement.page_should_contain_text("Calls")
                self.assertElement.page_should_contain_text(params["user"])
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call in progress")


            elif "callconference" in params.keys() and params["callconference"] != '':
                self.assertElement.page_should_contain_text("Calls")
                self.assertElement.page_should_contain_text(params["user"])
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call in progress")

            elif "callconsult" in params.keys() and params["callconsult"] != '':
                self.assertElement.page_should_contain_text("Calls")
                self.assertElement.page_should_contain_text(params["count"])
                # self.assertElement.page_should_contain_text("ON HOLD")
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call in progress")

            elif "callend" in params.keys() and params["callend"] != '':
                self.queryElement.element_not_displayed("first_panel_end_call")
                self.assertElement.page_should_not_contain_text(params["user"])
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call ended")

            elif "silentmonitor" in params.keys() and params["silentmonitor"] != '':
                # self.queryElement.element_not_displayed("default_client_pane_timer")
                self.assertElement.page_should_contain_text("Silent Monitor")
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call ended")

            elif "silentcoach" in params.keys() and params["silentcoach"] != '':
                # self.queryElement.element_not_displayed("default_client_pane_timer")
                self.assertElement.page_should_contain_text("Silent Coach")
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call ended")

            elif "whisperpage" in params.keys() and params["whisperpage"] != '':
                # self.queryElement.element_not_displayed("default_client_pane_timer")
                # self.assertElement.page_should_not_contain_text("Whisper Page")
                log.mjLog.LogReporter("PeopleGroup", "info", "verify_INCALL - verified the call ended")

            else:
                raise
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "verify_INCALL -error in verifying the call"
                                                          " error " + str(sys.exc_info()))
            raise
            
    def press_up_down_arrow(self,arrow_option):
        '''
           Author : Iswarya
           press_up_down_arrow- presses arrow_down or arrow_up based on arrow_option
           arrow_option=up/down
        '''
        try:
            x = self._browser.get_current_browser()
            if(arrow_option=="up"):
                ActionChains(x).send_keys(Keys.ARROW_UP).perform()
            elif (arrow_option=="down"):
                ActionChains(x).send_keys(Keys.ARROW_DOWN).perform()
            log.mjLog.LogReporter("PeopleGroup","info","press_up_down_arrow - done")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","press_up_down_arrow"+str(sys.exc_info()))
            raise
        
    def check_user_attribute_present(self,params):
        """
        check_user_attribute_present() - This method checks if an attribute is present in third panel of user info
        """
        try:
            if params["option"]=="info":
                self.webAction.explicit_wait("third_panel_info") 
                self.assertElement.element_should_be_displayed("third_panel_info")
                self.webAction.explicit_wait("third_panel_user")
                self.assertElement.element_should_be_displayed("third_panel_user")
                user = self.queryElement.get_text("third_panel_user")
                if "username" in params.keys():
                    if params["username"] == user:
                        log.mjLog.LogReporter("PeopleGroup", "info", "check_user_attribute_present"
                                          " - User is getting displayed")
                self.webAction.explicit_wait("third_panel_extn")
                self.assertElement.element_should_be_displayed("third_panel_extn")
                extension = self.queryElement.get_text("third_panel_extn")
                if "extn" in params.keys():
                    if params["extn"] in extension:
                        log.mjLog.LogReporter("PeopleGroup", "info", "check_user_attribute_present"
                                          " - extension is getting displayed")
            elif params["option"]=="sip_info":
                self.webAction.explicit_wait("third_panel_info") 
                self.assertElement.element_should_be_displayed("third_panel_info")
                self.webAction.explicit_wait("third_panel_user")
                self.assertElement.element_should_be_displayed("third_panel_user")
                user = self.queryElement.get_text("third_panel_user")
                if "username" in params.keys():
                    if params["username"] == user:
                        log.mjLog.LogReporter("PeopleGroup", "info", "check_user_attribute_present"
                                          " - User is getting displayed")   
            elif params["option"]=="call":
                print("in call")
                self.webAction.explicit_wait("third_panel_answer_call")
                self.assertElement.element_should_be_displayed("third_panel_answer_call")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - call attribute is present")
            elif params["option"]=="min":
                self.webAction.explicit_wait("third_panel_minimize_button")
                self.assertElement.element_should_be_displayed("third_panel_minimize_button")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - minimize attribute is present")
            elif params["option"]=="timer":
                self.assertElement.element_should_be_displayed("third_panel_call_timer")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - timer attribute is present")
            elif params["option"]=="endCall":
                self.assertElement.element_should_be_displayed("third_panel_end_call")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - end call attribute is present")
            elif params["option"]=="holdCall":
                self.assertElement.element_should_be_displayed("third_panel_hold_call")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - hold call attribute is present")
            elif params["option"]=="mute":
                self.assertElement.element_should_be_displayed("third_panel_mute")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - mute attribute is present")
            elif params["option"]=="video":
                self.assertElement.element_should_be_displayed("third_panel_video")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - video attribute is present")
            elif params["option"]=="share":
                self.assertElement.element_should_be_displayed("third_panel_share")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - share attribute is present")
            elif params["option"]=="conf":
                self.assertElement.element_should_be_displayed("third_panel_conf")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - add conference attribute is present")
            elif params["option"]=="transfer":
                self.assertElement.element_should_be_displayed("third_panel_transfer")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - transfer attribute is present")
            elif params["option"]=="record":
                self.assertElement.element_should_be_displayed("third_panel_record")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - record attribute is present")
            elif params["option"]=="callmove":
                self.assertElement.element_should_be_displayed("Third_panel_callmove")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - call move attribute is present")	
            elif params["option"]=="additionaloption":
                self.assertElement.element_should_be_displayed("Third_panel_additional_option")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - additional option attribute is present")	
            elif params["option"]=="transferdisabled":
                self.assertElement.element_should_be_displayed("Third_panel_transfer_disabled")
                log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_present - transfer-diasable attribute is present")
            else:
                raise AssertionError("wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","check_user_attribute_present - Failed to check user attribute"+str(sys.exc_info()))
            raise
            
    def check_user_attribute_not_present(self,params):
        """
        check_user_attribute_not_present() - This method checks if an attribute is not present in third panel of user info
        """
        try:
            if params["option"]=="info":
                value=self.queryElement.element_not_displayed("third_panel_info")
                print("@@@@@@@@@@Value is ", value)
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - info attribute is not present")
                else:
                    raise AssertionError("info attribute is present")
            elif params["option"]=="call":
                value=self.queryElement.element_not_displayed("third_panel_answer_call")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - call attribute is not present")
                else:
                    raise AssertionError("call attribute is present")
            elif params["option"]=="min":
                value=self.queryElement.element_not_displayed("third_panel_minimize_button")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - minimize attribute is not present")
                else:
                    raise AssertionError("minimize attribute is present")
            elif params["option"]=="timer":
                value=self.queryElement.element_not_displayed("third_panel_call_timer")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - timer attribute is not present")
                else:
                    raise AssertionError("timer attribute is present")
            elif params["option"]=="endCall":
                value=self.queryElement.element_not_displayed("third_panel_end_call")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - end call attribute is not present")
                else:
                    raise AssertionError("end call attribute is present")
            elif params["option"]=="holdCall":
                value=self.queryElement.element_not_displayed("third_panel_hold_call")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - hold call attribute is not present")
                else:
                    raise AssertionError("hold call attribute is present")
            elif params["option"]=="mute":
                value=self.queryElement.element_not_displayed("third_panel_mute")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - mute attribute is not present")
                else:
                    raise AssertionError("mute attribute is present")
            elif params["option"]=="video":
                value=self.queryElement.element_not_displayed("third_panel_video")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - video attribute is not present")
                else:
                    raise AssertionError("video attribute is present")
            elif params["option"]=="share":
                value=self.queryElement.element_not_displayed("third_panel_share")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - share attribute is not present")
                else:
                    raise AssertionError("share attribute is present")
            elif params["option"]=="conf":
                value=self.queryElement.element_not_displayed("third_panel_conf")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - add conference attribute is not present")
                else:
                    raise AssertionError("add conference attribute is present")
            elif params["option"]=="transfer":
                value=self.queryElement.element_not_displayed("third_panel_transfer")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - transfer attribute is not present")
                else:
                    raise AssertionError("transfer attribute is present")
            elif params["option"]=="record":
                value=self.queryElement.element_not_displayed("third_panel_record")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - record attribute is not present")
                else:
                    raise AssertionError("record attribute is present")
            elif params["option"]=="holdIcon":
                value=self.queryElement.element_not_displayed("third_panel_on_hold_icon")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - On hold attribute is not present")
                else:
                    raise AssertionError("On hold attribute is present")
            elif params["option"]=="unHold":
                value=self.queryElement.element_not_displayed("third_panel_unhold_call")
                if value:
                    log.mjLog.LogReporter("PeopleGroup","info","check_user_attribute_not_present - unhold button is not present")
                else:
                    raise AssertionError("unhold button is present")
            else:
                raise AssertionError("wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","check_user_attribute_not_present - Failed to check user attribute"+str(sys.exc_info()))
            raise
            
    def start_call(self):
        """
        start_call() - This method clicks on call button to place a call
        """
        try:
            self.webAction.explicit_wait("third_panel_answer_call")
            self.webAction.click_element("third_panel_answer_call")
            self.webAction.explicit_wait("first_panel_end_call")
            log.mjLog.LogReporter("PeopleGroup", "info", "start_call - Call placed successfully")
        except:
            try:
                log.mjLog.LogReporter("PeopleGroup", "info", "start_call - Clicking Second time")
                self.webAction.explicit_wait("third_panel_answer_call")
                self.webAction.click_element("third_panel_answer_call")
                self.webAction.explicit_wait("first_panel_end_call")
                log.mjLog.LogReporter("PeopleGroup", "info", "start_call - Call placed successfully")
            except:
                log.mjLog.LogReporter("PeopleGroup", "error", "start_call -"
                                      " Failed to click on start call button "+str(sys.exc_info()))
                raise
        
    def start_call_by_pressing_enter(self):
        try:
            autoit.win_activate("Mitel Connect")
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]",
                                "Chrome_RenderWidgetHostHWND1", "{ENTER}")
        except:
            raise
    
    def end_call(self):
        """
        end_call() - This method clicks on call button to end a call
        """
        try:
            time.sleep(2)
            self.webAction.explicit_wait("third_panel_end_call")
            self.webAction.click_element("third_panel_end_call")
            log.mjLog.LogReporter("PeopleGroup","info","end_call - Call ended successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","end_call - Failed to click on end call button "+str(sys.exc_info()))
            raise
            
    def end_call_dashboard(self):
        """
        end_call_dashboard() - This method clicks on end call button in dashboard
        """
        try:
            time.sleep(2)
            self.webAction.explicit_wait("first_panel_end_call")
            self.webAction.click_element("first_panel_end_call")
            log.mjLog.LogReporter("PeopleGroup","info","end_call - Call ended successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","end_call - Failed to click on end call button "+str(sys.exc_info()))
            raise
        
    def receive_call(self, params):
        """
        receive_call() - This method clicks on call button to receive a call
        """
        try:
            if "pos" in params.keys():
                call_to_be_answered = "first_panel_recvCall" + params["pos"]
                self.webAction.explicit_wait(call_to_be_answered)
                self.webAction.click_element(call_to_be_answered)
            else:
                #time.sleep(2)  # self.webAction.explicit_wait("default_recieve_call") is not working
                self.webAction.explicit_wait("default_recieve_call")
                self.webAction.click_element("default_recieve_call")
            log.mjLog.LogReporter("PeopleGroup","info","receive_call - Call received successfully")
        except:
            try:
                log.mjLog.LogReporter("PeopleGroup","info","receive_call - Attempting Second Time")
                self.webAction.explicit_wait("default_recieve_call")
                self.webAction.click_element("default_recieve_call")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "receive_call - Call received successfully")
            except:
                log.mjLog.LogReporter("PeopleGroup","error","receive_call - "
                                      "Failed to click on receive call button "+str(sys.exc_info()))
                raise

    def transfer_call(self, params):
        """
        transfer_call() - This method clicks on transfer call button to transfer a call
        change list: added if condition for verifying transfer(UKumar: 17-Aug-2016)
        """
        try:
            
            if "click" in params.keys():
                self.webAction.click_element("default_call_section")    
            
            self.webAction.click_element("third_panel_transfer")
            time.sleep(1)
            self.webAction.input_text("third_panel_transfer_input", params["user"])
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_user")
            #self.webAction.click_element("third_panel_conf_user")
            time.sleep(3)
            self.webAction.click_element("third_panel_transfer_click")
            log.mjLog.LogReporter("PeopleGroup","info","transfer_call - Call transferred successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","transfer_call - Failed to click on transfer call button "+str(sys.exc_info()))
            raise AssertionError("Failed to transfer call")
    
    def did_to_did_transfer(self, params):
        """
        Author: UKumar
        did_to_did_transfer() - This method clicks on transfer call button,
        enters DID number and clicks on transfer button
        Parameters: did
        """
        try:  
            if "click" in params.keys():
                self.webAction.click_element("default_call_section")
            self.webAction.click_element("third_panel_transfer")
            time.sleep(1)
            self.webAction.input_text("third_panel_transfer_input", params["did"])
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_click")
            log.mjLog.LogReporter("PeopleGroup","info","did_to_did_transfer"
                                " - clicked on transfer button")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","did_to_did_transfer"
                        " - Failed to click on transfer call button "+str(sys.exc_info()))
            raise AssertionError("Failed to transfer call")
            
    def trans_contact_check(self, params):
        """
        trans_contact_check() - This method clicks on transfer call button to transfer a call
        """
        try:
            self.webAction.click_element("third_panel_transfer")
            time.sleep(1)
            list = self._browser.elements_finder("TP_transfer_contact_option") 

            for i in list:
                if i.text.lower() != params["user"].lower():
                    raise AssertionError(params["user"]+" not present in recent contacts")
            log.mjLog.LogReporter("PeopleGroup", "info", "trans_contact_check - "
                                "Call transfered contacts checked successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "trans_contact_check - "
                                "Failed to check the contact in transfer dashboard "+str(sys.exc_info()))
            raise
            
    def blank_transfer_call(self):
        """
        blank_transfer_call() - This method clicks on transfer call button without selecting any user
        change list: added statement to press ENTER (UKumar: 22-Aug-2016)
        """
        try:
            self.webAction.click_element("third_panel_transfer")
            time.sleep(1)
            self.webAction.press_key("third_panel_transfer_input", "RETURN")
            log.mjLog.LogReporter("PeopleGroup", "info", "blank_transfer_call - "
                                "Pressed ENTER without selecting any user successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","blank_transfer_call - Failed to do blank transfer "+str(sys.exc_info()))
            raise AssertionError("Failed to press ENTER")

    def intercom_transfer(self, params):
        """
        Author: UKumar
        intercom_transfer() - To do Intercom transfer
        Parameters: user
        """
        try:
            self.webAction.click_element("third_panel_transfer")
            self.webAction.explicit_wait("third_panel_transfer_input")
            self.webAction.input_text("third_panel_transfer_input", params["user"])
            self.webAction.explicit_wait("third_panel_transfer_user")
            self.webAction.click_element("third_panel_transfer_user")
            self.webAction.explicit_wait("TP_transfer_intercom")
            self.webAction.click_element("TP_transfer_intercom")
            log.mjLog.LogReporter("PeopleGroup", "info", "intercom_transfer - clicked on intercom")
            self.webAction.explicit_wait("TP_transfer_intercom_complete")
            self.webAction.click_element("TP_transfer_intercom_complete")
            log.mjLog.LogReporter("PeopleGroup", "info", "intercom_transfer - Intercom transfer completed")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "intercom_transfer"
                                                          " - Failed to do Intercom transfer " + str(sys.exc_info()))
            raise

    def intercom_conference(self, params):
        """
        Author: UKumar
        intercom_conference() - To do Intercom transfer
        Parameters: user
        """
        try:
            self.webAction.click_element("third_panel_conf")
            self.webAction.explicit_wait("third_panel_conference_text")
            self.webAction.input_text("third_panel_conference_text", params["user"])
            self.webAction.explicit_wait("TP_chat_add_participants_user")
            self.webAction.click_element("TP_chat_add_participants_user")
            self.webAction.explicit_wait("TP_conf_intercom")
            self.webAction.click_element("TP_conf_intercom")
            log.mjLog.LogReporter("PeopleGroup", "info", "intercom_conference - Intercom transfer completed")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "intercom_conference"
                                                          " - Failed to do Intercom conference " + str(sys.exc_info()))
            raise
            
    def conference_call(self, params):
        """
        conference_call() - This method clicks on conference call button to start a conference call
        """
        try:
            self.webAction.click_element("third_panel_conf")
            time.sleep(1)
            self.webAction.input_text("third_panel_conf_input", params["user"])
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_user")
            time.sleep(1)
            #self.webAction.click_element("third_panel_conf_click")
            self.webAction.click_element("third_panel_conference_select")
            #self.webAction.explicit_wait("third_panel_on_hold_icon")
            log.mjLog.LogReporter("PeopleGroup", "info", "conference_call - Conference call started successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "conference_call - "
                                "Failed to click on conference call button "+str(sys.exc_info()))
            raise
            
    def consult_conference_call(self, params):
        """
        Author: UKumar
        consult_conference_call() - This method clicks on conference button then adds
                user to conference and clicks on consult button for consult conference
        Parameters: no parameter
        """
        try:
            self.webAction.click_element("third_panel_conf")
            time.sleep(1)
            self.webAction.input_text("third_panel_conf_input", params["user"])
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_user")
            time.sleep(1)
            self.webAction.click_element("TP_consult_conference_button")
            
            log.mjLog.LogReporter("PeopleGroup", "info", "consult_conference_call -"
                                " clicked on Consult button for Consult Conference")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "consult_conference_call -"
                                " Failed to click on Consult button "+str(sys.exc_info()))
            raise
    
    def did_to_did_conference(self, params):
        """
        did_to_did_conference() - This method clicks on conference call button to start a conference call using DIDs
        """
        try:
            self.webAction.click_element("third_panel_conf")
            self.webAction.explicit_wait("third_panel_conf_input")
            self.webAction.input_text("third_panel_conf_input", params["did"])
            self.webAction.click_element("third_panel_conference_select")
            log.mjLog.LogReporter("PeopleGroup","info","did_to_did_conference"
                                " - Clicked on Conference button for DID to DID  call")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","did_to_did_conference - "
                "Failed to click on conference button for DID to DID call "+str(sys.exc_info()))
            raise

    def consult_transfer(self, params):
        """
        consult_transfer() - This method clicks on transfer call button to transfer a call
        """
        try:
            time.sleep(3)
            self.webAction.click_element("third_panel_transfer")
            time.sleep(2)
            self.webAction.input_text("third_panel_transfer_input", params["user"])
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_user")
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_consult")
            log.mjLog.LogReporter("PeopleGroup", "info", "consult_transfer - Call consulted successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "consult_transfer - Failed to click"
                                                          " on consult transfer call button " + str(sys.exc_info()))
            raise

    def end_transfer_call(self):
        """
        end_transfer_call() - This method clicks on call button to end a call
        """
        try:
            self.webAction.click_element("default_end_transfer_call")
            log.mjLog.LogReporter("PeopleGroup","info","end_transfer_call - Call ended successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","end_transfer_call - Failed to click on end call button "+str(sys.exc_info()))
            raise

    def complete_consult(self):
        """
        complete_consult()-This method will complete the call consulting.
        """
        try:
            self.assertElement.element_should_be_displayed("third_panel_complete_consult_on_hold")
            self.assertElement.element_should_be_displayed("third_panel_consulting")
            self.webAction.click_element("third_panel_complete_consult")
            log.mjLog.LogReporter("PeopleGroup", "info", "complete_consult - Clicked on"
                                                         " complete consult button")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "complete_consult - Failed to"
                                                          " click on complete consult button" + str(sys.exc_info()))
            raise

    def cancel_consult(self):
        """
        cancel_consult()-This method will cancel the call consulting.
        """
        try:
            self.assertElement.element_should_be_displayed("third_panel_complete_consult_on_hold")
            self.assertElement.element_should_be_displayed("third_panel_consulting")
            self.webAction.click_element("third_panel_cancel_consult")
            log.mjLog.LogReporter("PeopleGroup", "info", "cancel_consult - Clicked on cancel consult button")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "cancel_consult -"
                                " Failed to click on cancel consult button" + str(sys.exc_info()))
            raise
            
    def cancel_consult_dashboard(self):
        """
        Author: ITripathi
        cancel_consult_dashboard(): Clicks on cancel button in dashboard during consult call
        Parameter: no parameter
        """
        try:
            self.webAction.explicit_wait("FP_cancel_consult_dashboard")
            self.webAction.click_element("FP_cancel_consult_dashboard")
            log.mjLog.LogReporter("PeopleGroup", "info", "cancel_consult_dashboard - Clicked on cancel consult button on dashboard")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "cancel_consult_dashboard -"
                                  " Failed to click on cancel consult button on dashboard " + str(sys.exc_info()))
            raise
            
    def hold_call(self):
        """
        hold_call() - This method clicks on hold call button to hold the current call
        """
        try:
            self.webAction.click_element("third_panel_hold_call")
            log.mjLog.LogReporter("PeopleGroup","info","hold_call - Clicked on hold call successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","hold_call - Failed to click on hold button "+str(sys.exc_info()))
            raise

    def un_hold_call(self):
        """
        un_hold_call() - This method clicks on unhold(resume) call button to unhold the on hold call
        """
        try:
            self.webAction.click_element("third_panel_unhold_call")
            log.mjLog.LogReporter("PeopleGroup","info","un_hold_call - Clicked on unhold call successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","un_hold_call - Failed to click on unhold button "+str(sys.exc_info()))
            raise
            
    def mute_unmute_call(self, params):
        """
        mute_unmute_call() - This method clicks on mute button to put call on mute or unmute
        """
        try:
            if params["option"] == "mute":
                self.webAction.click_element("third_panel_mute")
                log.mjLog.LogReporter("PeopleGroup", "info", "mute_unmute_call - Clicked on mute button")
            else:
                self.webAction.click_element("third_panel_mute")
                log.mjLog.LogReporter("PeopleGroup", "info", "mute_unmute_call - Clicked on unmute button")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","mute_unmute_call - Error: "+str(sys.exc_info()))
            raise
            
    def to_voice_mail(self):
        """
        to_voice_mail() - This method clicks on voice mail button to move the call to voice mail
        """
        try:
            self.webAction.click_element("default_voicemail")
            time.sleep(20)
            log.mjLog.LogReporter("PeopleGroup","info","to_voice_mail - clicked on voice mail successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","to_voice_mail - Failed to click on voice mail "+str(sys.exc_info()))
            raise
            
    def whisper_transfer(self, params):
        """
        whisper_transfer() - This method clicks on whisper transfer button to transfer a call
        """
        try:
            time.sleep(3)
            self.webAction.click_element("third_panel_transfer")
            time.sleep(2)
            self.webAction.input_text("third_panel_transfer_input", params["user"])
            time.sleep(1)
            self.webAction.click_element("third_panel_transfer_user")
            time.sleep(1)
            self.webAction.click_element("Tp_transfer_toWhisper")
            log.mjLog.LogReporter("PeopleGroup", "info", "whisper_transfer - Call consulted successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "whisper_transfer - Failed to click"
                                  " on whisper transfer call button "+str(sys.exc_info()))
            raise

    def video_call(self):
        """
        video_call()-This method will do a video call.
        """
        try:
            self.assertElement.element_should_be_displayed("FP_videocall")
            self.webAction.click_element("FP_videocall")
            log.mjLog.LogReporter("PeopleGroup", "info", "cancel_consult - Clicked on video button")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "cancel_consult - Failed to click on video button" + str(sys.exc_info()))
            raise

    def click_mute_button(self, params):
        '''
        click_mute_button- This API clicks on mute button
        '''
        try:
            if "mute" in params.keys():
                self.webAction.click_element("third_panel_mute")
                self.assertElement.element_should_be_displayed("Tp_unmute")
                log.mjLog.LogReporter("PeopleGroup", "info", "click_mute_button - Unmute button is getting displayed")
            elif "unmute" in params.keys():
                self.webAction.click_element("Tp_unmute")
                self.assertElement.element_should_be_displayed("third_panel_mute")
                log.mjLog.LogReporter("PeopleGroup", "info", "click_mute_button - Mute button is getting displayed")
            else:
                log.mjLog.LogReporter("PeopleGroup", "info", "click_mute_button - Nothing to be checked displayed")
            log.mjLog.LogReporter("PeopleGroup", "info", "click_mute_button - Clicked mute button succesfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "click_mute_button - Failed to click mute button " + str(sys.exc_info()))
            raise

    def blind_audio_conference(self, params):
        """
        Author: Iswarya,modified by prashanth for consult call
        blind_audio_conference() - This method clicks on conference and adds a third user to conference
        """
        try:
            print("#########,params ", params)
            # firstNameList=self._browser.elements_finder("first_panel_blindusers")
            if "verify" in params.keys():
                time.sleep(2)
                self.webAction.click_element("third_panel_conf")
                time.sleep(2)
                self.webAction.click_element("third_panel_conference_text")
                # self.webAction.input_text("third_panel_conference_text",params["user"])
                time.sleep(4)
                self.assertElement.element_should_be_displayed("first_panel_in_meeting")
                self.assertElement.element_should_be_displayed("first_panel_available")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "blind_audio_conference - verified the status successfully")

            elif "verifymeeting" in params.keys():
                self.webAction.click_element("third_panel_conf")
                time.sleep(2)
                self.webAction.click_element("third_panel_conference_text")
                # self.webAction.input_text("third_panel_conference_text",params["user"])
                time.sleep(4)
                self.assertElement.element_should_be_displayed("first_panel_in_meeting")
                self.assertElement.element_should_be_displayed("first_panel_out_office")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "blind_audio_conference - verified the status successfully")

            elif "verifynames" in params.keys():
                self.webAction.click_element("third_panel_conf")
                time.sleep(2)
                self.webAction.click_element("third_panel_conference_text")
                # self.webAction.input_text("third_panel_conference_text",params["user"])
                time.sleep(4)
                self.assertElement.element_should_be_displayed("first_panel_contacts")
                self.assertElement.page_should_contain_text(params["user1"])
                self.assertElement.page_should_contain_text(params["user2"])
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "blind_audio_conference - verified the status successfully")


            elif "changeavailable" in params.keys():
                self.webAction.click_element("third_panel_conf")
                time.sleep(2)
                self.assertElement.element_should_be_displayed("first_panel_available")



            elif "change" in params.keys():
                self.webAction.click_element("third_panel_conf")
                time.sleep(2)
                self.assertElement.element_should_be_displayed("first_panel_out_office")

            elif "consult" in params.keys():
                self.webAction.click_element("third_panel_conf")
                self.webAction.explicit_wait("third_panel_conference_text")
                self.webAction.input_text("third_panel_conference_text", params["user"])
                time.sleep(1)
                self.webAction.click_element("third_panel_conference_user")
                time.sleep(1)
                self.webAction.click_element("third_panel_blind_cons_click")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "blind_audio_conference - conference blind transferred successfully")

            elif "external" in params.keys():
                if "click" in params.keys():
                    self.webAction.click_element("default_call_section")
                    print("#################Clicked on call$$$$$$$$$$$$$$$$$$$$$$")

                self.webAction.click_element("third_panel_conf")
                time.sleep(2)
                self.webAction.click_element("third_panel_conference_text")
                time.sleep(2)
                self.webAction.input_text("third_panel_conference_text", params["user"])
                time.sleep(1)
                # if "external" in params.keys():
                # print("###################Entering for loop####################",firstNameList)
                # for name in firstNameList:
                # print("firstNameList is &&&&&&&&&&&",firstNameList)
                # print("######name is###############",name)
                # numbers = name.text.split("\n")[1]
                # print("######numbers are###############",numbers)
                # temp = params["user"]
                # actual = "(" + temp[:3] + ") " + temp[3:6] + "-" + temp[6:]
                # if (actual == numbers):
                # log.mjLog.LogReporter("verify_twotimes_forward_call","info","user external number appearing")
                # name.click()
                # break
                #self.webAction.click_element("first_panel_blindusers")
                time.sleep(1)
                self.webAction.click_element("third_panel_blind_conf_click")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "blind_audio_conference - conference blind transferred successfully")

            else:
                if "click" in params.keys():
                    self.webAction.click_element("default_call_section")
                    print("#################Clicked on call$$$$$$$$$$$$$$$$$$$$$$")
                print("#################Entered blind$$$$$$$$$$$$$$$$$$$$$$")
                time.sleep(2)
                self.webAction.click_element("third_panel_conf")
                print("#################cliecked third conf$$$$$$$$$$$$$$$$$$$$$$")
                time.sleep(2)
                self.webAction.click_element("third_panel_conference_text")
                print("#################clicked textbox$$$$$$$$$$$$$$$$$$$$$$")
                time.sleep(2)
                self.webAction.input_text("third_panel_conference_text", params["user"])
                print("#################Entered textbox$$$$$$$$$$$$$$$$$$$$$$")
                time.sleep(1)
                self.webAction.click_element("third_panel_conference_user")
                time.sleep(1)
                self.webAction.click_element("third_panel_blind_conf_click")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "blind_audio_conference - conference blind transferred successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "blind_audio_conference - Failed to blind transfer conference call button " + str(
                                      sys.exc_info()))
            raise

    def open_own_user_preferences(self):
        '''
           Author: Gautham modified by Uttam
           open_own_user_preferences() - To open own user preferences window  
           parameters:
           ex: open_own_user_preferences
        
        '''
        try:
            #time.sleep(3)
            log.mjLog.LogReporter("PeopleGroup","info","open_own_user_preferences- To open own user preferences window")
            if self.queryElement.element_not_displayed("people_preferences"):
                time.sleep(3)
                self.webAction.click_element("default_own_name")
                time.sleep(2)
            self.webAction.explicit_wait("people_preferences")
            self.webAction.click_element("people_preferences")
            log.mjLog.LogReporter("PeopleGroup", "info", "open_own_user_preferences"
                                                         " - Preference window opened successfully")
            # time.sleep(2)
                        # self.webAction.switch_to_window(1)
            # if self.queryElement.text_present("Loading preferences data. Please hold on..."):
                # log.mjLog.LogReporter("PeopleGroup","info","open_own_user_preferences - "
                                      # "Preference window opened successfully with message")
            # else:
                # log.mjLog.LogReporter("PeopleGroup", "info", "open_own_user_preferences - "
                                      # "Preference window opened successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "open_own_user_preferences - "
                                  "Failed to open preferences window"+str(sys.exc_info()))
            raise

    def verify_people_panel(self, option):
        """
        Author: UKumar
        verify_second_panel() - Verifies that second panel, People tab is opened or not
        Parameters: option
        """
        try:

            status = self.queryElement.element_not_displayed("peoples_group")
            if not status and option == "present":
                log.mjLog.LogReporter("PeopleGroup", "info", " verify_people_panel"
                                                             " - People panel is opened")
            elif not status and option == "absent":
                raise AssertionError("People panel is opened")
            elif status and option == "absent":
                log.mjLog.LogReporter("PeopleGroup", "info", " verify_people_panel"
                                                             " - People panel is not opened")
            else:
                raise AssertionError("People panel is not opened")
        except:
            log.mjLog.LogReporter("PeopleGroup", "info", " verify_people_panel -"
                                                         "failed to verify People panel " + str(sys.exc_info()))
            raise

    def accept_screen_share(self, join_how):
        """
        Author: UKumar
        accept_screen_share(): This API accept sharing either by pressing
            'green join button' in dashboard or by pressing 'View Screen Share'
            button (sharing started after chat)
        Parameters: join_how
        """
        try:
            if join_how == "accept_share_popup":
                try:
                    self.webAction.explicit_wait("TP_Accept_Share_From_Popup")
                    self.webAction.click_element("TP_Accept_Share_From_Popup")
                except:
                    raise AssertionError("Not able to click on accept Share button from popup" + str(sys.exc_info()))
            elif join_how == "green_join_button":
                try:
                    self.webAction.explicit_wait("default_accept_share")
                    self.webAction.mouse_hover("default_accept_share")
                    self.webAction.click_element("default_accept_share")
                except:
                    raise AssertionError("Not able to click on accept Share button from dashboard" + str(sys.exc_info()))
                log.mjLog.LogReporter("PeopleGroup", "info", "accept_screen_share"
                                                             " - accepted screen share by pressing green join button")
            else:
                self.webAction.explicit_wait("third_panel_share")
                self.webAction.click_element("third_panel_share")
                self.webAction.explicit_wait("TP_Accept_ScreenShare")
                self.webAction.click_element("TP_Accept_ScreenShare")
                log.mjLog.LogReporter("PeopleGroup", "info", "accept_screen_share"
                                                             " - accepted screen share by pressing View Screen Share button")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "accept_screen_share"
                                                          " - failed to accept screen share " + str(sys.exc_info()))
            raise

    def park_transfer_call(self, user):
        """
        Author:Manoj
        park_transfer_call() - This method clicks on transfer call button to park transfer a call
        change list: minimize delay (UKumar: 13-Jan-2017)
        """
        try:
            self.webAction.click_element("third_panel_transfer")
            self.webAction.explicit_wait("third_panel_transfer_input")
            self.webAction.input_text("third_panel_transfer_input", user)
            self.webAction.explicit_wait("third_panel_transfer_user")
            self.webAction.click_element("third_panel_transfer_user")
            self.webAction.explicit_wait("third_panel_transfer_park")
            self.webAction.click_element("third_panel_transfer_park")
            log.mjLog.LogReporter("PeopleGroup", "info", "park_transfer_call - user added for call park")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "park_transfer_call"
                                " - Failed to click on transfer call button " + str(sys.exc_info()))
            raise

    def end_hold_from_client_pane(self, option):
        """
        end_hold_from_client_pane() - This method clicks on end or hold call button in client pane of the user
        """
        try:
            if option == "hold":
                self.webAction.click_element("default_client_pane_hold_button")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "end_hold_from_client_pane - Clicked on hold call successfully")
            elif option == "end":
                time.sleep(1)
                self.webAction.explicit_wait("first_panel_end_call")
                self.webAction.click_element("first_panel_end_call")
                log.mjLog.LogReporter("PeopleGroup", "info", "end_hold_from_client_pane"
                                                             " - Clicked on end call successfully")
            else:
                raise AssertionError("Wrong argument passed")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "end_hold_from_client_pane "
                                "- Failed to click on " + option + " call button " + str(sys.exc_info()))
            raise
            
    def add_contact_conversation(self, name, checkname):
        """
        Author: Prashanth
        add_contact_conversation() - This API help in joining a contact to conversation
        parameters: name: Name of the contact

        ex: add_contact_conversation name=PUser
        """
        try:
            log.mjLog.LogReporter("PeopleGroup","info","add_contact_conversation - Adding contact to  Conversation")
            self.webAction.click_element("detials_control_adds")
            self.webAction.explicit_wait("TP_add_contact")
            self.webAction.input_text("TP_add_contact", name)
            firstNameList = self._browser.elements_finder("TP_AUTO_CONTACT")
            for names in firstNameList:
                if names.text == checkname:
                    time.sleep(3)
                    names.click()
                    break
            self.webAction.explicit_wait("TP_ADD_CONTACT1")
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_conversation"
                                                         " - able to join Conversation successfully")
            self.webAction.click_element("TP_ADD_CONTACT1")
            log.mjLog.LogReporter("PeopleGroup", "info", "add_contact_conversation"
                                                         " - click on join Conversation successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "add_contact_conversation"
                                                          " - Failed to join Conversation "+str(sys.exc_info()))
            raise

# Newly Add for Sanity
# By UKumar
    def scroll_down_use_keyboard(self, search_item):
        """
        Author: UKumar
        scroll_down_use_keyboard() : Uses down arrow key to scroll through search
                            results and verifies that it is actually scrolling
        Parameters: no parameter
        """
        try:
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            self.webAction.input_text("default_search_input", search_item)
            time.sleep(2) # wait for search results
            self.press_up_down_arrow("down")
            time.sleep(2) # wait for contact card to open
            name1 = self.queryElement.get_text("third_panel_recentlist_name")
            
            self.press_up_down_arrow("down")
            time.sleep(2) # wait for contact card to open
            name2 = self.queryElement.get_text("third_panel_recentlist_name")
            if name1 != name2:
                log.mjLog.LogReporter("PeopleGroup", "info", "scroll_down_use_keyboard"
                                    " - scrolled using down arrow key")
            else:
                raise AssertionError("Failed to scroll!")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "scroll_down_use_keyboard"
                            " - Error: "+str(sys.exc_info()))
            raise

    def show_verify_comp_name(self, info_to_verify):
        """
        Author: UKumar
        show_verify_comp_name() : To click on Show Company Name option after
            right clicking on a searched contact and verify that Phone number is visible
        Parameters: info_to_verify (company name to be verified)
        """
        try:
            info_to_verify = re.sub("\*", " ", info_to_verify)
            comp_name_not_shown = self.queryElement.element_not_displayed("people_right_click_company")
            if comp_name_not_shown:
                self.click_on_options_right_click("Company Name")
                log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_comp_name -"
                                                             " Clicked on 'Show Company Name' to show company name")
            self.assertElement.element_should_contain_text("people_right_click_company", info_to_verify)
            log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_comp_name -"
                                                         " company name is visible")
            self.click_on_options_right_click("Company Name")
            log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_comp_name -"
                                                         " Clicked on 'Show Company Name' to hide company name")
            self.assertElement.element_should_not_be_displayed("people_right_click_company")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "show_verify_comp_name - Error: " + str(sys.exc_info()))
            raise

    def show_verify_dept_name(self, info_to_verify):
        """
        Author: UKumar
        show_verify_dept_name() : To click on Show Department Name option after
            right clicking on a searched contact and verify that Phone number is visible
        Parameters: info_to_verify (department name to be verified)
        """
        try:
            info_to_verify = re.sub("\*", " ", info_to_verify)
            dept_name_not_shown = self.queryElement.element_not_displayed("people_right_click_dept")
            if dept_name_not_shown:
                self.click_on_options_right_click("Department Name")
                log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_dept_name -"
                                                             " Clicked on 'Show Department Name' to show Dept Name")
            self.assertElement.element_should_contain_text("people_right_click_dept", info_to_verify)
            log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_dept_name -"
                                                         " Department Name is visible")
            self.click_on_options_right_click("Department Name")
            log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_dept_name -"
                                                         " Clicked on 'Show Department Name' to hide Department Name")
            self.assertElement.element_should_not_be_displayed("people_right_click_dept")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "show_verify_dept_name - Error: " + str(sys.exc_info()))
            raise

    def show_verify_phone_number(self, info_to_verify):
        """
        Author: UKumar
        show_verify_phone_number() : To click on Show Phone Number option after
            right clicking on a searched contact and verify that Phone number is visible
        Parameters: info_to_verify (phone number to be verified)
        """
        try:
            info_to_verify = re.sub("\*", " ", info_to_verify)
            number_not_shown = self.queryElement.element_not_displayed("people_right_click_number")
            if number_not_shown:
                self.click_on_options_right_click("Phone Number")
                log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_phone_number -"
                                                             " Clicked on 'Show Phone Number' to show phone number")
            self.assertElement.element_should_contain_text("people_right_click_number", info_to_verify)
            log.mjLog.LogReporter("PeopleGroup", "info", "show_verify_phone_number -"
                                                         " phone number is visible")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "show_verify_phone_number - Error: " + str(sys.exc_info()))
            raise

    def hide_contact_info(self, contact_info):
        """
        Author: UKumar
        hide_contact_info(): To click on contact information to hide
        Parameter: contact_info to hide
        """
        try:
            if contact_info.lower() == "phone_number":
                time.sleep(1)
                self.click_on_options_right_click("Phone Number")
                log.mjLog.LogReporter("PeopleGroup", "info", "hide_contact_info -"
                                                             " Clicked on 'Show Phone Number' to hide phone number")
                # self.assertElement.element_should_not_be_displayed("people_right_click_number")
                log.mjLog.LogReporter("PeopleGroup", "info", "hide_contact_info - Phone number is hidden")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "hide_contact_info - FAILED" + str(sys.exc_info()))
            raise

    def click_on_options_right_click(self, option):
        """
        Author: UKumar
        click_on_options_right_click(): To select an option from the context menu after right clicking on a contact
        Parameters: option
        """
        try:
            autoit.win_activate("Mitel Connect")
            option_dict_from_bottom = {"Company Name": 3, "Department Name": 2, "Phone Number": 1}
            self.webAction.right_click("SP_anchor_contact")
            for i in range(0, int(option_dict_from_bottom[option])):
                time.sleep(1)
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "click_on_options_right_click - iteration %s " % i)
                autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{UP}")
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "", "{ENTER}")
            time.sleep(0.5)
            log.mjLog.LogReporter("PeopleGroup", "info", "click_on_options_right_click - Clicked on Show %s " % option)
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "click_on_options_right_click - FAILED" + str(sys.exc_info()))
            raise

# By PC    
    def select_soft_phone(self, params):
        """
        Author: Prashanth
        select_soft_phone(): This API selects the softphone option for a user & also selects the audio card displayed
        parameters: none
        """
        try:
            self.webAction.click_element("FP_softphone")
            # FP_checksoftphone clicks dropdown to select microphone
            self.webAction.explicit_wait("FP_softphone_icon")
            self.webAction.click_element("FP_checksoftphone")
            self.webAction.click_element("FP_selectmicrophone")
            #self.webAction.click_element("FP_selectconference_bridge")

            log.mjLog.LogReporter("PeopleGroup", "info", "select_soft_phone - PASSED")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "select_soft_phone - FAILED" +str(sys.exc_info()))
            raise

    def select_desk_phone(self, params):
        """
        Author: Prashanth
        select_desk_phone(): This API selects Deskphone option for a user
        parameters: none
        """
        try:
            #self.webAction.click_element("FP_selectprimary_assignment")
            self.webAction.click_element("FP_deskphone")
            self.webAction.explicit_wait("FP_deskphone_icon")
            log.mjLog.LogReporter("PeopleGroup", "info", "select_desk_phone - PASSED")
        except:
            try:
                log.mjLog.LogReporter("PeopleGroup", "info", "select_desk_phone - Attempting Second Time ")
                self.webAction.click_element("FP_deskphone")
                self.webAction.explicit_wait("FP_deskphone_icon")
                log.mjLog.LogReporter("PeopleGroup", "info", "select_desk_phone - PASSED")
            except:
                log.mjLog.LogReporter("PeopleGroup", "error", "select_desk_phone - FAILED" + str(sys.exc_info()))
                raise
            
    def add_new_label(self,**params):
        '''
        Author: Ankit modified by manoj modified by prashanth
        add_new_label() - to add a new label and number and verify that numbers are added or not.
        Parameters: label, number, activationType, no_of_rings 
        '''
        try:
            self.webAction.click_element("people_profile_external")
            time.sleep(2)
            if not self.queryElement.element_not_displayed("Edit_External"):
                self.webAction.click_element("Edit_External")
                time.sleep(1)
                self.webAction.click_element("Click_Remove_External")
                time.sleep(1)
                self.webAction.click_element("Click_Remove_External_Link")
                time.sleep(1)           
            self.webAction.click_element("people_profile_external")
            time.sleep(2)
            self.webAction.click_element("people_profile_primary_label1")
            self.webAction.input_text("people_profile_primary_label1", params["label"])
            self.webAction.click_element("people_profile_primary_number1")
            self.webAction.input_text("people_profile_primary_number1", params["number"])

            self.webAction.click_element("people_profile_connect_options1")
            time.sleep(1)

            if params["activationType"] == "1":              
                self.webAction.click_element("External_Automatically_Connect")                

            else:               
                self.webAction.click_element("External_Press_1_Connect")

            self.webAction.click_element("people_number_rings")
            ActionChains(self._browser.get_current_browser()).send_keys(Keys.CLEAR).perform()

            self.webAction.input_text("people_number_rings", params["no_of_rings"])

            self.webAction.click_element("people_select_number")
            if len(params["number"]) <= 5:
                self.assertElement.page_should_contain_text("The number format is incorrect. Please be sure to enter the full number; for example (xxx) xxx-xxxx.")
                log.mjLog.LogReporter("PeopleGroup","info","add_new_label - Expected error message is present - PASS")
            else:
                self.webAction.explicit_wait("people_profile_external")
                log.mjLog.LogReporter("PeopleGroup","info","add_new_label - new label added - PASS")
        except:
            log.mjLog.LogReporter("PeopleGroup","error","add_new_label - unable to add new label - FAIL "+str(sys.exc_info()))
            raise

    def edit_modify_label(self,**params):
        """
        Author: UKumar
        edit_modify_label() - To edit and modify a abel and number added under profile panel
        Parameters: label_to_edit, new_label new_number, activationType, no_of_rings
        """
        try:
            self.webAction.explicit_wait("people_profile_external")
            self.webAction.click_element("people_profile_external")
            self.webAction.click_element("Edit_External")
            if params["label_to_edit"] == "1":
                if "new_label" in params.keys():
                    self.webAction.input_text("people_profile_primary_label1", params["new_label"])
                    log.mjLog.LogReporter("PeopleGroup", "info",
                                          "edit_modify_label - New label name entered")
                if "new_number" in params.keys():
                    self.webAction.input_text("people_profile_primary_number1", params["new_number"])
                    log.mjLog.LogReporter("PeopleGroup", "info",
                                          "edit_modify_label - New number entered")
                # Click to make sure that Activation type and rings to try options are displaying
                time.sleep(1)
                self.webAction.click_element("people_profile_primary_label1")
                time.sleep(2)  #self.webAction.explicit_wait("people_number_rings1")

                self.webAction.click_element("people_profile_connect_options1")
                time.sleep(1)
                if "activationType" in params.keys():
                    if params["activationType"] == "1":                     
                        self.webAction.click_element("External_Automatically_Connect")
                    else:                       
                        self.webAction.click_element("External_Press_1_Connect")
                        time.sleep(2)

                    log.mjLog.LogReporter("PeopleGroup", "info",
                                          "edit_modify_label - new Activation Type entered")
                if "no_of_rings" in params.keys():
                    self.webAction.click_element("people_number_rings1")
                    ActionChains(self._browser.get_current_browser()).send_keys(Keys.CLEAR).perform()
                    self.webAction.input_text("people_number_rings1", params["no_of_rings"])
                    log.mjLog.LogReporter("PeopleGroup", "info",
                                          "edit_modify_label - Number of rings entered")

            self.webAction.click_element("Click_Update_External")
            if ("new_number" in params.keys()) and (len(params["new_number"]) <= 5):
                self.assertElement.page_should_contain_text("we cannot save these number(s). For this"
                                                            " Assigned External please only enter external numbers")
                log.mjLog.LogReporter("PeopleGroup", "info", "edit_modify_label - Expected error message is present - PASS")
            else:
                self.webAction.explicit_wait("people_profile_external")
                log.mjLog.LogReporter("PeopleGroup", "info", "edit_modify_label - label edited and saved - PASS")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "edit_modify_label - unable to edit abel - FAIL "+str(sys.exc_info()))
            raise

    def remove_label(self, label_to_remove):
        """
        Author: UKumar
        remove_label() - To remove the label
        Parameters: label_to_remove
        """
        try:
            self.webAction.click_element("people_profile_external")
            time.sleep(2)
            if label_to_remove == "1":
                self.webAction.click_element("Edit_External")
                time.sleep(1)
                self.webAction.click_element("Click_Remove_External")
                time.sleep(1)
                self.webAction.click_element("Click_Remove_External_Link")
                time.sleep(1)
                log.mjLog.LogReporter("PeopleGroup", "info", "remove_label - Clicked on Remove button")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "remove_label - Failed to remove label "+str(sys.exc_info()))
            raise
            
            
    def drag_drop_transfer_call(self,params):
        """
        blank_transfer_call() - This method clicks on transfer call button without selecting any user
        change list: added statement to press ENTER (UKumar: 22-Aug-2016)
        """
        try:
            log.mjLog.LogReporter("PeopleGroup", "info", "drag_and_move - function entered in people s group ")
            for item in params.items():
                if 'blindTransfer' in item:
                    self.webAction.drag_and_drop("drag_destination","drag_source")
                    log.mjLog.LogReporter("PeopleGroup", "info", "After clicked")
                    
                elif "blindTransferOnCall" in item:
                    log.mjLog.LogReporter("PeopleGroup", "info", "in blindtransfer_oncall")
                    self.webAction.drag_and_drop("drag_source","drag_destination")
          
                elif "groupTransferBlind" in item:
                    self.webAction.drag_and_move("drag_destinationgroup","drag_source")
                    self.webAction.click_element("Blind_Transfer_Menu")
                    
                elif "groupTransferPark" in item:
                    time.sleep(1)
                    self.webAction.drag_and_move("drag_destinationgroup","drag_source")
                    self.webAction.click_element("Park")

                elif "groupConsultTransfer" in item:
                    time.sleep(1)
                    self.webAction.drag_and_move("drag_destinationgroup","drag_source")
                    self.webAction.click_element("Consult_Transfer_Menu")    
                    
                elif "favouriteContactTransfer" in item:
                    self.webAction.drag_and_move("drag_favouritecontact","drag_source")
                    self.webAction.click_element("Intercom_Transfer")
                    
                elif "favouriteContactTransferPark" in item:
                    self.webAction.drag_and_move("drag_favouritecontact","drag_source")
                    self.webAction.click_element("Park")
                    
                elif "whisperTransfer" in item:
                    self.webAction.drag_and_move("drag_favouritecontact","drag_source")
                    time.sleep(5)
                    self.webAction.click_element("Transfer_Whisper")
                    
                elif "BlindConference" in item:
                    self.webAction.drag_and_move("drag_destination","drag_source")
                    self.webAction.click_element("Blind_Conference")
                    log.mjLog.LogReporter("PeopleGroup", "info", "After clicked")
                     
                    time.sleep(5)

            log.mjLog.LogReporter("PeopleGroup", "info", "drag_drop_transfer_call "
                                "Pressed ENTER without selecting any user successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "info", "drag_drop_transfer_call - Failed to do drag_and_move "+str(sys.exc_info()))
            raise AssertionError("Failed to press ENTER")
			
    def unzip_file(self, extension) :
        """
        unzip_file() - This method will unzip log file which downloaded
        Vijay         
        """
        try:
            file_dir="C:\Users\Public\Downloads"
            list_of_files= os.listdir(file_dir)
            for each_file in list_of_files:
                if each_file.startswith(extension):
                    break;
            file_name = os.path.splitext(each_file)[0]
            filename_suffix='zip'
            filename_with_suffix=os.path.join(file_dir, file_name + "." + filename_suffix)
            print filename_with_suffix
            self.Check_date_with_log_file(filename_with_suffix)
            zip_ref = zipfile.ZipFile(filename_with_suffix,'r')
            directory_to_extract_to=os.path.join(file_dir, file_name)
            zip_ref.extractall(directory_to_extract_to)
            zip_ref.close()
            list_of_file=os.listdir(directory_to_extract_to)
            for each_file in list_of_file:
                if each_file.startswith('Registry'):
                    console("Registry file :" + each_file + "Present")
                elif each_file.startswith('Environment'):
                    console("Environmnt file :" + each_file + " Present")
                elif each_file.startswith('Current'):
                    console("CurrentRunningProcess file :" + each_file + " Present")
                elif each_file.startswith('Presence'):
                    console("Presence file :" + each_file + " Present")
                    self.check_date_presenceBubble_file(each_file)
                elif each_file.startswith('Connect'):
                    console("Connect file :" + each_file + " Present")
                    self.check_date_connect_file(each_file)
                else:
                    log.mjLog.LogReporter("PeopleGroup", "info", "unzip_file "
                                "enter into else loop")
                    raise 
        except:
            log.mjLog.LogReporter("PeopleGroup", "error", "unzip_file - Failed to unzip "+str(sys.exc_info()))
            raise

    def Check_date_with_log_file (self,filename_log_with_suffix):
        """
        check_date_connect_file() - Verifying dates of log files
        Vijay         
        """
        console(filename_log_with_suffix)
        file_name = os.path.splitext(filename_log_with_suffix)[0]
        console(file_name)
        date_string = file_name[-10:]
        console(date_string)
        date1 = datetime.strptime(date_string, '%Y_%m_%d')  # this turns the string into a datetime object
        console(date1)
        date2 = datetime.date(date1)
        console(date2)
        today = datetime.today().date()
        console(today)
        try:
            if date2 == today:
                log.mjLog.LogReporter("zip_file", "info", "Check_date_with_log_file - "
                                                  "Its today file")
            else:
                raise 			
        except:
            log.mjLog.LogReporter("zip_file", "error", "Check_date_with_log_file - "
                                               "Its not today file " + str(sys.exc_info()))
            raise

    def check_date_connect_file(self,connect_file_name):
        """
        check_date_connect_file() - This method will Verifying dates of log files
        Vijay         
        """
        filename_connect = os.path.splitext(connect_file_name)[0]
        console(filename_connect)
        date_string = filename_connect[-13:-7]
        console(date_string)
        date1 = datetime.strptime(date_string, '%y%m%d').strftime('%Y_%m_%d')
        console(date1)
        date1 = datetime.strptime(date1, '%Y_%m_%d').date()
        console(date1)
        today = datetime.today().date()
        console(today)
        try:
            if date1 == today:
                log("zip_file", "info", "check_date_presenceBubble_file - "
                                                         "Its today file")
            else:
                raise
        except:
            log("zip_file", "error", "check_date_presenceBubble_file - "
                                                      "Its not today file " + str(sys.exc_info()))
            raise
			
    def check_date_presenceBubble_file(self,Presence_file_name):
        """
        check_date_presenceBubble_file() - This method will Verifying dates of log files
        Vijay         
        """
        filename_presence = os.path.splitext(Presence_file_name)[0]
        console(filename_presence)
        date_string = filename_presence[-6:]
        console(date_string)
        date1 = datetime.strptime(date_string, '%y%m%d').strftime('%Y_%m_%d')
        console(date1)
        date1 = datetime.strptime(date1, '%Y_%m_%d').date()
        console(date1)
        today = datetime.today().date()
        console(today)
        try:
            if date1 == today:
                log("zip_file", "info", "check_date_presenceBubble_file - "
                                                         "Its today file")
            else:
                raise
        except:
            log("zip_file", "error", "check_date_presenceBubble_file - "
                                                      "Its not today file " + str(sys.exc_info()))
            raise  			
