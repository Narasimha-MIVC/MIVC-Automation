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
Verify the logout Button on Locations and users page
    [Tags]  Regression  f1
    Given I login to AOB page
    and I verify the page "Welcome"
    When I navigate to transfer numbers page from welcome page
    Then I verify the page "Transfer Numbers"
    And I click on tab "Set Up" on aob page
    and I verify the page "Locations and User"
    When I click logout button
