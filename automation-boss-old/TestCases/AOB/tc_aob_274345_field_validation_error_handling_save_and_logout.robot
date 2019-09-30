*** Settings ***
Documentation     BOSS BCO Sanity suite
...               Saurabh Singh


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
*** Test Cases ***
Field Validation error handling upon pressing Save and Logout button
    [Tags]  Sanity  dev
    Given I login to AOB page
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    Set to Dictionary    ${AobUserDetail_to_Clear}    phone    None     #other option: "Existing" or "None"
    then I create User  &{AobUserDetail_to_Clear}
    then I clear "FirstName" field
    and I click save and logout button
    and I verify AOB error "${firstName}" for "FirstName"
    then I clear "LastName" field
    and I click save and logout button
    and I verify AOB error "${lastName}" for "LastName"
    then I clear "Extension" field
    and I click save and logout button
    and I verify AOB error "${extension}" for "Extension"
    then I clear "Email" field
    and I click save and logout button
    and I verify AOB error "${email}" for "Email"
    and I click "Cancel" button

*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    4    12345678
    Set suite variable    ${uni_str}

    Set suite variable    &{AobUserDetail_to_Clear}
    : FOR    ${key}    IN    @{AobUserDetail_to_Clear.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail_to_Clear["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AobUserDetail_to_Clear}    ${key}    ${updated_val}


    Set suite variable    &{AobUserDetail_to_Clear}
    : FOR    ${key}    IN    @{AobUserDetail_to_Clear.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail_to_Clear["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AobUserDetail_to_Clear}    ${key}    ${updated_val}
