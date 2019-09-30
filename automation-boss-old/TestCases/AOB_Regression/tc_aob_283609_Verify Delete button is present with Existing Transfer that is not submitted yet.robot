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
Verify Delete button is present with Existing Transfer that is not submitted yet
    [Tags]  Regression
    Given I login to AOB page
    When I navigate to transfer numbers page from welcome page
    Then I verify the page "Transfer Numbers"
    ${status}=   I check transfer number is created
    Run Keyword If   '${status}' == 'False'  run keyword  I configure transfer number page  &{AOBTransferPhoneNumber}
    Run Keyword If   '${status}' == 'False'  run keyword  I click "Save" button
    Run Keyword If   '${status}' == 'False'  run keyword  I click "Got It" button
    Run Keyword If   '${status}' == 'False'  run keyword  I verify the page "Transfer Numbers"
    And I delete first transfer number entry
    Then I check number "${AOBTransferPhoneNumber["numberRange"]}" is present on page
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

