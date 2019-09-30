*** Settings ***
Documentation    To Edit Paging group and validate the error message- Name Field connot be blank
...              Immani Mahesh Kumar

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
Vcfe edit Paging group with DM user
    [Tags]    Regression    PGG    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{Paginggroupedit_DM}
    log to console  ${extn_num}
    Set to Dictionary    ${Paginggroupedit}    Pg_Extension    ${extn_num}
    Set to Dictionary    ${Paginggroupedit}    Remove_Name    True
    and I edit paging group    &{Paginggroupedit}
    [Teardown]  run keywords  i delete vcfe entry for ${extn_num}
     ...                      I log off
     ...                      I check for alert

Vcfe edit Paging group with PM user
    [Tags]    Regression    PGG
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{Paginggroupedit_PM}
    log to console  ${extn_num}
    Set to Dictionary    ${Paginggroupedit}    Pg_Extension    ${extn_num}
    Set to Dictionary    ${Paginggroupedit}    Remove_Name    True
    and I edit paging group    &{Paginggroupedit}
    [Teardown]  run keywords  i delete vcfe entry for ${extn_num}
     ...                      I log off
     ...                      I check for alert

Vcfe edit Paging group with Staff user
    [Tags]    Regression    PGG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{Paginggroupedit_PM}
    log to console  ${extn_num}
    Set to Dictionary    ${Paginggroupedit}    Pg_Extension    ${extn_num}
    Set to Dictionary    ${Paginggroupedit}    Remove_Name    True
    and I edit paging group    &{Paginggroupedit}
    [Teardown]  run keywords  i delete vcfe entry for ${extn_num}
     ...                      I log off
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