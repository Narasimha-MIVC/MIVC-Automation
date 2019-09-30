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
    ${details}=   Load JSON From File       ../Details/GeographicLocations.json
    Set Suite Variable  ${grid}             ${details["accountLocations"]}
    Set Suite Variable  ${wizard}           ${details["LocationDetailsWizard"]}


    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/GeographicLocations.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable    ${update_values}         ${values["update_values"]}

Finalize Environment
    Log Off
    Close The Browsers

*** Test Cases ***
221544 - Geographic Locations - Edit and Map Location
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with ${AccWithoutLogin} option
    And I move to Geographic Locations page
    When I filter column headings for ${grid} with LabelFormatted in ${update_values}
    and I show the context menu for ${grid} with LabelFormatted in ${update_values}
    and I can choose the editdetails item from the grid context menu ${grid["contextitems"]}
    Then I click the ${wizard} mapit button