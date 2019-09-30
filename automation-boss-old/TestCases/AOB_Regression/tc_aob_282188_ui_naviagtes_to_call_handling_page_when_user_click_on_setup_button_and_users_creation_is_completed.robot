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
UI Naviagest to call hadling page upon clicking on Revisit button
    [Tags]  Regression
    Given I login to AOB page
    and I navigate to Location and user page
    then I check button name for location and user
    ${status}=  I verify location status "Completed - Activates" and button "Revisit"
    Run Keyword If   '${status}' == 'False'   run keyword  I go to add user page
    Run Keyword If   '${status}' == 'False'   run keyword  I create all user for one location   &{multiple_user}
    Run Keyword If   '${status}' == 'False'   run keyword  I login to AOB page
    Run Keyword If   '${status}' == 'False'   run keyword  I verify the page "Welcome"
    Run Keyword If   '${status}' == 'False'   run keyword  I navigate to Location and user page
    Run Keyword If   '${status}' == 'False'   run keyword  I verify the page "Locations and User"
    Run Keyword If   '${status}' == 'False'   run keyword  I verify location status "Completed - Activates" and button "Revisit"
    Run Keyword If   '${status}' == 'False'   run keyword  I click "Revisit" button
    Run Keyword If   '${status}' == 'False'   run keyword  I verify the page "Call Handling for "
    Run Keyword If   '${status}' == 'True'   run keyword  I click "Revisit" button
    Run Keyword If   '${status}' == 'True'   run keyword  I verify the page "Call Handling for "


