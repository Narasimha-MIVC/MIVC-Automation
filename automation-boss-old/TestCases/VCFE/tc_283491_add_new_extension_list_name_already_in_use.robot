*** Settings ***
Documentation    To add VCFE Extension list and validate the error message for Name already in use
...              Immani Mahesh Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/UserInfo.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String


*** Test Cases ***
01 Vcfe Create Extension list with DM user
    [Tags]  Regression     EL    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    And I create extension list     &{Extensionlist01}
    [Teardown]  run keywords  i delete vcfe entry by name ${Extensionlist01['extnlistname']}
    ...                       I check for alert
    ...                       And I log off


02 Vcfe Create Extension list with PM user
	[Tags]  Regression     EL
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    And I create extension list     &{Extensionlist01}
    [Teardown]  run keywords  i delete vcfe entry by name ${Extensionlist01['extnlistname']}
    ...                       I check for alert
    ...                       And I log off


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{Extensionlist01}

    : FOR    ${key}    IN    @{Extensionlist01.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist01}    ${key}    ${updated_val}
