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
As a PM create another geographic location
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    and I switch to "geographic_locations" page
    and I create geographic location    &{geolocation01}
    Then I verify location "${geolocation01['Location']}" with "Registered" state
    [Teardown]  run keywords  I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_str2}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${geolocation01}

    : FOR    ${key}    IN    @{geolocation01.keys()}
    \    ${updated_val}=    Replace String    ${geolocation01["${key}"]}    {rand_str}    ${uni_str2}
    \    Set To Dictionary    ${geolocation01}    ${key}    ${updated_val}
