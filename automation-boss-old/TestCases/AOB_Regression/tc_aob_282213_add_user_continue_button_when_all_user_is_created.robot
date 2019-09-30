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
Add user continue button when all user is created
    [Tags]  Regression
    Given I login to AOB page
    and I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    When I switch bundle and verify text
    ${status}=  I check for user in current bundle
    ${bundle_name}=   I get current bundle name
    Set to Dictionary    ${multiple_user}    bundle    ${bundle_name}     #add bundle name in dictionary
    Run Keyword If   '${status}' == 'True'   run keyword   I create multiple user for one bundle     &{multiple_user}
    Run Keyword If   '${status}' == 'True'   run keyword   I check "Continue" is present
    Run Keyword If   '${status}' == 'True'   run keyword   I check "Add User" is present
    Run Keyword If   '${status}' == 'False'   run keyword   I check "Continue" is present
    Run Keyword If   '${status}' == 'False'   run keyword   I check "Add User" is present

