"""Module for ECC portal functionalities
   Developer: Afzal Pasha
"""


class ECCComponent(object):
    ''' ECC Component Interface to interact with the ROBOT keywords
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def ecc_activate_click(self, **params):
        """
        `Description:` To click on Add-on features --> ECC --> Activate

        `Param:`  &{Settings}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            self.boss_page.ecc_handler.ecc_activate_click(params)

        except:
            print("Could not click on ECC Activate button")
            raise AssertionError("Click on ECC Activate Failed!!")

    def ecc_activate_review_click(self, **params):
        """
        `Description:` To view summary screen

        `Param:`  &{Settings}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            self.boss_page.ecc_handler.ecc_activate_review_click(params)
        except:
            print("Could not click on ECC Review button")
            raise AssertionError("Click on ECC Review Failed!!")


    def ecc_ok_click(self):
        """
        `Description:` To submit all values

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            self.boss_page.ecc_handler.ecc_OK_click()
        except:
            raise AssertionError("Failed to update Contact Center settings.")

    def report_recurring_tab_click(self):
        """
        `Description:` To click on recurring tab

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_recurring_tab_click()

    def report_onetime_tab_click(self):
        """
        `Description:` To click on onetime tab

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_onetime_tab_click()

    def recurring_report_add_click(self):
        """
        `Description:` To add recurring report click Add button

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            self.boss_page.ecc_handler.recurring_report_add_click()
        except:
            raise AssertionError("Failed to Load Report Templates/Fields")

    def onetime_report_add_click(self):
        """
        `Description:` To add onetime report click Add button

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            self.boss_page.ecc_handler.onetime_report_add_click()
        except:
            raise AssertionError("Failed to Load Report Templates/Fields")

    def report_enter_fieldvalues(self, **params):
        """
        `Description:` enter all filed values while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            self.boss_page.ecc_handler.report_enter_fieldvalues(params)
        except:
            raise AssertionError("Failed to Load Report Templates/Fields")

    def report_select_entities(self):
        """
        `Description:` To check all checkboxes of Agents...

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_select_entities()

    def report_select_reporttype(self, **params):
        """
        `Description:` To select report type while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_select_reporttype(params)

    def report_select_datetime(self):
        """
        `Description:` To select date time while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_select_datetime()

    def report_select_formatfile(self, **params):
        """
        `Description:` To select format type while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_select_formatfile(params)

    def report_enter_delivery_details(self, **params):
        """
        `Description:` To enter delivery details while creating report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_enter_delivery_details(params)

    def report_next_click(self):
        """
        `Description:` To click on next button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_next_click()

    def report_back_click(self):
        """
        `Description:` To click on back button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_back_click()

    def report_cancel_click(self):
        """
        `Description:` To click on cancel button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.report_cancel_click()

    def report_finish_click(self):
        """
        `Description:` To click on finish button while creating report

        `Param:`  None

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            status = self.boss_page.ecc_handler.report_finish_click()
            return status
        except:
            raise AssertionError("Failed to schedule the report!!")

    def recurring_report_exists_check(self, **params):
        """
        `Description:` To check whether recurring report exists

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.recurring_report_exists_check(params)

    def onetime_report_exists_check(self, **params):
        """
        `Description:` To check whether onetime report exists

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.onetime_report_exists_check(params)

    def select_recurring_report_to_edit(self, **params):
        """
        `Description:` Select recurring report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_recurring_report_to_edit(params)

    def select_onetime_report_to_edit(self, **params):
        """
        `Description:` Select onetime report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_onetime_report_to_edit(params)

    def recurring_report_edit_click(self):
        """
        `Description:` To click on edit button after select recurring report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.recurring_report_edit_click()

    def onetime_report_edit_click(self):
        """
        `Description:` To click on edit button after select onetime report to edit

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.onetime_report_edit_click()

    def select_recurring_report_to_delete(self, **params):
        """
        `Description:` To select onetime report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_recurring_report_to_delete(params)

    def select_onetime_report_to_delete(self, **params):
        """
        `Description:` To select onetime report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_onetime_report_to_delete(params)

    def recurring_report_delete_click(self):
        """
        `Description:` To click on delete button after select recurring report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        status = self.boss_page.ecc_handler.recurring_report_delete_click()
        return status

    def onetime_report_delete_click(self):
        """
        `Description:` To click on delete button after select onetime report to delete

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.onetime_report_delete_click()

    def recurring_report_verification(self, **params):
        """
        `Description:` To verify  recurring report details

        `Param:`  &{ReportValues}

        `:Returns`:  True/False

        `created by:` Afzal Pasha

        """
        status = self.boss_page.ecc_handler.recurring_report_verification(params)
        return status

    def onetime_report_verification(self, **params):
        """
        `Description:` To verify  onetime report details

        `Param:`  &{ReportValues}

        `:Returns`:  True/False

        `created by:` Afzal Pasha

        """
        status = self.boss_page.ecc_handler.onetime_report_verification(params)
        return status

    def select_recurring_report_to_copy(self, **params):
        """
        `Description:` To recurring report to copy

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_recurring_report_to_copy(params)

    def select_onetime_report_to_copy(self, **params):
        """
        `Description:` To onetime report to copy

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_onetime_report_to_copy(params)

    def recurring_report_copy_click(self):
        """
        `Description:` To click on recurring report copy button

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.recurring_report_copy_click()


    def onetime_report_copy_click(self):
        """
        `Description:` To click on onetime report copy button

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.onetime_report_copy_click()

    def recurring_report_copy_click_by_giving_report_name(self, **params):
        """
        `Description:` To click Ok button after giving name to copy the recurring report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            status = self.boss_page.ecc_handler.recurring_report_copy_click_by_giving_report_name(params)
            return status
        except:
            raise AssertionError("Failed to copy the report!!")

    def onetime_report_copy_click_by_giving_report_name(self, **params):
        """
        `Description:` To click Ok button after giving name to copy the onetime report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        try:
            status = self.boss_page.ecc_handler.onetime_report_copy_click_by_giving_report_name(params)
            return status
        except:
            raise AssertionError("Failed to copy the report!!")

    def select_recurring_report_to_edit_after_copy(self, **params):
        """
        `Description:` To verify report details after copy recurring report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_recurring_report_to_edit_after_copy(params)

    def select_onetime_report_to_edit_after_copy(self, **params):
        """
        `Description:` To verify report details after copy onetime report

        `Param:`  &{ReportValues}

        `:Returns`:  None

        `created by:` Afzal Pasha

        """
        self.boss_page.ecc_handler.select_onetime_report_to_edit_after_copy(params)