*** Settings ***
Documentation   BOSS User Grid - Add User-Set Roles when adding users (Phone Manager)
...             dev-Sameena Kauser

Resource        ../../RobotKeywords/DominatorKeywords.robot
Resource        ../../RobotKeywords/NavigationKeywords.robot
Resource        ../../RobotKeywords/BOSSKeywords.robot
Resource        ../../Variables/EnvVariables.robot

Library         ../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     Regression     Elvis      AddUser

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    # Load the JSON details into a Python Dictionary Data Structure
    ${details}=   Load JSON From File       ../Details/Users.json
    Set Suite Variable  ${usersDataGrid}    ${details["usersDataGrid"]}
    Set Suite variable  ${AddEditPersonWizard}     ${details["AddEditPersonWizard"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/Users.json
    ${values}=      Update Random Values  ${values}
    Set Suite variable    ${Fill_values}          ${values["Fill_values"]}
    Set Suite variable    ${confirmation_ok}          ${values["confirmation_ok"]}
    Set Suite variable    ${rolesandpermissions_pm}       ${values["rolesandpermissions_pm"]}

Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***

TC-221612_User Grid-Add User-Set Roles when adding users (Phone Manager).robot
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    When I move to Users page
    I click the ${usersDataGrid} adduser button
    I fill in ${AddEditPersonWizard} form with ${Fill_values}
    I click next to move the ${AddEditPersonWizard} to phone
    I click next to move the ${AddEditPersonWizard} to rolesandpermissions
    I fill in ${AddEditpersonWizard} form with ${rolesandpermissions_pm}
    And I click the ${AddEditpersonWizard} add button
    I click next to move the ${AddEditPersonWizard} to confirmation
    And I click the ${AddEditPersonWizard} finish button
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    When I move to Users page
    When I filter column headings for ${usersDataGrid} with BusinessEmail in ${Fill_values}
    Then I can find ${Fill_values["BusinessEmail"]} in the ${usersDatagrid}
