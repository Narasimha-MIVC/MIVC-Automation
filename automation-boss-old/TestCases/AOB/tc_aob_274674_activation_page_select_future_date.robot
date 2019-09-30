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
Proceed to Activation Page
    [Tags]  Sanity  dev
    Given I login to AOB page
    and I verify the page "Welcome"
    then I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    and I verify the page "Users for"
    then I switch bundle and verify text
    ${status}=  I check for user in current bundle
    ${bundle_name}=   I get current bundle name
    Set to Dictionary    ${multiple_user}    bundle    ${bundle_name}     #add bundle name in dictionary
    Run Keyword If   '${status}' == 'True'   run keyword   I create multiple user for one bundle     &{multiple_user}
    Run Keyword If   '${status}' == 'True'   run keyword   I click on skip user button
    Run Keyword If   '${status}' == 'True'   run keyword   I verify the page "Call Handling for"
    Run Keyword If   '${status}' == 'False'   run keyword   I click on skip user button
    Run Keyword If   '${status}' == 'False'   run keyword   I verify the page "Call Handling for"
    Then I select "Don't Set Up" button on call handling page   #"Don't Set Up" or "Set Up" - Choose either of option
    and I verify the page "Activate"
    Then I select future date on activate page
    and I click save & finish button on Activate page
    Then I verify the page "Mitel Easy Setup for"