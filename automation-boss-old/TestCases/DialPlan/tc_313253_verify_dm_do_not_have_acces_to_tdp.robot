*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify only staff has access to dial plan and permissions to change and edit Trunk Access Codes in
...                 Dial plan.
...              Palla Surya Kumar

Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String


*** Test Cases ***
As a DM verify whether he has access to dial plan and permissions to change and edit Trunk Access Codes in Dial plan.
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I verify tabs not exist    Operations
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
