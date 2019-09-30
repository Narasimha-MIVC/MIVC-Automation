*** Settings ***
Documentation     BOSS BCO Sanity suite
...               dev-Kenash, Rahul, Vasuja


#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
01 Login to the boss portal and create contract
    Given I login to http://10.198.105.68 with staff@shoretel.com and Test123!!
    and I switch to "switch_account" page
    and I switch to account Test-AOB2 with ${AccWithoutLogin} option
    When I switch to "aob" page
