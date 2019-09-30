*** Settings ***
Documentation     Transfer-Conference-Feature
...               Aakash
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        10 minutes
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
Transfer-Conference-Feature   
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Intercom transfer
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserA starts a call to UserB 
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB verifies incoming call in dashboard
    Check Incoming Call with ${client2}
    
    # UserB answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB transfers the call to UserC
    Place End Call with ${client2} and intercom_transfer and ${user03.first_name} ${user03.last_name}
    
    # UserC verifies that incoming call notification in present
    Check Incoming Call with ${client3}
    
    # UserC receives call
    Place End Call with ${client3} and recv and ${EMPTY}
    
    # Verifies that UserB is droped from the call
    Verify No Ongoing Call with ${client2}
    
    # UserC ends the call
    Place End Call with ${client3} and end_call_dashboard and ${EMPTY}
    
    # Intercom Conference
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    # UserA starts a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB answers the call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    # UserB adds UserC for Consult Conference
    Place End Call with ${client2} and intercom_conference and ${user03.first_name} ${user03.last_name}
    Verify Hold Consult In Conf Call with ${client2} and consulting
    Verify Hold Consult In Conf Call with ${client2} and Merge
    Sleep      2s
    
    # UserC answers the call
    #Verify Users In A Dashboard In Call with ${client1} and two_users and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    # UserC answers the call
    #Verify Users In A Dashboard In Call with ${client2} and two_users and ${user01.first_name} ${user01.last_name} and ${user03.first_name} ${user03.last_name}
    # UserC answers the call
    #Verify Users In A Dashboard In Call with ${client3} and two_users and ${user01.first_name} ${user01.last_name} and ${user02.first_name} ${user02.last_name}
    
    # UserA and UserB ends the call
    Place End Call with ${client1} and end_call_dashboard and ${EMPTY}
    Place End Call with ${client2} and end_call_dashboard and ${EMPTY}
    
    
    
    # Close the Manhattan Client 
    # Close Application with ${client3}
    # Close Application with ${client2}
    # Close Application with ${client1}