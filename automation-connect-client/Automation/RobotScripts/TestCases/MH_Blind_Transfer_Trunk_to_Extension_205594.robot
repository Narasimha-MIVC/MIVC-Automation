*** Settings ***
Documentation     MH_Blind_Transfer_Trunk_to_Extension
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
MH_Blind_Transfer_Trunk_to_Extension
    ${client1}=  Get library instance      client1   
    ${client2}=  Get library instance      client2
    ${client3}=  Get library instance      client3
    
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   ${client2}   ${client3}   
    

	# Login to Client B and C
	Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
	End Voicemail Call with ${client1}
    Login with ${client2} and ${user02.client_id} and ${user02.client_password} and ${user02.server}
    End Voicemail Call with ${client2}
    # Login to Client A  (External User)
	Login with ${client3} and ${ExtUser01.client_id} and ${ExtUser01.client_password} and ${ExtUser01.server}
	End Voicemail Call with ${client3}
    
	# Search extension and open third panel
	Search People Extension with ${client1} and ${ExtUser01.sip_trunk_did}

    # Place call from UserB to UserA
    Call Control with ${client1} and start and ${EMPTY} and ${EMPTY}
	
	# UserA verifies incoming call options
	Check Incoming Call with ${client3}
	# Answer call
	Call Control with ${client3} and recv and ${EMPTY} and ${EMPTY} 

    # UserB verifies that call attributes are present
	Check User Detail Attribute with ${client1} and sip_info and positive
	Check User Detail Attribute with ${client1} and timer and positive
	Check User Detail Attribute with ${client1} and endCall and positive
	Check User Detail Attribute with ${client1} and holdCall and positive
	Check User Detail Attribute with ${client1} and mute and positive
	Check User Detail Attribute with ${client1} and video and positive
	Check User Detail Attribute with ${client1} and conf and positive
	Check User Detail Attribute with ${client1} and transfer and positive
    
	# UserB transfers the call to UserC
	Call Control with ${client1} and trans and ${user02.first_name} ${user02.last_name} and ${EMPTY}

    Sleep    2s
    # UserC recieve the call
	Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}

	# UserA is end the call
	Call Control with ${client3} and end and ${EMPTY} and ${EMPTY}

    # UserC opens Recent->All
    Invoke Dashboard Tab with ${client2} and recent

    Verify Route Slip Third Panel with ${client2} and ${ExtUser01.sip_trunk_did}
    