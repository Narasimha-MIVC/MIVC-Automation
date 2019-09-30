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
    When I configure transfer number page  &{AOBTransferPhoneNumber}
    And I click "Save" button
    And I click "Got It" button
    Then I verify the page "Transfer Numbers"


*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    3    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}

    Set suite variable    &{AOBTransferPhoneNumber}
    : FOR    ${key}    IN    @{AOBTransferPhoneNumber.keys()}
    \    ${updated_val}=    Replace String    ${AOBTransferPhoneNumber["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AOBTransferPhoneNumber}    ${key}    ${updated_val}

