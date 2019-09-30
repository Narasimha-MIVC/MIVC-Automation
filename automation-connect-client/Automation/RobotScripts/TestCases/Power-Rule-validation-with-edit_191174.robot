*** Settings ***
Documentation     Power-Rule-validation-with-edit
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1

Test Timeout     4 minutes
Test Teardown    call method    ${client1}    close_browser
*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   
   

*** Test cases ***
Power-Rule-validation-with-edit
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
   
#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}

# USerA invokes Power Routing tab
    Verify Preferences Power Routing Tab with ${client1}

# Clicks on "Create New Power Rule" button
    Create New Power Rule with ${client1} and PowerRule1234

# Clicks on "+on the phone" tab
    Click On The Phone with ${client1}

# UserA clicks on "Forword Call" button
    Click Forward Call Button with ${client1}

# Selects 'my voicemail' from dropdown
    Configure Forward Call with ${client1} and dropdown and 1

# Clicks on create button and checks for error if it has
    Create Rule Check Error with ${client1} and PowerRule1234 and ${EMPTY}

# Edits the already created rule
    Edit Rule with ${client1} and PowerRule1234

# Removes the condition
    Remove Rule Option with ${client1} and on_the_phone

# Clicks on create button and checks for error if it has
    Edit Rule Check Error with ${client1} and PowerRule1234 and noCondition

# Clicks on "+number matches" tab
    Click On Number Matches with ${client1}

# Selects "The number is any internal number" option from dropdown
    Add Number Matches with ${client1} and 1

# Saves the rule
    Save Rule with ${client1} and PowerRule1234

# Closes the Manhattan Client for UserA
    Close Panel with ${client1} and second
