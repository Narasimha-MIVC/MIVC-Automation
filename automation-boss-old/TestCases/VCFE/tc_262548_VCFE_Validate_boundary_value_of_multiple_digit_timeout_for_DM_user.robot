*** Settings ***
Documentation  Regression
...            Validate boundary value of multiple digit time out for DM user
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
Validate boundary value of multiple digit time out for DM user
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    &{VCFEFields} =  copy dictionary  ${AA_01}
    @{Aa_MDT}=    Create List    900    8000   abcdefg    1000  7000    5000
    Set to Dictionary    ${VCFEFields}    boundary_value    ${Aa_MDT}
    And I validate VCFE component fields    &{VCFEFields}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
