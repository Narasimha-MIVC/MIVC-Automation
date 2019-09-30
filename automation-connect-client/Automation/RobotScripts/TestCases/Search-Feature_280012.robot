*** Settings ***
Documentation     Search-Feature
...               Bhupendra Singh Parihar
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        6 minutes
Test Teardown       Custom Teardown 

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Custom Teardown
    Run Keyword If   ${conf.parallel_execution} == 1    Parallel Teardown    ELSE    Serial Teardown 

User Provision
    [Arguments]       ${client1}     ${client2}     
    Log   ${client1}

Parallel Execution
    Import Library			    ${CURDIR}/../../ManhattanLibrary/lib/mnh_parallel_executor.py
    ${objects_list}=   Launch Login with ${user01} and ${user02} and ${user03} and ${user04} and 2 
    
    ${client_one} =      Get From List      ${objects_list}      0   
    ${client_two} =      Get From List      ${objects_list}      1     

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}         


Serial Execution
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
        
    ${client_one}=    Get library instance      client1   
    ${client_two}=    Get library instance      client2     

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}    
    
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  3
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}

Parallel Teardown
    Close Applications with 2

Serial Teardown
    Run Keywords    call method      ${client1}      close_browser         AND      call method      ${client2}      close_browser                 

*** Test cases ***
Search-Feature
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision 
    
    # Select the checkbox for not opening the outlook for contact creation
    Open Outlook Tab with ${client1}
    Configure Outlook Tab with ${client1} and contacts and check
   

    # UserA creates a contact
    Create New Contact with ${client1} and 1 and Mobile and 9977667766 and CUSER_273051 and CLast and shoretel and test and cclast@shoretel.com
    
    sleep    2s
    #Close Panel with ${client1} and second_search
    Close Panel with ${client1} and second
    sleep    2s

    # Initiate search by typing in dialer box and press escape to close search result
    # UserA types UserB's name to initiate search
    Initiate Search Close Dialog with ${client1} and ${user02.first_name}

    #Clicking star on a search result should add the contact to favorites. Clicking on star should not open contact card.
    #UserA adds UserC to Favorites
    Add Or Delete To Favorite Group with ${client1} and CUSER_273051 and add
    Close Panel with ${client1} and second_search
    
    # UserA verifies that UserC's contac tcard is not opened
    Verify Contact Card with ${client1} and absent and CUSER_273051
    
    # UserA verifies that UserC's is in UserA's Favorite list
    Invoke Dashboard Tab with ${client1} and people
    Check Favorite Symbol with ${client1} and true and CUSER_273051 CLast

# Double clicking a search result should dial the user's default number
    # UserA places a call to UserB by Double Clicking on its name after search
    Call Contact By Double Click with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserB verifies that it is getting call
    Check Incoming Call with ${client2}

    # UserA disconnects the call
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}
    
# Down arrow should scroll through results
    # UserA types some text and verifies that it is able to scroll
    #Sleep    2s
    Scroll search results use keyboard with ${client1} and down and CUSER
            
# Enter should dial default number of highlighted contact
    # UserA highlightes one contact and press ENTER to place call
    Make call press enter with ${client1} and ${user02.first_name} ${user02.last_name} and yes and ${user02.first_name} ${user02.last_name}
    
    # UserB verifies that it is getting call
    Check Incoming Call with ${client2}

    # UserA disconnects the call
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}
            
# Right clicking on search result should enable the user to also see phone number, department and company
    # Search for a contact
    Search People Extension with ${client1} and CUSER_273051 CLast
    
    # Right click, click on Show department name and verify that department name is visible
    Show Contact Info Right Click with ${client1} and show and dept_name and test
    
    Close Panel with ${client1} and second_search
    
    # Search for a contact
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # Right click, click on Show phone number and verify that phone number is visible
    Show Contact Info Right Click with ${client1} and show and phone_number and ${user02.extension}
        
# When phone number is revealed via right click on each search result row, single clicking the number should dial that number
    # Click on phone number to dial that number
    Call By Click Number Searched Contact with ${client1}
    
    # UserB verifies that it is getting call
    Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}
    
    # UserA disconnects the call
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}
    
    # Hide the phone number revealed via right click
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}

    Show Contact Info Right Click with ${client1} and hide and phone_number and ${EMPTY}
   

