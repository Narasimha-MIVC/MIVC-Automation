*** Settings ***
Documentation    To add VCFE Pickup Group with no location
...              Saurabh Singh

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
#Resource          tc_280747_add_pickup_group.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String
*** Test Cases ***
Vcfe Add Pickup group with DM user with No location
    [Tags]    Regression    PK    Generic
    Given Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    None
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    and I create pickup group with no location    &{Pickupgroup_Add}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

Vcfe Add Pickup group with PM user with no location
    [Tags]    Regression    PK
    Given Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    None
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    and I create pickup group with no location    &{Pickupgroup_Add}
    [Teardown]  run keywords  I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    

    : FOR    ${key}    IN    @{Pickupgroup_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_Add}    ${key}    ${updated_val}

