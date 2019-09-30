*** Settings ***
Documentation   BOSS Personal Contacts - Exercise Personal Contacts Processing
...             dev-Jim Wendt

Resource        ../RobotKeywords/DominatorKeywords.robot
Resource        ../RobotKeywords/NavigationKeywords.robot

Resource        ../RobotKeywords/BOSSKeywords.robot
Resource        ../Variables/EnvVariables.robot

Library         ../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     regression

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    # Load the JSON details into a Python Dictionary Data Structure
    ${details}=   Load JSON From File       ../Details/PersonalContacts.json
    Set Suite Variable  ${grid}             ${details["grid"]}
    Set Suite Variable  ${add_form}         ${details["add"]}
    Set Suite Variable  ${edit_form}        ${details["edit"]}
    Set Suite Variable  ${addgroup_form}    ${details["addgroup"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/PersonalContacts.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable    ${add_ok}         ${values["add_ok"]}
    Set Suite Variable    ${add_fail}       ${values["add_fail"]}
    Set Suite Variable    ${edit_ok}        ${values["edit_ok"]}
    Set Suite Variable    ${edit_fail}      ${values["edit_fail"]}
    Set Suite Variable    ${addgroup_ok}    ${values["addgroup_ok"]}
    Set Suite Variable    ${addgroup_fail}  ${values["addgroup_fail"]}

Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***

Setup JSON Proof of Concept
    # Liberties taken here for proof of concept that would not be acceptable in production
    Given I login to ${localHost} with ${bossUsername} and ${bossPassword}
    Then I switch to "switch_account" page
    And I switch to account Highball Report Testing with Brett Gardner option
    And I move to Personal Contacts page
    # Then I validate the ${grid} as a grid with no values

Validate Add Form
    Given I validate the ${add_form} as a form with ${add_ok}
    When I click the ${grid} add button
    Then I cancel the ${add_form} form with the cancel button

# Verify Add Failure
    # Given I click the ${grid} add button
    # When I fill in ${add_form} form with ${add_fail}
    # And I fail the ${add_form} form with the ok button
    # And I cancel the ${add_form} form with the cancel button

Verify Add Success
    Given I click the ${grid} add button
    Then I fill in ${add_form} form with ${add_ok}
    And I save the ${add_form} form with the ok button

# Filter the Grid
    # Given I move to Personal Contacts page
    # When I filter ${grid} with LastName in ${add_ok}
# Select All Rows
    # Then I select all rows from ${grid}
# Select No Rows
    # Then I select no rows from ${grid}
# Select 1 Rows
    # When I select 1 row from ${grid}
    # Then I select no rows from ${grid}
# Select 2 Rows
    # When I select 2 rows from ${grid}
    # Then I select no rows from ${grid}

# Select Update From Context Menu
    # When I show the context menu for ${grid} with LastName in ${edit_ok}
    # Then I can choose the Update item from the grid context menu ${grid["contextitems"]}
    # And I cancel the ${edit_form} form with the cancel button

# Select Delete
    # When I show the context menu for ${grid} with LastName in ${edit_ok}
    # Then I can't choose the Delete item from the grid context menu ${grid["contextitems"]}

# Validate Edit Form
    # Given I move to Personal Contacts page
    # When I filter ${grid} with LastName in ${add_ok}
    # Then I select 1 row from ${grid}
    # And I click the ${grid} update button
    # Then I validate the ${edit_form} as a form with ${edit_ok}
    # And I cancel the ${edit_form} form with the cancel button

# Verify Edit Failure
    # Given I click the ${grid} update button
    # Then I fill in ${edit_form} form with ${edit_fail}
    # And I fail the ${edit_form} form with the ok button
    # And I cancel the ${edit_form} form with the cancel button

# Verify Edit Success
    # Given I click the ${grid} update button
    # Then I fill in ${edit_form} form with ${edit_ok}
    # And I save the ${edit_form} form with the ok button

Verify Delete Success
    Given I move to Personal Contacts page
    When I filter ${grid} with LastName in ${add_ok}
    Then I click delete to delete from ${grid} with LastName in ${edit_ok}
