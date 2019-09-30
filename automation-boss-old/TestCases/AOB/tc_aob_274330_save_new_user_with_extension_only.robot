*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


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
Save new user with phone number
    [Tags]  Sanity
    Given I login to AOB page
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    ${bundle_name}=  I get current bundle name
    Set to Dictionary    ${AobUserDetail}    number    None     #Enter Phone Number which you want to select. Make "None"- if you dont want to select any number
    Set to Dictionary    ${AobUserDetail}    phone    None     #other option: "Existing" or "None"
    then I create User  &{AobUserDetail}
    and I click "Save" button         #Cancel or Save
    and I check user name "${AobUserDetail['firstName']} ${AobUserDetail['lastName']}" for bundle "${bundle_name}"
*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    4    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}

