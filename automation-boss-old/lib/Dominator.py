
class Dominator(object):

    def update_random_values(self, values):
        """
        Description: Randomizes Dictionary values using 'text|type|length' format

        :Param1 values: Dictionary of form values

        :Return: Dictionary containing randomized values

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.update_random_values(values)
        except Exception as e:
            print(e, "Randomizing form values has failed")

    def validate_component_with_json(self, component_type, details, values):
        """
        Description: FUTURE: Currently only checks component for JavaScript errors

        :Param1 component_type: Component type (grid, form, wizard, edit-in-place, etc)

        :Param2 details: Dictionary of the component definitions

        :Param3 values: Dictionary of values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.validate_component_with_json(component_type, details, values)
        except Exception as e:
            print(e, "Validating component has failed", component_type)

    def verify_component_state_with_json(self, component, state):
        """
        Description: Verifies that the specified component is in the specified state

        :Param1 component: Dictionary of component definition

        :Param2 state: String containing the expected state (enabled/disabled/hidden/visible/found/missing)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.verify_component_state_with_json(component, state)
        except Exception as e:
            print(e, "Verifying component state has failed", state)

    def confirm_component_text_with_json(self, component, text, expect):
        """
        Description: Confirms that the specified component contains the specified text

        :Param1 component: Dictionary of component definition

        :Param2 text: String containing the text to be found in the component

        :Param3 expect: String that contains the expected result (does/does not)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.confirm_component_text_with_json(component, text, expect)
        except Exception as e:
            print(e, "Confirming component text has failed")

    def update_form_with_json(self, form, values):
        """
        Description: Updates form with the specified values

        :Param1 form: Dictionary of form definitions

        :Param2 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.update_form_with_json(form, values)
        except Exception as e:
            print(e, "Updating form has failed", form, values)
            
    def update_field_with_json(self, field, value):
        """
        Description: Updates field with the specified value

        :Param1 field: Dictionary of field definition

        :Param2 value: String of field value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.update_field_with_json(field, value)
        except Exception as e:
            print(e, "Updating field has failed", field, value)

    def conclude_form_with_json(self, form, action, button):
        """
        Description: Finalizes form with the specified action and button

        :Param1 form: Dictionary of form definitions

        :Param2 action: String that contains the action to perform(fail, save)

        :Param3 button: String that contains the name of the button to click

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.conclude_form_with_json(form, action, button)
        except Exception as e:
            print(e, "Action: " + action + " for form has failed")

    def edit_in_place_with_json(self, fields, values, action):
        """
        Description: Updates form with the specified values

        :Param1 fields: Dictionary of edit in place field definitions

        :Param2 values: Dictionary of field values

        :Param3 action: String that contains the button action to perform(submit, cancel)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.edit_in_place_with_json(fields, values, action)
        except Exception as e:
            print(e, "Action: " + action + " for edit in place has failed")

    def click_grid_button_with_json(self, grid, button):
        """
        Description: Clicks the specified button and performs any validation required

        :Param1 grid: Dictionary of grid definitions

        :Param2 button: String that contains the name of the button to click

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.click_grid_button_with_json(grid, button)
        except Exception as e:
            print(e, "Button: " + button + "click has failed")

    def delete_from_grid_with_json(self, button, grid, field, values):
        """
        Description: Filters the grid with the specified parameters and performs any validation required

        :Param1 button: String that contains the name of the button to click

        :Param2 grid: Dictionary of grid definitions

        :Param3 field: String that contains the name of the field to filter

        :Param4 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.delete_from_grid_with_json(button, grid, field, values)
        except Exception as e:
            print(e, "Delete: for grid has failed")

    def show_contextmenu_from_grid_with_json(self, grid, field, values):
        """
        Description: Filters the grid with the specified parameters and shows the context menu

        :Param1 grid: Dictionary of grid definitions

        :Param2 field: String that contains the name of the field to filter

        :Param3 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.show_contextmenu_from_grid_with_json(grid, field, values)
        except Exception as e:
            print(e, "Context Menu: for grid has failed")

    def choose_contextmenuitem_from_grid_with_json(self, contextitems, menu_item, expect):
        """
        Description: Validates the context menu item and clicks if expected = 'can'

        :Param1 contextitems: Dictionary of grid context menu definitions

        :Param2 menu_item: String that contains the name of the context menu item to click

        :Param3 expect: String that contains the expected result (can/can not)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.choose_contextmenuitem_from_grid_with_json(contextitems, menu_item, expect)
        except Exception as e:
            print(e, "Context Menu Item: for grid has failed")

    def filter_grid_header_with_json(self, grid, field, values):
        """
        Description: Filters the grid with the specified parameters and selects one or more rows

        :Param1 grid: Dictionary of grid definitions

        :Param2 field: String that contains the name of the field to filter

        :Param3 values: Dictionary of form values

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.filter_grid_header_with_json(grid, field, values)
        except Exception as e:
            print(e, "Filtering grid header for " + field + " has failed")

    def filter_grid_with_json(self, grid, field, value):
        """
        Description: Filters the grid with the specified parameters

        :Param1 grid: Dictionary of grid definition

        :Param2 field: String that contains the name of the field to filter

        :Param3 value: String that contains the filter value

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.filter_grid_with_json(grid, field, value)
        except Exception as e:
            print(e, "Filtering grid for " + field + " has failed")

    def select_grid_row_with_json(self, grid, count):
        """
        Description: Filters the grid with the specified parameters and selects one or more rows

        :Param1 grid: Dictionary of grid definitions

        :Param2 count: Mixed either all, none or an integer of the number of rows to select

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.select_grid_row_with_json(grid, count)
        except Exception as e:
            print(e, "Select " + count + " for grid has failed")

    def find_value_in_grid_rows_with_json(self, grid, value, expect):
        """
        Description: Find the specified value in the grid

        :Param1 grid: Dictionary of grid definitions

        :Param2 value: String that contains the value to find

        :Param3 expect: String that contains the expected result (can/cannot)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.find_value_in_grid_rows_with_json(grid, value, expect)
        except Exception as e:
            print(e, "Find (" + expect + ") " + value + " in grid has failed")

    def click_grid_cell_with_json(self, grid, item, field, value):
        """
        Description: Click the text or icon in the specified cell of the grid

        :Param1 grid: Dictionary of grid definitions

        :Param2 item: String that contains the element to click (text/icon)

        :Param3 column: String that contains the column to search

        :Param4 value: String that contains the value to find

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.click_grid_cell_with_json(grid, item, field, value)
        except Exception as e:
            print(e, "Click grid cell has failed")

    def clear_all_grid_filters_with_json(self, grid):
        """
        Description: Clear all grid filters

        :Param1 grid: Dictionary of grid definitions

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.clear_all_grid_filters_with_json(grid)
        except Exception as e:
            print(e, "Clearing grid filters has failed")

    def handle_generic_confirmation_dialog(self, button):
        """
        Description: Handles the generic confirmation dialog with the specified button

        :Param1 button: String that contains the name of the button to click

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.handle_generic_confirmation_dialog(button)
        except Exception as e:
            print(e, "The " + button + " for the generic confirmation dialog has failed")

    def wizard_go_to_step_with_json(self, wizard, button, step):
        """
        Description: Move to the specified wizard step using the specified button

        :Param1 wizard: Dictionary of wizard definitions

        :Param2 button: String that contains the name of the button item to click (next/back)

        :Param3 step: String that contains the expected step definition

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.wizard_go_to_step_with_json(wizard, button, step)
        except Exception as e:
            print(e, "The " + button + " for the wizard change to " + step + "  has failed")
        return True

    def wizard_finalize_with_json(self, wizard, button, include):
        """
        Description: Finish/Cancel the wizard step using the specified button

        :Param1 wizard: Dictionary of wizard definitions

        :Param2 button: String that contains the name of the button item to click (finish/cancel)

        :Return: Boolean of execution results

        Created by: Jim Wendt
        """
        try:
            return self.boss_page.dominator.wizard_finalize_with_json(wizard, button, include)
        except Exception as e:
            print(e, "The " + button + " for the wizard has failed")
        return True
