*** Settings ***
Documentation     Events-Exo-Share
...               Indresh Tripathi
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py    ${port1}    WITH NAME    client1
 
Test Timeout      15 minutes
Test Teardown     Run Keywords    call method    ${client1}    close_browser    AND    call method    ${browser1}    close_browser

*** Variables ***
# Moved to Test Variables file
 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1} 

Keyword 2
    [Arguments]       ${client1}    
    
    Invoke Dashboard Tab with ${client1} and event
    # UserA clicks on new event button
    Open New Event with ${client1}

    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and auto_join and 1
    Sleep    1s

    # UserA adds UserB as participant
    # Events Meeting Type Add User with ${client1} and presenters and ${user07.first_name} ${user07.last_name}
    Events Meeting Type Add User with ${client1} and presenters and ${user03.first_name} ${user03.last_name}

    Events Change Meeting Settings with ${client1} and show
    Configure Meeting Settings with ${client1} and dial_out_to_participants and automatic    
    
    # UserA clicks on create button in client
    Events Create Invite with ${client1}
    Sleep    8s

    # UserA clicks on Send button in outlook to create event
    #Send Meeting Request Outlook with ${client1} and send_meeting_invite and auto_join    
        
    #${participant_code}=  Get Event Participant Code with ${client1} and auto_join
    
*** Test cases ***
Events-Exo-Share
    ${client1}=  Get library instance    client1
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}    
    Sleep     2s
    # Login to Clients    
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    
    # Checks that if event exists otherwise create it
    ${eventFound}=   Get Event with ${client1} and auto_join 
    
    Run Keyword If  "${eventFound}" == "no"  Keyword 2   ${client1}   
    
    # Test audio through Call Me feature through Endo for entering both internal extension and External Number
    # Call-Me for internal extension from Endo client
    Open Event Info with ${client1} and auto_join and yes
    
    # Copy event URL
    ${url}=   Get Url with ${client1}
    
    # UserA joins event
    Join Endo Conference with ${client1} and web_chat_mode and ${EMPTY} and ${EMPTY}
    
    # Launch browser for UserB
    Import Library    ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py    ${port5}    WITH NAME    browser1
    ${browser1}=  Get library instance    browser1
    
    # UserB join event
    Launch Url with ${browser1} and ${url}
    Join Exo Event with ${browser1} and user1
    
    #Exo ScreenShare
    # UserB shares full screen
    Share Exo Client Screen with ${browser1} and share_full_screen and chrome and auto_join  
    Sleep      6s
    
    # UserA verifies that sharing is in progress
    Verify Screen Share with ${client1} and sharing_in_progress
    
    # UserB stops sharing
    Play Pause Close Presenter with ${browser1} and pause
    Sleep    2s
    Play Pause Close Presenter with ${browser1} and close

    # Making sure the presenter is closed
    Close Presenter with ${client1}
    Sleep    3s

    # UserB shares Area
    Share Exo Client Screen with ${browser1} and share_area and chrome and auto_join  
    Sleep      6s
    
    # UserA verifies that sharing is in progress
    Verify Screen Share with ${client1} and sharing_in_progress
    
    # UserB stops sharing
    Play Pause Close Presenter with ${browser1} and pause
    Sleep    2s
    Play Pause Close Presenter with ${browser1} and close

    # Making sure the presenter is closed
    Close Presenter with ${client1}
    Sleep    3s

    # UserB shares window
    Share Exo Client Screen with ${browser1} and share_window and chrome and auto_join  
    Sleep      6s
    
    # UserA verifies that sharing is in progress
    Verify Screen Share with ${client1} and sharing_in_progress
    
    # UserB stops sharing
    Play Pause Close Presenter with ${browser1} and pause
    Sleep    2s
    Play Pause Close Presenter with ${browser1} and close

    # Making sure the presenter is closed
    Close Presenter with ${client1}
    
    # Delete Event with name event_266329
    Invoke Dashboard Tab with ${client1} and event        
    Open Event Info with ${client1} and auto_join and ${EMPTY}
    Cancel Event with ${client1}
    
    
    
    
    
    
   