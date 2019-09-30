*** Settings ***
Documentation     MH_Transfer_when_the_call_is_in_hold
...               Bhupendra Parihar
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections

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
MH_Transfer_when_the_call_is_in_hold
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name} 
    
    # UserA checks details of UserB
    Check User Detail Attribute with ${client1} and info and positive
    Check User Detail Attribute with ${client1} and call and positive
    Check User Detail Attribute with ${client1} and min and positive
    
    # UserA places a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}

    # UserB verifies that incoming call notification in present
    Check Incoming Call with ${client2}
       
    # UserB receives call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB verifies that in client pane caller name is present
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and onCall and ${EMPTY} and ${EMPTY}
        
    # UserA verifies that in client pane callee name is present
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY}
        
    # UserA checks call details of outgoing call
    Check User Detail Attribute with ${client1} and info and positive
    Check User Detail Attribute with ${client1} and timer and positive
    Check User Detail Attribute with ${client1} and endCall and positive
    Check User Detail Attribute with ${client1} and holdCall and positive
    Check User Detail Attribute with ${client1} and mute and positive
    Check User Detail Attribute with ${client1} and video and positive
    Check User Detail Attribute with ${client1} and share and positive
    Check User Detail Attribute with ${client1} and conf and positive
    Check User Detail Attribute with ${client1} and transfer and positive
    Check User Detail Attribute with ${client1} and record and positive
        
    # UserB again opens contact card of UserA
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name} 
   
    # UserB verifies that in client pane caller name is present
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and onCall and ${EMPTY} and ${EMPTY}
        
    # UserB checks call details of incoming call
    Check User Detail Attribute with ${client2} and info and positive
    Check User Detail Attribute with ${client2} and timer and positive
    Check User Detail Attribute with ${client2} and endCall and positive
    Check User Detail Attribute with ${client2} and holdCall and positive
    Check User Detail Attribute with ${client2} and mute and positive
    Check User Detail Attribute with ${client2} and video and positive
    Check User Detail Attribute with ${client2} and share and positive
    Check User Detail Attribute with ${client2} and conf and positive
    Check User Detail Attribute with ${client2} and transfer and positive
    Check User Detail Attribute with ${client2} and record and positive
        
    # UserA clicks on hold button
    Place End Call with ${client1} and hold and ${EMPTY}
    
    # UserA verifies on hold options for UserB
    Verify Hold User Dashboard with ${client1} and ${user02.first_name} ${user02.last_name} and on_hold
    Verify Hold Unhold In Third Panel with ${client1} and timer_onhold_call
    Verify Hold Unhold In Third Panel with ${client1} and resume
        
    # UserB transfers the call to UserC
    Place End Call with ${client2} and trans and ${user03.first_name} ${user03.last_name}

    # UserC verifies that incoming call notification in present
    Check Incoming Call with ${client3}
    
    # UserC answers the call
    Place End Call with ${client3} and recv and ${EMPTY}

    # Verifies that UserA is droped from the call
    Verify No Ongoing Call with ${client2}
    Place End Call with ${client1} and end and ${EMPTY}