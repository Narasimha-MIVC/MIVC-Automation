*** Settings ***
Documentation   BOSS Personal Contacts - Exercise Personal Contacts Processing
...             dev-Randall Arlitt

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
    ${details}=   Load JSON From File       ../Details/PersonalContactsElvis.json
    Set Suite Variable  ${grid}             ${details["grid"]}
    Set Suite Variable  ${add_form}         ${details["add"]}


    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/PersonalContactsElvis.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable    ${add_ok}         ${values["add_ok"]}
    Set Suite Variable    ${add_fail}       ${values["add_fail"]}


And I cancel the ${add_form} form with the cancel button
    Log    This is I cancel the ${add_form} form with the cancel button


Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***


TC-221104 - Verify mandatory fields for adding new Personal Contact
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    And I move to Personal Contacts page
    When I click the ${grid} add button
    Then I fail the ${add_form} form with the cancel button
    And I cancel the ${add_form} form with the cancel button