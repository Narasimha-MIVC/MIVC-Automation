*** Settings ***
Documentation  Login To Boss Portal And Add an Auto Attendant with blank extension.
...            Mahesh

#Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files

Resource          ../../Variables/AutoAttendantInfo.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
01 Add Auto Attendant With Blank Extension as DM User
    [Tags]    AA    Regression    AUS    UK    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I add Auto-Attendant with blank extension   &{AA_00}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


02 Add Auto Attendant With Blank Extension as PM User
    [Tags]    AA    Regression    AUS    UK
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I add Auto-Attendant with blank extension   &{AA_00}
   [Teardown]  run keywords  I log off
    ...                       I check for alert
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{AA_01}
    : FOR    ${key}    IN    @{AA_00.keys()}
    \    ${updated_val}=    Replace String    ${AA_00["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_00}    ${key}    ${updated_val}