*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...
Suite Teardown    Close The Browsers
Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot
#Resource    ../../Variables/PhoneNumberInfo.robot

Resource          ../GlobalUser/Variables/global_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***

1. Global User : Verify Global User Number Service
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "phonenumber" page
    And I verify turnup service      &{globalservice}
    [Teardown]  run keywords  I log off
    ...                      I check for alert
