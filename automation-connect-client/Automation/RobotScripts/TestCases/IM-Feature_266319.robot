*** Settings ***
Documentation     IM-Feature
...               Bhupendra Singh Parihar
...               Comments:

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
IM-Feature
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    # User1 opens contact card of User2
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}

    # User1 sends IM to User2
    Click Filter Message with ${client1} and Messages    
    #Sleep   2s
    Send IM with ${client1} and Hello02    
    #Sleep   1s

    # User2 verifies the IM sent by User1
    Invoke Dashboard Tab with ${client2} and messages 
    Received IMB with ${client2} and true and Hello02

    # User2 sends IM to User1
    Send IM with ${client2} and Hello01
    
    # User1 verifies the IM sent by User2
    Received IMA with ${client1} and true and Hello01
    #Sleep    2s

    #Create a new group & add the 3 users to the group,Verify the users in the group
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and Group1 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    # Create New Group with ${client1} and Group1 and save and ${user02.first_name} and ${user03.first_name}
    
    # Select group chat option
    Select Group Options with ${client1} and Group1 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${EMPTY} and ${EMPTY} and groupChat
     
    # Send an IM to the group by User1
    Send IM with ${client1} and Hello
    #Sleep     2s
    
    # verify IM is received by all users in the group(Use2,User3)
    Received IMB with ${client2} and true and Hello 
    Invoke Dashboard Tab with ${client3} and messages
    Received IMB with ${client3} and true and Hello
    
    # Send an IM to the group from User2
    Send IM with ${client2} and Hello01 
    
    #verify IM is received by all users in the group(User1,User3)
    Received IMA with ${client1} and true and Hello01
    Received IMA with ${client3} and true and Hello01
    
    #Send an IM to the group from USER3
    Send IM with ${client3} and Hello02
    
    # verify IM is received by all users in the group(USER1,USER2)
    Received IMA with ${client1} and true and Hello02
    Received IMA with ${client2} and true and Hello02