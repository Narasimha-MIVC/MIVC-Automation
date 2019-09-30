*** Settings ***
Documentation     Ad-hoc-Screenshare-Feature
...               Indresh Tripathi
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
Ad-hoc-Screenshare-Feature
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision

    Close Presenter with ${client1}
    
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}

    # UserA sends IM to UserB
    Click Filter Message with ${client1} and Messages    
    Send IM with ${client1} and Hello02    

    # UserB verifies the IM sent by UserA
    Invoke Dashboard Tab with ${client2} and messages 
    Received IMB with ${client2} and true and Hello02

    # UserB sends IM to UserA
    Send IM with ${client2} and Hello01    

    # UserA verifies the IM sent by UserA
    Received IMA with ${client2} and true and Hello01

# Full Screen Share
    # UserA clicks on share and Share full Screen buttons to starts full screen share
    Share Endo Client Screen with ${client1} and no and share_full_screen and organizer
    Sleep    6s
    
    # UserB again clicks on view screen share
    Accept Screen Share with ${client2} and after_play and accept_share_popup

    # UserB verifies that sharing is in progress
    Verify Screen Share with ${client2} and sharing_in_progress

    # UserA stops sharing
    Play Pause Close Presenter with ${client1} and pause
    Play Pause Close Presenter with ${client1} and close

    # Making sure the presenter is closed
    Close Presenter with ${client1}
    
    #Close second panel & search panel in User A
    Close Panel with ${client1} and third

    # UserB minimizes share screen
    Close Panel with ${client2} and screen_share
    Close Panel with ${client2} and third

    #Create a new group & add the 3 users to the group,Verify the users in the group
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and group_203687 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Select Group Options with ${client1} and group_203687 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${EMPTY} and ${EMPTY} and groupChat

    #Send an IM to the group by USERA
    Send IM with ${client1} and hello

    #verify IM is received by all users in the group(USERB,USERC)
    Invoke Dashboard Tab with ${client2} and messages
    Received IMB with ${client2} and true and hello
    Invoke Dashboard Tab with ${client3} and messages
    Received IMB with ${client3} and true and hello

    # UserA clicks on share and Share full Screen buttons to starts full screen share
    Share Endo Client Screen with ${client1} and no and share_full_screen and organizer
    Sleep    5s
    # UserB accepts screen share
    Accept Screen Share with ${client2} and after_play and accept_share_popup
    Sleep    3s

    # UserB verifies that sharing is in progress
    Verify Screen Share with ${client2} and sharing_in_progress

    # UserC accepts screen share
    Accept Screen Share with ${client3} and after_play and accept_share_popup
    Sleep    3s

    # UserC verifies that sharing is in progress
    Verify Screen Share with ${client3} and sharing_in_progress

    # UserA stops sharing
    Play Pause Close Presenter with ${client1} and pause
    Play Pause Close Presenter with ${client1} and close
    Close Presenter with ${client1}