"""
   File: Instance.py
   Author: Rohit Arora
"""

import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict
import inspect
from selenium import webdriver
#import autoit
#For console logs while executing ROBOT scripts
from robot.api.logger import console

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

#import base
import web_wrappers.selenium_wrappers as base
import log


class Instance(object):
    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)


    def add_global_country_to_smr_instance(self, params):
        self.action_ele.input_text('instance_name_search', params['smr_instance_name'])
        self.action_ele.click_element('instance_grid_row1_name')
        noAddBtn = self.query_ele.element_not_displayed('global_smr_first_add')

        if not noAddBtn:    #first time add, click at 'Add' button
            addBtn = self._browser.element_finder('global_smr_first_add')
            addBtn.click()
        else:  #if its not a first time add, 'Show Configured Countries' link would be showing
            self.action_ele.click_element('show_configured')
            self.action_ele.click_element('global_smr_add')

        self.action_ele.explicit_wait('ddl_global_countries')
        self.action_ele.select_from_dropdown_using_index('ddl_global_countries',1)
        selected_country = self.query_ele.get_text_of_selected_dropdown_option('ddl_global_countries')
        self.action_ele.select_from_dropdown_using_index('ddl_global_access_number',0)
        self.action_ele.select_from_dropdown_using_index('ddl_global_handover_number',1)
        self.action_ele.select_from_dropdown_using_index('ddl_global_reverse_dial_number',2)
        self.action_ele.click_element('global_smr_add_modal_save')
        time.sleep(1)
        self.action_ele.explicit_wait('confirm_ok')
        self.action_ele.click_element('confirm_ok')
        time.sleep(7)

        if not noAddBtn:
            self.action_ele.click_element('show_configured')

        self.action_ele.input_text('global_smr_grid_country_input',selected_country)
        grid_country_name_column = self._browser.elements_finder('global_smr_grid_country_column')
        if len(grid_country_name_column) == 1:
            result = True
        else:
            result = False

        return result



    def update_global_country_of_smr_instance(self, params):
        self.action_ele.input_text('instance_name_search', params['smr_instance_name'])
        self.action_ele.click_element('instance_grid_row1_name')
        self.action_ele.click_element('show_configured')
        self.action_ele.click_element('global_smr_grid_row1_checkbox')
        self.action_ele.click_element('global_smr_update')
        self.action_ele.explicit_wait('global_smr_country_label')
        selected_country = self.query_ele.get_text('global_smr_country_label')
        self.action_ele.select_from_dropdown_using_index('ddl_global_access_number', 1)
        self.action_ele.select_from_dropdown_using_index('ddl_global_handover_number', 2)
        self.action_ele.select_from_dropdown_using_index('ddl_global_reverse_dial_number', 3)
        selected_access = self.query_ele.get_text_of_selected_dropdown_option('ddl_global_access_number')
        selected_handover = self.query_ele.get_text_of_selected_dropdown_option('ddl_global_handover_number')
        selected_reverse_dial = self.query_ele.get_text_of_selected_dropdown_option('ddl_global_reverse_dial_number')
        self.action_ele.click_element('global_smr_add_modal_save')
        time.sleep(1)
        self.action_ele.explicit_wait('confirm_ok')
        self.action_ele.click_element('confirm_ok')
        time.sleep(7)
        self.action_ele.input_text('global_smr_grid_country_input', selected_country)
        self.action_ele.input_text('access_search', selected_access)
        self.action_ele.input_text('reverse_dial_search', selected_reverse_dial)
        self.action_ele.input_text('handover_search', selected_handover)
        grid_country_name_column = self._browser.elements_finder('global_smr_grid_country_column')

        if len(grid_country_name_column) == 1:
            result = True
        else:
            result = False

        return result



    def verify_existence_show_configured_link(self, params):
        self.action_ele.input_text('instance_name_search', params['smr_instance_name'])
        self.action_ele.click_element('instance_grid_row1_name')
        isShowConfiguredLinkDisplayed = self.query_ele.element_displayed('show_configured')
        if isShowConfiguredLinkDisplayed:
            result = True
        else:
            result = False
        return result
