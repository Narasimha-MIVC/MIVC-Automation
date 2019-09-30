*** Settings ***
Documentation  Login To Boss Portal And Add an Auto Attendant
...            Mahesh

#Suite Setup       Set Init Env
##Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../../Variables/ContractInfo.robot
Resource          ../../Variables/AutoAttendantInfo.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
Vcfe Add Auto Attendant With DM User
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
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

Vcfe Add Auto Attendant With PM User
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
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{AA_01}
    : FOR    ${key}    IN    @{AA_01.keys()}
    \    ${updated_val}=    Replace String    ${AA_01["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_01}    ${key}    ${updated_val}