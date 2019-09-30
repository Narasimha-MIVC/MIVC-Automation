*** Settings ***
Documentation  This is a test file to check if your dependency installations

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Env file
Resource          ../../Variables/EnvVariables.robot

#libraries
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***

BOSS Login
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I log off