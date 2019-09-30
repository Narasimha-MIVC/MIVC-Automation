*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...

Suite Teardown    Close The Browsers
Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot

Resource          ../GlobalUser/Variables/global_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections

*** Test Cases ***
1. Global User : Verify UserLocation dropdown during Add user show global locations for which there are available TNs
    [Tags]    GlobalUser    NonSmr
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "users" page
    then I verify the page "users"
    ${locList}=  I get locations from user location dropdown
    And I switch to "phone_number" page
    then I verify the page "Phone Numbers"
    Log    ${locList}    console=yes
    then I verify availability of tns of ${locList}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

