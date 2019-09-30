*** Settings ***
Documentation     MH_Create-New-Event-No-Exchange-and-no-Outlook-Co-Host-Can-Update
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
MH_Create-New-Event-No-Exchange-and-no-Outlook-Co-Host-Can-Update       
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision    
    
    # UserA opens Event tab
    Invoke Dashboard Tab with ${client1} and event
    Verify Events Page with ${client1}
    Verify Events Avail Upcoming with ${client1} and event_avail
    
    # UserA clicks on new event button
    Open New Event with ${client1}
    
    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and event1 and 20
    Events Select Meeting Type with ${client1} and custom
    
    # Adds UserB as an organizer
    Events Meeting Type Add User with ${client1} and organizers and ${user02.first_name} ${user02.last_name}
    
    #UserA clicks on create button to create event
    Events Create Invite with ${client1}
    Sleep     3s
    
    # Verify that third panel is closed
    Verify Events Avail Upcoming with ${client1} and event_third
    
    # UserB opens event tab
    Invoke Dashboard Tab with ${client2} and event
    Sleep     2s
    # Verify that event is listed under Upcoming tab and open it
    Open Event Info with ${client2} and event1 and yes
    
    # UserB edits meetimg details
    Chk Event Creation User with ${client2}
    Events Add Meeting Details with ${client2} and test and 2    
    Events Add Meeting Details with ${client2} and auto_update and 1
    Events Create Invite with ${client2}
    Sleep     10s
    
    # Verify that event name has been changed
    #Open Event Info with ${client2} and test and ${EMPTY}
    
    #USERA clicks on Event Tab
	#Invoke Dashboard Tab with ${client1} and event   
    Open Event Info with ${client1} and auto_update and yes       
    Cancel Event with ${client1}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   