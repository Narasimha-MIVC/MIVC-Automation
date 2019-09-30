*** Settings ***
Documentation    VCFE-Delete of Paging Group
#...               dev-Vasuja

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
VCFE-Delete of Paging Group with DM user
    [Tags]    Regression    PG    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{Paginggroupedit_DM}
    Set to Dictionary    ${Paginggroupedit_DM}    Pg_Extension    ${extn_num}
    Then I delete vcfe entry for ${extn_num}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

VCFE-Delete of Paging Group with PM user
    [Tags]    Regression    PG
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{Paginggroupedit_PM}
    Set to Dictionary    ${Paginggroupedit_PM}    Pg_Extension    ${extn_num}
    Then I delete vcfe entry for ${extn_num}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

VCFE-Delete of Paging Group with staff user
    [Tags]    Regression    PG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{PagingGroup}
    Set to Dictionary    ${PagingGroup}    Pg_Extension    ${extn_num}
    Then I delete vcfe entry for ${extn_num}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{PagingGroup}
    : FOR    ${key}    IN    @{PagingGroup.keys()}
    \    ${updated_val}=    Replace String    ${PagingGroup["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PagingGroup}    ${key}    ${updated_val}

    Set suite variable    &{Paginggroupedit_DM}
    : FOR    ${key}    IN    @{Paginggroupedit_DM.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit_DM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit_DM}    ${key}    ${updated_val}

    Set suite variable    &{Paginggroupedit_PM}
    : FOR    ${key}    IN    @{Paginggroupedit_PM.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit_PM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit_PM}    ${key}    ${updated_val}


