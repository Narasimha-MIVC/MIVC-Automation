*** Settings ***
Documentation    To Edit VCFE Extension List and to validate error message changed Name already in use
...              Immani Mahesh Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Vcfe Edit Extension list and verify message "name already in use" with DM user
    [Tags]  Regression		EL    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${user_extn}
    and Set to Dictionary    ${Extensionlist02}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    Then I create extension list    &{Extensionlist02}
    and Set to Dictionary    ${EditExtensionlist01}    extnlistname   ${Extensionlist02['extnlistname']}
    i select vcfe component by searching name "${Extensionlist01['extnlistname']}"
    Then I edit extension list  &{EditExtensionlist01}
    [Teardown]  run keywords  And I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{Extensionlist01}

    : FOR    ${key}    IN    @{Extensionlist01.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist01}    ${key}    ${updated_val}


    : FOR    ${key}    IN    @{Extensionlist02.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist02}    ${key}    ${updated_val}