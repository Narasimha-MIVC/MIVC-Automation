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

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     ../Values/GeographicLocations.json
    Set Suite Variable    ${test_values}         ${values["test_values"]}


Finalize Environment
    Stop Impersonating
    Log Off
    Close The Browsers

*** Test Cases ***
221551 - Geographic Locations - Filter and Sort
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account Automation_Elvis with Automation_Elvis Account option
    And I move to Geographic Locations page
    When I filter column headings for ${grid} with LabelFormatted in ${test_values}
    And I filter column headings for ${grid} with Status in ${test_values}
    And I filter column headings for ${grid} with FullAddress in ${test_values}
    Then I can find Austin in the ${grid}