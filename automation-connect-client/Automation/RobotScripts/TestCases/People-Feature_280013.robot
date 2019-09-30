*** Settings ***
Documentation     People-Feature
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
People-Feature
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    # Double clicking on contact to make a call
    Call Contact By Double Click with ${client1} and ${user02.first_name} ${user02.last_name}
    
    #UserB receives the call
    Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}
    Sleep    2s

    # UserA ends the call
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}

    # Create a new group & add users to the group,Verify the users in the group
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and Group1 and save and ${user02.first_name} ${user02.last_name} and ${EMPTY}

    #verifies the Group added with the members
    Select Group Options with ${client1} and Group1 and ${user02.first_name} ${user02.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY}   
    
    #Clicks on the 1st user in the group
    Open Contact Card with ${client1} and groups and ${user02.first_name} ${user02.last_name}
        
    # Verifies that contact card is opened
    Verify Contact Card Status with ${client1} and present and ${user02.first_name} ${user02.last_name} and yes
    
    #Close 3rd panel
    Close Panel with ${client1} and third
    
    # edit a group & add user to existing group
    Edit Group with ${client1} and Group1 and ${user02.first_name} ${user02.last_name}
    Sleep    2s
    Modify Group Add Member with ${client1} and Group1 and ${user03.first_name} ${user03.last_name} and ${user04.first_name} ${user04.last_name} and save and ${EMPTY} and ${EMPTY}       
    Sleep    2s

    #Send IM to group
    Select Group Options with ${client1} and Group1 and ${user03.first_name} ${user03.last_name} and ${user04.first_name} ${user04.last_name} and ${EMPTY} and ${EMPTY} and groupChat
    #Send an IM to the group by USERA
    Send IM with ${client1} and hello
    
    # verify IM is received by all users in the group(USERB,USERC,USERD)
    Invoke Dashboard Tab with ${client2} and messages
    Received IMB with ${client2} and true and hello
    Invoke Dashboard Tab with ${client3} and messages
    Received IMB with ${client3} and true and hello
    
    #Send IM from all users in the group & verify IM can be sent & received by group members
    Send IM with ${client2} and hello2
    Received IMA with ${client3} and true and hello2
    Click Filter Message with ${client1} and messages
    Received IMA with ${client1} and true and hello2
    
    #Send IM with ${client3} and hello3
    Send IM with ${client3} and hello3
    Received IMA with ${client2} and true and hello3
    Received IMA with ${client1} and true and hello3
    
    #Close second panel
    Close Panel with ${client1} and third
    
    # Opens people tab
    Invoke Dashboard Tab with ${client1} and people
                
    #Click pinned
    Click Pin with ${client1}
    
    #Open Own user details
    Open Own User Detail with ${client1}
    
    # #Close second panel
    Close Panel with ${client1} and second
    
    #Check people tab is still opened
    Verify Second Panel with ${client1} and people and present
            
    #Log out and login again
    Logout with ${client1} and 0
    Sleep    3s
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    Invoke Dashboard Tab with ${client1} and people
    
    #Check pinned is present even after restart
    Check Pinned with ${client1}
    
    #Click on pinned to make it unpinned
    Click Pinned with ${client1}
    
    # Opens the group & selects the option send groupvoicemail
    Select Group Options with ${client1} and Group1 and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and groupVM
    #Select Group Options with ${client1} and Group1 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${user04.first_name} ${user04.last_name} and ${EMPTY} and groupVM
    
    #Send groupvoicemail
    Send Group Vm with ${client1} and phone and send
    
    #Check voicemail is received in UserB & userC
    Check Badge Count with ${client2} and voicemail
    Check Badge Count with ${client3} and voicemail
    
    # Opens the group & selects the option "Schedule Meeting with Group"
    Select Group Options with ${client1} and Group1 and ${EMPTY} and ${EMPTY} and ${EMPTY} and ${EMPTY} and meetingWithGroup
    # Select Group Options with ${client1} and Group1 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${user04.first_name} ${user04.last_name} and ${EMPTY} and meetingWithGroup
    
    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and test_event and 1
    
    # UserA clicks on create button in cleint
    Events Create Invite with ${client1}			
    Sleep      7s
    # UserB verifies that event is listed in upcoming tab
    Invoke Dashboard Tab Event with ${client2} and event and ${user02.client_email} and ${user02.client_password}
    Open Event Info with ${client2} and test_event and ${EMPTY}
    # UserC verifies that event is listed in upcoming tab
    Invoke Dashboard Tab Event with ${client3} and event and ${user03.client_email} and ${user03.client_password}
    Open Event Info with ${client3} and test_event and ${EMPTY}
 