*** Settings ***
Documentation  Login To Boss Portal And Edit An Auto Attendant And Removing the Extension
...            Mahesh
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

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
01 Removing The Extension for AA as a DM user
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA03}    Aa_Extn     Remove
    And I edit Auto-Attendant     &{EditAA03}
    [Teardown]  run keywords   I delete vcfe entry for ${extn_num}
    ...                        I log off
    ...                        I check for alert

02 Removing The Extension for AA as a PM user
    [Tags]    AA    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA03}    Aa_Extn    Remove
    And I edit Auto-Attendant     &{EditAA03}
    [Teardown]  run keywords   I delete vcfe entry for ${extn_num}
    ...                        I log off
    ...                        I check for alert


