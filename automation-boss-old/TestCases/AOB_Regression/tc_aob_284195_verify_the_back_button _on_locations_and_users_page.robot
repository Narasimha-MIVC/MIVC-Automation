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
Verify the Back Button on Locations and users page
    [Tags]  Regression
    Given I login to AOB page
    and I verify the page "Welcome"
    then I navigate to Location and user page
    and I verify the page "Locations and User"
    When I click back button
    and I verify the page "Transfer Numbers"
