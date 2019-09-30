*** Settings ***
Documentation    VCFE-Delete of On-Hours Schedule
#...               dev-Vasuja

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
01 VCFE-Delete of On-Hours Schedule with DM User
    #When I check for alert
    [Tags]    Regression    OH    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    Set to Dictionary  ${OnHoursSchedule01}  scheduleName  ${OHS_name}
    Then I delete vcfe entry by name ${OnHoursSchedule01['scheduleName']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert


02 VCFE-Delete of On-Hours Schedule with PM User
    #When I check for alert
    [Tags]    Regression    OH
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    Set to Dictionary  ${OnHoursSchedule01}  scheduleName  ${OHS_name}
    Then I delete vcfe entry by name ${OnHoursSchedule01['scheduleName']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert


03 VCFE-Delete of On-Hours Schedule with Staff User
    [Tags]    Regression    OH
    Given I login to ${url} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    Set to Dictionary  ${OnHoursSchedule01}  scheduleName  ${OHS_name}
    Then I delete vcfe entry by name ${OnHoursSchedule01['scheduleName']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert



*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{OnHoursSchedule01}

    : FOR    ${key}    IN    @{OnHoursSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule01}    ${key}    ${updated_val}