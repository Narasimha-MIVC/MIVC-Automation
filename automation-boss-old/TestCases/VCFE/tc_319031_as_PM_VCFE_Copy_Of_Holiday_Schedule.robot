*** Settings ***
Documentation    To copy VCFE HolidaySchedule as PM user.
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
Copy of holiday schedule with PM user
    [Tags]    Regression    HS    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidaySchedulePM}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidaySchedulePM['scheduleName']}"
    Set to Dictionary  ${CopyHolidaySchedulePM}  holidayName  Holiday_NewCopy
    set to dictionary  ${CopyHolidaySchedulePM}    type    copy
    set to dictionary  ${CopyHolidaySchedulePM}    copy_message    Component was created successfully
    Then I copy holiday schedule  &{CopyHolidaySchedulePM}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${CopyHolidaySchedulePM["scheduleName"]}" with date "${CopyHolidaySchedulePM["date"]}" and "${CopyHolidaySchedulePM["timeZone"]}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry by name ${CopyHolidaySchedulePM['scheduleName']}
    ...                       I delete vcfe entry by name ${HolidaySchedulePM['scheduleName']}
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HolidaySchedulePM}
    Set suite variable    &{CopyHolidaySchedulePM}

    : FOR    ${key}    IN    @{HolidaySchedulePM.keys()}
    \    ${updated_val}=    Replace String    ${HolidaySchedulePM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidaySchedulePM}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CopyHolidaySchedulePM.keys()}
    \    ${updated_val}=    Replace String    ${CopyHolidaySchedulePM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CopyHolidaySchedulePM}    ${key}    ${updated_val}
