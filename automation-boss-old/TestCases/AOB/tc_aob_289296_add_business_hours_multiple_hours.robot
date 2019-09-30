*** Settings ***
Documentation     BOSS AOB regression
...               dev-Alex Medina


#Suite Setup and Teardown
#Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Proceed to Activation Page
    [Tags]  Sanity
    Given I login to AOB page
    and I verify the page "Welcome"
    then I navigate to Location and user page
    then I check button name for location and user
    then I go to add user page
    then I switch bundle and verify text
    
    when I click on skip user button
    then I verify the page "Call Handling for"
    
    when I click Update Call Handling button
    then I click button with Save text
    
    #verify removing all the business hours
    then I remove All Business Hours
    
    #then I click business hours add button
    when I click button with Add text
    
    #very that all the widgets exist in the add business hours screen
    and I verify Add Business Hours widgets
    
    I Add Multiple Business Hours

    