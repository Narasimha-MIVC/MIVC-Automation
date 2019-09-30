*** Settings ***
Documentation     MH_IM-pane-Switch-between-Group-and-a-1-1-IM-panes
...               HariPrakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot

Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Test Teardown      Run Keywords    call method      ${client1}      close_browser         AND      call method      ${browser1}      close_browser        AND      call method      ${browser2}      close_browser

Test Timeout        7 minutes



*** Variables ***
# Moved to Test Variables file 

*** Keyword ***	    
Keyword 1
    [Arguments]       ${client1}    ${client2}    
    
*** Test cases ***
MH_IM-pane-Switch-between-Group-and-a-1-1-IM-panes
    ${client1}=  Get library instance      client1
       
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}    ${client2}  

    #Login to the Manhattan Client from ST_Users/MT_Users   
    :FOR  ${Index}  IN RANGE  1  2
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    
	#USERA clicks the outlook tab
	Open Outlook Tab with ${client1}
	
	#USERA checks the no outlook contacts
	Configure Outlook Tab with ${client1} and contacts and check
	
	#USERA clicks on New Contact
	Go To New Contact with ${client1}
	
	#USERA adds new contact
	Add Contact Number with ${client1} and 1 and Mobile and 99999999
	
	#USERA adds new Contact Ajoy1 Kumar1
	Add Contact Details with ${client1} and Ajoy1 and Kumar1 and hrao@shoretel.com and Engineer and Regression and Mitel and KSLayout and Bangalore and India
	
    Sleep     1s
	
	#Closes the second panel in USERA Client
	Close Panel with ${client1} and second
	
    #USERA clicks on New Contact
	Go To New Contact with ${client1}
	
	#USERA adds new contact
	Add Contact Number with ${client1} and 1 and Mobile and 99999999
	
	#USERA adds new Contact Avantika kumari
	Add Contact Details with ${client1} and Avantika and kumari and hrao@shoretel.com and Engineer and Regression and Mitel and KSLayout1 and Bangalore and India
	
	# UserA opens Events tab
    Invoke Dashboard Tab with ${client1} and event
	
	# UserA clicks on new event button
    Open New Event with ${client1}
    
    # UserA enters meeting name
    Events Add Meeting Details with ${client1} and newEvent and 1
	
	#USERA selects the custom event
	Events Select Meeting Type with ${client1} and custom
	
	# UserA adds Ajoy1 Kumar1 as participant
    Events Meeting Type Add User with ${client1} and participants and Ajoy1 Kumar1 
	
	# UserA adds Avantika kumari  as participant
    Events Meeting Type Add User with ${client1} and participants and Avantika kumari      
	
    #UserA Creates Event
    Events Create Invite with ${client1}
	
	sleep    2s
	
	#USERA opens the created event
	Open Event Info with ${client1} and newEvent and yes
    
    # Copy event URL
    ${url}=    Get Url with ${client1}
   
    # UserA joins event
    Join Endo Conference with ${client1} and newEvent and ${EMPTY} and ${EMPTY}
    
    # Launch browser for UserB
    Import Library        ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py      ${port5}          WITH NAME      browser1
    ${browser1}=  Get library instance      browser1
    
    # Launch browser for UserC
    Import Library        ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py      ${port6}          WITH NAME      browser2
    ${browser2}=  Get library instance      browser2
    
	#Launch the browser with the url
    Launch Url with ${browser1} and ${url}
    
    #UserB join event
    Join Exo Event with ${browser1} and Ajoy1 Kumar1
    
	#Launch the browser with the url
    Launch Url with ${browser2} and ${url}
	
    # UserC join event    
    Join Exo Event with ${browser2} and Avantika kumari 
	
    # UserB send IM to group
    Click On Users For Chat with ${browser1} and group_chat 
    Send Im Exo with ${browser1} and group_B
    Sleep    2s

    # UserA verifies that IM is received
    Received IMA with ${client1} and true and group_B
    
    # UserC verifies that IM is received
    Click On Users For Chat with ${browser2} and group_chat 
   
    # UserC send IM to group
    Send Im Exo with ${browser2} and group_C
    Sleep    2s
    # UserA verifies that IM is received
    Received IMA with ${client1} and true and group_C
	Sleep    1s
    #User Ajoy1 Kumar1 does indivial chat	
	Exo Client Communication with ${browser2} and individual_chat and Ajoy1 Kumar1
	
	# UserAjoy1 Kumar1 send IM
	Send Im Exo with ${browser2} and Hello
	
	#User Avantika kumari does indivial chat
	Exo Client Communication with ${browser1} and individual_chat and Avantika kumari
	
	#User Avantika kumari send IM
	Send Im Exo with ${browser1} and Hi
    
	#USERA clicks on Event Tab
	Invoke Dashboard Tab with ${client1} and event
    
	#USERA opens the event 
    Open Event Info with ${client1} and newEvent and yes
	
	#USERA cancels the event
	Cancel Event with ${client1}
	
	
	 
	
	
