"""Module for adding, deleting and renaming On Hold Music
   File: On_Hold_Music.py
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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
import re
#import base
import web_wrappers.selenium_wrappers as base
import log
import inspect
from selenium.webdriver import ActionChains
from CommonFunctionality import CommonFunctionality
from lib import wait_in_loop as wil

__author__ = "Vasuja"


class OnHoldMusic(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.common_ele = CommonFunctionality(self._browser)
        self.INDEX = 1

    def add_on_hold_music(self, params):
        """
        `Description:` Add 'on hold music' from Phone system--> on hold music

        `Param:` params: Dictionary contains on_hold_music Info

        `Returns:` status - True/False

        `Created by:` Vasuja
         """
        try:
            params = defaultdict(lambda: '', params)
            fullpath = params["filePath"]
            filename = os.path.basename(fullpath)
            wil(self.action_ele.explicit_wait, "OnHoldMusicSearchFilenameInput")
            wil(self.action_ele.input_text, "OnHoldMusicSearchFilenameInput", filename)
            # grid_table = self._browser.element_finder("OnHoldMusicGridCanvas")
            grid_table = wil(self._browser.element_finder, "OnHoldMusicGridCanvas", return_value=True, loop_count=40)
            if grid_table:
                rows = grid_table.find_elements_by_class_name('slick-row')
                if rows:
                    wil(self.action_ele.explicit_wait, "moh_checkbox")
                    wil(self.action_ele.click_element, "moh_checkbox")
                    wil(self.action_ele.explicit_wait, "moh_delete")
                    wil(self.action_ele.click_element, "moh_delete")
                    wil(self.action_ele.explicit_wait, "ug_delete_yes")
                    wil(self.action_ele.click_element, "ug_delete_yes")
                else:
                    pass
            wil(self.action_ele.clear_input_text, "OnHoldMusicSearchFilenameInput")
            wil(self.action_ele.click_element, "moh_add_music_button")
            self.action_ele.explicit_wait("moh_browseButton")
            time.sleep(1)
            # self.action_ele.click_element("moh_browseButton")
            wil(self.action_ele.click_element, "moh_browseButton")
            time.sleep(4)
            try:
                import autoit
            except ImportError as e:
                print e.msg
            status = False
            time.sleep(3)  # this is for the path to resolve in the browse window
            console(autoit.win_exists("[TITLE:Open]"))
            autoit.win_activate("Open")
            autoit.control_send("[TITLE:Open]", "Edit1", params["filePath"])
            # autoit.control_send("[CLASS:#32770]", "Edit1", params["filePath"])
            time.sleep(3)
            autoit.control_click("[TITLE:Open]", "Button1")
            time.sleep(2)
            self.action_ele.input_text("moh_uploadFileDescription", params["musicDescription"])
            self.action_ele.explicit_wait("moh_fileUploadMusic_OK")
            time.sleep(1)
            # self.action_ele.click_element("moh_fileUploadMusic_OK")
            wil(self.action_ele.click_element, "moh_fileUploadMusic_OK")
            status = True
            if params['verify'] == 'True':
                moh_dec = self.query_ele.text_present(params["musicDescription"])

                if moh_dec:
                    time.sleep(2)
                    print("Expected MOH found: %s" % moh_dec)
                    status = True
                else:
                    print("Expected MOH is not found")
                    status = False
                print status
            else:
                pass
            #wil(self.action_ele.click_element, "OnHoldMusicUGSettings")
        except Exception, e:
            print(e)
            print("Could not create On Hold Music")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status


    def edit_on_hold_music(self, moh_name):
        wil(self.action_ele.click_element, "OnHoldMusicUGSettings")



    def delete_on_hold_music(self, moh_name):
        """
        `Description:` Delete user group from Phone System--> User groups

        `Param1:` user_group_name

        `Returns:` status - True/False

        `Created by:` Vasuja
         """
        try:
            status = False
            wil(self.action_ele.explicit_wait, 'moh_headerRow_Name')
            wil(self.action_ele.input_text, 'moh_headerRow_Name', moh_name)
            if self.query_ele.text_present(moh_name):
                self.action_ele.explicit_wait("moh_checkbox")
                time.sleep(1)
                self.action_ele.click_element("moh_checkbox")
                self.action_ele.explicit_wait("moh_delete")
                time.sleep(1)
                self.action_ele.click_element("moh_delete")
                self.action_ele.explicit_wait("ug_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("ug_delete_yes")
                time.sleep(2)
                self._browser._browser.refresh()
                if not self.assert_ele._is_text_present(moh_name):
                    print ("On Hold Music is successfully deleted")
                    status = True
                else:
                    print("Could not delete On Hold Music")
                    status = False
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    self.action_ele.clear_input_text('moh_headerRow_Name')
                    raise AssertionError
            self.action_ele.clear_input_text('moh_headerRow_Name')
        except Exception, e:
            print(e)
            print ("Failed to delete On Hold Music")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def rename_hold_music(self, params):
        """
        `Description:` Add 'on hold music' from Phone system--> on hold music

        `Param:` params: Dictionary contains on_hold_music Info

        `Returns:` status - True/False

        `Created by:` Vasuja
         """
        try:
            params = defaultdict(lambda: '', params)
            status = False
            self.action_ele.explicit_wait('moh_headerRow_Name')
            # self.action_ele.input_text('moh_headerRow_Name', params["musicDescription"])
            wil(self.action_ele.input_text, 'moh_headerRow_Name', params["musicDescription"])
            if self.query_ele.text_present(params["musicDescription"]):
                self.action_ele.click_element("moh_checkbox")
                action = ActionChains(self._browser._browser)
                time.sleep(2)
                print("Finding user.... %s" % params["musicDescription"])
                el = self._browser.elements_finder("moh_data")  # to get the list of elements from all the tray
                # print(el)
                for elm in el:
                    first_value = elm.find_elements_by_tag_name("div")
                    print("Finding user.... %s" % first_value[0].text)
                    if first_value[0].text == params["musicDescription"]:
                        action.context_click(first_value[0]).perform()
                        break
            self.action_ele.click_element('moh_RenameMusicContextMenuItem')
            self.action_ele.input_text("moh_rename_description", params["rename_musicDescription"])
            self.action_ele.explicit_wait("moh_fileUpdateMusic_OK")
            time.sleep(1)
            # self.action_ele.click_element("moh_fileUpdateMusic_OK")
            wil(self.action_ele.click_element, "moh_fileUpdateMusic_OK")
            self.action_ele.explicit_wait("moh_headerRow_Name")
            time.sleep(1)
            self.action_ele.clear_input_text('moh_headerRow_Name')

            status = True
            if params['verify'] == 'True':
                moh_dec = self.query_ele.text_present(params["rename_musicDescription"])
                if moh_dec:
                    time.sleep(2)
                    print("Expected MOH found: %s" % moh_dec)
                    status = True
                else:
                    print("Expected MOH is not found")
                    status = False
                print status
            else:
                pass
            self.action_ele.input_text("moh_headerRow_Name", params["rename_musicDescription"])
            self.action_ele.explicit_wait("moh_checkbox")
            time.sleep(1)
            self.action_ele.click_element("moh_checkbox")
            time.sleep(1)
            self.action_ele.clear_input_text('moh_headerRow_Name')
        except Exception, e:
            print(e)
            print("Could not rename On Hold Music")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status
