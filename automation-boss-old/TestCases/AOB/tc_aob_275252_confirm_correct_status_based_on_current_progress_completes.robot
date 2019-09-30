*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot

#Variable filesot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Confirm Correct Status based on Current Progress as Completed - Activates
    [Tags]  Sanity
    Given I login to AOB page
    and I verify the page "Welcome"
    then I navigate to Location and user page
    and I verify the page "Locations and User"
    #Activates On    In Progress - Activates    Not Started - Activates   Completed - Activates
    ${status}=  I verify location status "Completed - Activates" and button "Revisit"
    Run Keyword If   '${status}' == 'False'   run keyword  I go to add user page
    Run Keyword If   '${status}' == 'False'   run keyword  I create all user for one location   &{multiple_user}
    Run Keyword If   '${status}' == 'False'   run keyword  I login to AOB page
    Run Keyword If   '${status}' == 'False'   run keyword  I verify the page "Welcome"
    Run Keyword If   '${status}' == 'False'   run keyword  I navigate to Location and user page
    Run Keyword If   '${status}' == 'False'   run keyword  I verify the page "Locations and User"
    Run Keyword If   '${status}' == 'False'   run keyword  I verify location status "Completed - Activates" and button "Revisit"