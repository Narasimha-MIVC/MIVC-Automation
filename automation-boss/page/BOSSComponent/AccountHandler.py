"""Module for handling account functionalities such as Add user, Add Contract etc
   File: AccountHandler.py
   Author: Kenash Kanakaraj
"""

import os
import sys
import time
import datetime
from distutils.util import strtobool
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#For console logs while executing ROBOT scripts
from robot.api.logger import console

from lib import wait_in_loop as WIL
from lib import select_from_dropdown as SFD

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

import web_wrappers.selenium_wrappers as base
import log
import CommonFunctionality

import inspect

__author__ = "Kenash Kanakaraj"




#login to BOSS portal
class AccountHandler(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def verify_contract_state(self, accountName, exp_state):
        '''
        `Description:` Verify the contract state

        `Param1:` params: accountName: Name of account

        `Param2:` params: exp_state: State of account

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            self.action_ele.explicit_wait('cp_allContractsbtnRefresh',60)
            self.action_ele.click_element('cp_allContractsbtnRefresh')
            self.action_ele.explicit_wait('cp_headerRow_AccountName')
            self.action_ele.input_text('cp_headerRow_AccountName', accountName)
            time.sleep(5)   #time for the table to come up
            var = self.query_ele.text_present(exp_state)
            console(var)
            if var:
                status = True
            return status
        except AssertionError, e:
            print(e)
            print("Verify Contract failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_contract(self, params):
        """
        `Description:` To add contract. This method can run on windows only due to dependency on
        "autoit" package.

        `Param:` params: Dictionary contains contract information

        `Returns:` contract_state

        `Created by:` Kenash K
        """
        try:
            contract_state = False
            self.action_ele.click_element("ac_addcontract")
            self.add_account_for_contract(params)
            status = self.add_locations(params)
            if params.get("Failure_Add_Locations_Scenario", None) and params["Failure_Add_Locations_Scenario"] == "True":  # this is a negative test scenario
                return status
            status = self.add_products(params)
            if params.get("Failure_Add_Products_Scenario", None) and params["Failure_Add_Products_Scenario"] == "True":  # this is a negative test scenario
                return status

            contract_state = self.add_terms(params)
            return contract_state
        except AssertionError, e:
            print(e)
            print("Failed to add contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return contract_state

    def add_account_for_contract(self, params):
        """
        `Description:` To add account for contract

        `Param:` params: Dictionary contains account information

        `Returns:` None

        `Created by:` Kenash K
        `Modified by:` Prasanna
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("ac_type")
            self.action_ele.select_from_dropdown_using_text("ac_type", params["accountType"])

            if params["accountType"] != "New Customer":
                self.action_ele.input_text("add_contract_select_existing_ac", params["accountName"])
                time.sleep(2)
                self.action_ele.press_key("add_contract_select_existing_ac", "ENTER")
                time.sleep(2)
            else:
                self.action_ele.input_text("ac_companyName", params["accountName"])
                self.action_ele.select_from_dropdown_using_text("ac_partnerType", params["partnerType"])

            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params["accountType"] != "Migration":
                self.action_ele.select_from_dropdown_using_text("ac_salesPerson", params["salesPerson"])
                self.action_ele.select_from_dropdown_using_text("ac_platformType", params["platformType"])
                self.action_ele.select_from_dropdown_using_text("ac_country1", params["country"])
                if params.get("currency", None):
                    self.action_ele.select_from_dropdown_using_text("ac_currency", params["currency"])
            else:
                pass   # add the fields specific to accountType "Migration"

            # if params["accountType"] != "New Customer":
            #     WIL(self.action_ele.select_from_dropdown_using_text, "add_contract_select_existing_user",
            #                                                     params["SelectExistingUser"])

            self.action_ele.input_text("ac_firstName", params["firstName"])
            self.action_ele.input_text("ac_lastName", params["lastName"])

            self.action_ele.input_text("ac_email", params["email"])
            self.action_ele.input_text("ac_password", params["password"])
            self.action_ele.input_text("ac_passwordConfirm", params["confirmPassword"])
            self.action_ele.click_element("ac_nextbut_0")
        except Exception, e:
            print(e)
            print("Failed to add account for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_locations(self, params):
        """
        `Description:` To add location detail

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Kenash K

        `Modified by :` Vasuja K, Prasanna
        """

        status = True
        try:
            params = defaultdict(lambda: '', params)
            # verify the negative test scenario where we click "next" button without adding the address
            if params.get("Error_No_Address", None) and params["Error_No_Address"] == "True":
                self.action_ele.click_element("ac_nextbut_1")
                time.sleep(2)
                status = False
                element = self._browser.element_finder("add_contract_no_addr_error_msg")
                if element and params.get("Error_Msg", None) and params["Error_Msg"] in element.text:
                    status = True
                self.action_ele.click_element("ac_alert_ok")
                time.sleep(2)
                return status

            self.action_ele.click_element("ac_addLocation")
            self.action_ele.input_text("ac_locationName", params["locationName"])
            self.action_ele.select_from_dropdown_using_text("ac_country2", params["country"])
            if params['country'] == 'Australia':
                self.add_location_australia(params)
            if params['country']=='United States':
                self.add_location_united_states(params)
            if params['country']=='United Kingdom':
                self.add_location_united_kingdom(params)
            self.action_ele.input_text("ac_city", params["city"])
            self.action_ele.input_text("ac_zip", params["zip"])
            if params["no_validation"] == 'True':
                self.action_ele.select_checkbox("ac_validate")
            else:
                self.action_ele.unselect_checkbox("ac_validate")
            self.action_ele.click_element("ac_addlocationformok")

            # verify the negative test scenario where we click "ok" button with invalid address
            if params.get("Error_Invalid_Address", None) and params["Error_Invalid_Address"] == "True":
                time.sleep(2)
                status = False
                element = self._browser.element_finder("add_contract_invalid_addr_error_msg")
                if element and params.get("Error_Msg", None) and params["Error_Msg"] in element.text:
                    status = True
                self.action_ele.click_element("add_contract_add_location_cancel")
                time.sleep(2)
                return status

            self.action_ele.select_from_dropdown_using_text("ac_connectivity",
                                                            params["connectivity"])
            self.action_ele.click_element("ac_nextbut_1")

        except Exception, e:
            print(e)
            print("Failed to add location for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            status = False

        return status

    def add_location_australia(self, params):
        """
        `Description:` To add location details for Country Australia

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.input_text("ac_SubPremises", params["streetNo"])
            self.action_ele.input_text("ac_Address6", params["streetName"])
            self.action_ele.select_from_dropdown_using_text("ac_Address7", params["streetType"])
            self.action_ele.select_from_dropdown_using_text("ac_state", params["state"])
            self.action_ele.input_text("ac_ER_firstName", params["locfirstName"])
            self.action_ele.input_text("ac_ER_LastName", params["loclastName"])
            self.action_ele.input_text("ac_ER_PhoneNumber", params["phoneNumber"])
        except:
            print("Failed to add location with respect to Australia while creating contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_united_states(self, params):
        """
        `Description:` To add location details for Country US

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.input_text("ac_address1", params["Address1"])
            self.action_ele.input_text("ac_address2", params["Address2"])
            self.action_ele.select_from_dropdown_using_text("ac_state", params["state"])
        except:
            print("Failed to add location with respect to United States while creating contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_united_kingdom(self, params):
        """
        `Description:` To add location details for Country UK

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.input_text("ac_address2", params["buildingName"])
            self.action_ele.input_text("ac_address1", params["streetName"])
        except:
            print("Failed to add location with respect to United kingdom while creating contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_products(self, params):
        """
        `Description:` To add products

        `Param:` params: Dictionary contains products information

        `Returns:` None

        `Created by:` Kenash K
		`Modified by :`  Prasanna
        """
        status = True
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("ac_addProducts")
            if params["class"]:
                self.action_ele.select_from_dropdown_using_text("ac_class", params["class"])
            if params["product"]:
                self.action_ele.select_from_dropdown_using_text("ac_Product", params["product"])
            self.action_ele.input_text("ac_Quantity", params["quantity"])
            self.action_ele.select_from_dropdown_using_text("ac_location", params["location"])
            if params["MRR"]:
                self.action_ele.input_text("ac_MRR", params["MRR"])
            if params["NRR"]:
                self.action_ele.input_text("ac_NRR", params["NRR"])
            if params["waiveNRR"] == 'True':
                self.action_ele.select_checkbox("ac_waiveNRR")
            #self.action_ele.click_element("ac_addProducts")
            #self.action_ele.select_from_dropdown_using_text("ac_class01", params["class01"])
            #self.action_ele.select_from_dropdown_using_text("ac_Product01", params["product01"])
            #self.action_ele.input_text("ac_Quantity01", params["quantity01"])
            #self.action_ele.select_from_dropdown_using_text("ac_location01", params["location01"])
            #self.action_ele.input_text("ac_MRR01", params["MRR01"])
            #self.action_ele.input_text("ac_NRR01", params["NRR01"])
            #if params["waiveNRR01"] == 'True':
            #    self.action_ele.select_checkbox("ac_waiveNRR01")
            self.action_ele.click_element("ac_nextbut_2")

            # Adding the failure test scenarios
            if (params.get("Error_No_MRR", None) and params["Error_No_MRR"] == "True") or \
                    (params.get("Error_No_NRR", None) and params["Error_No_NRR"] == "True"):
                time.sleep(2)
                if params.get("Error_No_MRR", None) and params["Error_No_MRR"] == "True":
                    element = self._browser.element_finder("add_contract_no_mrr_error")
                else:
                    element = self._browser.element_finder("add_contract_no_nrr_error")
                if element and element.text == params["Error_Msg"]:
                    return True
                else:
                    return False

        except Exception, e:
            print(e)
            print("Failed to add product for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            status = False

        return status

    def add_terms(self, params):
        """
        `Description:` To add terms

        `Param:` params: ictionary contains terms information

        `Returns:` contract_state

        `Created by:` Kenash K
		`Modified by :`  Prasanna
        """
        try:
            try:
                import autoit
            except ImportError as e:
                print e.msg
            verify_text = ''
            contract_state = False
            params = defaultdict(lambda: '', params)
            self.action_ele.input_text("ac_contractNumber", params["contractNumber"])
            #self.action_ele.input_text("ac_forecastDate", params["forecastDate"])
            if bool(params['forecastDate']):
                if params['forecastDate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('ac_forecastDate', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'ac_forecastDate', params['forecastDate'])

            self.action_ele.input_text("ac_notes", params["notes"])

            # Simulating the scenario where no contract is uploaded
            if (not params.get("Error_No_Contract_Upload", None)) or \
                    (params.get("Error_No_Contract_Upload", None) and params["Error_No_Contract_Upload"] != "True"):
                self.action_ele.click_element("ac_uploadContract")
                for i in range(5):
                    #for clicking the browse button since another control overlaps the button
                    ex = self.query_ele._element_finder("ac_uploadFile1")
                    action = webdriver.common.action_chains.ActionChains(self._browser._browser)
                    action.move_to_element_with_offset(ex, 5, 5).click().perform()
                    time.sleep(5)
                    #autoit.win_wait_active("[TITLE:Open]", 5)
                    #status1 = autoit.win_active("[CLASS:#32770]")
                    status1 = autoit.win_exists("[TITLE:Open]")
                    #status1=1
                    console(status1)
                    if status1 == 0:
                        print("click on browse failed")
                        print("Retrying number: %s "% str(i))
                    else:
                        #Exiting as Open Dialog box has been found
                        print("Exiting as Open Dialog box has been found")
                        break
                else:
                    print("Raising Exception")
                    raise AssertionError
                time.sleep(2) #this is for the path to resolve in the browse window
                autoit.control_send("[TITLE:Open]", "Edit1", params["filePath"])
                time.sleep(1)
                autoit.control_click("[TITLE:Open]", "Button1")
                #autoit.send(params["filePath"])
                #time.sleep(2)
                #autoit.send("{ENTER}")
                self.action_ele.explicit_wait("ac_Ok")
                time.sleep(2)
                self.action_ele.click_element("ac_Ok")
            self.action_ele.select_from_dropdown_using_text("ac_termVersion", params["termVersion"])
            if params["accountType"] == "New Customer":
                self.action_ele.select_from_dropdown_using_text("ac_termLength", params["termLength"])
                self.action_ele.select_from_dropdown_using_text("ac_termRenewalType", params["termRenewalType"])
                if params["termVersion"] != "Version 2.0":
                    self.action_ele.select_from_dropdown_using_text("ac_termInstall", params["termInstall"])
            time.sleep(2)
            self.action_ele.explicit_wait("ac_nextbut_3")
            time.sleep(2)
            self.action_ele.click_element("ac_nextbut_3")
            # simulating the failure test scenario where the contract is not uploaded before clicking next
            if params.get("Error_No_Contract_Upload", None) and params["Error_No_Contract_Upload"] == "True":
                time.sleep(2)
                element = self._browser.element_finder("add_contract_no_contract_doc_error")
                if element and (params.get("Error_Msg", None) and params["Error_Msg"] in element.text):
                    status = True
                else:
                    status = False
                self.action_ele.click_element("ac_alert_ok")
                time.sleep(2)
                return status
            #self.action_ele.explicit_wait("ac_finish")
            time.sleep(2)
            self.action_ele.click_element("ac_finish")
            self.action_ele.explicit_wait("ac_alert_ok", 120)
            verify_text = self.query_ele.text_present("New Contract successfully added for Account")
            time.sleep(2)
            self.action_ele.click_element("ac_alert_ok")
            ##contract_message = self.query_ele.get_text('contract_alert_message')
            if verify_text:
                contract_state = True
            #self.action_ele.explicit_wait("ac_accountContractsDataGridAddContract", 20)  #remove exta wait to load grid uncomment if page is very slow
            return contract_state
        except Exception,e:
            print(e)
            print("Failed to add product for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def confirm_contract(self, instance, location):
        """
        `Description:` To confirm the added contract

        `Param1:' instance: Instance of contact

        `Param2:' location:  Location for which contract is created

        `Returns:` order_number

        `Created by:` Kenash K
        """
        confirm_state = False
        verify_msg = ''
        try:

            time.sleep(2)
            self._browser._browser.refresh()
            self.action_ele.select_from_dropdown_using_text('cf_ContractBillingLocationId', location)

            self.action_ele.explicit_wait('contract_alert_ok')
            self.action_ele.click_element('contract_alert_ok')

            time.sleep(2)
            element = self._browser.element_finder('cf_complianceRequired_no')
            if element:
                element.click()
            else:
                return False
            time.sleep(2)
            
            self._browser._browser.refresh()
            self.add_instance(instance)



            self.action_ele.explicit_wait('cf_btnConfirmContract')
            time.sleep(2)
            self.action_ele.click_element('cf_btnConfirmContract')

            if self._browser.location == "australia":
                self.action_ele.explicit_wait('Par_localAreaCode')
                time.sleep(1)
                self.action_ele.input_text('Par_localAreaCode', 2)
                self.action_ele.click_element('setLocalAreaCodesForm_OK')
            if self._browser.location == "uk":
                self.action_ele.explicit_wait('Par_localAreaCode')
                time.sleep(1)
                self.action_ele.input_text('Par_localAreaCode', 28)
                self.action_ele.click_element('setLocalAreaCodesForm_OK')

            #confirmation of proceeding
            self.action_ele.explicit_wait('contract_alert_ok')
            time.sleep(2)
            self.action_ele.click_element("contract_alert_ok")

            #wait for contract confirmation
            self.action_ele.explicit_wait('contract_alert_ok', 300)
            print("Clicked Confirm OK")
            time.sleep(2)
            #contract_message = self.query_ele.get_text('contract_alert_message')
            verify_msg = self.query_ele.text_present("Contract Status successfully updated.")

            if verify_msg:
                time.sleep(2)
                print("Message found: %s" %verify_msg)
                confirm_message = self.query_ele.get_text("ac_confirm_message")
                order_number = confirm_message.split(":")[-1]
                print(order_number)
                self.action_ele.click_element("contract_alert_ok")
                self._browser._browser.refresh()
                confirm_msg = self.query_ele.text_present("Confirmed")
                if confirm_msg:
                    confirm_state = True
            else:
                print("Message not found")
                time.sleep(1)
                self.action_ele.click_element("contract_alert_ok")
                self._browser._browser.refresh()

            return order_number

        except Exception, e:
            print(e)
            print("Failed to confirm contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_instance(self, instance_name):
        """
        To add instace
        :param instance_name: Name of instance
        :return:
        """
        try:
            self.action_ele.click_element('cf_clustersLink')
            self.action_ele.explicit_wait('ai_editClustersAddButton')
            self.action_ele.click_element('ai_editClustersAddButton')
            self.action_ele.explicit_wait('ai_ClusterId')

            self.action_ele.select_from_dropdown_using_text('ai_ClusterId', instance_name)
            time.sleep(1)
            self.action_ele.click_element('ai_addClusterForm_OK')
            #wait for instance checkbox to appear
            self.action_ele.click_element('ai_clustersForm_Close')

        except Exception, e:
            print(e)
            print("Failed to add product for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def set_location_as_site(self):
        """
        `Description:` This function will set the location as Site

        `Param:` None

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.explicit_wait("site_checkbox")
            self.action_ele.click_element("site_checkbox")
            print("Checked site checkbox")
            time.sleep(2)    #for the site to be marked on UI
            self.action_ele.explicit_wait("ok_btnPartitionSitesOk")
            print("Clicking Ok button to set default location as site")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("ok_btnPartitionSitesOk")
            self.action_ele.explicit_wait("site_checkbox")
            time.sleep(5)   #processing window appears
            for counter in range(20):
                if "Processing, please wait" in self._browser._browser.page_source:
                    print("Waiting for processing..!!!")
                    time.sleep(2)
                else:
                    break
            self.action_ele.explicit_wait("ok_btnPartitionSitesOk", 120)
            self.action_ele.explicit_wait("site_checkbox", 120)
            self.action_ele.explicit_wait("Phone_system_tab")
        except Exception, e:
            print(e)
            print("Failed to set default location as a site")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def delete_contract(self, param):
        """
        To delete contract.
        :param param: Name of contract to delete
        :return:
        """
        try:
            self.action_ele.click_element("cp_allContractsbtnRefresh")
            time.sleep(2)
            self.action_ele.input_text('cp_headerRow_AccountName', param)
            time.sleep(2)
            self.action_ele.click_element('contract_grid_first_column')
            time.sleep(2)
            self.action_ele.click_element('Organization_tab')
            self.action_ele.click_element('orders_page')
            self.action_ele.select_from_dropdown_using_text('order_status_input', "Open")
            rows = self._browser.elements_finder("order_grid")
            rows = rows[1:]
            count = len(rows)
            while rows and count != 0:
                row = rows.pop(0)
                div_list = row.find_elements_by_tag_name("div")
                account_link = div_list[0].find_element_by_tag_name("a")
                account_link.click()
                self.action_ele.explicit_wait('process_button')
                time.sleep(2)
                self.action_ele.click_element('process_button')
                time.sleep(2)
                self.action_ele.click_element('close_yes')
                time.sleep(2)
                rows = self._browser.elements_finder("order_grid")
                rows = rows[1:]
                count = count - 1
            cm = CommonFunctionality.CommonFunctionality(self._browser)
            cm.switch_page_accounts(param)
            self.action_ele.click_element('ac_filter_link')
            # self.action_ele.select_from_dropdown_using_index('ac_filter',5)
            elements = self._browser.elements_finder('ac_filter')
            for element in elements:
                if (element.text == "All accounts"):
                    element.click()
            self.action_ele.input_text('ac_search_account', param)
            row = self._browser.element_finder('ac_contracts_grid')
            div_list = row.find_elements_by_tag_name("div")
            checkbox = div_list[0].find_element_by_tag_name("input")
            checkbox.click()
            self.action_ele.click_element('ac_contract_close')
            cur_date = datetime.date.today()
            self.action_ele.input_text('ac_cease_date', cur_date.strftime('%m/%d/%Y'))
            self.action_ele.select_from_dropdown_using_text('ac_cease_reason', "Lost For Cause")
            self.action_ele.select_from_dropdown_using_index('ac_requested_by', 2)
            self.action_ele.select_from_dropdown_using_text('ac_request_source', "Case")
            self.action_ele.input_text('ac_case_number', "12345")
            self.action_ele.input_text('ac_notify_mail', 'staff@shoretel.com')
            time.sleep(5)
            self.action_ele.click_element('ac_next')
            self.action_ele.click_element('ac_next')
            self.action_ele.click_element('ac_closeaccount_finish')
            try:
                element = self._browser.element_finder('ac_error')
                return False
            except Exception, e:
                return True
        except:
            print(e)
            print("Failed to delete contract")

    def verify_delete_contract(self, param):
        """
        To verify the contract is deleted.
        :param param: Contract name
        :return:
        """
        try:
            # self.action_ele.click_element('ac_filter_link')
            # elements = self._browser.elements_finder('ac_filter')
            # for element in elements:
            #     if (element.text == "All accounts"):
            #         element.click()
            status = False
            import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.click_element("account_filter_button")
            elements = self._browser.elements_finder("filer_list")
            for ele in elements:
                if ele.text == "All accounts":
                    ele.click()
                    break
            self.action_ele.clear_input_text("contract_name_filed")
            self.action_ele.input_text("contract_name_filed",param)
            self.action_ele.click_element("contract_chk_box")
            self.action_ele.click_element("name_contract")
            elements_label=self._browser.elements_finder("disp_name")
            elements_data=self._browser.elements_finder("dis_value")
            for i in range(len(elements_label)):
                if elements_label[i].text == "Status" and elements_data[i].text == "Closed":
                    status = True
                    print("Contract Closed")
        except Exception,e:
            print(e)
        return status

    def provision_initial_order(self):
        """
        `Description:` Provisioning initial order

        `:param:` None

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            self.action_ele.explicit_wait('order_status_input')
            self.action_ele.select_from_dropdown_using_text('order_status_input', "Pending")
            self.action_ele.select_from_dropdown_using_text('order_type', "Initial")
            rows = self._browser.elements_finder("order_grid")
            rows = rows[1:]
            count = len(rows)
            while rows and count != 0:
                row = rows.pop(0)
                div_list = row.find_elements_by_tag_name("div")
                account_link = div_list[0].find_element_by_tag_name("a")
                account_link.click()
                self.action_ele.explicit_wait('auto_provisioning')
                time.sleep(2)
                self.action_ele.click_element('auto_provisioning')
                time.sleep(2)
                self.action_ele.click_element('close_yes')
                time.sleep(2)
                rows = self._browser.elements_finder("order_grid")
                rows = rows[1:]
                count = count - 1
            status = True
            time.sleep(3)
            self._browser._browser.refresh()
        except Exception,e:
            print(e)
        return status

    def activate_all_service(self):
        """
        `Description:` Activate all services

        `:param:` None

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = False
            # Prasanna: self.action_ele.explicit_wait("select_all_check_box")
            WIL(self.action_ele.click_element, "select_all_check_box")
            # Prasanna: time.sleep(2)
            #if self.query_ele.element_enabled("service_update_button"):
            WIL(self.action_ele.click_element, "service_update_button")
            time.sleep(5)
            # self.action_ele.explicit_wait("service_next_button")
            # self.action_ele.select_from_dropdown_using_text("service_list", "Active")
            WIL(self.action_ele.select_from_dropdown_using_text, "service_list", "Active")
            cur_date = datetime.date.today()
            # self.action_ele.input_text("active_date", cur_date.strftime('%m/%d/%Y'))
            self.action_ele.input_text("effective_date", cur_date.strftime('%m/%d/%Y'))
            self.action_ele.click_element("service_next_button")
            cm = CommonFunctionality.CommonFunctionality(self._browser)
            cm.check_alert()
            time.sleep(2)
            WIL(self.action_ele.explicit_wait, "service_finish_button", {'ec': "text_to_be_present_in_element", 'msg_to_verify': "Finish"})
            # time.sleep(1)
            WIL(self.action_ele.click_element, "service_finish_button")
            time.sleep(2)
            WIL(self.action_ele.explicit_wait, "ac_alert_ok", {'ec': "text_to_be_present_in_element", 'msg_to_verify': "OK"})
            # time.sleep(1)
            self.action_ele.click_element("ac_alert_ok")
            time.sleep(5)
            self._browser._browser.refresh()
            status = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status


    def close_all_order(self):
        """
        `Description:`  To close all order

        `:param:` None

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = False
            time.sleep(2)
            WIL(self.action_ele.select_from_dropdown_using_text, 'order_status_input', "All")
            WIL(self.action_ele.select_from_dropdown_using_text, 'order_type', "All")
            ordersid = WIL(self._browser.elements_finder, "order_id_list", return_value=True)
            for id in range(len(ordersid)):
                self._browser._browser.refresh()
                ordersid = WIL(self._browser.elements_finder, "order_id_list", return_value=True)
                order_status = WIL(self._browser.elements_finder, "current_order_status", return_value=True)
                if order_status[id].text != "Closed":
                    time.sleep(2)
                    ordersid[id].click()
                    self.action_ele.explicit_wait('save_button_order_page')
                    time.sleep(2)
                    WIL(self.action_ele.select_from_dropdown_using_text, "order_status_to_close", "Closed")
                    WIL(self.action_ele.click_element, 'save_button_order_page')
                    time.sleep(2)
                    # Prasanna: Added the extra condition
                    el = WIL(self._browser.elements_finder, "ac_error_ok", return_value=True)
                    if el:
                        el[1].click()
                        time.sleep(1)
                        WIL(self.action_ele.explicit_wait, "expand_button")
                        time.sleep(3)

            time.sleep(3)

            status = True
        except Exception, e:
            print(e)
        return status

    def close_contract(self,name, req_by=None):
        """
        `Description:`  To close contract

        `:param:` contract name

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """

        try:
            status = False
            self.action_ele.click_element("account_filter_button")
            elements = self._browser.elements_finder("filer_list")
            for ele in elements:
                if ele.text == "All accounts":
                    ele.click()
                    break
            self.action_ele.input_text("contract_name_filed",name)
            time.sleep(3)
            self.action_ele.click_element("contract_chk_box")
            self.action_ele.click_element("close_conract")
            WIL(self.action_ele.explicit_wait, "next_button", loop_count=40)
            cur_date = datetime.date.today()
            self.action_ele.input_text("close_date", cur_date.strftime('%m/%d/%Y'))
            self.action_ele.click_element("label1")
           # Modified by: Priyanka
            if req_by:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'req_by', req_by, loop_count=40)
                # self.action_ele.select_from_dropdown_using_text("req_by", params["requestedBy"])
            else:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                    'req_by', 1, loop_count=40)
 #            self.action_ele.select_from_dropdown_using_index("req_by",-1)
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'req_source', "Email", loop_count=40)
            #self.action_ele.select_from_dropdown_using_text("req_source","Email")
            # WIL(self._browser.elements_finder, "next_button", return_value=True)
            WIL(self.action_ele.click_element, "next_button", loop_count=40)
            # WIL(self._browser.elements_finder, "next_button", return_value=True)
            WIL(self.action_ele.click_element, "next_button", loop_count=40)
            self.action_ele.click_element("finishbtn")
            #WIL(self._browser.elements_finder, "ac_error_ok", return_value=True)
            WIL(self.action_ele.explicit_wait, "ac_error_ok", loop_count=40)
            time.sleep(3)
            WIL(self.action_ele.click_element, "ac_error_ok")
            time.sleep(4)
            status = True
        except Exception,e:
            print(e)
        return status

    def add_account(self, params):
        """
        `Description:` To add account.

        `Param:` params: Dictionary contains new account information

        `Returns:` status

        `Created by:` Prasanna
        """
        status = True
        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            # Add new account
            self.action_ele.click_element("add_ac")

            # Verify the error message when the continue button is clicked without required information
            if params.get("continue_without_req_info", None):
                WIL(self.action_ele.click_element, "add_ac_continue")
                element = WIL(self.query_ele._element_finder, "add_ac_continue_error_acc_type", return_value=True)
                if element and params.get("ErrorMsg", None) and element.text == params["ErrorMsg"]:
                    return True
                else:
                    raise Exception("Error message verification failed")
            # Adding Company ---
            self.action_ele.explicit_wait("add_ac_company_type")
            self.action_ele.select_from_dropdown_using_text("add_ac_company_type", params["accountType"])
            self.action_ele.input_text("add_ac_company_name", params["accountName"])

            # Adding Contact ---
            self.action_ele.input_text("add_ac_contact_firstname", params["firstName"])
            self.action_ele.input_text("add_ac_contact_lastname", params["lastName"])
            self.action_ele.input_text("add_ac_contact_email", params["email"])
            self.action_ele.input_text("add_ac_contact_password", params["password"])
            self.action_ele.input_text("add_ac_contact_confirm_password", params["confirmPassword"])

            # Adding Location ---
            self.action_ele.input_text("add_ac_location_name", params["locationName"])
            self.action_ele.select_from_dropdown_using_text("add_ac_location_country", params["country"])

            if params['country'] == 'Australia':
                self.action_ele.input_text("add_ac_location_country_aus_street_no", params["streetNo"])
                self.action_ele.input_text("add_ac_location_country_aus_street_name", params["streetName"])
                self.action_ele.select_from_dropdown_using_text("add_ac_location_country_aus_street_type", params["streetType"])
                self.action_ele.select_from_dropdown_using_text("add_ac_location_state", params["state"])

                # Emergency registration --- Applicable only for Australia
                self.action_ele.input_text("add_ac_emergency_reg_firstname", params["locfirstName"])
                self.action_ele.input_text("add_ac_emergency_reg_lastname", params["loclastName"])
                self.action_ele.input_text("add_ac_emergency_reg_phonenumber", params["phoneNumber"])

            elif params['country'] == 'United States':
                self.action_ele.input_text("add_ac_location_country_us_address1", params["Address1"])
                # self.action_ele.input_text("ac_address2", params["Address2"])
                self.action_ele.select_from_dropdown_using_text("add_ac_location_state", params["state"])

            elif params['country'] == 'United Kingdom':
                pass
            else:
                raise Exception("No Country selected!!")

            self.action_ele.input_text("add_ac_location_city", params["city"])
            self.action_ele.input_text("add_ac_location_zipcode", params["zip"])

            # Check if validation is required for the location info ---
            if params["no_validation"]:
                self.action_ele.select_checkbox("add_ac_location_bypass")

            # Create Partition ---
            if params["create_partition_flag"]:
                self.action_ele.select_checkbox("add_ac_create_partition")
                self.action_ele.select_from_dropdown_using_text("add_ac_create_partition_instance", params["clusterInstance"])
                self.action_ele.select_from_dropdown_using_text("add_ac_create_partition_timezone", params["timezone"])

            # Continue ---
            time.sleep(3)
            self.action_ele.click_element("add_ac_continue")
            time.sleep(5)

            t_sec = 0
            for i in range(5):
                t_sec = t_sec + 5
                try:
                    self.action_ele.explicit_wait("add_ac_yes_button")
                    self.action_ele.click_element("add_ac_yes_button")
                    t_sec = 0
                    break
                except Exception:
                    pass
                time.sleep(t_sec)
            else:
                raise Exception("The 'Yes' button not active")

            for i in range(5):
                t_sec = t_sec + 5
                try:
                    self.action_ele.explicit_wait("ac_alert_ok")
                    self.action_ele.click_element("ac_alert_ok")
                    t_sec = 0
                    break
                except Exception:
                    pass
                time.sleep(t_sec)
            else:
                raise Exception("The 'OK' button not active")

            for i in range(5):
                t_sec = t_sec + 5
                try:
                    self.action_ele.explicit_wait("Account_Home_Page")
                    self.action_ele.click_element("Account_Home_Page")
                    t_sec = 0
                    break
                except Exception:
                    pass
                time.sleep(t_sec)
            else:
                raise Exception("The Account home page is not visible")

            time.sleep(3)

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

        return status

    def get_account_details(self, params):

        try:
            if params.get("get_account_id", None):
                new_ac_id = (self._browser._browser.current_url).split("accountId=")[1].split("&")[0]
                params.update({'account_id': new_ac_id})
                # clicking on partition tab and get the account information
                WIL(self.action_ele.click_element, "partition_tab")
                # get the grid
                grid = self._browser.element_finder("partition_tab_grid")
                if not grid:
                    raise Exception("No element grid found")
                row = grid.find_element_by_tag_name("div")
                if not row:
                    raise Exception("No row in grid found")
                columns = row.find_elements_by_tag_name("div")
                if not columns:
                    raise Exception("No fields !!")
                params.update({'partition_id': columns[3].text, 'prefix': columns[4].text})
            else:
                self.action_ele.explicit_wait("organization_account_details_show")
                self.action_ele.click_element("organization_account_details_show")
                time.sleep(2)
                self.action_ele.explicit_wait("organization_account_details_ac_id")
                ac_id = self.query_ele.get_text("organization_account_details_ac_id")
                self.action_ele.explicit_wait("organization_account_details_token")
                token = self.query_ele.get_text("organization_account_details_token")
                params.update({"accountId": ac_id, "token": token})
        except Exception, e:
            print(e.message)
            return False

        return True

    def verify_account(self, params):
        """Verify the account"""

        status = True
        # click on account status filter options
        try:
            cm = CommonFunctionality.CommonFunctionality(self._browser)
            cm.switch_page_accounts(params)
            self.action_ele.click_element('ac_filter_link')
            elements = self._browser.elements_finder('ac_filter')
            for element in elements:
                if element.text == "All accounts":
                    element.click()
                    break
            else:
                raise Exception("All accounts option not found")

            # verify that the account is present in the grid
            self.action_ele.input_text("ac_search_account", params["accountName"])
            element = self._browser.element_finder("ac_grid")
            if not element:
                raise Exception("No account grid")

            row = element.find_element_by_tag_name("div")
            if not row:
                raise Exception("No rows found with the account name")

            # @Added By: Prasanna
            if params.get("get_account_info", None):
                link = self._browser._browser.find_element_by_link_text(params["accountName"])
                link.click()
                time.sleep(2)
                new_ac_id = (self._browser._browser.current_url).split("accountId=")[1].split("&")[0]
                params.update({'account_id': new_ac_id})
                time.sleep(2)
        except Exception as e:
            print(e.message)
            status = False

        return status

    def verify_global_user_loc_not_in_account_details_page(self,params):
        '''
        `Description:` verify global user loc in account details page

        `Param:` Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Palla Surya Kumar
        ''' 
        status=False
        try:
            self.action_ele.click_element('acc_page_geo_loc')
            self.action_ele.explicit_wait('acc_page_geo_loc_dropdown')
            self.action_ele.click_element('acc_page_geo_loc_dropdown')
            loc_list=self._browser.element_finder('acc_page_geo_loc_dropdown')
            drop_down_values=loc_list.find_elements_by_tag_name('option')
            for ele in range(len(drop_down_values)):
                if drop_down_values[ele].text==params['geo_location']:
                    status=False
                    break
                else:
                    status=True
        except:
            print ('Could not verify global user loc in account details page!!')
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        finally:
            return status



    def add_account_using_Connect(self, params):
        """
        `Description:` To add account through connect

        `Param:` params: Dictionary contains new account information

        `Returns:` status

        `Created by:` Priyanka
        """
        status = False
        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            # Add new account
            # Adding Company ---
            self.action_ele.input_text("add_ac_company_name", params["accountName"])

            # Adding Contact ---
            self.action_ele.input_text("add_ac_contact_firstname", params["firstName"])
            self.action_ele.input_text("add_ac_contact_lastname", params["lastName"])
            self.action_ele.input_text("add_ac_contact_email", params["email"])
            self.action_ele.input_text("add_ac_contact_password", params["password"])
            self.action_ele.input_text("add_ac_contact_confirm_password", params["confirmPassword"])

            # Adding Location ---
            self.action_ele.input_text("add_ac_location_name", params["locationName"])
            self.action_ele.select_from_dropdown_using_text("add_ac_location_country", params["country"])

            if params['country'] == 'Australia':
                self.action_ele.input_text("add_ac_location_country_aus_street_no", params["streetNo"])
                self.action_ele.input_text("add_ac_location_country_aus_street_name", params["streetName"])
                self.action_ele.select_from_dropdown_using_text("add_ac_location_country_aus_street_type", params["streetType"])
                self.action_ele.select_from_dropdown_using_text("add_ac_location_state", params["state"])

                # Emergency registration --- Applicable only for Australia
                self.action_ele.input_text("add_ac_emergency_reg_firstname", params["locfirstName"])
                self.action_ele.input_text("add_ac_emergency_reg_lastname", params["loclastName"])
                self.action_ele.input_text("add_ac_emergency_reg_phonenumber", params["phoneNumber"])

            elif params['country'] == 'United States':
                self.action_ele.input_text("add_ac_location_country_us_address1", params["Address1"])
                # self.action_ele.input_text("ac_address2", params["Address2"])
                self.action_ele.select_from_dropdown_using_text("add_ac_location_state", params["state"])

            elif params['country'] == 'United Kingdom':
                pass
            else:
                raise Exception("No Country selected!!")

            self.action_ele.input_text("add_ac_location_city", params["city"])
            self.action_ele.input_text("add_ac_location_zipcode", params["zip"])

            # Check if validation is required for the location info ---
            if params["no_validation"]:
                self.action_ele.select_checkbox("add_ac_location_bypass")

            # Accept Terms and Condition ---
            self.action_ele.click_element("accept_terms_cond_link")
        #    self._browser.find_elements_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            self.action_ele.click_element("accept_terms_cond_checkbox")

            # Continue ---
            time.sleep(3)
            self.action_ele.click_element("add_ac_continue")
            time.sleep(5)
            cm = CommonFunctionality.CommonFunctionality(self._browser)
            cm.check_alert()
            time.sleep(2)
            t_sec = 0
            status = True
            for i in range(5):
                t_sec = t_sec + 5
                try:
                    self.action_ele.explicit_wait("Account_Home_Page")
                    self.action_ele.click_element("Account_Home_Page")
                    t_sec = 0
                    status = True
                    break
                except Exception:
                    pass
                time.sleep(t_sec)
            else:
                raise Exception("The Account home page is not visible")

            time.sleep(3)

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

        return status

    def update_verify_account_website_detail(self,siteName):
        status = False
        try:
            self.action_ele.click_element("website_link")
            self.action_ele.clear_input_text("website_input")
            self.action_ele.input_text("website_input",siteName)
            time.sleep(2)
            self.action_ele.click_element("website_save_click")
            #self._browser._browser.refresh()
            time.sleep(1)
            # verify site name
            #self.action_ele.click_element("website_link")
            verify_text = self.query_ele.get_text("website_link")
            #verify_text = verify_text.split("//")
            print(verify_text)
            console(verify_text)
            #self.verify_website_detail(verify_text[1], siteName, "update")
            status = True
        except Exception, e:
            print(e.message)
        return status


    def delete_account_website_detail(self):
        status = False
        try:
            self.action_ele.click_element("website_link")
            self.action_ele.clear_input_text("website_input")
            time.sleep(2)
            self.action_ele.click_element("website_save_click")
            time.sleep(1)
            self._browser._browser.refresh()
            time.sleep(2)
            #verify site name
            self.action_ele.click_element("website_link")
            verify_text = self.query_ele.get_value("website_input")
            time.sleep(1)
            console(verify_text)
            self.verify_website_detail(verify_text, "N/A", "delete")
            status = True
        except Exception, e:
            print(e.message)
        return status

    def verify_website_detail(self,actual_val,expected_val,action):
        if actual_val == expected_val :
            print("Website name updated and verified")
            return True
        else :
            raise Exception("Fail to "+action +" Website name")


