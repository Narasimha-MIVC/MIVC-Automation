*** Settings ***
Documentation   Verify that Type dropdown is disabled for global user in update TN Wizard.

Suite Teardown    Close The Browsers
#Variable files
Suite Setup     Set Init Env
Resource          ../../RobotKeywords/BOSSKeywords.robot

Resource          ../../Variables/EnvVariables.robot

Resource          ../../Variables/PhoneNumberInfo.robot

#Resource          ../../Variables/LoginDetails.robot

Library           ../../lib/BossComponent.py    browser=${BROWSER}

#Library           ../../lib/BossComponent.py    browser=${BROWSER}    country=${country}
Library           ../../lib/DirectorComponent.py
#Library           PPhoneInterface

Library     String
Library     Collections


*** Test Cases ***
Verify that Type dropdown is disabled for global user in update TN Wizard
    [Tags]    GLOBAL
    Given i login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    when I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "phonenumber" page
    ${Updatephoneform}=    create dictionary  TnType=disabled
    Set to Dictionary   ${PhoneNumber_Global_UK}    global_no_check     True
    Set to Dictionary   ${PhoneNumber_Global_UK}    updateformfield     ${Updatephoneform}
    I add PhoneNumber  &{PhoneNumber_Global_UK}
    and I set PhoneNumberFields state    &{PhoneNumber_Global_UK}


    [Teardown]  run keywords  I log off
    ...                      I check for alert

 #   if params['global_no_check']=="True":
    #And i select checkbox and click update "phonenumber" page

   # Then I check for "Global User" in Type drop down


*** Keywords ***
Set Init Env
    @{user_list}=    Create list
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    &{PhoneNumber_Global_UK}
    : FOR    ${key}    IN    @{PhoneNumber_Global_UK.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumber_Global_UK["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumber_Global_UK}    ${key}    ${updated_val}
