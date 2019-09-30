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
    Set Suite Variable  ${edit_form}        ${details["edit"]}


    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/PersonalContactsElvis.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable    ${edit_ok}        ${values["edit_ok"]}


Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers


*** Test Cases ***


TC-221107 - Verify the user is able to update Personal Contacts
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    And I move to Personal Contacts page
    When I select 1 row from ${grid}
    And I click the ${grid} update button
    And I fill in ${edit_form} form with ${edit_ok}
    Then I save the ${edit_form} form with the ok button

TC-221108 - Verify user is able to delete Personal Contacts
    Given I move to Personal Contacts page
    When I click delete to delete from ${grid} with DisplayName in ${edit_ok}
    Then I cannot find Name2 in the ${grid}

