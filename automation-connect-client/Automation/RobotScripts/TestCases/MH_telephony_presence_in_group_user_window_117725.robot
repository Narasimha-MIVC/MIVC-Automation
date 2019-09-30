*** Settings ***
Documentation     MH_telephony_presence_in_group_user_window
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
MH_telephony_presence_in_group_user_window
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision

# Open People tab
    Invoke Dashboard Tab with ${client1} and people

# Create Group with userB as one of the members
    Create New Group with ${client1} and GroupAB and save and ${user02.first_name} ${user02.last_name} and ${EMPTY}

# Change to compact view 
    Select People View with ${client1} and compact

# Verify the telephony presence status
    Select Group Options with ${client1} and GroupAB and ${user02.first_name} ${user02.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY}
    Telephony Presence Status With Contactlist with ${client1} and GroupAB and Green

#Change User Telephony Status for userB from available to out of office
    Change User Telephony Status with ${client2} and out_of_office

# Verify the telephony presence status
    Select Group Options with ${client1} and GroupAB and ${user02.first_name} ${user02.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY}
    Telephony Presence Status With Contactlist with ${client1} and GroupAB and red

#Change User Telephony Status for userB to in_a_meeting
    Change User Telephony Status with ${client2} and in_a_meeting

# $client1 command action telephony_presence_status_with_contactlist groupName=groupA verifycolor=yellow component_id=$componentId
    Select Group Options with ${client1} and GroupAB and ${user02.first_name} ${user02.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY}
    Telephony Presence Status With Contactlist with ${client1} and GroupAB and yellow

#Change User Telephony Status for userB to available
    Change User Telephony Status with ${client2} and available
    Change User Telephony Status with ${client1} and available