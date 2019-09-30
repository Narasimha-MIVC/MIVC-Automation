*** Settings ***
Documentation   BOSS User Grid - Add User as DM-PM - Add User with Profile , but no add on features
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

    Set Suite Variable  ${usersDataGrid}    ${details["usersDataGrid"]}
    Set Suite variable  ${AddEditPersonWizard}     ${details["AddEditPersonWizard"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/Users.json
    ${values}=      Update Random Values  ${values}


    Set Suite variable    ${Fill_values}          ${values["Fill_values"]}
    Set Suite variable    ${new_managed_phone_number}          ${values["new_managed_phone_number"]}
    Set Suite variable    ${new_managed_type_phone}          ${values["new_managed_type_phone"]}
    Set Suite variable    ${new_managed_phone_activation_date}          ${values["new_managed_phone_activation_date"]}
    Set Suite variable    ${rolesandpermissions_dm}       ${values["rolesandpermissions_dm"]}


Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***

TC-221604_User Grid-Add User as DM-PM - Add User with Profile , but no add on features
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
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
    And I click the ${AddEditPersonWizard} finish button