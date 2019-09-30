import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict
import inspect
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

from CommonFunctionality import CommonFunctionality

__author__ = "Rahul Doshi"




class AddPartition(object):
    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.commonfunctionality = CommonFunctionality(self._browser)

    def add_partition(self, partition_data):
        '''
        `Description:` Add primary partition

        `Param:` partition_data: Dictionary contains partition information

        `Returns:` None

        `Created by:` rdoshi
        '''
        try:
            self.action_ele.click_element('partitionsGridAddButton')
            partition_data = defaultdict(lambda: '', partition_data)
            self.action_ele.explicit_wait('tbPartitionName')
            self.action_ele.input_text("tbPartitionName", partition_data["partitionName"])
            self.action_ele.select_from_dropdown_using_text("ddlClusters",partition_data["clusterName"])
            if(partition_data["add_sites"]=='True'):
                self.action_ele.select_checkbox("cbAddSites")
            else:
                self.action_ele.unselect_checkbox("cbAddSites")
            self.action_ele.click_element('addPartitionForm_OK')
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if self._browser.location == "australia":
                self.action_ele.explicit_wait('Par_localAreaCode')
                self.action_ele.input_text('Par_localAreaCode', partition_data["localAreaCode"])
                self.action_ele.click_element('setLocalAreaCodesForm_OK')
            if self._browser.location == "uk":
                self.action_ele.explicit_wait('Par_localAreaCode')
                self.action_ele.input_text('Par_localAreaCode', partition_data["localAreaCode"])
                self.action_ele.click_element('setLocalAreaCodesForm_OK')
            self.action_ele.explicit_wait('setting_tab_checkbox')
        except Exception,e:
            print(e)
            print("Add Partition Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_partition(self, partitionName):
        """
        `Description:` Verify the partition is created

        `Param:` partitionName:partitionName: to verify

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        #self.commonfunctionality.switch_link_in_operations("Primary Partition")
        try:
            time.sleep(1)
            self.action_ele.input_text("primary_partition_header",partitionName)
            grid_elements = self._browser.elements_finder("name_grid")
            if grid_elements[0].text == partitionName:
                grid_elements[0].click()
                return True
            else:
                return False
        except Exception,e:
            print(e)
            print("Add Partition Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def edit_enabled_digit_from_dial_plan(self,type):
        """
        `Description:` Edit enabled digit from dial plan

        `Param:` type of dial plan

        `Returns:` Dictionary containing edited values and status of operation

        `Created by:` Palla Surya Kumar
        """
        try:
            message="Tenant Dial Plan updated successfully."
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status=False
            #taking xpaths list in to diffferent variables
            dial_plan_values = self._browser.elements_finder("dialplanoperations")
            dial_plan_digits = self._browser.elements_finder("dialplandigits")
            dic = {}
            #traversing for enabled element and storing them in dictionary
            for i in range(len(dial_plan_values)):
                if dial_plan_values[i].is_enabled():
                    options=dial_plan_values[i].find_elements_by_tag_name('option')
                    # traversing for spaecific type of element which has come from the input
                    for value in range(len(options)):
                        if options[value].text == type:
                            options[value].click()
                            print("The type is selected sucesfully.")
                            break #if required type is found
                    else:
                        self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                        raise Exception("The type of dial plan is not selected .")
                    break #if enabled element is found
            else:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                raise Exception("There is no enabled dial plan in this page.")
            dic['dial plan digit'] =dial_plan_digits[i].text
            if type=='Trunk Access Codes (1 Digit)':
                dic['dial plan value'] ='Trunk Access Codes 1 Digit'
            else:
                dic['dial plan value']=type
            self.action_ele.explicit_wait('dial_plan_save_button')
            self.action_ele.click_element('dial_plan_save_button')
            self.action_ele.explicit_wait('fnMessageBox_OK')
            if message in self.query_ele.get_text("Aa_edit_confirm"):
                status = True
                self.action_ele.click_element('fnMessageBox_OK')
            return  dic,status
        except Exception, e:
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            print(e)
            print("Editing enabled digit from dial plan failed")

    def verify_edited_dial_plan_from_phone_system_page(self,params):
        '''
        `Description:` This function will verify edited dial plan from phone system page.

        `Param:` Dictionary containing edited values

        `Returns:` status of operation

        `Created by:` Palla Surya Kumar
        '''
        try:
            # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status=False
            #taking xpaths list in to diffferent variables
            phone_system_dial_plan_values = self._browser.elements_finder("phone_system_dialplanoperations")
            phone_system_dial_plan_digits = self._browser.elements_finder("phone_system_dialplandigits")
            #traversing and verifying values from dictionary
            for i in range(len(phone_system_dial_plan_values)):
                if phone_system_dial_plan_values[i].text==params['dial plan value']\
                    and phone_system_dial_plan_digits[i].text==params['dial plan digit']:
                    status=True
                    break
            return status
        except Exception, e:
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            print(e)
            print("Verification of enabled digit from phone system dial plan failed")

    def verify_created_components_in_profile_tab(self, params):
        '''
        `Description:` Verify whether any created components (VCFE/BCA/Users), that is present in profiles tab or not .

        `Param:` : Component name

        `Returns: ` result - True/False

        `Created by:` Vasuja
        '''
        try:
            status=False
            self.action_ele.explicit_wait('PrimaryPartitionFirstName')
            self.action_ele.clear_input_text('PrimaryPartitionFirstName')
            self.action_ele.input_text('PrimaryPartitionFirstName',params['component_name'])
            if self.assert_ele._is_text_present(params['component_name']):
                time.sleep(1)
                print("Component is found: %s" % params['component_name'])
                status = True
            else:
                status = False
                print("Component is not present in profile tab or it is deleted")
        except Exception, e:
            print e
            print("Could not verify created components from profiles page!!")
        return status