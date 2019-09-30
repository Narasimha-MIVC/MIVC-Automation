*** Settings ***
Documentation  Regression
...            Validate decimal value of multiple digit time out for PM user
...            Palla Surya Kumar

#Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

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
Validate decimal value of multiple digit time out for PM user
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    &{VCFEFields} =  copy dictionary  ${AA_01}
    @{Aa_MDT}=    Create List    1000.1    6999.9
    Set to Dictionary    ${VCFEFields}    decimal_value    ${Aa_MDT}
    And I validate VCFE component fields    &{VCFEFields}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
