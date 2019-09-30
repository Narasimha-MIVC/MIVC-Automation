*** Settings ***
Documentation    Suite description
...               dev-Vasuja
...
Suite Teardown    Close The Browsers

Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot
Resource          ../../Variables/Geolocationinfo.robot

Resource          ../GlobalUser/Variables/global_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library   string
*** Test Cases ***

1. Global User : Verify two new radio buttons in close location wizard
    [Tags]    GlobalUser  test
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName1} with ${AccWithoutLogin} option
   And I switch to "geographic_locations" page
   Set to Dictionary    ${geolocation_US}    location     ${GlobalUserBillingLoc}
   And I switch to "close_location" page for "&{geolocation_US}[location]"
   Then I verify radio button "geo_close_radio1"
   Then I verify radio button "geo_close_radio2"
   And I click on "closeLocation_Wizard_cancel" button/link
   And I click on "confirm_box" button/link
   [Teardown]  run keywords  I log off
   ...                       I check for alert
