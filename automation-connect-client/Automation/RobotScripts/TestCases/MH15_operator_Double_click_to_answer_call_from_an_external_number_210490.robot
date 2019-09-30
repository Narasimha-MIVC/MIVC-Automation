*** Settings ***
Documentation     MH15_operator_Double_click_to_answer_call_from_an_external_number
...               HariPrakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        4 minutes
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
MH15_operator_Double_click_to_answer_call_from_an_external_number
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
	
    # Search extension and open third panel
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name} 
           
    # UserB places a call to UserB
    Place End Call with ${client2} and start and ${EMPTY}
               
    # UserA verifies that incoming call notification in present
    Check Incoming Call with ${client1}
    
    # UserA receives call
    #Place End Call with ${client1} and recv and ${EMPTY}
	
	Double Click Dashboard Notification with ${client1} and operator and call
        
    
    #UserA receives call
    Place End Call with ${client1} and end and ${EMPTY}
	
 
