*** Settings ***
Documentation     MH_connected_call_record
...               Bhupendra Parihar
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
Test Timeout        4 minutes   
Test Teardown       Run Keywords    call method      ${client1}      close_browser       AND      call method      ${client2}      close_browser

*** Variables ***
# Moved to Test Variables file
 
*** Keyword ***    
Keyword 1
    [Arguments]       ${client1}    ${client2}

Keyword2
	# ${count}=  Set Variable    1

    
*** Test cases ***
MH_connected_call_record 
    ${client1}=  Get library instance      client1   
    ${client2}=  Get library instance      client2

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

    # Login to Client A
	Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    End Voicemail Call with ${client1}

    # Login to Client B  (External User)
	Login with ${client2} and ${ExtUser01.client_id} and ${ExtUser01.client_password} and ${ExtUser01.server}
    End Voicemail Call with ${client2}

    # Search extension and open third panel
	Search People Extension with ${client1} and ${ExtUser01.sip_trunk_did}
			
	Check User Detail Attribute with ${client1} and sip_info and positive
	Check User Detail Attribute with ${client1} and call and positive
	Check User Detail Attribute with ${client1} and min and positive

	# Place call from UserA to UserB
	Call Control with ${client1} and start and ${EMPTY} and ${EMPTY}

    # UserB verifies incoming call options
	Check Incoming Call with ${client2}
	# Answer call
	Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}

	# check for badge count on client1
	# ${count}=    Get Badge Count with ${client1} and Voicemails
	# Run Keyword If "${count}" == "None" Keyword2

	# UserA starts recording
	Third Panel Call Record with ${client1} and start_recording
	Sleep   3s
	# UserA stops recording
	Third Panel Call Record with ${client1} and stop_recording

	# calculating incremented batch count
	# ${new_count}=    Evaluate ${count} + 1

	# UserA verifes voicemail notification
	Check Badge Count with ${client1} and voicemail
	# Verify Recent Counter Badge with ${client1} and ${new_count} and voicemails

	# End Call
	Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}

	# UserA opens dashboard voicemail notification
	Invoke Dashboard Tab with ${client1} and voicemail
	Select Tab with ${client1} and all and voicemail

	# UserA opens voicemail and plays that
	Play Unread Voicemails Via Phone with ${client1}