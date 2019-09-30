*** Settings ***
Documentation  Regression
...            Verify the tool tip text for Staff user
...            Palla Surya Kumar

#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/AutoAttendantInfo.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
Verify the tool tip text for Staff user
    [Tags]    AA    Regression    one    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    &{VCFEFields} =  copy dictionary  ${AA_01}
    #below 'demo_text' value is given just as [Key-Value] pair purpose, it has nothing to do with API
    SET TO DICTIONARY  ${VCFEFields}    tooltip_info    demo_text
    And I validate VCFE component fields    &{VCFEFields}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
