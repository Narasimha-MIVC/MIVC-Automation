*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...

Suite Teardown    Close The Browsers
Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot
#Resource    ../../Variables/PhoneNumberInfo.robot

Suite Setup       Set Init Env

Resource          ../GlobalUser/Variables/global_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections
*** Test Cases ***
1. Global User : Verify Mobility Checkbox for Global user
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "users" page
    And I verify mobility checkbox for global user       &{add_user_global}
    [Teardown]  run keywords  I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{add_user_global}
    : FOR    ${key}    IN    @{add_user_global.keys()}
    \    ${updated_val}=    Replace String    ${add_user_global["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${add_user_global}    ${key}    ${updated_val}


