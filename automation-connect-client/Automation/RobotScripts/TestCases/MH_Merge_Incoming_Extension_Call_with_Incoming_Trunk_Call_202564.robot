*** Settings ***
Documentation     MH_Merge_Incoming_Extension_Call_with_Incoming_Trunk_Call
...               Bhupendra Parihar
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3
Test Timeout        4 minutes  
Test Teardown       Run Keywords    call method      ${client1}      close_browser       AND      call method      ${client2}      close_browser        AND      call method      ${client3}      close_browser     

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}         ${client2}           ${client3}  
   

*** Test cases ***
MH_Merge_Incoming_Extension_Call_with_Incoming_Trunk_Call
    ${client1}=  Get library instance      client1   
    ${client2}=  Get library instance      client2
    ${client3}=  Get library instance      client3
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

    # Login to Client A and B
	Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    End Voicemail Call with ${client1}  
    Login with ${client2} and ${user02.client_id} and ${user02.client_password} and ${user02.server}
    End Voicemail Call with ${client2}  
    # Login to Client C  (External User)
	Login with ${client3} and ${ExtUser01.client_id} and ${ExtUser01.client_password} and ${ExtUser01.server}
    End Voicemail Call with ${client3}  
    
    # UserB opens cantact card of UserA to place call
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}

    Check User Detail Attribute with ${client1} and info and positive
	Check User Detail Attribute with ${client1} and call and positive
	Check User Detail Attribute with ${client1} and min and positive
   
    # Place call from UserB to UserA
    Call Control with ${client1} and start and ${EMPTY} and ${EMPTY}
    

    # UserB verifies incoming call options
    Check Incoming Call with ${client2}
	# Answer call
	Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}
    
    # UserC opens cantact card of UserA
    Search People Extension with ${client3} and ${user02.sip_trunk_did}
    
    # UserC places a call to UserA
    Call Control with ${client3} and start and ${EMPTY} and ${EMPTY}
    

    # UserA verifies incoming call
    Check Incoming Call with ${client2}
	# Answer call
	Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}

    # UserA merges the calls
    Click Merge Call with ${client2} and Merge_hold and yes 
    Sleep     3s
    # UserA verifies that UserB and UserC are in call
    Verify Users In A Dashboard In Call with ${client2} and two_users and ${user01.first_name} ${user01.last_name} and ${ExtUser01.sip_trunk_did}

    # UserA places the call on hold
    # Call Control with ${client2} and hold and ${EMPTY} and ${EMPTY}

    # UserA retrieves the call
    Call Control with ${client2} and unHold and ${EMPTY} and ${EMPTY}
    Sleep     2s
    # UserA drops UserB out of the call
    Verify ConferenceCall Users Ends Call with ${client2} and ${user01.first_name} ${user01.last_name} and end_call
    
    # Verifies that UserB is droped from the call
    Verify No Ongoing Call with ${client1}

    # UserA ends the call
    Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}
    
    # UserA opens Recent panel
    Invoke Dashboard Tab with ${client2} and recent
    
    # Verifies call details
    Check First Recent Call Type with ${client2} and conference
            