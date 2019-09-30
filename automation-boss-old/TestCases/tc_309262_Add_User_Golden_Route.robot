*** Settings ***
Documentation     BOSS Elvis test cases
...               dev-Sameena

#Suite Setup and Teardown
Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../RobotKeywords/BOSSKeywords.robot
Resource          ../Variables/UserInfo.robot

#Variable files
Resource          ../Variables/EnvVariables.robot
Resource          ../Variables/LoginDetails_Elvis.robot


#BOSS Component
Library           ../lib/BossComponent.py



*** Test Cases ***
TC_309262_Add_User_Golden_Route
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account Automation_Elvis with ${AccWithoutLogin} option
    When I switch to "users" page
    and I Add User  &{DMUser_Elvis}
    Then I verify that User exist in user table  &{DMUser_Elvis}
    # I need to create a new user variable and try this code with that


*** Keywords ***

Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}


    Set suite variable    &{DMUser_Elvis}
    : FOR    ${key}    IN    @{DMUser_Elvis.keys()}
    \    ${updated_val}=    Replace String    ${DMUser_Elvis["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser_Elvis}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser_Elvis["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser_Elvis}    ${key}    ${updated_val}