*** Settings ***
Documentation   BOSS Personal Information - Add Account Level Authorized Contacts
...             dev-Jim Wendt

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../Variables/EnvVariables.robot
Resource          ../Variables/UserInfo.robot

#BOSS Component
Library           ../lib/BossComponent.py

*** Test Cases ***
Add Account Level Authorized Contacts
    Given I Login To ${URL} with ${username} and ${password}
    And I go to personal information page
    Then I switch to Roles and Permissions tab

Add Roles, Verify and Delete
    #When I add role Billing
    #Then I remove role Billing
    #When I add role Partner
    #Then I remove role Partner
    #When I add role Phone Manager
    #Then I remove role Phone Manager
    #When I add role Technical
    #Then I remove role Technical
    When I add role Emergency
    Then I log off

Change Role Location to User Location for Emergency
    Given I Login To ${URL} with ${username} and ${password}
    And I go to personal information page
    And I switch to Roles and Permissions tab
    Then I change the location for role Emergency to ${location}
    And I log off
    Given I Login To ${URL} with ${username} and ${password}
    And I go to personal information page
    And I switch to Roles and Permissions tab
    Then I remove the location for role Emergency
    And I remove role Emergency
    And I log off

*** Keywords ***

Set Init Env
    ${NAME} =	Set Variable	\${username}
    Set Suite Variable	${NAME}  boss_auto_dm_VYtC4uLv@shoretel.com
    ${NAME} =	Set Variable	\${password}
    Set Suite Variable	${NAME}  Abc123!!
    ${NAME} =	Set Variable	\${location}
    Set Suite Variable	${NAME}  AobLoc1