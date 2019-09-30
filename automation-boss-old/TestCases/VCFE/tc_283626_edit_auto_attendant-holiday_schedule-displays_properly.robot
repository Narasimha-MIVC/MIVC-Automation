*** Settings ***
Documentation  Login To Boss Portal And Edit An Auto Attendant With Custom Schedule and check whether the Custom
...            Schedule is Displayed properly for an Auto Attendant
...            Mahesh
Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files

Resource          ../../Variables/AutoAttendantInfo.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
01 Edit Auto Attendant and Validate Holiday Schedule name is Displayed Properly as DM user
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=   Then I create holiday schedule  &{HolidaySchedule01}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA04}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA05}    Validate_vcfe_name   HolidaySchedule
    Set to Dictionary    ${EditAA05}    vcfe_name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA05}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${holi_name}
    ...               I log off
    ...               I check for alert

02 Edit Auto Attendant and Validate Holiday Schedule name is Displayed Properly as PM user
    [Tags]    AA    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=   Then I create holiday schedule  &{HolidaySchedule01}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA04}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA05}    Validate_vcfe_name   HolidaySchedule
    Set to Dictionary    ${EditAA05}    vcfe_name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA05}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${holi_name}
    ...               I log off
    ...               I check for alert


*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{HolidaySchedule01}

    : FOR    ${key}    IN    @{HolidaySchedule01.keys()}
    \    ${updated_val}=    Replace String    ${HolidaySchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidaySchedule01}    ${key}    ${updated_val}