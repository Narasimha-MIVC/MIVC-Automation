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
Select Pending port in and unassigned number
    [Tags]  Sanity
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    When I switch to account ${AOBAccount} with ${AccWithoutLogin} option
    When I switch to "phonenumber" page
    Then I add PhoneNumber    &{AOBPhoneNumber}
    When I switch to "aob" page
    When I navigate to Location and user page
    then I check button name for location and user
    When I go to add user page
    Then I verify the page "Users for"
    ${bundle_name}=  I get current bundle name
    Set to Dictionary    ${AobUserDetail}    phone    Existing     #other option: "Existing" or "None"
    Set to Dictionary    ${AobUserDetail}    number    ${AOBPhoneNumber['numberRange']}  #Give None if you want to select random number, Provide Number if you want to select specific
    Then I create User  &{AobUserDetail}
    Then I click "Save" button   #Cancel or Save
    and I check user name "${AobUserDetail['firstName']} ${AobUserDetail['lastName']}" for bundle "${bundle_name}"


Show only Available or Pending Port In and Unassigned
    [Tags]  Sanity
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    When I switch to account ${AOBAccount} with ${AccWithoutLogin} option
    When I switch to "phonenumber" page
    ${AOBPhoneNumber['numberRange']}=  evaluate  ${AOBPhoneNumber['numberRange']}+1
    Set to Dictionary    ${AOBPhoneNumber}    number    ${AOBPhoneNumber['numberRange']}
    and I update single phone number state    &{AOBPhoneNumber}
    When I switch to "aob" page
    When I navigate to Location and user page
    then I check button name for location and user
    When I go to add user page
    Then I verify the page "Users for"
    Then I check if phone number "${AOBPhoneNumber['numberRange']}" is not available

*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    3    0123456789
    ${ext}=    Generate Random String    4    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}

    Set suite variable    &{AOBPhoneNumber}
    : FOR    ${key}    IN    @{AOBPhoneNumber.keys()}
    \    ${updated_val}=    Replace String    ${AOBPhoneNumber["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AOBPhoneNumber}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_int}    ${ext}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}