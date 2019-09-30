*** Settings ***

Library     Collections
Library     String

*** Keywords ***
#
# Common Keywords
#
Update Random Values ${values}
    ${values}=  Run Keyword  update_random_values  ${values}
    [Return]    ${values}

I validate the ${details} as a ${component_type:(form|grid)} with ${values}
    ${result}=  Run Keyword   validate_component_with_json  ${component_type}  ${details}  ${values}
    Should be True    ${result}

I click ${button} for the generic confirmation dialog
    ${result}=  Run Keyword  handle_generic_confirmation_dialog  ${button}
    Should be True    ${result}

I verify ${component} state is ${state:(enabled|disabled|hidden|visible|found|missing)}
    ${result}=  Run Keyword   verify_component_state_with_json  ${component}  ${state}
    Should be True    ${result}

I confirm ${component} ${expect:(does|does not)} contain the text ${text}
    ${result}=  Run Keyword   confirm_component_text_with_json  ${component}  ${text}  ${expect}
    Should be True    ${result}

#
# Form Specific Keywords
#
I fill in ${form} form with ${values}
    ${result}=  Run Keyword   update_form_with_json  ${form}  ${values}
    Should be True    ${result}

I update field ${field} with ${value}
    ${result}=  Run Keyword   update_field_with_json  ${field}  ${value}
    Should be True    ${result}

I ${action:(cancel|fail|save)} the ${form} form with the ${button} button
    ${result}=  Run Keyword  conclude_form_with_json  ${form}  ${action}  ${button}
    Should be True    ${result}

#
# Edit in Place Specific Keywords
#
I edit in place ${fields} with ${values} and ${action:(cancel|fail|save)}
    ${result}=  Run Keyword   edit_in_place_with_json  ${fields}  ${values}  ${action}
    Should be True    ${result}

#
# Grid Specific Keywords
#
I click the ${grid} ${button} button
    ${result}=  Run Keyword  click_grid_button_with_json  ${grid}  ${button}
    Should be True    ${result}

I click ${button} to delete from ${grid} with ${field} in ${values}
    ${result}=  Run Keyword  delete_from_grid_with_json  ${button}  ${grid}  ${field}  ${values}
    Should be True    ${result}

I filter column headings for ${grid} with ${field} in ${values}
    ${result}=  Run Keyword  filter_grid_header_with_json  ${grid}  ${field}  ${values}
    Should be True    ${result}

I filter the ${grid} with ${field} and value of ${value}
    ${result}=  Run Keyword  filter_grid_with_json  ${grid}  ${field}  ${value}
    Should be True    ${result}

I clear all ${grid} filters
    ${result}=  Run Keyword  clear_all_grid_filters_with_json  ${grid}
    Should be True    ${result}

I select ${count} ${rows:(row|rows)} from ${grid}
    ${result}=  Run Keyword  select_grid_row_with_json  ${grid}  ${count}
    Should be True    ${result}

I show the context menu for ${grid} with ${field} in ${values}
    ${result}=  Run Keyword  show_contextmenu_from_grid_with_json  ${grid}  ${field}  ${values}
    Should be True    ${result}

I ${expect:(can|cannot)} choose the ${menu_item} item from the grid context menu ${contextitems}
    ${result}=  Run Keyword  choose_contextmenuitem_from_grid_with_json  ${contextitems}  ${menu_item}  ${expect}
    Should be True    ${result}

I ${expect:(can|cannot)} find ${value} in the ${grid}
    ${result}=  Run Keyword  find_value_in_grid_rows_with_json  ${grid}  ${value}  ${expect}
    Should be True    ${result}

I click the ${grid} cell ${item:(text|icon)} where ${field} equals ${value}
    ${result}=  Run Keyword  click_grid_cell_with_json  ${grid}  ${item}  ${field}  ${value}
    Should be True    ${result}

#
# Wizard Specific Keywords
#
I click ${button:(next|back)} to move the ${wizard} to ${step}
    ${result}=  Run Keyword  wizard_go_to_step_with_json  ${wizard}  ${button}  ${step}
    Should be True    ${result}

I ${button:(cancel|finish)} the ${wizard} ${include:(with|without)} confirmation
    ${result}=  Run Keyword  wizard_finalize_with_json  ${wizard}  ${button}  ${include}
    Should be True    ${result}