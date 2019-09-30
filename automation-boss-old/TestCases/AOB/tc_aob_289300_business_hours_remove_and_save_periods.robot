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
    
    then I remove All Business Hours
    
    #then I click business hours add button
    then I click button with Add text
    
    then I Add Multiple Business Hours
    
    then I remove All Business Hours
    
    #business hours have a close button and also other elements
    ${close_buttons_count}=   I get number of elements "aob_x_close_button"
    
    when I Add Single Business Hours
    
    #verify there is only one single business hour period
    and I verify Business Hours Count matches "${close_buttons_count+1}"
    
    then I click button with Save text
    
    then I click Business Hours section
    
    #verify the business hour was saved correctly all the way
    and I verify Business Hours Count matches "${close_buttons_count+1}"
    