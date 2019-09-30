*** Settings ***
Documentation     MH_Group_Options_in_Third_Panel_Start_Group_Chat_All_Members_with_IM_Address
...               Aakash
...               Comments:
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
  

*** Test cases ***
MH_Group_Options_in_Third_Panel_Start_Group_Chat_All_Members_with_IM_Address
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision     
    
    # open people tab
    Invoke Dashboard Tab with ${client1} and people
    
    # Create new group
    Create New Group with ${client1} and group_test1 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    
    #Click on the group & start an IM Conference
    Select Group Options with ${client1} and group_test1 and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and groupChat
    
    #Send an IM to the group from userA
    Send IM with ${client1} and hello1

    #Check badge count on messages tab in dashboard
    Check Badge Count with ${client2} and messages
    Check Badge Count with ${client3} and messages
    
    #Open messages Tab
    Invoke Dashboard Tab with ${client2} and messages
    Invoke Dashboard Tab with ${client3} and messages
   
    #Verify IMs sent by User A
    Received IMB with ${client2} and true and hello1
    Received IMB with ${client3} and true and hello1
    
    #Send an IM to the group from userB
    Send IM with ${client2} and helloman
    
    #Verify IMs sent by User B
    Click Filter Message with ${client1} and messages
    Received IMA with ${client1} and true and helloman
    Received IMA with ${client3} and true and helloman
    
    #Send an IM to the group from User C
    Send IM with ${client3} and hello2    
    
    #Verify IMs sent by User C
    Received IMA with ${client2} and true and hello2
    Received IMA with ${client2} and true and hello2
    
    
    
	
	
	
	