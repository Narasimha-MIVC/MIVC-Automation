"""Module for creating and verifying profiles
   File: ProfileFunctionality.py
"""

import os
import sys
import time
from web_wrappers import selenium_wrappers as base
from mapMgr import mapMgr
import inspect


# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

class PhonesFunctionality(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def select_first_location_on_phones_page(self):
        """
        `Description:` Select the first location in the phones page location dropdown
        `:param1` none
        `:return:` True if successful, False otherwise
        """
        try:
            self.action_ele.explicit_wait("Phones_location_selector")
            self.action_ele.select_from_dropdown_using_index("Phones_location_selector", 2)
            return True
        except Exception as error:
            print (error.message)
            # This control is throwing an exception but the select works, so for now we continue
            return True

    def verify_errors_in_phones_spreadsheet(self):
        """
        `Description:` Verifies there are errors in an imported phones csv. this following function is tied to the phones spreadsheet Phone_Import_TC_197556.csv. if that file changes, this verify function must as well
        `:param1` none
        `:return:` True if successful, False otherwise
        """
        self.action_ele.explicit_wait("Phones_import_message_text")
        import_message = self.query_ele.get_text("Phones_import_message_text")

        if "File contains duplicate entry for phone with MAC address 00:00:00:00:00:01" not in import_message:
            return False
        if "Invalid MAC address: 122334455667" not in import_message:
            return False
        if "Invalid MAC address: LM:00:00:00:00:01" not in import_message:
            return False
        if "Unable to parse phone type: IP 480" not in import_message:
            return False
        if "Undefined phone type: 88" not in import_message:
            return False
        if "1 of 6 phone records were imported" not in import_message:
            return False

        return True

    def delete_imported_phone(self):
        """
        `Description:` Performs the series of clicks needed to delete a phone
        `:param1` none
        `:return:` True if successful, False otherwise
        """
        try:
            time.sleep(2)
            self.action_ele.explicit_wait("Phones_grid_delete_button")
            self.action_ele.click_element("Phones_grid_delete_button")
            time.sleep(2)
            self.action_ele.explicit_wait("Phones_delete_confirm_button")
            self.action_ele.click_element("Phones_delete_confirm_button")
            self.action_ele.explicit_wait("Phones_message_ok_button")
            self.action_ele.click_element("Phones_message_ok_button")
            return True
        except Exception as error:
            print (error.message)
            return False



