*** Settings ***
Documentation     MH_IM_moved_to_history_when_user_is_offline
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot

Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2
Test Timeout        4 minutes
Test Teardown       Run Keywords    call method      ${client1}      close_browser      AND        call method      ${client2}      close_browser     

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1} 
    
    
*** Test cases ***
MH_IM_moved_to_history_when_user_is_offline     
    ${client2}=  Get library instance      client2     
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   
    Sleep     2s
    #Login to the Manhattan Client from ST_Users/MT_Users     
    Login with ${client2} and ${user02.client_id} and ${user02.client_password} and ${user02.server}
    End Voicemail Call with ${client2}       
    
    # UserA opens contact card of UserB
    Search People Extension with ${client2} and ${user04.first_name} ${user04.last_name}
    
    # UserA sends IM to UserB
    Click Filter Message with ${client2} and Messages 
    Send IM with ${client2} and Hello02
    
    # On sending 1st IM, a new conversation is created in dashboard and hence it fails to send second IM.
    Sleep      1s
    Send IM with ${client2} and Hello
    Sleep      5s
    
    # Launch Manhattan Client for UserA
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1
    ${client1}=  Get library instance      client1 
    
    # Login to Manhattan Client 
    Login with ${client1} and ${user04.client_id} and ${user04.client_password} and ${user04.server}        
    Sleep       5s
    
    #Verify recent counter badge
    Check Badge Count with ${client1} and messages
    
    # UserB verifies the IM sent by UserA
    Invoke Dashboard Tab with ${client1} and messages
    Received IMB with ${client1} and true and Hello
    
    
    
   