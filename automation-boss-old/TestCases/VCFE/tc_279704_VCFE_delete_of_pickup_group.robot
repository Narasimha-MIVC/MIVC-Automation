*** Settings ***
Documentation    VCFE-Delete of Pickup Group
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
VCFE-Delete of Pickup Group with DM user
    [Tags]    Regression    PK    AUS    UK    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Then I delete vcfe entry for ${extn_num}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

VCFE-Delete of Pickup Group with PM user
    [Tags]    Regression    PK    AUS    UK
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Then I delete vcfe entry for ${extn_num}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

VCFE-Delete of Pickup Group with staff user
    [Tags]    Regression    PK    AUS    UK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Then I delete vcfe entry for ${extn_num}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Pickupgroup_Add}
    : FOR    ${key}    IN    @{Pickupgroup_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_Add}    ${key}    ${updated_val}
