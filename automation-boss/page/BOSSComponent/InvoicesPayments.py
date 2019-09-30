"""Module for creating and verifying invoice group
   File: InvoicesPayments.py
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

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

import web_wrappers.selenium_wrappers as base
import log
import inspect
__author__ = "Vasuja"



#login to BOSS portal
class InvoicesPayments(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def create_invoice_group(self, params):
        """
        `Description:` This function will create the invoice group.

        `Param:` params: Dictionary contains  invoice group Info

        `Returns:` None

        `Created by:` Vasuja
        """
        try:
            time.sleep(2)
            self.action_ele.click_element("tab_invoices_groups")
            self.action_ele.click_element("invoiceGroups_AddButton")
            self.action_ele.input_text("Invoice_name", params["invoiceName"])
            self.action_ele.select_from_dropdown_using_text("invoice_contact", params["primaryInvoiceContact"])
            self.action_ele.select_from_dropdown_using_text("SecondaryBillingContact",params["secondaryInvoiceContact"])
            self.action_ele.click_element("invoiceGroupWizard_next")
            self.action_ele.select_from_dropdown_using_text("invoice_location", params["Location"])
            self.action_ele.click_element("btnAddLocation")
            self.action_ele.click_element("invoiceGroupWizard_next")
            self.action_ele.select_from_dropdown_using_text("CountryKey", params["Country"])
            if self._browser.location == 'australia':
                self.create_mailing_address_For_Austarlia(params)
            if self._browser.location=='us':
                self.create_mailing_address_For_US(params)
            if self._browser.location=='uk':
                self.create_mailing_address_For_UK(params)
            self.action_ele.input_text("ZipCode", params["Zip"])
            self.action_ele.click_element("invoiceGroupWizard_finish")
            self.action_ele.explicit_wait('fnMessageBox_OK')
            time.sleep(2)
            self.action_ele.click_element("fnMessageBox_OK")

        except AssertionError as assert_err:
            print("ASSERTION ERROR: %s" % assert_err.message)
            print("Invoice group creation failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_mailing_address_For_US(self, params):
        """
        `Description:` This function will create the mailing address for invoice group which is specific to US location.

        `Param:` params: Dictionary contains  invoice group Info

        `Returns:` None

        `Created by:` Tantri Tanisha
        """
        try:
            self.action_ele.input_text("Address1", params["Address01"])
            self.action_ele.input_text("Address2", params["Address02"])
            self.action_ele.input_text("City", params["city"])
            self.action_ele.select_from_dropdown_using_text("StateProvinceKey", params["state"])
        except:
            print("Failed to add Mailing address with respect to US for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_mailing_address_For_Austarlia(self, params):
        """
        `Description:` This function will create the mailing address for invoice group which is specific to Austarlia location.

        `Param:` params: Dictionary contains  invoice group Info

        `Returns:` None

        `Created by:` Hanumanthu Susmitha
        """
        try:
            self.action_ele.input_text("ac_SubPremises", params["streetNo"])
            self.action_ele.input_text("ac_Address6", params["streetName"])
            self.action_ele.select_from_dropdown_using_text("ac_Address7", params["streetType"])
            self.action_ele.input_text("City", params["city"])
            self.action_ele.select_from_dropdown_using_text("ac_state", params["state"])
        except:
            print("Failed to add Mailing address with respect to Austarlia for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def create_mailing_address_For_UK(self, params):
        """
        `Description:` This function will create the mailing address for invoice group which is specific to UK location.

        `Param:` params: Dictionary contains invoice group Info

        `Returns:` None

        `Created by:` Hanumanthu Susmitha/ Tantri Tanisha
        """
        try:
            self.action_ele.input_text("Address2", params["buildingName"])
            self.action_ele.input_text("Address1", params["streetName"])
            self.action_ele.input_text("City", params["postalTown"])
        except:
            print("Failed to add Mailing address with respect to UK for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_invoice_group_location(self, params):
        """
        `Description:` This function will verify the invoice group location.

        `Param:` params: Dictionary contains  invoice group Info

        `Returns:` status - True/False

        `Created by:` Vasuja
        """
        try:
            status = False
            self.action_ele.explicit_wait('invoiceGroupWizard_next')
            self.action_ele.click_element("invoiceGroupWizard_next")
            verify_text = self.query_ele.text_present(params["Location"])
            self.action_ele.click_element("invoiceGroupWizard_next")
            self.action_ele.click_element("invoiceGroupWizard_finish")
            self.action_ele.explicit_wait('fnMessageBox_OK')
            time.sleep(2)
            self.action_ele.click_element("fnMessageBox_OK")
            if verify_text:
                print(verify_text)
                status=True
                return status
            else:
                status = False
                return status
        except:
            print("Invoice group is not associated with location ")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status
