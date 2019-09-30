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
Edit operation on existing user
    [Tags]  Sanity
    Given I login to AOB page
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    ${status}=  I check if user is created
    ${bundle_name}=  I get current bundle name
    Set to Dictionary    ${AobUserDetail}    phone    None     #other option: "Existing" or "None"
    Run Keyword If   '${status}' == 'False'   run keyword    I create User  &{AobUserDetail}
    Run Keyword If   '${status}' == 'False'   run keyword    and I click "Save" button
    Run Keyword If   '${status}' == 'False'   run keyword    I check if user is created
    Run Keyword If   '${status}' == 'False'   run keyword    I Edit AOB User   &{EditAobUserDetail}
    Run Keyword If   '${status}' == 'False'   run keyword    and I click "Save" button
    Run Keyword If   '${status}' == 'True'   run keyword     I Edit AOB User   &{EditAobUserDetail}
    Run Keyword If   '${status}' == 'True'   run keyword     and I click "Save" button
    Run Keyword If   '${status}' == 'True'   run keyword    I check user name "${EditAobUserDetail['firstName']} ${EditAobUserDetail['lastName']}" for bundle "${bundle_name}"

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

    Set suite variable    &{EditAobUserDetail}
    : FOR    ${key}    IN    @{EditAobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${EditAobUserDetail["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditAobUserDetail}    ${key}    ${updated_val}

    Set suite variable    &{EditAobUserDetail}
    : FOR    ${key}    IN    @{EditAobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${EditAobUserDetail["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${EditAobUserDetail}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}

