"""Module for BOSS portal functionalities
   Author: Kenash Kanakaraj
"""
import os
import sys
import time

import stafenv

#from base import LocalBrowser
#import web_wrappers.selenium_wrappers as base
from web_wrappers.selenium_wrappers import LocalBrowser
from page.BOSSComponent import BossPage
from mapMgr import mapMgr

#BOSS feature component files
from AOBComponent import AOBComponent as aob
from VCFEComponent import VCFEComponent as vcfe
from BcaComponent import BcaComponent as Bca
from ECCComponent import ECCComponent as ecc
from UserComponent import UserComponent as user
from ServiceComponent import ServiceComponent as service
from InstanceComponent import InstanceComponent as instance
from std2.std2component import Std2Component as st_d2
from Dominator import Dominator as dominator

_DEFAULT_TIMEOUT = 3

GLOBAL_AUTH_FLAG = True    # The flag to log in using global auth portal

class BossComponent( aob, vcfe, Bca, ecc, user, service, instance, st_d2, dominator):
    ''' BOSS Component Interface to interact with the ROBOT keywords
    '''

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, **params):
        self.browsertype = params.get('browser', 'chrome').lower()
        self.location = params.get('country', 'US').lower()
        self._browser = LocalBrowser(self.browsertype)
        browser_obj = self._browser.get_current_browser()
        browser_obj.maximize_window()
        self._browser.location = self.location
        self.boss_page = BossPage(self._browser)
        mapMgr.create_maplist("BossComponent")
        self.mapDict = mapMgr.getMapDict()

        # initializing the entire STD2 components
        st_d2.__init__(self, self._browser)

    def close_and_reopen_browser(self):
        # self._browser.reset_browser()
        self._browser.quit()
        time.sleep(2)
        # open a new browser
        self._browser = LocalBrowser(self.browsertype)
        self._browser.get_current_browser().maximize_window()
        self.boss_page = BossPage(self._browser)

    def open_url(self,url):
        """
        `Description:` This function is used to open BOSS portal page

        `:param1` url: URL of boss page

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.open_url(url)
        except Exception,e:
            print(e)

    def reset_password_from_home_page(self,email):
        """
        `Description:` This Function will try to reset password from Home page. By Sending link to Email

        `:param1` email: Email address

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.reset_password_from_home_page(email)
            #return current_time
        except:
            raise AssertionError("Reset password Va email has failed")

    def switch_page_switch_account(self):
        """
        `Description:` This Function will switch to account page.

        `:param1` None

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.switch_page_switch_account()
        except:
            raise AssertionError("Failed to Switch Account")

    def client_login(self, **params):
        """
        `Description:` Login to the BOSS portal using the username and password

        `:param1` username: URL

        `:param2` username: User email address

        `:param3` password: user password

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.open_url(params["URL"])

            if GLOBAL_AUTH_FLAG:
                self.boss_page.commonfunctionality.client_login(params["username"],
                                                                params["password"],
                                                                global_auth=True)
            else:
                self.boss_page.commonfunctionality.client_login(params["username"],
                                                                params["password"])
            print("DEBUG: Login successful")
        except:
            raise AssertionError("Login Failed!!")

    def switch_page(self, **params):
        """
        `Description:` Switch page using the account link on the top of the page

        `:param` params: name of the page which need to be switch

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            print("IN MAIN:")
            if params.keys():
                self.boss_page.commonfunctionality.switch_page(**params)
            else:
                print("Please check that the input parameters have been provided",
                        self.switch_page.__doc__)
        except:
            raise AssertionError("Page Switch Failed!!")

    def verify_page(self, **params):
        """
        `Description:` Verify if the expected string is available on the page

        `:param1` page- Page identifier

        `:param2` exp_content- Text in the identifier

        `:return:` status - True if comtent is found on the page else False

        `Created by:` Kenash K
        """
        try:
            time.sleep(_DEFAULT_TIMEOUT)
            status = False
            if params.keys():
                status = self.boss_page.commonfunctionality.verify_text(params["page"],
                                                                        params["exp_content"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_page.__doc__)
            return status
        except:
            raise AssertionError("Page Verification Failed!!")

    def verify_user(self, **params):
        '''
        `Description:` Verify that the user is available in the user table

        `:param1` Business Email

        `:param2` Role

        `:return:` status - True if user is found on the page else False

        `Created by:` Kenash K
        '''
        try:

            status = False
            if params.keys():
                status = self.boss_page.user_handler.verify_user(params["au_businessmail"],
                                                                 params["role"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_user.__doc__)
            return status
        except:
            raise AssertionError("User verification Failed!!")

    def verify_contract_state(self, **params):
        '''
        `Description:` Verify the contract state

        `Param1:` params: accountName: Name of account

        `Param2:` params: exp_state: State of account

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.account_handler.verify_contract_state(
                    params["account_name"], params["exp_state"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_contract_state.__doc__)
            return status
        except:
            raise AssertionError("Contarct state verification Failed!!")

    def switch_link_in_partition(self, **params):
        '''
        `Description:` This function will switch partition link

        `Param1:` Partition Name

        `Param2:` Link to Switch

        `Returns:` None

        `Created by:` rdoshi
        '''
        try:
            print("Switch to link in partition")
            if params.keys():
                self.boss_page.commonfunctionality.switch_link_in_partition(params['switch_link'],
                                                                            params['partition'])
            else:
                print("Switch failed")
        except:
            raise AssertionError("Switch to link partition failed!!")

    def switch_account(self, **params):
        """
        `Description:` Switch account using the account link on the top of the page

        `Param:` params: Dictionary with account information

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.commonfunctionality.switch_account(params['newacc'], params['seloption'])
            else:
                print("Please check that the input parameters have been provided",
                        self.switch_account.__doc__)
        except:
            raise AssertionError("Switch Account Failed!!")

    def add_contract(self, **params):
        '''
        `Description:` This Function will create contact

        `Param:` params: Dictionary with contract information

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.account_handler.add_contract(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_contract.__doc__)
                status = False
            return status
        except:
            raise AssertionError("Add contract Failed!!")

    def add_phonenumber(self, **params):
        '''
        `Description:` This function will add phone numbers to BOSS portal

        `Param:` params: Dictionary with phone number information

        `Returns:` None

        `Created by:` Vasuja K

        `Modified by :` Kenash K
        '''
        try:
            if params.keys():
                self.boss_page.phone_number.add_phonenumber(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("Add Phone number Failed!!")

    def add_user(self, **params):
        '''
        `Description:` This Function will create user in portal

        `Param:` params: Dictionary with user information

        `Returns:` phone_num, extn

        `Created by:` Kenash K

        'Modified By:' Palla Surya Kumar
        '''
        try:
            if params.keys():
                #'Modified By:' Palla Surya Kumar
                # using status to handle the error occured, so added it
                phone_num, extn, status=self.boss_page.user_handler.add_user(params)
                return phone_num, extn, status
            else:
                print("Please check that the input parameters have been provided",
                        self.add_user.__doc__)
        except:
            raise AssertionError("Add user Failed!!")

    def update_phonestate(self, **params):
        '''
        `Description:` This Function will update phone state to available

        `Param:` params: Dict with phone information

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            if params.keys():
                self.boss_page.phone_number.update_phonenumbers(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("update phone state Failed!!")

    def verify_phone_state(self, **params):
        '''
        `Description:` This function will verify phone update

        `Param:` params: Dictionary with phone state

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.phone_number.verify_phonenumbers(params)
                return status
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("verify phone state Failed!!")

    def set_location_as_site(self):
        '''
        `Description:` This function will set the location as Site

        `Param:` None

        `Returns:` None

        `Created by:` Vasuja K
        '''
        try:
            self.boss_page.account_handler.set_location_as_site()

        except:
            print("Please check that the input parameters have been provided",
                    self.set_location_as_site.__doc__)
            raise AssertionError("Set location as site Failed!!")

    def click_link_in_grid(self, **params):
        '''
        `Description:` This function will click link in GRID

        `Param1:` Grid ID

        `Param2:` Link

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            self.boss_page.commonfunctionality.click_link_in_grid(params['grid'], params['link'])
        except:
            print("Could not access link", self.click_link_in_grid.__doc__)
            raise AssertionError("Click operation Failed!!")

    def add_instance(self, **params):
        '''
        `Description:` This Function will add instance

        `Param1:` Instance Name

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            self.boss_page.account_handler.add_instance(params['instance_name'])
        except:
            print("Could not access link", self.add_instance.__doc__)
            raise AssertionError("Add instance Failed!!")

    def confirm_contract(self, **params):
        '''
        `Description:` This function will confirm contract.

        `Param:` params: Instance Name , Location

        `Returns:` order_number

        `Created by:` Kenash K
        '''
        try:
            order_number = self.boss_page.account_handler.confirm_contract(params['instance'], params['location'])
            return order_number
        except:
            print("Could not access link", self.confirm_contract.__doc__)
            raise AssertionError("Confirm contract Failed!!")

    def select_option(self, **params):
        '''
        `Description:` Select perticular option

        `Param1:` Option

        `Param2:` Element

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            self.boss_page.commonfunctionality.select_option(params['option'], params['element'])
        except:
            print("Could not access link", self.select_option.__doc__)
            raise AssertionError("Selection Failed!!")

    def add_partition(self, **params):
        '''
        `Description:` add a primary partition to a newly created account

        `Param:` params: Dictionary contains partition info

        `Returns:` None

        `Created by:` rdoshi
        '''
        try:
            if params.keys():
                self.boss_page.add_partition.add_partition(params)
                #verifying the created partition

            else:
                print("Please check if input params have been provided")
        except:
            raise AssertionError("Add partition Failed!!")

    def verify_partition(self, **params):
        '''
        `Description:` This Function will verify the partition has been created or not

        `Param:` params: Dictionary contains partition info

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        '''
        try:
            if params.keys():
                status = self.boss_page.add_partition.verify_partition(params["partitionName"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_partition.__doc__)
            return status
        except:
            raise AssertionError("Verify parition Failed!!")

    def enter_contact_name(self, **params):
        """
        `Description:` This function will enter contract name

        `Param1:` contact_name

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.commonfunctionality.search_user(params['contact_name'])
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Enter contact name Failed!!")

    def verify_grid_value(self, **params):
        """
        `Description:` This function will verify the grid value.

        `Param1:` gridvalue: values of grid

        `Returns:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status = False
            if params.keys():
                status = self.boss_page.commonfunctionality.verify_grid_value(
                    params['gridvalue'])
            else:
                print("Please check that the input parameters have been provided")
            return status
        except:
            raise AssertionError("Grid verification Failed!!")


    def move_to_tab(self, **params):
        """
        `Description:` This function will help to switch to tabs

        `Param1:` tab_name

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.commonfunctionality.move_to_tab(params['tab_name'])
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Move to tab Failed!!")

    def verify_tabs_exist(self, *params):
        """
        `Description:` This function will verify the tab is exist or not

        `Param1:` tab_list: list of all tabs

        `Returns:` True or False

        `Created by:` Kenash K
        """
        try:
            status = False
            if len(params):
                status = self.boss_page.commonfunctionality.verify_tabs(params)
            else:
                print("Please check that the input parameters have been provided")
            return status
        except:
            raise AssertionError("Verification tab Failed!!")

    def verify_loc_status(self, **params):
        '''
       `Description:` This function will verify Emergency registration status of location

        `Param1:` Loc_name

        `Param2:` exp_state

        `Returns:` status - True/False

        `Created by:` Vasuja
        '''
        try:
            result=self.boss_page.VCFE_Handler.verify_loc_status(params)
            return result

        except:
            print("Please check that the input parameters have been provided",
                    self.verify_loc_status.__doc__)
            raise AssertionError("Location status verification Failed!!")

    def create_invoice_group(self, **params):
        '''
        `Description:` This function will create the invoice group.

        `Param:` params: Dictionary contains  invoice group Info

        `Returns:` None

        `Created by:` Vasuja
        '''
        try:
            self.boss_page.Invoices_Payments.create_invoice_group(params)
        except:
            print("Please check that the input parameters have been provided",
                    self.create_invoice_group.__doc__)
            raise AssertionError("Invoice group creation Failed!!")

    def verify_invoice_group_location(self, **params):
        '''
        `Description:` To verify the invoice group location is being created

        `Param:` Location to verify

        `Returns:` None

        `Created by:` Vasuja
        '''
        try:
            status = self.boss_page.Invoices_Payments.verify_invoice_group_location(params)
            return status
        except:
            print("Please check that the input parameters have been provided",
                    self.verify_invoice_group_location.__doc__)
            e.args += ("Please check that the input parameters have been provided",)
            raise

    def verify_user_profile(self, **params):
        '''
        `Description:` this function verify user profile

        `Param:` params:  Dictionary contains phone information

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.user_handler.verify_user_profile(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_user_profile.__doc__)
            return status
        except:
            raise AssertionError("verification user profile Failed!!")

    def accept_agreement(self):
        """
        `Description:` This function will accept agreement.

        `Param:` None

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.accept_agreement()

        except:
            print("Could not accept agreement")
            raise AssertionError("Accept agreement Failed!!")

    def log_off(self):
        """
        `Description:` This function will perform log off operation

        `Param:` None

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.log_off()
        except:
            # raise AssertionError("Log Off Failed!!")
            # Close the browser and open another
            self.close_and_reopen_browser()


    def right_click(self, name):
        """
        `Description:` perform right click operation on elments and redirect to change password field

        `:param` name: First Name last Name

        `:return:` None

        `Created by:` Saurabh Singh
        """
        try:

            self.boss_page.commonfunctionality.right_click(name)
        except Exception,e:
            print(e)
            raise AssertionError("Right click failed !!")


    def change_profile_password_from_user_page(self,name):
        """
        `Description:` redirect user to change password setting page from inside user detail page

        `:param` name: First Name last Name

        `:return:` result - True/False

        `Created by:` Saurabh Singh
        """
        try:
            result = self.boss_page.commonfunctionality.change_profile_password_from_user_page(name)
            return result
        except Exception,e:
            print("Reached Exception"+e)
            raise

    def get_build(self):
        """
        `Description:` This function will get the build of BOSS portal

        `:param` None

        `:return:` None

        `Created by:` Saurabh Singh
        """
        self.boss_page.commonfunctionality.get_build()

    def close_user(self, **params):
        """
        `Description:` This Test case will close the User from the page with and without phone number user

        `:param` email: email of user who is going to close

        `:param` name: name of requester

        `:return:` result - True/False

        `Created by:` Saurabh Singh
        `Modified by:` Megha Bansal
        """
        try:
            # print("From Boss: "+email)
            result = self.boss_page.commonfunctionality.close_user(**params)
            return result
            # print("Validation of result"+str(result))
        except Exception, e:
            print(e)
            return False

    def change_password(self, **params):
        """
        `Description:`  This function will change the password

        `:param1` new_password: new password which need to be set

        `:param2` old_pwd: old password of user

        `:param` options:

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            old_pass = params.get('oldpassword', '')
            self.boss_page.commonfunctionality.change_password(params["newpassword"],
                                                               old_pass)

        except:
            print("Could not accept agreement")
            raise AssertionError("Change password Failed!!")

    def update_password(self, **params):
        """
        `Description:`  This function will update the password

        `:param1` new_password: new password which need to be set

        `:param2` old_pwd: old password of user

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            old_pass = params.get('oldpassword', '')
            self.boss_page.commonfunctionality.update_password(params["newpassword"],
                                                               params["oldpassword"])

        except:
            raise AssertionError("Update password failed Failed!!")

    def close_the_browser(self, **params):
        """
        `Description:` Close the browser object

        `:param` driver: WebDriver object

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            time.sleep(2)
            self.boss_page.commonfunctionality.close_browser()
        except:
            raise AssertionError("Close browser Failed!!")

    def add_prog_button(self, **params):
        """
        `Description:` For adding program buttons

        `:param` params:  Dictionary contains programmable button information

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.prog_button_handler.add_programmable_buttons(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_programmable_buttons.__doc__)
        except Exception, e:
            print e
            raise AssertionError("Add programable button Failed!!")

    def switch_prog_button(self, email):

        try:
            if email:
                self.boss_page.prog_button_handler.switch_programmable_buttons(email)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_programmable_buttons.__doc__)
        except Exception, e:
            print e
            raise AssertionError("Switch programable button Failed!!")

    def add_prog_button_bca(self, **params):
        """
        `Description:` For adding program buttons

        `:param` params:  Dictionary contains programmable button information

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.prog_button_handler.add_programmable_buttons_bca(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_programmable_buttons.__doc__)
        except Exception, e:
            print e
            raise AssertionError("Add programable button Failed!!")

    def add_prog_button_sca(self, **params):
        """
        `Description:` For adding program buttons

        `:param` params:  Dictionary contains programmable button information

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.prog_button_handler.add_programmable_buttons_sca(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_programmable_buttons.__doc__)
        except Exception, e:
            print e
            raise AssertionError("Add programable button Failed!!")

    def remove_prog_button(self, **params):
        """
        `Description:` For adding program buttons

        `:param` params:  Dictionary contains programmable button information

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.prog_button_handler.remove_programmable_buttons(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_programmable_buttons.__doc__)
        except Exception, e:
            print e
            raise AssertionError("Add programable button Failed!!")

    def close_open_order(self, Location):
        """
        `Description:` Close open order which create at the time of geo location created

        `:param1:` Location name

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status= self.boss_page.commonfunctionality.close_open_order(Location)
            return status
        except Exception,e:
            print e
            raise AssertionError("Closing Order Failed!!")

    def close_location(self, Location, name):
        """
        `Description:` Close the Geo location

        `:param1:` Location name

        `:param2:` requester name

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status=self.boss_page.commonfunctionality.close_location(Location, name)
            return status
        except Exception,e:
            print e
            raise AssertionError("Closing Location Failed!!")

    def update_geo_location(self, **params):
        """
            `Description:` update the Geo location

            `:param1:` Location name

            `:return:` status - True/False

            `Created by:` Priyanka M
        """
        try:
            status = self.boss_page.commonfunctionality.update_geo_location(params)
            return status
        except Exception, e:
            print e
            raise AssertionError("Closing Location Failed!!")



    def reset_password_via_email(self, **params):
        """
        `Description:` reset password from email

        `:param` user_email: whom password will be reset

        `:param` emailPassword: email password

        `:param` emailServer: email server

        `:param` setPassword: what password need to be set

        `:return:` status

        `Created by:` Saurabh Singh
        """
        try:
            status=self.boss_page.commonfunctionality.reset_password_via_email(params["emailToReset"], params["emailPassword"],params["emailServer"],params["setPassword"])
            return status
        except Exception, e:
            print(e)
            raise AssertionError("Password Reset via email Failed!!")

    def check_email(self,FROM_EMAIL,fromAdd):
        """
        `Description:` check the email time of latest email

        `:param` fromAdd: sender name

        `:param` user_email: user email

        `:param` emailPassword: email password

        `:param` emailServer: email server

        `:return:` None

        `Created by:` Saurabh Singh
        """
        try:
            self.boss_page.commonfunctionality.check_email(FROM_EMAIL, fromAdd)
        except Exception,e:
            print e
            raise AssertionError("Email Check has been Failed!!")

    def check_alert(self):
        """
        `Description:` Check for alert pop up on page

        `:return:`

        `Created by`  Saurabh Singh
        """
        try:
            self.boss_page.commonfunctionality.check_alert()
        except Exception, e:
            print e

    def switch_page_personal_information(self):
        """
        `Description:` switch to personal information page

        `:param:` None

        `:return:` result - True/False

        `Created by:` Kenash K
        """
        try:
            result = self.boss_page.commonfunctionality.switch_page_personal_information()
            return result
        except Exception,e:
            print e
            raise AssertionError("Switch is  Failed!!")

    def switch_page_primary_partition(self):

        try:
            result = self.boss_page.commonfunctionality.switch_page_primary_partition()
            return result
        except Exception,e:
            print(e)
            raise AssertionError("Page partitionswitch failed!!")

    def delete_contract(self,params):

        '''
        `Description:` To delete contract.

        `:param1:` Name of contract to delete

        `:return:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            if params:
                    status=self.boss_page.account_handler.delete_contract(params)
                    time.sleep(2)
                    return status
                    #self.action_ele.explicit_wait("cp_allContractsbtnRefresh")
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Delete Contract Failed!!")


    def verify_contract_delete(self,param):
        """
        `Description:` verify the contract is deleted

        `:param:` Dictionary of contract information

        `:return:` status True/False

        `Created by:` Kenash K
        """
        try:
            if param:
                status = self.boss_page.account_handler.verify_delete_contract(param)
                return status
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Verifcation of Delete contract Failed!!")

    def provision_initial_order(self):
        """
        `Description:` Provisioning initial order

        `:param:` None

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.account_handler.provision_initial_order()
            return status
        except:
            raise AssertionError("Provisioning initial order Failed!!")

    def activate_all_service(self):
        """
        `Description:` Activate all services

        `:param:` None

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.account_handler.activate_all_service()
            return status
        except:
            raise AssertionError("Activate services Failed!!")

    def close_all_order(self):
        """
        `Description:`  To close all order

        `:param:` None

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.account_handler.close_all_order()
            return status
        except:
            raise AssertionError("Activate services Failed!!")

    def close_contract(self, name,req_by=None):
        """
        `Description:`  To close contract

        `:param:` contract name

        `:return:` status True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.account_handler.close_contract(name, req_by)
            return status
        except:
            raise AssertionError("Activate services Failed!!")

    def check_for_error(self):
        """
        `Description:` To check for errors in phone number page

        `:param:` None

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status = self.boss_page.commonfunctionality.check_for_error()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def add_transfer_request(self, **params):
        """
        `Description:` To add number transfer equest

        `:param` params:

        `:return: status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.commonfunctionality.add_transfer_request(**params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_transfer_request(self,params):
        """
        `Description:` TO verify transfer request

        `:param` params:

        `:return:` status - True/False

         `Created by:` Kenash K
        """
        try:
            status = self.boss_page.commonfunctionality.verify_transfer_request(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def add_LNP_service(self,**params):
        """
        `Description:` To add LNP request

        `:param` prams:

        `:return:` order_id

         `Created by:` Saurabh Singh
        """
        try:
            order_id = self.boss_page.commonfunctionality.add_LNP_service(**params)
            return order_id
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def activate_service(self, order_id, phone):
        '''
        `Description:` To activate service

        `Param1:` order_id

        `Param2:` phone

        `Returns:` status - True/False

        `Created by:` rdoshi
        '''
        try:
            status = self.boss_page.commonfunctionality.activate_service(order_id, phone)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_message_displayed(self, **params):
        """
        `Description:` This function will help to check whether the error message is displayed on screen or not

        `Param1:'  error_message

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            if params:
                status = self.boss_page.commonfunctionality.verify_message_displayed(params["error_message"])
                return status
            else:
                print("No error message is displayed")
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def click_cancel(self):
        """
        `Description:` This function will click on Cancel button

        `Param:`  None

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.boss_page.commonfunctionality.click_cancel()

        except:
            print("Could not click on Cancel button")
            raise AssertionError("Click on cancel Failed!!")

    def add_usergroup(self, **params):
        '''

        :param params:
        :return:
        '''
        if params.keys():
            self.boss_page.user_handler.add_usergroup(params)
        else:
            print("Please check that the input parameters have been provided")

    def assign_usergroup(self, **params):
        '''

        :param params:
        :return:
        '''
        if params.keys():
            self.boss_page.user_handler.assign_usergroup(params)
        else:
            print("Please check that the input parameters have been provided")

    def delete_usergroup(self, params):
        '''

        :param params:
        :return:
        '''
        try:
            status = self.boss_page.user_handler.delete_usergroup(params)
            return status
        except:
            raise AssertionError("Error occured, could not delete user group!!")

    def add_on_hold_music(self, **params):
        '''
        `Description:` Add 'on hold music' from Phone system--> on hold music

        `Param:` params: Dictionary contains on_hold_music Info

        `Returns:` status - True/False

        `Created by:` Vasuja
        '''
        try:
            status = self.boss_page.OH_music.add_on_hold_music(params)
            return status
        except:
            print("Please check that the input parameters have been provided",
                  self.add_on_hold_music.__doc__)
            raise AssertionError("Adding On Hold Music Failed!!")

    def delete_on_hold_music(self, params):
        '''
        `Description:` Delete 'on hold music' from Phone system--> on hold music

        `Param:` params: Dictionary contains on_hold_music Info

        `Returns:` status - True/False

        `Created by:` Vasuja
        '''
        try:
            status = self.boss_page.OH_music.delete_on_hold_music(params)
            return status
        except:
            raise AssertionError("Error occured, could not delete On Hold Music!!")

    def rename_hold_music(self, **params):
        '''
        `Description:` Rename 'on hold music' from Phone system--> on hold music

        `Param:` params: Dictionary contains on_hold_music Info

        `Returns:` status - True/False

        `Created by:` Vasuja
        '''
        try:
            status = self.boss_page.OH_music.rename_hold_music(params)
            return status
        except:
            print("Please check that the input parameters have been provided",
                  self.rename_hold_music.__doc__)
            raise AssertionError("Adding On Hold Music Failed!!")

    def click_on_manage_button(self, **params):
        '''
        `Description:` This Function will click on manage button of specified feature

        `Param:`  feature name

        `Returns:` None

        `Created by:` Megha Bansal
        '''
        try:
            self.boss_page.commonfunctionality.click_on_manage_button(params)
        except:
            print("Could not access link", self.click_on_manage_button.__doc__)
            raise AssertionError("Click on Manage button failed!!")

    def add_globaluser_mobility(self, **params):
        '''
        `Description:` This Function will add global user to mobility via add on features page
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.addonfeature.add_globaluser_mobility(params)
            return result
        except:
            print("Could not access link", self.add_globaluser_mobility.__doc__)
            raise AssertionError("Add Global User to mobility failed!!")

    def add_mobility_profile(self, **params):
        '''
        `Description:` This Function will add mobility profile for a global user via personal information page
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.personal_information.add_mobility_profile(params)
            return result
        except:
            print("Could not access link", self.add_mobility_profile.__doc__)
            raise AssertionError("Add Global User to mobility failed!!")

    def verify_mobility_checkbox(self, **params):
        '''
        `Description:` This Function will verify mobility checkbox for a global user if there is smr instance setup for selected country
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.user_handler.verify_mobility_checkbox(params)
            return result
        except:
            print("Could not access link", self.verify_mobility_checkbox.__doc__)
            raise AssertionError("Verify mobility checkbox present failed!!")

    def verify_turnup_service(self, **params):
        '''
                `Description:` This Function will verify Global User Number Service
                `Param:` params
                `Returns: ` result - True/False
                `Created by:` Megha Bansal
                '''
        try:
            result = self.boss_page.phone_number.verify_turnup_service(params)
            return result
        except:
            print("Could not access link", self.verify_turnup_service.__doc__)
            raise AssertionError("Verify Global User Number Service failed!!")

    def verify_swap_globaluser(self, **params):
        '''
        `Description:` This Function will verify swap option for global user is disabled or not
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.user_handler.verify_swap_globaluser(params)
            return result
        except:
            print("Could not access link", self.verify_swap_globaluser.__doc__)
            raise AssertionError("Verify swap for GlobalUser failed!!")

    def verify_provisioning_details(self, **params):
        '''
        `Description:` This Function will verify provisioning details of selected service
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.service.verify_provisioning_details(params)
            return result
        except:
            print("Could not access link", self.verify_provisioning_details.__doc__)
            raise AssertionError("Verify provisioning details of global user tn service failed!!")

    def create_DNIS_with_Save(self, **params):
        """
        To create DNIS in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result, selectedTn, selectedDestType = self.boss_page.phone_number.create_DNIS_with_Save(params)
                return result, selectedTn, selectedDestType
            else:
                print("Please check that the input parameters have been provided",
                      self.create_DNIS_with_Save.__doc__)
        except:
            raise AssertionError("Create DNIS Failed!!")

    def create_DNIS_with_Cancel(self, **params):
        """
        To set information to create DNIS with cancel in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.create_DNIS_with_Cancel(params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.create_DNIS_with_Cancel.__doc__)
        except:
            raise AssertionError("Create DNIS with cancel failed")

    def select_number_for_Edit(self, **params):
        """
         To select a number for edit in phone numbers  page

         :param params: Variable contains phone information

         :return: None

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                self.boss_page.phone_number.select_number_for_Edit(params)

            else:
                print("Please check that the input parameters have been provided",
                      self.select_number_for_Edit.__doc__)
        except:
            raise AssertionError("Selecting Number Failed!!")

    def verify_PhoneNumber_Operation(self, **params):
        """
         To verify assign window in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

          `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_PhoneNumber_Operation(params)
                return result

            else:
                print("Please check that the input parameters have been provided",
                      self.verify_PhoneNumber_Operation.__doc__)
        except:
            raise AssertionError("Verification failed!!")

    def verify_PhoneNumber_Operation_for_Edit(self, **params):
        """
        To verify edit window in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_PhoneNumber_Operation_for_Edit(params)
                return result

            else:
                print("Please check that the input parameters have been provided",
                      self.verify_PhoneNumber_Operation_for_Edit.__doc__)
        except:
            raise AssertionError("Verification failed!!")

    def verify_findme(self, option):
        return self.boss_page.commonfunctionality.verify_findme(option)

    def block_here(self):
        print('blocking')

    def config_phone_numbers_callrouting(self, label, phone, num):
        try:
            self.boss_page.commonfunctionality.config_phone_numbers_callrouting(label, phone, num)
        except:
            raise AssertionError("config_phone_numbers_callrouting")

    def config_sim_ring(self, label, num):
        try:
            self.boss_page.commonfunctionality.config_sim_ring(label, num)
        except:
            raise AssertionError("config_phone_sim_ring")

    def config_find_me(self, label, num):
        try:
            self.boss_page.commonfunctionality.config_find_me(label, num)
        except:
            raise AssertionError("config_phone_find_me")

    def config_oae_did(self, label, num):
        try:
            self.boss_page.commonfunctionality.config_oae_did(label, num)
        except:
            raise AssertionError("config_phone_did_oae")


    def refresh_grid(self):
        """
         To refresh grid in phone numbers  page

         :param params: None

         :return: None

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            self.boss_page.phone_number.refresh_grid()
        except:
            raise AssertionError("Refresh failed!")

    def verify_destination_type(self, selectedTn, **params):
        """
        To verify Destination type of DNIS created in phone numbers  page

        :param params: Variable contains phone information , selectedTn

        :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_destination_type(selectedTn, params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.verify_destination_type.__doc__)
        except:
            raise AssertionError("Verify Destination Failed!")

    def verify_destination_and_status(self, selectedTn, selectedDestType, **params):
        """
         To verify Destination name and status of the created DNIS in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_destination_and_status(selectedTn, selectedDestType, params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.verify_destination_and_status.__doc__)
        except:
            raise AssertionError("Verify Destination and Status Failed!")

    def verify_tn_status(self, serviceTn, **params):
        """
         Description : To verify the status of Tn

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha Bansal
        """
        try:
            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params.keys():
                result = self.boss_page.phone_number.verify_tn_status(serviceTn,  params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.verify_tn_status.__doc__)
        except:
            raise AssertionError("Verify Tn Status Failed!")

    def add_mobile_number_to_user(self, **params):
        try:
            if params.keys():
                self.boss_page.user_handler.add_mobile_number_to_user(params)
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Adding mobile number to user Failed!!")

    def remove_mobile_number_for_user(self, **params):
        try:
            if params.keys():
                self.boss_page.user_handler.remove_mobile_number_for_user(params)
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Removing mobile number Failed!!")

    def verify_available_tns(self, params):
        """
        Description : To verify the availability of Tns of the country List

        :param: Variable contains List of country

        :return: Status- True or false

        `Created by:` Megha Bansal
        """
        try:
            result = self.boss_page.phone_number.verify_available_tns(params)
            return result
        except:
            print("Could not access link", self.verify_available_tns.__doc__)
            raise AssertionError("Verify user location dropdown failed!!")

    def add_personal_contact_required_fail(self):
        """
        `Description:` This function will test adding a contact for personal contacts without required fields.

        `Param:`  None

        `Returns:` None

        `Created by:` Wendt J
        """
        try:
            result = self.boss_page.personal_contacts.add_personal_contact_required_fail()
            return result
        except Exception as e:
            print(e)
            raise AssertionError("Personal Contact Add Required Field Verification")

    def add_personal_contact_success(self, **params):
        """
        `Description:` This function will test adding a contact for personal contacts with required fields.

        `Param:`  None

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_contacts.add_personal_contact_success(**params)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Personal Contact Add Verification Failed!!")

    def delete_personal_contact(self, **params):
        """
        `Description:` This function will test deleting a contact for personal contacts.

        `Param:`  None

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_contacts.delete_personal_contact(**params)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Personal Contact Delete Verification Failed!!")

    def verify_grid_toolbar_update_state(self, **params):
        """
        `Description:` Verifies the personal contacts grid update button state.

        `Param:`  None

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_contacts.verify_grid_toolbar_update_state(**params)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Personal Contact Grid Update Button Verification Failed!!")

    def switch_tab(self, tabName):
        """
        `Description:` Switch to the selected tab.

        `Param:` tabName

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.switch_tab(tabName)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Switch to " + tabName + " Tab Failed!!")

    def verify_contact_tab(self):
        """
        `Description:` Verify the Contact tab.

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.verify_contact_tab()
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Verify the Contact Tab Failed!!")

    def verify_roles_permissions_tab(self):
        """
        `Description:` Verify the Roles and Permissions tab.

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.verify_roles_permissions_tab()
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Verify the Roles and Permissions Tab Failed!!")

    def verify_notification_preferences_tab(self):
        """
        `Description:` Verify the Notification Preferences tab.

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.verify_notification_preferences_tab()
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Verify the Notification Preferences Tab Failed!!")

    def add_role(self, role):
        """
        `Description:` Adds the role to the user.

        `Param:` role

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.add_role(role)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Add Role Failed!!")

    def change_role_location(self, role, location):
        """
        `Description:` Changes the location of the role for the user.

        `Param1:` role

        `Param2:` location

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.change_role_location(role, location)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Change Role Location Failed!!")

    def remove_role_location(self, role):
        """
        `Description:` Removes the location of the role for the user and sets scope to account.

        `Param:` role

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.remove_role_location(role)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Remove Role Location Failed!!")

    def delete_role(self, role):
        """
        `Description:` Deletes the role from the user.

        `Param1:` role

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.delete_role(role)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Remove Role Failed!!")

    def change_first_name(self, **params):
        """
        `Description:` This function will change the first name in Personal Information.

        `Param:`  None

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.change_first_name()
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Personal Information Change First Name Failed!!")

    def change_user_data(self, field, value, action):
        """
        `Description:` This function will change the first name in Personal Information.

        `Param1:`   field - name of field to change

        `Param2:`   value - value to change the field to

        `Param3:`   action - button to be clicked (submit/cancel)

        `Returns:` status - True/False

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_information.change_user_data(field, value, action)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Personal Information Change Failed for " + field + " Failed!!")

    def edit_personal_contact(self, **params):
        """
        `Description:` This function will test editing a personal contact

        `Param:`  None

        `Returns:` None

        `Created by:` Wendt J
        """
        try:
            status = self.boss_page.personal_contacts.edit_personal_contact(**params)
            return status
        except Exception as e:
            print(e)
            raise AssertionError("Edit Personal Contact Failed")

    def navigate_to_page(self, page_name):
        """
            `Description:` This function will navigate to the requested page

            `Param:`  page_name: Name of the page to navigate to

            `Created by:` Jim Wendt
        """
        try:
            status = self.boss_page.navigation.navigate_to_page(page_name)
            return status

        except Exception as e:
            print("Navigating to the " + page_name + " page has failed")

    def phonenumber_checboxbox(self, **params):
        """
            Checking Global user in type dropdown
            :param params: type_variable
            :return: status
            `Created by:` Siva
        """

        try:
            status = self.boss_page.shilpa_file.phonenumber_checboxbox(params)
            return status
        except:
            print("Global user verification failed")

    def phonenumber_update(self, **params):
        """
        Checking Global user in type dropdown
        :param params: type_variable
        :return: status
		`Created by:` Siva
        """

        try:
            status = self.boss_page.shilpa_file.phonenumber_update(params)
            return status
        except:
            print("Global user verification failed")

    def update_phonestatefields(self, **params):
        '''
        This Function will update phone state to available
        :param params: Dict with phone information
        :return:
		`Created by:` Siva
        '''
        try:
            if params.keys():
                self.boss_page.phone_number.update_phonenumberfields(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("update phone state Failed!!")

    def verify_user_fields(self, params):
        '''
        This function will verify phone update
        :param params: Dictionary with phone state
        :return: status
		`Created by:` Siva
        '''
        try:
            status = False

         #   if params.keys():
            status = self.boss_page.user_handler.verify_user_fields(params)
            return status

        except:
            raise AssertionError("verify user fields Failed!!")

    def verify_usr_field(self, params):
        '''
        This function will verify phone update
        :param params: Dictionary with phone state
        :return: status
		`Created by:` Siva

        '''
        try:
            status = False

         #   if params.keys():
            status = self.boss_page.user_handler.verify_usr_field(params)
            return status

        except:
            raise AssertionError("verify user fields Failed!!")

    def verify_text_similar(self, text, button):
        """
        `Description:` To verify button text

        `param:` button

        `return:` status - True/False

        `Created by:` Shravan
        """

        try:
            status = self.boss_page.commonfunctionality.verify_text_similar(text, button)
            return status
        except Exception, e:
            print(e)
            raise AssertionError("Button " + text + " Not Similar")

    def stop_impersonating(self):
        """
        `Description:` This function will perform stop impersonating operation

        `Param:` None

        `Returns:` None

        `Created by:` Shravan
        """
        try:
            status = self.boss_page.commonfunctionality.stop_impersonating()
            return status
        except:
            raise AssertionError("Log Off Failed!!")

    def right_click_users(self, extension):
        """
        `Description:` This function will right click users

        `Param:` None

        `Returns:` None

        `Created by:` Shravan
        """
        try:
            status = self.boss_page.commonfunctionality.right_click_users(extension)
            return status
        except:
            raise AssertionError("Right click users Failed!!")

    def right_click_users_with_option(self, **params):
        """
        `Description:` This function will right click users

        `Param:` None

        `Returns:` None

        `Created by:` Priyanak M
        """
        try:
            status = self.boss_page.commonfunctionality.right_click_users_with_option(params['option'], params['email'])
            return status
        except:
            raise AssertionError("Right click users Failed!!")

    def enter_text(self, **params):
        """
        `Description:` This function will enter text in a textbox

        `Param:` None

        `Returns:` None

        `Created by:` Shravan
        """
        try:
            status = self.boss_page.commonfunctionality.enter_text(params['text'], params['element'])
            return status
        except:
            raise AssertionError("Enter text error.")

    def click_button_link(self, button):
        """
        `Description:` Click the given button or link

        `:param` options: button/link

        `:return:`

        `Created by:` Shravan
        """
        try:
            self.boss_page.commonfunctionality.click_button_link(button)
        except Exception, e:
            print(e)
            raise AssertionError("Failed to click on the button or link", e)

    def click_tab_link(self, **params):
        """
        `Description:` Click the Tab -> Link

        `:param` options: params

        `:return:`

        `Created by:` Shravan
        """
        try:
            self.boss_page.commonfunctionality.click_tab_link(params['tab'], params['link'])
        except Exception, e:
            print(e)
            raise AssertionError("Failed to click on the Tab -> Link", e.message)

    def add_user_profile(self, **params):
        """
        `Description:` This function is used add a user profile
        `:param1` user profile data
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            if params.keys():
                result = self.boss_page.profileFunctionality.add_user_profile(params)
                return result
        except:
            raise AssertionError("Creation of profile failed")

    def reassign_user_profile(self, **params):
        try:
            if params.keys():
                result = self.boss_page.profileFunctionality.reassign_user_profile(params)
                return result
        except:
            raise AssertionError("Phone Number re-assignment of profile failed")

    def read_profile_in_profile_grid(self, canvas_id, search_column_id, **params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = ['2', '3', '4', '5', '6', '7', '8']

            result = self.boss_page.commonfunctionality.read_item_in_grid(canvas_id, search_column_id, params["email"], column_data)
            return result
        except Exception, e:
            print(e)
            raise AssertionError("Could not read the profile in the profile grid")

    def verify_profile_updated_in_profile_grid(self, canvas_id, search_column_id, searchParam, **verifyingParams):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = ['2', '3', '4', '5', '6', '7', '8']
            status = False

            result = self.boss_page.commonfunctionality.read_item_in_grid(canvas_id, search_column_id, searchParam, column_data)
            if result['7'] != verifyingParams['7']:
                status = True
            return status
        except Exception, e:
            print(e)
            raise AssertionError("Could not read the profile in the profile grid")

    def verify_profile_in_profile_grid(self, canvas_id, search_column_id, **params):
        """
        `Description:` This function is used to verify that the supplied user profile data is found in the profile grid
        `:param1` the id of the profile grid canvas
        `:param1` The id of the search text field
        `:param1` user profile data. It expects a first name, last name, and email. If there is an extension or phone number that will be used too.
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['2'] = params["firstName"]
            column_data['3'] = params["lastName"]
            if 'selectedPhoneNumber' in params:
                column_data['6'] = params["selectedPhoneNumber"]

            if 'selectedExtn' in params:
                column_data['5'] = params["selectedExtn"]

            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, params["email"], column_data)
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the profile grid")

    def verify_updated_profile_in_users_grid(self, canvas_id, search_column_id, searchParams, **verifyingParams):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = ['2', '3', '4', '5', '6']
            result = self.boss_page.commonfunctionality.read_item_in_grid(canvas_id, search_column_id, searchParams, column_data)
            if result['4'] != verifyingParams['7']:
                status = True
            return status
        except Exception, e:
            print(e)
            raise AssertionError("Could not verify that the profile is updated in the users grid")

    def verify_profile_in_users_grid(self, canvas_id, search_column_id, **params):
        """
        `Description:` This function is used to verify that the supplied user profile data is found in the users grid
        `:param1` the id of the profile users canvas
        `:param1` The id of the search text field
        `:param1` user profile data. It expects a first name, last name, and email.
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['2'] = params["firstName"] + " " + params["lastName"]
            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, params["email"], column_data)
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the users grid")

    def select_profile_in_profile_grid(self, canvas_id, search_column_id, **params):
        """
        `Description:` This function is used to select the supplied user profile data in the profile grid
        `:param1` the id of the profile canvas
        `:param1` The id of the search text field
        `:param1` user profile data. It expects an email.
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            result = self.boss_page.commonfunctionality.select_item_in_grid(canvas_id, search_column_id, params["email"])
            return result
        except:
            raise AssertionError("Could not select the profile in the profile grid")

    def select_multiple_profiles_in_profile_grid(self, canvas_id, search_column_id, *search_list):
        """
        `Description:` This function is used to select multiple profiles based on the supplied user profile data list in the profile grid
        `:param1` the id of the profile canvas
        `:param1` The id of the search text field
        `:param1` the list of user profile data. It expects an email.
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            if len(search_list) == 0:
                return False

            profile_list = []
            for profile in search_list:
                profile_list.append(profile["email"])

            result = self.boss_page.commonfunctionality.select_multiple_items_in_grid(canvas_id, search_column_id, profile_list)
            return result
        except Exception, e:
            print(e)
            raise AssertionError("Could not select the profiles in the profile grid")

    def click_button(self, button_id):
        """
        `Description:` Click the supplied button id
        `:param1` the id of the button
        `:return:` none
        `Created by:` Jane Knickle
        """
        try:
            result = self.boss_page.commonfunctionality.click_button(button_id)
        except Exception as error:
            raise AssertionError("Could not click on the specified button " + error.message)

    def refresh_browser(self):
        """
        `Description:` To refresh browser page
        """
        try:
            self.boss_page.commonfunctionality.refresh_browser()
        except:
            raise AssertionError("No error message is displayed on the screen")

    def change_phone_pin_and_save(self, pin):
        """
        `Description:` To change the phone pin and press save
        `:param1` the pin to change to
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.commonfunctionality.change_phone_pin_and_save(pin)
        except:
            raise AssertionError("Could not change the phone pin")

    def verify_phone_pin_change(self, pin):
        """
        `Description:` To verify that the pin change succeeded
        `:param1` the pin to change to
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.commonfunctionality.verify_phone_pin_change(pin)
        except:
            raise AssertionError("Could not verify the change the phone pin")

    def verify_phone_pin_change_failed(self, message):
        """
        `Description:` To verify that the pin change failed
        `:param1` the pin to change to
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.commonfunctionality.verify_phone_pin_change_failed(message)
        except:
            raise AssertionError("Could not verify the change the phone pin failed")

    def click_element_by_xpath(self, **params):
        """
        `Description:` Login to the BOSS portal using the username and password

        `:param1` username: URL

        `:param2` username: User email address

        `:param3` password: user password

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.click_element_by_xpath(params)
            print("DEBUG: Click successful")
        except:
            raise AssertionError("Click Failed!!")

    def input_text_in_input_field(self, **params):
        try:
            self.boss_page.commonfunctionality.input_text_in_input_field(params)
            time.sleep(1)
            print("DEBUG: Input successful")
        except Exception, e:
            print(e)
            raise AssertionError("Input Failed!!")

    def select_option_in_select(self, **params):
        try:
            self.boss_page.commonfunctionality.select_option_in_select(params)
            time.sleep(1)
            print("DEBUG: Select successful")
        except Exception, e:
            print(e)
            raise AssertionError("Select Failed!!")

    def sleep_in_seconds(self, **params):
        try:
            self.boss_page.commonfunctionality.sleep_in_seconds(params)
            print("DEBUG: Sleep successful")
        except Exception, e:
            print(e)
            raise AssertionError("Sleep Failed!!")

    def verify_page_does_not_contain(self, **params):
        status = self.verify_page(**params)
        if status is True:
            return False;
        else:
            return True

    def click_on_phone_system_users(self):
        '''
        `Description:` Click on Phone System -> Users
        '''
        self.boss_page.commonfunctionality.click_on_phone_system_users()

    def right_click_link_in_grid(self, **params):
        '''
        `Description:` This function will right click link in GRID

        `Param1:` Grid ID

        `Param2:` Link

        `Returns:` None

        '''
        try:
            self.boss_page.commonfunctionality.right_click_link_in_grid(params['grid'], params['link'], params['context_item'])
        except:
            print("Could not access link", self.click_link_in_grid.__doc__)
            raise AssertionError("Right Click operation Failed!!")

    def check_it_says(self, option):
        self.boss_page.commonfunctionality.check_it_says(option)

    def select_tab(self, tab, tabContent):
        '''
        Selects a tab

        :param tab:
        :return:
        '''
        try:
            self.boss_page.commonfunctionality.select_tab(tab, tabContent)
        except:
            print("Could not access link", self.select_tab.__doc__)
            raise AssertionError("Select tab operation Failed!!")

    def adjust_voicemail_interaction(self, extension):
        self.boss_page.commonfunctionality.adjust_voicemail_interation(extension)

    def verify_voicemail_interaction(self, extension):
        self.boss_page.commonfunctionality.verify_voicemail_interaction(extension)

    def select_call_routing_for_user(self, user_email):
        """
         To select Call Routing tab in the Phone/Service details of the selected user

         :param params: Email address of user

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.select_call_routing_for_user(user_email)
            return result
        except:
            raise AssertionError("Call Routing configuration failed!")


    def configure_call_routing(self):
        """
         To configure Call Routing with phone numbers

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_call_routing_options()
            return result
        except:
            raise AssertionError("Call Routing configuration failed!")

    def configure_call_forwarding(self):
        """
         To configure Incoming Call Forwarding

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_call_forwarding()
            return result
        except:
            raise AssertionError("Call Forwarding configuration failed!")

    def call_forwarding_configured(self):
        """
         To verify Call Forwarding is configured

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.call_forwarding_configured()
            return result
        except:
            raise AssertionError("Verify Call Forwarding configured failed!")

    def unassign_profile(self,*params):
        try:
                self.boss_page.profileFunctionality.unassign_profile()
        except:
            raise AssertionError("Unassign of profile failed")

    def verify_close_order_is_created(self, canvas_id, search_column_id,closeOrderID,**params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['3'] = closeOrderID                         #OrderID column
            column_data['5'] = params['profileLocation']            #Location column
            column_data['11'] = "Close"                             #Type column
            column_data['12'] = "Close Service"                     #Sub Type column
            column_data['13'] = "Closed"                            #Status column
            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, column_data['3'], column_data)
            return result
        except:
            raise AssertionError("Could not verify the close order was created")


    def verify_service_status_closed(self, canvas_id, search_column_id, *params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['5']=params[0]
            column_data['10'] = "Closed"
            column_data['27'] = params[0]
            column_data['32'] = "Closed"
            column_data['49'] = params[0]
            column_data['54'] = "Closed"
            column_data['71'] = params[0]
            column_data['76'] = "Closed"
            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, params[0], column_data)
            return result
        except:
            raise AssertionError("Could not verify the close order was created")

    def orderID_of_latest_orders(self):
        try:
            return self.boss_page.commonfunctionality.orderID_of_latest_orders()
        except:
            raise AssertionError("Could not get the latest order id")


    def configure_always_forward_to_voicemail(self):
        """
         Configure always forward to voicemail

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_always_forward_to_voicemail()
            return result
        except:
            raise AssertionError("Always forward to voicemail configuration failed!")


    def always_forward_to_voicemail_configured(self):
        """
         Check to see if always forward to voicemail is configured

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.always_forward_to_voicemail_configured()
            return result
        except:
            raise AssertionError("Check for always forward configuration failed!")


    def open_operations_ipPbx_primaryPartition(self):
        """
        `Description:` To open the Profile page in the Operations > IP PBX, Primary Paritiion > Profiles
        """
        try:
            self.boss_page.commonfunctionality.open_operations_ipPbx_primaryPartition()

        except:
            raise AssertionError("Click on 'Operations > IP IPBX - Primary Partition > Profiles' - Failed!")

    def verify_profiles_grid_display(self):
        """
         `Description:` To verify the Profiles grid is displayed.

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_profiles_grid_display()
            return result

        except:
            raise AssertionError("To verify the Profiles grid is displayed - Failed!")


    def select_one_profile(self, **parmas):
        """
         `Description:` To verify the Profiles grid is displayed.

         `Param:`  Product type to filter on (eg: Product "Connect CLOUD Standard")

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.select_one_profile(parmas)
            return result

        except:
            raise AssertionError("To verify the Profiles grid is displayed - Failed!")


    def get_first_record_from_profile(self):
        """
         `Description:` Gets the first profile record.

         :return: A list of data from the first record.
        """

        try:
            profileData = self.boss_page.commonfunctionality.get_first_record_from_profile()
            return profileData

        except:
            raise AssertionError("Gets the first profile record. - Failed!")


    def click_reassign_button(self):
        """
         `Description:` Click on ReAssign button

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.click_reassign_button()
            return result

        except:
            raise AssertionError("Click on ReAssign button - Failed!")


    def verify_reassign_wizard_display(self):
        """
         `Description:` Verify the reassign wizard is displayed

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_reassign_wizard_display()
            return result

        except:
            raise AssertionError("Verify the reassign wizard is displayed - Failed!")


    def validate_reassigned_extension(self, **params):
        """
        `Description:` Validate reassigned number.
        Given an invalid number, validates the number is invalid with the error message.

         :return: True if error validation is successful.
        """
        try:
            result = self.boss_page.commonfunctionality.validate_reassigned_extension(params)
            return result

        except:
            raise AssertionError("Validate reassigned number - Failed!!")

    def  click_checkbox_of_first_entry_by_search(self, **params):
        """
          `Description:` This function is used to click checkbox of the first enrty by search

          `:return:` None

          `Created by:` Guo Zheng
          """
        try:
            self.boss_page.commonfunctionality.click_checkbox_of_first_entry_by_search(params['canvasId'], params['text'])
        except Exception, e:
            print(e)

    def validate_button_status(self, **params):
        """
          `Description:` This function will validate button status

          `:param1` url: URL of boss page

          `:return:` True or False

          `Created by:`Guo Zheng
          """
        try:
            time.sleep(_DEFAULT_TIMEOUT)
            status = False
            if params.keys():
                status = self.boss_page.commonfunctionality.validate_button_status(params['button_xpath'],
                                                                        params['expect_status'])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_page.__doc__)
            return status
        except:
            raise AssertionError("Page Verification Failed!!")

    def configure_find_me_numbers(self):
        """
         To configure Find Me Numbers

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_find_me_numbers()
            return result
        except:
            raise AssertionError("Verify Find Me Numbers configured failed!")

    def find_me_numbers_configured(self):
        """
         To verify Find Me Numbers are configured

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.find_me_numbers_configured()
            return result
        except:
            raise AssertionError("Verify Call Forwarding configured failed!")

    def upload_specified_file(self, **params):
        """
        `Description:` To upload the specified file
        `:param1` Contains information on the browser button Id, and the path of the file to upload
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            if params.keys():
                return self.boss_page.commonfunctionality.upload_specified_file(params)
            return False
        except:
            raise AssertionError("Could not upload specified file")

    def preview_profile_import(self):
        """
        `Description:` To preview the profiles that are to be imported
        `:param1` None
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.profileFunctionality.preview_profile_import()
        except:
            raise AssertionError("Could not preview the imported profiles")

    def import_previewed_profiles(self):
        """
        `Description:` To import the profiles that were uploaded/ and previously previewed
        `:param1` None
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.profileFunctionality.import_previewed_profiles()
        except:
            raise AssertionError("Could not import the previewed profiles")

    def read_profiles_from_import_file(self, file_path):
        """
        `Description:` To read the profile from the specified import profile csv file
        `:param1` The path of the profiles csv
        `:return:` the list of profiles in the csv file
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.profileFunctionality.read_profiles_from_import_file(file_path)
        except:
            raise AssertionError("Could not read from the specified import file")

    def verify_imported_profiles_in_profile_grid(self, canvas_id, search_column_id, *profile_list):
        """
        `Description:`  Verifies that the specified list of profiles can be found in the profile grid
        `:param1` the id of the profile canvas
        `:param2` The id of the search text field
        `:param3` the list of user profile data. It expects an email.
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            for profile in profile_list:
                # here we will extract the data we want to use to do the search and comparison
                column_data = dict()
                column_data['2'] = profile["firstName"]
                column_data['3'] = profile["lastName"]
                column_data['8'] = profile["type"]
                if profile['phoneNumber'] != '':
                    column_data['7'] = profile["phoneNumber"]
                if profile['extn'] != '':
                    column_data['6'] = profile["extn"]
                result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, profile["email"], column_data)
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the profile grid")

    def verify_imported_profile_in_users_grid(self, canvas_id, search_column_id, *profile_list):
        """
        `Description:`  Verifies that the specified list of profiles can be found in the users grid
        `:param1` the id of the users canvas
        `:param2` The id of the search text field
        `:param3` the list of user profile data. It expects an email.
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            for profile in profile_list:
                # here we will extract the data we want to use to do the search and comparison
                column_data = dict()
                column_data['2'] = profile["firstName"] + " " + profile["lastName"]
                if profile['phoneNumber'] != '':
                    column_data['4'] = profile["phoneNumber"]
                if profile['extn'] != '':
                    column_data['5'] = profile["extn"]
                result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, profile["email"], column_data)
                if result == False:
                    return result
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the profile grid")

    def verify_number(self, *param):
        """
        `Description:` To verify a number exists (Extension or Number)
         :param A number either Extension or Number.

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_number(param)
            return result

        except:
            raise AssertionError("To verify a number exists - Failed!")


    def verify_all_column_names_in_Profiles(self):
        """
        `Description:` Gets all the column headings from the Profiles table
         and checks to see if all the column headings are displayed.

        `Returns:` True if all column headings are found, False if the expected columns heading are not found.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_all_column_names_in_Profiles()
            return result

        except:
            raise AssertionError("Getting the column headings from the Profiles table - Failed!!")


    def verify_buttons_enabled_in_Profiles(self, *param):
        """
         `Description:` To verify the buttons that are passed in are enabled in the profiles

         :param List of button ids that should be enabled.

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_buttons_enabled_in_Profiles(param)
            return result

        except:
            raise AssertionError("To verify the buttons that are passed in are enabled in the profiles - Failed!!")


    def select_profile(self, **param):
        """
         `Description:` Selects a profile based on the optional product filter passed in.
         :param A map (dictionary) containing the product name and the minimum number of results needed

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.select_profile(param)
            return result

        except:
            raise AssertionError("Selects a profile based on the optional product filter passed in - Failed!!")

    def verify_errors_in_profile_spreadsheet(self):
        """
        `Description:`  Verifies that there are errors in the profile spreadsheet to be imported
        `:param1` none
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.profileFunctionality.verify_errors_in_profile_spreadsheet()
        except Exception as error:
            raise AssertionError("Could not verify that the spreadsheet was in error " + error.message)

    def open_on_hold_music(self):
        """
         `Description:` Opens the Phone System > On Hold Music UI.
        """
        try:
            self.boss_page.commonfunctionality.open_on_hold_music()

        except:
            raise AssertionError("Opens the Phone System > On Hold Music UI - Failed!!")


    def select_on_hold_music_file(self):
        """
         `Description:` Selects the first on hold music file
        """
        try:
            result = self.boss_page.commonfunctionality.select_on_hold_music_file()
            return result

        except:
            raise AssertionError("Selects the first on hold music file - Failed!!")


    def click_On_Hold_Music_delete_button_and_confirm(self):
        """
         `Description:` Clicks the On Hold Music delete button and confirms Yes.
        """
        try:
            self.boss_page.commonfunctionality.click_On_Hold_Music_delete_button_and_confirm()

        except:
            raise AssertionError("Clicks the On Hold Music delete button and confirms Yes - Failed!!")


    def verify_delete_operation_is_successful(self, *param):
        """
         `Description:` Verify the delete operation by search for the deleted record.
         :param Data of the deleted record.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_delete_operation_is_successful(param)
            return result

        except:
            raise AssertionError("Verify the delete operation  - Failed!!")

    def verify_programmable_button(self, **params):
        """
         `Description:` Verify the buttons have been programmed properly.
         :param Programmed buttons data.
        """
        try:
            if params.keys():
                result = self.boss_page.prog_button_handler.verify_programmed_button(params)
                return result
        except:
            raise AssertionError("Button verification failed!")

    def select_first_location_on_phones_page(self):
        """
        `Description:`  Selects the first location on the phones page
        `:param1` none
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.phonesFunctionality.select_first_location_on_phones_page()
        except Exception as error:
            raise AssertionError("Could not select a location on the phones page " + error.message)

    def verify_errors_in_phones_spreadsheet(self):
        """
        `Description:`  Verifies that there are errors in the phones spreadsheet to be imported
        `:param1` none
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            return self.boss_page.phonesFunctionality.verify_errors_in_phones_spreadsheet()
        except Exception as error:
            raise AssertionError("Could not verify the errors in the phones spreadsheet " + error.message)

    def delete_imported_phone(self, macaddress):
        """
        `Description:`  Deletes a phone from the phone grid identified by the specified macaddress
        `:param1` macaddress of the phone to be deleted
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            self.boss_page.commonfunctionality.select_item_in_grid("Phones_data_grid_canvas", "Phones_search_macaddress", macaddress)
            return self.boss_page.phonesFunctionality.delete_imported_phone()
        except Exception as error:
            raise AssertionError("Could not delete the imported phone " + error.message)

    def delete_all_imported_profiles(self, *profile_list):
        """
        `Description:`  Deletes all the phones indicated in the profile list
        `:param1` profile_list - list of profiles to be deleted
        `:return:` True if successful, False otherwise
        `Created by:` Jane Knickle
        """
        try:
            for profile in profile_list:
                self.boss_page.commonfunctionality.select_item_in_grid("ProfileDataGridCanvas", "ProfileGridHeaderEmailSearch", profile["email"])
                self.boss_page.profileFunctionality.unassign_profile_with_no_TN()
            return True
        except Exception as error:
            raise AssertionError("Could not delete all the imported profiles " + error.message)

    # this method should not be needed because deleting a profile with no TN should be no different than deleting one with a TN
    def unassign_profile_with_no_TN(self):
        try:
            self.boss_page.profileFunctionality.unassign_profile_with_no_TN()
        except Exception as error:
            raise AssertionError("Could not unassign a profile with no TN " + error.message)

    def upload_file_to_On_Hold_Music(self, **params):
        """
         `Description:` Adds a music file
         :param Containing the Browse button id and file path to upload file.
        """
        try:
            result = self.boss_page.commonfunctionality.upload_file_to_On_Hold_Music(params)
            return result

        except:
            raise AssertionError("Adds a music file  - Failed!!")


    def verify_wrong_file_format_error_message(self):
        """
         `Description:` Verify wrong file format error message
        """
        try:
            result = self.boss_page.commonfunctionality.verify_wrong_file_format_error_message()
            return result

        except:
            raise AssertionError("Verify wrong file format error message  - Failed!!")


    def search_file_on_hold_music(self, param):
        """
         `Description:` Searches if a file exists in On Hold Music
         :params Name of the file.
        """
        try:
            result = self.boss_page.commonfunctionality.search_file_on_hold_music(param)
            return result

        except:
            raise AssertionError("Searches if a file exists in On Hold Music  - Failed!!")


    def verify_on_hold_music_file_added(self, **params):
        """
         `Description:` Verify the add operation by search for the added record.
         :params Data used to upload the file.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_on_hold_music_file_added(params)
            return result

        except:
            raise AssertionError("Adds a music file  - Failed!!")

    def verify_text_in_dropdown(self, **params):
        """
        This function will help to check the text is present in the given dropdown
        :param params: dictionary contains text to be verified and xpath of the dropdown
        :return: status whether text is present or not
        """
        try:
            status = self.boss_page.commonfunctionality.verify_text_in_dropdown(params)
            return status

        except:
            print("Check in dropdown has failed", self.verify_text_in_dropdown.__doc__)

    def edit_user_phone_settings_page(self, **params):
        """
        `Description:` To assign or edit user phone settings in user phone settings page

        `Param1:` user mail id

        `Params:` user Group Name/ Shared Call Appearance/ Video Conferencing  etc

        `Returns:` status - True/False

        `Created by:` Vasuja
        """
        try:
            if params.keys():
                status = self.boss_page.user_handler.edit_user_phone_settings_page(params)
                return status
            else:
                print("Please check that the input parameters have been provided",
                      self.edit_user_phone_settings_page.__doc__)
        except:
            raise AssertionError("Could not edit user phone settings!!")

    def add_user_from_profiles_tab(self, **params):
        '''
        `Description:` Add user from profiles tab.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - True/False,extn

        `Created by:` Palla Surya Kumar
        '''
        try:
            extn,status = self.boss_page.user_handler.add_user_from_profiles_tab(params)
        except:
            raise AssertionError("Could not add user from profiles tab!!")
        return extn,status

    def add_user_from_numbers_tab(self, **params):
        '''
        `Description:` Add user from numbers tab.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - True/False,extn

        `Created by:` Palla Surya Kumar
        '''
        try:
            extn, status = self.boss_page.user_handler.add_user_from_numbers_tab(params)
        except:
            raise AssertionError("Could not add user from numbers tab!!")
        return extn, status

    def verify_user_created_from_profiles_page(self, **params):
        '''
        `Description:` Verify user created from profiles tab.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - True/False

        `Created by:` Palla Surya Kumar
        '''
        try:
            status = self.boss_page.user_handler.verify_user_created_from_profiles_page(params)
        except:
            raise AssertionError("Could not verify user created from profiles page!!")
        return status

    def assign_profile_to_contact_with_no_profile(self, **params):
        '''
        `Description:` This function will assign profile to contact with no profile.

        `Param:` : Dictionary contains profile information

        `Returns: ` result - phone_num,extn

        `Created by:` Palla Surya Kumar
        '''
        try:
            phone_num, extn = self.boss_page.user_handler.assign_profile_to_contact_with_no_profile(params)
        except:
            raise AssertionError("Could not assign profile to the contact!!")
        return phone_num, extn

    def edit_profiles(self, **params):
        '''
        `Description:` This function edits profile.
        `Param:` : Dictionary contains profile information
        `Returns: ` True/False
        `Created by:` Prasanna
        '''
        return self.boss_page.user_handler.edit_profiles(params)

    def get_first_dm_user_info(self, params):
        '''

        `:param:` params:
        `:return:` True/ False
        `:Created by:` Prasanna
        '''

        return self.boss_page.user_handler.get_first_dm_user_info(params)


    def edit_user_personal_information(self, **params):
        '''
        `Description:` This function edits user personal information such as Fname/Last Name/Buisness email.
        `Param:` : Dictionary contains profile information
        `Returns: ` True/False
        `Created by:` Priyanka
        '''
        return self.boss_page.user_handler.edit_user_personal_information(params)

    def verify_type_of_phone_numbers(self, **params):
        '''
        `Description:` This function will verify type of phone numbers sent thrpugh dictionary.

        `Param:` : Dictionary contains phone numbers information

        `Returns: ` result - True/False

        `Created by:` Palla Surya Kumar
        '''
        try:
            status = self.boss_page.phone_number.verify_type_of_phone_numbers(params)
            return status
        except:
            raise AssertionError("Could not verify type of phone number!!")

    def assign_ph_number_to_auto_attendant(self, **params):
        '''
        `Description:` This function will assign ph number to auto attendant.

        `Param:` : dictionary  containing  aa_name

        `Returns: ` status(True/False).

        `Created by:` Palla Surya Kumar
        '''
        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = self.boss_page. \
                phone_number.assign_ph_number_to_auto_attendant(params)
        except:
            raise AssertionError("Could not assign ph number to auto attendant!!")
        return status

    def assign_ph_number_to_hunt_group(self, **params):
        '''
        `Description:` This function will assign ph number to hunt group.

        `Param:` : dictionary  containing  hg_name

        `Returns: ` status(True/False).

        `Created by:` Palla Surya Kumar
        '''
        try:
            status = self.boss_page. \
                phone_number.assign_ph_number_to_hunt_group(params)
        except:
            raise AssertionError("Could not assign ph number to hunt group!!")
        return status

    def edit_enabled_digit_from_dial_plan(self, type):
        '''
        `Description:` Edit enabled digit from dial plan

        `Param:` type of dial plan

        `Returns:` Dictionary containing edited values and status of operation

        `Created by:` Palla Surya Kumar
        '''
        try:
            dialplandict, status = self.boss_page.add_partition.edit_enabled_digit_from_dial_plan(type)
        except:
            raise AssertionError("Editing enabled digit from dial plan failed!!")
        return dialplandict, status

    def verify_edited_dial_plan_from_phone_system_page(self, **params):
        '''
        `Description:` This function will verify edited dial plan from phone system page.

        `Param:` Dictionary containing edited values

        `Returns:` status of operation

        `Created by:` Palla Surya Kumar
        '''
        try:
            status = self.boss_page.add_partition.verify_edited_dial_plan_from_phone_system_page(params)
        except:
            raise AssertionError("Verification of edited digit from phone system page failed!!")
        return status

    def configure_exchange_server(self, name):
        """
        `Description:` configure exchange server on App Integration Tab

        `:name` options: name of exchange server

        `:return:`

        `Created by:` Priyanka
        """
        status = False
        try:
            status = self.boss_page.commonfunctionality.configure_exchange_server(name)
        except Exception, e:
            print(e)
            raise AssertionError("Failed to configure the exchange server", e.message)
        return status

    def verify_created_components_in_profile_tab(self, **params):
        '''
        `Description:` Verify whether any created components (VCFE/BCA/Users), that is present in profiles tab or not .

        `Param:` : Component name

        `Returns: ` result - True/False

        `Created by:` Vasuja
        '''
        try:
            status = self.boss_page.add_partition.verify_created_components_in_profile_tab(params)
        except:
            raise AssertionError("Could not verify created components from profiles page!!")
        return status

    def login_using_new_tab(self, login_info):
        if GLOBAL_AUTH_FLAG:
            login_info.update({'global_auth': True})
        else:
            login_info.update({'global_auth': False})
        self.boss_page.commonfunctionality.login_using_new_tab(login_info)

    def switch_to_tab(self, login_info):
        self.boss_page.commonfunctionality.switch_to_tab(login_info)

    def add_on_feature_activate_shoretel_connect_hybrid(self):
        '''
        `Description:` The API will activate shoretel connect hybrid
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Prasanna
        '''
        result = self.boss_page.addonfeature.add_on_feature_activate_shoretel_connect_hybrid()
        return result

    def add_on_feature_manage_connect_scribe_hybrid(self, params):
        '''
        `Description:` The API will add users to the connect scribe Hybrid
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Prasanna
        '''
        result = self.boss_page.addonfeature.add_on_feature_manage_connect_scribe_hybrid(params)
        return result

    def add_on_feature_activate_and_manage_cloud_hybrid_fax(self, **params):
        '''
        `Description:` The API will Activate the Fax for the Hybrid users
        `Returns: ` result - True/False
        `Created by:` Prasanna
        '''
        result = self.boss_page.addonfeature.add_on_feature_activate_and_manage_cloud_hybrid_fax(params)
        return result

    def activate_add_on_feature(self, **params):
        '''
        `Description:` The API will Activate add in features
        `Returns: ` result - True/False
        `Created by:` Prasanna
        '''
        result = self.boss_page.addonfeature.activate_add_on_feature(params)
        return result

    def add_account(self, **params):
        '''
        `Description:` This Function will create a new account

        `Param:` params: Dictionary with account information

        `Returns:` status - True/False

        `Created by:` Prasanna
        '''

        status = self.boss_page.account_handler.add_account(params)
        return status

    def get_account_details(self, params):
        status = self.boss_page.account_handler.get_account_details(params)
        return status

    # @ Modified By: Prasanna
    def verify_account(self, params):
        status = self.boss_page.account_handler.verify_account(params)
        return status

    def verify_synced_user_profile(self, **params):
        """
        `Description:` This function verifies that the user name phone numbers once sync happen between STD2 and Boss
        `:param1` params: User name and Phone number to be verify
        `:return:` True/False
        `Created by:` Priyanka
        """
        status = self.boss_page.commonfunctionality.verify_synced_user_profile(**params)
        return status

    def verify_phone_settings_sip_password(self, user_email):
        '''
        `Description:` Verify whether sip password field is present in Phone Settings page of user or not.

        `Param:` : Component name

        `Returns: ` result - True/False

        `Created by:` Shilpa K N
        '''
        try:
            status = self.boss_page.phoneServiceUsers.verify_phone_settings_sip_password(user_email)
        except:
            raise AssertionError("Could not verify phone settings page of user!!")
        return status

    def verify_global_user_loc_not_in_account_details_page(self,**params):
        '''
        `Description:` verify global user loc not in account details page

        `Param:` Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Palla Surya Kumar
        '''
        status=False
        try:
            status=self.boss_page.account_handler.verify_global_user_loc_not_in_account_details_page(params)
        except:
            raise AssertionError("Could not verify global user loc in account details page!!")
        return status

    def retrieve_phn_num_with_required_status_from_operations_page(self, **params):
        '''
        `Description:` retrieve phn num with required status from operations page

        `Param:` Dictionary contains required phone number information

        `Returns:` status - True/False,phone number

        `Created by:` Palla Surya Kumar
        '''
        status = False
        try:
            status, phone_num = self.boss_page.phone_number.retrieve_phn_num_with_required_status_from_operations_page(params)
        except:
            raise AssertionError("Could not retrieve phone number in operations page!!")
        return status, phone_num

    def verify_radio_button(self, **params):
        '''
        `Description:` This Function will verify the radio button
        `:params` radio_btn:  xpath of radio button
        `Returns: ` result - True/False
        `Created by:` Vasuja
        '''
        result = self.boss_page.commonfunctionality.verify_radio_button(params['radio_btn'])
        return result

    def Add_Account_using_Connect(self, **params):
        '''
        `Description:` This Function will create a new account

        `Param:` params: Dictionary with account information

        `Returns:` status - True/False

        `Created by:` Priyanka
        '''

        status = self.boss_page.account_handler.add_account_using_Connect(params)
        return status

    def update_verify_account_website_detail(self,urlName):
        '''
            `Description:` This Function will update website detail of  account

            `Param:` params: URL name need to update

            `Returns:` status - True/False

            `Created by:` Priyanka
                '''

        status = self.boss_page.account_handler.update_verify_account_website_detail(urlName)
        return status

    def delete_account_website_detail(self):
        '''
            `Description:` This Function will delete website detail of account

            `Param:` params: None

            `Returns:` status - True/False

            `Created by:` Priyanka
                '''

        status = self.boss_page.account_handler.delete_account_website_detail()
        return status


    def search_mac_address_and_delete(self, mac_addess):
        try:
            self.boss_page.phone_number.search_mac_address_and_delete(mac_addess)
        except:
            raise AssertionError("Error while searching mac address")

    #BCACOmponent file
    def regenerate_programming_page_element_locators(self, username, button_box, line_no):
        """
        `Description:` The API will get an available line on a programming box page and
        will regenerate the element locators for programming page
        `:param1` username: Phone user
        `:param2` button_box: The button box name
        `:param3` line_no: Available line number (if already known)
        `:return:` True/False and the Available line number
        `Created by:` Prasanna
        """
        status, line_no = \
            self.boss_page.BCAOperations.regenerate_programming_page_element_locators(username, button_box, line_no)
        return status, line_no
    #

    def configure_availablity_Settings(self, **params):
        """
         Configure always forward to voicemail

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_availablity_Settings(params['available_state'], params['Call_routing_condition'], params['Call_forward_condition'], params['PhNumber'], params['noofrings'])
            return result
        except:
            raise AssertionError("configure availabilty settings configuration failed!")

    def create_new_power_routing(self, **params):
        """
         Configure always forward to voicemail

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.create_new_power_routing(params['rulename'], params['prcondition'], params['prforward'], params['PhNumber'], params['deleteflag'])
            return result
        except:
            raise AssertionError("create new power routing failed!")


    def select_call_routing_using_extension(self, phextension):
        """
         Configure always forward to voicemail

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.select_call_routing_using_extension(phextension)
            return result
        except:
            raise AssertionError("create new power routing failed!")
