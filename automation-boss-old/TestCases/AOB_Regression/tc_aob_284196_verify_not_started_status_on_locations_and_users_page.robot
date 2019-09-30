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
Verify Not Started -Activates status on locations and users page
    [Tags]  Regression
    Given I login to AOB page
    and I verify the page "Welcome"
    then I navigate to Location and user page
    and I verify the page "Locations and User"
    #Activates On    In Progress - Activates    Not Started - Activates   Completed - Activates
    ${status}=  I verify location status "Not Started - Activates" and button "Start"
    Run Keyword If   '${status}' == 'False'   run keyword   should be true  ${status}

