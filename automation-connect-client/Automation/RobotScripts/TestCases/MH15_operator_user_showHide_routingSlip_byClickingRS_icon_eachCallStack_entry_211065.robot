*** Settings ***
Documentation     MH15_operator_user_showHide_routingSlip_byClickingRS_icon_eachCallStack_entry
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
MH15_operator_user_showHide_routingSlip_byClickingRS_icon_eachCallStack_entry
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
# select show routing slip option for userA 
    Check Uncheck Routing Slip with ${client1} and yes

# userB calls userA
    Call Contact By DoubleClick with ${client2} and ${user01.first_name} ${user01.last_name}

#userA answers the call
    Call Control with ${client1} and recv and ${EMPTY} and ${EMPTY}

# userA verifies routing slip
    Click Verify Routing Slip with ${client1} and 1 and yes and simple_call and ${user02.first_name} ${user02.last_name} and ${user01.first_name} ${user01.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY}

#STEP-4 // not possible to automate this : tooltip checking is not possible in automation             

# userA hides the routing slip by clicking on routing slip icon and again clicks on RS to show it 
    Click Verify Routing Slip with ${client1} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and yes
    Click Verify Routing Slip with ${client1} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and yes and ${EMPTY}

# userA put the call with userB on hold and close the contact card of userB from third panel
    Call Control with ${client1} and hold and ${EMPTY} and ${EMPTY}
    Close Panel with ${client1} and third

# userA hides the routing slip by clicking on routing slip icon
    Click Verify Routing Slip with ${client1} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and held and ${EMPTY} and yes

# end the call from userB
    Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}