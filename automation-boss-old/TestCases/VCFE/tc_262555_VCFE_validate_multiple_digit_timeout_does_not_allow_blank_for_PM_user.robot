*** Settings ***
Documentation  Regression
...            Validate multiple digit time out does not allow blank for PM
...            Palla Surya Kumar

#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/AutoAttendantInfo.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
Validate multiple digit time out does not allow blank for PM
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I add Auto-Attendant with blank multiple digit timeout value    &{AA_11}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
