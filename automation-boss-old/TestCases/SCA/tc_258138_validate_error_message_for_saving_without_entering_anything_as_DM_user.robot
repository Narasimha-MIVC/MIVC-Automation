*** Settings ***
Documentation     Login to BOSS portal as DM user and Validate error message for saving without entering anything
#...               dev-Vasuja
#...               Comments:

#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/UserInfo.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}    country=${country}
Library  String

*** Test Cases ***

Login as DM and Validate error message for saving without entering anything
    [Tags]    Regression    Sanity_Phase2
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "home_phone_settings" page
    Set to Dictionary    ${user_ph_setting_Info}    shared_call_appearance    Enabled
    Set to Dictionary    ${user_ph_setting_Info}    extn    None
    Set to Dictionary    ${user_ph_setting_Info}    error_message    SCA extension can not be empty
    Then I edit user phone settings    &{user_ph_setting_Info}
   [Teardown]  run keywords   I log off
   ...                       I check for alert