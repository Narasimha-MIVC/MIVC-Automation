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
UI navigates to Call Handling page when atleast one user is created
    [Tags]  Regression
    Given I login to AOB page
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    ${status}=  I check if user is created
    Run Keyword If   '${status}' == 'False'   run keyword   I create User  &{AobUserDetail}
    then I switch bundle and verify text
    ${heading}=  I click on skip user button
    and I verify the page "Call Handling for"


