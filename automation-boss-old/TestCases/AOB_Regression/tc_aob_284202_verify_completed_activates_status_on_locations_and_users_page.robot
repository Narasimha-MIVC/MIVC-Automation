*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../AOB/Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Verify completed Activates status on locations and users page
    [Tags]  Regression
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

*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    3    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}

    Set suite variable    &{AOBTransferPhoneNumber}
    : FOR    ${key}    IN    @{AOBTransferPhoneNumber.keys()}
    \    ${updated_val}=    Replace String    ${AOBTransferPhoneNumber["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AOBTransferPhoneNumber}    ${key}    ${updated_val}

