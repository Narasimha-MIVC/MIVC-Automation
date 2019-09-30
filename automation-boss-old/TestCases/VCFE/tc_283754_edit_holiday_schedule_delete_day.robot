*** Settings ***
Documentation     Login to BOSS portal and Edit Holiday Schedule - Delete Day
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
1 Login as staff user and Edit Holiday Schedule - Delete Day
    [Tags]    Regression    HS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleStaff}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleStaff['scheduleName']}"
    Set to Dictionary    ${HolidayScheduleEdit}    Holidays    Delete
    Then I edit holiday schedule  &{HolidayScheduleEdit}
    Then I select vcfe component by searching name "${HolidayScheduleStaff["scheduleName"]}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    [Teardown]  run keywords   I delete vcfe entry by name ${HolidayScheduleStaff['scheduleName']}
    ...                       I log off
    ...                       I check for alert

2 Login as DM user and Edit Holiday Schedule - Delete Day
    [Tags]    Regression    HS    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidayScheduleDM}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidayScheduleDM['scheduleName']}"
    Set to Dictionary    ${HolidayScheduleEdit}    Holidays    Delete
    Then I edit holiday schedule  &{HolidayScheduleEdit}
    Then I select vcfe component by searching name "${HolidayScheduleDM["scheduleName"]}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    [Teardown]  run keywords   I delete vcfe entry by name ${HolidayScheduleDM['scheduleName']}
    ...                       I log off
    ...                       I check for alert

3 Login as PM user and Edit Holiday Schedule - Delete Day
    [Tags]    Regression    HS
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=    Then I create holiday schedule  &{HolidaySchedulePM}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching name "${HolidaySchedulePM['scheduleName']}"
    Set to Dictionary    ${HolidayScheduleEdit}    Holidays    Delete
    Then I edit holiday schedule  &{HolidayScheduleEdit}
    Then I select vcfe component by searching name "${HolidaySchedulePM["scheduleName"]}"
    Then I verify holidays schedule  &{HolidayScheduleEdit}
    [Teardown]  run keywords   I delete vcfe entry by name ${HolidaySchedulePM['scheduleName']}
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


