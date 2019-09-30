*** Settings ***
Documentation     Call-Control-Feature
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        13 minutes
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
 
    
*** Test cases ***
Call-Control-Feature 
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Select SoftPhone of USERA
    Select Phone Type with ${client1} and desk_phone and ${EMPTY}
    #Sleep     1s
    # Select SoftPhone of USERB
    Select Phone Type with ${client2} and desk_phone and ${EMPTY}
    #Sleep     1s
    Close Panel with ${client2} and second
    #Sleep     1s
    # Make outgoing call which is not in the system and hold/unhold
    # UserA searches for UserD and opens third panel    
    Search People Extension with ${client1} and ${user03.first_name} ${user03.last_name}

    # UserA checks details of UserD
    Check User Detail Attribute with ${client1} and call and positive
    
    # UserA starts a call to UserD
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserD verifies incoming call in dashboard
    Check Incoming Call with ${client3}

    # UserD answers the call
    Place End Call with ${client3} and recv and ${EMPTY}
    #Sleep      2s
    
    # UserA puts the call to UserD on hold
    Place End Call with ${client1} and hold and ${EMPTY}
    
    # UserA verifies that resume button is getting displayed
    Verify Hold Unhold In Third Panel with ${client1} and resume
    #Sleep      2s
    Sleep      1s
    
    # UserA clicks on Retrieve button
    Place End Call with ${client1} and unHold and ${EMPTY}
    
    # UserA verifies that hold button is getting displayed
    Verify Hold Unhold In Third Panel with ${client1} and hold
    
    # UserA ends the call to UserD
    Place End Call with ${client1} and end and ${EMPTY}
    
    # UserD closes the Client
    #Close Application with ${client3}
    
    #Receive Inbound call to Client. Make sure this call appears in the dashboard.
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserA starts a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB verifies incoming call in dashboard
    Check Incoming Call with ${client2}
    
    # UserB answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB Verifies that the call appears in the dashboards
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and onCall and ${EMPTY} and ${EMPTY}
    # UserA Verifies that the call appears in the dashboard
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY}
    
    # Make an internal call from client & Hold/UnHold and audio is successfull
    # UserA puts the call to UserB on hold
    Place End Call with ${client1} and hold and ${EMPTY}
    #Sleep       2s
    
    # UserA verifies that call to UserB is actually on hold
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onHold and ${EMPTY} and yes
    
    # UserA retrieves the call to UserB
    Place End Call with ${client1} and unHold and ${EMPTY}
    
    # UserA verifies that call to UserB is actually in unhold state
    Verify Hold Unhold In Third Panel with ${client1} and timer_normal_call
    
    # Blind transfer
    # UserB transfers the call to UserC
    Place End Call with ${client2} and trans and ${user03.first_name} ${user03.last_name}
    Sleep     1s
    # UserC verifies that incoming call notification in present
    Check Incoming Call with ${client3}
    
    # UserC receives call
    Place End Call with ${client3} and recv and ${EMPTY}
    
    # Verifies that UserB is droped from the call
    Verify No Ongoing Call with ${client2} 

    # UserC ends the call
    Place End Call with ${client3} and endTransfer and ${EMPTY}
    
    # Consult Transfer
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name} 
    
    # UserA starts a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB does consult transfer to UserC
    Place End Call with ${client2} and consult and ${user03.first_name} ${user03.last_name}
    Sleep       1s
    
    # UserC verifies incoming call in dashboard
    Check Incoming Call with ${client3}
    
    # UserC answers the call
    Place End Call with ${client3} and recv and ${EMPTY}
    #Sleep      2s
    
    # UserB verifies that it is in Consulting state
    Verify Hold Consult In Conf Call with ${client2} and consulting
    # UserB presses merge button to complete consult transfer
    Verify Hold Consult In Conf Call with ${client2} and complete_consult
    # wait for call entry to disappear
    #Sleep      2s
    # Verifies that UserB is droped from the call
    Verify No Ongoing Call with ${client2}
    
    # UserC ends the call
    Place End Call with ${client3} and end and ${EMPTY}
    
    # Blind Conference
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserA starts a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB adds UserC for Blind Conference
    Place End Call with ${client2} and conf and ${user03.first_name} ${user03.last_name}
    #Sleep     1s
    # UserC verifies incoming call in dashboard
    Check Incoming Call with ${client3}

    # UserC answers the call
    Place End Call with ${client3} and recv and ${EMPTY}
    #Sleep     2s
    # UserA verifies that other users present in conference are listed in dashboard
    #Verify Users In A Dashboard In Call with ${client1} and two_users and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    
    # UserA and UserB end the call
    Place End Call with ${client1} and end and ${EMPTY}
    #Sleep    2s
    Place End Call with ${client2} and end and ${EMPTY}
    
    # Consult Conference
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserA starts a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB adds UserC for Consult Conference
    Place End Call with ${client2} and consult_conf and ${user03.first_name} ${user03.last_name}
    #Sleep      1s

    # UserC verifies incoming call in dashboard
    Check Incoming Call with ${client3}

    # UserC answers the call
    Place End Call with ${client3} and recv and ${EMPTY}    
    #Sleep       2s
    # UserB verifies that it is in Consulting state
    Verify Hold Consult In Conf Call with ${client2} and consulting
    
    # UserB presses merge button to complete consult conference
    Verify Hold Consult In Conf Call with ${client2} and Merge
    # wait for calls to get merged
    #Sleep       2s
    
    # UserA verifies that other users present in conference are listed in dashboard
    #Verify Users In A Dashboard In Call with ${client1} and two_users and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    
    # UserA and UserB ends the call
    Place End Call with ${client1} and end and ${EMPTY}
    Place End Call with ${client2} and end and ${EMPTY}
    Sleep    2s
    
    
   