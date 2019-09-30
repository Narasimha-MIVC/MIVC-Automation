*** Settings ***
Documentation    VCFE-Delete of Custom Schedule
...              Vasuja K

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

VCFE-Delete of Custom Schedule with staff account
    #When I check for alert
    [Tags]    CS    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule_staff}
    And I delete VCFE entry by name ${CustomSchedule_staff['customScheduleName']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

VCFE-Delete of Custom Schedule with DM account
    #When I check for alert
    [Tags]    CS    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule01}
    And I delete VCFE entry by name ${CustomSchedule01['customScheduleName']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

VCFE-Delete of Custom Schedule with PM account
    #When I check for alert
     [Tags]    Regression       CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule02}
    And I delete VCFE entry by name ${CustomSchedule02['customScheduleName']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule_staff}
    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{CustomSchedule02}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule02}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule_staff.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule_staff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule_staff}    ${key}    ${updated_val}
