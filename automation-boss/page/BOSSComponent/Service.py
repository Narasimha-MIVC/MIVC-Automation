"""Module for execution of Service Page functionalities
   File: Service.py
   Author: Megha Bansal
"""

import os
import sys
import pdb
import time
import imaplib
import time, re
import email
import datetime
from time import gmtime, strftime
from collections import defaultdict
import inspect
from lib import wait_in_loop as wil
from lib import select_from_dropdown as SFD
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# For console logs while executing ROBOT scripts
from robot.api.logger import console

# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
# import base
import web_wrappers.selenium_wrappers as base

from log import log
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

__author__ = ""

_RETRY_COUNT = 3

class Service(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 25

    def verify_provisioning_details(self, params):
        """
        `Description:` This Function will verify provisioning details of selected service

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        params = defaultdict(lambda: '', params)
        # self.action_ele.explicit_wait("datagrid_servicesExplorerDataGrid")
        wil(self.action_ele.explicit_wait, "datagrid_servicesExplorerDataGrid", loop_count=40)
        if params['servicename']:
            self.action_ele.clear_input_text("headerRow_ServiceName")
            self.action_ele.input_text("headerRow_ServiceName", params['servicename'])
        if params['servicestatus']:
            # self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", params['servicestatus'])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                "headerRow_ServiceStatus", params['servicestatus'])

        serviceTnName = self.query_ele.get_text("ServiceGrid_Tn")
        self.action_ele.click_element("ServiceGrid_ServiceId_Link")
        # self.action_ele.explicit_wait("ServiceDetails_Tabs")
        wil(self.action_ele.explicit_wait, "ServiceDetails_Tabs")

        serviceTn = serviceTnName.split(',', 1)[0]
        isProvisioningDetailsPresent = self.query_ele.text_present("Provisioning Details")

        if params['servicename'].lower() == "global user tn service":
            isPhoneNumberPresent = self.query_ele.text_present("Phone Number")
            isTurnupPresent = self.query_ele.text_present("TN Port or Turnup Service")
            if isProvisioningDetailsPresent and isPhoneNumberPresent and isTurnupPresent:
                return True
            else:
                return False

        elif params['servicename'].lower() == "global user service":
            isUserPresent = self.query_ele.text_present("User")
            isTnPresent = self.query_ele.text_present(serviceTn)
            if isProvisioningDetailsPresent and isUserPresent and isTnPresent:
                return True
            else:
                return False
        else:
            return False


    def close_service(self, params):
        """
        `Description:` This Test case will close the Service from the services page

        `Param:` params: Dictionary contains global user service information

        `:return:` True/False

        `Created by:` Megha Bansal
        `Modified by:` Prasanna
        """
        params = defaultdict(lambda: '', params)
        self.action_ele.explicit_wait('ServiceGrid_Checkbox')
        self.action_ele.click_element("headerRow_ServiceName")
        self.action_ele.input_text("headerRow_ServiceName", params['serviceName'])
        time.sleep(1)
        # self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", params['serviceStatus'])
        SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
            "headerRow_ServiceStatus", params['serviceStatus'])

        time.sleep(1)
        # Additional filter "Parent" field
        if params.get("parent", None):
            for c in ['(', ')', ' ', '-', '+']:
                params["parent"] = params["parent"].replace(c, "")
            self.action_ele.input_text("headerRow_BaseNameStripped", params["parent"])
            self.action_ele.explicit_wait("select_all_check_box")
            wil(self.action_ele.click_element, "select_all_check_box")
            wil(self.action_ele.clear_input_text, "headerRow_BaseNameStripped")

        ####
        # serviceId = self.query_ele.get_text('ServiceGrid_ServiceId_Link')
        # self.action_ele.click_element('ServiceGrid_Checkbox')
        ####

        # Retrieve the first row from the grid table. In this case only one
        else:
            self.action_ele.explicit_wait("ServiceGrid_DataGrid")
            # Prasanna: Modified
            data_grid = wil(self._browser.element_finder, "ServiceGrid_DataGrid", return_value=True)
            if not data_grid:
                return True
            # Get the first row
            try:
                row = data_grid.find_element_by_tag_name('div')
                if row:
                    # get the fields of the row
                    fields = row.find_elements_by_tag_name('div')
                    if fields:
                        # Click on the checkbox
                        fields[0].click()
                        raise
            except Exception as e:
                if params["ReturnSuccessIfNoRowSelected"] and 'no such element: Unable to locate element' in e.msg:
                    return True
                else:
                    return False

        # self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", "All")
        SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
            "headerRow_ServiceStatus", "All")

        self.action_ele.clear_input_text("headerRow_ServiceName")
        # self.action_ele.explicit_wait('ServiceGrid_CloseButton')
        wil(self.action_ele.explicit_wait, 'ServiceGrid_CloseButton')
        time.sleep(1)
        self.action_ele.click_element('ServiceGrid_CloseButton')
        self.action_ele.explicit_wait('confirm_box')
        time.sleep(1)
        # self.action_ele.click_element("confirm_box")
        wil(self.action_ele.click_element, "confirm_box", loop_count=40)
        self.action_ele.explicit_wait("header_close_service")
        self.action_ele.click_element("close_user_date")
        self.action_ele.input_text('close_user_date', datetime.date.today().strftime('%m/%d/%Y'))
        self.action_ele.click_element("simple_click")
        if params['keepGlobalTn']:
            element = self._browser.element_finder("close_service_radio1")
            if element.is_selected():
                print("The expected radio button is selected by default")
            else:
                print("The expected radio button is not selected by default")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                raise AssertionError("Could not verify the radio button")
        if params.get('keepGlobalTn', None):
            if params['keepGlobalTn'] == 'no':
                wil(self.action_ele.select_radio_button, "keepGlobalTn_no")
        if params['keepGlobalTn'] == 'yes':
                self.action_ele.select_radio_button('keepGlobalTn_yes')
        if params.get('requested_by', None):
            self.action_ele.explicit_wait("request_dropdown")
            self.action_ele.select_from_dropdown_using_text("request_dropdown", params['requested_by'])
        else:
            self.action_ele.select_from_dropdown_using_index("request_dropdown", 1)

        if params.get('request_source', None) and params['request_source'] != "Case":
            self.action_ele.explicit_wait("ServiceGrid_RequestSource")
            self.action_ele.select_from_dropdown_using_text("ServiceGrid_RequestSource", params['request_source'])
        else:
            self.action_ele.input_text("case_id", 123)
        self.action_ele.click_element("closeServiceWizard_next")
        self.action_ele.click_element("closeServiceWizard_next")
        self.action_ele.click_element("CloseServiceWizard_finish")
        for i in range(self.counter):
            try:
                isDisplayed = self.query_ele.element_displayed("ok_box")
                if isDisplayed:
                    verify_order = self.query_ele.text_present("Close Service order was created")
                    self.action_ele.click_element("ok_box")
                    break
                else:
                    time.sleep(5)
            except:
                print("Retrying click: %d" % i)
                pass
        self._browser._browser.refresh()
        if verify_order:
            return True
        else:
            try:
                self.action_ele.explicit_wait('ServiceGrid_Checkbox')
                self.action_ele.click_element('ServiceGrid_ClearFilter')
                self.action_ele.click_element('ServiceGrid_Refresh')
                self.action_ele.explicit_wait('ServiceGrid_Checkbox')
                self.action_ele.input_text('headerRow_ServiceId', serviceId)
                status = self.query_ele.get_text('ServiceGrid_ServiceStatus_Retrieve')

                if status.tolower() == 'closed':
                    return True
                else:
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    return False

            except Exception:
                print "Service is not closed successfully"
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return False

    def void_global_user_service(self, params):
        """
        `Description:` This Test case will void the global user service from the services page

        `Param:` params: Dictionary contains global user service information

        `:return:` True/False

        `Created by:` Megha Bansal
        """
        params = defaultdict(lambda: '', params)
        self.action_ele.explicit_wait('ServiceGrid_Checkbox')
        self.action_ele.click_element("headerRow_ServiceName")
        if params['serviceName']:
            self.action_ele.input_text("headerRow_ServiceName", params['serviceName'])
        time.sleep(1)
        if params['serviceStatus']:
            self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", params['serviceStatus'])
        #serviceId = self.query_ele.get_text('ServiceGrid_ServiceId_Link')
        if params.get("parent", None):
            for c in ['(', ')', ' ', '-', '+']:
                params["parent"] = params["parent"].replace(c, "")
            self.action_ele.input_text("headerRow_BaseNameStripped", params["parent"])

        serviceTnName = self.query_ele.get_text("ServiceGrid_Tn")
        serviceTn = serviceTnName.split(',', 1)[0]
        self.action_ele.click_element('ServiceGrid_ServiceId_Link')
        self.action_ele.explicit_wait('LNP_service_Detail_tab')

        self.action_ele.select_from_dropdown_using_text('LNP_service_status', params['newStatus'])
        time.sleep(1)
        self.action_ele.explicit_wait('Service_Void_Yes')
        self.action_ele.click_element("Service_Void_Yes")
        self.action_ele.explicit_wait("header_void_service")

        self.action_ele.click_element("Void_EffectiveDate")
        self.action_ele.input_text('Void_EffectiveDate', datetime.date.today().strftime('%m/%d/%Y'))
        self.action_ele.click_element("simple_click")

        time.sleep(1)
        if params['keepGlobalTn'] == "no":
            self.action_ele.select_radio_button('Void_keepGlobalTn_no')
        elif params['keepGlobalTn'] == "yes":
            self.action_ele.select_radio_button('Void_keepGlobalTn_yes')

        self.action_ele.select_from_dropdown_using_index("Void_RequestedBy", 1)
        self.action_ele.select_from_dropdown_using_index("Void_RequestSource", 1)

        self.action_ele.click_element("VoidWizard_next")
        self.action_ele.click_element("VoidWizard_finish")

        for i in range(self.counter):
            try:
                isDisplayed = self.query_ele.element_displayed("LNP_ok")
                if isDisplayed:
                    break
                else:
                    time.sleep(5)
            except:
                self._browser._browser.refresh()

        verify_order = self.query_ele.text_present("successfully updated.")
        self.action_ele.click_element("ok_box")

        if verify_order == False:
            return serviceTn, False
        else:
            self.action_ele.explicit_wait('datagrid_servicesExplorerDataGrid')
            return serviceTn, True

    def update_service_status(self, params):
        """
        `Description:` To update the service status.
        `Param:` Dictionary contains service information
        `Returns:` result - True/False
        `Created by:` Vasuja
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("datagrid_servicesExplorerDataGrid")
            if params['orderId']:
                self.action_ele.input_text("service_headerRow_OrderId", params['orderId'])
            if params['servicename']:
                self.action_ele.clear_input_text("headerRow_ServiceName")
                self.action_ele.input_text("headerRow_ServiceName", params['servicename'])
            if params.get("parent", None):
                for c in ['(', ')', ' ', '-', '+']:
                    params["parent"] = params["parent"].replace(c, "")
                self.action_ele.input_text("headerRow_BaseNameStripped", params["parent"])
            self.action_ele.explicit_wait("select_all_check_box")
            self.action_ele.click_element("select_all_check_box")
            self.action_ele.click_element("service_update_button")
            self.action_ele.explicit_wait("serviceStatus")
            self.action_ele.select_from_dropdown_using_text('serviceStatus', params['serviceStatus'])
            cur_date = datetime.date.today()
            self.action_ele.input_text("Void_EffectiveDate", cur_date.strftime('%m/%d/%Y'))
            self.action_ele.click_element("service_next_button")
            self.action_ele.explicit_wait("service_finish_button")
            # self._browser.waitfor_ajax_complete()
            self.action_ele.click_element("service_finish_button")
            # self.action_ele.explicit_wait("ac_alert_ok")
            wil(self.action_ele.explicit_wait, "ac_alert_ok")
            time.sleep(1)
            self.action_ele.click_element("ac_alert_ok")
            self.action_ele.explicit_wait("select_all_check_box")
            self.action_ele.click_element("select_all_check_box")
            status = True
        except Exception, e:
            print(e)
            self.action_ele.clear_input_text("headerRow_ServiceName")
            print("Failed to update service status")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        finally:
            # self.action_ele.clear_input_text("headerRow_BaseNameStripped")
            wil(self.action_ele.clear_input_text, "headerRow_BaseNameStripped")
            # self.action_ele.clear_input_text("headerRow_ServiceName")
            wil(self.action_ele.clear_input_text, "headerRow_ServiceName")
            return status

    def retrieve_service_id(self, params):

        """
        `Description:` This function retrieves the service id from service page
        `:param1` Dictionary contains service information
        `:return:` serviceId
        `Created by:` Vasuja
        """
        serviceId = None
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("datagrid_servicesExplorerDataGrid")
            if params['orderId']:
                self.action_ele.input_text("service_headerRow_OrderId", params['orderId'])
            if params.get("parent", None):
                for c in ['(', ')', ' ', '-', '+']:
                    params["parent"] = params["parent"].replace(c, "")
                wil(self.action_ele.input_text, "headerRow_BaseNameStripped", params["parent"])
            if params['servicename']:
                self.action_ele.clear_input_text("headerRow_ServiceName")
                self.action_ele.input_text("headerRow_ServiceName", params['servicename'])
            # Get the service info
            service_grid_table = self._browser.element_finder("User_Grid_Canvas")
            if service_grid_table:
                # Get the fields
                columns = service_grid_table.find_elements_by_tag_name('div')
                # verify the columns and get the serviceid
                if 0 != len(columns):
                    serviceId = columns[2].text
        except Exception as err:
            print("Retrieving the serviceId failed")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        # Reset
        self.action_ele.input_text("headerRow_BaseNameStripped", "")
        self.action_ele.input_text("headerRow_ServiceName", "")
        time.sleep(1)
        return serviceId

    def verify_service_status(self, params):
        """
        `Description:` To Verify service status in service page.
        `Param:` Dictionary contains service information (Service id and status)
        `Returns:` result - True/False
        `Created by:` Vasuja
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("headerRow_ServiceId")
            if params['serviceid']:
                wil(self.action_ele.input_text, 'headerRow_ServiceId', params['serviceid'])
            for i in range(self.counter):
                try:
                    service_grid_table = self._browser.element_finder("User_Grid_Canvas")
                    if service_grid_table:
                        # Get the fields
                        columns = service_grid_table.find_elements_by_tag_name('div')
                        if params['serviceStatus']:
                            if columns[10].text == params['serviceStatus']:
                                print ("Expected service status is verified")
                                status = True
                                break
                except:
                    self._browser._browser.refresh()

        except Exception,e:
            print("Retrieving the serviceId failed")
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status
