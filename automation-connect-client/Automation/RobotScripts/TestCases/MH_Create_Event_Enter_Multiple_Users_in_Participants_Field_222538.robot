*** Settings ***
Documentation     MH_Create_Event_Enter_Multiple_Users_in_Participants_Field
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Test Timeout        4 minutes
Test Teardown       call method      ${client1}      close_browser       

*** Variables ***
# Moved to Test Variables file
 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1}   

    
*** Test cases ***
MH_Create_Event_Enter_Multiple_Users_in_Participants_Field  
    ${client1}=  Get library instance      client1     
    
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}     
    Sleep     2s
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  2
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    
    # UserA opens Events tab
    Invoke Dashboard Tab with ${client1} and event 
    Open New Event with ${client1}
    
    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and event786 and 1
    Sleep       2s
    
    # Select meeting type as Presentation
    Events Select Meeting Type with ${client1} and custom
    
    # Verify Capitalization case for Organizers, Presenters and Participants
    Verifying Event Details with ${client1} and event and Organizers
    Verifying Event Details with ${client1} and event and Presenters
    Verifying Event Details with ${client1} and event and Participants
    
    # Add multiple organizers
    Events Meeting Type Add User with ${client1} and organizers and ${user02.first_name} ${user02.last_name}
        
    # Add multiple participants
    Events Meeting Type Add User with ${client1} and participants and ${user03.first_name} ${user03.last_name}
    Events Meeting Type Add User with ${client1} and participants and ${user05.first_name} ${user05.last_name}
        
    # Add multiple presenters
    Events Meeting Type Add User with ${client1} and presenters and ${user04.first_name} ${user04.last_name}
        
    #UserA Creates Event
    Events Create Invite with ${client1}    
    Sleep     8s
    
    # Delete Event with name event_266329           
    Open Event Info with ${client1} and event786 and ${EMPTY}
    Cancel Event with ${client1}
    #Closes the Manhattan Client
    # Close Application with ${client1}
    
    