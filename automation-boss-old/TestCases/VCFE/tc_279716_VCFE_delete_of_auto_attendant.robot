*** Settings ***
Documentation  Login To Boss Portal And VCFE-Delete of Auto Attendant
...            Vasuja K


Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../../Variables/AutoAttendantInfo.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
VCFE-Delete of Auto Attendant With Staff User
    [Tags]    Regression    AA
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I delete vcfe entry for ${AA_01['AA_Extension']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

VCFE-Delete of Auto Attendant With DM User
    [Tags]    Regression    AA    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I delete vcfe entry for ${AA_01['AA_Extension']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

VCFE-Delete of Auto Attendant With PM User
    [Tags]    Regression        AA
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I delete vcfe entry for ${AA_01['AA_Extension']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert