*** Settings ***
Documentation  Login To Boss Portal And VCFE Creation of Auto Attendant with customized extension
...            Vasuja K

Suite Setup       Set Init Env
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
VCFE Creation of Auto Attendant with customized extension With staff User
    [Tags]    Regression    AA
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_02}
    Set to Dictionary    ${AA_02}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_02["Aa_Name"]}" with extension "${AA_02["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I log off
    ...                      I check for alert

VCFE Creation of Auto Attendant with customized extension With DM User
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
    ${extn_num}=    And I add Auto-Attendant    &{AA_02}
    Set to Dictionary    ${AA_02}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_02["Aa_Name"]}" with extension "${AA_02["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I log off
    ...                      I check for alert

VCFE Creation of Auto Attendant with customized extension With PM User
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
    ${extn_num}=    And I add Auto-Attendant    &{AA_02}
    Set to Dictionary    ${AA_02}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_02["Aa_Name"]}" with extension "${AA_02["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{AA_02}
    : FOR    ${key}    IN    @{AA_02.keys()}
    \    ${updated_val}=    Replace String    ${AA_02["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_02}    ${key}    ${updated_val}