*** Settings ***
Documentation     BOSS Personal Contacts - Verify Update Button disable
...               dev-Jim Wendt

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition files
Resource          ../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../Variables/EnvVariables.robot

#BOSS Component
Library           ../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***

Personal Contacts - Verify the user is NOT able to add the personal contact
    Given I login to ${URL} with ${username} and ${password}
    And I navigate to personal contacts page
    And I add personal contact required fail
    Then I log off

*** Keywords ***

Set Init Env
    ${NAME} =	Set Variable	\${username}
    Set Suite Variable	${NAME}  bgardner@hbreport.com
    ${NAME} =	Set Variable	\${password}
    Set Suite Variable	${NAME}  Abc123!!