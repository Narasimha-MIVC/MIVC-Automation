*** Settings ***
Documentation   BOSS - Geographic Locations
...             dev-Randall Arlitt

Resource        ../../RobotKeywords/DominatorKeywords.robot
Resource        ../../RobotKeywords/NavigationKeywords.robot
Resource        ../../RobotKeywords/BOSSKeywords.robot
Resource        ../../Variables/LoginDetails_Elvis.robot

Library         ../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     Regression     Elvis      GeographicLocations

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***
Initialize Environment
    # Load the JSON details into a Python Dictionary Data Structure
    ${details}=   Load JSON From File       ../Details/EmergencyRegistration.json
    Set Suite Variable  ${grid}             ${details["locationRegistrationGrid"]}
    Set Suite Variable  ${contextitems}     ${grid["contextitems"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/EmergencyRegistration.json
    Set Suite Variable    ${E911_change}         ${values["E911_change"]}

Finalize Environment
    Log Off
    Close The Browsers

*** Test Cases ***
221550 - Geographic Locations - Edit E911 phone number for location
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with ${AccWithoutLogin} option
    And I move to Emergency Registration page
    When I filter column headings for ${grid} with Name in ${E911_change}
    and I show the context menu for ${grid} with Name in ${E911_change}
    and I can choose the update item from the grid context menu ${contextitems}
    and I click on "//*[@id="updateLocationRegistrationForm"]/div/fieldset/div[3]/button[1]/span" button/link
    and I Click On "//*[@id="fnMessageBox_OK"]/span" Button/link
    Then I can find Registered in the ${grid}
