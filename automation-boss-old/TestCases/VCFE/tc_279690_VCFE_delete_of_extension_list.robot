*** Settings ***
Documentation    VCFE-Delete of  Extension List
...              Vasuja K

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String

*** Test Cases ***
VCFE-Delete of Extension List with staff user
    [Tags]    Regression    EL    
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Set to Dictionary    ${Extensionlist_staff}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist_staff}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify extension list "${Extensionlist_staff['extnlistname']}" is set for ${params['partition_id']}
    And I delete VCFE entry by name ${Extensionlist_staff['extnlistname']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

VCFE-Delete of Extension List with DM user
    [Tags]    Regression    EL    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Set to Dictionary    ${Extensionlist01}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify extension list "${Extensionlist01['extnlistname']}" is set for ${params['partition_id']}
    And I delete VCFE entry by name ${Extensionlist01['extnlistname']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

VCFE-Delete of Extension List with PM user
    [Tags]    Regression    EL
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Set to Dictionary    ${Extensionlist02}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify extension list "${Extensionlist02['extnlistname']}" is set for ${params['partition_id']}
    And I delete VCFE entry by name ${Extensionlist02['extnlistname']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{Extensionlist01}
    Set suite variable    &{Extensionlist02}
    Set suite variable    &{Extensionlist_staff}

    : FOR    ${key}    IN    @{Extensionlist01.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{Extensionlist_staff.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist_staff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist_staff}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{Extensionlist02.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist02}    ${key}    ${updated_val}
