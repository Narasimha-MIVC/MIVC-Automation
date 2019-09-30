*** Settings ***
Documentation     MH_Blind_Transfer_Trunk_to_Trunk
...               Bhupendra Parihar
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3 
Test Timeout        4 minutes   
Test Teardown       Run Keywords    call method      ${client1}      close_browser         AND      call method      ${client2}      close_browser      AND      call method      ${client3}      close_browser

*** Variables ***
# Moved to Test Variables file
 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1}    ${client2}     ${client3} 

    
*** Test cases ***
MH_Blind_Transfer_Trunk_to_Trunk
    ${client1}=  Get library instance      client1   
    ${client2}=  Get library instance      client2
    ${client3}=  Get library instance      client3
    
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   ${client2}   ${client3}   
             
    # Login to Client A and C (External Users)
    Login with ${client1} and ${ExtUser01.client_id} and ${ExtUser01.client_password} and ${ExtUser01.server}
    End Voicemail Call with ${client1}
    Login with ${client3} and ${ExtUser02.client_id} and ${ExtUser02.client_password} and ${ExtUser02.server}
    End Voicemail Call with ${client3}
    # Login to Client B
    Login with ${client2} and ${user02.client_id} and ${user02.client_password} and ${user02.server}
    End Voicemail Call with ${client2}
    
    # Search extension and open third panel
    #Search People Extension No Exception with ${client1} and ${user03.sip_trunk_did}
    Search People Extension with ${client1} and ${user02.sip_trunk_did}

    Check User Detail Attribute with ${client1} and sip_info and positive
    Check User Detail Attribute with ${client1} and call and positive
    Check User Detail Attribute with ${client1} and min and positive
    
    # Sleep      2s
    # UserA places a call to UserB
    Call Control with ${client1} and start and ${EMPTY} and ${EMPTY}
    # Sleep      2s
    
    # UserB verifies incoming call options
    Check Incoming Call with ${client2}

    # Answer call
    Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}

    # UserB verifies that call attributes are present
    Check User Detail Attribute with ${client2} and sip_info and positive
    Check User Detail Attribute with ${client2} and timer and positive
    Check User Detail Attribute with ${client2} and endCall and positive
    Check User Detail Attribute with ${client2} and holdCall and positive
    Check User Detail Attribute with ${client2} and mute and positive
    Check User Detail Attribute with ${client2} and video and positive
    Check User Detail Attribute with ${client2} and conf and positive
    Check User Detail Attribute with ${client2} and transfer and positive
    
    # UserB transfers the call to UserC
    Call Control with ${client2} and did_to_did_trans and ${EMPTY} and ${ExtUser02.sip_trunk_did}
    # # $client1 command action place_end_call click=yes option=did_to_did_trans did=[::cfgutil::getGlobalVariable SETUP1_SITE1_DID_NUMBER2]\
    # # component_id=$componentIdUserB
    
    Sleep     1s
    # UserC verifies incoming call options
    Check Incoming Call with ${client3}
    
    # UserC answers call
    Call Control with ${client3} and recv and ${EMPTY} and ${EMPTY}         
    #Sleep     2s

    # Verifies that UserB is droped from the call
    Verify No Ongoing Call with ${client2}

    # UserA ends the call
    Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}