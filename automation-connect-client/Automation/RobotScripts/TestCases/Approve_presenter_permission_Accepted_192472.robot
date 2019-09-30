*** Settings ***
Documentation     Approve_presenter_permission_Accepted
...               Indresh Tripathi
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        7 minutes
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
Approve_presenter_permission_Accepted
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision

    Close Presenter with ${client1}
    
# UserA, UserB and userC opens Event tab
    Invoke Dashboard Tab with ${client1} and event
    Invoke Dashboard Tab with ${client2} and event
    Invoke Dashboard Tab with ${client3} and event

# UserB clicks on new event button
    Open New Event with ${client2}

# UserB enters meeting name
    Events Add Meeting Details with ${client2} and event_192472 and 1
    Events Select Meeting Type with ${client2} and custom
    Sleep    2s

# UserB adds participants to the meeting
    Events Meeting Type Add Users with ${client2} and participants and ${user01.first_name} ${user01.last_name} and ${user03.first_name} ${user03.last_name}

# UserB clicks on create button to create event
    Events Create Invite with ${client2}
    Sleep    4s

# UserB opens event info
    Open Event Info with ${client2} and event_192472 and ${EMPTY}
    Join Endo Conference with ${client2} and web_chat_mode and ${EMPTY} and ${EMPTY}

# UserB joins web conference
    Open Event Info with ${client1} and event_192472 and ${EMPTY}
    Join Endo Conference with ${client1} and web_chat_mode and ${EMPTY} and ${EMPTY}

# UserC joins web conference
    Open Event Info with ${client3} and event_192472 and ${EMPTY}
    Join Endo Conference with ${client3} and web_chat_mode and ${EMPTY} and ${EMPTY}

# UserA clicks on Screen Share button to start full screen share
    Share Endo Client Screen with ${client1} and no and share_full_screen and participant

# UserB verifies that it is getting approval dialog
    Permit Share Screen with ${client2} and no and ${user01.first_name} and ${user01.last_name} and no_action

# UserA clicks away and verifies that dialog disappears
    Click Away Verify Share Dialog with ${client1} and participant

# UserB clicks away and verifies that dialog disappears
    Click Away Verify Share Dialog with ${client2} and orgainzer

# UserA again clicks on Screen Share button and verifies that dialog appears
    Share Endo Client Screen with ${client1} and yes and ${EMPTY} and participant

# UserB grants sharing permission
    Permit Share Screen with ${client2} and yes and ${user01.first_name} and ${user01.last_name} and yes
    Sleep    4s

# UserB and UserC verifies that sharing is in progress
    Verify Screen Share with ${client2} and sharing_in_progress
    Verify Screen Share with ${client3} and sharing_in_progress

# UserA stops sharing
    Play Pause Close Presenter with ${client1} and pause
    Sleep    2s
    Play Pause Close Presenter with ${client1} and close
    Sleep    1s
# Delete Event with name event_266329
    Invoke Dashboard Tab with ${client2} and event        
    Open Event Info with ${client2} and event_192472 and ${EMPTY}
    Cancel Event with ${client2}    