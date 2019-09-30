*** Settings ***
Documentation     MH15_connectClient_multi_incomingCall_inRingingState_placed_top_of_stack
...               Indresh Tripathi
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
	${client_four}=  Get library instance      client4  

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
MH15_connectClient_multi_incomingCall_inRingingState_placed_top_of_stack
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
# userA called to userB
    Call Contact By DoubleClick with ${client1} and ${user02.first_name} ${user02.last_name}

# userC called to userB
    Call Contact By DoubleClick with ${client3} and ${user02.first_name} ${user02.last_name}

# userB checks the status of users ## here we are passing the contacts in the same order as we expect to be in connect client license user
    Check Status Of Call InStack with ${client2} and firstCall and ${user03.first_name} ${user03.last_name}
    Check Status Of Call InStack with ${client2} and secondCall and ${user01.first_name} ${user01.last_name}

# userD called to userB
    Call Contact By DoubleClick with ${client4} and ${user02.first_name} ${user02.last_name}

# userB checks the status of users
    Check Status Of Call InStack with ${client2} and firstCall and ${user04.first_name} ${user04.last_name}
    Check Status Of Call InStack with ${client2} and secondCall and ${user03.first_name} ${user03.last_name}
    Check Status Of Call InStack with ${client2} and thirdCall and ${user01.first_name} ${user01.last_name}

#End Calls
    Place End Call with ${client1} and end and ${EMPTY} 
    Place End Call with ${client3} and end and ${EMPTY}
    Place End Call with ${client4} and end and ${EMPTY}