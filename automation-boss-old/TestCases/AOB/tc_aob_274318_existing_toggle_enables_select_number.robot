*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Existing toggle enables Select Number
    [Tags]  Sanity
    Given I login to AOB page
    and I navigate to Location and user page
    and I verify the page "Locations and Users"
    then I go to add user page
    and I verify the page "Users for"
    then I cilck button "Existing" to check phone number drop down status


