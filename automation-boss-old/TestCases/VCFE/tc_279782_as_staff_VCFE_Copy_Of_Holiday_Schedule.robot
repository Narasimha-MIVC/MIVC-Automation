*** Settings ***
Documentation    To copy VCFE HolidaySchedule as staff user.
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
Copy of holiday schedule with staff user
    [Tags]    Regression    HS    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
	when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleStaff['scheduleName']}"
    Set to Dictionary  ${CopyHolidayScheduleStaff}  holidayName  Holiday_NewCopy
    set to dictionary  ${CopyHolidayScheduleStaff}    type    copy
    set to dictionary  ${CopyHolidayScheduleStaff}    copy_message    Component was created successfully
    Then I copy holiday schedule  &{CopyHolidayScheduleStaff}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${CopyHolidayScheduleStaff["scheduleName"]}" with date "${CopyHolidayScheduleStaff["date"]}" and "${CopyHolidayScheduleStaff["timeZone"]}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry by name ${CopyHolidayScheduleStaff['scheduleName']}
    ...                       I delete vcfe entry by name ${HolidayScheduleStaff['scheduleName']}
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HolidayScheduleStaff}
    Set suite variable    &{CopyHolidayScheduleStaff}

    : FOR    ${key}    IN    @{HolidayScheduleStaff.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleStaff}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CopyHolidayScheduleStaff.keys()}
    \    ${updated_val}=    Replace String    ${CopyHolidayScheduleStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CopyHolidayScheduleStaff}    ${key}    ${updated_val}



