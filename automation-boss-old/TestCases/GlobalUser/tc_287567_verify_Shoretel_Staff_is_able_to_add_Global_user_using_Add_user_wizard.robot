*** Settings ***
Documentation    Suite description
#...               dev-Tantri Tanisha ,Susmitha
...

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../GlobalUser/Variables/global_variables.robot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py
Library  String
Library  Collections
*** Test Cases ***
03 Add users
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    When I switch to "users" page
    Log    ${DMUser}    console=yes
    log to console   ${global_countries}

    #Setting varaiables to dictionary
    set to dictionary   ${DMuser}   global_countries    ${global_countries}
    set to dictionary   ${DMuser}   au_userlocation    ${GlobalUserLocation}
    set to dictionary   ${DMuser}   au_location    ${GlobalUserBillingLoc}
    set to dictionary   ${DMuser}   request_by    ${request_by}

    and I add user    &{DMUser}
    Then I verify that User exist in user table    &{DMUser}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{DMUser}
    : FOR    ${key}    IN    @{DMUser.keys()}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}

