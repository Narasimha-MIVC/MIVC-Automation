*** Settings ***
Documentation    Global User Regression Test Cases
...              Verify global user location not present in account page geo location tab
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
As DM verify global user location not present in account page geo location tab
   [Tags]    GlobalUser    Regression    NonSmr
   Given I login to ${URL} with ${DMemail} and ${DMpassword}
   sleep  3s
   Set to Dictionary    ${testglobaluser_location}    geo_location    Global User
   And I switch to "account_details" page
   And I verify global user loc not in account details page    &{testglobaluser_location}
   [Teardown]  run keywords  I log off
    ...                      I check for alert

