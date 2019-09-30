*** Settings ***
Documentation    Suite description
#...               dev-Rohit Arora
...

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../GlobalUser/Variables/global_variables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections
*** Test Cases ***
Update access numbers for an existing Global SMR country
    [Tags]    GlobalUser, SMR
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "instances" page
    And I update a global country of smr instance     &{Instances}
    [Teardown]  run keywords  I log off
    ...                      I check for alert
