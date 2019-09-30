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
tc-310853 Close User - Cancel
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account Automation_Elvis with ${AccWithoutLogin} option
    When I switch to "users" page
    and I Add User  &{DMUser_Elvis}
    Then I verify that User exist in user table  &{DMUser_Elvis}
    When I switch to "users" page
    and I do right click and do a close user cancel in elvis ${DMUser_Elvis["au_businessmail"]} with user "Automation_Elvis Account"
    Then I verify that User exist in user table  &{DMUser_Elvis}

tc-310854 Close User - Close

    When I switch to "users" page
    and I do right click and go to close user page in elvis ${DMUser_Elvis["au_businessmail"]} with user "AutoElvisPM acc"
    Then I verify that User does not exist in user table  &{DMUser_Elvis}


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





