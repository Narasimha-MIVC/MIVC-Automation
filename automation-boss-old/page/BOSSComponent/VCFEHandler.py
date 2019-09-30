"""Module for creating and verifying VCFE components
   File: VCFEHandler.py
   Author: Vasuja
"""

import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict

from selenium import webdriver
#For console logs while executing ROBOT scripts
from robot.api.logger import console
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
import re
#import base
import web_wrappers.selenium_wrappers as base
import log
import inspect
from CommonFunctionality import CommonFunctionality
__author__ = "Vasuja"

HG_EDIT_ELEMENT = {"Call_member_when_forwarding_all_calls": "vcfe_Call_member_when_forwarding_all_calls", "Rings_per_Member": "vcfe_rings_per_member",
                   "Distribution_pattern_Simultaneous": "vcfe_hg_simultaneous", "No_answer_number_of_rings": "vcfe_hg_noAnswerRings", "On_hours_schedule":"vcfe_onHour",
                   "Skip_member_if_already_on_a_call": "vcfe_Skip_member_if_already_on_a_call", "Include_in_System_Dial_by_Name_directory": "vcfe_hg_includeDialByName",
                   "Make_extension_private": "vcfe_extn_private_checkbox", "Holiday_schedule": "vcfe_holidaySchedule", "call_stack_full": "hg_call_stack",
                   "no_answer":"hg_NoAnswer", "Off_hours_or_holiday_destination": "hg_OffHoursHoliday"}

#login to BOSS portal
class VCFEHandler(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.common_ele = CommonFunctionality(self._browser)
        self.INDEX = 1

    def create_emergency_hunt_group(self, params):
        """
        `Description:` Create emergency hunt group

        `Param:` params: Dictionary contains  emergency hunt group Info

        `Returns:` emergency hunt group extension

        `Created by:` Vasuja
         """
        try:
            extn = ''
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("Emergency_add_dropdown")
            self.action_ele.click_element("Emergency_huntgroup")
            time.sleep(3)
            self.action_ele.explicit_wait("Emergency_huntgroup_location")
            self.action_ele.select_from_dropdown_using_text("Emergency_huntgroup_location", params["Location"])
            extn = self.query_ele.get_value("vcfe_Huntgrp_Extn")
            if params["grp_member"]!='':
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.input_text('vcfe_HG_Search', params['grp_member'])
                self.action_ele.click_element("vcfe_Select_Extn")
                self.action_ele.clear_input_text('vcfe_HG_Search')
                self.action_ele.click_element("vcfe_HG_Back")
            time.sleep(2)
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(5)
            self.action_ele.explicit_wait("fnMessageBox_OK")
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(3)
            return extn
        except:
            print("Emergency hunt group creation failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_loc_status(self, params):
        """
        `Description:` This function will verify Emergency registration status of location

        `Param1:` Loc_name

        `Param2:` exp_state

        `Returns:` status - True/False

        `Created by:` Vasuja
        """
        try:
            for i in range(4):
                # TODO: Links has to be identified and clicked.
                # since the submenu disappears after clicking menu link
                try:
                    self.action_ele.click_element('phone_system_nav')
                    time.sleep(2)
                    self.action_ele.click_element("Emergency_Registration_link")
                    print("SWITCHING TO VCFE PAGE :%s" % i)
                    vcfe_loaded = self.action_ele.explicit_wait("headerRow_Name")
                    if vcfe_loaded:
                        result = True
                        break
                except:
                    print("Retrying click: %d" % i)
                    pass
            status = False
            time.sleep(2)
            self.action_ele.explicit_wait('headerRow_Name')
            self.action_ele.input_text('headerRow_Name', params["loc_name"])
            for i in range(3):
                var = self.query_ele.text_present(params["exp_state"])
                if var:
                    status = True
                    break
                else:
                    time.sleep(1)

            return status
        except:
            print("Verify Location status failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_geo_location(self, params):
        """
        `Description:` This function will add Geographic location

        `Param:` params: Dictionary with Geolocationinfo

        `Returns:` status - True/False

        `Created by:` Vasuja
        """
        status=False
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("geo_accountLocationsAddButton")
            self.action_ele.input_text("geo_LocationDetails_LocationNameFormatted", params["Location"])
            self.action_ele.select_from_dropdown_using_text("geo_Address_CountryKey", params["Country"])
            if self._browser.location == 'australia':
                self.add_location_australia(params)
            if self._browser.location=='us':
                self.add_location_united_states(params)
            if self._browser.location=='uk':
                self.add_location_united_kingdom(params)

            if params["by_pass"]=="True":
                self.action_ele.click_element("geo_bypass_validation")
            self.action_ele.click_element("geo_locationDetailsWizard_next")
            if self._browser.location == 'us':
                pass
            elif self._browser.location == 'australia' or 'uk':
                self.action_ele.select_from_dropdown_using_text("geo_timeZone", params["timeZone"])
                self.action_ele.input_text("geo_AreaCode", params["areaCode"])
            self.action_ele.click_element("geo_locationDetailsWizard_next")
            self.action_ele.click_element("geo_locationDetailsWizard_next")
            self.action_ele.click_element("geo_locationDetailsWizard_finish")
            print("waiting for adding geo....")
            time.sleep(40)
            status = True
        except:
            print("Geographic location creation failed")
            status = False
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def add_location_australia(self, params):
        """
        `Description:` This function will add Geographic location for Australia

        `Param:` params: Dictionary with Geolocationinfo

        `Returns:` None

        `Created by:` Vasuja
        """
        try:
            self.action_ele.input_text("geo_Street_HouseNo", params["streetNo"])
            self.action_ele.input_text("geo_StreetName", params["streetName"])
            self.action_ele.select_from_dropdown_using_text("geo_streetType", params["streetType"])
            self.action_ele.input_text("geo_city", params["City"])
            self.action_ele.select_from_dropdown_using_text("geo_state", params["state"])
            self.action_ele.input_text("geo_zipcode", params["postcode"])
            self.action_ele.input_text("geo_FirstName", params["firstName"])
            self.action_ele.input_text("geo_LastName", params["lastName"])
            self.action_ele.input_text("geo_PhoneNumber", params["phoneNumber"])
        except:
            print("Failed to add location with respect to Australia for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_united_states(self, params):
        """
        `Description:` This function will add Geographic location for US

        `Param:` params: Dictionary with Geolocationinfo

        `Returns:` None

        `Created by:` Vasuja
        """
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            params = defaultdict(lambda: '', params)
            self.action_ele.input_text("geo_Address_Address1", params["Address01"])
            self.action_ele.input_text("geo_Address_Address2", params["Address02"])
            self.action_ele.select_from_dropdown_using_text("geo_Address_StateProvinceKey", params["state"])
            self.action_ele.input_text("geo_Address_City", params["city"])
            self.action_ele.input_text("geo_Address_ZipCode", params["Zip"])
        except:
            print("Failed to add location with respect to United States for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_united_kingdom(self, params):
        """
        `Description:` This function will add Geographic location for UK

        `Param:` params: Dictionary with Geolocationinfo

        `Returns:` None

        `Created by:` Vasuja
        """
        try:
            self.action_ele.input_text("geo_Address_Address2", params["buildingName"])
            self.action_ele.input_text("geo_Address_Address1", params["streetName"])
            self.action_ele.input_text("geo_city", params["postalTown"])
            self.action_ele.input_text("geo_zipcode", params["Postcode"])
        except:
            print("Failed to add location with respect to United States for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_hunt_group(self, params):
        """
        `Description:` Create hunt group with different input parameters

        `Param:` params: Dictionary with Hunt_Group_Info

        `Returns:` Hunt Group Extension Number

        `Created by:` Vasuja
        """
        try:
            extn = ''
            errors=[]
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("vcfe_add_dropdown")
            self.action_ele.click_element("vcfe_add_dropdown")
            self.action_ele.click_element("vcfe_hunt_group")
            elements = self._browser.elements_finder("pg_refresh_btn")
            time.sleep(2)
            if elements[0].is_displayed():
                pass
            else:
                #self.action_ele.explicit_wait("pg_editor_panel")
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)
            self.action_ele.input_text('vcfe_huntgrp_Name', params['HGname'])
            if params["HGExtn"]:
                self.action_ele.input_text('vcfe_Huntgrp_Extn', params['HGExtn'])
                extn = params["HGExtn"]

            if params["extnprivate"]:
                self.action_ele.select_checkbox("vcfe_extn_private_checkbox")

            self.action_ele.input_text('vcfe_Huntgrp_Bckup_Extn',  params['HGBckupExtn'])

            if params['hglocation']=='random':

                self.action_ele.select_from_dropdown_using_index('vcfe_huntgroup_location', 1)
            else:
                self.action_ele.select_from_dropdown_using_text('vcfe_huntgroup_location', params['hglocation'])

            if params['hg_phonenumber']:
                self.action_ele.explicit_wait("vcfe_assign")
                self.action_ele.click_element("vcfe_assign")
                time.sleep(2)
                if params['hg_phonenumber']=='random':
                    self.INDEX += 2
                    self.action_ele.select_from_dropdown_using_index('vcfe_selPhoneNumber', self.INDEX)
                    phonenum=self.query_ele.get_text_of_selected_dropdown_option('vcfe_selPhoneNumber')
                    params['hg_phonenumber']=phonenum
           # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

            if params['Rings_per_Member']!='':
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Rings_per_Member"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["Rings_per_Member"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["Rings_per_Member"], params["Rings_per_Member"])

            if params['No_answer_number_of_rings']!='':
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["No_answer_number_of_rings"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["No_answer_number_of_rings"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["No_answer_number_of_rings"], params["No_answer_number_of_rings"])

            if params["grp_member"]:
                self.action_ele.click_element("vcfe_edit")
                for member in params["grp_member"]:
                    self.action_ele.input_text('vcfe_HG_Search', member)
                    self.action_ele.click_element("vcfe_Select_Extn")
                    self.action_ele.clear_input_text('vcfe_HG_Search')
                self.action_ele.click_element("vcfe_HG_Back")
            time.sleep(2)
            #self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(4)
            errors = self._browser.elements_finder('vcfe_val_errors')
            extn = self.query_ele.get_value("vcfe_Huntgrp_Extn")
            if errors:
                for error in errors:
                    if "The extension is not available" in error.text:
                        extension = error.text.split(':')[-1].strip()
                        self.action_ele.input_text('vcfe_Huntgrp_Extn', extension)
                        extn = self.query_ele.get_value("vcfe_Huntgrp_Extn")
                        self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
                    time.sleep(4)
            if params["error_message"]:
                return
            self.action_ele.explicit_wait("fnMessageBox_OK")
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(3)
            self.action_ele.explicit_wait("vcfe_extension_textbox", ec="visibility_of_element_located")
            return extn

        except:
            print("Hunt group creation failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)


    def create_extension_list(self, params):
        """
        `Description:` Create extension list by giving extension list name and extension Number

        'param:` params: Dictionary with ExtensionListInfo

        `Returns:` None

        `Created by:` Vasuja

        `Modified by :` Immani Mahesh, Saurabh Singh
        """
        #print params
        try:
            ext_list_name_blank = "Failed creating component. Error: Name - can't be blank"
            ext_list_name_already_taken = "Failed creating component. Error: Name - has already been taken"
            self.action_ele.click_element("vcfe_add_dropdown")
            self.action_ele.click_element("vcfe_extnlist")
            time.sleep(2)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)
            #self.assert_ele.element_should_be_displayed("vcfe_EL_CompDetails")
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            user_list = params['extnNumber']
            for extn in user_list:
                self.action_ele.input_text('vcfe_EL_Search', extn)
                self.action_ele.click_element("vcfe_Select_Extn")
                self.action_ele.clear_input_text('vcfe_EL_Search')
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if params['extnlistname'] == "blank":
                self.action_ele.clear_input_text('vcfe_extnlist_name')
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(2)
                if ext_list_name_blank in self.query_ele.get_text("Aa_edit_confirm"):
                    self.action_ele.click_element("fnMessageBox_OK")
                    time.sleep(1)
                self.action_ele.click_element("pgg_cancel_button")
                self.action_ele.explicit_wait("VCFE_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete_yes")
                time.sleep(2)
                return
            else:
                self.action_ele.clear_input_text('vcfe_extnlist_name')
                self.action_ele.input_text('vcfe_extnlist_name', params['extnlistname'])
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(1)
                self.action_ele.explicit_wait("fnMessageBox_OK")
                time.sleep(1)
                if ext_list_name_already_taken in self.query_ele.get_text("Aa_edit_confirm"):
                    self.action_ele.explicit_wait("fnMessageBox_OK")
                    time.sleep(1)
                    self.action_ele.click_element("fnMessageBox_OK")
                    time.sleep(2)
                    self.action_ele.click_element("pgg_cancel_button")
                    self.action_ele.explicit_wait("VCFE_delete_yes")
                    time.sleep(1)
                    self.action_ele.click_element("VCFE_delete_yes")
                    time.sleep(2)
                    return
                else:
                    self.action_ele.click_element("fnMessageBox_OK")
                    self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                    time.sleep(1)
        except Exception,e:
            print(e)
            print("Creating extension list failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_pickup_group(self, params):
        """
        `Description:` This function will create pickup group

        `Param:` params: Dictionary contains PickupGroupInfo

        `Returns:` Pickup Group Extension number

        `Created by:` Vasuja

        `Modified by :` Saurabh Singh

        """
        print params
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            extn = ''
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_add_dropdown")
            self.action_ele.click_element("vcfe_pickup_group")
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                self.action_ele.explicit_wait("pg_editor_panel")
                self.action_ele.click_element("pg_editor_panel")
            self.action_ele.explicit_wait('vcfe_pickup_group_name')
            if params['pickupgpname'] != '':
                self.action_ele.input_text('vcfe_pickup_group_name', params['pickupgpname'])
            else:
                pass
            time.sleep(3)
            extn = self.query_ele.get_value("vcfe_pickup_group_extn")
            if params['pickuploc'] != "None":
                self.action_ele.select_from_dropdown_using_text('vcfe_pickup_group_location', params['pickuploc'])
            elif params['pickuploc'] == "None":
                self.action_ele.select_from_dropdown_using_index('vcfe_pickup_group_location', 1)
            self.action_ele.select_from_dropdown_using_text('vcfe_pickup_group_extnlist', params['extnlistname'])
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.action_ele.click_element("vcfe_pickup_finish")
            time.sleep(2)
            if "This field is required." in self._browser._browser.page_source:
                print("Error Occured on page")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return False
            else:
                pass
            self.action_ele.explicit_wait("fnMessageBox_OK")  ###
            time.sleep(1)  ##
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(2)
            return extn

        except Exception, e:
            print(e)
            print("Creating pick up group failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError

    def add_Auto_Attendant(self, params):
        """
        `Description:` This function will create Auto Attendant

        `Param:` params: Dictionary contains AutoAttendantInfo

        `Returns:` Auto Attendant Extension number

        `Created by:` rdoshi

        `Modified by :` Immani Mahesh

        """

        message = "Extension is a required field. Please select an extension"
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("Add_VCFE")
            self.action_ele.click_element("Add_AA")
            self.action_ele.explicit_wait("pg_editor_panel")
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                self.action_ele.explicit_wait("pg_editor_panel")
                self.action_ele.click_element("pg_editor_panel")
            self.action_ele.explicit_wait("Aa_Name")
            self.action_ele.input_text("Aa_Name", params["Aa_Name"])
            extn = self.query_ele.get_value("Aa_Extension")
            while extn == '':
                extn = self.query_ele.get_value("Aa_Extension")
                if extn:
                    break
                else:
                    time.sleep(1)
            extn = self.query_ele.get_value("Aa_Extension")
            if (params["AA_customExtension"]):
                self.action_ele.input_text("Aa_Extension", params["AA_customExtension"])
                extn= params["AA_customExtension"]
            if (params["Aa_privateExtension"] == "yes"):
                self.action_ele.select_checkbox('Aa_privateExtension')
            if (params["Aa_Location"] == "random"):
                time.sleep(1)
                self.action_ele.select_from_dropdown_using_index("Aa_Location", 1)
            else:
                self.action_ele.select_from_dropdown_using_text("Aa_Location",
                                                                params["Aa_Location"])
            if params['Aa_Extension'].lower() == 'blank':
                time.sleep(1)
                # import pdb;
                # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                self.action_ele.clear_input_text("Aa_Extension")
                time.sleep(1)
                self.action_ele.click_element("Aa_finishAA")
                time.sleep(1)
                self.action_ele.click_element("Aa_finishAA")
                time.sleep(1)
                if message in self.query_ele.get_text("Aa_edit_confirm"):
                    self.action_ele.click_element("fnMessageBox_OK")
                    time.sleep(1)
                self.action_ele.click_element("pgg_cancel_button")
                self.action_ele.explicit_wait("VCFE_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete_yes")
                time.sleep(2)
                return True
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params["Aa_assignDID"] or params["Aa_assignDID"] == "random":
                self.action_ele.click_element("Aa_assignDID")
                self.action_ele.explicit_wait("Aa_PNselector")
                time.sleep(1)
                if params["Aa_assignDID"]:
                    self.action_ele.select_from_dropdown_using_text("Aa_PNselector", params["Aa_assignDID"])
                else:
                    self.action_ele.select_from_dropdown_using_index("Aa_PNselector", 1)
             # import pdb;
                # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                #time.sleep(1)
                #self.action_ele.select_from_dropdown_using_index("Aa_PNselector", self.INDEX)
                #self.action_ele.select_from_dropdown_using_index("Aa_PNselector", 1)#Modifed to select first number from the list
                #self.INDEX += 1
            time.sleep(3)
            self.action_ele.click_element("Aa_finishAA")
            time.sleep(3)
            errors = self._browser.elements_finder('vcfe_val_errors')

            if errors :
                for error in errors:
                    if "The extension is not available" in error.text:
                        extn = error.text.split(':')[-1].strip()
                        self.action_ele.input_text('vcfe_Huntgrp_Extn', extn)
                        extn = self.query_ele.get_value("vcfe_Huntgrp_Extn")
                        self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
                    # if "Extension is a required field. Please select an extension" in error.text:
                    #     return True
                time.sleep(4)


            #extn = self.query_ele.get_value("vcfe_Huntgrp_Extn")
            self.action_ele.explicit_wait("fnMessageBox_OK")
            time.sleep(1)
            self.action_ele.click_element("fnMessageBox_OK")
            return extn
        except Exception as e:
            print(e.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Creating Auto Attendant Failed:", e.message)

    def create_custom_schedule(self, params):
        """
        `Description:` This function will create custom schedule

        `Param:` params: Dictionary contains CustomScheduleInfo

        `Returns:` status - True/False

        `Created by:` Vasuja K

        `Modified by :` Immani Mahesh, Saurabh Singh
        """
        try:
            status = False
            blank_name_error = "Failed creating component. Error: ScheduleName - can't be blank"
            name_already_in_use = "Failed creating component. Error: ScheduleName - has already been taken"
            message1 = 'Component was created successfully'
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_add_dropdown")
            self.action_ele.click_element("vcfe_custom_schedule")
            time.sleep(3)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)
            self.action_ele.input_text('vcfe_custom_schedule_name', params['customScheduleName'])
            time.sleep(2)
            if params['timeZone']:
                self.action_ele.select_from_dropdown_using_text('vcfe_selScheduleTimezone', params['timeZone'])
            self.action_ele.click_element("vcfe_add_button")
            self.action_ele.input_text('vcfe_custom_name', params['customName'])
            self.action_ele.input_text('vcfe_custom_date', params['customDate'])
            self.action_ele.input_text('vcfe_custom_starttime', params['startTime'])
            self.action_ele.input_text('vcfe_custom_stoptime', params['stopTime'])
            time.sleep(3)
            # self.action_ele.explicit_wait("vcfe_pickup_finish")
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            self.action_ele.click_element("vcfe_pickup_finish")
            if message1 in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.explicit_wait("fnMessageBox_OK")
                time.sleep(1)
                self.action_ele.click_element("fnMessageBox_OK")
                status = True
            elif blank_name_error or name_already_in_use in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.click_element("fnMessageBox_OK")
                time.sleep(1)
                self.action_ele.click_element("vcfe_cancel_button")
                time.sleep(2)
                self.action_ele.explicit_wait("VCFE_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete_yes")
                return True
            time.sleep(3)
        except:
            print("Creating custom schedule failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status


    def add_Paging_Group(self, params):
        """
        `Description:` This function will create Paging Group

        `Param:` params: Dictionary contains PageGroupInfo

        `Returns:` Extension Number

        `Created by:` rdoshi

        `Modified by :` Immani Mahesh Kumar , Saurabh Singh

        """
        #print params
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("Add_VCFE")
            self.action_ele.click_element("Add_PG")
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                self.action_ele.explicit_wait("pg_editor_panel")
                self.action_ele.click_element("pg_editor_panel")

            self.action_ele.explicit_wait('Pg_Name')
            self.action_ele.input_text("Pg_Name",params["Pg_Name"])
            time.sleep(3)
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            extn = self.query_ele.get_value("Pg_Extension")
            #extn += 1
            #self.action_ele.input_text("Pg_Extension",extn)
            if(params["Pg_Extension"]):
                self.action_ele.input_text("Pg_Extension",params["Pg_Extension"])
                extn=params["Pg_Extension"]
            if(params["Pg_privateExtension"]=="yes"):
                self.action_ele.select_checkbox("Pg_PrivateExtension")
            if(params["Pg_Location"]=="random"):
                self.action_ele.select_from_dropdown_using_index("Pg_Location",1)
                time.sleep(3)
            self.action_ele.select_from_dropdown_using_text("Pg_ExtensionList", params['extnlistname'])
            self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            self.action_ele.explicit_wait("fnMessageBox_OK")
            time.sleep(1)
            self.action_ele.click_element("fnMessageBox_OK")
            return extn
        except:
            print("Adding Page Group Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def delete_vcfe_components(self,params):
        """
        `Description:` This function will delete all vcfe components

        `Param:` params: Dictionary contains all VCFE component info

        `Returns:` None

        `Created by:` rdoshi
        """
        self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        params = defaultdict(lambda: '', params)
        #rows = self._browser.elements_finder(mapDict['VCFE_datagrid']["BY_VALUE"] + r'//*[@id="datagrid_vcfComponentsGrid"]/div[5]/div/div[contains(@class, "ui-widget-content")]')
        #rows.append(self._browser.elements_finder(mapDict['VCFE_datagrid']["BY_VALUE"] + "//[@class='ui-widget-content slick-row even']"))
        rows = self._browser.elements_finder("VCFE_datagrid")
        while rows:
            row=rows.pop(0)
            div_list=row.find_elements_by_tag_name("div")
            checkbox=div_list[0].find_element_by_tag_name("input")
            vcfe_name=div_list[1].text
            vcfe_type=div_list[3].text
            vcfe_extn=div_list[2].text
            if (params['VCFE_Name']=="Tenant Auto-Attendant" ):
                #rows.append(row)
                continue
            if(params['VCFE_Name'] == vcfe_name and vcfe_type == "Extension List"):
                extn_list=params
                checkbox.click()
                time.sleep(4)
                self.action_ele.click_element('VCFE_delete')
                time.sleep(4)
                self.action_ele.click_element('VCFE_delete_yes')
                try:
                    element = self._browser.element_finder("VCFE_extn_list_error")
                    time.sleep(3)
                    error_div=self._browser.element_finder("VCFE_error_text")
                    error_text=error_div.text
                    vcfe_list=re.findall(r"'(.*?)'", error_text, re.DOTALL)
                    time.sleep(2)
                    self.action_ele.click_element('fnMessageBox_OK')
                    time.sleep(5)
                    for entry in vcfe_list:
                            entry_details={'VCFE_Name':entry}
                            self.action_ele.input_text('VCFE_entry_search',entry)
                            #self.delete_vcfe_entries(entry_details)
                            rows = self._browser.elements_finder("VCFE_datagrid")
                            while rows:
                                row = rows.pop(0)
                                div_list = row.find_elements_by_tag_name("div")
                                checkbox = div_list[0].find_element_by_tag_name("input")
                                checkbox.click()
                                self.action_ele.click_element('VCFE_delete')
                                time.sleep(2)
                                self.action_ele.click_element('VCFE_delete_yes')
                                time.sleep(5)
                                rows = self._browser.elements_finder("VCFE_datagrid")
                    self.action_ele.clear_input_text('VCFE_entry_search')
                    self.delete_vcfe_entries(extn_list)
                except:
                       return
            if (params['VCFE_Extn']==" " or params['VCFE_Extn']=='' ):
                if(params['VCFE_Name']==vcfe_name):
                    checkbox.click()
                    self.action_ele.click_element('VCFE_delete')
                    time.sleep(2)
                    self.action_ele.click_element('VCFE_delete_yes')
                    time.sleep(5)
                    rows = self._browser.elements_finder("VCFE_datagrid")
                    return
            elif(vcfe_extn and int(params['VCFE_Extn'])==int(vcfe_extn) and params['VCFE_Name']==vcfe_name):
                checkbox.click()
                self.action_ele.click_element('VCFE_delete')
                time.sleep(2)
                self.action_ele.click_element('VCFE_delete_yes')
                time.sleep(5)
                rows = self._browser.elements_finder("VCFE_datagrid")
                return

    def verify_vcfe_entries_deleted(self,params):
        """
        `Description:` To verify that the vcfe entries are got deleted

        `:param params: Dictionary contains all VCFE component info

        `Returns:` True/False

        `Created by:` rdoshi

        """
        try:
            time.sleep(2)
            rows=self._browser.elements_finder("VCFE_datagrid")
            for row in rows:
                    div_list = row.find_elements_by_tag_name("div")
                    vcfe_name = div_list[1].text
                    vcfe_extn = div_list[2].text
                    if (params['VCFE_Extn'] == " " or params['VCFE_Extn'] == ''):
                        if(vcfe_name==params['VCFE_Name']):
                            return False
                        else:
                            continue
                    elif (vcfe_extn == params['VCFE_Extn'] and vcfe_name==params['VCFE_Name']):
                        return False
            return True
        except Exception, e:
            print(e)
            print("Verify VCFE delete failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def delete_vcfe_entries(self, params):
        """
        `Description:` To delete vcfe entries

        `:param params: Dictionary contains all VCFE component info

        `Returns:` None

        `Created by:` rdoshi
        """
        params = defaultdict(lambda: '', params)
        rows = self._browser.elements_finder("VCFE_datagrid")
        while rows:
            row = rows.pop(0)
            div_list = row.find_elements_by_tag_name("div")
            checkbox = div_list[0].find_element_by_tag_name("input")
            vcfe_name = div_list[1].text
            vcfe_type = div_list[3].text
            vcfe_extn = div_list[2].text
            if (params['VCFE_Name'] == "Tenant Auto-Attendant"):
                # rows.append(row)
                continue
            if (params['VCFE_Name'] == vcfe_name and vcfe_type == "Extension List"):
                extn_list = params
                checkbox.click()
                time.sleep(4)
                self.action_ele.click_element('VCFE_delete')
                time.sleep(4)
                self.action_ele.click_element('VCFE_delete_yes')
                try:
                    element = self._browser.element_finder("VCFE_extn_list_error")
                    time.sleep(3)
                    error_div = self._browser.element_finder("VCFE_error_text")
                    error_text = error_div.text
                    vcfe_list = re.findall(r"'(.*?)'", error_text, re.DOTALL)
                    time.sleep(2)
                    self.action_ele.click_element('fnMessageBox_OK')
                    time.sleep(5)
                    for entry in vcfe_list:
                        entry_details = {'VCFE_Name': entry}
                        self.action_ele.input_text('VCFE_entry_search', entry)
                        # self.delete_vcfe_entries(entry_details)
                        rows = self._browser.elements_finder("VCFE_datagrid")
                        while rows:
                            row = rows.pop(0)
                            div_list = row.find_elements_by_tag_name("div")
                            checkbox = div_list[0].find_element_by_tag_name("input")
                            checkbox.click()
                            self.action_ele.click_element('VCFE_delete')
                            time.sleep(2)
                            self.action_ele.click_element('VCFE_delete_yes')
                            time.sleep(5)
                            rows = self._browser.elements_finder("VCFE_datagrid")
                    self.action_ele.clear_input_text('VCFE_entry_search')
                    self.delete_vcfe_entries(extn_list)
                except:
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    return
            if (params['VCFE_Extn'] == " " or params['VCFE_Extn'] == ''):
                if (params['VCFE_Name'] == vcfe_name):
                    checkbox.click()
                    self.action_ele.click_element('VCFE_delete')
                    time.sleep(2)
                    self.action_ele.click_element('VCFE_delete_yes')
                    time.sleep(5)
                    rows = self._browser.elements_finder("VCFE_datagrid")
                    return
            elif (vcfe_extn and int(params['VCFE_Extn'])==int(vcfe_extn) and params['VCFE_Name'] == vcfe_name):
                checkbox.click()
                self.action_ele.click_element('VCFE_delete')
                time.sleep(2)
                self.action_ele.click_element('VCFE_delete_yes')
                time.sleep(5)
                rows = self._browser.elements_finder("VCFE_datagrid")
                return

##################################################################################################################
#regression function
    def verify_pickup_group(self, ext):
        """
        `Description:` This function will verify pickup group by searching extension

        `Param1:` pickup group extension number - ext

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = False
            self.action_ele.explicit_wait("pg_extension_head")
            time.sleep(3)
            self.action_ele.input_text("pg_extension_head",ext)
            if self.query_ele.get_text("pg_extension_number")==ext:
                status = True
            time.sleep(1)
            self.action_ele.clear_input_text('pg_extension_head')
            time.sleep(2)
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def edit_pickup_group(self, params):
        """
        `Description:` This function will edit pickup group details

        `Param:`  params: Dictionary contains pickup group details - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh

        `Modified by :` Vasuja K
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            time.sleep(2)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")

            if params['pickupgpname']== "Delete":
                self.action_ele.explicit_wait('pg_edit_page_text_box')
                self.action_ele.clear_input_text('pg_edit_page_text_box')
                time.sleep(1)
                self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
                time.sleep(3)
                status = True
                print(status)
                return status

            if params['PGExtn']== "Delete":
                self.action_ele.explicit_wait('vcfe_pickup_group_extn')
                self.action_ele.clear_input_text('vcfe_pickup_group_extn')

            if params['PGExtn']!= '' and params['PGExtn']!= "Delete":
                self.action_ele.explicit_wait('vcfe_pickup_group_extn')
                self.action_ele.clear_input_text('vcfe_pickup_group_extn')
                self.action_ele.input_text('vcfe_pickup_group_extn', params['PGExtn'])


            if params['pickuploc']== "Remove":
                self.action_ele.explicit_wait('vcfe_pickup_group_location')
                self.action_ele.select_from_dropdown_using_index('vcfe_pickup_group_location', 0)
                time.sleep(1)
                self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
                time.sleep(3)
                status = True
                print(status)
                return status

            time.sleep(1)
            if params['pickupgpname'] != '' and params['pickupgpname'] != "Delete":
                self.action_ele.explicit_wait("pg_edit_page_text_box")
                self.action_ele.clear_input_text('pg_edit_page_text_box')
                self.action_ele.input_text('pg_edit_page_text_box',params['pickupgpname'])

            if params['extnlistname'] != '':
                self.action_ele.select_from_dropdown_using_text('pg_edit_page_drop', params['extnlistname'])
            time.sleep(1)
            self.action_ele.click_element("pg_edit_finish_button")
            time.sleep(3)
            errors = []
            errors = self._browser.elements_finder('vcfe_val_errors')
            if errors:
                for error in errors:
                    if "The extension is not available" in error.text:
                        print(self.query_ele.get_text("vcfe_val_errors"))
                        status = True
                        print(status)
                        return status
            self.action_ele.explicit_wait("fnMessageBox_OK")
            self.action_ele.click_element("fnMessageBox_OK")
            self.action_ele.explicit_wait("VCFE_datagrid")
            status = True
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_edited_pickup_group(self, params):
        """
        `Description:` This function will verify the given pickup group details

        `Param:`  params: Dictionary contains pickup group details - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            time.sleep(2)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)
            status = False
            if params['pickupgpname']!= '':
                value_from_text_box = self.query_ele.get_value("pg_edit_page_text_box")
                print("Expected value: %s" % params["pickupgpname"])
                print("Actual value from textbox is: %s" % value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["pickupgpname"])
                status = True
                time.sleep(3)

            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.explicit_wait("vcfe_cancel_button")
            self.action_ele.click_element("vcfe_cancel_button")

        except AssertionError as assert_err:
            print("ASSERTION ERROR: %s" % assert_err.message)
            status = False

        except Exception, e:
            print(e)
            print("Verifying holidays schedule failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            status = False

        finally:
            return status

    def delete_vcfe_entry(self, ext):
        """
        `Description:` To delete vcfe entries

        `Param:`  params: Dictionary contains all VCFE component info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(3)
            self.action_ele.explicit_wait("pg_extension_head")
            time.sleep(1)
            self.action_ele.clear_input_text("pg_extension_head")
            self.action_ele.input_text("pg_extension_head", ext)
            time.sleep(2)
            if self.query_ele.get_text("pg_extension_number") == ext:
                self.action_ele.click_element("pg_delete")
                self.action_ele.explicit_wait("VCFE_delete")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete")
                self.action_ele.explicit_wait("VCFE_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete_yes")
                self.action_ele.explicit_wait("fnMessageBox_OK", ec="element_to_be_clickable")
                self.action_ele.click_element("fnMessageBox_OK")
                for i in range(5):
                    extention_list = self._browser.elements_finder("pg_ext_list")
                    if len(extention_list)==0:
                        status = True
                        break
                    time.sleep(3)
            self.action_ele.clear_input_text('pg_extension_head')
                #self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def __editor_panel(self,params):
        """
        `Description:` To edit vcfe entries

        `Param1:'  VCFE Extension

        `Returns:` None

        `Created by:` Saurabh Singh
        """
        try:
            time.sleep(5)
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("pg_extension_head")
            time.sleep(1)
            self.action_ele.input_text("pg_extension_head",params['Pg_Extension'])
            time.sleep(1)
            check_elements = self._browser.elements_finder("pg_edit_checkbox")
            check_elements[1].click()
            time.sleep(1)
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
            time.sleep(1)
            self.action_ele.click_element("pg_edit_button")
            elements= self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def edit_paging_group(self, params):
        """
            `Description:` Editing the selected paging group

            `:param params: Dictionary contains	info about fields that has to be edited like Name, Location, Sync delay...

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:

            pg_extn_error = "Extension is a required field. Please select an extension"
            pg_name_error = "Failed updating component. Error: dn.Description - can't be blank"
            pg_loc_error = "An error occurred while trying to Update Vcf Component Programming Profile. The Site does not have an associated location."
            status = False
            self.__editor_panel(params)
            self.action_ele.explicit_wait("pgg_edit_page_name")
            self.action_ele.clear_input_text('pgg_edit_page_name')
            self.action_ele.input_text('pgg_edit_page_name', params['Pg_Name'])
            self.action_ele.select_from_dropdown_using_text('pgg_extention_list', params['extnlistname'])
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if params['mode'] != '':
                check_box = self._browser.elements_finder("pgg_epp_check")
                if not check_box[0].is_selected():
                    check_box[0].click()
                    time.sleep(1)
                    if self.query_ele.get_text('pgg_active_audio') == params["mode"]:
                        self.action_ele.click_element("pgg_active_audio_btn")
                    elif self.query_ele.get_text('pgg_speaker') == params["mode"]:
                        self.action_ele.click_element("pgg_speaker_btn")
                    else:
                        print("option is not present on page")
                        status = False
                        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                        return status
                else:
                    if self.query_ele.get_text('pgg_active_audio') == params["mode"]:
                        self.action_ele.click_element("pgg_active_audio_btn")
                    elif self.query_ele.get_text('pgg_speaker') == params["mode"]:
                        self.action_ele.click_element("pgg_speaker_btn")
                    else:
                        print("option is not present on page")
                        status = False
                        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                        return status
            else:
                pass
            if params['Pg_Location']:
                self.action_ele.select_from_dropdown_using_text("Pg_Location", params['Pg_Location'])
                time.sleep(3)
            if params['sync_delay'] != '':
                self.action_ele.input_text("pgg_sync_delay", params['sync_delay'])
            else:
                pass
            if params['Remove_Extn'].lower() == "true":
                self.action_ele.clear_input_text("Pg_Extension")
                time.sleep(1)
                self.action_ele.click_element("pg_edit_finish_button")
                time.sleep(1)
                self.action_ele.click_element("pg_edit_finish_button")
                if self.verify_error_and_click_cancel(pg_extn_error):
                    return True
            if params['Remove_Name'].lower() == "true":
                self.action_ele.clear_input_text("Pg_Name")
                time.sleep(1)
                self.action_ele.click_element("pg_edit_finish_button")
                if self.verify_error_and_click_cancel(pg_name_error):
                    return True
            if params['Remove_Location'].lower() == "true":
                self.action_ele.select_from_dropdown_using_index("Pg_Location", 0)
                time.sleep(1)
                self.action_ele.click_element("pg_edit_finish_button")
                if self.verify_error_and_click_cancel(pg_loc_error):
                    return True
            if params['Make_extn_private'].lower() == "true":
                self.action_ele.select_checkbox("Pg_PrivateExtension")
            if params['No_Ans_Rings']:
                self.action_ele.clear_input_text("vcfe_hg_noAnswerRings")
                self.action_ele.input_text("vcfe_hg_noAnswerRings", params['No_Ans_Rings'])
            if params['Include_in_sys_dir']:
                self.action_ele.unselect_checkbox("pg_include_dial_by_name")

            self.action_ele.click_element("pg_edit_finish_button")
            self.action_ele.explicit_wait("fnMessageBox_OK")
            time.sleep(1)
            self.action_ele.click_element("fnMessageBox_OK")
            self.action_ele.explicit_wait("pg_add_btn")
            self.action_ele.clear_input_text("pg_extension_head")
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def vcfe_invalid_extention(self,params):
        """
        `Description:` To check invalid extention for vcfe

        `Param:`  params: Dictionary contains all VCFE component info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("Add_VCFE")
            self.action_ele.click_element("Add_PG")
            time.sleep(2)
            elements= self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)
            self.action_ele.input_text("Pg_Name",params["Pg_Name"])
            self.action_ele.clear_input_text("Pg_Extension")
            time.sleep(1)
            self.action_ele.input_text("Pg_Extension",params["Pg_Extension"])
            time.sleep(3)
            if (params["Pg_Location"] == "random"):
                self.action_ele.select_from_dropdown_using_index("Pg_Location", 1)
                time.sleep(3)
            if "The extension is not available. Suggested extension : " in self.query_ele.get_text("pgg_extension_error"):
                print(self.query_ele.get_text("pgg_extension_error"))
                status = False
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element("pgg_cancel_button")
            self.action_ele.explicit_wait("VCFE_delete_yes")
            time.sleep(1)
            self.action_ele.click_element("VCFE_delete_yes")
            self.action_ele.explicit_wait("Add_VCFE")
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        except Exception, e:
            print(e)
            print("Validation Failed!!")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def vcfe_jump_extention_list(self,params):
        try:
            status = False
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("Add_VCFE")
            self.action_ele.click_element("Add_PG")
            self.action_ele.input_text("Pg_Name",params["Pg_Name"])
            time.sleep(3)
            if (params["Pg_Location"] == "random"):
                self.action_ele.select_from_dropdown_using_index("Pg_Location", 1)
                time.sleep(3)
            self.action_ele.click_element("pgg_open_schdule")
            self.action_ele.explicit_wait("VCFE_delete_yes")
            time.sleep(1)
            self.action_ele.click_element("VCFE_delete_yes")
            panel= self._browser.elements_finder("pgg_svg_panel")
            if panel[0].is_displayed():
                print("Panel is opened properly")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            else:
                print("Panel is not opened")
                status = False
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return status
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element("pgg_cancel_button")
            self.action_ele.explicit_wait("Add_VCFE")
            status = True
        except Exception, e:
            print(e)
            print("Validation Failed!!")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def edit_custome_schedule(self, params):
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = False
            time_error = "Failed updating component.Error: schedule_items.stop_time - Stop time should be different"
            message1 = "Component was updated successfully"
            error = "Failed creating component. Error: ScheduleName - has already been taken"
            blank_error = "Failed creating component. Error: ScheduleName - can't be blank"
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            if params['editName'] != "":
                self.action_ele.input_text("VCFE_entry_search", params['editName'])
            else:
                pass
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
            time.sleep(1)
            check_elements = self._browser.elements_finder("pg_edit_checkbox")
            check_elements[1].click()
            time.sleep(1)
            self.action_ele.click_element("pg_edit_button")
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)

            self.action_ele.input_text('vcfe_custom_schedule_name', params['customScheduleName'])
            time.sleep(2)
            if params['timeZone'] and params['timeZone'] == "clear":
                self.action_ele.select_from_dropdown_using_index('vcfe_selScheduleTimezone', 0)
            elif params['timeZone'] and params['timeZone'] != "clear":
                self.action_ele.select_from_dropdown_using_text('vcfe_selScheduleTimezone', params['timeZone'])
            # self.action_ele.click_element("vcfe_add_button")
            self.action_ele.input_text('vcfe_custom_name', params['customName'])
            self.action_ele.clear_input_text("vcfe_custom_date")
            self.action_ele.input_text('vcfe_custom_date', params['customDate'])
            self.action_ele.click_element("cs_label")
            self.action_ele.clear_input_text("vcfe_custom_starttime")
            self.action_ele.input_text('vcfe_custom_starttime', params['startTime'])
            self.action_ele.clear_input_text("vcfe_custom_stoptime")
            self.action_ele.input_text('vcfe_custom_stoptime', params['stopTime'])
            time.sleep(3)
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['deletevcfeday'].lower() == "true":
                self.action_ele.click_element("vcfe_daydelete_icon")
            time.sleep(2)
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element("vcfe_pickup_finish")
            time.sleep(3)
            if message1 in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.explicit_wait("fnMessageBox_OK")
                time.sleep(1)
                self.action_ele.click_element("fnMessageBox_OK")
                return True
                self.action_ele.explicit_wait("add_button")
            elif blank_error or error or time_error in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.click_element("fnMessageBox_OK")
                self.action_ele.click_element("pgg_cancel_button")
                self.action_ele.explicit_wait("VCFE_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete_yes")
                time.sleep(2)
                return True
            time.sleep(3)
            self.action_ele.explicit_wait("pg_add_btn")
            self.action_ele.clear_input_text("VCFE_entry_search")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def delete_vcfe_day_name(self, params):
        try:
            status = False
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            if params['editName']!="":
                self.action_ele.input_text("VCFE_entry_search",params['editName'])
            else:
                pass
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
            time.sleep(1)
            check_elements = self._browser.elements_finder("pg_edit_checkbox")
            check_elements[1].click()
            time.sleep(1)
            self.action_ele.click_element("pg_edit_button")
            time.sleep(1)
            elements= self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)
            self._browser._browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.clear_input_text("vcfe_custom_schedule_name")
            time.sleep(1)
            self.action_ele.click_element("vcfe_pickup_finish")
            time.sleep(3)
            if "Failed updating component. Error: ScheduleName - can't be blank" == self.query_ele.get_text("cs_error"):
                print("Error Occured")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            else:
                print(self.query_ele.get_text("cs_error"))
                status= True
            self.action_ele.explicit_wait("fnMessageBox_OK")
            time.sleep(1)
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(3)
            self.action_ele.click_element("pgg_cancel_button")
            time.sleep(1)
            self.action_ele.click_element("VCFE_delete_yes")
            time.sleep(3)
            self.action_ele.explicit_wait("pg_add_btn")
            self.action_ele.clear_input_text("VCFE_entry_search")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def edit_extension_list(self,params):
        edit_ext_list_name_blank = "Failed updating component. Error: Name - can't be blank"
        ext_list_name_already_taken = "Failed updating component. Error: Name - has already been taken"
        ext_list_cannot_remove_all_extns = "Select atleast one user from the available list"
        try:
            status = False
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            #console(params)
            #console(params['editName'])
            # if params['editName']!="":
            #     self.action_ele.input_text("VCFE_entry_search",params['editName'])
            #     time.sleep(3)
            # else:
            #     pass
            # self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
            # time.sleep(1)
            # check_elements = self._browser.elements_finder("pg_edit_checkbox")
            # check_elements[1].click()
            time.sleep(1)
            self.action_ele.click_element("pg_edit_button")
            time.sleep(1)
            elements= self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)
            self._browser._browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            if params['extnNumber']:
                self.action_ele.input_text('vcfe_EL_Search', params['extnNumber'])
                self.action_ele.click_element("vcfe_Select_Extn")
                self.action_ele.clear_input_text('vcfe_EL_Search')
                time.sleep(1)
            if params['extnlistname'] == "blank":
                self.action_ele.clear_input_text('vcfe_extnlist_name')
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(2)
                if self.verify_error_and_click_cancel(edit_ext_list_name_blank):
                    status = True
            elif params['extnlistname'] and params['extnlistname'] != "blank":
                self.action_ele.clear_input_text('vcfe_extnlist_name')
                self.action_ele.input_text('vcfe_extnlist_name', params['extnlistname'])
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(1)
                if self.verify_error_and_click_cancel(ext_list_name_already_taken):
                    status = True
            elif params['extnlist'].lower() == "remove":
                extn_list=self._browser.elements_finder('el_remove_extn')
                for extn in extn_list:
                    time.sleep(1)
                    extn.click()
                time.sleep(2)
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(1)
                if ext_list_cannot_remove_all_extns in self.query_ele.get_text("Aa_edit_confirm"):
                    self.action_ele.click_element("fnMessageBox_OK")
                    status = True
                    time.sleep(1)
                self.action_ele.click_element("pgg_cancel_button")
            else:
                self.action_ele.click_element("pg_edit_finish_button")
                self.action_ele.explicit_wait("fnMessageBox_OK")
                time.sleep(1)
                self.action_ele.click_element("fnMessageBox_OK")
                self.action_ele.explicit_wait("pg_add_btn")
                status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        self.action_ele.clear_input_text("VCFE_entry_search")
        return status

    def edit_auto_attendant(self, params):
        """
            `Description:` Edit Auto Attendant like name, location, Multiple digit Time out etc...

            `:param params: Dictionary contains Auto Attendant info like name, location, Multiple digit Time out etc...

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = False
            message1 = 'Component was updated successfully'
            message2 = 'Please enter a value between 1000 and 7000.'
            message3 = 'The extension is not available. Suggested extension :'
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            for i in range(4):
                if "Processing..." in self._browser._browser.page_source:
                    time.sleep(2)
                else:
                    break
            time.sleep(1)
            self.action_ele.click_element("pg_edit_button")
            time.sleep(2)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)
            if (params['Assign_vcfe_component'] != "" or params['Edit_vcfe_component'] != "") \
                    and params['neg'] == "False":
                status1 = self.assign_vcfe_component(params)
                if status1 is True:
                    status = True
            elif params['Validate_vcfe_name'] != '':
                status1 = self.validate_vcfe_names(params)
                if status1 is True:
                    return True

            elif params['Location'] != "" and params['neg'] == "False":
                time.sleep(1)
                self.action_ele.select_from_dropdown_using_text("Aa_Location",
                                                                params["Location"])
                time.sleep(1)
                status = True
            elif params['Location'] == "Remove" and params['neg'] == "True":
                time.sleep(1)
                self.action_ele.select_from_dropdown_using_index("Aa_Location", 0)
                time.sleep(1)
            elif params['Aa_Name'] != " " and params['neg'] == "False":
                time.sleep(1)
                self.action_ele.clear_input_text("Aa_Name")
                self.action_ele.input_text("Aa_Name", params['Aa_Name'])
                time.sleep(1)
                status = True
            elif params['Aa_Name'] == "Remove" and params['neg'] == "True":
                time.sleep(1)
                self.action_ele.clear_input_text("Aa_Name")
                time.sleep(1)
            elif params['Aa_Extn'] != '' and params['neg'] == "True":
                time.sleep(1)
                if params['Aa_Extn'] == "Remove":
                    self.action_ele.clear_input_text("Aa_Extension")
                else:
                    self.action_ele.clear_input_text("Aa_Extension")
                    time.sleep(1)
                    self.action_ele.input_text('Aa_Extension', params['Aa_Extn'])
                time.sleep(1)
                self.action_ele.click_element("Aa_click_out")
                time.sleep(2)
                err_chk = self._browser.element_finder("vcfe_val_errors")
                time.sleep(1)
                if message3 in err_chk.text:
                    self.action_ele.click_element("vcfe_cancel_button")
                    self.action_ele.explicit_wait("VCFE_delete_yes")
                    time.sleep(1)
                    self.action_ele.click_element("VCFE_delete_yes")
                    return True
            if params['MDT'] != '':
                for x in params['MDT']:
                    time.sleep(2)
                    if x.isdigit() and 1000 <= int(x) <= 7000:
                        self.action_ele.clear_input_text("Aa_edit_MDT")
                        self.action_ele.input_text("Aa_edit_MDT", x)
                        status = True
                        break
                    else:
                        self.action_ele.clear_input_text("Aa_edit_MDT")
                        self.action_ele.input_text("Aa_edit_MDT", x)
                        self.action_ele.click_element("Aa_click_out")
                        err_chk = self._browser.element_finder("vcfe_mdt_errors")
                        if err_chk.text == message2:
                            status = True
                            pass
                        else:
                            return False
            self.action_ele.click_element("Aa_finishAA")
            time.sleep(2)
            errors = self._browser.elements_finder('vcfe_val_error')
            if errors:
                for error in errors:
                    if "This field is required" in error.text:
                        self.action_ele.click_element("vcfe_cancel_button")
                        self.action_ele.explicit_wait("VCFE_delete_yes")
                        time.sleep(1)
                        self.action_ele.click_element("VCFE_delete_yes")
                        return True
            time.sleep(2)
            self.action_ele.explicit_wait("fnMessageBox_OK")
            if message1 in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.click_element("fnMessageBox_OK")
                return status
            else:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

                return False
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def delete_vcfe_by_name(self, vcfe_name):
        """
            `Description:` This Method helps to delete a vcfe component by name Such as Schedules which do not have
                            Extensions

            `:param vcfe_name: Name of the VCFE component to be deleted

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = False
            time.sleep(3)
            self.action_ele.clear_input_text("pg_extension_head")
            self.action_ele.clear_input_text("VCFE_entry_search")
            self.action_ele.input_text("VCFE_entry_search", vcfe_name)
            time.sleep(1)
            check_elements = self._browser.elements_finder("pg_edit_checkbox")
            check_elements[0].click()
            self.action_ele.explicit_wait("VCFE_delete")
            time.sleep(1)
            self.action_ele.click_element("VCFE_delete")
            self.action_ele.explicit_wait("VCFE_delete_yes")
            time.sleep(1)
            self.action_ele.click_element("VCFE_delete_yes")
            time.sleep(5)
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(2)
            for i in range(5):
                extention_list = self._browser.elements_finder("pg_ext_list")
                if len(extention_list) == 0:
                    status = True
                    break
                else:
                    print("VCFE grid is not loaded yet. Extending wait")
                    time.sleep(3)
            self.action_ele.clear_input_text("VCFE_entry_search")
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def upload_prompt(self,params):
        """
            `Description:` This Method helps to add prompt for Auto Attendant schedules. This method can run on windows only due to dependency on
        "autoit" package.

            `:param params: Dictionary contains	type of schedule and name of the schedule to be validated.

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:
            try:
                import autoit
            except ImportError as e:
                print e.msg
            status=False
            self.action_ele.click_element('vcfe_upload_prompt')
            time.sleep(3)  # this is for the path to resolve in the browse window
            console(autoit.win_exists("[TITLE:Open]"))
            autoit.win_activate("Open")
            autoit.control_send("[TITLE:Open]", "Edit1", params["filePath"])
            #autoit.control_send("[CLASS:#32770]", "Edit1", params["filePath"])
            time.sleep(3)
            autoit.control_click("[TITLE:Open]", "Button1")
            time.sleep(2)
            if "prompt.wav" in  self.query_ele.get_text("vcfe_verify_prompt"):
                status=True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def validate_vcfe_names(self,params):
        """
            `Description:` This Method helps to validate whether Assigned Schedules are displayed properly for an
                            Auto Attendant.

            `:param params: Dictionary contains	type of schedule and name of the schedule to be validated.

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status1=False
            NameCheck=self._browser.elements_finder("vcfe_name_check")
            if(params['Validate_vcfe_name'])=="CustomSchedule":
                if params['vcfe_name'] == NameCheck[2].text:
                    print(NameCheck[2].text)
                    status1=True
            if (params['Validate_vcfe_name']) == "HolidaySchedule":
                if params['vcfe_name'] == NameCheck[1].text:
                    print(NameCheck[1].text)
                    status1 = True
            if (params['Validate_vcfe_name']) == "OnHoursSchedule":
                if params['vcfe_name'] == NameCheck[0].text:
                    print(NameCheck[0].text)
                    status1 = True
            time.sleep(1)
            self.action_ele.click_element("vcfe_cancel_button")

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status1

    def assign_vcfe_component(self, params):
        """
            `Description:` Helps to assign a schedule for an Auto Attendant

            `:param params: Dictionary contains	info about schedule to be assigned to AA and operations to be performed
                            on that schedule.

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['Assign_vcfe_component'] == "CustomSchedule" or \
                            params['Edit_vcfe_component']== "CustomSchedule":
                self.action_ele.click_element("vcfe_assign_CustomSchedule")
                time.sleep(2)
                self.action_ele.select_from_dropdown_using_text("vcfe_select_schedule", params["Assign_vcfe_Name"])
                time.sleep(2)
            elif params['Assign_vcfe_component'] == "HolidaySchedule" or \
                            params['Edit_vcfe_component'] == "HolidaySchedule":
                self.action_ele.click_element("vcfe_assign_HolidaySchedule")
                time.sleep(2)
                self.action_ele.select_from_dropdown_using_text("vcfe_select_schedule", params["Assign_vcfe_Name"])
                time.sleep(2)
                if params['verify_interactive_diagram'] == "True":
                    time.sleep(1)
                    status2 = self.verify_in_interactive_diagram(params)
                    if status2:
                        status=True
                    else:
                        console("vcfe component not verified on vcfe interactive diagram")


            elif params['Assign_vcfe_component'] == "OnHoursSchedule" or \
                            params['Edit_vcfe_component'] == "OnHoursSchedule":
                self.action_ele.click_element("vcfe_assign_OHSchedule")
                time.sleep(2)
                self.action_ele.select_from_dropdown_using_text("vcfe_select_schedule", params["Assign_vcfe_Name"])
                time.sleep(2)

            if params['Remove_Operations'] == "All":
                elements = self._browser.elements_finder("ohs_remove_operations")
                time.sleep(1)
                elements[0].click()
                time.sleep(1)
                elements[1].click()
                time.sleep(1)
                elements[2].click()
                time.sleep(1)
                status = True

            if params['Monitor'] == "Disable":
                self.action_ele.click_element('ohs_disable_monitor')
                time.sleep(2)
                status=True
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['Multiple_Digit_Operation'] != '':
                self.action_ele.click_element("ohs_show_MDO")
                elements = self._browser.elements_finder("ohs_multiple_digit_operation")
                for element in elements:
                    if element.is_displayed():
                        if params['Multiple_Digit_Operation'] == "GoToMenu":
                            Select(element).select_by_visible_text('Go to menu')
                        elif params['Multiple_Digit_Operation'] == "TransferToExtension":
                            Select(element).select_by_visible_text('Transfer to extension')
                        elif params['Multiple_Digit_Operation'] == "TakeAMessage":
                            Select(element).select_by_visible_text('Take a message')
                        time.sleep(2)
                        extn_field = self._browser.element_finder("ohs_mdo_extn_field")
                        extn_field.clear()
                        extn_field.send_keys(params["MDO_Extension"])
                        time.sleep(2)
                        self.action_ele.click_element("ohs_save_ckbox")
                        time.sleep(5)
                        status = True
                        break
                    else:
                        pass

            if params['Press_one_Operation'] != '':
                self.action_ele.click_element("ohs_show_MDO")
                elements = self._browser.elements_finder("ohs_Press_one_Operation")
                for element in elements:
                    if element.is_displayed():
                        if params['Press_one_Operation'] == "GoToMenu":
                            Select(element).select_by_visible_text('Go to menu')
                        elif params['Press_one_Operation'] == "TransferToExtension":
                            Select(element).select_by_visible_text('Transfer to extension')
                        elif params['Press_one_Operation'] == "TakeAMessage":
                            Select(element).select_by_visible_text('Take a message')
                        time.sleep(2)
                        extn_field = self._browser.element_finder("ohs_mdo_extn_field")
                        extn_field.clear()
                        extn_field.send_keys(params["MDO_Extension"])
                        time.sleep(2)
                        self.action_ele.click_element("ohs_save_ckbox")
                        status = True
                        break
                    else:
                        pass


            if params['Press_0_Option'] != '':
                self.action_ele.click_element("ohs_show_MDO")
                elements = self._browser.elements_finder("ohs_Press_0_Option")
                for element in elements:
                    if element.is_displayed():
                        if params['Press_0_Option'] == "GoToMenu":
                            Select(element).select_by_visible_text('Go to menu')
                        elif params['Press_0_Option'] == "TransferToExtension":
                            Select(element).select_by_visible_text('Transfer to extension')
                        elif params['Press_0_Option'] == "TakeAMessage":
                            Select(element).select_by_visible_text('Take a message')
                        elif params['Press_0_Option'] == "GoToExtension":
                            Select(element).select_by_visible_text('Go to extension')
                        time.sleep(2)
                        extn_field = self._browser.element_finder("ohs_mdo_extn_field")
                        extn_field.clear()
                        extn_field.send_keys(params["P0_Extension"])
                        time.sleep(2)
                        self.action_ele.click_element("p0_save_ckbox")
                        status = True
                        break
                    else:
                        pass

            if params['Adjust_Timeout']:
                adjust_status = self.vcfe_adjust_timeout(params)
                if adjust_status:
                    status = True
                else:
                    console("Adjust Timeout for vcfe component failed")
                    status = False

            if params['prompt'] == 'Enable':
                status1 = self.upload_prompt(params)
                if status1:
                    status = True
                else:
                    console("prompt was not uploaded Properly")
                    status = False
            else:
                status = True

        except Exception, e:
            print(e)
        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status



    def create_on_hours_schedule(self, params):
        """
            `Description:` Create On Hours  schedule

            `:param params: Dictionary contains	On-Hours Schedule info like Schedule Name and TIme zone

            `return:` Schedule name

             `created by:` Immani Mahesh Kumar
         """
        error1 = 'Failed creating component. Error: ScheduleName - has already been taken'
        try:
            message1 = 'Component was created successfully'
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_add_dropdown")
            self.action_ele.click_element("ohs_add_OnHours_schedule")
            time.sleep(3)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)
            self.action_ele.clear_input_text("ohs_name")
            self.action_ele.input_text("ohs_name", params['scheduleName'])
            if params['timezone']:
                self.action_ele.select_from_dropdown_using_text("vcfe_selScheduleTimezone",params['timezone'])
                time.sleep(2)
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(3)
            self.action_ele.explicit_wait("fnMessageBox_OK")
            time.sleep(1)
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(2)
            self.action_ele.explicit_wait("vcfe_add_dropdown")
            return params['scheduleName']

        except:
            print("On-Hours schedule creation failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_hunt_group(self, params):
        """
        `Description:` To verify the presence of created hunt group in VCFE component list by searching extension

        `Param1:' Hunt Group Extension number

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
            for i in range(4):
                # TODO: Links has to be identified and clicked.
                try:
                    self.action_ele.click_element('phone_system_nav')
                    time.sleep(2)
                    self.action_ele.click_element("Visual_Call_Flow_Editor")
                    print("SWITCHING TO VCFE PAGE :%s" % i)
                    vcfe_loaded = self.action_ele.explicit_wait("vcfe_extension_textbox")
                    if vcfe_loaded:
                        result = True
                        break
                except:
                    print("Retrying click: %d" % i)
                    pass
            status = False
            time.sleep(2)
            #self.action_ele.explicit_wait('vcfe_extension_textbox')
            self.action_ele.input_text('vcfe_extension_textbox', params["hg_extn"])
            for i in range(3):
                var = self.query_ele.text_present(params["hg_extn"])
                if var:
                    status = True
                    break
                else:
                    time.sleep(1)
            self.action_ele.clear_input_text("vcfe_extension_textbox")
            return status
        except:
            print("Verify hunt group failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def select_vcfe_component_by_extension(self, params):
        """
        `Description:` Select a particular VCFE component after filtering by extension in VCFE page

        `Param1:' Any VCFE component Extension number - vcfe_comp

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            result = False
            self.action_ele.clear_input_text("VCFE_entry_search")
            self.action_ele.clear_input_text("vcfe_extension_textbox")

            time.sleep(2)
            for i in range(5):
                self.action_ele.clear_input_text("vcfe_extension_textbox")
                [self.action_ele.input_text_basic("vcfe_extension_textbox", e) for e in params["vcfe_comp"]]
                time.sleep(1)
                print self.query_ele.get_value_execute_javascript("document.getElementById('%s').value" % "headerRow_ExtensionData")
                if self.query_ele.get_value_execute_javascript("document.getElementById('%s').value" % "headerRow_ExtensionData") == params["vcfe_comp"]:
                    print("Extension is mathched")
                    status = True
                    break
                else:
                    print("Full extension has not been entered")

            self.action_ele.click_element("vcfe_checkbox")
            self.action_ele.explicit_wait("vcfe_vcfComponentsGrideditButton", ec="element_to_be_clickable")
            return status
        except:
            print("Could not select vcfe component")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def select_vcfe_component_by_name(self, params):
        """
        `Description:` Select a particular VCFE component after filtering by name in VCFE page

        `Param1:' Any VCFE component Name - vcfe_comp

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = False
            self.action_ele.clear_input_text("vcfe_extension_textbox")
            self.action_ele.clear_input_text("VCFE_entry_search")
            time.sleep(2)
            for i in range(5):
                #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                self.action_ele.clear_input_text("VCFE_entry_search")
                #[self.action_ele.input_text_basic("VCFE_entry_search", e) for e in params["vcfe_comp"]]
                self.action_ele.input_text("VCFE_entry_search", params["vcfe_comp"])
                if self.query_ele.get_value_execute_javascript("document.getElementById('%s').value"%"headerRow_ComponentName")==params["vcfe_comp"]:
                    print("Name mathched")
                    status = True
                    break
                else:
                    print("Full name has not been entered")

            self.action_ele.click_element("vcfe_checkbox")
            self.action_ele.explicit_wait("vcfe_vcfComponentsGrideditButton", ec="element_to_be_clickable")
            return status
        except:
            print("Could not select vcfe component")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def edit_hunt_group(self, params):
        """
        `Description:` Edit hunt group with different inputs

        `Param:`  params: Dictionary with Vcfe_variables

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            for i in range(4):
                try:
                    time.sleep(2)
                    elements = self._browser.elements_finder("pg_refresh_btn")
                    if elements[0].is_displayed():
                        pass
                    else:
                        self.action_ele.explicit_wait("pg_editor_panel", ec="element_to_be_clickable")
                        self.action_ele.click_element("pg_editor_panel")
                except:
                    print("Retrying click: %d" % i)
                    pass
            if params['Call_member_when_forwarding_all_calls'] == "True":
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Call_member_when_forwarding_all_calls"])
                self.action_ele.select_checkbox(HG_EDIT_ELEMENT["Call_member_when_forwarding_all_calls"])

            # if params['Call_member_when_forwarding_all_calls'] == "False":
            #     self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Call_member_when_forwarding_all_calls"])
            #     self.action_ele.unselect_checkbox(HG_EDIT_ELEMENT["Call_member_when_forwarding_all_calls"])
            # time.sleep(3)
            #
            if params['Skip_member_if_already_on_a_call'] == "True":
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Skip_member_if_already_on_a_call"])
                self.action_ele.select_checkbox(HG_EDIT_ELEMENT["Skip_member_if_already_on_a_call"])

            if params['Rings_per_Member']!='':
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Rings_per_Member"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["Rings_per_Member"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["Rings_per_Member"], params["Rings_per_Member"])

            if params['Distribution_pattern'] == "Simultaneous":
                #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Distribution_pattern_Simultaneous"])
                self.action_ele.select_radio_button(HG_EDIT_ELEMENT["Distribution_pattern_Simultaneous"])

            if params['No_answer_number_of_rings']!='':
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["No_answer_number_of_rings"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["No_answer_number_of_rings"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["No_answer_number_of_rings"], params["No_answer_number_of_rings"])

            if params['On_hours_schedule']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["On_hours_schedule"])
                self.action_ele.select_from_dropdown_using_text(HG_EDIT_ELEMENT["On_hours_schedule"], params["On_hours_schedule"])

            if params['Holiday_schedule']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                if params["Off_hours"]:
                    self.action_ele.explicit_wait("vcfe_Off_hours")
                    self.action_ele.clear_input_text("vcfe_Off_hours")
                    self.action_ele.input_text("vcfe_Off_hours", params["Off_hours"])
                else:
                    raise AssertionError("Group member should be provided")
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Holiday_schedule"])
                self.action_ele.select_from_dropdown_using_text(HG_EDIT_ELEMENT["Holiday_schedule"], params["Holiday_schedule"])

            if params['call_stack_full']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                if params["call_stack_full"]:
                    self.action_ele.explicit_wait(HG_EDIT_ELEMENT["call_stack_full"])
                    self.action_ele.clear_input_text(HG_EDIT_ELEMENT["call_stack_full"])
                    self.action_ele.input_text(HG_EDIT_ELEMENT["call_stack_full"], params["call_stack_full"])
                else:
                    raise AssertionError("Valid user extension should be provided")

            if params['no_answer']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                if params["no_answer"]:
                    self.action_ele.explicit_wait(HG_EDIT_ELEMENT["no_answer"])
                    self.action_ele.clear_input_text(HG_EDIT_ELEMENT["no_answer"])
                    self.action_ele.input_text(HG_EDIT_ELEMENT["no_answer"], params["no_answer"])
                else:
                    raise AssertionError("Valid user extension should be provided")

            if params['Off_hours_or_holiday_destination']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                if params["Off_hours_or_holiday_destination"]:
                    self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Off_hours_or_holiday_destination"])
                    self.action_ele.clear_input_text(HG_EDIT_ELEMENT["Off_hours_or_holiday_destination"])
                    self.action_ele.input_text(HG_EDIT_ELEMENT["Off_hours_or_holiday_destination"], params["Off_hours_or_holiday_destination"])
                else:
                    raise AssertionError("Valid user extension should be provided")

            if params['Include_in_System_Dial_by_Name_directory'] == "False":
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Include_in_System_Dial_by_Name_directory"])
                self.action_ele.unselect_checkbox(HG_EDIT_ELEMENT["Include_in_System_Dial_by_Name_directory"])

            if params['Make_extension_private']!= '':
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Make_extension_private"])
                self.action_ele.select_checkbox(HG_EDIT_ELEMENT["Make_extension_private"])

            if params['HGname'] == "Delete":
                self.action_ele.explicit_wait('vcfe_huntgrp_Name')
                self.action_ele.clear_input_text('vcfe_huntgrp_Name')

            if params['HGname'] != '' and params["HGname"] != "Delete":
                self.action_ele.explicit_wait('vcfe_huntgrp_Name')
                self.action_ele.clear_input_text('vcfe_huntgrp_Name')
                self.action_ele.input_text('vcfe_huntgrp_Name', params['HGname'])

            if params['HGExtn'] != '' and params["HGExtn"] != "Delete":
                self.action_ele.clear_input_text('vcfe_Huntgrp_Extn')
                self.action_ele.input_text('vcfe_Huntgrp_Extn', params['HGExtn'])

            if params["HGExtn"] == "Delete":
                self.action_ele.explicit_wait('vcfe_Huntgrp_Extn')
                self.action_ele.clear_input_text('vcfe_Huntgrp_Extn')

            if params['HGBckupExtn'] == "Delete":
                self.action_ele.explicit_wait('vcfe_Huntgrp_Bckup_Extn')
                self.action_ele.clear_input_text('vcfe_Huntgrp_Bckup_Extn')
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
                return

            if params['HGBckupExtn'] != '' and params['HGBckupExtn'] != "Delete":
                self.action_ele.explicit_wait('vcfe_Huntgrp_Bckup_Extn')
                self.action_ele.input_text('vcfe_Huntgrp_Bckup_Extn', params['HGBckupExtn'])
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element('Emergency_huntgroup_Finishbutton')

                time.sleep(3)
                if params["error_message"]:
                    if params["error_message"] in self._browser._browser.page_source:
                        print("Error message '" + params["error_message"] + "' is verified in page")
                        self.action_ele.click_element("fnMessageBox_OK")
                        return
                    else:
                        print("Error message is not verified in page")
                        return

            if params['hglocation'] == "Delete":
                self.action_ele.explicit_wait('vcfe_huntgroup_location')
                self.action_ele.select_from_dropdown_using_index('vcfe_huntgroup_location', 0)
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
                return

            if params["hg_phonenumber"] == "Delete":
                self.action_ele.click_element("vcfe_pphone_delete")

            if params["grp_member"] == "Delete":
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.explicit_wait("hg_group_member_delete")
                self.action_ele.click_element("hg_group_member_delete")
                self.action_ele.click_element("vcfe_HG_Back")

            if params["grp_member"] != '' and params["grp_member"] != "Delete":
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.input_text('vcfe_HG_Search', params['grp_member'])
                self.action_ele.click_element("vcfe_Select_Extn")
                self.action_ele.clear_input_text('vcfe_HG_Search')
                self.action_ele.click_element("vcfe_HG_Back")

            self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
            self.action_ele.click_element('Emergency_huntgroup_Finishbutton')
            time.sleep(4)
            errors = []
            errors = self._browser.elements_finder('vcfe_val_errors')
            if errors:
                for error in errors:
                    if "The extension is not available" in error.text:
                        print(self.query_ele.get_text("vcfe_val_errors"))
                        status = True
                        print(status)
                        return
            time.sleep(6)
            self.action_ele.explicit_wait("fnMessageBox_OK", ec="element_to_be_clickable")
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(4)
            self.action_ele.explicit_wait("VCFE_datagrid")

        except Exception, e:
            print(e)
            print("Editing hunt group failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_updated_hunt_group_value(self, params):
        """
        `Description:` Verify the given hunt group details

        `Param:`  params: Dictionary with Vcfe_variables

        `Returns:` status: True/False

        `Created by:` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            for i in range(4):
                try:
                    time.sleep(2)
                    elements = self._browser.elements_finder("pg_refresh_btn")
                    if elements[0].is_displayed():
                        pass
                    else:
                        self.action_ele.explicit_wait("pg_editor_panel", ec="element_to_be_clickable")
                        self.action_ele.click_element("pg_editor_panel")
                except:
                    print("Retrying click: %d" % i)
                    pass

            status = False
            if params['Rings_per_Member'] != '':
                value_from_text_box = self.query_ele.get_value_execute_javascript("document.getElementsByName('ringsPerMember')[0].value")
                print("Expected value: %s" %params["Rings_per_Member"])
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["Rings_per_Member"])
                status = True

            if params['No_answer_number_of_rings']!='':
                value_from_text_box = self.query_ele.get_value_execute_javascript("document.getElementsByName('noAnswerRings')[0].value")
                print("Expected value: %s" %params["No_answer_number_of_rings"])
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["No_answer_number_of_rings"])
                status = True

            if params['Call_member_when_forwarding_all_calls'] == "True":
                self.assert_ele.element_should_be_selected(HG_EDIT_ELEMENT["Call_member_when_forwarding_all_calls"])
                status = True

            #if params['Call_member_when_forwarding_all_calls'] == "False":
            #     self.assert_ele.element_should_not_be_selected(HG_EDIT_ELEMENT["Call_member_when_forwarding_all_calls"])
            #     time.sleep(3)
            #
            # #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['Skip_member_if_already_on_a_call'] == "True":
                self.assert_ele.element_should_be_selected(HG_EDIT_ELEMENT["Skip_member_if_already_on_a_call"])
                status = True

            if params['Distribution_pattern'] == "Simultaneous":
                self.assert_ele.element_should_be_selected(HG_EDIT_ELEMENT["Distribution_pattern_Simultaneous"])
                status = True

            if params['On_hours_schedule']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                try:
                    text_list = self._browser.elements_finder("vcfe_onHour_option")
                    for txt in text_list:
                        if txt.text == params["On_hours_schedule"]:
                            status = True
                            print("On hours schedule is present in list")
                            break
                    if status == False:
                        print("On hours schedule is not present in list")
                except:
                    raise AssertionError("Could not find On hours schedule")

            if params['Holiday_schedule']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                try:
                    text_list = self._browser.elements_finder("vcfe_holidaySchedule_option")

                    for txt in text_list:
                        if txt.text == params["Holiday_schedule"]:
                            status = True
                            print("Holiday schedule is present in list")
                            break
                    if status == False:
                        print("Holiday schedule is not present in list")
                except:
                    raise AssertionError("Could not find Holiday schedule")

            if params['call_stack_full']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                ele_obj = self.query_ele.get_value_execute_javascript("document.getElementsByClassName('floatRightAttr ng-pristine ng-untouched ng-valid')[0]")
                value_from_text_box=ele_obj.get_attribute('value')
                expected_val = params["call_stack_full"] + " : " + params["user_name"]
                print("Expected value is : %s"%expected_val )
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, expected_val)
                status = True

            if params['no_answer']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                ele_obj = self.query_ele.get_value_execute_javascript("document.getElementsByClassName('floatRightAttr ng-pristine ng-untouched ng-valid')[1]")
                value_from_text_box=ele_obj.get_attribute('value')
                expected_val = params["no_answer"]+" : "+params["user_name"]
                print("Expected value is : %s"%expected_val )
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, expected_val)
                status = True

            if params['Off_hours_or_holiday_destination']!='':
                self.action_ele.explicit_wait("vcfe_Call_Forward_Settings")
                self.action_ele.click_element('vcfe_Call_Forward_Settings')
                ele_obj = self.query_ele.get_value_execute_javascript("document.getElementsByClassName('floatRightAttr ng-pristine ng-untouched ng-valid')[2]")
                value_from_text_box=ele_obj.get_attribute('value')
                expected_val = params["Off_hours_or_holiday_destination"]+" : "+params["user_name"]
                print("Expected value is : %s"%expected_val )
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, expected_val)
                status = True

            if params['Include_in_System_Dial_by_Name_directory'] == "False":
                self.assert_ele.element_should_not_be_selected(HG_EDIT_ELEMENT["Include_in_System_Dial_by_Name_directory"])
                status = True

            if params['Make_extension_private']!= '':
                self.assert_ele.element_should_be_selected(HG_EDIT_ELEMENT["Make_extension_private"])
                status = True

            if params['HGname']!= '':
                value_from_text_box = self.query_ele.get_value("vcfe_huntgrp_Name")
                print("Expected value: %s" % params["HGname"])
                print("Actual value from textbox is: %s" % value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["HGname"])
                status = True

            if params["grp_member"] == "Delete":
                self.action_ele.explicit_wait("vcfe_edit")
                self.action_ele.click_element("vcfe_edit")
                self.assert_ele.element_should_not_be_displayed("hg_group_member")
                self.action_ele.explicit_wait("vcfe_HG_Back")
                self.action_ele.click_element("vcfe_HG_Back")
                status = True

            if params["grp_member"] !='' and params["grp_member"] != "Delete":
                time.sleep(1)
                self.action_ele.explicit_wait("vcfe_edit", ec="element_to_be_clickable")
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.explicit_wait("hg_group_member", ec="element_to_be_clickable")
                value_from_text_box = self.query_ele.get_text("hg_group_member")
                print("Expected value: %s" % params["grp_member"])
                print("Actual value from textbox is: %s" % value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["grp_member"])
                self.action_ele.explicit_wait("vcfe_HG_Back", ec="element_to_be_clickable")
                self.action_ele.click_element("vcfe_HG_Back")
                status = True

            if params["hg_phonenumber"] == "Delete":
                phonenum = self.query_ele.get_text_of_selected_dropdown_option('vcfe_selPhoneNumber')
                if phonenum=="Select...":
                    print("Phone number is not displayed as expected")
                    status = True
                else:
                    print("The phone number should not be visible, but it is.")

            self.action_ele.explicit_wait("vcfe_cancel_button", ec="element_to_be_clickable")
            self.action_ele.click_element("vcfe_cancel_button")
            self.action_ele.explicit_wait("vcfe_extension_textbox", ec="visibility_of_element_located")

        except AssertionError as assert_err:
            print("ASSERTION ERROR: %s" %assert_err.message)
            status = False

        except Exception,e:
            print(e)
            print("Verifying hunt group failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            status = False

        finally:
            return status

    def create_holiday_schedule(self, params):
        """
        `Description:` Create holiday schedule and return name and date of the holiday schedule

        `Param:`  params: Dictionary contains HolidayScheduleInfo - Vcfe_variables

        `Returns:` name and date of the holiday schedule

        `Created by:` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_add_dropdown")
            self.action_ele.click_element("hs_add_holidays_schedule")
            time.sleep(3)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            if params['scheduleName'] == '':
                self.action_ele.explicit_wait("hs_name")
                self.action_ele.clear_input_text("hs_name")
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                if params["error_message"]:
                    name = params["scheduleName"]
                    date = params["date"]
                    return name, date
            if params['scheduleName'] != '':
                self.action_ele.input_text('hs_name', params['scheduleName'])
            if params['timeZone'] != '':
                self.action_ele.select_from_dropdown_using_text("hs_selScheduleTimezone", params["timeZone"])
            if params['holidayName'] != '':
                self.action_ele.click_element("hs_add_button")
                self.action_ele.input_text('hs_holidayScheduleItemName', params['holidayName'])
                self.action_ele.input_text('hs_holidayScheduleDatepicker', params['date'])
            self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(3)
            self.action_ele.explicit_wait("fnMessageBox_OK", ec="element_to_be_clickable")
            name = params["scheduleName"]
            date = params["date"]
            if params["error_message"]:
                return name, date
            self.action_ele.click_element("fnMessageBox_OK")
            self.action_ele.explicit_wait("VCFE_entry_search", ec="element_to_be_clickable")
            return name, date
        except Exception, e:
            print(e)
            print("Holiday schedule creation failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError

    def edit_holiday_schedule(self, params):
        """
        `Description:` Edit holiday schedule details

        `Param:`  params: Dictionary contains HolidayScheduleInfo - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")

            for i in range(4):
                try:
                    time.sleep(2)
                    elements = self._browser.elements_finder("pg_refresh_btn")
                    if elements[0].is_displayed():
                        pass
                    else:
                        self.action_ele.explicit_wait("pg_editor_panel", ec="element_to_be_clickable")
                        self.action_ele.click_element("pg_editor_panel")
                except:
                    print("Retrying click: %d" % i)
                    pass

            if params['scheduleName'] == 'Remove':
                self.action_ele.explicit_wait("hs_name")
                self.action_ele.clear_input_text("hs_name")
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(2)
                if params["error_message"]:
                    status = True
                    return status
            if params['Holidays']== 'Delete':
                self.action_ele.explicit_wait("hs_removebutton")
                self.action_ele.click_element("hs_removebutton")

            if params['scheduleName']!='' and params['scheduleName']!='Remove':
                self.action_ele.explicit_wait("hs_name")
                self.action_ele.clear_input_text("hs_name")
                self.action_ele.input_text("hs_name", params["scheduleName"])
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(3)
                if params["error_message"]:
                    if params["error_message"] in self._browser._browser.page_source:
                        print("Error message '"+ params["error_message"] +"' is verified in page" )
                        self.action_ele.click_element("fnMessageBox_OK")
                        return True
                    else:
                        print("Error message is not verified in page")
                        return False

            if params['Holidays']== 'Yearly':
                self.action_ele.explicit_wait("hs_yearly_checkbox")
                self.action_ele.select_checkbox("hs_yearly_checkbox")

            if params['timeZone'] != '':
                self.action_ele.explicit_wait("hs_selScheduleTimezone")
                self.action_ele.select_from_dropdown_using_text("hs_selScheduleTimezone", params["timeZone"])

            if params['holidayName']!='':
                self.action_ele.explicit_wait("hs_holidayScheduleItemName")
                self.action_ele.clear_input_text("hs_holidayScheduleItemName")
                self.action_ele.input_text("hs_holidayScheduleItemName", params["holidayName"])

            if params['date']!='':
                self.action_ele.explicit_wait("hs_holidayScheduleDatepicker")
                self.action_ele.clear_input_text("hs_holidayScheduleDatepicker")
                self.action_ele.input_text("hs_holidayScheduleDatepicker", params["date"])

            if params["error_message"]:
                self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
                self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                time.sleep(2)
                status = True
                return True

            self.action_ele.explicit_wait("Emergency_huntgroup_Finishbutton", ec="element_to_be_clickable")
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(2)
            #self.action_ele.explicit_wait("fnMessageBox_OK", ec="element_to_be_clickable")
            self.action_ele.click_element("fnMessageBox_OK")
            self.action_ele.explicit_wait("VCFE_entry_search", ec="element_to_be_clickable")
            status = True

        except Exception,e:
            print(e)
            print("Failed to edit holiday schedule")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_holidays_schedule(self, params):
        """
        `Description:` Verify holiday schedule details

        `Param:`  params: Dictionary contains HolidayScheduleInfo - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            for i in range(4):
                try:
                    time.sleep(2)
                    elements = self._browser.elements_finder("pg_refresh_btn")
                    if elements[0].is_displayed():
                        pass
                    else:
                        self.action_ele.explicit_wait("pg_editor_panel", ec="element_to_be_clickable")
                        self.action_ele.click_element("pg_editor_panel")
                except:
                    print("Retrying click: %d" % i)
                    pass
            status = False
            if params["scheduleName"]!='':
                expected_schedule_name = params["scheduleName"]
                self.action_ele.explicit_wait("hs_name")
                actual_schedule_name = self.query_ele.get_value("hs_name")
                print("Expected schedule name : %s" %expected_schedule_name)
                print("Actual schedule name from textbox : %s" %actual_schedule_name)
                self.assert_ele.values_should_be_equal(expected_schedule_name, actual_schedule_name)
                status = True

            if params['Holidays'] == 'Delete':
                self.assert_ele.element_should_not_be_displayed("hs_removebutton")
                status = True

            if params['Holidays'] == 'Yearly':
                self.action_ele.explicit_wait("hs_yearly_checkbox")
                self.assert_ele.element_should_be_selected("hs_yearly_checkbox")
                status = True

            if params['holidayName']!='':
                expected_name = params["holidayName"]
                self.action_ele.explicit_wait("hs_holidayScheduleItemName")
                actual_name = self.query_ele.get_value("hs_holidayScheduleItemName")
                print("Expected name : %s" % expected_name)
                print("Actual name from textbox : %s" % actual_name)
                self.assert_ele.values_should_be_equal(expected_name, actual_name)
                status = True

            if params["date"]!='':
                expected_date = params["date"]
                self.action_ele.explicit_wait("hs_holidayScheduleDatepicker")
                actual_date = self.query_ele.get_value("hs_holidayScheduleDatepicker")
                print("Expected date : %s" %expected_date)
                print("Actual date from textbox : %s" %actual_date)
                self.assert_ele.values_should_be_equal(expected_date, actual_date)
                status = True

            if params["timeZone"]!='':
                self.action_ele.explicit_wait("hs_selScheduleTimezone_options")
                self.assert_ele.verify_text_in_dropdown("hs_selScheduleTimezone_options", params["timeZone"])
                status = True

            self.action_ele.explicit_wait("vcfe_cancel_button", ec="element_to_be_clickable")
            self.action_ele.click_element("vcfe_cancel_button")
            self.action_ele.explicit_wait("VCFE_entry_search", ec="visibility_of_element_located")

        except AssertionError as assert_err:
            print("ASSERTION ERROR: %s" % assert_err.message)
            status = False

        except Exception, e:
            print(e)
            print("Verifying holidays schedule failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            status = False

        finally:
            return status


    def edit_on_hours_schedule(self, params):
        """
            `Description:` Edit On Hours  schedule

            `:param params: Dictionary contains	Info for Editing On Hours Schedule like schedule name and timezone

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
        """
        error1 = "Failed updating component. Error: ScheduleName - has already been taken"
        error2 = "Failed updating component. Error: schedule_items.stop_time - Stop time should be different from (later than) Start time"
        try:
            params = defaultdict(lambda: '', params)
            message1 = 'Component was updated successfully'
            status = False
            time.sleep(1)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            time.sleep(2)
            # self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['scheduleName']:
                if params['scheduleName'] == "Remove":
                    self.action_ele.clear_input_text("ohs_name")
                    time.sleep(1)
                    self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                    name_error=self._browser.element_finder('vcfe_val_error')
                    if "This field is required" in name_error.text:
                        self.action_ele.click_element("vcfe_cancel_button")
                        self.action_ele.explicit_wait("VCFE_delete_yes")
                        time.sleep(1)
                        self.action_ele.click_element("VCFE_delete_yes")
                        return True
                else:
                    self.action_ele.clear_input_text("ohs_name")
                    self.action_ele.input_text("ohs_name", params['scheduleName'])
                    time.sleep(1)
            if params['timezone']:
                self.action_ele.select_from_dropdown_using_text("vcfe_selScheduleTimezone", params['timezone'])
                time.sleep(2)
            if params['timePeriod'] == "change":
                time.sleep(1)
                self.action_ele.clear_input_text("ohs_first_start_time")
                self.action_ele.input_text("ohs_first_start_time", params['StartTime'])
                time.sleep(2)
                self.action_ele.clear_input_text("ohs_first_stop_time")
                self.action_ele.input_text("ohs_first_stop_time", params['StopTime'])
                time.sleep(2)
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(3)
            self.action_ele.explicit_wait("fnMessageBox_OK")
            if message1 in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.click_element("fnMessageBox_OK")
                status = True
            if error1 or error2 in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.click_element("fnMessageBox_OK")
                time.sleep(1)
                self.action_ele.click_element("vcfe_cancel_button")
                time.sleep(2)
                self.action_ele.explicit_wait("VCFE_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("VCFE_delete_yes")
                status = True

        except:
            print("On-Hours schedule creation failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_in_interactive_diagram(self, params):
        """
            `Description:` Verify on interactive diagram after pressing refresh button. VCFE component creation or
                            updating should reflect on interactive diagram

            `:param params: Dictionary contains	Info for Regarding Schedule to be verified in interactive diagram

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status1 = False
            self.action_ele.click_element("pg_refresh_btn")
            time.sleep(2)
            interactive_grid = self._browser.element_finder("vcfe_interactive_grid")
            if interactive_grid.is_displayed():
                schedule_name1 = self._browser.element_finder("vcfe_updated_component")
                if schedule_name1.is_displayed():
                    schedule_name2 = self.query_ele.get_text("vcfe_interactive_display")
                    time.sleep(1)
                    schedule_name = schedule_name2[:13]
                    if schedule_name in params["Assign_vcfe_Name"]:
                        status1 = True
            else:
                print "VCFE Interactive Grid is not displayed Properly"

        except:
            print("Verification on interactive diagram failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status1

    def vcfe_adjust_timeout(self, params):
        """
            `Description:` This helps to validate error messages for Adjust timeout. Timeout limit(0-30000)

            `:param params: Adjust timeout values for verifying error messages

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        status = False
        val_msg1 = "Failed updating component. Error: sub_menus.Timeout - must be greater than or equal to 0 sub_menus_attributes -"
        val_msg2 = "Failed updating component. Error: sub_menus.Timeout - is not a number sub_menus_attributes"
        val_msg3 = "Failed updating component. Error: sub_menus.Timeout - must be less than or equal to 30000 sub_menus_attributes"
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            time.sleep(1)
            for x in params['Adjust_Timeout']:
                if x.isdigit() and 0 <= int(x) <= 30000:
                    self.action_ele.clear_input_text("vcfe_adjust_timeout")
                    self.action_ele.input_text("vcfe_adjust_timeout", x)
                    status = True
                    break
                else:
                    self.action_ele.clear_input_text('vcfe_adjust_timeout')
                    time.sleep(1)
                    self.action_ele.input_text('vcfe_adjust_timeout', x)
                    time.sleep(1)
                    self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
                    self.action_ele.explicit_wait("fnMessageBox_OK")
                    if val_msg1 or val_msg2 or val_msg3 in self.query_ele.get_text("Aa_edit_confirm"):
                        time.sleep(1)
                        self.action_ele.click_element("fnMessageBox_OK")

        except:
            print("Adjust Timeout Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_error_and_click_cancel(self, message):
        """
            `Description:` Verify the error pop-up and click ok and then click cancel button to cancel VCFE component

            `:param message:` Message to be validated on error Pop-Up

            `return:` Status- True or False

            `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status1 = False
            if message in self.query_ele.get_text("Aa_edit_confirm"):
                self.action_ele.click_element("fnMessageBox_OK")
                status1 = True
                time.sleep(1)
            self.action_ele.click_element("pgg_cancel_button")
            self.action_ele.explicit_wait("VCFE_delete_yes")
            time.sleep(1)
            self.action_ele.click_element("VCFE_delete_yes")
            time.sleep(2)
        except:
            print("There is no such error message")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status1

    def edit_emergency_hunt_group(self, params):
        """
        `Description:` Edit emergency hunt group with different inputs

        `Param:`  params: Dictionary contains emergency hunt group info - Vcfe_variables

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            time.sleep(2)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)

            if params['Distribution_pattern'] == "Top_down":
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element("Emr_hg_show_more_operations")
                time.sleep(2)
                self.action_ele.explicit_wait("vcfe_hg_top_down")
                self.action_ele.select_radio_button("vcfe_hg_top_down")
                time.sleep(3)

            if params['no_answer']!='':
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element('Emr_hg_show_more_operations')
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["no_answer"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["no_answer"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["no_answer"], params["no_answer"])
                time.sleep(3)

            if params['No_answer_number_of_rings']!='':
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element("Emr_hg_show_more_operations")
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["No_answer_number_of_rings"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["No_answer_number_of_rings"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["No_answer_number_of_rings"], params["No_answer_number_of_rings"])
                time.sleep(3)

            if params['Rings_per_Member']!='':
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element("Emr_hg_show_more_operations")
                self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Rings_per_Member"])
                self.action_ele.clear_input_text(HG_EDIT_ELEMENT["Rings_per_Member"])
                self.action_ele.input_text(HG_EDIT_ELEMENT["Rings_per_Member"], params["Rings_per_Member"])
                time.sleep(3)

            if params["grp_member"] != '' and params["grp_member"] != "Remove":
                self.action_ele.explicit_wait("vcfe_edit")
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.input_text('vcfe_HG_Search', params['grp_member'])
                self.action_ele.click_element("vcfe_Select_Extn")
                self.action_ele.clear_input_text('vcfe_HG_Search')
                self.action_ele.click_element("vcfe_HG_Back")
                time.sleep(3)

            if params["grp_member"] == "Remove":
                self.action_ele.explicit_wait("vcfe_edit")
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.explicit_wait("hg_group_member_delete")
                self.action_ele.click_element("hg_group_member_delete")
                self.action_ele.click_element("vcfe_HG_Back")
                time.sleep(3)

            if params["show_more_operations"] == "True":
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element("Emr_hg_show_more_operations")
            # if params['Distribution_pattern'] == "Simultaneous":
            #     #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            #     self.action_ele.explicit_wait(HG_EDIT_ELEMENT["Distribution_pattern_Simultaneous"])
            #     self.action_ele.select_radio_button(HG_EDIT_ELEMENT["Distribution_pattern_Simultaneous"])
            #     time.sleep(3)

            time.sleep(2)
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("Emergency_huntgroup_Finishbutton")
            time.sleep(3)
            self.action_ele.explicit_wait("fnMessageBox_OK")
            self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(3)
        except Exception,e:
            print(e)
            print("Editing hunt group failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_emergency_hunt_group(self, params):
        """
        `Description:` Verify all given emergency hunt group fields

        `Param:`  params: Dictionary contains emergency hunt group info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("vcfe_vcfComponentsGrideditButton")
            time.sleep(2)
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(2)
            status = False

            if params['Distribution_pattern'] == "Top_down":
                self.action_ele.click_element("Emr_hg_show_more_operations")
                self.assert_ele.element_should_be_selected("vcfe_hg_top_down")
                status = True
                time.sleep(3)

            if params['no_answer']!='':
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element('Emr_hg_show_more_operations')
                ele_obj = self.query_ele.get_value_execute_javascript("document.getElementsByName('answer')[0]")
                value_from_text_box=ele_obj.get_attribute('value')
                expected_val = params["no_answer"] + " : " + params["user_name"]
                print("Expected value is : %s"%expected_val )
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, expected_val)
                status = True
                time.sleep(3)

            if params['No_answer_number_of_rings']!='':
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element('Emr_hg_show_more_operations')
                value_from_text_box = self.query_ele.get_value_execute_javascript("document.getElementsByClassName('ng-pristine ng-untouched ng-valid')[5].value")
                print("Expected value: %s" %params["No_answer_number_of_rings"])
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["No_answer_number_of_rings"])
                status = True
                time.sleep(3)

            if params['Rings_per_Member'] != '':
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element('Emr_hg_show_more_operations')
                value_from_text_box = self.query_ele.get_value_execute_javascript("document.getElementsByClassName('ng-pristine ng-untouched ng-valid')[4].value")
                print("Expected value: %s" %params["Rings_per_Member"])
                print("Actual value from textbox is: %s" %value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["Rings_per_Member"])
                status = True
                time.sleep(3)

            if params["grp_member"] == "Remove":
                self.action_ele.click_element("vcfe_edit")
                self.assert_ele.element_should_not_be_displayed("hg_group_member")
                self.action_ele.click_element("vcfe_HG_Back")
                status = True
                time.sleep(3)

            if params["grp_member"] !='' and params["grp_member"] != "Remove":
                self.action_ele.click_element("vcfe_edit")
                self.action_ele.explicit_wait("hg_group_member")
                value_from_text_box = self.query_ele.get_text("hg_group_member")
                print("Expected value: %s" % params["grp_member"])
                print("Actual value from textbox is: %s" % value_from_text_box)
                self.assert_ele.values_should_be_equal(value_from_text_box, params["grp_member"])
                self.action_ele.click_element("vcfe_HG_Back")
                status = True
                time.sleep(3)

            if params["show_more_operations"] == "True":
                self.action_ele.explicit_wait("Emr_hg_show_more_operations")
                self.action_ele.click_element("Emr_hg_show_more_operations")
                elements = self._browser.elements_finder("Emr_hg_show_fewer_operations")
                if elements[0].is_displayed():
                    status = True
                    time.sleep(3)
                else:
                    status = False
                    time.sleep(1)

            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.action_ele.explicit_wait("vcfe_cancel_button")
            self.action_ele.click_element("vcfe_cancel_button")

        except AssertionError as assert_err:
            print("ASSERTION ERROR: %s" %assert_err.message)
            status = False

        except Exception,e:
            print(e)
            print("Verifying hunt group failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            status = False

        finally:
            return status

    def go_to_vcfe_page(self, params):
        """
            `Description:` This function will help to go and land in a given vcfe page

            `Param:`  params: page name

            `Created by:` Immani Mahesh kumar
        """
        try:
            self.action_ele.click_element("Emergency_add_dropdown")
            # This function can be expanded to all vcfe pages
            if params.lower() == 'emergency_hunt_group':
                self.action_ele.click_element("Emergency_huntgroup")
            elements = self._browser.elements_finder("pg_refresh_btn")
            if elements[0].is_displayed():
                pass
            else:
                time.sleep(1)
                self.action_ele.click_element("pg_editor_panel")
            time.sleep(1)

        except:
            print("switching to vcfe page failed", self.go_to_vcfe_page.__doc__)

    def verify_emergency_hg_up_down_button(self, params):
        """
            `Description:`This helps to validate the functioning of the up down button in the emergency hunt group

            `Param:`  params: Dictionary contains emergency hunt group info - Vcfe_variables

            `Returns:` status - True/False

            `Created by:` Immani Mahesh Kumar
        """
        try:
            status = False
            self.action_ele.explicit_wait("vcfe_edit")
            self.action_ele.click_element("vcfe_edit")
            move_up_btn = self._browser.elements_finder('Emergency_hg_Move_up')
            move_down_btn = self._browser.elements_finder('Emergency_hg_Move_down')
            extn_list = self._browser.elements_finder('Emergency_hg_member_list')
            pre_list = []
            for x in range(2):
                pre_list.append(extn_list[x].text)

            if params['verify_up_down_button'] == 'up':
                move_up_btn[1].click()
            if params['verify_up_down_button'] == 'down':
                move_down_btn[0].click()
            extn_list1 = self._browser.elements_finder('Emergency_hg_member_list')
            updated_list = []
            for y in range(2):
                updated_list.append(extn_list1[y].text)
            if pre_list != updated_list:
                status = True
            else:
                pass
        except:
            print("Up-Down button in emergency hunt group verification failed", self.go_to_vcfe_page.__doc__)
        return status


    def assign_ph_number_to_vcfe_component(self, param):
        """
        `Description:` Assign any available phone number to any vcfe component on 'Phone System--> Phone Numbers' page

        `Param:` Type of destination. Eg; Auto Attendant, Hunt Group

        `Returns:` status - True / False

        `Created by:` Vasuja
        """
        # Assumption is that the control is already in Phone System--> Phone Numbers page

        status = True

        try:

            self.wait("Ph_System_Ph_Number_Assign")
            self.action_ele.click_element("Ph_System_Ph_Number_Assign")
            time.sleep(1)

            if param["auto_Attendant"]:
                # change the destination type to Auto Attendant
                self.wait("Ph_System_Ph_Number_Op_Dest_Type_AutoAttendant")
                self.action_ele.click_element("Ph_System_Ph_Number_Op_Dest_Type_AutoAttendant")
                time.sleep(1)
                self.wait("Ph_System_Ph_Number_Op_Destination")
                self.action_ele.select_from_dropdown_using_text("Ph_System_Ph_Number_Op_Destination", param['auto_Attendant'])

            elif param["hunt_Group"]:
                # change the destination type to Hunt Group
                self.wait("Ph_System_Ph_Number_Op_Dest_Type_HuntGroup")
                self.action_ele.click_element("Ph_System_Ph_Number_Op_Dest_Type_HuntGroup")
                time.sleep(1)
                self.wait("Ph_System_Ph_Number_Op_Destination")
                self.action_ele.select_from_dropdown_using_text("Ph_System_Ph_Number_Op_Destination", param['hunt_Group'])


            # Save the changes
            self.wait("Ph_System_Ph_Number_Op_Save_Button")
            self.action_ele.click_element("Ph_System_Ph_Number_Op_Save_Button")
            time.sleep(3)
            self.wait("BCA_OK_Button")

            if "The phone number was assigned successfully" in self._browser._browser.page_source:
                print("Message 'The phone number was assigned successfully' is displayed")
            else:
                raise BossExceptionHandle("message on page not as required!")
            # Click on OK button
            time.sleep(3)
            self.action_ele.click_element("BCA_OK_Button")

        except (Exception, BossExceptionHandle) as err:
            status = False
            print("Could not assign phone number to vcfe component")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return status

        # End of function "assign_ph_number_to_vcfe_component"
    def vcfe_default_AA(self, params):
        """
        `Description:`

        `Param:` Type of destination. Eg; Auto Attendant, Hunt Group

        `Returns:` status - True / False

        `Created by:` Diksha Singh
        """
        #import pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()

        try:
            status = False
            time.sleep(1)
            self.action_ele.clear_input_text("pg_extension_head")
            self.action_ele.clear_input_text("VCFE_entry_search")
            self.action_ele.input_text("VCFE_entry_search", params)
            time.sleep(1)
            extn=self.query_ele.get_text('vcfe_default_AA')
            #fields=self._browser.elements_finder('vcfe_default_AA')
            #extn=fields[2].text
            return extn
        except:
            print("Failed to update phone info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
