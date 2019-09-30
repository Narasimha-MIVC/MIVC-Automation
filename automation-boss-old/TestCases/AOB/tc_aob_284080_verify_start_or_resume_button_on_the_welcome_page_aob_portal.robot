*** Settings ***
Documentation    Verify Start or Resume Button on the Welcome page AOB portal

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
01 Verify Start or Resume Button on the Welcome page AOB portal
    When I login to AOB page
    Then I verify Start/Resume button exists
