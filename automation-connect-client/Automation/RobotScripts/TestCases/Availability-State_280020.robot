*** Settings ***
Documentation     Availability-State
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
Availability-State
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # Create an event in outlook to verify that it loggels Client's state to in a meeting
    # Create Meeting Outlook with ${client1} and meeting_273023 and ${user01.client_email} and ${user02.client_email}

    # UserB sets its presence to 'Out of Office'
    Change User Telephony Status with ${client2} and out_of_office

    # UserA checks that UserB's status is changed to Out of Office
    Check Presence In Third Panel with ${client1} and ${user02.first_name} ${user02.last_name} and out_of_office

    # Close second panel search,third panel
    Close Panel with ${client1} and second_search
    Close Panel with ${client1} and third
    
    #Change User Telephony Status with ${client1} and in_a_meeting
    # wait for event to start
    #Check User Telephony Presence with ${client1} and in_a_meeting and yellow

    # UserA sets its presence back to 'available'
    #Change User Telephony Status with ${client1} and available
    Change User Telephony Status with ${client2} and available


