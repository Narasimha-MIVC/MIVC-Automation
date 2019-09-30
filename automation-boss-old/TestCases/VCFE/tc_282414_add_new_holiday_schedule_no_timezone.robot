*** Settings ***
Documentation     Login to BOSS portal and add Holidays Schedule with no timezone
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
1 Login as staff user and Add New Holiday Schedule - No Timezone
    [Tags]    Regression    HS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary  ${HolidayScheduleEdit}  scheduleName  ${HolidayScheduleStaff["scheduleName"]}
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleEdit['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidayScheduleEdit["scheduleName"]}" with date "${HolidayScheduleEdit["date"]}" and "${HolidayScheduleEdit["timeZone"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleEdit['scheduleName']}
    ...                       I log off
    ...                       I check for alert

2 Login as DM and Add New Holiday Schedule - No Timezone
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
    Set to Dictionary  ${HolidayScheduleEdit}  scheduleName  ${HolidayScheduleDM["scheduleName"]}
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleEdit['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidayScheduleEdit["scheduleName"]}" with date "${HolidayScheduleEdit["date"]}" and "${HolidayScheduleEdit["timeZone"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleEdit['scheduleName']}
    ...                       I log off
    ...                       I check for alert

3 Login as PM and Add New Holiday Schedule - No Timezone
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
    Set to Dictionary  ${HolidayScheduleEdit}  scheduleName  ${HolidaySchedulePM["scheduleName"]}
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleEdit['scheduleName']}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify holiday schedule "${HolidayScheduleEdit["scheduleName"]}" with date "${HolidayScheduleEdit["date"]}" and "${HolidayScheduleEdit["timeZone"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${HolidayScheduleEdit['scheduleName']}
    ...                       I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

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

