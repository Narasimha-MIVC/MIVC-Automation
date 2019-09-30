*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Create an user via Primary Partition profiles page.
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/UserInfo.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
As a staff create an user via primary partition profiles page.
    [Tags]    Sanity_Phase2    one    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3s
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Set to Dictionary    ${ProfilePageUser}    profile_loc    ${locationName}
    Set to Dictionary    ${ProfilePageUser}    request_by    ${request_by}
    Set to Dictionary    ${ProfilePageUser}    request_source    Email
    ${extn} =  I add user from profiles tab   &{ProfilePageUser}
    When I switch to "users" page
    And I verify the User exist in user table created from profiles page    &{ProfilePageUser}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify user email ${ProfilePageUser['profile_mail']} with extension ${extn} is set for ${params['partition_id']}
#    Then In D2 I verify user email ${ProfilePageUser['profile_mail']} with extension ${extn} is set for ${accountName1}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    ${ProfilePageUser}

    : FOR    ${key}    IN    @{ProfilePageUser.keys()}
    \    ${updated_val}=    Replace String    ${ProfilePageUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${ProfilePageUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${ProfilePageUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${ProfilePageUser}    ${key}    ${updated_val}
