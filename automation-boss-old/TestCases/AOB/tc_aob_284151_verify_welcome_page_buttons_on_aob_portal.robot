*** Settings ***
Documentation    Verify Welcome page Buttons on AOB portal

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
01 UI have the Transfer Phone Numbers, Set Up Locations and Users buttons in circular Icon
    When I login to AOB page
    Then I verify element "welcome_page_transfer_icon_block" exists
    And I verify element "welcome_page_locations_users_icon_block" exists
