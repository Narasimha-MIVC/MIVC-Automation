*** Settings ***
Documentation    Verify Transfer numbers page on AOB Portal

#Suite Setup and Teardown
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
01 Verify Transfer numbers page on AOB Portal
    Given I login to AOB page
    When I navigate to transfer numbers page from welcome page
    Then I verify Transfer requests page


