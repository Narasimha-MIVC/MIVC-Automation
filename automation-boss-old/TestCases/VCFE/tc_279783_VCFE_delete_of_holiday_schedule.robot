*** Settings ***
Documentation     Login to BOSS portal and delete of  Holiday Schedule
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
Library  String

*** Test Cases ***

1 Login as staff user and VCFE-Delete of Holiday Schedule
    [Tags]    Regression    HS    
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    And I delete vcfe entry by name ${HolidayScheduleStaff['scheduleName']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

2 Login as DM user and VCFE-Delete of Holiday Schedule
    [Tags]    Regression    HS    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleDM}
    And I delete vcfe entry by name ${HolidayScheduleDM['scheduleName']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

3 Login as PM user and VCFE-Delete of Holiday Schedule
    [Tags]    Regression    HS    
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidaySchedulePM}
    And I delete vcfe entry by name ${HolidaySchedulePM['scheduleName']}
    [Teardown]  run keywords  I log off
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

    Set suite variable    &{HolidayScheduleDM}

    : FOR    ${key}    IN    @{HolidayScheduleDM.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleDM}    ${key}    ${updated_val}

    Set suite variable    &{HolidaySchedulePM}

    : FOR    ${key}    IN    @{HolidaySchedulePM.keys()}
    \    ${updated_val}=    Replace String    ${HolidaySchedulePM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidaySchedulePM}    ${key}    ${updated_val}
