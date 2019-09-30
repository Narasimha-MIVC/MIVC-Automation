"""Module for creating and verifying profiles
   File: ProfileFunctionality.py
"""

import os
import sys
import time
import random
import string
from web_wrappers import selenium_wrappers as base
from mapMgr import mapMgr
import inspect


# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

class ProfileFunctionality(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    # Start -- Function "click_ok_button"
    def click_ok_button(self, OkConfirmElement):
        """
            `Description:` This function verifies the page contents before clicking on OK button.
            In case of Error message it throws an exception
            `Returns:` True / False
        """
        status = True
        self.action_ele.explicit_wait("ProfileOperationSuccessOK")
        try:
            self._browser.element_finder(OkConfirmElement)
        except Exception as error:
            print(error.message)
            status = False
        time.sleep(5)
        self.action_ele.click_element("ProfileOperationSuccessOK")
        return status
    # End -- Function "click_ok_button"

    def handle_next_operation(self, params, len_list):
        """
             `Description:` Handling of the next button in case of add Profile operations
             `Param1:` params: profile info
             `Param2:` len_list: length of the list of phone numbers
             `Returns:` True / False
         """
        status = True

        i = 2
        while True:
            self.action_ele.explicit_wait("ProfileAddNextButton")
            self.action_ele.click_element("ProfileAddNextButton")
            try:
                self.action_ele.explicit_wait("RequestedByAdd", 3)
                status = True
            except Exception as error:
                print(error.message)
                status = False

            if status:
                break
            elif i >= len_list:
                print("Wait for the next page out of phone numbers")
                # cancel the operation
                self.action_ele.explicit_wait("ProfileAddCancelButton")
                self.action_ele.click_element("ProfileAddCancelButton")
                self.action_ele.explicit_wait("ProfileConfirmYesButton")
                self.action_ele.click_element("ProfileConfirmYesButton")

            elif not status:
                if 'customExtn' in params:
                    print("EXTENSION IN USE, try another custom one")
                    self.action_ele.explicit_wait('ErrorMessageAddExtension')
                    message = (self.query_ele.get_text("ErrorMessageAddExtension"))
                    new_extn = 1000
                    if "Suggested extension" in message:
                        msg_to_list = message.split(" ")
                        new_extn = int(msg_to_list.pop())
                    else:
                        new_extn = random.randint(1000, 9999)
                    self.action_ele.input_text('AddExtension', new_extn)

                else:
                    print("EXTENSION IN USE, try the next one")
                    self.action_ele.select_from_dropdown_using_index("AddTnId", i)
                    params["selectedPhoneNumber"] = (self.query_ele.get_text_of_selected_dropdown_option("AddTnId").strip())

                params["selectedExtn"] = self.query_ele.get_value("AddExtension")
                i += 1

        return status

    # Start --- Function "handle_save_operation"
    def handle_save_operation(self, params, len_list):
        """
            `Description:` Handling of the save button in case of add Profile operations
            `Param1:` params: profile info
            `Param2:` len_list: length of the list of phone numbers
            `Returns:` True / False
        """
        status = True

        self.action_ele.explicit_wait("ProfileAddSaveButton")
        self.action_ele.click_element("ProfileAddSaveButton")
        status = self.click_ok_button("ProfileSaveSuccessPageTitle")

        if not status:
            # cancel the operation
            self.action_ele.explicit_wait("ProfileAddCancelButton")
            self.action_ele.click_element("ProfileAddCancelButton")
            self.action_ele.explicit_wait("ProfileConfirmYesButton")
            self.action_ele.click_element("ProfileConfirmYesButton")

        return status
    # End --- Function "handle_save_operation"

    def add_user_profile(self, params):
        """
        `Description:` Adds a user profile based on the supplied data
        `:param1` user profile data
        `:return:` True if successful, False otherwise
        """
        self.action_ele.explicit_wait("partitionProfilesDataGridAddButton")
        self.action_ele.click_element('partitionProfilesDataGridAddButton')
        self.action_ele.explicit_wait("AddLocationToAssign")
        self.action_ele.select_from_dropdown_using_text('AddLocationToAssign', params['profileLocation'])

        # only select a phone number if there is a parameter for phoneNumber
        listLen = 0;
        if 'phoneNumber' in params:
            self.action_ele.explicit_wait("TnEnabled")
            self.action_ele.select_checkbox("TnEnabled")
            self.action_ele.explicit_wait("AddTnId")
            # if the param is randon, then select the first one
            if params['phoneNumber'] == 'random':
                phoneNumberList= self.query_ele.get_text_list_from_dropdown("AddTnId")
                listLen=    len(phoneNumberList);
                self.action_ele.select_from_dropdown_using_index("AddTnId", listLen-1)
                self.action_ele.explicit_wait("AddTnId")
                params["selectedPhoneNumber"]=  (self.query_ele.get_text_of_selected_dropdown_option("AddTnId").strip())
            else:
                self.action_ele.select_from_dropdown_using_index("AddTnId", params['phoneNumber'])

        # autoExtn should only exist if this open should be selected
        if 'customExtn' in params:
            self.action_ele.input_text('AddExtension', params['customExtn'])
        elif 'autoExtn' in params:
            self.action_ele.explicit_wait("AddAutoAssignExtn")
            self.action_ele.select_checkbox("AddAutoAssignExtn")

        params["selectedExtn"] = self.query_ele.get_value("AddExtension")
        self.action_ele.input_text('AddFirstName', params['firstName'])
        self.action_ele.input_text('AddLastName', params['lastName'])
        self.action_ele.input_text('AddEmail', params['email'])
        result=     self.handle_next_operation(params, listLen)
        if result:
            self.action_ele.explicit_wait("RequestedByAdd")
            self.action_ele.select_from_dropdown_using_index("RequestedByAdd", 1)
            self.action_ele.select_from_dropdown_using_index("RequestSourcesAdd", 1)
        return self.handle_save_operation(params, listLen)

    def preview_profile_import(self):
        """
        `Description:` Clicks the Preview button on the import profiles dialog
        `:param1` none
        `:return:` True
        """
        self.action_ele.explicit_wait("ImportPreviewButton")
        self.action_ele.click_element('ImportPreviewButton')
        return True


    def unassign_profile(self):
        """
        `Description:` Unassign selected profiles

        `:param`

        `:return:`

        """
        print("Start unassign_profile ")
        self.action_ele.explicit_wait('ProfileUnassignButton')
        self.action_ele.click_element("ProfileUnassignButton")
        #Select the first person in the request by  dropdown. There should be at least one
        self.action_ele.select_from_dropdown_using_index("RequestedByDropdown", 1)
        #Select email as the request source
        self.action_ele.select_from_dropdown_using_index("RequestSources", 1)
        self.action_ele.explicit_wait('ProfileUnassignOKButton')
        self.action_ele.click_element("ProfileUnassignOKButton")
        self.action_ele.explicit_wait_not_visible('ProfileUnassignProcessing')
        self.action_ele.explicit_wait('ProfileUnassignSuccessOK')
        self.action_ele.click_element("ProfileUnassignSuccessOK")
        print("End unassign_profile ")

    def unassign_profile_with_no_TN(self):
        """
        `Description:` Unassign selected profiles THIS SHOULD NOT BE NEEDED BECAUSE IT SHOULD BE NO DIFFERENT TO UNASSIGN A PROFILE

        `:param`

        `:return:`

        """
        print("Start unassign_profile ")
        self.action_ele.explicit_wait('ProfileUnassignButton')
        self.action_ele.click_element("ProfileUnassignButton")
        #Select the first person in the request by  dropdown. There should be at least one
        self.action_ele.select_from_dropdown_using_index("RequestedByDropdown", 1)
        #Select email as the request source
        self.action_ele.select_from_dropdown_using_index("RequestSources", 1)
        self.action_ele.explicit_wait('ProfileUnassignOKButton')
        self.action_ele.click_element("ProfileUnassignOKButton")
        print("End unassign_profile ")

    def import_previewed_profiles(self):
        """
        `Description:` Imports profiles that are currently being previewed
        `:param1` none
        `:return:` True if successful, False otherwise
        """
        status = False
        try:
            self.action_ele.explicit_wait("ImportFormRequestedBy")
            self.action_ele.select_from_dropdown_using_index("ImportFormRequestedBy", 1)
            self.action_ele.select_from_dropdown_using_index("ImportFormRequestedSources", 1)
            self.action_ele.explicit_wait("ImportFormImportButton")
            self.action_ele.click_element('ImportFormImportButton')
            self.action_ele.explicit_wait("ImportFormMessageText", 70)
            msgText = self.query_ele.get_text("ImportFormMessageText")
            if "uploaded successfully" in msgText:
                self.action_ele.click_element('ImportFormCloseButton')
                # to allow the import to finish
                time.sleep(15)
                status = True
        except Exception as e:
            print("Exception when trying to import profiles " + e.message)
        return status

    def read_profiles_from_import_file(self, file_path):
        """
        `Description:` Reads profiles from the specified csv file
        `:param1` the path of the csv fiel
        `:return:` True if successful, False otherwise
        """
        try:
            profile_list=[]
            with open(file_path) as fp:
                i = 0
                for line in fp:
                    if i == 0:
                        i += 1
                        continue
                    print(line)
                    line = line.replace('\n', '').replace('\r', '')
                    profile_data = line.split(',')
                    profile = dict()
                    profile['type'] = profile_data[1]
                    profile['phoneNumber'] = profile_data[2]
                    profile['extn'] = profile_data[3]
                    profile['firstName'] = profile_data[4]
                    profile['lastName'] = profile_data[5]
                    profile['email'] = profile_data[6]
                    profile['profileLocation'] = profile_data[7]
                    profile_list.append(profile)
                    i += 1
            fp.close()
            return profile_list
        except Exception as e:
            print("Exception when trying to read the import profiles file" + e.message)
            return None

    def verify_tooltip_error(self, row, col_num, error_text):
        """
        `Description:` Verifies an error exists in the import of the profile based on the specified parameters
        `:param1` the row the error exists in the preview
        `:param2` the column the error exists in the preview
        `:param3` the error that should exist
        `:return:` True if successful, False otherwise
        """
        columns = row.find_elements_by_class_name('slick-cell')
        col_err = columns[col_num].find_elements_by_tag_name('span')
        if len(col_err) == 0:
            return False

        tootip_text = col_err[0].get_attribute("title")
        if tootip_text != error_text:
            return False
        return True

    def verify_errors_in_profile_spreadsheet(self):
        """
        `Description:` Verifies there are errors in an imported profiles csv. this function is for TC 202291  only and relies on the spreadsheet Profiles_Import_TC_202291.csv
        `:param1` none
        `:return:` True if successful, False otherwise
        """
        try:
            self.action_ele.explicit_wait("ImportFormProfileGrid")
            grid_table = self._browser.element_finder("ImportFormProfileGrid")
            if grid_table:
                rows = grid_table.find_elements_by_class_name('slick-row')

                # row 1 should have a "Phone number does not exist" error
                if self.verify_tooltip_error(rows[0], 0, "Phone number does not exist") == False:
                    return False

                # row 2 should have a "Extension already in use" error
                if self.verify_tooltip_error(rows[1], 1, "Extension already in use") == False:
                    return False

                # row 3 should have a "Duplicate phone number in spreadsheet" error
                if self.verify_tooltip_error(rows[2], 0, "Duplicate phone number in spreadsheet") == False:
                    return False

                # row 4 should have a "Duplicate phone number in spreadsheet" error to match its dup above
                if self.verify_tooltip_error(rows[3], 0, "Duplicate phone number in spreadsheet") == False:
                    return False

                # row 5 should have a "Extension should be 4 digits" error
                if self.verify_tooltip_error(rows[4], 1, "Extension should be 4 digits") == False:
                    return False

                # row 6 should have a "Extension should be 4 digits" error
                if self.verify_tooltip_error(rows[5], 1, "Extension should be 4 digits") == False:
                    return False

                # row 7 should have a "Extension should not start with 0 or 9" error
                if self.verify_tooltip_error(rows[6], 1, "Extension should not start with 0 or 9") == False:
                    return False

                # row 8 should have a "Extension should not start with 0 or 9" error
                if self.verify_tooltip_error(rows[7], 1, "Extension should not start with 0 or 9") == False:
                    return False

                # row 9 should have a "Incorrect Product name or Profile type" error
                if self.verify_tooltip_error(rows[8], 2, "Incorrect Product name or Profile type") == False:
                    return False

                # row 10 should have a "Missing email address" error
                if self.verify_tooltip_error(rows[9], 5, "Missing email address") == False:
                    return False

                # row 11 should have a "Missing First Name" error
                if self.verify_tooltip_error(rows[10], 3, "Missing First Name") == False:
                    return False

                # unfortunately no amount of scrolling returned the last 2 rows, so we will query them knowing their extension

                self.action_ele.explicit_wait("ImportFormExtnSearch")
                self.action_ele.input_text("ImportFormExtnSearch", "1029")
                self.action_ele.explicit_wait("ImportFormProfileGrid")
                rows = self._browser.element_finder("ImportFormProfileGrid")

                # row 12 should have a "Missing Last Name" error (ext 1029)
                if self.verify_tooltip_error(rows, 4, "Missing Last Name") == False:
                    return False

                self.action_ele.input_text("ImportFormExtnSearch", "1030")
                self.action_ele.explicit_wait("ImportFormProfileGrid")
                rows = self._browser.element_finder("ImportFormProfileGrid")
                # row 13 should have a "Location not found" error (ext 1030)
                if self.verify_tooltip_error(rows, 6, "Location not found") == False:
                    return False

                return True
        except Exception as e:
            print("Exception when trying verifying errors in the import spreadsheet" + e.message)

    def reassign_user_profile(self, params):
        self.action_ele.explicit_wait("partitionProfilesDataGridReassignButton")
        self.action_ele.click_element('partitionProfilesDataGridReassignButton')
        listLen = 0;

        phoneNumberList = self.query_ele.get_text_list_from_dropdown("ReassignTnId")
        listLen = len(phoneNumberList);
        self.action_ele.select_from_dropdown_using_index("ReassignTnId", listLen - 1)
        self.action_ele.explicit_wait("ReassignTnId")
        params["selectedPhoneNumber"] = (
            self.query_ele.get_text_of_selected_dropdown_option("ReassignTnId").strip())

        status = True

        self.action_ele.explicit_wait("ProfileReassignSaveButton")
        self.action_ele.click_element("ProfileReassignSaveButton")
        status = self.click_ok_button('ProfileReassignSuccessPageMsg')

        if not status:
            # cancel the operation
            self.action_ele.explicit_wait("ProfileReassignCancelButton")
            self.action_ele.click_element("ProfileReassignCancelButton")
            self.action_ele.explicit_wait("ProfileConfirmYesButton")
            self.action_ele.click_element("ProfileConfirmYesButton")
        return status
		
    def populate_user_profile(self, params):
        """
            `Description:` Populates the add user profile dialog box without saving
            Used when validating dialog box
            `Param1:` params: profile info
        """
        self.action_ele.explicit_wait("partitionProfilesDataGridAddButton")
        self.action_ele.click_element('partitionProfilesDataGridAddButton')
        time.sleep(5)
        self.action_ele.explicit_wait("AddLocationToAssign")
        self.action_ele.select_from_dropdown_using_text('AddLocationToAssign', params['profileLocation'])
        self.action_ele.explicit_wait("TnEnabled")
        self.action_ele.select_checkbox("TnEnabled")
        self.action_ele.explicit_wait("AddTnId")
        phoneNumberList = self.query_ele.get_text_list_from_dropdown("AddTnId")
        listLen = len(phoneNumberList)
        # self.action_ele.select_from_dropdown_using_index("AddTnId", 0)
        self.action_ele.select_from_dropdown_using_index("AddTnId", listLen - 1)
        self.action_ele.input_text('AddFirstName', params['firstName'])
        self.action_ele.input_text('AddLastName', params['lastName'])
        self.action_ele.input_text('AddEmail', params['email'])

    def read_first_extension_in_profile_grid(self):
        """
            Retrieves the first non empty extension number in the profiles grid
        """
        # Iterate through the table and select the profile with first valid extension
        self.action_ele.explicit_wait("ProfileDataGridCanvas")
        grid_table = self._browser.element_finder("ProfileDataGridCanvas")
        rows = grid_table.find_elements_by_class_name('slick-row')
        extension= ""

        for row in rows:
           div_list = row.find_elements_by_tag_name("div")
           # indexes seem to be hard coded, extension index in row is 5
           # if the extension is not empty, grab the value and exit loop
           if hasattr(div_list[5], 'text'):
               extension = div_list[5].text
               break

        return extension

    def enter_profile_extension(self, extension):
        """
                Simply resets and enters a new  extension number in the profiles grid add profile wizard
        """
        self.action_ele.explicit_wait("AddExtension")
        self.action_ele.clear_input_text("AddExtension")
        self.action_ele.input_text('AddExtension', extension)


    def verify_extension_error(self, error):
        """
            Sees if the error displayed in the message box matches (or more accurately contains the
            given error
        """
        #click next button to force validation and msg box
        self.action_ele.explicit_wait("ProfileAddNextButton")
        self.action_ele.click_element("ProfileAddNextButton")

        self.action_ele.explicit_wait("ErrorMessageAddExtension")
        #see if the error msg contains what we expect
        if error in self.query_ele.get_text('ErrorMessageAddExtension'):
            return True
        else:
            return False

    def cancel_add_profile(self):
        """
            Cancels out of the add profile wizard
        """
        self.action_ele.explicit_wait("ProfileAddCancelButton")
        self.action_ele.click_element("ProfileAddCancelButton")

        try:
            self.action_ele.explicit_wait("ProfileWizardConfirmCancel")
        except Exception as e:
            print("Exception waiting for confirm cancel dialog" + e.message)

        self.action_ele.explicit_wait("ProfileConfirmYesButton")
        self.action_ele.click_element("ProfileConfirmYesButton")
	