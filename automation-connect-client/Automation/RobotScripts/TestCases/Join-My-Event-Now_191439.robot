*** Settings ***
Documentation     Join-My-Event-Now
...               Bhupendra Singh Parihar
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        4 minutes
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
    ${objects_list}=   Launch Login with ${user01} and ${user02} and ${user03} and ${user04} and 3 
    
    ${client_one} =      Get From List      ${objects_list}      0   
    ${client_two} =      Get From List      ${objects_list}      1
    ${client_three} =    Get From List      ${objects_list}      2 

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three}      


Serial Execution
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3 
    
    ${client_one}=    Get library instance      client1   
    ${client_two}=    Get library instance      client2
    ${client_three}=  Get library instance      client3  

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three} 
    
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  4
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
   
Parallel Teardown
    Close Applications with 3

Serial Teardown
    Run Keywords    call method      ${client1}      close_browser         AND      call method      ${client2}      close_browser    AND      call method      ${client3}      close_browser             

*** Test cases ***
Join-My-Event-Now
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # UserA, UserB and UserC opens Event tab
    Invoke Dashboard Tab with ${client1} and event
    Invoke Dashboard Tab with ${client2} and event
    Invoke Dashboard Tab with ${client3} and event

    # UserA clicks on new event button
    Open New Event with ${client1}

    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and event_191439 and 1

    # UserA adds UserB as participant
    Events Meeting Type Add User with ${client1} and presenters and ${user02.first_name} ${user02.last_name}
    Events Meeting Type Add User with ${client1} and presenters and ${user03.first_name} ${user03.last_name}

    # Show meeting settings and select radio button to automatically join audio portion of a meeting
    Events Change Meeting Settings with ${client1} and show
    Configure Meeting Settings with ${client1} and dial_out_to_participants and automatic

    # UserA clicks on create button in client
    Events Create Invite with ${client1}
			    
    # Click on event
    Open Event Info with ${client1} and event_191439 and ${EMPTY}
    Join Endo Conference with ${client1} and by_dial_in and internal_number and deskphone
    Click First Ongoing Event with ${client1}
    
    # UserB joins web conference
    Open Event Info with ${client2} and event_191439 and ${EMPTY}
    Join Endo Conference with ${client2} and by_dial_in and internal_number and deskphone
    Click First Ongoing Event with ${client2}

    # UserC joins web conference
    Open Event Info with ${client3} and event_191439 and ${EMPTY}
    Join Endo Conference with ${client3} and by_dial_in and internal_number and deskphone
    Click First Ongoing Event with ${client3}
    
    # UserA verifies attendees
    Verifying Event Users Avail with ${client1} and ${user02.first_name} ${user02.last_name} and Endo
    Verifying Event Users Avail with ${client1} and ${user03.first_name} ${user03.last_name} and Endo
    
    # UserB verifies attendees
    Verifying Event Users Avail with ${client2} and ${user01.first_name} ${user01.last_name} and Endo
    Verifying Event Users Avail with ${client2} and ${user03.first_name} ${user03.last_name} and Endo
    
    # UserC verifies attendees
    Verifying Event Users Avail with ${client3} and ${user01.first_name} ${user01.last_name} and Endo
    Verifying Event Users Avail with ${client3} and ${user02.first_name} ${user02.last_name} and Endo

    # UserA sends an IM to group
    Send IM with ${client1} and from_A_to_group
    # UserB verifies IM send by UserA
    Received IMA with ${client2} and true and from_A_to_group
    # UserC verifies IM send by UserA
    Received IMA with ${client3} and true and from_A_to_group
    
    # UserA leaves conference by Hangup the phone
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}
    Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}
    Call Control with ${client3} and end and ${EMPTY} and ${EMPTY}

# Delete Event with name event_191439
    Invoke Dashboard Tab with ${client1} and event
    Open Event Info with ${client1} and event_191439 and ${EMPTY}
    Cancel Event with ${client1}