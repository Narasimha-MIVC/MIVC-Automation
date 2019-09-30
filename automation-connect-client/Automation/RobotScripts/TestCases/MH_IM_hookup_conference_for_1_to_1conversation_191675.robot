*** Settings ***
Documentation     MH_IM_hookup_conference_for_1_to_1conversation
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
    
    
*** Test cases ***
MH_IM_hookup_conference_for_1_to_1conversation
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
     
    # UserA opens contact card of UserB
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name}
    
    # UserA sends IM to UserB
    Click Filter Message with ${client2} and Messages 
    Send IM with ${client2} and Hello02
    
    # UserA verifies the IM sent by UserB
    Invoke Dashboard Tab with ${client1} and messages
    Received IMB with ${client1} and true and Hello02
    
    # UserA sends IM to UserB
    Send IM with ${client1} and Hi
    Verify Im Chat Time with ${client1}
    
    
    
    
    
    
    
    
   
    
   