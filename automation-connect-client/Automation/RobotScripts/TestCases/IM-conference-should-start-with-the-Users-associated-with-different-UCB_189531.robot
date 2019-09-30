*** Settings ***
Documentation     IM-conference-should-start-with-the-Users-associated-with-different-UCB
...               HariPrakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        7 minutes
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
IM-conference-should-start-with-the-Users-associated-with-different-UCB
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
	
    Cleanup Groups with ${client1}
    Cleanup Groups with ${client1}
	
	#UserA creates a group
    Invoke Dashboard Tab with ${client1} and people
    
	#UserA Creates new group
	Create New GroupThreeMembers with ${client1} and group_2027632 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${user04.first_name} ${user04.last_name}
	
	#UserA Selects GroupChat 
	Select Group Options with ${client1} and group_2027632 and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and groupChat
	
    #USERA sends IM	
	Send IM with ${client1} and HelloB
	
	#UserB checks the Messages  badge count
	Check Badge Count with ${client2} and messages
	 
	#UserB opens messages tab
	Invoke Dashboard Tab with ${client2} and messages
	
	#UserC checks the messages count
	Check Badge Count with ${client3} and messages
	
	#USERC opens the message tab
	Invoke Dashboard Tab with ${client3} and messages

	#USERB verifies the message recieved by USERA
    Received IMB with ${client2} and true and HelloB
	
	#USERC verifies the message recieved by USERA
	Received IMB with ${client3} and true and HelloB
		
	#UserD checks the Messages  badge count
	Check Badge Count with ${client4} and messages
	 
	#UserD opens messages tab
	Invoke Dashboard Tab with ${client4} and messages
	
	#USERD verifies the message recieved by USERA
	Received IMB with ${client4} and true and HelloB
	
	#USERA sends the message to the Group IM
    Send IM with ${client1} and HelloAll
	
	#USERA sends the message to the Group IM
	Send IM with ${client1} and !@#$%^&*
	
	#USERA sends the message to the Group IM
	Send IM with ${client1} and "Hello"
	
	#USERA sends the message to the Group IM
	Send IM with ${client1} and The longest message ever
	
	#USERA sends the message to the Group IM
	Send IM with ${client1} and mitel@gmail.com
	
	#USERB sends the message to the Group IM
	Send IM with ${client2} and HelloAll
	
	#USERB sends the message to the Group IM
	Send IM with ${client2} and !@#$%^&*
	
	#USERB sends the message to the Group IM
	Send IM with ${client2} and "Hello"
	
	#USERB sends the message to the Group IM
	Send IM with ${client2} and The longest message ever
	
	#USERB sends the message to the Group IM
	Send IM with ${client2} and mitel@gmail.com
	
	#USERC sends the message to the Group IM
	Send IM with ${client3} and HelloAll
	
	#USERC sends the message to the Group IM
	Send IM with ${client3} and !@#$%^&*
	
	#USERC sends the message to the Group IM
	Send IM with ${client3} and "Hello"
	
	#USERC sends the message to the Group IM
	Send IM with ${client3} and The longest message ever
	
	#USERC sends the message to the Group IM
	Send IM with ${client3} and mitel@gmail.com
	
	#USERC sends the message to the Group IM
	Send IM with ${client3} and added USERD
	
	#USERD sends the message to the Group IM
	Send IM with ${client4} and Yes This is USERD
	
	#USERD sends the message to the Group IM
	Send IM with ${client4} and HelloAll
	
	#USERD sends the message to the Group IM
	Send IM with ${client4} and !@#$%^&*
	
	#USERD sends the message to the Group IM
	Send IM with ${client4} and "Hello"
	
	#USERD sends the message to the Group IM
	Send IM with ${client4} and The longest message ever
	
	#USERD sends the message to the Group IM
	Send IM with ${client4} and mitel@gmail.com
	
	#UserA opens people tab
	Invoke Dashboard Tab with ${client1} and people
	
	#UserA Deletes the group group_2027632
	Delete Group with ${client1} and group_2027632 and yes