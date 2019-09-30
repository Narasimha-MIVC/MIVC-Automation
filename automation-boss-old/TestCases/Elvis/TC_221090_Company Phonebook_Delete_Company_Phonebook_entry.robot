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
    ${details}=   Load JSON From File       ../Details/CompanyPhonebook.json
    Set Suite Variable  ${grid}             ${details["companyDirectoryDataGrid"]}
    Set Suite Variable  ${add_form}         ${details["directory_form"]}


    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/CompanyPhonebook.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable    ${edit_ok}         ${values["edit_ok"]}


Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***

TC-221190 - Company Phonebook - Delete Company Phonebook entry
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    And I move to Company Phonebook page
    When I click delete to delete from ${grid} with DisplayName in ${edit_ok}
    and I Click yes ok For The Generic Confirmation Dialog
    Then I cannot find Test Name2 in the ${grid}