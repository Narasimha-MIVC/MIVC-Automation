"""Module for AOB portal functionalities
   Author: Saurabh Singh
"""

class AOBComponent(object):
    ''' BOSS Component Interface to interact with the ROBOT keywords
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def aob_login(self, **params):
        """
        `Description:` Login to the BOSS portal using the username and password and redirect to AOB page

        `:param params:` URL, username, password, Accoutn Name, page name

        created by: Saurabh Singh
        """
        try:
            self.boss_page.commonfunctionality.open_url(params["url"])
            self.boss_page.commonfunctionality.client_login(params["bossusername"],
                                                            params["bosspassword"])
            self.boss_page.commonfunctionality.switch_page_switch_account()
            self.boss_page.commonfunctionality.switch_account(params['AOBaccountName'], params['AccWithoutLogin'])
            self.boss_page.commonfunctionality.switch_page(page=params['page'])
        except:
            raise AssertionError("Navigation Failed!!")

    def aob_navigateto_locationanduser(self):
        """
        `Description:` Naviage to location and user page from Welcome page

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:

            # status = self.boss_page.commonfunctionality.aob_navigateto_locationanduser()
            status = self.boss_page.aobfunctionality.aob_navigateto_locationanduser()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_navigate_to_transfer_requests(self):
        """
        `Description:` Navigate to transfer requests page from Welcome page

        `return:` Status- True or False
        """
        try:
            status = self.boss_page.aobfunctionality.aob_navigate_to_transfer_requests()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_click_transfer_button(self):
        """
        `Description:` To click on Transfer/Transfer More button on Transfer requests page
        """
        try:
            self.boss_page.aobfunctionality.aob_click_transfer_button()
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_select_other_current_provider(self):
        """
        `Description:` To select Other (specify) provider on Transfer request form
        """
        try:
            self.boss_page.aobfunctionality.aob_select_other_current_provider()
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_set_provider_name(self, param):
        """
        `Description:` To set provider name value

        `:param` params: provider name
        """
        try:
            self.boss_page.aobfunctionality.aob_set_provider_name(param)
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_authorize_transfer_request(self):
        """
        `Description:` To click on "I am authorized..." checkbox
        """
        try:
            self.boss_page.aobfunctionality.aob_authorize_transfer_request()
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_save_transfer_request(self):
        """
        `Description:` To save transfer request
        """
        try:
            self.boss_page.aobfunctionality.aob_save_transfer_request()
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_validate_location_activation_date(self, *status):
        """
        `Description:` To validate the location and Activation date in AOB page

        `:param` status: Status of location which need to validate

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.aobfunctionality.aob_validate_location_activation_date(status)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def validate_geo_location_date(self, params, name):
        """
        `Description:` To validate the geo location date in Boss Portal correspond to AOB portal

        `:param` params: Location date

        `:param` name:  name of location

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            # status = self.boss_page.commonfunctionality.validate_geo_location_date(params, name)
            status = self.boss_page.aobfunctionality.validate_geo_location_date(params, name)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_back_button(self):
        """
        `Description:` To click on back button on AOB page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            # status = self.boss_page.commonfunctionality.aob_back_button()
            status = self.boss_page.aobfunctionality.aob_back_button()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_page_aob(self, param):
        """
        `Description:` To verify the correct AOB page is opened or not

        `:param` params: Name of Page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            # status = self.boss_page.commonfunctionality.verify_page(param)
            status = self.boss_page.aobfunctionality.verify_page_title(param)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_location_and_user_button(self):
        """
        `Description:` To validate the button name in Location and user page AOB

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.aobfunctionality.aob_location_and_user_button()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_user_page(self):
        """
        `Description:` To navigate to User page from location and user page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            # status = self.boss_page.commonfunctionality.aob_user_page()
            status = self.boss_page.aobfunctionality.aob_user_page()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_create_user(self, **params):
        """
        `Description:` To create user in User page. This function will all the user fields

        `:param` params: firstname, lastname, email and extention

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_create_user(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_message_displayed(self, params):
        """
        `Description:` To validate if error message displayed in the screen or not

        `:param` params: Error Message which need to be validated

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            if params:
                status = self.boss_page.aobfunctionality.verify_message_displayed(params)
            else:
                print("No error message is displayed")
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_message_displayed(self, params, min_matches = 1, max_matches = 1):
        """
        `Description:` To validate if error message displayed in the screen or not

        `:param` params: Error Message which need to be validated
        `:param` min_matches: Minimum number of matches to find
        `:param` max_matches: Maximum number of matches to find
        
        `:return`:  True or False

        `created by:` Alex Medina
        """
        try:
            if params:
                status = self.boss_page.aobfunctionality.aob_verify_message_displayed(params, min_matches, max_matches)
            else:
                print("No error message is displayed")
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def remove_popup(self, **params):
        """
        `Description:` To remove error pop up from the page by choosing Continue or Stay on Page button

        `:param` button name which need to be choose

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.remove_popup(**params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def user_page_verification(self):
        """
        `Description:` This function will verify bundle utilization count, eg. How many users are created in one bundle

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.user_page_verification()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_save_and_logout_button(self):
        """
        `Description:` To click on Save and Logout button

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_save_and_logout_button()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_logout_button(self):
        """
        `Description:` To click on Save and Logout button

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_logout_button()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_click_button(self, btn):
        """
        `Description:` To click on button on AOB page

        `:param` btn- Name of button which need to press

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_click_button(btn)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_user_field(self):
        """
        `Description:` To verify if user filed is reset properly

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_user_field()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_location_label(self):
        """
        `Description:` To validate if location is in sorted order not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_location_label()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_bundle_switch(self):
        """
        `Description:` To switch to every bundle from start to end

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_bundle_switch()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_click_next_bundle(self):
        """
        `Description:` To click on next bundle

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_click_next_bundle()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_click_skip_user(self):
        """
        `Description:` TO click on Skip user button at User page

        `:return`:  True or False and Heading of bundle

        `created by:` Saurabh Singh
        """
        try:

            status, heading = self.boss_page.aobfunctionality.aob_click_skip_user()
            return status, heading
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_bundle_name(self, name):
        """
        `Description:` To check the bundle name os present or not

        `:param` name: name of bundle

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_bundle_name(name)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_user_name(self, name, bundle_name):
        """
        `Description:` To check if user name is exist in bundle or not

        `:param` name: Name of user

        `:param` bundle_name: Name of bundle

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_user_name(name, bundle_name)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_help_url(self, **params):
        """
        `Description:` To click on Help url and validate correct url is opened or not

        `:param` params: url, username, password

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_help_url(**params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_clear_users_fields(self, params):
        """
        `Description:` To clear user fields

        `:param` params: name of field which need to clear eg. firstName or lastName

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_clear_users_fields(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_error_message(self, params, field):
        """
        `Description:` To validate if error message displayed in the screen or not

        `:param` params: Error Message which need to be validated

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_error_message(params, field)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_created_user(self):
        """
        `Description:` To validate if user is created

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_created_user()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_user_switch(self, **params):
        """
        `Description:` To validate if user switches to next bundle upon cliking on Save button

        `:param` params: user detail like firstname, last name, heading of bundle

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_user_switch(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_get_bundle_name(self):
        """
        `Description:` To get the current bundle name

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_get_bundle_name()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_user_inBoss(self, email):
        """
        `Description:` To validate if created user is refelected in Boss or not

        `:param` email: user email address

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_verify_user_inBoss(email)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_enables_disbale_drop_down(self, params):
        """
        `Description:` To make phone number drop down enable or disble

        `:param` params: Name of button eg. Existing(to enable) or None(to disbale)

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.aobfunctionality.aob_enables_disbale_drop_down(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_user_with_profile(self):
        """
        `Description:` To check if any user is created with phone number or notd

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status, num = self.boss_page.aobfunctionality.aob_check_user_with_profile()
            return status, num
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_if_number_available(self, num):
        """
        `Description:` To validate if phone number becomes available in AOB page

        `:param` num: phone number which need to check

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_if_number_available(num)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_validate_location_status(self, **params):
        """
        `Description:` To validate location status

        `:param` params: status of location

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_validate_location_status(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_create_multiple_user(self, **params):
        """
        `Description:` To create remaining user in one bundle

        `:param` params: User detail like- firstname, lastname, extension,email

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_create_multiple_user(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_get_location_name(self):
        """
        `Description:` To get current active loccation name

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            bundle = self.boss_page.aobfunctionality.aob_get_location_name()
            return bundle
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_get_intial_order_detail(self, name):
        """
        `Description:` To get initial order detail from order page in boss portal

        `:param` name: location name for which order detail needed

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status, bundle = self.boss_page.aobfunctionality.aob_get_intial_order_detail(name)
            return status, bundle
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_inital_order(self, name):
        """
        `Description:` To verify the initial order in AOB page

        `:param` name: location name for which initial order need to be verify

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_verify_inital_order(name)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_user_in_current_budnle(self):
        """
        `Description:` To check if user is present in current bundle or not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_user_in_current_budnle()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_zoom_in_zoom_out(self):
        """
        `Description:` To zoom in and zoom out aob portal

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_zoom_in_zoom_out()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_aob_link(self):
        """
        `Description:` To validate if aob link is available or not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_aob_link()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_location_status(self, location):
        """
        `Description:` To verify the location status present or not

        `:param` location: status which need to verify for location

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_verify_location_status(location)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_callhandling_setup(self, btn):
        """
        `Description:` To click on call handling setup button

        `:param` btn: name of button which need to click "Setup" or "Dont Setup"

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_callhandling_setup(btn)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_select_future_day(self):
        """
        `Description:` To select future date radio box in Actiavation page and enter future date

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_select_future_day()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_save_and_finsih(self):
        """
        `Description:` To clikc on Save and finish button

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_save_and_finsih()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_create_all_user_in_location(self, **params):
        """
        `Description:` To create all user for one location

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_create_all_user_in_location(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_no_tn_number(self, params):
        """
        `Description:` To check if no TN's present in OAB portal and proper message should be displayed

        `:param` params: message

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_no_tn_number(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def update_single_phonenumber(self, **params):
        """
        `Description:` To update single phone number state

        `:param` params: phone number which need to update

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.phone_number.update_single_phonenumber(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

            ######################AOB Regression####################

    def aob_check_current_active_user(self):
        """
        `Description:` To check current active user

        `return:` Status- True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_current_active_user()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_go_to_bundle(self, name):
        """
        `Description:` Go to Specific bundle

        `:param` name: name of bundle on which user want to travel

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_go_to_bundle(name)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_activate_icon_state(self, icon):
        """
        `Description:` To check if page icon is enable or disable

        `:param` icon: nae of feature which need to check (call handling,activate)

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_activate_icon_state(icon)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_call_handling_setup_selection(self, option):
        """
        `Description:` To check if page icon is enable or disable

        `:param` option: name of button

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_call_handling_setup_selection(option)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def refresh_browser(self):
        """
        `Description:` To refresh browser page

        `created by:` Saurabh Singh
        """
        try:
            self.boss_page.aobfunctionality.refresh_browser()
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_call_handling_setup(self):
        """
        `Description:` To check if call handling is set up or not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.aobfunctionality.aob_check_call_handling_setup()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_welcome_page_start_button_exists(self):
        """
        `Description:` This function will check if Welcome page contains Start/Resume button

        `return:` True or False
        """
        try:
            return self.boss_page.aobfunctionality.aob_welcome_page_start_button_exists()
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_get_first_available_number(self):
        """
        `Description:` To get first available numer from user page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status,number = self.boss_page.aobfunctionality.aob_get_first_available_number()
            return status,number
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_available_phone_number_in_call_handling_page(self,num):
        """
        `Description:` To check if number is available in call handling page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_check_available_phone_number_in_call_handling_page(num)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def get_dgrid_values(self, colname, grid):
        """
        `Description:` To check if number is available in call handling page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.get_dgrid_values(colname, grid)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_goto_transfer_more(self):
        """
        `Description:` To naviage to transfer number page from welcome page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_goto_transfer_more()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_configure_transfer_more_page(self,**params):
        """
        `Description:` To naviage to transfer number page from welcome page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_configure_transfer_more_page(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_learn_more_url(self,**params):
        """
        `Description:` This function will verify the Learn More url on user page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_verify_learn_more_url(params)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_activationpage_calendar(self,):
        """
        `Description:` This function will verify if caledar is present on activation page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_activationpage_calendar()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_calendar_enabled(self):
        """
        `Description:` This function will verify if caledar is enabled or not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            #import pdb,sys;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status= self.boss_page.aobfunctionality.aob_calendar_enabled()
            return status
        except Exception, e:
            print e
            raise AssertionError("No error message is displayed on the screen")

    def aob_click_on_calendar(self):
        """
        `Description:` This function will click on calendar

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_click_on_calendar()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_transfer_number_is_created(self):
        """
        `Description:` This function will check if tn entries present on transfer page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_transfer_number_is_created()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_open_two_section(self):
        """
        `Description:` This function will check two section should not open at same time

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_open_two_section()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_phone_number_on_transfer_number_page(self,num):
        """
        `Description:` This function will verify the number on call handling page

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status, num= self.boss_page.aobfunctionality.aob_verify_phone_number_on_transfer_number_page(num)
            return status,num
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_activation_verify_temporary_link(self,linkText):
        """
        `Description:` This function will verify if temporary number link is available on Activation page or not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_activation_verify_temporary_link(linkText)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_activate_icon_visiblity(self,Text):
        """
        `Description:` This function will verify if temporary number link is available on Activation page or not

        `:return`:  True or False

        `created by:` Saurabh Singh
        """
        try:
            status= self.boss_page.aobfunctionality.aob_activate_icon_visiblity(Text)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_element_exists(self, element):
        """
        `Description:` This function will check if element exists or not

        `:param` element

        `return:` True or False
        """
        try:
            return self.boss_page.aobfunctionality.aob_element_exists(element)
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_tab_click(self, element):
        """
        `Description:` This function will click on AOB tabs

        `:param` element - name of tab

        `return:` True or False
        """
        try:
            return self.boss_page.aobfunctionality.aob_tab_click(element)
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_verify_transfer_requests_page(self):
        """
        `Description:` This function will verify transfer requests page

        `return:` True or False
        """
        try:
            existing_numbers_message = self.boss_page.aobfunctionality.aob_verify_message_displayed("Would you like to bring existing phone numbers to Mitel?")
            additional_numbers_message = self.boss_page.aobfunctionality.aob_verify_message_displayed("Would you like to bring additional phone numbers to Mitel?")
            return existing_numbers_message or additional_numbers_message
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_click_and_wait_element(self, element):
        """
        `Description:` This function will click on provided element

        `:param` element
        """
        try:
            #sleep 3 seconds after click
            self.boss_page.aobfunctionality.aob_click_element(element, 10)
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")    

    def aob_click_element(self, element, sleep_seconds = 0):
        """
        `Description:` This function will click on provided element

        `:param` element
        """
        try:
            self.boss_page.aobfunctionality.aob_click_element(element, sleep_seconds)
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_verify_add_user_type_modal_currency_fields(self):
        """
        `Description:` This function will verify currency format on Add User Type modal

        `return:` True or False
        """
        currency_regexp = r"\d+\.\d{2} [A-Z]{3}"
        try:
            onetime_charge_text = self.boss_page.aobfunctionality.aob_get_text("add_user_type_onetime_charge_value")
            onetime_charge_valid = self.boss_page.aobfunctionality.aob_verify_text(onetime_charge_text, currency_regexp)

            monthly_charge_text = self.boss_page.aobfunctionality.aob_get_text("add_user_type_monthly_charge_value")
            monthly_charge_valid = self.boss_page.aobfunctionality.aob_verify_text(monthly_charge_text, currency_regexp)

            return onetime_charge_valid and monthly_charge_valid
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def check_currency_abbreviations(self, params):
        """
            `Description:` This function will check the currency abbrevations on add user type page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:
            status = self.boss_page.aobfunctionality.check_currency_abbreviations(params)
            return status
        except:
            raise AssertionError("Currency abbreviation check failed")

    def select_option_on_call_handling_summary_page(self, option):
        """
            `Description:` This function will click on selected option on call handling summary page

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:

            status = self.boss_page.aobfunctionality.select_option_on_call_handling_summary_page(option)
            return status
        except:
            raise AssertionError("Could not select the option on call handling summary page")

    def aob_ch_setup_business_hour(self, **option):
        """
            `Description:` This function will configure business hour in call handling page

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:

            status = self.boss_page.aobfunctionality.aob_ch_setup_business_hour(option)
            return status
        except:
            raise AssertionError("Could not select the option on call handling summary page")

    def aob_ch_setup_operator_rings(self, **option):
        """
            `Description:` This function will setup rings in operator page and clear the ring based on the flag pass from the dictionary

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:

            status = self.boss_page.aobfunctionality.aob_ch_setup_operator_rings(option)
            return status
        except:
            raise AssertionError("Could not select the option on call handling summary page")

    def aob_delete_transfer_number_entry(self):
        """
            `Description:` This function will setup rings in operator page and clear the ring based on the flag pass from the dictionary

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:

            status = self.boss_page.aobfunctionality.aob_delete_transfer_number_entry()
            return status
        except:
            raise AssertionError("Could not select the option on call handling summary page")

    def add_user_as_an_operator(self, extn):
        """
            `Description:` This function will add user as an operator on call handling summary page

            `:param` extn: Extension of the user which need to be added as operator on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:
            status = self.boss_page.aobfunctionality.add_user_as_an_operator(extn)
            return status
        except:
            raise AssertionError("Could not add user as an operator on call handling summary page")

    def aob_check_ch_tab_open(self, option):
        """
            `Description:` This function will click on selected option on call handling summary page

            `:param` option: name of option which need to click on call handling summary page

            `:return`:  True or False

            `created by:` Immani Mahesh Kumar
        """
        try:

            status = self.boss_page.aobfunctionality.aob_check_ch_tab_open(option)
            return status
        except:
            raise AssertionError("Could not select the option on call handling summary page")

    def aob_get_number_from_ch_page(self):
        """
            `Description:` This function will get the selected number from ch page

            `:return`:  True or False

            `created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.aobfunctionality.aob_get_number_from_ch_page()
            return status
        except:
            raise AssertionError("Could not select the option on call handling summary page")

    def aob_select_bundle_type(self,type):
        try:
            status = self.boss_page.aobfunctionality.aob_select_bundle_type(type)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_add_user_bundle(self,type):
        try:
            status = self.boss_page.aobfunctionality.aob_add_user_bundle(type)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def add_user_confirm_button(self):
        try:
            status = self.boss_page.aobfunctionality.add_user_confirm_button()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_select_user(self,name):
        try:
            status = self.boss_page.aobfunctionality.aob_select_user(name)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_change_user_number(self,index):
        try:
            status, number = self.boss_page.aobfunctionality.aob_change_user_number(index)
            return status, number
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_check_user_number(self, number):
        try:
            status = self.boss_page.aobfunctionality.aob_check_user_number(number)
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_find_user_bundle_type(self, name):
        try:
            status, bundle = self.boss_page.aobfunctionality.aob_find_user_bundle_type(name)
            return status, bundle
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_navigateto_locationactivation(self):
        try:
            status = self.boss_page.aobfunctionality.aob_navigateto_locationactivation()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def aob_verify_activation(self):
        try:
            status = self.boss_page.aobfunctionality.aob_verify_activation()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def verify_bundle_user_counter(self):
        try:
            status = self.boss_page.aobfunctionality.verify_bundle_user_counter_and_checkbox()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def verify_location_checkmark(self):
        try:
            status = self.boss_page.aobfunctionality.verify_location_checkmark()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def click_users_continue_button(self):
        try:
            status = self.boss_page.aobfunctionality.click_users_continue_button()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")

    def click_phone_system(self):
        try:
            self.boss_page.commonfunctionality.click_phone_system()

        except:
            raise AssertionError("No error message is displayed on the screen")

    def click_phone_system_phone_numbers(self):
        try:
            status = self.boss_page.commonfunctionality.click_phone_system_phone_numbers()
            return status
        except:
            raise AssertionError("No error message is displayed on the screen")
    def aob_update_button(self):
        """
        `Description:` To click on update button on AOB page

        `:return`:  True or False

        `created by:` Alex Medina
        """
        try:
            status = self.boss_page.aobfunctionality.aob_update_button()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_add_button(self):
        """
        `Description:` To click on Add button on AOB page

        `:return`:  True or False

        `created by:` Alex Medina
        """
        try:
            status = self.boss_page.aobfunctionality.aob_add_button()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_saveinner_button(self):
        """
        `Description:` To click on Save inner button on AOB page

        `:return`:  True or False

        `created by:` Alex Medina
        """
        try:
            status = self.boss_page.aobfunctionality.aob_saveinner_button()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_verify_add_business_hours_empty(self):
        """
        `Description:` This function will verify adding empty business hours

        `return:` True or False
        
        `created by:` Alex Medina
        """
        try:
            message_text_exists = self.boss_page.aobfunctionality.aob_verify_message_displayed("At least one day is required")
            return message_text_exists
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_add_random_business_hours(self):
        """
        `Description:` This function will add random business hours
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            status = self.boss_page.aobfunctionality.aob_add_random_business_hours()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
            
    def aob_add_multiple_business_hours(self, min_days = 2, max_days = 7):
        """
        `Description:` This function will add multiple business hours
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            status = self.boss_page.aobfunctionality.aob_add_multiple_business_hours()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_get_elements_count(self, param):
        """
        `Description:` This function will get the number of matches of element $param
        `return:` integer count

        `created by:` Alex Medina
        """
        try:
            status = self.boss_page.aobfunctionality.aob_get_elements_count(param)
            
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
        
    def aob_verify_business_hours_count_matches(self, param):
        """
        `Description:` This function will verify if the business hours count matches $param
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = self.boss_page.aobfunctionality.aob_verify_business_hours_count_matches(param)
            
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
    
    def aob_add_single_business_hours(self):
        """
        `Description:` This function will add a single business hours period
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            status = self.boss_page.aobfunctionality.aob_add_multiple_business_hours(1, 1)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
        
    def aob_remove_business_hours(self):
        """
        `Description:` This function will remove the business hours
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            status = self.boss_page.aobfunctionality.aob_remove_business_hours()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")
        
    def aob_verify_add_business_hours_widgets(self):
        """
        `Description:` This function verify add business hours widgets
        `return:` True or False

        `created by:` Alex Medina
        """   
        try:
            result = False
            result = self.boss_page.aobfunctionality.aob_verify_add_business_hours_widgets()
            return result
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_verify_add_business_hours_widgets_reset(self):
        """
        `Description:` This function verify add business hours widgets in their initial state
        `return:` True or False

        `created by:` Alex Medina
        """   
        try:
            active_days_list = []
            inactive_days_list = ["Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat"]
            result = self.boss_page.aobfunctionality.aob_verify_add_business_hours_widgets(active_days_list, inactive_days_list)
            return result
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_verify_business_hours_all_times(self):
        """
        `Description:` This function will verify the business hours section is "At all times"

        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            at_all_times_message = self.boss_page.aobfunctionality.aob_verify_message_displayed("At all times")
            return at_all_times_message
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def aob_unselect_add_business_hours(self):
        """
        `Description:` This function will unselect the days in the add business section
        `return:` True or False

        `created by:` Alex Medina
        """
        try:
            status = False
            status = self.boss_page.aobfunctionality.aob_unselect_add_business_hours()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

