*** Settings ***
Documentation    To add VCFE Pickup Group
...              Saurabh Singh

Suite Setup       Set Init Env

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
Vcfe Invalid extension for Paging group with DM user
    [Tags]    Regression    PGG    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    @{extn_list}=    Create List    9999    0123
    : FOR   ${extn}   IN  @{extn_list}
    \    set to dictionary   ${PagingGroup}   Pg_Extension    ${extn}
    \    I check for invalid extention   &{PagingGroup}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

Vcfe Invalid extension for Paging group with PM user
    [Tags]    Regression    PGG
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    @{extn_list}=    Create List    9999    0000
    : FOR   ${extn}   IN  @{extn_list}
    \    set to dictionary   ${PagingGroupPM}   Pg_Extension    ${extn}
    \    I check for invalid extention   &{PagingGroupPM}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Paginggroupedit}
    : FOR    ${key}    IN    @{Paginggroupedit.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit}    ${key}    ${updated_val}

    Set suite variable    &{Paginggroupedit_DM}
    : FOR    ${key}    IN    @{Paginggroupedit_DM.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit_DM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit_DM}    ${key}    ${updated_val}

    Set suite variable    &{Paginggroupedit_PM}
    : FOR    ${key}    IN    @{Paginggroupedit_PM.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit_PM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit_PM}    ${key}    ${updated_val}


