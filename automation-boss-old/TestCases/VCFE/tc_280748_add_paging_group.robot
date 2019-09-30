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
Vcfe Add paging group with DM user
    [Tags]    Regression    PGG    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{PagingGroup}
    Set to Dictionary    ${PagingGroup}    Pg_Extension    ${extn_num}
    and I verify the group for ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${PagingGroup["Pg_Name"]}" with extension "${PagingGroup["Pg_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords           I delete vcfe entry for ${PagingGroup['Pg_Extension']}
    ...                                I log off
    ...                                I check for alert

Vcfe Add paging group with PM user
    [Tags]    Regression    PGG    AUS    UK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I add Paging Group    &{PagingGroupPM}
    Set to Dictionary    ${PagingGroupPM}    Pg_Extension    ${extn_num}
    and I verify the group for ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${PagingGroupPM["Pg_Name"]}" with extension "${PagingGroupPM["Pg_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords           I delete vcfe entry for ${PagingGroupPM['Pg_Extension']}
    ...                                I log off
    ...                                I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{PagingGroup}
    Set suite variable    &{PagingGroupPM}

    : FOR    ${key}    IN    @{PagingGroup.keys()}
    \    ${updated_val}=    Replace String    ${PagingGroup["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PagingGroup}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{PagingGroup.keys()}
    \    ${updated_val}=    Replace String    ${PagingGroup["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PagingGroup}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{PagingGroupPM.keys()}
    \    ${updated_val}=    Replace String    ${PagingGroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PagingGroupPM}    ${key}    ${updated_val}
