*** Settings ***
Documentation     Login to BOSS portal and edit Holidays Schedule
#...               dev-Vasuja
#...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot


#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***

1 Login as staff user and Connect VCFE - Edit Holiday Schedule Settings
    [Tags]    Regression   HS    AUS    UK    Generic
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
    Set to Dictionary  ${HolidayScheduleStaff2}  holidayName  Holiday_NewEdit
    Set to Dictionary  ${HolidayScheduleStaff2}  date  11/02/2017
    Then I edit holiday schedule  &{HolidayScheduleStaff2}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleStaff2['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleStaff2}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidayScheduleStaff2["scheduleName"]}" with date "${HolidayScheduleStaff2["date"]}" and "${HolidayScheduleStaff["timeZone"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleStaff2['scheduleName']}
    ...                       I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HolidayScheduleStaff}
    Set suite variable    &{HolidayScheduleStaff2}


    : FOR    ${key}    IN    @{HolidayScheduleStaff.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleStaff}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HolidayScheduleStaff2.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleStaff2["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleStaff2}    ${key}    ${updated_val}
