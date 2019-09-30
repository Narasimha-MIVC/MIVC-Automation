*** Settings ***
Documentation    To add VCFE Pickup Group
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
Edit custom schedule with DM account
    [Tags]    Regression    CS    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule01}
    Set to Dictionary  ${EditCustomSchedule01}  editName  ${CustomSchedule01["customScheduleName"]}
    #Set to Dictionary  ${EditCustomSchedule01}  editName  DM_Custom_01_DBn0pGaP
    I delete custom schedule name   &{EditCustomSchedule01}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

Edit custom schedule with PM account
    [Tags]    Regression    CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule02}
    Set to Dictionary  ${EditCustomSchedule02}  editName  ${CustomSchedule02["customScheduleName"]}
    I delete custom schedule name   &{EditCustomSchedule01}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{EditCustomSchedule01}
    Set suite variable    &{EditCustomSchedule02}
    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{CustomSchedule02}

    : FOR    ${key}    IN    @{EditCustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule02}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{EditCustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule02}    ${key}    ${updated_val}
