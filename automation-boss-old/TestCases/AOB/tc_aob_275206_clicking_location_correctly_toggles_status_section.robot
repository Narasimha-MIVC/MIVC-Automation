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
Navigate to Location and User page and validate location creation date
    [Tags]  Sanity
    Given I login to AOB page
    and I verify the page "Welcome"
    and I navigate to Location and user page
    @{status_list}=    Create List    Activates On    In Progress - Activates    Not Started - Activates
    ${loc_name}  ${date}=  then I check activation date   @{status_list}