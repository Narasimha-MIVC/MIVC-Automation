*** Settings ***
Documentation     Login to BOSS portal as PM user and Validate allignment of Settings field for AA menu
...               Priyanka M
...               Comments:

#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/EnvVariables.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
01 Login to the boss portal as PM user and verify Allignment of Settings field
    [Tags]      Regression    Generic

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    ### Actions:
    #1. Switch to VCFE page
    When I switch to "Visual_Call_Flow_Editor" page
    #2. Verify Language Field allignment for AA menu
    Then I verify Allignment in VCFE with Settings
    sleep  2s
    [Teardown]
    Run Keywords  I log off
    ...           I check for alert

