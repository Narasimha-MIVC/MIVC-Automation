*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify only staff has access to dial plan and permissions to change and edit Operations in Dial plan.
...              Palla Surya Kumar

Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***
As a staff user verify whether he has access to dial plan and permissions to change and edit Operations in Dial plan.
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "primary_partition" page
    And I move to "dialplan" tab
    ${DialPlanDict}=  I edit enabled digit from Dial plan    Operator
    And When I switch to "ph_system_dialplan" page
    And I verify edited dial plan from phone system page    &{DialPlanDict}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
