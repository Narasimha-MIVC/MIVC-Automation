*** Settings ***
Documentation     Events-Endo-Conference
...               Bhupendra Singh Parihar
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        10 minutes
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

Keyword 2
    [Arguments]       ${client1}
    
    # UserA opens Events tab
    Invoke Dashboard Tab with ${client1} and event
    
    # UserA clicks on new event button
    Open New Event with ${client1}

    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and event_266329 and 1

    # UserA adds UserB as participant
    Events Meeting Type Add User with ${client1} and presenters and ${user02.first_name} ${user02.last_name}

    # Show meeting settings and select radio button to automatically join audio portion of a meeting
    Events Change Meeting Settings with ${client1} and show
    Configure Meeting Settings with ${client1} and dial_out_to_participants and automatic
    

    # UserA clicks on create button in client
    Events Create Invite with ${client1}
    Sleep    8s
    # UserA clicks on Send button in outlook to create event
    #Send Meeting Request Outlook with ${client1} and send_meeting_invite and event_266329      

*** Test cases ***
Events-Endo-Conference
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    ${eventFound}=   Get Event with ${client1} and event_266329
	
    Close Presenter with ${client1}

    Run Keyword If  "${eventFound}" == "no"  Keyword 2   ${client1}    
   
    # UserA clicks on event in second panel
    Open Event Info with ${client1} and event_266329 and ${EMPTY}
    
    # UserA joins audio & web conference by dial-in
    Join Endo Conference with ${client1} and by_dial_in and internal_number and deskphone 
    Click First Ongoing Event with ${client1}
    
    # UserB opens Events panel
    Invoke Dashboard Tab with ${client2} and event
    
    # UserB clicks on event in second panel
    Open Event Info with ${client2} and event_266329 and ${EMPTY}
    
    # UserB joins audio & web conference by dial-in
    Join Endo Conference with ${client2} and by_dial_in and internal_number and deskphone 
    Click First Ongoing Event with ${client2}

    # UserA verifies the attendee in dashboard
    Verifying Event Users Avail with ${client1} and ${user02.first_name} ${user02.last_name} and Endo

    # UserB verifies the attendee in dashboard
    Verifying Event Users Avail with ${client2} and ${user01.first_name} ${user01.last_name} and Endo
            
# Full Screen Share
    # UserA clicks on share and Share full Screen buttons to starts full screen share
    Share Endo Client Screen with ${client1} and no and share_full_screen and organizer

    # UserB is waiting for UserA to start sharing
    Click First Ongoing Event with ${client2}

    # UserB verifies that sharing is in progress
    #Verify Screen Share with ${client2} and sharing_in_progress

    # UserA starts recording the conference
    Record Conference with ${client1} and start_recording
    
    # UserA stops recording
    Record Conference with ${client1} and stop_recording
        
    # UserA stops sharing
    Play Pause Close Presenter with ${client1} and pause
    Sleep     2s
    Play Pause Close Presenter with ${client1} and close
    Sleep     2s        
# Area Share
    # UserA clicks on share and Area Screen buttons to starts Area share
    Share Endo Client Screen with ${client1} and no and share_area and organizer
    Sleep    5s    
    
    # UserB verifies that sharing is in progress
    #Verify Screen Share with ${client2} and sharing_in_progress
    
    # UserA stops sharing
    Play Pause Close Presenter with ${client1} and pause
    Sleep    2s
    Play Pause Close Presenter with ${client1} and close    
    Sleep    2s    
# Window Share
    # UserA clicks on share and window Share button to start Window share
    Share Endo Client Screen with ${client1} and no and share_window and organizer
    Sleep   6s
    
    # UserB verifies that sharing is in progress
    #Verify Screen Share with ${client2} and sharing_in_progress
    
    # UserA stops sharing
    Play Pause Close Presenter with ${client1} and pause
    Sleep    2s
    Play Pause Close Presenter with ${client1} and close
        
    # UserA leaves conference by Hangup the phone
    Place End Call with ${client1} and end and ${EMPTY} 
    # UserB leaves conference by Hangup the phone
    Place End Call with ${client2} and end and ${EMPTY} 
        
# Record conference (UCB) and play through Endo client
    # UserA opens the events to play the recording
    Sleep     2s
    Invoke Dashboard Tab with ${client1} and event
    Sleep     3s    
    Open Event Info with ${client1} and event_266329 and ${EMPTY}

    # Play the recording via connect client
    Play Download Delete Recording with ${client1} and play    
    Sleep    4s

# Delete Event with name event_266329
    Invoke Dashboard Tab with ${client1} and event        
    Open Event Info with ${client1} and event_266329 and ${EMPTY}
    Cancel Event with ${client1}
    Sleep    3s
	