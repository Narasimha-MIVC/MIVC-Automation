*** Settings ***
Documentation    To Edit VCFE Extension List and to validate error message Name cannot be blank
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
#Test Setup      run keywords   Given I login to ${URL} with AutoTest_iW53qRaQ@shoretel.com and Abc123!!
#...             ${phone_num}  ${extn}=    and I add user    &{DMUserProfile}
#...             log to console  ${phone_num}
#...             and Set to Dictionary    ${Extensionlist01}    extnNumber    ${extn}

*** Test Cases ***
Vcfe Create Extension list with DM user
    [Tags]  Regression  	EL    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    and Set to Dictionary    ${EditExtensionlist01}    extnlistname    blank
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