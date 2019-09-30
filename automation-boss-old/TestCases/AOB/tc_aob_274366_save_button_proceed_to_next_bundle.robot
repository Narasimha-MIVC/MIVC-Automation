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
Verify User page opened properly
    [Tags]  Sanity
    Given I login to AOB page
    and I verify the page "Welcome"
    and I navigate to Location and user page
    then I check button name for location and user
    and I go to add user page
    and I verify the page "Users for"
    ${bundle_name}=   I get current bundle name
    Set to Dictionary    ${multiple_user}    bundle    ${bundle_name}     #add bundle name in dictionary
    then I create multiple user for one bundle     &{multiple_user}
