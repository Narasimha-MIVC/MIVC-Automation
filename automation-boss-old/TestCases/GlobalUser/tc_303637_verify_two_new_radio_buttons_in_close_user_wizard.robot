*** Settings ***
Documentation    Suite description
...               dev-Vasuja
...

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource    ../../RobotKeywords/BossKeywords.robot

#Variable files
Resource          ../GlobalUser/Variables/global_variables.robot
Resource    ../../Variables/EnvVariables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library   string

*** Test Cases ***
1. Global User : Verify two new radio buttons in close user wizard
    [Tags]    GlobalUser    test    NonSmr
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName1} with ${AccWithoutLogin} option
   And I switch to "users" page
   Log    ${DMUser}    console=yes
   log to console   ${global_countries}

   #Setting varaiables to dictionary
   set to dictionary   ${DMUser}   global_countries    ${global_countries}
   set to dictionary   ${DMUser}   au_userlocation    ${GlobalUserLocation}
   set to dictionary   ${DMUser}   au_location    ${GlobalUserBillingLoc}
   set to dictionary   ${DMUser}   request_by    ${request_by}

   and I add user    &{DMUser}

   And I switch to "close_user" page for "${DMUser['au_businessmail']}"
   Then I verify radio button "close_user_radio_button1"
   Then I verify radio button "close_user_radio_button2"
   And I click on "cancel_button1" button/link
   And I click on "confirm_box" button/link
   [Teardown]  run keywords  I log off
   ...                       I check for alert

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
