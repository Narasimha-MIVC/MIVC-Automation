*** Settings ***
Documentation    Suite description

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../GlobalNumber/Variables/GlobalNumber_variable.robot
Resource          ../../Variables/LoginDetails.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}   country=${country}
Library  String
Library  Collections


*** Test Cases ***

1. Global Number : Verify display name error message
   [Tags]    GlobalNumber
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   when I switch to "phone_number" page
   And I select number for Edit    &{PhoneNumber_Edit}
   then I verify PhoneNumber Operation for Edit   &{PhoneNumber_Edit}

*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    34    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{PhoneNumber_Edit}
     : FOR    ${key}    IN    @{PhoneNumber_Edit.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumber_Edit["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PhoneNumber_Edit}    ${key}    ${updated_val}