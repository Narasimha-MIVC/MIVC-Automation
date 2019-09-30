*** Settings ***
Documentation     Conversation-Presence-Change-CHS-from-Client
...               Aakash
...               Comments:
Default Tags        tc-Suite
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        7 minutes
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
Conversation-Presence-Change-CHS-from-Client    
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision     
         
    # UserA sets its presence to 'Available'
    Change User Telephony Status with ${client1} and available
    
    # UserB sets its presence to 'In a Meeting'
    Change User Telephony Status with ${client2} and in_a_meeting
    
    # UserC sets its presence to 'Available'
    Change User Telephony Status with ${client3} and available
    
    Cleanup Groups with ${client1}
    Cleanup Groups with ${client1}
    
    # UserA_192689 verifies that UserB and Userc are not part of any contact group
    Invoke Dashboard Tab with ${client1} and people
    
    #UserA Creates new group
	Create New Group with ${client1} and group_2027632 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    
    Search All Groups Contact Member with ${client1} and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and negative
    
    # UserA verifies that UserB and UserC are not Favorites 
    Check Favourite Symbol From Search ${client1} and ${user02.first_name}**${user02.last_name}
    Close Panel with ${client1} and second_search
    Check Favourite Symbol From Search ${client1} and ${user03.first_name}**${user03.last_name}
    Close Panel with ${client1} and second_search
    
    # UserA opens third panel for sending IM to UserC
    Search People Extension with ${client1} and ${user03.first_name} ${user03.last_name}
    Click Filter Message with ${client1} and messages
    Send IM with ${client1} and helloC
    
    # UserC checks for IM notification
    Check Badge Count with ${client3} and messages

    Close Panel with ${client1} and second_search
    # UserA checks that UserC's status is Available
    Check Presence In Third Panel with ${client1} and ${user03.first_name} ${user03.last_name} and Available
    
    # UserA opens third panel for sending IM to UserB
    Close Panel with ${client1} and second_search
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    
    Send IM with ${client1} and helloB
    
    # UserB checks for IM notification
    Check Badge Count with ${client2} and messages
    
    Close Panel with ${client1} and second_search
    # UserA checks that UserB's status is In a Meeting
    Check Presence In Third Panel with ${client1} and ${user02.first_name} ${user02.last_name} and In_a_Meeting
    Close Panel with ${client1} and second_search
    
    # UserB sets its presence to 'Out of Office'
    Change User Telephony Status with ${client2} and out_of_office
      
    # UserA checks that UserB's status is changed to Out of Office
    Check Presence In Third Panel with ${client1} and ${user02.first_name} ${user02.last_name} and Out_of_Office
    Change User Telephony Status with ${client2} and available
        
   
    #UserA opens people tab
	Invoke Dashboard Tab with ${client1} and people
    #UserA Deletes the group group_2027632
	Delete Group with ${client1} and group_2027632 and yes
