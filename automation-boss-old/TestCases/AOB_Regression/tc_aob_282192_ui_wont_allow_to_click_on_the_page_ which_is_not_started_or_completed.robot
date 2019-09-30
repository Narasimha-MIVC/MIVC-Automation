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
UI wont allow to click on the page which is not stared or completed
    [Tags]  Regression
    Given I login to AOB page
    When I navigate to Location and user page
    And I go to add user page
    Then I verify the page "Users for"
    Then I check "Activate" is enabled


