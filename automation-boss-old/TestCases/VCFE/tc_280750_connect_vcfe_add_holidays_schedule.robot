*** Settings ***
Documentation     Login to BOSS portal and create Holidays Schedule
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

1 Login as staff user and Connect VCFE - Add Holidays Schedule
    [Tags]    Regression    HS    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    Set to Dictionary    ${HolidayScheduleEdit}    HSname    ${holi_name}
    Set to Dictionary    ${HolidayScheduleEdit}    date    ${holi_date}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleStaff['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleStaff['scheduleName']}
    ...                       I log off
    ...                       I check for alert




*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HolidayScheduleStaff}


    : FOR    ${key}    IN    @{HolidayScheduleStaff.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleStaff}    ${key}    ${updated_val}
