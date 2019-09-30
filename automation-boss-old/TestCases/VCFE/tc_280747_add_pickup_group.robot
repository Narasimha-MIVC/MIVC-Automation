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
Library            String
*** Test Cases ***
Vcfe Add Pickup group with DM user
    [Tags]    Regression    PK    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    log many  &{params}
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    and I verify the group for ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_Add['pickupgpname']}" with extension "${Pickupgroup_Add['PGExtn']}" is set for ${params['partition_id']}

    [Teardown]  run keywords  I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    ...                       AND  I log off
    ...                       AND  I check for alert

Vcfe Add Pickup group with PM user
    [Tags]    Regression    PK    AUS    UK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    log many  &{params}
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    and I verify the group for ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_Add['pickupgpname']}" with extension "${Pickupgroup_Add['PGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    ...                      I log off
    ...                      I check for alert
#
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Pickupgroup_Add}

     : FOR    ${key}    IN    @{Pickupgroup_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_Add}    ${key}    ${updated_val}

