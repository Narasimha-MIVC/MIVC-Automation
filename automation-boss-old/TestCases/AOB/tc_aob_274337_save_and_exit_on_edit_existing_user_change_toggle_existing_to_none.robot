*** Settings ***
Documentation     AOB regression Suite
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
Change Phone number toggle to None from Existing
    [Tags]  Sanity
    Given I login to AOB page   #&{AOB_login_dic}
    and I verify the page "Welcome"
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    ${status}   ${num}=  I check if user exist with phone number
    log to console  ${status}
    Set to Dictionary    ${AobUserDetail}    phone    Existing     #other option: "Existing" or "None"
    Set to Dictionary    ${AobUserDetail}    number    None     #Give None if you want to select random number, Provide Number if you want to select specific
    Set to Dictionary    ${EditAobUserDetail}    phone    None     #other option: "Existing" or "None"
    Set to Dictionary    ${EditAobUserDetail}    number    None     #Give None if you want to select random number, Provide Number if you want to select specific
    Run Keyword If   '${status}' == 'False'   run keyword    I create User  &{AobUserDetail}
    Run Keyword If   '${status}' == 'False'   run keyword    and I click "Save" button
    Run Keyword If   '${status}' == 'False'   run keyword    I check if user is created
    Run Keyword If   '${status}' == 'False'   run keyword    I Edit AOB User   &{EditAobUserDetail}
    Run Keyword If   '${status}' == 'False'   run keyword    I click save and logout button
    Run Keyword If   '${status}' == 'True'   run keyword     I Edit AOB User   &{EditAobUserDetail}
    Run Keyword If   '${status}' == 'True'   run keyword     I click save and logout button
    Run Keyword If   '${status}' == 'True'   run keyword     I verify the page "Sign in to Mitel"
    I login to AOB page   #&{AOB_login_dic}
    and I verify the page "Welcome"
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    then I check if phone number "${num}" becomes available

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

