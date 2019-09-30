*** Settings ***
Documentation     Login to BOSS portal and add new Holidays Schedule with same name
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

1 Login as staff user and Add New Holiday Schedule - Name Already in Use
    [Tags]    Regression    HS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    Set to Dictionary  ${HolidayScheduleStaff}  timeZone  ${HolidayScheduleEdit["timeZone"]}
    Set to Dictionary  ${HolidayScheduleStaff}  holidayName  ${HolidayScheduleEdit["holidayName"]}
    Set to Dictionary    ${HolidayScheduleStaff}  date  ${HolidayScheduleEdit["date"]}
    Set to Dictionary    ${HolidayScheduleStaff}    error_message  Failed creating component. Error: ScheduleName - has already been taken
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    [Teardown]  run keywords   I click on cancel button
    ...                        I delete vcfe entry by name ${HolidayScheduleStaff['scheduleName']}
    ...                        I log off
    ...                       I check for alert

2 Login as DM and Add New Holiday Schedule - Name Already in Use
    [Tags]    Regression    HS    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleDM}
    Set to Dictionary  ${HolidayScheduleDM}  timeZone  ${HolidayScheduleEdit["timeZone"]}
    Set to Dictionary  ${HolidayScheduleDM}  holidayName  ${HolidayScheduleEdit["holidayName"]}
    Set to Dictionary  ${HolidayScheduleDM}  date  ${HolidayScheduleEdit["date"]}
    Set to Dictionary    ${HolidayScheduleDM}    error_message  Failed creating component. Error: ScheduleName - has already been taken
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleDM}
    [Teardown]  run keywords   I click on cancel button
    ...                        I delete vcfe entry by name ${HolidayScheduleDM['scheduleName']}
    ...                        I log off
    ...                       I check for alert


3 Login as PM and Add New Holiday Schedule - Name Already in Use
    [Tags]    Regression    HS
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidaySchedulePM}
    Set to Dictionary  ${HolidaySchedulePM}  timeZone  ${HolidayScheduleEdit["timeZone"]}
    Set to Dictionary  ${HolidaySchedulePM}  holidayName  ${HolidayScheduleEdit["holidayName"]}
    Set to Dictionary  ${HolidaySchedulePM}  date  ${HolidayScheduleEdit["date"]}
    Set to Dictionary    ${HolidaySchedulePM}    error_message  Failed creating component. Error: ScheduleName - has already been taken
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidaySchedulePM}
    [Teardown]  run keywords   I click on cancel button
    ...                        I delete vcfe entry by name ${HolidaySchedulePM['scheduleName']}
    ...                        I log off
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

