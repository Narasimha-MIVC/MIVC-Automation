*** Settings ***
Documentation   BOSS Personal Information - Update Contact Information
...             dev-Jim Wendt

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../Variables/EnvVariables.robot

#BOSS Component
Library           ../lib/BossComponent.py

*** Test Cases ***

Update Contact Information and Location
    Given I Login To ${URL} With ${username} And ${password}
    Then I go to personal information page
    When I change the user First Name to first name and save
    And I change the user last name to last name and save
    And I change the user title to title and save
    And I change the user business email to business@mitel.com and save
    And I change the user personal email to personal@mitel.com and save
    And I change the user mobile phone to 5551111111 and save
    And I change the user home phone to 5552222222 and save
    Then I log off
*** Keywords ***

Set Init Env
    ${NAME} =	Set Variable	\${username}
    Set Suite Variable	${NAME}  a2user2dm@mitel.com
    ${NAME} =	Set Variable	\${password}
    Set Suite Variable	${NAME}  Abc123!!