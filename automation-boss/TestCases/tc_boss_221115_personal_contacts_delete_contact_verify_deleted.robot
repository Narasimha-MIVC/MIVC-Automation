*** Settings ***
Documentation     BOSS Personal Contacts - Delete the Personal contact
...               dev-Jim Wendt

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition files
Resource          ../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../Variables/EnvVariables.robot
Resource          ../Variables/PersonalContactsInfo.robot

#BOSS Component
Library           ../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***
Personal Contacts - Delete the Personal contact
    Given I login to ${URL} with ${username} and ${password}
    And I navigate to personal contacts page
    And I add personal contact success  &{Contact}
    Then I delete personal contact  &{Contact}
    And I log off

*** Keywords ***
Set Init Env
    ${NAME} =	Set Variable	\${username}
    Set Suite Variable	${NAME}  a2user2dm@mitel.com
    ${NAME} =	Set Variable	\${password}
    Set Suite Variable	${NAME}  Abc123!!

    ${uni_str}=     Generate Random String    20    [LETTERS][NUMBERS]
    Set suite variable  ${uni_str}
    Set suite variable  &{Contact}
    Set to Dictionary   ${Contact}    departmentName    ${uni_str}



