*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...
Suite Teardown    Close The Browsers
Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot

Resource          ../GlobalUser/Variables/global_variables.robot
Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***


1. Global User : Verify Provisioning Details of GlobalUser Service
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "services" page
    then I verify the page "services"
    then I verify provisioning details of service     &{globaluser_userservice}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

