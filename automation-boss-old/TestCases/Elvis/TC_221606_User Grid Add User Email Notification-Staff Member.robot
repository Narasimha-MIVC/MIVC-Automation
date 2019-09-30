*** Settings ***
#This test case is just a copy of DM Notification .
#The Emails are always sent to Staff by default
Documentation   BOSS User Grid - Add User Email Notification- Staff Member
...             dev-Sameena Kauser

Resource        ../../RobotKeywords/DominatorKeywords.robot
Resource        ../../RobotKeywords/NavigationKeywords.robot
Resource        ../../RobotKeywords/BOSSKeywords.robot
Resource        ../../Variables/EnvVariables.robot

Library         ../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     Regression     Elvis

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    # Load the JSON details into a Python Dictionary Data Structure
    ${details}=   Load JSON From File       ../Details/Users.json
    Set Suite Variable  ${grid}             ${details["usersDataGrid"]}
    Set Suite Variable  ${usersDataGrid}    ${details["usersDataGrid"]}
    Set Suite variable  ${AddEditPersonWizard}     ${details["AddEditPersonWizard"]}

    #Load the JSON values into a Python Dictionary Data Structure
    ${values}=      Load JSON From File   ../Values/Users.json
    ${values}=      Update Random Values  ${values}

    Set Suite variable    ${Fill_values}          ${values["Fill_values"]}
    Set Suite variable    ${new_managed_phone_number}          ${values["new_managed_phone_number"]}
    Set Suite variable    ${new_managed_type_phone}          ${values["new_managed_type_phone"]}
    Set Suite variable    ${new_managed_phone_activation_date}          ${values["new_managed_phone_activation_date"]}
    Set Suite variable    ${rolesandpermissions_dm}       ${values["rolesandpermissions_dm"]}
    Set Suite variable    ${confirmation_for_requestsource}       ${values["confirmation_for_requestsource"]}
    Set Suite variable    ${confirmation_for_requestby_dm}       ${values["confirmation_for_requestby_dm"]}


Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***

TC-221606_User Grid-Add User Email Notification-Staff Member
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with ${AccWithoutLogin} option
    When I move to Users page
    I click the ${usersDataGrid} adduser button
    I fill in ${AddEditPersonWizard} form with ${Fill_values}
    I click next to move the ${AddEditPersonWizard} to phone
    I fill in ${AddEditpersonWizard} form with ${new_managed_type_phone}
    I fill in ${AddEditpersonWizard} form with ${new_managed_phone_number}
    I fill in ${AddEditpersonWizard} form with ${new_managed_phone_activation_date}
    I click next to move the ${AddEditPersonWizard} to hardware
    I click next to move the ${AddEditPersonWizard} to rolesandpermissions
    I fill in ${AddEditpersonWizard} form with ${rolesandpermissions_dm}
    And I click the ${AddEditpersonWizard} add button
    I click next to move the ${AddEditPersonWizard} to confirmation
    I fill in ${AddEditpersonWizard} form with ${confirmation_for_requestsource}
    I fill in ${AddEditpersonWizard} form with ${confirmation_for_requestby_dm}
    And I click the ${AddEditPersonWizard} finish button