*** Settings ***
Documentation     MH15_operator_leftClick_dragAContact_InFavTab_andHoverToActiveCall
...               HariPrakash
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        6 minutes
Test Teardown       Custom Teardown 

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Custom Teardown
    Run Keyword If   ${conf.parallel_execution} == 1    Parallel Teardown    ELSE    Serial Teardown 

User Provision
    [Arguments]       ${client1}     ${client2}     
    Log   ${client1}

Parallel Execution
    Import Library			    ${CURDIR}/../../ManhattanLibrary/lib/mnh_parallel_executor.py
    ${objects_list}=   Launch Login with ${user01} and ${user02} and ${user03} and ${user04} and 3 
    
    ${client_one} =      Get From List      ${objects_list}      0   
    ${client_two} =      Get From List      ${objects_list}      1
    ${client_three} =    Get From List      ${objects_list}      2 

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three}      


Serial Execution
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3 
    
    ${client_one}=    Get library instance      client1   
    ${client_two}=    Get library instance      client2
    ${client_three}=  Get library instance      client3  

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three} 
    
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  4
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}

Parallel Teardown
    Close Applications with 3

Serial Teardown
    Run Keywords    call method      ${client1}      close_browser         AND      call method      ${client2}      close_browser    AND      call method      ${client3}      close_browser             
   

*** Test cases ***
MH15_operator_leftClick_dragAContact_InFavTab_andHoverToActiveCall
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    Cleanup Favorites with ${client1}
    
    # UserB opens contact card of UserA
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name} 
 
    # UserB places a call to UserA
    Place End Call with ${client2} and start and ${EMPTY}

    # UserA verifies that incoming call notification in present
    Check Incoming Call with ${client1}
       
    # UserA receives call
    Place End Call with ${client1} and recv and ${EMPTY}
    
    # UserB verifies that in client pane caller name is present
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and onCall and ${EMPTY} and ${EMPTY}
        
    # UserA verifies that in client pane callee name is present
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY}
	
	# UserA adds UserC in Favotites
    Add Or Delete To Favorite Group with ${client1} and ${user03.first_name} ${user03.last_name} and add    
    #Close Panel with ${client1} and second_search
	
    
    # UserA verifies that UserC is present in Favorites
    #Invoke Dashboard Tab with ${client1} and people
   	
	#UserA drags and drops the call to the UserC to Intercom transfer the call
	Place End Call with ${client1} and drag_and_move and favouriteContactTransfer
	
	#UserA completes the Intercom Transfer
	Complete the Intercom Transfer with ${client1} and Complt_trans
	
	#UserC receives the calll from UserB
	Place End Call with ${client3} and recv and ${EMPTY}
     
    # UserB ends the call with UserC
    Place End Call with ${client2} and end and ${EMPTY}	
    
	#UserA removes the contact from Favourites
	Add Or Delete To Favorite Group with ${client1} and ${user03.first_name} ${user03.last_name} and remove 
	
	
	
  
