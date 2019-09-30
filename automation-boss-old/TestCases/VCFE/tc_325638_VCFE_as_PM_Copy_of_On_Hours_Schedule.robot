*** Settings ***
Documentation    To copy On-Hours Schedule as PM user
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String

*** Test Cases ***
01 Create On Hours schedule with out timezone with PM User
     [Tags]    Regression    OHS    AUS    UK    Generic
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    And i select vcfe component by searching name "${OHS_name}"
    set to dictionary  ${CopyOnHoursSchedule01}    type    copy
    set to dictionary  ${CopyOnHoursSchedule01}    copy_message    Component was created successfully
    Then I copy on-hours schedule   &{CopyOnHoursSchedule01}
    [Teardown]  run keywords  I delete vcfe entry by name ${CopyOnHoursSchedule01['scheduleName']}
    ...                       I delete VCFE entry by name ${OHS_name}
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{OnHoursSchedule01}
    Set suite variable    &{CopyOnHoursSchedule01}

    : FOR    ${key}    IN    @{OnHoursSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CopyOnHoursSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CopyOnHoursSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CopyOnHoursSchedule01}    ${key}    ${updated_val}