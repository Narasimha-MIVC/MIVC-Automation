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
As a Staff create any contact and assign a profile to the contact.
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3s
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}

    When I switch to "users" page
    SET TO DICTIONARY  ${GenUser}    au_userlocation    ${locationName}
    Set to Dictionary  ${GenUser}    request_by    ${request_by}
    Set to Dictionary  ${GenUser}    request_source    Email
    Set to Dictionary  ${GenUser}    role    Decision Maker

    ${phone_num}  ${extn} =  I add user   &{GenUser}
    I verify that User exist in user table   &{GenUser}
    SET TO DICTIONARY  ${GenUser}    ap_phonenumber    random
    SET TO DICTIONARY  ${GenUser}    ap_phonetype    MiCloud Connect Essentials
    SET TO DICTIONARY  ${GenUser}    ap_activationdate    today
    SET TO DICTIONARY  ${GenUser}    user_role    Staff
    SET TO DICTIONARY  ${GenUser}    hw_power    False

    ${phone_num}  ${extn} =  I assign profile to the contact with no profile    &{GenUser}
    I verify that User exist in user table   &{GenUser}

    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify user email ${GenUser['au_businessmail']} with extension ${extn} is set for ${params['partition_id']}
#    Then In D2 I verify user email ${GenUser['au_businessmail']} with extension ${extn} is set for ${accountName1}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    ${GenUser}

    : FOR    ${key}    IN    @{GenUser.keys()}
    \    ${updated_val}=    Replace String    ${GenUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${GenUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${GenUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${GenUser}    ${key}    ${updated_val}

