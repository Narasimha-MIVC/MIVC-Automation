"""Module for all Navigation actions"""

import os
import inspect
import json
from log import log
import web_wrappers.selenium_wrappers as base

__author__ = "Jim Wendt"


class Navigation(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        # Load navigation details
        base_path = os.environ["PYTHONPATH"].split(os.pathsep)[0] + os.path.sep
        with open(base_path + os.path.join("..", "automation-boss", "Values", "Navigation.json")) as json_data:
            self.pages = json.load(json_data)

    def show_menu(self, locator):
        """
        Description: Routine to show a navigation menu/sub-menu

        Param1:  locator - XPath of menu display

        Returns:  status - True/False

        Created by: Jim Wendt
        """
        status = False
        try:
            if locator.find("button") != -1:
                self.action_ele.click_element(locator)
            else:
                self.action_ele.mouse_hover(locator)

            menu = self._browser.element_finder(locator)
            offset_left = menu.get_attribute('offsetLeft')
            if offset_left < -1:
                return status
            status = True
            return status
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def navigate_to_page(self, page_name):
        """
        Description: Routine to navigate from a menu/sub-menu

        Param:  pageName

        Returns:  status - True/False

        Created by: Jim Wendt
        """
        status = False
        try:
            page = page_name.lower()
            if not self.pages[page]["locator"]:
                raise Exception("The " + page_name + " page does not have a locator configured")

            # Loop through the menu array to show all
            for menu in self.pages[page]["menu"]:
                self.show_menu(menu)

            # Click the navigation item
            self.action_ele.click_element(self.pages[page]["locator"])

            # Handle the expected page
            if self.pages[page]["external"] == "false":

                # Wait for Ajax to complete
                self._browser.waitfor_ajax_complete()

                # Wait for the expected page
                self.action_ele.explicit_wait(self.pages[page]["expect"])

                # Verify no JavaScript errors have occurred
                self.assert_ele.page_should_not_contain_javascript_errors()

            elif self.pages[page]["external"] == "true" and self.action_ele.window_handles_count() > 1:
                self.action_ele.switch_to_window(1)
                self.action_ele.explicit_wait(self.pages[page]["expect"])
                self.action_ele.close_window()
                self.action_ele.switch_to_window(0)
            else:
                raise Exception("The " + page_name + " page does not have validation configured")

            status = True
            return status
        except Exception as err:
            # Check for error conditions
            error_block = self._browser.elements_finder(self.pages["error block"]["locator"])
            error_dialog = self._browser.elements_finder(self.pages["error dialog"]["locator"])
            if len(error_block) > 0 or len(error_dialog) > 0:
                log.mjLog.LogReporter("Navigation", "error", "The " + page_name + " page is exiting with an error")
            else:
                print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status