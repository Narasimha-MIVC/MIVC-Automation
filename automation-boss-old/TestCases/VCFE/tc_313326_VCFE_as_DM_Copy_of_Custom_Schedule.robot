*** Settings ***
Documentation    To copy VCFE CustomSchedule as DM user.
...              Palla Surya Kumar

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
Copy of custom schedule with DM user
    [Tags]    Regression    CS    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule01}
    Set to Dictionary    ${CopyCustomSchedule01}    editName    ${CustomSchedule01["customScheduleName"]}
    set to dictionary  ${CopyCustomSchedule01}    type    copy
    And I copy custom schedule    &{CopyCustomSchedule01}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify custom schedule "${CopyCustomSchedule01["customScheduleName"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete VCFE entry by name ${CopyCustomSchedule01['customScheduleName']}
    ...                       I delete VCFE entry by name ${CustomSchedule01['customScheduleName']}
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{CopyCustomSchedule01}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CopyCustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CopyCustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CopyCustomSchedule01}    ${key}    ${updated_val}
