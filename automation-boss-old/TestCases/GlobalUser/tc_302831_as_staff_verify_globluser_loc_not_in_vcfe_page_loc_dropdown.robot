*** Settings ***
Documentation    Global User Regression Test Cases
...              Verify global user location not present in VCFE page location dropdown.
...              Palla Surya Kumar

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource    ../../RobotKeywords/BossKeywords.robot

#Variable files
Resource    ../../Variables/EnvVariables.robot
Resource          ../GlobalUser/Variables/global_variables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
As staff verify global user location not present in VCFE page location dropdown.
   [Tags]    GlobalUser    Regression
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName1} with ${AccWithoutLogin} option
   Set to Dictionary    ${testglobaluser_location}    geo_location    Global User
   Set to Dictionary    ${testglobaluser_location}    verify_global_location    Yes
   When I switch to "Visual_Call_Flow_Editor" page
   And I verify global user loc not in VCFE page    &{testglobaluser_location}
   [Teardown]  run keywords  I log off
    ...                      I check for alert

