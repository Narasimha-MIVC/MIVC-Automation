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
#add mobility to globaluser via personalinformation page
1. Global User : Add Global User to mobility
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "users" page
    And I add mobility profile      &{add_mobility_profile}
    [Teardown]  run keywords  I log off
    ...                      I check for alert


