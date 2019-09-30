*** Settings ***
Documentation     Blind-conference-in-a-mesh-conference
...               Aakash
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
Blind-confernce-in-a-mesh-conference  
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    #UserA opens contact card of UserB
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
    
    
       
    # UserB starts conference with UserC
    Place End Call with ${client2} and conf and ${user03.first_name} ${user03.last_name}
    
    # UserC verifies that incoming call notification in present
    Check Incoming Call with ${client3}
    
    # UserC receives call
    Place End Call with ${client3} and recv and ${EMPTY}    
    Sleep     3s
    # UserC verifies that in Dashboard there is a group call with UserB and UserA
    Verify Users In A Dashboard In Call with ${client3} and two_users and ${user01.first_name} ${user01.last_name} and ${user02.first_name} ${user02.last_name}
    
    # UserB starts conference with UserD
    Place End Call with ${client2} and conf and ${user04.first_name} ${user04.last_name}
    
    # UserD verifies incoming call options
    Check Incoming Call with ${client4}
    
    # Answer call
    Place End Call with ${client4} and recv and ${EMPTY}    
    Sleep     2s
    # UserC verifies that in Dashboard there is a group call with UserB and UserA
    Verify Three Users In A Dashboard In Call with ${client3} and three_users and ${user01.first_name} ${user01.last_name} and ${user02.first_name} ${user02.last_name} and ${user04.first_name} ${user04.last_name}
    
    # UserA,UserB,UserC  ends the call
    Place End Call with ${client1} and end and ${EMPTY}    
    Place End Call with ${client3} and end and ${EMPTY}    
    
    Logout with ${client1} and 0
    Logout with ${client2} and 0
    Logout with ${client3} and 0
    Logout with ${client4} and 0
    