"""
BCA Portal functionality
"""


class BcaComponent(object):

    def create_bca(self, params):
        """
        `Description:` This function will create new BCA
        `:param1` params: BCA information
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.create_bca(params)
        return status

    def verify_bca(self, **params):
        """
        `Description:` This function will verify a BCA
        `:param1` params: BCA information
        `:return:` True/False
        `Created by:` Prasanna
        """
        try:

            status = self.boss_page.BCAOperations.verify_bca(params)
            return status

        except Exception, e:
            print("Please check that the input parameters have been provided",
                    self.verify_bca.__doc__)
            print(e.message)
            raise AssertionError("Verification of new BCA Failed!!")

    def retrieve_phone_number(self, params):
        """
        `Description:` This function will retrieve the user phone info
        `:param1` params: Phone information
        `:return:` True/False  and the phone number
        `Created by:` Prasanna
        """
        status, phone_number = False, None

        try:
            status, phone_number= self.boss_page.BCAOperations.retrieve_phone_number(params)
        except Exception, e:
            print(e.message)
        return status, phone_number

    def verify_phone_number(self, **params):
        """
        `Description:` This function verifies that the phone numbers in a particular range have been added and
        are in desired state
        `:param1` params: Phone number info
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_phone_number(params)
        return status

    def verify_geo_location(self, param):
        """
        `Description:` This function verifies if the geographic location is already added
        `:param1` param: Location Name
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_geo_location(param)
        return status

    # def delete_bca(self, **param):
    def bca_deletion(self, param):
        """
        `Description:` This function will delete the BCA
        `:param1` param: BCA name
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.delete_bca(param)
        return status

    def verify_bca_page(self, param):
        """
        `Description:` This function verifies the BCA page UI for various buttons and tabs
        `:param1` param: BCA Information
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_bca_page(param)
        return status

    def verify_add_bca_page(self):
        """
        `Description:` This function verifies the Add BCA page
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_add_bca_page()
        return status

    def verify_deletion_of_bca(self, **params):
        """
        `Description:` The function will verify the deletion functionality of BCA
        `:param1` params: BCA Information
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_deletion_of_bca(params)
        return status

    def verify_bca_m5portal_bread_crumb(self, param):
        """
        `Description:` The function will verify the BCA page bread crumb
        `:param1` param: The account name
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_bca_m5portal_bread_crumb(param)
        return status

    def verify_call_forward_busy_field_options(self):
        """
        `Description:` The function will verify the Add BCA page Call forward busy field options
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_call_forward_busy_field_options()
        return status

    def verify_call_forward_no_answer_field_options(self):
        """
        `Description:` The function will verify the Add BCA page Call forward no answer field options
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_call_forward_no_answer_field_options()
        return status

    def verify_conferencing_field_options(self):
        """
        `Description:` The function will verify the Add BCA page Conferencing field options
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_conferencing_field_options()
        return status

    def verify_enable_tone_check_box(self):
        """
        `Description:` The function will verify the Add BCA page Enable Tone check box
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_enable_tone_check_box()
        return status

    def select_bca_on_prog_buttons_page(self, **params):
        """
        `Description:` The Function will select the BCA on Phone setting page
        `:param1` params: BCA information
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.select_bca_on_prog_buttons_page(params)
        return status

    def copy_bca(self, params):
        """
        `Description:` The Function copies a BCA / aBCA
        `:param1` params: BCA / aBCA info
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.copy_bca(params)
        return status

    def edit_bca(self, params):
        """
        `Description:` The Function edits a BCA / aBCA
        `:param1` param: BCA / aBCA info
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.edit_bca(params)
        return status

    def verify_show_less_settings(self):
        """
        `Description:` The API verifies the show less settings on Add BCA page
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_add_bca_page_show_less_settings()
        return status

    def verify_show_more_settings(self):
        """
        `Description:` The API verifies the show more settings on Add BCA page
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_add_bca_page_show_more_settings()
        return status

    def select_and_verify_user_on_phone_system_users(self, user_name, **kwargs):
        """
        `Description:` The function will select and verify user on Phone system page
        `:param1` user_name: The user name
        `:param2` kwargs: information regarding different fields which need to be verified
        `:return:` True/False
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.select_and_verify_user_on_phone_system_users(user_name, kwargs)

    def enable_sca(self, **params):
        """
        `Description:` The API enables shared call appearance on Phone setting page
        `:param1` params: SCA info
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.enable_sca(params)
        return status

    def verify_copy_bca_page(self, **params):
        """
        `Description:` The API verifies the copy BCA page
        `:param1` params: BCA info
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_copy_bca_page(params)
        return status

    def verify_bca_edit_page(self, **params):
        """
        `Description:` The API verifies the edit BCA page
        `:param1` params: BCA information
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.verify_bca_edit_page(params)
        return status

    def get_abca_profile_name(self, param):
        """
        `Description:` The API gets the required profile name from the list of aBCA profiles
        `:param1` param: partial profile name
        `:return:` True / False, profile name
        `Created by:` Prasanna
        """
        status, profile_name = self.boss_page.BCAOperations.get_abca_profile_name(param)
        return status, profile_name

    def find_entry_on_phone_number_page(self, **param):
        """
        `Description:` The API will verify the required element in the phone number page
        `:param1` param: BCA info
        `:return:` True/False
        `Created by:` Prasanna
        """
        status = self.boss_page.BCAOperations.find_entry_on_phone_number_page(param)
        return status

    def switch_to_profiles_tab_on_primary_partition_profile_page(self):
        return self.boss_page.BCAOperations.click_profiles_element()

    def verify_element_on_primary_partition_profile_page(self, **kwargs):
        """
        `Description:` The function will verify an element on primary partition page
        `:param1` kwargs: element information
        `:return:` True/False
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.elements_on_primary_partition_profile_page(kwargs)

    def clean_bca_suite(self, cleanAll):
        """
        `Description:` The function cleans up the BCAs created
        `Created by:` Prasanna
        """
        self.boss_page.BCAOperations.clean_bca_suite(cleanAll)

    def get_available_program_button_line(self, user_name, button_box):
        """
        `Description:` The API will return an available line on a button box
        `:param1` user_name: Phone user
        `:param2` button_box: The button box name
        `:return:` Available line number
        `Created by:` Prasanna
        """
        line_no = self.boss_page.BCAOperations.get_available_program_button_line(user_name, button_box)
        return line_no

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

    def move_to_line_on_prog_button_page(self, username, button_box):
        """
        `Description:` Moving to a program button page
        `:param1` username: Phone user
        `:param2` button_box: The button box name
        `:return:` True/False
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.move_to_line_on_prog_button_page(username, button_box)

    def verify_bca_on_required_prog_button_line(self, **params):
        """
        `Description:` The function will verify the BCA on a particular program button line
        `:param1` params: BCA info
        `:return:` True/False
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.verify_bca_on_required_prog_button_line(params)

    def assign_ph_number_to_bca(self, ph_status, bca_name, _type):
        """
        `Description:` The function will assign an available phone number to a BCA
        `:param1` ph_status: status of the required phone number
        `:param2` bca_name: The BCA name
        `:param3` _type:  Destination type
        `:return:` True/False and the phone number
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.assign_ph_number_to_bca(ph_status, bca_name, _type)

    def assign_ph_number_to_user(self, ph_status, _type):
        """
        `Description:` The function will assign an available phone number to an user
        `:param1` ph_status: status of the required phone number
        `:param2` _type:  Destination type
        `:return:` True/False and the phone number
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.assign_ph_number_to_user(ph_status, _type)

    def get_phone_number_with_required_status(self, status, _type="Domestic", location=None, country=None, destination="-"):
        """
        `Description:` The function will help find a phone number with the required status
        `:param1` status: status of the required phone number
        `:param2` _type:  Destination type
        `:return:` True/False and the phone number
        `Created by:` Prasanna
        """
        return self.boss_page.BCAOperations.get_phone_number_with_required_status(status, _type, location, country, destination)

    # def select_type_and_function_on_program_page(self, button_box, line_no, **params):
    #     """
    #     The API will select the required
    #     :param button_box:
    #     :param line_no:
    #     :param params:
    #     :return:
    #     """
    #     select_type_and_function_on_program_page(self, button_box, line_no, params)

    ##########################################################
    ####
    # Start - - Mahesh
    ####
    ##########################################################

    def create_bca_from_programmable_button_page(self, params):
        """
        `Description:` The function will create a BCA on programmable button page
        `:param1` params: BCA info
        `:return:` True/False
        `Created by:` Mahesh
        """
        try:
            status = \
                self.boss_page.BCAOperations.create_bca_from_programmable_button_page(params)

        except Exception, e:
            print(e.message)
            raise AssertionError("Create BCA from programmable button failed!!")

        return status

    ##########################################################
    ####
    # End - - Mahesh
    ####
    ##########################################################

    ##########################################################
    ####
    # Start - - Vasuja
    ####
    ##########################################################
    def edit_dnis_on_phone_numbers_page(self, params):
        """
        `Description:` The function edit the selected DNIS on phone number page
        `:param1` param: DNIS info
        `:return:` True/False
        `Created by:` Vasuja
        """
        status = self.boss_page.BCAOperations.edit_dnis_on_phone_numbers_page(params)
        return status

    ##########################################################
    ####
    # End - - Vasuja
    ####
    ##########################################################