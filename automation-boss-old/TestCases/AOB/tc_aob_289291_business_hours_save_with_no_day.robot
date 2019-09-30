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
    
    #then I click business hours add button
    then I click button with Add text
    
    then I unselect the days in Add Business Hours screen
    
    then I click primary Save button
    
    I verify AOB message "At least one day is required"
    
    