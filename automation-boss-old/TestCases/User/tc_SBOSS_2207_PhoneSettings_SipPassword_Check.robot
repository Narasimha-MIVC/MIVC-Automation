*** Settings ***
Documentation    Suite description
...               dev-Shilpa K N

#Variable files
Resource    ../../Variables/EnvVariables.robot

#Keywords Definition file
Resource    ../../RobotKeywords/BossKeywords.robot

#BOSS Component
Library	    ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***

1. User : Verify Sip Password in Phone Settings
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName1} with ${AccWithoutLogin} option
   And I switch to "users" page
   then I verify the page "users"
   then I verify sip password in phone settings of user ${username}
