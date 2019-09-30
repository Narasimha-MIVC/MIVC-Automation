*** Settings ***
Documentation    Verify Billing impact on Add User Type User modal on the Users Page

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
01 Verify Billing impact on Add User Type User modal on the Users Page
    Given I login to AOB page
    And I navigate to Location and user page
    And I go to add user page
    When I open Add User Type modal
    Then I verify Add User Type modal currency fields
