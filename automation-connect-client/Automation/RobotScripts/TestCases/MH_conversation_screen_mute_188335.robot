*** Settings ***
Documentation     MH_conversation_screen_mute
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
    
*** Test Cases ***
MH_conversation_screen_mute     
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    Select Phone Type with ${client1} and desk_phone and ${EMPTY}
    
    # Search extension and open third panel
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name} 
    
    # Verify third panel
    Verify Contact Card with ${client1} and present and ${user02.first_name} ${user02.last_name}
    
    # Check Info button in third panel
    Check User Detail Attribute with ${client1} and info and positive
    # Check call button in third panel
    Check User Detail Attribute with ${client1} and call and positive
    # Check min button in third panel
    Check User Detail Attribute with ${client1} and min and positive
    
    # Place call from connectauto1 third pane to connectauto2
    Place End Call with ${client1} and start and ${EMPTY}
    
    # Check incoming call options at connectauto2
    Check Incoming Call with ${client2}
    # connectauto2 answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # Check client pane of connectauto2
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and onCall and ${EMPTY} and ${EMPTY}
    # Check client pane of connectauto1
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY}
    
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
    
    # connectauto1 click mute
    Click Mute Button with ${client1} and yes

    # connectauto2 click mute
    Click Mute Button with ${client2} and yes 
    
    # connectauto1 unmute
    Click Unmute Button with ${client1} and yes

    # connectauto2 unmute
    Click Unmute Button with ${client2} and yes
    
    # End the call
    Place End Call with ${client1} and end and ${EMPTY}
    
    # Close the Manhattan Client 
    # Close Application with ${client1}
    # Close Application with ${client2}