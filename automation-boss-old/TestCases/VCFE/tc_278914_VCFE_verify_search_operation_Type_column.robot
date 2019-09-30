*** Settings ***
Documentation  Regression
...            VCFE Verify search operation on Type column
...            Palla Surya Kumar

#Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/AutoAttendantInfo.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
Verify search operation on Type column for Staff user
    [Tags]    AA    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn}=    I add Auto-Attendant    &{AA_01}
    SET TO DICTIONARY  ${AA_01}     Aa_Extension     ${extn}
    SET TO DICTIONARY  ${AA_01}     comp_type     Auto Attendant
    And I search VCFE component by searching type  &{AA_01}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

Verify search operation on Type column for DM user
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn}=    I add Auto-Attendant    &{AA_01}
    SET TO DICTIONARY  ${AA_01}     Aa_Extension     ${extn}
    SET TO DICTIONARY  ${AA_01}     comp_type     Auto Attendant
    And I search VCFE component by searching type  &{AA_01}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

Verify search operation on Type column for PM user
    [Tags]    AA    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn}=    I add Auto-Attendant    &{AA_01}
    SET TO DICTIONARY  ${AA_01}     Aa_Extension     ${extn}
    SET TO DICTIONARY  ${AA_01}     comp_type     Auto Attendant
    And I search VCFE component by searching type  &{AA_01}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
