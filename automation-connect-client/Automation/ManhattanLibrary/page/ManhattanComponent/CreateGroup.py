## Module: Create_Group
## File name: Create_Group.py
## Description: This class create the new people group
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

from log import log
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement


class CreateGroup:
    def __init__(self, browser):
        self._browser = browser
        self.webAction = WebElementAction(self._browser)
        self.queryElement = QueryElement(self._browser)
        self.assertElement = AssertElement(self._browser)

    def drag_drop_contact_to_group(self, contactList):
        """
        Author: UKumar
        drag_drop_contact_to_group(): Searches for a contact and Drag and drop contact to new group contact list
        Parameters: contactList
        """
        try:
            self.webAction.click_element("default_name_number_search")
            for contact in contactList:
                self.webAction.input_text("default_search_input", contact)
                time.sleep(1)
                searchResultsList = self._browser.elements_finder("peoples_panel_customer_name")
                if len(searchResultsList) != 1:
                    raise AssertionError("Check your contact name, either 0 or more than 1 contact found")
                else:
                    searchedName = "".join(searchResultsList[0].text.strip().split("\n"))
                    if searchedName == contact:
                        self.webAction.drag_and_drop("peoples_search_first_name", "peoples_drang_drop_name")
                        log.mjLog.LogReporter("CreateGroup", "info",
                                              "drag_drop_contact_to_group - %s added to group" % contact)
        except:
            log.mjLog.LogReporter("CreateGroup", "error",
                                  "drag_drop_contact_to_group - Drag and Drop failed" + str(sys.exc_info()))
            raise

    def add_new_group(self, groupName, contacts, choice, discardMyChanges=''):
        """
        Author: modified by Uttam
        add_new_group() - This method will add a new group with contacts
        Parameters: groupName, contacts, choice and discardMyChanges
        (This method is modified to implement new UI changes in the popup
         while clicking on cancel button 23-07-2015)
        """
        try:
            self.webAction.input_text("peoples_name",groupName)
            time.sleep(2)
            if len(contacts) == 0:
                log.mjLog.LogReporter("add_new_group", "info","add_new_group - clicking on the save changes")
                self.webAction.click_element("peoples_save_Changes")
                return True
            
            for self.contact in contacts:
                self.webAction.input_text("peoples_drang_drop_name",self.contact)
                time.sleep(2)
                name_list = self._browser.elements_finder("people_grp_drop_drown_contact_name")
                for name in name_list:
                    if self.contact in name.text:                        
                        name.click()                        
                        break
            if choice.lower() == "save":
                self.webAction.click_element("peoples_save_Changes")
                log.mjLog.LogReporter("Create_Group", "info", "add_new_group - clicked on save button")
            elif choice.lower() == "cancel" or choice.lower() == "x":
                self.discard_group_draft(discardMyChanges)
            else:
                log.mjLog.LogReporter("add_new_group", "info", "add_new_group - draft saved")
            
        except :
            log.mjLog.LogReporter("CreateGroup","error","add_new_group - Error while "
                                  "creating the new group_contact "+str(sys.exc_info()))
            raise
    
    def discard_group_draft(self, discardMyChanges):
        try:
            self.webAction.click_element("TP_Group_Form_Close")
            self.assertElement.element_should_be_displayed("TP_Group_Form_Close_Yes")
            if discardMyChanges == "yes":
                self.webAction.click_element("TP_Group_Form_Close_Yes")
                log.mjLog.LogReporter("discard_group_draft", "info", "discard_group_draft - change discarded")
            else:
                self.webAction.click_element("TP_Group_Form_Close_Cancel")
                self.assertElement.element_should_be_displayed("TP_delete_group")
                log.mjLog.LogReporter("discard_group_draft", "info", "discard_group_draft - you are at same page, changes are in place")
        except:
            log.mjLog.LogReporter("CreateGroup","error","discard_group_draft - Error while discarding group draft "+str(sys.exc_info()))
            raise

    def modify_group_add_contact(self, groupName, contacts, choice, discardMyChanges=''):
        """
        Author:modified by Uttam
        modify_group_add_contact() - This method adds contacts to an existing group
        Parameters: groupName, contacts, choice and discardMyChanges
        """
        try:
            if groupName:
                self.webAction.input_text("peoples_name", groupName)

            for contact in contacts:
                self.webAction.input_text("peoples_drang_drop_name", contact)
                time.sleep(2)
                self.webAction.click_element("people_grp_drop_drown_contact_name")
                time.sleep(2)
            time.sleep(5)
            # self.webAction.explicit_wait("peoples_save_Changes")
            if choice.lower() == "save":
                print("Inside Save Choice")
                self.webAction.click_element("peoples_save_Changes")
                # time.sleep(5)
                log.mjLog.LogReporter("Create_Group", "info", "modify_group_add_contact -"
                                                              " clicked on save changes button successfully")
            elif choice.lower() == "cancel" or choice.lower() == "x":
                self.discard_group_draft(discardMyChanges)
            else:
                log.mjLog.LogReporter("Create_Group", "info", "modify_group_add_contact - draft saved")
        except:
            log.mjLog.LogReporter("CreateGroup", "error", "modify_group_add_contact - "
                                                          "Error while modifying the group_contact %s" + str(
                sys.exc_info()))
            raise
            
    def delete_group_of_contacts(self,contacts, choice, discardMyChanges=''):
        """
        Author: modified by Uttam
        delete_group_of_contacts() - Identifies contacts in group and click on delete button
        Parameters: contacts and choice
        """
        try:
            if choice == "none":
                print("Nothing to be done")
            else:
                groupContactsList=self._browser.elements_finder("third_panel_contact_list")
                time.sleep(6)
                if len(groupContactsList) == 0:
                    log.mjLog.LogReporter("Create_Group", "info", "delete_group_of_contacts - "
                                          "contacts do not exist in the group")
                    return False
                else:
                    for self.contact in contacts:
                        count=0
                        deleteButtonsList = self._browser.elements_finder("third_panel_contact_list_delete")
                        groupContactsList = self._browser.elements_finder("third_panel_contact_list")
                        for groupContact in groupContactsList:
                            if (groupContact.text == self.contact):
                                contactIndex = groupContactsList.index(groupContact)
                                count = count + 1
                                break
                        for deleteButton in deleteButtonsList:
                            if (count != 0 and deleteButtonsList.index(deleteButton) == contactIndex):
                                deleteButton.click()
                                time.sleep(3)
                                
                    if choice.lower() == "save":
                        self.webAction.click_element("peoples_save_Changes")
                        #self.assertElement.page_should_contain_text("New Group")
                        log.mjLog.LogReporter("Create_Group", "info", "delete_group_of_contacts - "
                                              "clicked on save changes button successfully")
                    elif choice.lower() == "cancel" or choice.lower() == "x":
                        self.webAction.click_element("peoples_cancel")
                        self.assertElement.element_should_be_displayed("people_dscrdChanges_Popup")
                        if discardMyChanges == "yes":
                            self.webAction.click_element("people_dscrdChanges_Popup_Yes")
                            log.mjLog.LogReporter("Create_Group", "info", "delete_group_of_contacts - change discarded")
                        else:
                            self.webAction.click_element("people_dscrdChanges_Popup_Cancel")
                            self.assertElement.element_should_be_displayed("peoples_cancel")
                            log.mjLog.LogReporter("Create_Group", "info", "delete_group_of_contacts "
                                                  "- you are at same page, changes are in place")
                    else:
                        log.mjLog.LogReporter("Create_Group", "info", "delete_group_of_contacts - draft saved")
                    time.sleep(6) 
        except :
            log.mjLog.LogReporter("Create_Group", "error", "delete_group_of_contacts - Error while"
                                  " deleting the contacts from group "+str(sys.exc_info()))
            raise
            
    def rename_group_withdouble_quotes(self,newgroupName):
        
        '''
        Author : surendra
        This API will rename an exiting group with new group name
        newgroupName is the parameter which will be replaced as edited group name
        e.g. group G1 is renamed as testGroup
        '''
        try: 
            new_group_name1='"'+newgroupName+'"'
            #m = str(new_group_name1)
            self.webAction.clear_input_text("peoples_name")
            self.webAction.input_text("peoples_name",new_group_name1)
            self.webAction.click_element("peoples_save_Changes")			
        except:
            log.mjLog.LogReporter("CreateGroup", "error", "rename_group_withdouble_quotes - "
                    "Error while modifying the group_contact %s" % str(sys.exc_info()))
            raise

    def search_group_contact(self, contact, type):
        '''
        Author: Gautham
        search for a contact in an existing group 
        (supports both positive and negative case)
        change list: replaced xpath peoples_grp_customer_name with TP_GroupUsers (UKumar: 18-Sep-2016)
        '''
        try:
            self.contact = contact
            self.type = type
            if self.type == "positive":
                user_list = self._browser.elements_finder("TP_GroupUsers")
                print("length of user list :positive: is ", user_list)
                print("length of user list :positive: is ", len(user_list))
                presence = 0
                for user in user_list:
                    time.sleep(5)
                    user_name = user.text
                    print("printing user_name information:", user_name)
                    user_id = user_name.split()
                    print("printing user_id information:", user_id)
                    if (user_id[0] == self.contact):
                        presence = presence + 1
                        print("printing presence information:", presence)
                if (presence):
                    log.mjLog.LogReporter("CreateGroup", "info",
                                          "search_group_contact -user " + self.contact + " is present in the group as expected")
                else:
                    raise AssertionError("search_group_contact -user " + self.contact + " is not present in the group")
            elif self.type == "negative":
                user_list = self._browser.elements_finder("TP_GroupUsers")
                presence = 0
                print("length of user list :Negative: is ", len(user_list))
                # sys.exit()
                if len(user_list) == 1:
                    pass
                else:
                    for user in user_list:
                        user_name = user.text
                        user_id = user_name.split()
                        if (user_id[0] == self.contact):
                            presence = presence + 1
                if (presence == 0):
                    log.mjLog.LogReporter("CreateGroup", "info",
                                          "search_group_contact -user " + self.contact + " is not present in the group as expected")
                else:
                    raise AssertionError("search_group_contact -user " + self.contact + " is present in the group")
        except:
            log.mjLog.LogReporter("CreateGroup", "error",
                                  "Error while executing search_group_contact - " + str(sys.exc_info()))
            raise

    def verify_groups_name(self, grouplist):
        '''
        Author : kiran
        verify_groups_name : This API verify the name of all groups added to the list
        '''
        try:
            grplist = self._browser.elements_finder("peoples_first_group")
            if len(grplist) > 0:
                count = 0
                for j in range(len(grouplist)):
                    for i in grplist:
                        if grouplist[j] == i.text:
                            print("Group name is found")
                            log.mjLog.LogReporter("CreateGroup", "info",
                                                  "verify_groups_name - " "group name:" + grouplist[j] + " is present")
                            count += 1
                            break
                    if count == 0:
                        raise
            
            if len(grouplist) == count:
                return True

            elif len(grouplist) != count:
                return False

            elif len(grplist) == 0:
                print("empty list found")
                raise
        except:
            log.mjLog.LogReporter("CreateGroup", "error",
                                  "verify_groups_name - " "Error while modifying the group_contact %s" % str(
                                      sys.exc_info()))
            raise

    def verify_groupMembers_name(self, contactlist):
        '''
        Author : kiran
        verify_groupMembers_name : This API verify the name of all groups added to the list
        '''
        try:
            grpMemblist = self._browser.elements_finder("people_filter_lastcontact")
            if len(grpMemblist) > 0:
                found = 0
                for j in range(len(contactlist)):
                    for i in grpMemblist:
                        if contactlist[j] == i.text:
                            print("contacts are listed in the group")
                            log.mjLog.LogReporter("CreateGroup", "info",
                                                  "verify_groupMembers_name - " "group member " + contactlist[
                                                      j] + "is present")
                            found = 1
                            break
                    if found == 0:
                        print("contact name not found")
                        raise
            elif len(grpMemblist) == 0:
                raise
        except:
            log.mjLog.LogReporter("CreateGroup", "error",
                                  "verify_groupMembers_name - " "Error while modifying the group_contact %s" % str(
                                      sys.exc_info()))
            raise