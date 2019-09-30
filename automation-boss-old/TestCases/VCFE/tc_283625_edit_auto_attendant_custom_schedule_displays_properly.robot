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
01 Edit Auto Attendant and Validate Custom Schedule name is Displayed Properly as DM user
   [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule03}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component  CustomSchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA04}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA05}    Validate_vcfe_name   CustomSchedule
    Set to Dictionary    ${EditAA05}    vcfe_name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA05}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${CustomSchedule03['customScheduleName']}
    ...               I log off
    ...               I check for alert

02 Edit Auto Attendant and Validate Custom Schedule name is Displayed Properly as PM user
    [Tags]    AA    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule03}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component  CustomSchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA04}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA05}    Validate_vcfe_name   CustomSchedule
    Set to Dictionary    ${EditAA05}    vcfe_name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA05}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${CustomSchedule03['customScheduleName']}
    ...               I log off
    ...               I check for alert

03 Edit Auto Attendant and Validate Custom Schedule name is Displayed Properly as Staff user
   [Tags]    AA    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule03}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Then I select vcfe component by searching extension "${extn_num}"
   Set to Dictionary    ${EditAA04}    Assign_vcfe_component  CustomSchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA04}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA05}    Validate_vcfe_name   CustomSchedule
    Set to Dictionary    ${EditAA05}    vcfe_name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA05}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${CustomSchedule03['customScheduleName']}
    ...               I log off
    ...               I check for alert




*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{CustomSchedule03}

    : FOR    ${key}    IN    @{CustomSchedule03.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule03}    ${key}    ${updated_val}
