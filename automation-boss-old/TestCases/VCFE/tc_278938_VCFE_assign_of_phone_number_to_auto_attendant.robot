*** Settings ***
Documentation  Login To Boss Portal And assign of Phone number to Auto Attendant
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
Assign of Phone number to Auto Attendant With Staff User
    [Tags]    Regression    AA
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${AA_01}    Aa_assignDID    random
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I log off
    ...                      I check for alert

Assign of Phone number to Auto Attendant With DM User
    [Tags]    Regression    AA    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${AA_01}    Aa_assignDID    random
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I log off
    ...                      I check for alert

Assign of Phone number to Auto Attendant With PM User
    [Tags]    Regression        AA
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${AA_01}    Aa_assignDID    random
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I log off
    ...                      I check for alert
