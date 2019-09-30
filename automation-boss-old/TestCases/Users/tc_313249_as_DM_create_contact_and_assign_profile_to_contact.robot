*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Create any contact and assign a profile to the contact.
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/UserInfo.robot
Resource           ../../Variables/ErrorStrings.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
As a DM create any contact and assign a profile to the contact.
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    sleep  3s
    When I switch to "users" page
    SET TO DICTIONARY  ${DMUser}    au_userlocation    ${locationName}
    Set to Dictionary  ${DMUser}    login_user    DM

    ${phone_num}  ${extn} =  I add user   &{DMUser}
    I verify that User exist in user table   &{DMUser}
    SET TO DICTIONARY  ${DMUser}    ap_phonenumber    random
    SET TO DICTIONARY  ${DMUser}    ap_phonetype    MiCloud Connect Essentials
    SET TO DICTIONARY  ${DMUser}    ap_activationdate    today
    SET TO DICTIONARY  ${DMUser}    user_role    DM
    SET TO DICTIONARY  ${DMUser}    hw_power    False

    ${phone_num}  ${extn} =  I assign profile to the contact with no profile    &{DMUser}
    I verify that User exist in user table   &{DMUser}

    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify user email ${DMUser['au_businessmail']} with extension ${extn} is set for ${params['partition_id']}
#    Then In D2 I verify user email ${DMUser['au_businessmail']} with extension ${extn} is set for ${accountName1}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    ${DMUser}

    : FOR    ${key}    IN    @{DMUser.keys()}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
