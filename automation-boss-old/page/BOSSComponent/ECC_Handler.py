"""Module for execution of ECC portal functionalities
   File: ECC_Handler.py
   Author: Afzal Pasha
"""

import os
import sys
import time
import imaplib
import time, re
import email
import datetime
from time import gmtime, strftime
from collections import defaultdict
import inspect
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# For console logs while executing ROBOT scripts
from robot.api.logger import console

# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
# import base
import web_wrappers.selenium_wrappers as base

from log import log
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

__author__ = "Afzal Pasha"

_RETRY_COUNT = 3


class ECC_Handler(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def ecc_activate_click(self, params):
        """
        `Description:` To click on Add-on features --> ECC --> Activate

        `Param:`  &{Settings}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("ecc_activate_click")
        time.sleep(1)
        if params["activateIvrDbIntrgration"] == "True":
            self.action_ele.click_element("activate_ivr_database_integration")
            time.sleep(1)
        if params["activateAdditionalPorts"] == "True":
            self.action_ele.click_element("activate_additional_ivr_Ports")
            time.sleep(1)
            self.action_ele.input_text("Ports_Quantity", params["ports"])
        self.action_ele.select_from_dropdown_using_text("ECC_Cluster", params["eccClutster"])
        self.action_ele.select_from_dropdown_using_text("ECC_TimeZone", params["eccTimeZone"])
        time.sleep(1)

    def ecc_activate_review_click(self, params):
        """
        `Description:` To view summary screen

        `Param:`  &{Settings}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.click_element("ecc_activate_review")
        self.action_ele.explicit_wait("requested_by")
        time.sleep(1)
        self.action_ele.select_from_dropdown_using_text("requested_by", params["requestedBy"])
        self.action_ele.select_from_dropdown_using_text("requested_source", params["requestedSource"])

    def ecc_ok_click(self):
        """
        `Description:` To submit all values

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("ecc_activate_update_submit")
        time.sleep(3)

    def report_recurring_tab_click(self):
        """
        `Description:` To click on recurring tab

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(5)
        self.action_ele.click_element("recurring_tab")
        time.sleep(1)

    def report_onetime_tab_click(self):
        """
        `Description:` To click on onetime tab

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(5)
        self.action_ele.click_element("onetime_tab")
        time.sleep(5)

    def recurring_report_add_click(self):
        """
        `Description:` To add recurring report click Add button

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("recurring_report_add_report")
        time.sleep(2)

    def onetime_report_add_click(self):
        """
        `Description:` To add onetime report click Add button

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("onetime_report_add_report")
        time.sleep(2)

    def report_enter_fieldvalues(self, params):
        """
        `Description:` enter all filed values while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(10)
        self.action_ele.input_text("text_report_name", params["reportName"])
        self.action_ele.select_from_dropdown_using_text("base_report", params["basereport"])
        time.sleep(5)

    def report_select_entities(self):
        """
        `Description:` To check all checkboxes of Agents...

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("search_agents")
        time.sleep(1)

    def report_select_reporttype(self, params):
        """
        `Description:` To select report type while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element(params["reportType"])
        time.sleep(1)

    def report_select_datetime(self):
        """
        `Description:` To select date time while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("datetime_date_last_days")
        time.sleep(1)
        self.action_ele.click_element("datetime_time_last_hours")
        time.sleep(1)

    def report_select_formatfile(self, params):
        """
        `Description:` To select format type while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.input_text("text_file_name", params["textFileName"])
        time.sleep(1)

    def report_enter_delivery_details(self, params):
        """
        `Description:` To enter delivery details while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.input_text("text_email_from", params["emailFrom"])
        self.action_ele.input_text("text_subject", params["emailSubject"])
        time.sleep(1)

    def report_next_click(self):
        """
        `Description:` To click on next button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("report_next_button")
        time.sleep(1)

    def report_back_click(self):
        """
        `Description:` To click on back button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("Report_Back_Button")
        time.sleep(1)

    def report_cancel_click(self):
        """
        `Description:` To click on cancel button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("report_cancel_button")
        time.sleep(1)

    def report_finish_click(self):
        """
        `Description:` To click on finish button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            successMessage = "Report has been scheduled successfully."
            self.action_ele.click_element("report_finish_button")
            self.action_ele.explicit_wait("fnMessage_box_ok")
            time.sleep(5)
            if successMessage in self.query_ele.get_text("fnMessage_box_ok_text"):
                self.action_ele.click_element("fnMessage_box_ok")
                status = True
            else:
                self.action_ele.click_element("fnMessage_box_ok")
                status = False
        except:
            raise AssertionError("Failed to schedule the report!!")
        return status


    def recurring_report_exists_check(self, params):
        """
        `Description:` To check whether recurring report exists

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("recurring_tab_Grid_name_filter", params["reportName"])
        time.sleep(1)

    def onetime_report_exists_check(self, params):
        """
        `Description:` To check whether onetime report exists

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("onetime_tab_grid_name_filter", params["reportName"])
        time.sleep(1)


    def select_recurring_report_to_edit(self, params):
        """
        `Description:` Select recurring report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("recurring_tab_grid_name_filter", params["recurringReportName_ToEdit"])
        time.sleep(1)
        self.action_ele.click_element("recurring_tab_selected_report")
        time.sleep(1)

    def select_onetime_report_to_edit(self, params):
        """
        `Description:` Select onetime report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("onetime_tab_grid_name_filter", params["oneTimeReportName_ToEdit"])
        time.sleep(1)
        self.action_ele.click_element("onetime_tab_selected_report")
        time.sleep(1)

    def recurring_report_edit_click(self):
        """
        `Description:` To click on edit button after select recurring report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("recurring_report_edit_report")
        time.sleep(1)

    def onetime_report_edit_click(self):
        """
        `Description:` To click on edit button after select onetime report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("onetime_report_edit_report")
        time.sleep(1)

    def select_recurring_report_to_delete(self, params):
        """
        `Description:` To select onetime report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(5)
        self.action_ele.input_text("recurring_tab_grid_name_filter", params["recurringReportName_ToDelete"])
        time.sleep(1)
        self.action_ele.click_element("recurring_tab_selected_report")
        time.sleep(1)

    def select_onetime_report_to_delete(self, params):
        """
        `Description:` To select onetime report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("onetime_tab_grid_name_filter", params["oneTimeReportName_ToDelete"])
        time.sleep(1)
        self.action_ele.click_element("onetime_tab_selected_report")
        time.sleep(1)

    def select_recurring_report_to_copy(self, params):
        """
        `Description:` To recurring report to copy

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("recurring_tab_grid_name_filter", params["recurringReportToCopy"])
        time.sleep(1)
        self.action_ele.click_element("recurring_tab_selected_report")
        time.sleep(1)

    def select_onetime_report_to_copy(self, params):
        """
        `Description:` To onetime report to copy

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("onetime_tab_grid_name_filter", params["oneTimeReportToCopy"])
        time.sleep(1)
        self.action_ele.click_element("onetime_tab_selected_report")
        time.sleep(1)

    def recurring_report_delete_click(self):
        """
        `Description:` To click on delete button after select recurring report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            successMessage = "Selected Report(s) have been deleted"
            self.action_ele.click_element("recurring_report_delete_report")
            time.sleep(2)
            self.action_ele.click_element("fnMessage_box_yes")
            time.sleep(2)
            self.action_ele.explicit_wait("fnMessage_box_ok")
            time.sleep(2)
            if successMessage in self.query_ele.get_text("fnMessage_box_ok_text"):
                self.action_ele.click_element("fnMessage_box_ok")
                time.sleep(10)
                status = True
            else:
                self.action_ele.click_element("fnMessage_box_ok")
                status = False
        except:
            raise AssertionError("Fail to delete the report!!")
        return status


    def onetime_report_delete_click(self):
        """
        `Description:` To click on delete button after select onetime report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            successMessage = "Selected Report(s) have been deleted"
            self.action_ele.click_element("onetime_report_delete_report")
            time.sleep(2)
            self.action_ele.click_element("fnMessage_box_yes")
            time.sleep(2)
            self.action_ele.explicit_wait("fnMessage_box_ok")
            time.sleep(2)
            if successMessage in self.query_ele.get_text("fnMessage_box_ok_Text"):
                self.action_ele.click_element("fnMessage_box_ok")
                time.sleep(1)
                status = True
            else:
                self.action_ele.click_element("fnMessage_box_ok")
                status = False
        except:
            raise AssertionError("Fail to delete the report!!")
        return status

    def recurring_report_verification(self, params):
        """
        `Description:` To verify  recurring report details

        `Param:`  &{ReportValues}

        `:Returns`:  True/False

        `created by:` Afzal Pasha

        """
        try:
            time.sleep(5)
            stastus = False
            self.action_ele.click_element("report_next_button")
            time.sleep(1)
            self.action_ele.click_element("report_next_button")
            time.sleep(1)
            reportType = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=rbtschedule]:checked').value")
            time.sleep(1)
            dateOption = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=paramsDateOptions]:checked').value")
            timeoption = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=paramsTimeOptions]:checked').value")
            time.sleep(1)
            self.action_ele.click_element("report_next_button")
            formatOption = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=rbtformattype]:checked').value")
            textFile = self.query_ele.get_value_execute_javascript("document.getElementById('txtAddFilename').value")
            self.action_ele.click_element("report_next_button")
            subjectText = self.query_ele.get_value_execute_javascript("document.getElementById('txtsubject').value")
            if reportType == params["standardRecurringReportType"] and dateOption == params["standardDateOption"] and \
                    timeoption == params["standardTimeoption"] and formatOption == params["reportFormatType"] \
                    and textFile == params["textFileName"] and (subjectText == params["emailSubject"] or subjectText == params["copyReportName"] ):
                stastus = True
            else:
                console("Report Details doesn't match!!")
        except:
            raise AssertionError("Report Details doesn't match!!")
        return stastus

    def onetime_report_verification(self, params):
        """
        `Description:` To verify  onetime report details

        `Param:`  &{ReportValues}

        `:Returns`:  True/False

        `created by:` Afzal Pasha

        """
        try:
            time.sleep(5)
            stastus = False
            self.action_ele.click_element("report_next_button")
            time.sleep(1)
            self.action_ele.click_element("report_next_button")
            time.sleep(1)
            reportType = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=rbtschedule]:checked').value")
            time.sleep(1)
            dateOption = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=paramsDateOptions]:checked').value")
            timeoption = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=paramsTimeOptions]:checked').value")
            time.sleep(1)
            self.action_ele.click_element("report_next_button")
            formatOption = self.query_ele.get_value_execute_javascript("document.querySelector('input[name=rbtformattype]:checked').value")
            textFile = self.query_ele.get_value_execute_javascript("document.getElementById('txtAddFilename').value")
            self.action_ele.click_element("report_next_button")
            subjectText = self.query_ele.get_value_execute_javascript("document.getElementById('txtsubject').value")
            if reportType == params["standardOneTimeReportType"] and dateOption == params["standardDateOption"] and \
                    timeoption == params["standardTimeoption"] and formatOption == params["reportFormatType"] \
                    and textFile == params["textFileName"] and (subjectText == params["emailSubject"] or subjectText == params["copyReportName"] ):
                stastus = True
            else:
                console("Report Details doesn't match!!")
        except:
            raise AssertionError("Report Details doesn't match!!")
        return stastus


    def recurring_report_copy_click(self):
        """
        `Description:` To click on recurring report copy button

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("recurring_report_copy_report")
        time.sleep(1)

    def onetime_report_copy_click(self):
        """
        `Description:` To click on onetime report copy button

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.action_ele.click_element("onetime_report_copy_report")
        time.sleep(1)

    def recurring_report_copy_click_by_giving_report_name(self, params):
        """
        `Description:` To click Ok button after giving name to copy the recurring report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            successMessage = "Report has been copied"
            self.action_ele.input_text("text_copy_report_name", params["copyReportName"])
            time.sleep(2)
            self.action_ele.click_element("button_report_copy")
            time.sleep(5)
            if successMessage in self.query_ele.get_text("fnMessage_box_ok_text"):
                self.action_ele.click_element("fnMessage_box_ok")
                time.sleep(1)
                status = True
            else:
                self.action_ele.click_element("fnMessage_box_ok")
                status = False
        except:
            raise AssertionError("Fail to copy the report!!")
        return status

    def onetime_report_copy_click_by_giving_report_name(self, params):
        """
        `Description:` To click Ok button after giving name to copy the onetime report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            successMessage = "Report has been copied"
            self.action_ele.input_text("text_copy_report_name", params["copyReportName"])
            time.sleep(2)
            self.action_ele.click_element("button_report_copy")
            time.sleep(5)
            if successMessage in self.query_ele.get_text("fnMessage_box_ok_text"):
                self.action_ele.click_element("fnMessage_box_ok")
                time.sleep(1)
                status = True
            else:
                self.action_ele.click_element("fnMessage_box_ok")
                status = False
        except:
            raise AssertionError("Fail to copy the report!!")
        return status

    def select_recurring_report_to_edit_after_copy(self, params):
        """
        `Description:` To verify report details after copy recurring report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("recurring_tab_grid_name_filter", params["copyReportName"])
        time.sleep(1)
        self.action_ele.click_element("recurring_tab_selected_report")
        time.sleep(1)

    def select_onetime_report_to_edit_after_copy(self, params):
        """
        `Description:` To verify report details after copy onetime report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        time.sleep(1)
        self.action_ele.input_text("onetime_tab_grid_name_filter", params["copyReportName"])
        time.sleep(1)
        self.action_ele.click_element("onetime_tab_selected_report")
        time.sleep(1)