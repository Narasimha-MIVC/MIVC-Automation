*** Settings ***
Documentation     MH_Blind_conference_in_trunk_party 
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        5 minutes
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
MH_Blind_conference_in_trunk_party
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Search extension and open third panel
    # Search People Extension with ${client1} and ${user02.first_name}
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserA checks details of UserB
    Check User Detail Attribute with ${client1} and info and positive
    Check User Detail Attribute with ${client1} and call and positive
    Check User Detail Attribute with ${client1} and min and positive
    #Sleep      2s
    # UserA places a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    #Sleep      2s
    
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
    Check User Detail Attribute with ${client1} and conf and positive
    Check User Detail Attribute with ${client1} and transfer and positive  
   
    
    # UserB checks call details of incoming call
    Check User Detail Attribute with ${client2} and info and positive
    Check User Detail Attribute with ${client2} and timer and positive
    Check User Detail Attribute with ${client2} and endCall and positive
    Check User Detail Attribute with ${client2} and holdCall and positive
    Check User Detail Attribute with ${client2} and mute and positive
    Check User Detail Attribute with ${client2} and video and positive    
    Check User Detail Attribute with ${client2} and conf and positive
    Check User Detail Attribute with ${client2} and transfer and positive
    #Sleep       2s       
    
    # UserB add external user UserC conference call
    Place End DID Call with ${client2} and did_to_did_conf and ${user03.sip_trunk_did}   
    
    # UserC verifies that an incoming call is present in dashboard
    Check Incoming Call with ${client3}
    
    # UserC receives call
    Place End Call with ${client3} and recv and ${EMPTY}
    #Sleep      2s
    
    # UserA verifies that other 2 parties are in a call
    Verify Users In A Dashboard In Call with ${client1} and two_users and ${user03.sip_trunk_did} and ${user02.client_id}
    
    # UserB verifies that other 2 parties are in a call
    Verify Users In A Dashboard In Call with ${client2} and two_users and ${user03.sip_trunk_did} and ${user01.client_id}
    
    # UserA hangs up the call
    Place End Call with ${client1} and end and ${EMPTY}
    
    # UserB hangs up the call
    Place End Call with ${client2} and end and ${EMPTY}
    
                
    #Closes the Manhattan Client
    # Close Application with ${client2}
    # Close Application with ${client1}
    # Close Application with ${client3}
    
