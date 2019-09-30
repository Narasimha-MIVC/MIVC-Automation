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
Vcfe edit Pickup group with DM user
    [Tags]    Regression    PK    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_edit}    PGExtn    ${extn_num}
    Set to Dictionary    ${Pickupgroup_edit}    pickupgpname    ${Pickupgroup2_Add['pickupgpname']}
    Set to Dictionary    ${Pickupgroup_edit}    extnlistname    ${extnlistname}
    Then I select vcfe component by searching extension "${Pickupgroup_edit['PGExtn']}"
    and I edit pickup group    &{Pickupgroup_edit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_edit['pickupgpname']}" with extension "${Pickupgroup_edit['PGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

Vcfe edit Pickup group with PM user
    [Tags]    Regression    PK    AUS    UK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_edit}    PGExtn    ${extn_num}
    Set to Dictionary    ${Pickupgroup_edit}    pickupgpname    ${Pickupgroup2_Add['pickupgpname']}
    Set to Dictionary    ${Pickupgroup_edit}    extnlistname    ${extnlistname}
    Then I select vcfe component by searching extension "${Pickupgroup_edit['PGExtn']}"
    and I edit pickup group    &{Pickupgroup_edit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_edit['pickupgpname']}" with extension "${Pickupgroup_edit['PGExtn']}" is set for ${params['partition_id']}
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

    Set suite variable    &{Pickupgroup2_Add}
    : FOR    ${key}    IN    @{Pickupgroup2_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup2_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup2_Add}    ${key}    ${updated_val}
