"""Module for adding and updating phone numbers
   File: AddPhoneNumber.py
   Author: Vasuja
"""

import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict
import string

from BCA_Operations import BCAOperations
from lib import wait_in_loop as WIL
from lib import select_from_dropdown as SFD

from selenium import webdriver
#import autoit

#For console logs while executing ROBOT scripts
from robot.api.logger import console

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

#import base
import web_wrappers.selenium_wrappers as base
import log
import inspect

__author__ = "Vasuja"


#login to BOSS portal
class PhoneNumber(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.BCAOperations = BCAOperations(self._browser)

    def add_phonenumber(self, params):
        """
        `Description:` This function will add phone numbers to BOSS portal

        `Param:` params: Dictionary with phone number information

        `Returns:` None

        `Created by:` Vasuja K

        `Modified by :` Kenash K
        """
        try:
            self.action_ele.click_element("ph_add_button")
            self.add_numbers(params)
            self.add_type(params)
            self.add_carrier(params)
            self.ph_review(params)

        except:
            print("Failed to add phone number")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_numbers(self, params):
        """
        `Description:` To add numbers range

        `Param:` params: Dictionary with phone number information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            time.sleep(1)
            params = defaultdict(lambda: '', params)
            # Modified By: Prasanna
            if int(params['range']) != 0:
                max_phone_num = int(params["numberRange"])+int(params['range'])
                self.action_ele.input_text("ph_TnsString", "+"+params["numberRange"]+"-"+str(max_phone_num))
            else:
                self.action_ele.input_text("ph_TnsString", "+" + params["numberRange"])
            self.action_ele.click_element("ph_ServiceUsage")
            self.action_ele.select_from_dropdown_using_text("ph_ServiceUsage", params["serviceUsage"])
            self.action_ele.click_element("ph_AddTNsWizard_next")
            time.sleep(5)
            try:
                verify_text = self.query_ele.text_present("Extension Conflicts")
                if verify_text:
                    self.action_ele.click_element("Ph_ExtnConfclt_checkbox")
                    self.action_ele.click_element("Ph_TNConflictsForm_OK")
            except:
                print("There is no Extension Conflicts ")
        except:
            print("Failed to add phone number range")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_type(self, params):
        """
        `Description:` To add type of phone

        `Param:` params: Dictionary contains phone number information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            time.sleep(1)
            params = defaultdict(lambda: '', params)
            if params['tn_type']=='system':
                self.action_ele.select_radio_button('ph_System')
            else:
                self.action_ele.select_radio_button('ph_Client')
            self.action_ele.clear_input_text('ph_tnCompaniesAutocomplete')
            self.action_ele.input_text('ph_tnCompaniesAutocomplete', params['clientAccount'])
            time.sleep(2)   #wait for the autocomplete to fetch data
            self.action_ele.press_key('ph_tnCompaniesAutocomplete', 'ENTER')
            self.action_ele.explicit_wait('ph_TnLocationId')
            time.sleep(2)
            self.action_ele.select_from_dropdown_using_text("ph_TnLocationId", params["clientLocation"])
            self.action_ele.click_element("ph_AddTNsWizard_next")
            try:
                verify_text = self.query_ele.text_present("Extension Conflicts")
                if verify_text:
                    self.action_ele.explicit_wait('Ph_ExtnConfclt_checkbox')
                    self.action_ele.click_element("Ph_ExtnConfclt_checkbox")
                    # self.action_ele.explicit_wait('Ph_TNConflictsForm_OK')
                    self.action_ele.click_element("Ph_TNConflictsForm_OK")
                    # self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            except:
                print("There is no Extension Conflicts ")

        except:
            print("Failed to select phone number type")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_carrier(self, params):
        """
        `Description:` To add carrier detaiil.

        `Param:` params: Dictionary contains carrier information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.select_from_dropdown_using_text("ph_TrunkgroupId", params["vendor"])
            self.action_ele.input_text("ph_VendorOrderNumber", params["vendorOrderNumber"])

            self.action_ele.explicit_wait("ph_AddTNsWizard_next")
            self.action_ele.click_element("ph_AddTNsWizard_next")

        except:
            print("Failed to add carrier")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def ph_review(self, params):
        """
        `Description:` To review the phone confirmation

        `Param:` params: requestedBy: Name of user who requested, requestSource

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            # Modified by: Prasanna
            if params["requestedBy"]:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'Ph_requested', params['requestedBy'],loop_count=40)
                #self.action_ele.select_from_dropdown_using_text("Ph_requested", params["requestedBy"])
            else:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                    'Ph_requested', 1, loop_count=40)
               # self.action_ele.select_from_dropdown_using_index("Ph_requested", 1)
            #self.action_ele.select_from_dropdown_using_text("Ph_RequestSrc", params["requestSource"])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'Ph_RequestSrc', params['requestSource'], loop_count = 40)
            self.action_ele.explicit_wait("Ph_finish_Button")
            self.action_ele.click_element("Ph_finish_Button")
            self.action_ele.explicit_wait('ph_table')
        except:
            print("Failed to select requested person and source")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def update_phonenumbers(self, params):
        """
        `Description:` To update phone numbers in page

        `Param:` params: Dictionary contains phone information

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            #select the phone numbers
            phone_num = params["numberRange"]
            max_phone_num = int(params["numberRange"]) + int(params['range'])
            for number in range(int(params['range'])+1):
                if self._browser.location=='us':
                    self.action_ele.input_text('Ph_NumberSearch', str(phone_num))
                    self.action_ele.explicit_wait('ph_table')
                    time.sleep(2)
                    tn_chkbox = self.get_obj_from_table('ph_table', 1, str(phone_num), 0)
                elif self._browser.location == 'australia' or 'uk':
                    self.action_ele.input_text('Ph_NumberSearch', str(phone_num))
                    self.action_ele.explicit_wait('ph_table')
                    time.sleep(2)
                    tn_chkbox = self.get_obj_from_table('ph_table', 1, '+' + str(phone_num), 0)
                tn_chkbox.click()
                phone_num = int(phone_num)+1
            self.action_ele.click_element('ph_update_button')
            #self.action_ele.explicit_wait('ph_headerRow_Tn')
            self.action_ele.explicit_wait('ph_State')
            self.action_ele.select_from_dropdown_using_text('ph_State', params['state'])
            self.action_ele.click_element('ph_UpdateTNsWizard_next')

            self.action_ele.explicit_wait('ph_headerRow_Tn')
            self.action_ele.explicit_wait('ph_UpdateTNsWizard_finish')
            self.action_ele.click_element('ph_UpdateTNsWizard_finish')
            self.action_ele.explicit_wait('ph_table')
        except Exception,e:
            print(e)
            console(e)
            print("Update state Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)


    def verify_phonenumbers(self, params):
        """
        `Description:` To verify the phone number.

        `Param:` params: Dictionary contains phone  range information

        `Returns:` status - True/False

        `Created by:` Kenash K
        """
        try:
            # select the phone numbers
            result = []
            phone_num = params["numberRange"]
            max_phone_num = int(params["numberRange"]) + int(params['range'])
            for number in range(int(params['range']) + 1):
                if self._browser.location == 'us':
                    self.action_ele.input_text('Ph_NumberSearch', str(phone_num))
                    self.action_ele.explicit_wait('ph_table')
                    time.sleep(2)
                    tn_status = self.get_obj_from_table('ph_table', 1, str(phone_num), 8)
                elif self._browser.location == 'australia' or 'uk':
                    self.action_ele.input_text('Ph_NumberSearch', str(phone_num))
                    self.action_ele.explicit_wait('ph_table')
                    time.sleep(2)
                    tn_status = self.get_obj_from_table('ph_table', 1, '+' + str(phone_num), 8)
                if tn_status.text == params['state']:
                    result.append(True)
                else:
                    print("Failed verifying %s" % str(phone_num))
                    print("Expected Text: %s" % params['state'])
                    print("State in UI: %s" % tn_status.text)
                    result.append(False)
                phone_num = int(phone_num) + 1

            print(result)
            if False in result:
                return False
            else:
                return True
        except:
            print("Could not find the requested data in table")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def get_obj_from_table(self, locator, primaryCol, primaryId, elementCol):
        """
        `Description:` Returns cell obj of a table using primary Id  & element col number.
                your xpath for table should be something like : //form[2]/table/tbody
        `Created by:` Kenash K
        """

        try:
            self.flag = 0
            self.table = self._browser.element_finder(locator)
            if self.table:
                for row in self.table.find_elements_by_tag_name('tr'):
                    self.colList = row.find_elements_by_tag_name('td')
                    if (len(self.colList) > primaryCol):
                        col_text = self.colList[primaryCol].text
                        for c in ['(', ')', ' ', '-','+']: col_text = col_text.replace(c, "")
                        if col_text == primaryId:
                            self.flag = 1
                            break
                if self.flag:
                    if (len(self.colList) >= elementCol):
                        print "Found expect column"
                        return self.colList[elementCol]
                    else:
                        print "Could not find expected column"
                        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                        raise AssertionError("Expected primary Id is not present in table")
                else:
                    print "Error Found"
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    raise AssertionError("Expected primary Id is not present in table")

        except Exception,e:
            print(e)
            console(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error in get_table_cell_obj_using_primaryId" \
                                 "- Check table xpath or primaryID or element col no")

    def update_single_phonenumber(self, params):
        """
        To update phone numbers in page

        :param params: Dictionary contains phone information

        :return: Status- True or false

        `Created by:` Saurabh Singh
        """
        try:
            #select the phone numbers
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            phone_num = params["number"]
            max_phone_num = int(params["numberRange"]) + int(params['range'])
            if self._browser.location=='us':
                self.action_ele.input_text('Ph_NumberSearch', str(phone_num))
                self.action_ele.explicit_wait('ph_table')
                time.sleep(2)
                tn_chkbox = self.get_obj_from_table('ph_table', 1, str(phone_num), 0)
            elif self._browser.location == 'australia' or 'uk':
                self.action_ele.input_text('Ph_NumberSearch', str(phone_num))
                self.action_ele.explicit_wait('ph_table')
                time.sleep(2)
                tn_chkbox = self.get_obj_from_table('ph_table', 1, '+' + str(phone_num), 0)
            tn_chkbox.click()
            phone_num = int(phone_num)+1
            self.action_ele.click_element('ph_update_button')
            #self.action_ele.explicit_wait('ph_headerRow_Tn')
            self.action_ele.explicit_wait('ph_State')
            self.action_ele.select_from_dropdown_using_text('ph_State', params['state'])
            self.action_ele.click_element('ph_UpdateTNsWizard_next')

            self.action_ele.explicit_wait('ph_headerRow_Tn')
            self.action_ele.explicit_wait('ph_UpdateTNsWizard_finish')
            self.action_ele.click_element('ph_UpdateTNsWizard_finish')
            self.action_ele.explicit_wait('ph_table')
            status = True
        except Exception,e:
            print(e)
            console(e)
            print("Update state Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_turnup_service(self, params):

        """
        To verify the presence of specified turnup service

        :param params: Dictionary contains service name

        :return: Status- True or false

        `Created by:` Megha Bansal
        """

        self.action_ele.click_element("ph_add_button")
        self.action_ele.select_from_dropdown_using_text("ph_ServiceUsage", params["serviceName"])
        text = self.query_ele.get_text_of_selected_dropdown_option("ph_ServiceUsage")

        if text == params["serviceName"]:
            return True
        else:
            return False

    def create_DNIS(self, params):
        """
        To set information to create DNIS in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false , selectedTn , selectedDestType

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            params = defaultdict(lambda: '', params)
            self.filter_Phone_number_page(params)

            selectedTn = self.query_ele.get_text("PhoneSystem_FetchTN")
            self.action_ele.click_element("PhoneSystem_SelectedRow_Checkbox")
            self.action_ele.click_element("PhoneSystem_Assign")
            if params["DNIS_Type"] == 'Bridged Call Appearance':
                self.action_ele.select_radio_button("PhoneSystem_Assign_BCA")
            elif params["DNIS_Type"] == 'Auto Attendant':
                self.action_ele.select_radio_button("PhoneSystem_Assign_AA")
            elif params["DNIS_Type"] == 'Hunt Group':
                self.action_ele.select_radio_button("PhoneSystem_Assign_HG")

            if params["DNIS_Type"]:
                self.action_ele.explicit_wait("PhoneSystem_DestinationDropdown")
                time.sleep(1)
                self.action_ele.select_from_dropdown_using_index("PhoneSystem_DestinationDropdown", 1)
            selectedDestType = self.query_ele.get_text_of_selected_dropdown_option("PhoneSystem_DestinationDropdown")

            if params['d_name_32']:
                self.action_ele.clear_input_text("PhoneSystem_Edit_DisplayName")
                self.action_ele.input_text("PhoneSystem_Edit_DisplayName", params['d_name_32'])
            return selectedTn, selectedDestType
        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_DNIS_with_Save(self, params):
        """
        To create DNIS in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            params = defaultdict(lambda: '', params)
            selectedTn, selectedDestType = self.create_DNIS(params)
            self.action_ele.click_element("PhoneSystem_Save")
            self.action_ele.explicit_wait("PhoneSystem_OK")

            verify_success = self.query_ele.text_present("The phone number was assigned successfully")
            time.sleep(.5)
            if verify_success == False:
                return False, selectedTn, selectedDestType

            self.action_ele.click_element("PhoneSystem_OK")
            self.action_ele.explicit_wait("PhoneSystem_Grid")
            return True, selectedTn, selectedDestType

        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_DNIS_with_Cancel(self, params):
        """
        To set information to create DNIS with cancel in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            params = defaultdict(lambda: '', params)
            selectedTn, selectedDestType = self.create_DNIS(params)
            if selectedTn:
                self.action_ele.click_element("PhoneSystem_Cancel")
                self.action_ele.explicit_wait("PhoneSystem_Yes")
                self.action_ele.click_element("PhoneSystem_Yes")
                self.action_ele.explicit_wait("PhoneSystem_Grid")
                return True
            else:
                return False

        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def select_number_for_Edit(self, params):
        """
        To select a number for edit in phone numbers  page

        :param params: Variable contains phone information

        :return: None

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            params = defaultdict(lambda: '', params)
            self.filter_Phone_number_page(params)
            self.action_ele.click_element("PhoneSystem_SelectedRow_Checkbox")
            self.action_ele.click_element("PhoneSystem_Edit")
            self.action_ele.explicit_wait("PhoneSystem_Save")
            self.action_ele.explicit_wait("PhoneSystem_Edit_DisplayName")
            time.sleep(1)
            if params['d_name_32']:
                isEnable = self.query_ele.element_enabled("PhoneSystem_Edit_DisplayName")
                if isEnable:
                    self.action_ele.clear_input_text("PhoneSystem_Edit_DisplayName")
                    self.action_ele.input_text("PhoneSystem_Edit_DisplayName", params['d_name_32'])
                    self.action_ele.click_element("PhoneSystem_Save")

        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def filter_Phone_number_page(self, params):
        """
        To filter phone number grid in phone numbers  page

        :param params: Variable contains phone information

        :return: None

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            self.action_ele.explicit_wait("PhoneSystem_Grid")
            time.sleep(1)
            if params['tn_status']:
                self.action_ele.select_from_dropdown_using_text("PhoneSystem_tnStatus", params['tn_status'])
            if params['tn_type']:
                self.action_ele.select_from_dropdown_using_text("PhoneSystem_tnType", params['tn_type'])
            if params['dest_type']:
                self.action_ele.select_from_dropdown_using_text("PhoneSystem_DestType", params['dest_type'])
            if params['display_name']:
                self.action_ele.input_text("PhoneSystem_DisplayName", params['display_name'])
            if params['country_code']:
                self.action_ele.select_from_dropdown_using_text("PhoneSystem_CountryCode", params['country_code'])
            if params['location']:
                self.action_ele.input_text("PhoneSystem_Location", params['location'])
            if params['tRequest']:
                self.action_ele.select_from_dropdown_using_text("PhoneSystem_TransferRequest", params['tRequest'])
            if params['number']:
                self.action_ele.input_text("PhoneSystem_Number", params['number'])

        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_PhoneNumber_Operation(self, params):
        """
         To verify assign window in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            params = defaultdict(lambda: '', params)
            self.filter_Phone_number_page(params)
            selectedTn = self.query_ele.get_text("PhoneSystem_FetchTN")
            self.action_ele.click_element("PhoneSystem_SelectedRow_Checkbox")
            self.action_ele.click_element("PhoneSystem_Assign")

            verify_text = self.query_ele.text_present("Assign")
            verify_tn = self.query_ele.text_present(selectedTn)
            if verify_text == False or verify_tn == False:
                return False
            else:
                response = self.query_ele.element_not_displayed("PhoneSystem_DestinationDropdown")
                if response == True:
                    return False
                return True

        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_PhoneNumber_Operation_for_Edit(self, params):
        """
         To verify edit window in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("PhoneSystem_Edit_DisplayName")
            verify_text = self.query_ele.text_present("Edit")
            if verify_text == False:
                return False
            else:
                isEnable = self.query_ele._is_enabled("PhoneSystem_Edit_DisplayName")
                if isEnable == False:
                    return False
                if params['error_msg']:
                    error = self.query_ele.get_text("PhoneSystem_DisplayName_Error")
                    if params['error_msg'] == error:
                        return True
                    return False

                return True

        except:
            print("Failed to select valid TN")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def refresh_grid(self):
        """
        To refreash grid in phone numbers  page

        :param params: None

        :return: None

        `Created by:` Megha ,Tantri Tanisha
        """
        self.action_ele.explicit_wait("PhoneSystem_Grid")
        self.action_ele.click_element("PhoneSystem_Refresh")
        self.action_ele.explicit_wait("PhoneSystem_Grid")

    def verify_destination_type(self, selectedTn, params):
        """
        To verify Destination type of DNIS created in phone numbers  page

        :param params: Variable contains phone information , selectedTn

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        self.action_ele.explicit_wait("PhoneSystem_Grid")
        params = defaultdict(lambda: '', params)
        self.action_ele.click_element("PhoneSystem_ClearFilter")
        self.action_ele.input_text("PhoneSystem_Number", selectedTn)
        destinationType = self.query_ele.get_text("PhoneSystem_FetchDestinationType")

        if params["DNIS_Type"] == destinationType:
            return True
        else:
            return False

    def verify_destination_and_status(self, selectedTn, selectedDestType, params):
        """
        To verify Destination name and status of the created DNIS in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        self.action_ele.explicit_wait("PhoneSystem_Grid")
        params = defaultdict(lambda: '', params)
        self.action_ele.click_element("PhoneSystem_ClearFilter")
        self.action_ele.input_text("PhoneSystem_Number", selectedTn)

        tnStatus = self.query_ele.get_text("PhoneSystem_FetchTnStatus")
        destinationName = self.query_ele.get_text("PhoneSystem_FetchDestinationName")
        addsuffix = ''
        if params["DNIS_Type"] == 'Bridged Call Appearance':
            addsuffix = ' BCA '
        elif params["DNIS_Type"] == 'Auto Attendant':
            addsuffix = ' AA '
        elif params["DNIS_Type"] == 'Hunt Group':
            addsuffix = ' HG '

        dname = ((selectedDestType[::-1]).split(" ", 1)[1])[::-1] + addsuffix + ((selectedDestType[::-1]).split(" ", 1)[
                                                                                     0])[::-1] + ' (' + params[
                    "d_name_32"] + ')'

        if tnStatus.lower() != 'active' and tnStatus.lower() != 'pending port in':
            return False
        elif dname != destinationName:
            return False
        else:
            return True


    def verify_tn_status(self, serviceTn, params):
        """
        Description : To verify the status of Tn

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha Bansal
        """
        params = defaultdict(lambda: '', params)
        # self.action_ele.explicit_wait('Ph_NumberSearch')
        WIL(self.action_ele.explicit_wait, 'Ph_NumberSearch')
        self.action_ele.input_text('Ph_NumberSearch', serviceTn)
        # self.action_ele.explicit_wait('ph_table')
        WIL(self.action_ele.explicit_wait, 'ph_table')
        time.sleep(2)
        for c in ['(', ')', ' ', '-', '+']:
            serviceTn = serviceTn.replace(c, "")
        time.sleep(1)
        # status = self.get_obj_from_table('ph_table', 1, serviceTn, 8)
        status = WIL(self.get_obj_from_table, 'ph_table', 1, serviceTn, 8, return_value=True, loop_count=40)

        if status.text.lower() == params['expectedTnStatus'].lower():
            return True
        else:
            return False


    def verify_available_tns(self, params):
        """
        Description : To verify the availability of Tns of the country List

        :param: Variable contains List of country

        :return: Status- True or false

        `Created by:` Megha Bansal

        'Modified By:' Palla Surya Kumar
        """
        time.sleep(1)
        self.action_ele.explicit_wait("PhoneSystem_Grid")
        self.action_ele.input_text("PhoneSystem_DisplayName",'-')
        for i in range(len(params)):
            self.action_ele.clear_input_text('PhoneSystem_Location')
            country = params[i].replace(" ", "")
            self.action_ele.input_text('PhoneSystem_Location', country)

            # wait till the page is download successfully
            ph_numbers_grid = WIL(self._browser.element_finder, "Grid_Canvas", return_value=True, loop_count=30)
            if not ph_numbers_grid:
                raise Exception("Grid canvas not selected in the Grid")

            rows = None
            for i in range(10):
                rows = ph_numbers_grid.find_elements_by_tag_name("div")
                if rows:
                    break
                time.sleep(5)
            else:
                raise Exception("No Row selected in the Grid")

            # eml = self._browser.elements_finder("PhoneSystem_LocationValue")
            if not len(rows) > 0:
                return False

        return True

    def update_phonenumberfields(self, params):
        """
        To update phone numbers in page
        :param params: Dictionary contains phone information
        :return: Status- True or false
		Created by:` Siva
        """

        try:
            #select the phone numbers
            phone_num = params["numberRange"]
            max_phone_num = int(params["numberRange"]) + int(params['range'])
            status = False
            for number in range(int(params['range'])+1):
                if self._browser.location=='us':
                    self.action_ele.input_text('ph_number_filter', str(phone_num))
                    self.action_ele.explicit_wait('ph_table')
                    time.sleep(2)
                    tn_chkbox = self.get_obj_from_table('ph_table', 1, str(phone_num), 0)
                elif self._browser.location == 'australia' or 'uk':
                    self.action_ele.input_text('ph_number_filter', str(phone_num))
                    self.action_ele.explicit_wait('ph_table')
                    time.sleep(2)
                    tn_chkbox = self.get_obj_from_table('ph_table', 1, str(phone_num), 0)
                tn_chkbox.click()
                phone_num = int(phone_num)+1
            self.action_ele.click_element('ph_update_button')
            #self.action_ele.explicit_wait('ph_headerRow_Tn')
            self.action_ele.explicit_wait('ph_State')
            if params['global_no_check']=="True":
                for label, state in params['updateformfield'].iteritems():
                    if params['updateformfield'][label] == 'enabled':
                        if self._browser.elements_finder(label)[0].is_enabled():
                            status = True
                            self.action_ele.click_element('Ph_Cancel')
                            self.action_ele.explicit_wait('Ph_CancelWizrd')
                            self.action_ele.click_element('Ph_CancelWizrd')
                    elif params['updateformfield'][label] == 'disabled':
                        if not self._browser.elements_finder(label)[0].is_enabled():
                            status = True
                            print("Phone number fields enabled/disabled Passed")
                            time.sleep(2)
                            self.action_ele.click_element('Ph_Cancel')
                            time.sleep(2)
                            self.action_ele.explicit_wait('Ph_CancelWizrd')
                            self.action_ele.click_element('Ph_CancelWizrd')

                    else:
                        return False

        except Exception, e:
                print(e)
                console(e)
                print("Phone number fields enabled/disabled Failed")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_type_of_phone_numbers(self,params):
        '''
        `Description:` This function will verify type of phone numbers sent thrpugh dictionary.

        `Param:` : Dictionary contains phone numbers information

        `Returns: ` result - True/False

        `Created by:` Palla Surya Kumar
        '''
        try:
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status=False
            #verifying count for status of all diff type phone numbers
            count=0
            self.action_ele.explicit_wait('phonesystem_phone_numbers_input')
            for item in params:
                #clear the input box of phone number every time before checking for phone number
                self.action_ele.clear_input_text('phonesystem_phone_numbers_input')
                self.action_ele.input_text('phonesystem_phone_numbers_input', params[item])
                self.action_ele.explicit_wait('phonesystem_phone_numbers_destination_type')
                destination_type_field=self._browser.element_finder('phonesystem_phone_numbers_destination_type')
                seen_destination_type = destination_type_field.text
                if item == 'emerNumber':
                    if seen_destination_type=='Emergency':
                        count += 1
                elif item =='userNumber':
                    if seen_destination_type =='User':
                        count += 1
                elif item == 'bcaNumber':
                    if seen_destination_type == 'Bridged Call Appearance':
                        count += 1
                elif item == 'aaNumber':
                    if seen_destination_type == 'Auto Attendant':
                        count += 1
                else:
                    if item == 'hgNumber':
                        if seen_destination_type == 'Hunt Group':
                            count += 1
            if count==5:
                status=True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error in checking the status of the phone numbers")
        return status

    def assign_ph_number_to_auto_attendant(self, params):
        '''
        `Description:` This function will assign ph number to auto attendant.

        `Param:` : dictionary  containing  aa_name

        `Returns: ` status(True/False).

        `Created by:` Palla Surya Kumar
        '''
        try:
            # removing the dependency of taking the phone number from here
            params = defaultdict(lambda: '', params)
            status = False
            WIL(self.action_ele.explicit_wait, "Ph_System_Ph_Number_Assign")
            # self.action_ele.explicit_wait("Ph_System_Ph_Number_Assign")
            # time.sleep(1)
            self.action_ele.click_element("Ph_System_Ph_Number_Assign")

            WIL(self.action_ele.explicit_wait, 'Ph_System_Ph_Number_Op_Dest_Type_AutoAttendant')
            # self.action_ele.explicit_wait('Ph_System_Ph_Number_Op_Dest_Type_AutoAttendant')
            # time.sleep(1)
            self.action_ele.click_element("Ph_System_Ph_Number_Op_Dest_Type_AutoAttendant")

            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                "Ph_System_Ph_Number_Op_Destination", params['aa_name'])
            # self.action_ele.explicit_wait("Ph_System_Ph_Number_Op_Destination" ,
            #                               ec="text_to_be_present_in_element", msg_to_verify="Select Component...")
            # time.sleep(1)
            # self.action_ele.select_from_dropdown_using_text("Ph_System_Ph_Number_Op_Destination", params['aa_name'])

            WIL(self.action_ele.explicit_wait, 'Ph_System_Ph_Number_Op_Save_Button')
            # self.action_ele.explicit_wait('Ph_System_Ph_Number_Op_Save_Button')
            # time.sleep(1)
            self.action_ele.click_element("Ph_System_Ph_Number_Op_Save_Button")

            WIL(self.action_ele.explicit_wait, "BCA_OK_Button")
            self.action_ele.click_element("BCA_OK_Button")

            self._browser._browser.refresh()
            status = True
        except Exception , e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error in assigning ph number to auto attendant")
        return status

    def assign_ph_number_to_hunt_group(self, params):
        '''
        `Description:` This function will assign ph number to hunt group.

        `Param:` : dictionary  containing  hg_name

        `Returns: ` status(True/False).

        `Created by:` Palla Surya Kumar
        '''
        try:
            # removing the dependency of taking the phone number from here
            params = defaultdict(lambda: '', params)
            status = False
            self.action_ele.explicit_wait("Ph_System_Ph_Number_Assign")
            time.sleep(1)
            # self.action_ele.click_element("Ph_System_Ph_Number_Assign")
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Assign")

            self.action_ele.explicit_wait('Ph_System_Ph_Number_Op_Dest_Type_HuntGroup')
            time.sleep(1)
            # self.action_ele.click_element("Ph_System_Ph_Number_Op_Dest_Type_HuntGroup")
            WIL(self.action_ele.click_element, "Ph_System_Ph_Number_Op_Dest_Type_HuntGroup")

            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.explicit_wait("Ph_System_Ph_Number_Op_Destination" ,
                                          ec="text_to_be_present_in_element", msg_to_verify="Select Component...")
            time.sleep(1)
            # self.action_ele.select_from_dropdown_using_text("Ph_System_Ph_Number_Op_Destination", params['hg_name'])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'Ph_System_Ph_Number_Op_Destination', params['hg_name'], loop_count=40)

            self.action_ele.explicit_wait('Ph_System_Ph_Number_Op_Save_Button')
            time.sleep(1)
            self.action_ele.click_element("Ph_System_Ph_Number_Op_Save_Button")

            # self.action_ele.explicit_wait("BCA_OK_Button")
            time.sleep(1)
            # self.action_ele.click_element("BCA_OK_Button")
            WIL(self.action_ele.click_element, "BCA_OK_Button", loop_count=20)

            self._browser._browser.refresh()
            status = True
        except Exception , e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Error in assigning ph number to hunt group")
        return status

    def search_mac_address_and_delete(self, mac):
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.explicit_wait("Ph_mac_address_search")
            time.sleep(1)
            self.action_ele.clear_input_text("Ph_mac_address_search")
            mac= str(mac)
            mac = mac[0:2] + ':' + mac[2:4] + ':' + mac[4:6] + ':' + mac[6:8] + ':' + mac[8:10] + ':' + mac[10:12]
            self.action_ele.input_text("Ph_mac_address_search", mac)
            if self.query_ele.element_not_displayed('Ph_select_mac_address_check_box2'):
                print("mac address not found")
            else:
                self.action_ele.click_element("Ph_select_mac_address_check_box2")
                self.action_ele.explicit_wait("Ph_remove_phone")
                self.action_ele.click_element("Ph_remove_phone")
                #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                time.sleep(1)
                self.action_ele.explicit_wait("Ph_delete_phone_yes")
                self.action_ele.click_element("Ph_delete_phone_yes")
                time.sleep(1)
                self.action_ele.explicit_wait("Ph_mitel_management_portal")
                self.action_ele.click_element("Ph_mitel_management_portal")
                self.action_ele.explicit_wait("Ph_mac_address_search")
                time.sleep(1)
                self.action_ele.clear_input_text("Ph_mac_address_search")

        except:
            raise AssertionError("Error during phone delete")
