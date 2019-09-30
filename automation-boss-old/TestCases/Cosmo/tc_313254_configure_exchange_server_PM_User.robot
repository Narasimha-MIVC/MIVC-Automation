*** Settings ***
Documentation    1. navigate to App integration tab in the add on features page
...              2. configure the exchange server as user Email ID

#...               Priyanka
#...               Comments:

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
#Variables          Variables/BCA_Variables.py

#BOSS Component
Library           ../../lib/BossComponent.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
1. Login as PM user and Configure Exchange Server
    [Tags]    Sanity-phase2

    #1.  Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}

    #2. move to phone system -> Add-on feature
    And I switch to "addonfeatures" page
    sleep  5s
    #3 move to Add-on feature->App Integrations tab
    And I move to "App Integrations" tab

    #4 configure Exchange server
    And I configure exchange server name    ${exchange_server_name}
    #5 [Teardown]

    Run Keywords  I log off
    ...           I check for alert
    ...         #  Close The Browsers
