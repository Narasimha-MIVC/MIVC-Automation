*** Settings ***
Documentation     BOSS Personal Information - Tab Displays with content verification
...               dev-Jim Wendt

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../Variables/EnvVariables.robot

#BOSS Component
Library           ../lib/BossComponent.py
Library  String

*** Test Cases ***

Add Account Level Authorized Contacts
    Given I Login To ${URL} With ${username} And ${password}
Verify Personal Information Page
    And I go to personal information page
    Then I verify Contact tab
Verify Roles and Permissions Tab
    When I switch to Roles and Permissions tab
    Then I verify Roles and Permissions tab
Verify Notification Preferences Tab
    When I switch to Notification Preferences tab
    Then I verify Notification Preferences tab
Verify Contact Tab
    When I switch to Contact tab
    Then I log off

*** Keywords ***

Set Init Env
    ${NAME} =	Set Variable	\${username}
    Set Suite Variable	${NAME}  boss_auto_dm_VYtC4uLv@shoretel.com
    ${NAME} =	Set Variable	\${password}
    Set Suite Variable	${NAME}  Abc123!!