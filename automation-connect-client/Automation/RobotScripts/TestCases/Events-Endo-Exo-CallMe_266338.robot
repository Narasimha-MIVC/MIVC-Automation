*** Settings ***
Documentation     Events-Endo-Exo-CallMe_266338
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        15 minutes
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
    ${objects_list}=   Launch Login with ${user01} and ${user02} and ${user03} and ${user04} and 4 
    
    ${client_one} =      Get From List      ${objects_list}      0   
    ${client_two} =      Get From List      ${objects_list}      1
    ${client_three} =    Get From List      ${objects_list}      2
	${client_four} =     Get From List      ${objects_list}      3 

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three}
	Set Test Variable    ${client4}    ${client_four}      


Serial Execution
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port4}          WITH NAME      client4 

    ${client_one}=    Get library instance      client1   
    ${client_two}=    Get library instance      client2
    ${client_three}=  Get library instance      client3
	${client_four}=   Get library instance      client4  

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three}
	Set Test Variable    ${client4}    ${client_four} 
    
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  5
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    
Parallel Teardown
    Close Applications with 4

Serial Teardown
    Run Keywords    call method      ${client1}      close_browser         AND      call method      ${client2}      close_browser    AND      call method      ${client3}      close_browser    AND      call method      ${client4}      close_browser            


Keyword 2
    [Arguments]       ${client1}    ${client2}     ${client3}     ${client4}
    
    Invoke Dashboard Tab with ${client1} and event
    # UserA clicks on new event button
    Open New Event with ${client1}

    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and auto_join and 1
    Sleep    1s

    # UserA adds UserB as participant
    Events Meeting Type Add User with ${client1} and presenters and ${user02.first_name} ${user02.last_name}

    # Show meeting settings and select radio button to automatically join audio portion of a meeting
    Events Change Meeting Settings with ${client1} and show
    Configure Meeting Settings with ${client1} and dial_out_to_participants and automatic
    
    # UserA clicks on create button in cleint
    Events Create Invite with ${client1}
    Sleep    8s

    # UserA clicks on Send button in outlook to create event
    #Send Meeting Request Outlook with ${client1} and send_meeting_invite and auto_join    
        
    
*** Test cases ***
Events-Endo-Exo-CallMe  
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Checks that if event exists otherwise create it
    ${eventFound}=   Get Event with ${client1} and auto_join 
    
    Run Keyword If  "${eventFound}" == "no"  Keyword 2   ${client1}   ${client2}   ${client3}    ${client4}
    
    # Test audio through Call Me feature through Endo for entering both internal extension and External Number
    # Call-Me for internal extension from Endo client
    Open Event Info with ${client1} and auto_join and ${EMPTY}
    
    # Places call to UserC's extension
    Join Event By Callme with ${client1} and endo and ${user04.extension}
    
    # UserC receives call
    Place End Call with ${client4} and recv and ${EMPTY}
    
    # Call-Me for external number from Endo client
    Invoke Dashboard Tab with ${client2} and event
    Open Event Info with ${client2} and auto_join and ${EMPTY}
    
    # Places call to UserD's DID in another PBX
    Join Event By Callme with ${client2} and endo and ${user03.sip_trunk_did}
    Sleep     2s
    
    # UserC receives call
    Place End Call with ${client3} and recv and ${EMPTY}
    
    # Userd hangs up the conference call
    Place End Call with ${client4} and end and ${EMPTY}
    
    # UserD hangs up the conference call
    Place End Call with ${client3} and end and ${EMPTY}
    Sleep    2s
    
    # Remove conference entry from UserC's dashboard
    Close Conference Entry with ${client4} and participant

    # Remove conference entry from UserA's dashboard
    Close Conference Entry with ${client1} and organizer    
    
    # Test audio through Call Me feature through Exo for entering both internal extension and External Number
    # Call-Me for internal extension from Exo client
    # UserA opens Events tab
    Invoke Dashboard Tab with ${client1} and event
    Sleep    3s
    Open Event Info with ${client1} and auto_join and info
    
    # Copy event URL
    ${conferenceURL}=   Get Url with ${client1}

    # Join event in chat mode
    Join Endo Conference with ${client1} and web_chat_mode and ${EMPTY} and ${EMPTY}

    # Launch browser for UserE
    Import Library        ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py      ${port5}          WITH NAME      browser1
    ${browser1}=  Get library instance      browser1

    Launch Url with ${browser1} and ${conferenceURL}

    # Call-Me from Exo client
    Join Exo Event with ${browser1} and UserE
    Sleep    1s 
    Join Event By Callme with ${browser1} and exo and ${user04.extension}
    
    # UserC receives call
    Place End Call with ${client4} and recv and ${EMPTY}
    Sleep     2s    
    Place End Call with ${client4} and end_call_dashboard and ${EMPTY}    
    
    #Close Browser with ${browser1}
    
    # Call-Me for external number from Exo client
    # Launch browser for UserE    
    Import Library        ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py      ${port6}          WITH NAME      browser2
    ${browser2}=  Get library instance      browser2

    Launch Url with ${browser2} and ${conferenceURL}

    # Call-Me from Exo client
    Join Exo Event with ${browser2} and UserE
    Sleep    1s 
    Join Event By Callme with ${browser2} and exo and ${user03.sip_trunk_did}
    
    # UserC receives call
    Place End Call with ${client3} and recv and ${EMPTY}
    Sleep     2s    
    Place End Call with ${client3} and end and ${EMPTY}    
    
    # Delete Event with name event_266329
    Invoke Dashboard Tab with ${client1} and event    
    Sleep    2s    
    Open Event Info with ${client1} and auto_join and ${EMPTY}
    Cancel Event with ${client1}

    call method      ${browser1}      close_browser
    call method      ${browser2}      close_browser