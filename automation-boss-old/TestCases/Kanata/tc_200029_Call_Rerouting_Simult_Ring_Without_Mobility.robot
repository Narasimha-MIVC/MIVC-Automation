*** Settings ***
Documentation    Suite description

#Suite Teardown
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../Kanata/Variables/global_variables.robot

#BOSS ComponentTestCas
Library           ../../lib/BossComponent.py

*** Test Cases ***

Testing Call Rerouting - Simultanious Ring Without Mobility
    [Tags]    REGRESSION
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${AutomationNew} with ${AccWithoutLogin} option
    When I open Call Routing for user auser1@shoretel.com
    then I open Configure Main Settings with Phone Numbers

