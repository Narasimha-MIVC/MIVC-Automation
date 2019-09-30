*** Settings ***
Documentation     MH_conversation_screen_consult_transfer
...               Aakash
...               Comments:
Default Tags        tc-Suite
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        6 minutes
Test Teardown       Custom Teardown

*** Variables ***
# Moved to Test Variables file 

*** Keywords ***	     
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
    
*** Test Cases ***
MH_conversation_screen_consult_transfer     
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Search extension and open third panel
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name} 
    
    # Check Info button in third panel    
    Check User Detail Attribute with ${client1} and info and positive
    # Check call button in third panel
    Check User Detail Attribute with ${client1} and call and positive
    # Check min button in third panel
    Check User Detail Attribute with ${client1} and min and positive
    
    # Place call from connectauto1 third pane to connectauto2
    Place End Call with ${client1} and start and ${EMPTY}
    
    # Check incoming call options
    Check Incoming Call with ${client2}
    
    # Answer call
    Place End Call with ${client2} and recv and ${EMPTY}
    #Sleep      10s
    
    # Check client pane of connectauto2
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and onCall and 1 and ${EMPTY}
    # Check client pane of connectauto1
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and 1 and ${EMPTY}
    
    # Check connectauto1 conversation pane
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
    
    # connectauto2 transfer call to connectauto3
    Place End Call with ${client2} and consult and ${user03.first_name} ${user03.last_name}
    
    # connectauto3 answers call
    Place End Call with ${client3} and recv and ${EMPTY}
    
    # connectauto3 ends the call
    Place End Call with ${client3} and end and ${EMPTY}
    Place End Call with ${client1} and end and ${EMPTY}   
    
    
    # Close the Manhattan Client 
    # Close Application with ${client1}
    # Close Application with ${client2}
    # Close Application with ${client3}