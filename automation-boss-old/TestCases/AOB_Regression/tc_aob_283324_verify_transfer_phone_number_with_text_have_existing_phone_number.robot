*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../AOB/Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Verify Transfer Phone Numbers with text Have existing phone numbers
    [Tags]  Regression
    Given I login to AOB page
    and I verify the page "Welcome"
    Then I check text "Have existing phone numbers? We'll kick off the process to get them moved to Mitel." is present
