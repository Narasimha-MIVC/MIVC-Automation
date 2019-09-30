*** Settings ***
Documentation     MH_Alert_when_available_call_theuser
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections

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
MH_Alert_when_available_call_theuser
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
# UserB sets his presence to Vacation
    Change User Telephony Status with ${client2} and vacation
            
# open contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
# From dropdown set "Alert when available"
    Click Filter Under Greeny Button with ${client1} and Alert
    Close Panel with ${client1} and third

# UserB Changes his telephony status to Available
    Change User Telephony Status with ${client2} and available

# UserA verifies that there is a notification in dashboard
    Verify User Notifications with ${client1} and ${user02.first_name} ${user02.last_name}

# UserA clicks on the notification to open contact card
    Verify User Notifications Click with ${client1} and ${user02.first_name} ${user02.last_name}
    Verify Contact Card Status with ${client1} and present and ${user02.first_name} ${user02.last_name} and ${EMPTY}