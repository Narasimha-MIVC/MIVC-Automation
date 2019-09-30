*** Settings ***
Documentation     MH_Consult_Transfer_Extension_to_Trunk
...               Bhupendra Parihar
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3
Test Timeout        5 minutes  
Test Teardown       Run Keywords    call method      ${client1}      close_browser       AND      call method      ${client2}      close_browser        AND      call method      ${client3}      close_browser     

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}         ${client2}           ${client3}  
   

*** Test cases ***
MH_Consult_Transfer_Extension_to_Trunk
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
    
    # Select the checkbox for not opening the outlook for contact creation for UserA
    Open Outlook Tab with ${client1}
    Configure Outlook Tab with ${client1} and contacts and check

    # UserA creates a contact
    Create New Contact with ${client1} and 1 and Mobile and ${ExtUser01.sip_trunk_did} and CUSER_193095 and CLast and mitel and test and CUSER_193095@mitel.com

    # Select the checkbox for not opening the outlook for contact creation for UserB
    Open Outlook Tab with ${client2}
    Configure Outlook Tab with ${client2} and contacts and check

    # UserA creates a contact
    #Create New Contact with ${client2} and 1 and Mobile and ${ExtUser01.sip_trunk_did} and CUSER_193095 and CLast and mitel and test and CUSER_193095@mitel.com
    
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
			
	Check User Detail Attribute with ${client1} and info and positive
	Check User Detail Attribute with ${client1} and call and positive
	Check User Detail Attribute with ${client1} and min and positive

    # Place call from UserA to UserB
	Call Control with ${client1} and start and ${EMPTY} and ${EMPTY}
			
	#Sleep    2s
	# UserB verifies incoming call options
	Check Incoming Call with ${client2}
	# Answer call
	Call Control with ${client2} and recv and ${EMPTY} and ${EMPTY}

    Call Control with ${client1} and consult and CUSER_193095 and ${EMPTY}

    Check Incoming Call with ${client3}
    Call Control with ${client3} and recv and ${EMPTY} and ${EMPTY}

    Verify Hold User Dashboard with ${client2} and ${user01.first_name} ${user01.last_name} and put_you_on_hold

    # UserA presses transfer button to complete the transfer
    Verify Hold Consult In Conf Call with ${client1} and consulting

    # UserA clicks on transfer button to coplete the consult transfer
    Verify Hold Consult In Conf Call with ${client1} and complete_consult
    Sleep    2s

    # Verifies that UserA is droped from the call
    Verify No Ongoing Call with ${client1}

    # Verifiy that UserB's dashboard lists UserC for the call
    #Verify Click User Dashboard with ${client2} and CUSER_193095 CLast
    
    # UserC ends the call
    Place End Call with ${client2} and end and ${EMPTY}
    #Place End Call with ${client3} and end and ${EMPTY}
    
    Delete Contact with ${client1} and CUSER_193095 and CLast  