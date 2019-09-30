*** Settings ***
Documentation     Events-Join-Feature
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        10 minutes
Test Teardown       Custom Teardown

*** Variables ***
# Moved to Test Variables file
&{params}     phone_type=desk_phone    

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
    call method    ${client2}    select_phone_type    &{params}
    Close Applications with 3

Serial Teardown
    Run Keywords    call method    ${client2}    select_phone_type    &{params}    AND    call method    ${client1}    close_application    AND    call method    ${client2}    close_application    AND    call method    ${client3}    close_application

*** Test cases ***
Events-Join-Feature
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision

# select softphone type for userB
    Select Phone Type with ${client2} and soft_phone and ${EMPTY}

# UserA opens Events tab
    Invoke Dashboard Tab with ${client1} and event

# UserA clicks on new event button
    Open New Event with ${client1}

# UserA enters meeting name
    Events Add Meeting Details with ${client1} and event_273002 and 1

# UserA adds UserB as participant
    Events Meeting Type Add User with ${client1} and presenters and ${user02.first_name} ${user02.last_name}

# Show meeting settings and select radio button to automatically join audio portion of a meeting
    Events Change Meeting Settings with ${client1} and show
    Configure Meeting Settings with ${client1} and dial_out_to_participants and automatic

# UserA clicks on create button in client
    Events Create Invite with ${client1}

# UserA clicks on event in second panel
    Open Event Info with ${client1} and event_273002 and ${EMPTY}

# UserA joins audio & web conference by dial-in
    Join Endo Conference with ${client1} and by_dial_in and internal_number and deskphone

# Softphone: Click initiates a dial in and user enters the conference without having to enter a participant code

# UserB opens Events panel
    Invoke Dashboard Tab with ${client2} and event
    
# UserB clicks on event in second panel
    Open Event Info with ${client2} and event_273002 and ${EMPTY}

# UserB joins audio & web conference by dial-in
    Join Endo Conference with ${client2} and by_dial_in and internal_number and softphone 

# UserA verifies the attendee in dashboard
    Verifying Event Users Avail with ${client1} and ${user02.first_name} ${user02.last_name} and Endo

# UserB verifies the attendee in dashboard
    Verifying Event Users Avail with ${client2} and ${user01.first_name} ${user01.last_name} and Endo

# UserA clicks on event entry in dashboard to open second panel
    Open Conference Panel with ${client1} and event_273002 

# UserB clicks on event entry in dashboard to open second panel
    Open Conference Panel with ${client2} and event_273002 

# UserA leaves conference by Hangup the phone
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}

# UserB leaves conference by Hangup the phone
    Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}

# Remove conference entry from UserB's dashboard
    Close Conference Entry with ${client2} and participant

# Remove conference entry from UserA's dashboard
    Close Conference Entry with ${client1} and organizer

#  cancel/delete event
    Invoke Dashboard Tab with ${client1} and event
    Open Event Info with ${client1} and event_273002 and ${EMPTY}
    Cancel Event with ${client1}

# UserB assigns himself back to deskphone
    Select Phone Type with ${client2} and desk_phone and ${EMPTY}
    Close Panel with ${client2} and second

# below done    
# Deskphone: click initiates a call back, user presses 1 to join
# UserB does external assignment
    Add New Label with ${client2} and External and ${user03.sip_trunk_did} and 2 and 10
    Close Panel with ${client2} and second

# UserB opens Events tab
    Invoke Dashboard Tab with ${client2} and event

# Make sure that there is no residual conference entry on dashboard
    Close Conference Entry with ${client1} and organizer

# UserA opens Events tab
    Invoke Dashboard Tab with ${client1} and event

# UserA clicks on new event button
    Sleep    2s
    Open New Event with ${client1}

# UserA enters meeting name
    Events Add Meeting Details with ${client1} and test_event_press_one and 1

# UserA adds UserB as participant
    Events Meeting Type Add User with ${client1} and presenters and ${user02.first_name} ${user02.last_name}

# UserA clicks on create button in cleint
    Sleep    2s
    Events Create Invite with ${client1}
    Sleep    2s

# Open event information
    Open Event Info with ${client1} and test_event_press_one and ${EMPTY}

# UserA joins audio & web conference by pressing 1
    Join Endo Conference with ${client1} and by_dial_in and internal_number and deskphone 

# Open dialpad
    Open Dialpad with ${client1}
    Click Dialpad Numbers with ${client1} and one
    Close Dialpad Search with ${client1}
    Sleep     1s

# External assignment: click initiates a call back, user presses 1 to join
    Open Event Info with ${client2} and test_event_press_one and ${EMPTY}

# UserB joins audio & web conference by pressing 1 on external number
    Join Endo Conference with ${client2} and by_dial_in and external_number and ${EMPTY} 

# UserB accpets call on external number
    Call Control with ${client3} and recv and ${EMPTY} and ${EMPTY}

# Open dialpad and press one
    Open Dialpad with ${client3}
    Click Dialpad Numbers with ${client3} and one
    Close Dialpad Search with ${client3}

# UserA verifies the attendee in dashboard
    Verifying Event Users Avail with ${client1} and ${user02.first_name} ${user02.last_name} and Endo

# UserB verifies the attendee in dashboard
    Verifying Event Users Avail with ${client2} and ${user01.first_name} ${user01.last_name} and Endo

# UserA clicks on event entry in dashboard to open second panel
    Open Conference Panel with ${client1} and test_event_press_one 

# UserB leaves audio conference
    Call Control with ${client3} and end and ${EMPTY} and ${EMPTY}

# UserA leaves audion conference
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}

# Remove conference entry from UserA's dashboard
    Close Conference Entry with ${client1} and organizer

# Remove conference entry from UserB's dashboard
    Close Conference Entry with ${client2} and participant

# Cancel Meetings
    Invoke Dashboard Tab with ${client1} and event
    Open Event Info with ${client1} and test_event_press_one and ${EMPTY}
    Cancel Event with ${client1}