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


#BOSS Component
Library           ../lib/BossComponent.py



*** Test Cases ***
TC-309836 Close User - Cancel
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account AOB_Automation_1 with ${AccWithoutLogin} option
    When I switch to "users" page
    and I Add User  &{DMUser2}
    Then I verify that User exist in user table  &{DMUser2}
    When I switch to "users" page
    and I do right click and do a close user cancel for ${DMUser2["au_businessmail"]} with user "Wally Auto"
    Then I verify that User exist in user table  &{DMUser2}

TC-309845 Close User - Close

    When I switch to "users" page
    and I do right click and go to close user page for ${DMUser2["au_businessmail"]} with user "Wally Auto"
    Then I verify that User does not exist in user table  &{DMUser2}


*** Keywords ***
Set Init Env

    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}


    Set suite variable    &{DMUser2}
    : FOR    ${key}    IN    @{DMUser2.keys()}
    \    ${updated_val}=    Replace String    ${DMUser2["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser2}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser2["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser2}    ${key}    ${updated_val}





