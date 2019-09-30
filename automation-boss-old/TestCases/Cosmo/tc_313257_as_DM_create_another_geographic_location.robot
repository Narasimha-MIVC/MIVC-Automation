*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Create another geographic location
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/Geolocationinfo.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***
As a DM create another geographic location
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    and I switch to "geographic_locations" page
    and I create geographic location    &{geolocation_US}
    Then I verify location "${geolocation_US['Location']}" with "Registered" state
    [Teardown]  run keywords  I log off
    ...                      I check for alert
*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_str2}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${geolocation_US}

    : FOR    ${key}    IN    @{geolocation_US.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_US["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${geolocation_US}    ${key}    ${updated_val}
