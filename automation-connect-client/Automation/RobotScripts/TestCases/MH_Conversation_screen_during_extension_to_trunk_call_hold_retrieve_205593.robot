*** Settings ***
Documentation     MH_Conversation_screen_during_extension_to_trunk_call_hold_retrieve
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port2}          WITH NAME      client2 

Test Timeout        6 minutes   
Test Teardown       Run Keywords    call method      ${client1}      close_application        AND      call method      ${client2}      close_application    

*** Variables ***
# Moved to Test Variables file
 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1}    ${client2}     

    
*** Test cases ***
MH_Conversation_screen_during_extension_to_trunk_call_hold_retrieve    
    ${client1}=  Get library instance      client1   
    ${client2}=  Get library instance      client2    
    
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   ${client2}  
    
    # Login to Clients   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    Login with ${client2} and ${user03.client_id} and ${user03.client_password} and ${user03.server}
  
    End Voicemail Call with ${client1}
    End Voicemail Call with ${client2}
    
    #UserA opens contact card of UserB
    Search Contact Using DID with ${client1} and ${user03.sip_trunk_did} 
    
    # UserA checks details of UserB
    Check User Detail Attribute with ${client1} and call and positive
    Check User Detail Attribute with ${client1} and min and positive
    
    # UserA places a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    
    # UserB verifies that incoming call notification in present
    Check Incoming Call with ${client2}
    
    # UserB receives call
    Place End Call with ${client2} and recv and ${EMPTY}   
    
    # UserA puts the call to UserB on hold
    Place End Call with ${client1} and hold and ${EMPTY}
    Verify Hold Unhold In Third Panel with ${client1} and timer_onhold_call     
    Verify Hold Unhold In Third Panel with ${client1} and put_on_hold     
    Verify Hold Unhold In Third Panel with ${client1} and resume     
    
    # UserA clicks on Retrieve button
    Place End Call with ${client1} and unHold and ${EMPTY}
    Verify Hold Unhold In Third Panel with ${client1} and timer_normal_call     
    Verify Hold Unhold In Third Panel with ${client1} and hold  

    # UserA ends the call to UserB    
    Place End Call with ${client1} and end and ${EMPTY}
    Sleep     1s
    Check User Detail Attribute with ${client1} and endCall and negative
   
    
    
    
    
   