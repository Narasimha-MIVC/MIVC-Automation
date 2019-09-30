*** Settings ***
Documentation   Personal Information page testcases for Elvis


Resource        ../../RobotKeywords/DominatorKeywords.robot
Resource        ../../RobotKeywords/NavigationKeywords.robot

Resource        ../../RobotKeywords/BOSSKeywords.robot
Resource        ../../Variables/EnvVariables.robot

Library         ../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     regression

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    # Load the JSON details into a Python Dictionary Data Structure
    ${details}=   Load JSON From File       ../Details/PersonalInformation.json
    Set Suite Variable  ${formPersonDetails}        ${details["formPersonDetails"]}
    Set Suite Variable  ${edit_in_place}            ${details["edit_in_place"]}


    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=          Load JSON From File         ../Values/PersonalInformation.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=          Update Random Values        ${values}
    Set Suite Variable  ${edit_in_place_ok}         ${values["edit_in_place_ok"]}
    Set Suite Variable  ${edit_in_place_orig}       ${values["edit_in_place_orig"]}

Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers


*** Test Cases ***
TC221171 - Personal Information - Update Contact Information
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    When I move to Personal Information page
    Then I edit in place ${edit_in_place} with ${edit_in_place_ok} and save
#Revert TC221171 values for next run
    When I move to Personal Information page
    Then I edit in place ${edit_in_place} with ${edit_in_place_orig} and save