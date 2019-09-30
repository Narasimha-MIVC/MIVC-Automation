*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../AOB/Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Verify Tranfer More button allows to Transfer more number
    [Tags]  Regression  f1
    Given I login to AOB page
    When I navigate to transfer numbers page from welcome page
    Then I verify the page "Transfer Numbers"
    set to dictionary  ${AOBTransferPhoneNumber}   currentProvider   Astound Broadband

    When I configure transfer number page  &{AOBTransferPhoneNumber}
    And I click "Save" button
    And I click "Got It" button
    Then I verify the page "Transfer Numbers"

    And I click "Continue" button
    And I go to add user page
    Then I verify the page "Users for"

    set to dictionary  ${AobUserDetail}   phone   Existing   #Select which option to select in user page for phone number
    set to dictionary  ${AobUserDetail}   number   None      #To select first number
    I create User  &{AobUserDetail}
    I click "Save" button

    When I switch bundle and verify text
    When I click on skip user button
    Then I verify the page "Call Handling for"

    When I select "Don't Set Up" button on call handling page
    Then I verify the page "Activate"
    Then I verify temporary number "Set Up temporary forwarding" on activation page


*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    3    12345678
    ${uni_int1}=    Generate Random String    4    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}
    Set suite variable    ${uni_int1}

    Set suite variable    &{AOBTransferPhoneNumber}
    : FOR    ${key}    IN    @{AOBTransferPhoneNumber.keys()}
    \    ${updated_val}=    Replace String    ${AOBTransferPhoneNumber["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AOBTransferPhoneNumber}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_int}    ${uni_int1}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}
