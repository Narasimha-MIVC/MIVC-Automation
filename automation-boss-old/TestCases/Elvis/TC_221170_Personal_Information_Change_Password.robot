*** Settings ***
Documentation   Personal Information page testcases for Elvis


Resource        ../../RobotKeywords/DominatorKeywords.robot
Resource        ../../RobotKeywords/NavigationKeywords.robot

Resource        ../../RobotKeywords/BOSSKeywords.robot
Resource        ../../Variables/EnvVariables.robot

Library         ../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     regression    Elvis

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    # Load the JSON details into a Python Dictionary Data Structure
    ${details}=   Load JSON From File       ../Details/PersonalInformation.json
    Set Suite Variable  ${formPersonDetails}        ${details["formPersonDetails"]}
    Set Suite Variable  ${edit_in_place}            ${details["edit_in_place"]}
    Set Suite Variable  ${changePersonPassword}     ${details["changePersonPassword"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=          Load JSON From File         ../Values/PersonalInformation.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=          Update Random Values        ${values}
    Set Suite Variable  ${changePersonPassword_ok}  ${values["changePersonPassword_ok"]}
    Set Suite Variable  ${changePersonPassword_orig}  ${values["changePersonPassword_orig"]}




Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers


*** Test Cases ***

TC221170 - Personal Information - Change Password
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    And I move to Personal Information page
    When I click the ${edit_in_place} changepassword button
    And I Fill In ${changePersonPassword} Form With ${changePersonPassword_ok}
    Then I save the ${changePersonPassword} form with the ok button
    and I click ok for the generic confirmation dialog

#Revert TC221170 values for next run
    Given I click the ${edit_in_place} changepassword button
    And I Fill In ${changePersonPassword} Form With ${changePersonPassword_orig}
    When I save the ${changePersonPassword} form with the ok button
    Then I click ok for the generic confirmation dialog