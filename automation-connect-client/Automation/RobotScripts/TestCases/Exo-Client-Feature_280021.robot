*** Settings ***
Documentation     Exo-Client-Feature
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1 
 
Test Timeout        15 minutes   

Test Teardown       Run Keywords    call method      ${client1}      close_browser        AND     call method      ${browser1}      close_browser    AND     call method      ${browser2}      close_browser

*** Variables ***
# Moved to Test Variables file
 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1}    ${client2}     ${client3} 

Keyword 2
    [Arguments]       ${client1}    
    
    Invoke Dashboard Tab with ${client1} and event
    # UserA clicks on new event button
    Open New Event with ${client1}

    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and join_by_press_one and 1
    Sleep    1s

    # UserA adds UserB as participant
    Events Meeting Type Add User with ${client1} and presenters and ${user02.first_name} ${user02.last_name}
    #Events Meeting Type Add User with ${client1} and presenters and ${user03.first_name} ${user03.last_name}

    Events Change Meeting Settings with ${client1} and show
    Configure Meeting Settings with ${client1} and dial_out_to_participants and automatic    
    
    # UserA clicks on create button in cleint
    Events Create Invite with ${client1}
    Sleep    8s

    # UserA clicks on Send button in outlook to create event
    #Send Meeting Request Outlook with ${client1} and send_meeting_invite and join_by_press_one    
        
    #${participant_code}=  Get Event Participant Code with ${client1} and join_by_press_one
    
*** Test cases ***
Exo-Client-Feature   
    ${client1}=  Get library instance      client1     
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}    
    Sleep     2s
    # Login to Clients    
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    End Voicemail Call with ${client1}
    
    # GroupChat Exo
    # UserA opens Events tab
    #Invoke Dashboard Tab with ${client1} and event
    
    # Checks that if event exists otherwise create it
    ${eventFound}=   Get Event with ${client1} and join_by_press_one 
    
    Run Keyword If  "${eventFound}" == "no"  Keyword 2   ${client1}   
    
    # Test audio through Call Me feature through Endo for entering both internal extension and External Number
    # Call-Me for internal extension from Endo client
    Open Event Info with ${client1} and join_by_press_one and yes
    
    # Copy event URL
    ${url}=   Get Url with ${client1}
    
    # UserA joins event
    Join Endo Conference with ${client1} and web_chat_mode and ${EMPTY} and ${EMPTY}
    
    # Launch browser for UserB
    Import Library        ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py      ${port5}          WITH NAME      browser1
    ${browser1}=  Get library instance      browser1
    
    # Launch browser for UserC
    Import Library        ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py      ${port6}          WITH NAME      browser2
    ${browser2}=  Get library instance      browser2
    
    Launch Url with ${browser1} and ${url}
    # UserB join event
    Join Exo Event with ${browser1} and user1
    
    Launch Url with ${browser2} and ${url}
    # UserC join event    
    Join Exo Event with ${browser2} and user2
    
    # UserB send IM to group
    Click On Users For Chat with ${browser1} and group_chat
    Sleep    2s
    Send Im Exo with ${browser1} and group_B
    Sleep    2s
    # UserA verifies that IM is received
    Received IMA with ${client1} and true and group_B
    
    # UserC verifies that IM is received
    Click On Users For Chat with ${browser2} and group_chat
    Verify Exo IM with ${browser2} and yes and group_B
    
    # UserC send IM to group
    Send Im Exo with ${browser2} and group_C
    Sleep    2s
    # UserA verifies that IM is received
    Received IMA with ${client1} and true and group_C
    
    # UserB verifies that IM is received
    Verify Exo IM with ${browser1} and yes and group_C
    Sleep     1s
    
    #Exo ScreenShare
    # UserB shares full screen
    Share Exo Client Screen with ${browser1} and share_full_screen and chrome and join_by_press_one  
    Sleep      6s
    
    # UserC verifies that sharing is in progress
    Verify Screen Share with ${browser2} and sharing_in_progress
    
    #Exo ScreenShare does not freeze
    # UserB send IM to group
    Send Im Exo with ${browser1} and not_freeze_B
    Sleep    2s
    # UserA verifies that IM is received
    Received IMA with ${client1} and true and not_freeze_B
    Click On Users For Chat with ${browser2} and group_chat
    
    # UserC verifies that IM is received
    Verify Exo IM with ${browser2} and yes and not_freeze_B
    
    # UserC verifies that sharing is in progress
    Verify Screen Share with ${browser2} and sharing_in_progress
    
    #Tab away &  verify sharing is in progress
    # UserC does tab away to a different screen
    # Tab Away with ${browser1}
    # Sleep      1s
    # Tab Away with ${browser1}                               

    # UserB send IM to group    
    Send Im Exo with ${browser1} and tab_B
    Sleep    2s
    # UserA verifies that IM is received
    Received IMA with ${client1} and true and tab_B
    
    # UserC verifies that IM is received
    Verify Exo IM with ${browser2} and yes and tab_B
    
    # UserC verifies that sharing is in progress
    Verify Screen Share with ${browser2} and sharing_in_progress
    
    # UserB stops sharing
    Play Pause Close Presenter with ${browser1} and pause
    Sleep     2s
    Play Pause Close Presenter with ${browser1} and close
    Sleep      5s
    
    # Delete Event with name event_266329
    Invoke Dashboard Tab with ${client1} and event        
    Open Event Info with ${client1} and join_by_press_one and ${EMPTY}
    Cancel Event with ${client1}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   