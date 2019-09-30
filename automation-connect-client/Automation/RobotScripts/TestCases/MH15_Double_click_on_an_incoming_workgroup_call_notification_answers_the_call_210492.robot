*** Settings ***
Documentation     MH15_Double_click_on_an_incoming_workgroup_call_notification_answers_the_call
...               Bhupendra Parihar
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
MH15_Double_click_on_an_incoming_workgroup_call_notification_answers_the_call
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Click login button in the second panel
    Handle Workgroup Login with ${client2} and yes and yes and ${Workgroup01.first_name}
    # set status "[$client1 command action handle_workgroup present=yes login=yes workGroupName=autoworkgroup1 component_id=$componentId1]"        
			
    # User B called to workgroup.
    Call Contact By Double Click with ${client1} and ${Workgroup01.first_name}
    # set status "[$client1 command action call_contact_by_doubleclick searchItem=autoworkgroup1 component_id=$componentId2]"
    
    # User A answers by double clicking on workgroup incoming call
    # Only user with license_type=operator are allowed to answer the call on double click
    Double Click Dashboard Notification with ${client2} and operator and call
    
    # User A ended the call of user B
    Place End Call with ${client1} and end and ${EMPTY}
    
    # Logout from Workgroup
    #Handle Workgroup Logout with ${client1} and yes and yes and ${Workgroup01.first_name} and ${Workgroup01.first_name}
    Handle Workgroup Logout with ${client2}    
    #Sleep     2s
       