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
Select Available Number from the drop down
    [Tags]  Sanity  dev
    Given I login to AOB page
    Then I navigate to Location and user page
    ${location_name}=   I get current active location name
    Then I open login page with ${URL}
    and I switch to "switch_account" page
    and I switch to account ${AOBAccount} with ${AccWithoutLogin} option
    Then I switch to "order" page
    ${bundle}=   I check initial order for location "${location_name}"
    log to console  ${bundle}
    Then I switch to "aob" page
    Then I navigate to Location and user page
    then I go to add user page
    and I verify initial order in user page    ${bundle}

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

