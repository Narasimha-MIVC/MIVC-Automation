*** Settings ***
Documentation    Add custom schedule without timezone and validate the error message
...              Saurabh Singh

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String
*** Test Cases ***
Create custom schedule with DM account
    [Tags]    CS    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule05}
    [Teardown]  run keywords
    ...                      I log off
    ...                      I check for alert

Create custom schedule with PM account
    #When I check for alert
     [Tags]    Regression       CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule06}
    [Teardown]  run keywords
    ...                      I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule05}

    : FOR    ${key}    IN    @{CustomSchedule05.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule05["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule05}    ${key}    ${updated_val}

     : FOR    ${key}    IN    @{CustomSchedule06.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule06["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule06}    ${key}    ${updated_val}
