import os
import sys
import time
import datetime
from distutils.util import strtobool
from collections import defaultdict
from lib import wait_in_loop as WIL
from lib import select_from_dropdown as SFD
from CommonFunctionality import CommonFunctionality
from AccountHandler import AccountHandler

#For console logs while executing ROBOT scripts
from robot.api.logger import console

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

#import base
import web_wrappers.selenium_wrappers as base
import log

import inspect
__author__ = "Kenash Kanakaraj"




#login to BOSS portal
class UserHandler(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.hw_info = False
        self.counter = 3
        self.commonfunctionality = CommonFunctionality(self._browser)
        self.account_handler = AccountHandler(self._browser)

    def add_user(self, params):
        '''
        `Description:` Create user in BOSS portal

        `Param:` params: Dictionary contains user information

        `Returns:` phone_number, extn, status

        `Created by:` Kenash K

        'Modified By:' Palla Surya Kumar
        '''
        phone_number, extn = (None, None)
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            params = defaultdict(lambda: '', params)
            status = False
            self.hw_info = False
            self.action_ele.explicit_wait('adduser_button')
            WIL(self.action_ele.click_element,'adduser_button', loop_count=40)
            isglobaluser = self.add_contact_info(params)
            # Prasanna: Added status. Added the check to skip the addition of phone
            if not params["skip_add_phone"]:
                status, phone_number, extn = self.add_phone_info(params)
                if not status:
                    raise Exception("Adding phone info failed")
            if not isglobaluser:
                if self.hw_info:
                    self.add_hardware_info(params)
            if params["skip_add_phone"]:
                WIL(self.action_ele.click_element, 'adduser_contactnextbutton')

            self.add_role(params)
            # Modified By: Palla Surya Kumar
            # added status to ensure checking of user added other than checking at verify user
            status = self.add_user_confirm(params)
            WIL(self.action_ele.click_element, "email_search", loop_count=30)
            # self.action_ele.explicit_wait('email_search', 300)
            # WIL(self.action_ele.click_element, "email_search")
            return phone_number, extn, status
        except:
            print("Failed to add user")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return None, None, False

    def add_contact_info(self, params):
        '''
        `Description:` Add user for BOSS portal

        `Param:` params: Dictionary contains user information

        `Returns:` global user status - True/False

        `Created by:` Kenash K

        `Modified by:` Tantri Tanisha, Hanumanthu Susmitha
        '''
        isglobaluser = False
        try:
            params = defaultdict(lambda: '', params)
            WIL(self.action_ele.explicit_wait, "adduser_firstname", loop_count=40)
            self.action_ele.input_text('adduser_firstname', params['au_firstname'])
            self.action_ele.input_text('adduser_lastname', params['au_lastname'])
            self.action_ele.input_text('adduser_businessEmail', params['au_businessmail'])
            self.action_ele.input_text('adduser_personalEmail', params['au_personalmail'])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'adduser_userLocation', params['au_userlocation'])
            # time.sleep(3)
            # self.action_ele.select_from_dropdown_using_text('adduser_userLocation', params['au_userlocation'])
            if params['au_userlocation'] in params['global_countries']:
                isglobaluser = True  #its a global user
            # Prasanna: else is not required
            # else:
            #     isglobaluser = False #its a normal user
            self.action_ele.select_from_dropdown_using_text('adduser_billingLocation', params['au_location'])
            self.action_ele.input_text('adduser_title', params['au_title'])
            self.action_ele.input_text('adduser_cellPhone', params['au_cellphone'])
            self.action_ele.input_text('adduser_homePhone', params['au_homephone'])
            self.action_ele.select_from_dropdown_using_text('adduser_preferredNotificationEmail',
                                                            params['au_preferrednotificationemail'])
            self.action_ele.select_from_dropdown_using_text('adduser_preferredContactMethod',
                                                            params['au_preferredcontactmethod'])
            self.action_ele.input_text('adduser_userName', params['au_username'])
            self.action_ele.input_text('adduser_password', params['au_password'])
            self.action_ele.input_text('adduser_confirmPassword', params['au_confirmpassword'])
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element('adduser_contactnextbutton')
        except:
            print("Failed to add contact info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return isglobaluser

    def add_phone_info(self, params):
        '''
        `Description:` Add phone info while adding user for BOSS portal

        `Param:` params: Dictionary contains phone information

        `Returns:` phonenum, extn

        `Created by:` Kenash K
        '''
        phonenum = ''
        extn = ''
        index = 1
        status = True
        try:
            params = defaultdict(lambda: '', params)
            if params['ap_phoneloc']:
                self.action_ele.select_from_dropdown_using_text('phone_Location', params['ap_phoneloc'])
            self.action_ele.select_from_dropdown_using_text('phone_Type', params['ap_phonetype'])

            if bool(params['ap_phonenumber']):
                if params['ap_phonetype'] != 'MiCloud Connect Voicemail Only':
                    self.hw_info = True
                else:
                    self.hw_info = False
                # Added by: Priyanka - Checking phone numbers for all locations
                if params.get('ph_num_chk_box', None) == 'Yes':
                    self.action_ele.click_element('adduser_phoneAllLocations')
                if params['ap_phonenumber'] == "random":
                    SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                        'phone_Number', index)
                    # # Prasanna: Added the index to make it dynamic
                    # self.action_ele.select_from_dropdown_using_index('phone_Number', index)
                    index += 1
                else:
                    self.action_ele.select_from_dropdown_using_text('phone_Number', params['ap_phonenumber'])
                phonenum = self.query_ele.get_text_of_selected_dropdown_option('phone_Number')
                if not params['ap_extn']:
                    extn = self.query_ele.get_value('Person_Profile_Extension')
                else:
                    extn = params['ap_extn']

            if bool(params['ap_activationdate']):
                if params['ap_activationdate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('activationDate', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'activationDate', params['ap_activationdate'])

            #todo checkbox
            #account_type = params.get('account_type', 'cosmo').lower()
            #if account_type == 'cosmo':
            #    self.select_products_for_users_cosmo(params)
            #else:
            #    self.select_products_for_users(params)
            self.action_ele.click_element("user_label")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            # Modified by - Prasanna:
            while True:
                self.action_ele.click_element('adduser_contactnextbutton')
                errors = self._browser.elements_finder('user_errors')
                for error in errors:
                    if "Extension is in use or not valid." in error.text:
                        # Modified by - Prasanna: Assigning new number from the drop down instead of new extension
                        if params["assign_new_number"]:
                            self.action_ele.select_from_dropdown_using_index('phone_Number', index)
                            index += 1
                            params["assign_new_number"] = index
                            extn = self.query_ele.get_value('Person_Profile_Extension')
                            phonenum = self.query_ele.get_text_of_selected_dropdown_option('phone_Number')
                            break
                        else:
                            extn = error.text.split(':')[-1].strip()
                            self.action_ele.input_text('Person_Profile_Extension', extn)
                            # Prasanna: self.action_ele.click_element('adduser_contactnextbutton')
                            break
                else:
                    break
        except:
            status = False
            print("Failed to update phone info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status, phonenum, extn

    def add_mobile_number_to_user(self, params):
        """
        """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            params = defaultdict(lambda: '', params)
            self.action_ele.input_text('email_search', params['email'])
            self.action_ele.explicit_wait('user_phone_settings_dm_pm')
            self.action_ele.click_element('user_phone_settings_dm_pm')
            self.action_ele.explicit_wait('user_mobile_number')
            self.action_ele.click_element('user_mobile_number')
            self.action_ele.input_text('user_mobile_number_text', params['num'])
            time.sleep(1)
            self.action_ele.click_element('user_mobile_number_save')
        except:
            raise AssertionError("Could not assign mobile number to user!!")

    def remove_mobile_number_for_user(self, params):
        """
        """
        try:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            params = defaultdict(lambda: '', params)
            self.action_ele.input_text('email_search', params['email'])
            self.action_ele.explicit_wait('user_phone_settings_dm_pm')
            self.action_ele.click_element('user_phone_settings_dm_pm')
            self.action_ele.explicit_wait('user_mobile_number')
            self.action_ele.click_element('user_mobile_number')
            self.action_ele.clear_input_text('user_mobile_number_text')
            time.sleep(1)
            self.action_ele.click_element('user_mobile_number_save')
        except:
            raise AssertionError("Could not remove  mobile number!!")

    def add_hardware_info(self, params):
        '''
        `Description:` Add hardware info while adding user for BOSS portal

        `Param:` params: Dictionary contains hardware information

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            params = defaultdict(lambda: '', params)
            if bool(strtobool(params['hw_addhwphone'])):
                self.action_ele.select_checkbox('hw_add')
                self.action_ele.select_from_dropdown_using_text('hw_type', params['hw_type'])
                self.action_ele.select_from_dropdown_using_text('hw_model', params['hw_model'])
                self.action_ele.input_text('hw_ship_date', params['hw_shipdate'])
            if bool(strtobool(params['hw_power'])):
                self.action_ele.select_checkbox('hw_power_supply')
                self.action_ele.select_from_dropdown_using_text('hw_power_supply_type', params['hw_power_type'])
            self.action_ele.click_element('adduser_contactnextbutton')
        except:
            print("Failed to add hardware info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_role(self, params):
        '''
        `Description:` Add Role of user while adding user for BOSS portal

        `Param1:` params: role: Role of user, scope: Scope of user

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait('availableRoles')
            self.action_ele.select_from_dropdown_using_text('availableRoles', params['role'])
            self.action_ele.explicit_wait('addRoles')
            self.action_ele.click_element('addRoles')
            if params['scope'].lower() == 'location':
                self.action_ele.click_element('loc_scope')
            #self.action_ele.explicit_wait('adduser_contactnextbutton')
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element('adduser_contactnextbutton')
        except:
            print("Failed to add user roles")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def process_given_order(self,order_num):
        '''
        `Description:` To process given order

        `Param1:` params: order_num

        `Returns:` None

        `Created by:` Palla Surya Kumar
        '''
        try:
            # enter the order number
            self.action_ele.explicit_wait('OrderOrderIDTextSearch')
            self.action_ele.clear_input_text('OrderOrderIDTextSearch')
            self.action_ele.input_text('OrderOrderIDTextSearch',order_num)

            #retrieve the order id link and click on it
            rows = self._browser.elements_finder("order_grid")
            row = rows[1]
            div_list = row.find_elements_by_tag_name("div")
            order_id_col = div_list[0].find_element_by_tag_name("span")
            order_id_link = order_id_col.find_element_by_tag_name("a")
            order_id_link.click()
            self.action_ele.explicit_wait('process_button')
            self.action_ele.click_element('process_button')
            self.action_ele.click_element('close_yes')
        except:
            print("Failed to process order")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def check_add_user_error(self, params):
        '''
        `Description:` To check add user error

        `Param1:` params: user error: message

        `Returns:` status (True/False)

        `Created by:` Palla Surya Kumar
        '''
        status = False
        try:
            observed_title = self._browser.element_finder('Add_User_Request_Submitted_Title')
            if observed_title:
                # Prasanna: Added the second condition
                if observed_title.text() == params['add_user_error'] or \
                        "Error" in observed_title.text():

                    # Prasanna: Add the steps to check with another number
                    if params["assign_new_number"]:
                        # 1. click on the "OK" button of the error message
                        self.action_ele.click_element('fnMessageBox_OK')
                        # 2. click on the back button - go to the previous page (3 back buttons)
                        for i in range(3):
                            self.action_ele.explicit_wait('adduser_backbtn')
                            self.action_ele.click_element('adduser_backbtn')
                            time.sleep(2)

                        # 3. check with another phone number
                        index = params["assign_new_number"]
                        self.action_ele.explicit_wait('phone_Number')
                        self.action_ele.select_from_dropdown_using_index('phone_Number', index)
                        index += 1
                        while True:
                            self.action_ele.click_element('adduser_contactnextbutton')
                            errors = self._browser.elements_finder('user_errors')
                            for error in errors:
                                if "Extension is in use or not valid." in error.text:
                                    self.action_ele.select_from_dropdown_using_index('phone_Number', index)
                                    index += 1
                                    break
                            else:
                                break
                        # 4. Again call the function
                        status = self.add_user_confirm(params)

                    else:
                        # retrieve error message
                        order_error_msg = self.query_ele.get_text('Aa_edit_confirm')
                        print(order_error_msg)

                        # retrieve order number
                        order_number = order_error_msg.split('#')[-1].strip()
                        print(order_number)
                        self.action_ele.click_element('fnMessageBox_OK')

                        # switching to services page and activate all the services related to the order based on the order id
                        self.commonfunctionality.switch_page_services()
                        self.action_ele.explicit_wait('Service_search_box')
                        self.action_ele.input_text("Service_search_box", order_number)
                        status = self.account_handler.activate_all_service()

                        # switching to orders page and process the order
                        self.commonfunctionality.switch_page_order()
                        self.process_given_order(order_number)
                        # when observed_title is found and we fix that issue,which is pass case , so we make it true
                        status = True
        except:
            #when observed_title is not found it raises exception ,which is pass case , so we make it true
            status = True
            print("Failed to check add user error")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def add_user_confirm(self, params):
        '''
        `Description:` To confirm the add user operation

        `Param1:` params: request_by: The person who requested, request_source

        `Returns:` None

        `Created by:` Kenash K

        'Modified by' Palla Surya Kumar, Prasanna
        '''

        try:
            # making status true by default so that even if u do not pass add_user_error arg it will take care
            status = True
            #params['login_user'] = params.get('login_user', 'testuser')
            params = defaultdict(lambda: '', params)
            # Modified by: Prasanna
            # Modified by: Palla Surya Kumar
            # validating with login user because PM DM do not have request by attribute
            if str(params['login_user']).lower() in ('staff'):
                if params['request_by']:
                    SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                        'requestedBy', params['request_by'], loop_count=40)
                    #self.action_ele.select_from_dropdown_using_text('requestedBy', params['request_by'])
                else:
                    #self.action_ele.select_from_dropdown_using_index('requestedBy', 1)
                    SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                        'requestedBy', 1, loop_count=40)
                    #self.action_ele.select_from_dropdown_using_index("requestedBy", 1)
                if params['request_source']:
                    SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                        'requestSource', params['request_source'], loop_count=40)
                    #self.action_ele.select_from_dropdown_using_text('requestSource', params['request_source'])

                if params['request_source'] == 'Case':
                    self.action_ele.input_text('caseNumber', params['case_number'])
            self.action_ele.click_element('adduser_finish')
            self._browser.waitfor_ajax_complete()
            # using this parameter to handle the error occured
            # Pasanna: Added the extra check params["assign_new_number"]
            if params['add_user_error'] or params["assign_new_number"]:
                status = self.check_add_user_error(params)

            WIL(self.action_ele.explicit_wait, 'add_user_button1', loop_count=30)
            # WIL(self.action_ele.explicit_wait, 'add_user_button1')
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        except:
            print("Failed to complete user confirm")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_user(self, usermailid, role):
        '''
        `Description:` To verify the created user

        `Param:` params: usermailid: email id of user, role: role of user

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            user_role = {'Phone Manager': 'au_isPM', 'Decision Maker': 'au_isDM',
                         'Billing': 'au_isBC', 'Technical': 'au_isTC',
                         'Emergency': 'au_isEC'}
            status = False
            self._browser._browser.refresh()
            time.sleep(3)
            self.action_ele.explicit_wait('email_search')
            self.action_ele.input_text('email_search', usermailid)
            self.action_ele.explicit_wait(user_role[role])
            self.action_ele.select_checkbox(user_role[role])
            for i in range(5):
                try:
                    time.sleep(1)
                    self._browser._browser.refresh()
                    grid_load=self.action_ele.explicit_wait('user_wait_grid')
                    console("iteration number: %s" %i)
                    self._browser._browser.refresh()
                    if grid_load:
                        break
                except:
                    self._browser._browser.refresh()
                    pass
            time.sleep(3)
            #self._browser._browser.refresh()
            self.action_ele.explicit_wait(user_role[role])
            var = self.query_ele.text_present(usermailid)
            self.action_ele.unselect_checkbox(user_role[role])
            self.action_ele.clear_input_text('email_search')

            if usermailid in var:
                status = True
            return status
        except:
            print("Verify user failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def verify_user_profile(self, params, **options):
        """
        Verify the user profile
        :param params:  Dictionary contains phone information
        :param options:
        :return:
        """
        status = False
        ph_num = params['ap_phonenumber']
        for c in ['(', ')', ' ', '-', '+']: ph_num = ph_num.replace(c, "")
        time.sleep(3)
        self.action_ele.explicit_wait('headerRow_ProductName')
        self.action_ele.clear_input_text("service_headerRow_OrderId")
        self.action_ele.input_text('headerRow_BaseNameStripped', ph_num)
        self.action_ele.input_text('headerRow_ProductName', params['ap_phonetype'])
        self._browser._browser.refresh()
        time.sleep(3)  #Remove after demo
        self._browser._browser.refresh()
        var = self.query_ele.text_present(params['ap_phonetype'])
        if var:
            status = True
        WIL(self.action_ele.clear_input_text, "headerRow_BaseNameStripped")
        WIL(self.action_ele.clear_input_text, "headerRow_ProductName")
        return status

    def select_products_for_users_cosmo(self,params):
        """
        Select product for Cosmo User
        :param params:  Dictionary contains cosmo user information
        :return:
        """
        divFeatures = self._browser.elements_finder('divBundleLabels')
        labellist = [i.text for i in divFeatures]
        divInputs = self._browser.elements_finder('divBundleInputs')
        featureInputs = params['features_cosmo_bundle'].split(',')
        for featureInput in featureInputs:
            if featureInput in labellist:
                idx = labellist.index(featureInput)
                divInputs[idx].click()
        divFeatures = self._browser.elements_finder('divalacarteLabels')
        labellist = [i.text for i in divFeatures]
        divInputs = self._browser.elements_finder('divalacarteInputs')
        featureInputs = params['features_cosmo_alacarte'].split(',')
        for featureInput in featureInputs:
            if featureInput in labellist:
                idx = labellist.index(featureInput)
                divInputs[idx].click()

    def add_usergroup(self, params):
        """
        `Description:` Add 'User group' from Phone system

        `Param:` params: Dictionary contains User_group Info

        `Returns:` None

        `Created by:` Vasuja
         """
        try:
            self.action_ele.explicit_wait('userGroupGridnew_group_addButton')
            # self.action_ele.click_element('userGroupGridnew_group_addButton')
            WIL(self.action_ele.click_element, 'userGroupGridnew_group_addButton')
            self.action_ele.input_text('userGroup_Name', params['userGroupName'])
            self.action_ele.select_from_dropdown_using_text('UG_ProfileTypeId', params['profileType'])
            self.action_ele.select_from_dropdown_using_text('UG_HoldMusicId', params['holdMusic'])
            self.action_ele.click_element('UG_groupWizard_next')
            self.action_ele.select_checkbox('UG_AllowCallPickUp')
            self.action_ele.select_checkbox('UG_AllowOverheadPaging')
            self.action_ele.select_checkbox('UG_AllowHuntgroupStateChange')
            self.action_ele.select_checkbox('UG_AllowExtensionAssignment')
            self.action_ele.select_checkbox('UG_ShowCallerId')
            self.action_ele.select_checkbox('UG_ShowCallHistory')
            self.action_ele.select_checkbox('UG_AllowAvailabilityStateChange')
            self.action_ele.select_from_dropdown_using_text('UG_DirectedIntercom', params['directedIntercom'])
            self.action_ele.select_from_dropdown_using_text('UG_WhisperPage', params['whisperPage'])
            self.action_ele.select_from_dropdown_using_text('UG_Barge', params['Barge'])
            self.action_ele.select_from_dropdown_using_text('UG_SilentMonitor', params['silentMonitor'])
            self.action_ele.click_element('UG_groupWizard_next')
            self.action_ele.select_checkbox('UG_AllowVoicemailCallBack')
            self.action_ele.select_checkbox('UG_AllowBroadcastList')
            self.action_ele.select_checkbox('UG_AllowSystemList')
            self.action_ele.select_checkbox('UG_AllowDownloadWav')
            self.action_ele.click_element('UG_groupWizard_next')
            self.action_ele.select_from_dropdown_using_text('UG_ClassofService', params['classOfService'])
            self.action_ele.select_from_dropdown_using_text('UG_AccountCodeMode', params['accountCodeMode'])
            self.action_ele.click_element('UG_groupWizard_finish')

        except:
            console("Failed to add user group")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def assign_usergroup(self, params):
        """
        `Description:` Assign any user in User group

        `Param1:` user mail id

        `Param2:` user Group Name

        `Returns:` None

        `Created by:` Vasuja
         """
        try:
            self.action_ele.explicit_wait('email_search')
            self.action_ele.input_text('email_search', params['usermailid'])
            self.action_ele.click_element('User_phoneName')
            self.action_ele.click_element('User_UserGroup')
            self.action_ele.select_from_dropdown_using_text('User_UserGroup', params['userGroupName'])
            self.action_ele.click_element('User_UserGroup_submit')
        except Exception, e:
            print(e)
            console("Failed to assign user group")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def delete_usergroup(self, user_group_name):
        """
        `Description:` Delete user group from Phone System--> User groups

        `Param1:` user_group_name

        `Returns:` status - True/False

        `Created by:` Vasuja
         """
        try:
            status = False
            self.action_ele.explicit_wait('ug_headerRow_Name')
            self.action_ele.input_text('ug_headerRow_Name', user_group_name)
            if self.query_ele.get_text("ug_name_in_grid") == user_group_name:
                self.action_ele.click_element("ug_checkbox")
                self.action_ele.explicit_wait("ug_delete")
                time.sleep(1)
                self.action_ele.click_element("ug_delete")
                self.action_ele.explicit_wait("ug_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("ug_delete_yes")
                time.sleep(3)
                # ug_list = self._browser.elements_finder("ug_list")
                ug_list = WIL(self._browser.elements_finder, "ug_list", return_value=True, loop_count=40)
                if len(ug_list) == 0:
                    status = True
            self.action_ele.clear_input_text('ug_headerRow_Name')
        except Exception, e:
            print(e)
            print ("Failed to delete User group")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_mobility_checkbox(self, params):
        """
            `Description:` This Function will verify mobility checkbox for a global user if there is smr instance setup for selected country

            `Param:` params: Dictionary contains global user information

            `Returns:` status - True/False

            `Created by:` Megha Bansal
            """

        self.action_ele.explicit_wait('adduser_button')
        self.action_ele.click_element('adduser_button')
        self.add_contact_info(params)

        isDisplayed = self.query_ele.element_displayed("mobilityCheckbox")
        isEnable = self.query_ele.element_enabled("mobilityCheckbox")

        if isDisplayed and isEnable:
            return True
        else:
            return False

    def verify_swap_globaluser(self, params):
        """
        `Description:` This Function will verify swap is disabled for globaluser or not

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['username']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['username'])

        self.action_ele.right_click("gu_user_link")
        disabledList = self._browser.elements_finder("disabledoption")
        for item in disabledList:
            name_list = item.text
            if name_list == 'Swap':
                return False

        return True

    def get_locations_user_location_dropdown(self):
        """
        `Description:` This Function will verify the User Location dropdown while adding a global user

        `Param:` None

        `Returns: ` result - True/False

        `Created by:` Megha Bansal
        """
        # self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        WIL(self.action_ele.explicit_wait, "au_datagrid_usersDataGrid", loop_count=40)
        self.action_ele.click_element('adduser_button')
        # self.action_ele.explicit_wait("adduser_firstname")
        WIL(self.action_ele.explicit_wait, "adduser_firstname", loop_count=40)

        # userLocationList = self._browser.elements_finder('User_Location_dd')
        userLocationList = WIL(self._browser.elements_finder, 'User_Location_dd', return_value=True, loop_count=40)
        locList = []
        for i in userLocationList:
            locList.append(i.text)

        self.action_ele.click_element("adduser_cancel")
        time.sleep(1)
        # self.action_ele.explicit_wait("confirm_box")
        WIL(self.action_ele.explicit_wait, "confirm_box")
        self.action_ele.click_element("confirm_box")
        return locList

    def add_personal_address(self, params):
        """
        Function to add a new personal address to the user phone_settings page
        :param params: The address information
        :return: True / False
        :created By: Prasanna
        """
        status = False
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("personal_address")
            self.action_ele.click_element("personal_address")
            self.action_ele.explicit_wait("emergency_loc_next")
            self.action_ele.click_element("emergency_loc_next")
            self.action_ele.explicit_wait("select_address")
            if params["select_using_text"]:
                self.action_ele.select_from_dropdown_using_text("select_address", params["select_using_text"])
            else:
                self.action_ele.select_from_dropdown_using_index("select_address", params["select_using_index"])

            # Fill the address
            self.action_ele.explicit_wait("address_1")
            self.action_ele.input_text("address_1", params["Address_1"])
            if params["Address_2"]:
                self.action_ele.explicit_wait("address_2")
                self.action_ele.input_text("address_2", params["Address_2"])
            self.action_ele.explicit_wait("city")
            self.action_ele.input_text("city",params["City"])
            self.action_ele.explicit_wait("state")
            self.action_ele.select_from_dropdown_using_text("state", params["State"])
            self.action_ele.explicit_wait("zip_code")
            self.action_ele.input_text("zip_code",params["Zip"])
            status = True
        except Exception as e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def edit_emergency_location(self, params):
        """
        Function to edit the emegency location on user -> Phone_Settings page
        :param params: The values to edit the emergency location
        :return: True / False
        :Created By:  Prasanna
        """
        status = False
        try:
            time.sleep(2)
            # Click on "Emergency Location" button
            self.action_ele.explicit_wait("tab_emergency_loc")
            self.action_ele.click_element("tab_emergency_loc")

            self.action_ele.explicit_wait("button_change")
            self.action_ele.click_element("button_change")

            time.sleep(1)

            # Adding personal address
            if params["personal_address"]:
                status = self.add_personal_address(params)
                if not status:
                    raise Exception("Adding Personal address failed")
            elif params["company_address"]:
                pass

            self.action_ele.explicit_wait("emergency_loc_next")
            self.action_ele.click_element("emergency_loc_next")

            # Accept the change
            self.action_ele.explicit_wait("accept_address_change")
            self.action_ele.click_element("accept_address_change")

            # click Finish button
            self.action_ele.explicit_wait("emergency_location_update_finish")
            self.action_ele.click_element("emergency_location_update_finish")

            # Check if address validation error crops up
            status = True
        except Exception as e:
            print(e)
        return status

    def edit_user_phone_settings_page(self, params):
        """
        `Description:` To enable or edit user phone settings in user phone settings page

        `Param1:` user mail id

        `Params:` user Group Name/ Shared Call Appearance/ Video Conferencing  etc

        `Returns:` status - True/False

        `Created by:` Vasuja
        """
        try:
            status = False
            params = defaultdict(lambda: '', params)
            if params['user_email']:
                self.action_ele.input_text('email_search', params['user_email'])
                self.action_ele.explicit_wait('user_phone_settings_dm_pm')
                time.sleep(1)
                self.action_ele.click_element('user_phone_settings_dm_pm')
            if params['shared_call_appearance'] != "":
                verify_text = self.query_ele.text_present("Shared Call Appearance")
                if verify_text:
                    print("Shared Call Appearance tab is verified")
                else:
                    print("Shared Call Appearance tab is not verified")
                    raise AssertionError
                self.action_ele.click_element('User_SCA')
                if params['shared_call_appearance'] == "Enabled":
                    self.action_ele.select_from_dropdown_using_text('User_SCA', "Enabled")
                    self.action_ele.explicit_wait('User_SCA_submit')
                    time.sleep(1)
                    if params['extn'] != '' and params['extn'] != 'None':
                        self.action_ele.explicit_wait("User_Ph_Settings_Sca_Enable_Extn")
                        time.sleep(1)
                        self.action_ele.input_text("User_Ph_Settings_Sca_Enable_Extn", params["extn"])
                    elif params['extn'] == 'None':
                        self.action_ele.explicit_wait("User_Ph_Settings_Sca_Enable_Extn")
                        time.sleep(1)
                        self.action_ele.clear_input_text("User_Ph_Settings_Sca_Enable_Extn")
                        self.action_ele.click_element('User_SCA_submit')
                        WIL(self.action_ele.explicit_wait, 'fnMessageBox_OK')
                        time.sleep(1)
                        if params['error_message'] in self._browser._browser.page_source:
                            print("Error message (" + params['error_message'] + ") is verified on page")
                            WIL(self.action_ele.click_element, "fnMessageBox_OK")
                            status = True
                            return status
                    WIL(self.action_ele.click_element, 'User_SCA_submit')
                    WIL(self.action_ele.explicit_wait, 'fnMessageBox_OK')
                    time.sleep(1)
                    verify_text = self.query_ele.text_present(
                        "Warning: Enabling Shared Call Appearance will remove this user from all Hunt group memberships. Click OK to proceed")
                    if verify_text:
                        print("Expected message is verified")
                    else:
                        print("Expected message is not verified")
                        self.action_ele.click_element("fnMessageBox_OK")
                        raise AssertionError
                    time.sleep(1)
                    self.action_ele.click_element("fnMessageBox_OK")
                    if params['error_message']:
                        self.action_ele.explicit_wait('fnMessageBox_OK')
                        time.sleep(1)
                        if params['error_message'] in self._browser._browser.page_source:
                            print("Error message ("+params['error_message']+") is verified on page")
                            self.action_ele.click_element("fnMessageBox_OK")
                            status = True
                            return status
                elif params['shared_call_appearance'] == "Disabled":
                    self.action_ele.select_from_dropdown_using_text('User_SCA', "Disabled")
                    self.action_ele.explicit_wait('User_SCA_submit')
                    time.sleep(1)
                    self.action_ele.click_element('User_SCA_submit')
                # self.action_ele.explicit_wait('fnMessageBox_OK', 40)
                WIL(self.action_ele.explicit_wait, 'fnMessageBox_OK', loop_count=40)
                time.sleep(1)
                self.action_ele.click_element('fnMessageBox_OK')
                expected_option = self.query_ele.get_text('User_SCA')
                if params['shared_call_appearance'] == "Enabled":
                    if expected_option == "Enabled":
                        print("Shared Call Appearance is enabled")
                        status = True
                    else:
                        print("Shared Call Appearance is not enabled")
                        raise AssertionError
                if params['shared_call_appearance'] == "Disabled":
                    if expected_option == "Disabled":
                        print("Shared Call Appearance is disabled")
                        status = True
                    else:
                        print("Shared Call Appearance is not disabled")
                        raise AssertionError
            # Added By: Prasanna
            if params["emergency_location"]:
                status = self.edit_emergency_location(params)
            return status
        except Exception, e:
            print(e)
            print ("Failed to edit User phone settings")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def add_user_from_profiles_tab(self,params):
        '''
        `Description:` Add user from profiles tab.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - True/False,extn

        `Created by:` Palla Surya Kumar
        '''
        try:
            succes_message="Profile added"
            WIL(self.action_ele.click_element, 'profile_add_button', loop_count=40)
            self.action_ele.explicit_wait("profile_loc_drop_down",
                                          ec="text_to_be_present_in_element", msg_to_verify="Select Location")
            self._browser.waitfor_ajax_complete()
            # self.action_ele.select_from_dropdown_using_text('profile_loc_drop_down',params['profile_loc'])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'profile_loc_drop_down', params['profile_loc'], loop_count=40)
            self.action_ele.click_element('profile_phone_num_check_box')
            # self.action_ele.select_from_dropdown_using_text('profile_phone_num_loc_drop_down',params['profile_loc'])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'profile_phone_num_loc_drop_down', params['profile_loc'], loop_count=40)
            # self.action_ele.select_from_dropdown_using_index('profile_phone_num_drop_down',2)
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                'profile_phone_num_drop_down', 2, loop_count=40)
            self.action_ele.explicit_wait('profile_first_name_text_box')
            self.action_ele.input_text('profile_first_name_text_box',params['profile_firstname'])
            self.action_ele.input_text('profile_last_name_text_box',params['profile_lastname'])
            extn=self.query_ele.get_value('add_user_extension_input')
            self.action_ele.input_text('profile_email_text_box', params['profile_mail'])
            # self.action_ele.select_from_dropdown_using_text('profile_phone_type_drop_down',params['profile_phonetype'])
            SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                'profile_phone_type_drop_down', params['profile_phonetype'], loop_count=40)
            if bool(params['profile_activationdate']):
                if params['profile_activationdate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('profile_activation_date', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'profile_activation_date', params['profile_activationdate'])
            self.action_ele.click_element('profile_user_details_next_button')
            if params['request_by']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'profile_requestedBy', params['request_by'], loop_count=40)
                # self.action_ele.select_from_dropdown_using_text('profile_requestedBy', params['request_by'])
            if params['request_source']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'profile_requestSource', params['request_source'], loop_count=40)
                # self.action_ele.select_from_dropdown_using_text('profile_requestSource', params['request_source'])

            if params['request_source'] == 'Case':
                self.action_ele.input_text('profile_caseNumber', params['case_number'])
            self.action_ele.click_element('profile_user_confirm_button')
            self._browser.waitfor_ajax_complete()
            WIL(self.action_ele.explicit_wait, 'fnMessageBox_OK', loop_count=40)
            # self.action_ele.explicit_wait("fnMessageBox_OK")
            if succes_message in self.query_ele.get_text("Aa_edit_confirm"):
                WIL(self.action_ele.click_element, "fnMessageBox_OK", loop_count=40)
                self._browser._browser.refresh()
                status = True
        except Exception, e:
            print e
            print("Could not add user")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return extn,status

    def add_user_from_numbers_tab(self,params):
        '''
        `Description:` Add user from numbers tab.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - True/False,extn

        `Created by:` Palla Surya Kumar
        '''
        try:
            status = False
            time.sleep(2)
            self.action_ele.explicit_wait('PrimaryPartitionPhoneNumber')
            # Prasanna: Added WIL
            WIL(self.action_ele.clear_input_text, 'PrimaryPartitionPhoneNumber')
            WIL(self.action_ele.input_text, 'PrimaryPartitionPhoneNumber', params['ph_number'])

            time.sleep(2)
            ph_numbers_grid = self._browser.element_finder("numbers_page_grid")
            if not ph_numbers_grid:
                raise Exception("No grid elements selected in the Grid")
            time.sleep(2)
            t_sec = 0
            for i in range(5):
                t_sec = t_sec + 5
                # Prasanna: Changed from find elements to element
                row = ph_numbers_grid.find_element_by_tag_name("div")
                if row:
                    break
                time.sleep(t_sec)
            else:
                raise Exception("No Row selected in the Grid")

            fields = row.find_elements_by_tag_name("div")
            if not fields:
                raise Exception("No element selected!")

            ph_num = fields[1].text
            fields[0].click()

            succes_message="The number "+ph_num+" was assigned"

            self.action_ele.explicit_wait('num_page_assign_button')
            self.action_ele.click_element('num_page_assign_button')
            WIL(self.action_ele.input_text,"ac_ER_firstName", params['profile_firstname'])
            self.action_ele.input_text('ac_ER_LastName',params['profile_lastname'])
            self.action_ele.input_text('numbers_page_email_text_box', params['profile_mail'])
            self.action_ele.explicit_wait("numbers_page_loc_drop_down",
                                          ec="text_to_be_present_in_element", msg_to_verify="Select Location")
            self.action_ele.select_from_dropdown_using_text('numbers_page_loc_drop_down',params['profile_loc'])
            self.action_ele.select_from_dropdown_using_text('profile_phone_type_drop_down', params['profile_phonetype'])
            extn=self.query_ele.get_value('num_page_add_user_extension_input')

            if bool(params['profile_activationdate']):
                if params['profile_activationdate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('numbers_page_activation_date', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'numbers_page_activation_date', params['profile_activationdate'])

            if params['request_by']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'ac_requested_by', params['request_by'])

                # self.action_ele.select_from_dropdown_using_text('ac_requested_by', params['request_by'])

            if params['request_source']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'requestSource_num_tab', params['request_source'])

                # self.action_ele.select_from_dropdown_using_text('requestSource', params['request_source'])

            if params['request_source'] == 'Case':
                self.action_ele.input_text('ac_case_number', params['case_number'])
            self.action_ele.click_element('num_page_add_user_OK')
            self._browser.waitfor_ajax_complete()
            WIL(self.action_ele.explicit_wait, "fnMessageBox_OK")
            if succes_message in self.query_ele.get_text("Aa_edit_confirm"):
                WIL(self.action_ele.click_element, "fnMessageBox_OK")
                self._browser._browser.refresh()
                status = True
            else:
                WIL(self.action_ele.click_element, "fnMessageBox_OK")
                self.action_ele.click_element("num_page_add_user_Cancel")

        except Exception, e:
            print e
            print("Could not assign number to user")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return extn, status

    def verify_user_created_from_profiles_page(self,params):
        '''
        `Description:` Verify user created from profiles tab.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - True/False

        `Created by:` Palla Surya Kumar
        '''
        try:
            status=False
            self.action_ele.explicit_wait('user_search_email')
            # self.action_ele.clear_input_text('user_search_email')
            WIL(self.action_ele.clear_input_text, 'user_search_email')
            self.action_ele.input_text('user_search_email',params['profile_mail'])
            email_field=self._browser.element_finder('user_mail')
            seen_mail=email_field.text
            if seen_mail==params['profile_mail']:
                status=True
        except Exception, e:
            print e
            print("Could not verify user created from profiles page!!")
        return status

    def assign_profile_to_contact_with_no_profile(self,params):
        '''
        `Description:` This function will assign profile to contact with no profile.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - phone_num,extn

        `Created by:` Palla Surya Kumar
        '''
        try:
            time.sleep(2)
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait('email_search', 300)
            self.action_ele.input_text('email_search',params['au_businessmail'])
            users_grid = self._browser.element_finder("Grid_Canvas")
            if not users_grid:
                raise Exception("No grid elements selected in the Grid")

            t_sec = 0
            for i in range(5):
                t_sec = t_sec + 5
                rows = users_grid.find_elements_by_tag_name("div")
                if rows:
                    break
                time.sleep(t_sec)
            else:
                raise Exception("No Row selected in the Grid")

            fields = rows[0].find_elements_by_tag_name("div")
            if not fields:
                raise Exception("No element selected!")

            if params['user_role']=='PM' or params['user_role']=='DM':
                service_phone_url = fields[1].text
            if params['user_role']=='Staff':
                service_phone_url = fields[2].text

            if service_phone_url=='Unassigned':
                if params['user_role']=='PM' or params['user_role']=='DM':
                    url=fields[1].find_elements_by_tag_name("a")
                elif params['user_role'] == 'Staff':
                    url = fields[2].find_elements_by_tag_name("a")
                url[0].click()
            else:
                raise Exception("Clicking of service_phone_url is not working.")

            time.sleep(2)
            self.action_ele.explicit_wait("adduser_userLocation",
                                          ec="text_to_be_present_in_element", msg_to_verify="Select..")
            self.action_ele.select_from_dropdown_using_text('adduser_userLocation', params['au_userlocation'])
            self.action_ele.click_element('adduser_contactnextbutton')

            phone_num=''
            extn=''
            self.action_ele.select_from_dropdown_using_text('phone_Type', params['ap_phonetype'])

            if bool(params['ap_phonenumber']):
                if params['ap_phonetype'] != 'MiCloud Connect Voicemail Only':
                    self.hw_info = True
                else:
                    self.hw_info = False
                if params['ap_phonenumber'] == "random":
                    self.action_ele.select_from_dropdown_using_index('phone_Number',1)
                    phone_num = self.query_ele.get_text_of_selected_dropdown_option('phone_Number')
                else:
                    self.action_ele.select_from_dropdown_using_text('phone_Number', params['ap_phonenumber'])

                if not params['ap_extn']:
                    extn = self.query_ele.get_value('Person_Profile_Extension')
                else:
                    extn = params['ap_extn']

            if bool(params['ap_activationdate']):
                if params['ap_activationdate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('activationDate', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'activationDate', params['ap_activationdate'])

            self.action_ele.click_element("user_label")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element('adduser_contactnextbutton')
            errors = self._browser.elements_finder('user_errors')
            for error in errors:
                if "Extension is in use or not valid." in error.text:
                    extn = error.text.split(':')[-1].strip()
                    self.action_ele.input_text('Person_Profile_Extension', extn)
                    self.action_ele.click_element('adduser_contactnextbutton')
                    break
            # clicking next in hardware page
            self.action_ele.click_element('adduser_contactnextbutton')

            if params['request_by']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'requestedBy', params['request_by'])

                # self.action_ele.select_from_dropdown_using_text('requestedBy', params['request_by'])

            if params['request_source']:
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'requestSource', params['request_source'])
                # self.action_ele.select_from_dropdown_using_text('requestSource', params['request_source'])

            if params['request_source'] == 'Case':
                self.action_ele.input_text('caseNumber', params['case_number'])
            self.action_ele.click_element('adduser_finish')
            self.action_ele.explicit_wait('add_user_button1')
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        except:
            raise AssertionError("Could not assign profile to the contact!!")
        return phone_num,extn

    def verify_GU_products_swap(self, params):
        """
        `Description:` This Function will verify Global Users products for swap

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['username']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['username'])

        self.action_ele.right_click("gu_user_link")

        context_menu_items = self._browser.elements_finder("close_user_context_menu")
        for menu_items in range(len(context_menu_items)):
            if context_menu_items[menu_items].text.lower() == "Swap".lower():
                context_menu_items[menu_items].click()
                self.action_ele.explicit_wait('swap_productType')
                selectionlist = self._browser.element_finder('swap_productType')
                for option in selectionlist.find_elements_by_tag_name('option'):
                    if option.text in ['MiCloud Connect Elite','MiCloud Connect Premier','MiCloud Connect Essentials']:
                        continue
                    else:
                        return False

                return True


        return False

    def swap_global_user(self, params):
        """
        `Description:` This Function will swap Global User

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        # self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        WIL(self.action_ele.explicit_wait, "au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['username']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['username'])

        # self.action_ele.right_click("gu_user_link")
        WIL(self.action_ele.right_click, "gu_user_link")
        # context_menu_items = self._browser.elements_finder("close_user_context_menu")
        context_menu_items = WIL(self._browser.elements_finder, "close_user_context_menu", return_value=True, loop_count=20)
        for menu_items in range(len(context_menu_items)):
            if context_menu_items[menu_items].text.lower() == "Swap".lower():
                context_menu_items[menu_items].click()
                self.action_ele.explicit_wait('swap_productType')
                # self.action_ele.select_from_dropdown_using_index('swap_productType',1)
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_index,
                    'swap_productType', 1)
                self.action_ele.click_element('Swap_next')
                # self.action_ele.select_from_dropdown_using_index('requestedBy',1)
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'requestedBy', params['requested_by'])
                # self.action_ele.select_from_dropdown_using_index('requestSource',2)
                SFD(self.query_ele.get_text_list_from_dropdown, self.action_ele.select_from_dropdown_using_text,
                    'requestSource', params['request_source'])
                self.action_ele.click_element('Swap_finish')

                for i in range(self.counter):
                    if "Processing, please wait.." in self._browser._browser.page_source:
                        time.sleep(1)
                    else:
                        # isDisplayed = self.query_ele.element_displayed("OK_button")
                        isDisplayed = WIL(self.query_ele.element_displayed, "OK_button", return_value=True, loop_count=20)
                        if isDisplayed:
                            verify_success = self.query_ele.text_present("Order has been created")
                            if verify_success == False:
                                return verify_success
                            else:
                                self.action_ele.click_element("OK_button")
                                return True
        return True
		
    def edit_profiles(self, params):
        """
        The function edits the user profile
        :param params: profile related information
        :return: True/ False
        :Created by: Prasanna
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.input_text('email', params['email'])
            grid = self._browser.element_finder('user_grid')
            if not grid:
                raise Exception("user grid not available")
            row = grid.find_element_by_tag_name("div")
            if not row:
                raise Exception("No rows selected for the given email")
            fields = row.find_elements_by_tag_name("div")
            if not fields:
                raise Exception("No fields selected for the given row")
            fields[0].click()

            if params.get('extension', None):
                WIL(self.action_ele.click_element, 'edit')
                WIL(self.action_ele.click_element, 'extension')
                self.action_ele.input_text('extension_input', params['extension'])
                self.action_ele.click_element('extension_submit')
            for i in range(5):
                try:
                    WIL(self.wait, "fnMessage_box_ok")
                    element = self._browser.element_finder("extension_submit_error")
                    if not element:
                        element = self._browser.element_finder("extension_submit_error_message")
                        text = element.text
                        extension = text[-5:-1]
                        self.action_ele.input_text('extension_input', extension)
                        self.action_ele.click_element('extension_submit')
                except Exception as e:
                    print(e)
                    break

            return True

        except Exception as e:
            print(e)
            return False

    def get_first_dm_user_info(self, params):
        """
        The function retrieves the information about the first DM user placed in the User slick grid
        :param params: to retrieve the first DM user info
        :return:
        :Created By:  Prasanna
        """
        try:
            # list all DM users
            self.action_ele.explicit_wait("au_isDM")
            self.action_ele.click_element("au_isDM")
            time.sleep(2)
            # get the first DM user from grid-canvas
            dm_user_grid = self._browser.element_finder("User_Grid_Canvas")
            if not dm_user_grid:
                raise Exception("No user-grid")
            first_dm_user = dm_user_grid.find_element_by_tag_name("div")
            if not first_dm_user:
                raise Exception("user not present in grid")
            record_fields = first_dm_user.find_elements_by_tag_name("div")
            if not record_fields:
                raise Exception("Fields not found")
            # get the DM user's email
            params.update({'email': record_fields[5].find_element_by_tag_name("span").get_attribute('data')})

            # click on phone settings link and get the profile id
            (record_fields[2].find_element_by_tag_name("a")).click()

            # get the Profile Id from the browser url
            profile_id = (self._browser._browser.current_url).split("profileId=")[1]
            params.update({'profileId': profile_id})

        except Exception as e:
            print(e)
            return False
        return True

    def edit_user_personal_information(self, params):
        """
        The function edits the user personal information
        :param params: profile related information
        :return: True/ False
        :Created by: Priyanka
        """
        status=False
        try:
            params = defaultdict(lambda: '', params)
            if params['au_firstname']:
                self.action_ele.click_element("pi_tab_contact_firstName")
                self.action_ele.input_text('pi_tab_contact_firstName_input', params['au_firstname'])
                time.sleep(1)
                self.action_ele.click_element('pi_tab_contact_firstName_submit')
                time.sleep(1)
            if params['au_lastname']:
                self.action_ele.click_element("pi_tab_contact_lastName")
                self.action_ele.input_text('pi_tab_contact_lastName_input', params['au_lastname'])
                time.sleep(1)
                self.action_ele.click_element('pi_tab_contact_lastName_submit')
                time.sleep(1)
            if params['au_businessmail']:
                self.action_ele.click_element("pi_tab_contact_businessEmail")
                self.action_ele.input_text('pi_tab_contact_businessEmail_input', params['au_businessmail'])
                time.sleep(1)
                self.action_ele.click_element('pi_tab_contact_businessEmail_submit')
                time.sleep(1)
            if params['au_personalmail']:
                self.action_ele.click_element("pi_tab_contact_personalEmail")
                self.action_ele.input_text('pi_tab_contact_personalEmail_input', params['au_personalmail'])
                time.sleep(1)
                self.action_ele.click_element('pi_tab_contact_personalEmail_submit')
                time.sleep(1)
            if params['au_username']:
                self.action_ele.click_element("pi_tab_contact_username")
                self.action_ele.input_text('pi_tab_contact_username_input', params['au_username'])
                time.sleep(1)
                self.action_ele.click_element('pi_tab_contact_username_submit')
                time.sleep(1)
            status=True
        except Exception as e:
            print(e)
        return status

