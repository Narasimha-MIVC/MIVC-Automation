*** Settings ***
Documentation    AOB - Transfer Numbers page clicking save button show require that at least one letter has been entered in the -Provider Name- text box that shows when Current Provider is set to Other (specify)

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
#Resource          ../../Variables/LoginDetails.robot
Resource          Variables/aob_variables.robot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
01 Empty provider name shows an error
    Given I login to AOB page
    and I navigate to transfer numbers page from welcome page
    and I click Transfer button
    and I select other current provider
    and I click on authorization checkbox
    When I save Transfer request
    Then BOSSKeywords.I verify "Provider name required" is displayed on screen

02 Numbers only provider name shows an error
    Given I login to AOB page
    and I navigate to transfer numbers page from welcome page
    and I click Transfer button
    and I select other current provider
    and I insert "${random_int}" into provider name
    and I click on authorization checkbox
    When I save Transfer request
    Then BOSSKeywords.I verify "Invalid provider name" is displayed on screen

03 Letters only provider name passes the validation
    Given I login to AOB page
    and I navigate to transfer numbers page from welcome page
    and I click Transfer button
    and I select other current provider
    and I insert "${random_str}" into provider name
    and I click on authorization checkbox
    When I save Transfer request
    Then I verify "Provider name required" is not displayed on screen
    and I verify "Invalid provider name" is not displayed on screen

*** Keywords ***
Set Init Env
    ${random_str}=    Generate Random String    8    [LETTERS]
    ${random_int}=    Generate Random String    4    [NUMBERS]
    Set suite variable    ${random_str}
    Set suite variable    ${random_int}