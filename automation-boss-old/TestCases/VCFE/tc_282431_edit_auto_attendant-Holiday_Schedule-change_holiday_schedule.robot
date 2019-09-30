*** Settings ***
Documentation  Login To Boss Portal And Edit An Auto Attendant And Change  Holiday Schedule Assigned To AA
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
01 Edit Auto Attendant and Change a Holiday Schedule as DM user
    [Tags]    Regression   AA    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=   Then I create holiday schedule  &{HolidaySchedule01}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA04}
    ${holi_name2}  ${holi_date2}=   Then I create holiday schedule  &{HolidaySchedule02}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Edit_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name2}
    And I edit Auto-Attendant     &{EditAA04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${holi_name}
    ...               I delete VCFE entry by name ${holi_name2}
    ...               I log off
    ...               I check for alert


02 Edit Auto Attendant and Change a Holiday Schedule as PM user
    [Tags]    Regression   AA
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=   Then I create holiday schedule  &{HolidaySchedule01}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA04}
    ${holi_name2}  ${holi_date2}=   Then I create holiday schedule  &{HolidaySchedule02}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Edit_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name2}
    And I edit Auto-Attendant     &{EditAA04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${holi_name}
    ...               I delete VCFE entry by name ${holi_name2}
    ...               I log off
    ...               I check for alert

03 Edit Auto Attendant and Change a Holiday Schedule as Staff user
    [Tags]    Regression   AA
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    ${holi_name}  ${holi_date}=   Then I create holiday schedule  &{HolidaySchedule01}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name}
    And I edit Auto-Attendant     &{EditAA04}
    ${holi_name2}  ${holi_date2}=   Then I create holiday schedule  &{HolidaySchedule02}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Edit_vcfe_component    HolidaySchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${holi_name2}
    And I edit Auto-Attendant     &{EditAA04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${holi_name}
    ...               I delete VCFE entry by name ${holi_name2}
    ...               I log off
    ...               I check for alert




*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{HolidaySchedule01}
    Set suite variable    &{HolidaySchedule02}

    : FOR    ${key}    IN    @{HolidaySchedule01.keys()}
    \    ${updated_val}=    Replace String    ${HolidaySchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidaySchedule01}    ${key}    ${updated_val}

     : FOR    ${key}    IN    @{HolidaySchedule02.keys()}
    \    ${updated_val}=    Replace String    ${HolidaySchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HolidaySchedule02}    ${key}    ${updated_val}