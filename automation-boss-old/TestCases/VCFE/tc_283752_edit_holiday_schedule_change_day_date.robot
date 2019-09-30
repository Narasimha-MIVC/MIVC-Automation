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

1 Login as staff and Edit Holiday Schedule - Change Day Date
    [Tags]    Regression    HS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    Set to Dictionary  ${HolidayScheduleEdit}  date  10/31/2017
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleStaff['scheduleName']}"
    Then I edit holiday schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleStaff['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidayScheduleStaff["scheduleName"]}" with date "${HolidayScheduleEdit["date"]}" and "${HolidayScheduleStaff["timeZone"]}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleStaff['scheduleName']}
    ...                       I log off
    ...                       I check for alert

2 Login as DM and Edit Holiday Schedule - Change Day Date
    [Tags]    Regression    HS    Generic
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
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleDM}
    Set to Dictionary  ${HolidayScheduleEdit}  date  10/31/2017
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleDM['scheduleName']}"
    Then I edit holiday schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleDM['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidayScheduleDM["scheduleName"]}" with date "${HolidayScheduleEdit["date"]}" and "${HolidayScheduleDM["timeZone"]}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleDM['scheduleName']}
    ...                       I log off
    ...                       I check for alert


3 Login as PM and Edit Holiday Schedule - Change Day Date
    [Tags]    Regression    HS
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
    Set to Dictionary  ${HolidayScheduleEdit}  date  10/31/2017
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidaySchedulePM['scheduleName']}"
    Then I edit holiday schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidaySchedulePM['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidaySchedulePM["scheduleName"]}" with date "${HolidayScheduleEdit["date"]}" and "${HolidaySchedulePM["timeZone"]}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidaySchedulePM['scheduleName']}
    ...                       I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HolidayScheduleStaff}
    Set suite variable    &{HolidayScheduleDM}
    Set suite variable    &{HolidaySchedulePM}



    : FOR    ${key}    IN    @{HolidayScheduleStaff.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleStaff}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HolidayScheduleDM.keys()}
    \    ${updated_val}=    Replace String    ${HolidayScheduleDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidayScheduleDM}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HolidaySchedulePM.keys()}
    \    ${updated_val}=    Replace String    ${HolidaySchedulePM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidaySchedulePM}    ${key}    ${updated_val}
