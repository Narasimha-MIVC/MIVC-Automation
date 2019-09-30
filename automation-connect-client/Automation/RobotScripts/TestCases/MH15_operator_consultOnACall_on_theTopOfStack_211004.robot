*** Settings ***
Documentation     MH15_operator_consultOnACall_on_theTopOfStack
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        5 minutes
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
    ${objects_list}=   Launch Login with ${user01} and ${user02} and ${user03} and ${user04} and 4 
    
    ${client_one} =      Get From List      ${objects_list}      0   
    ${client_two} =      Get From List      ${objects_list}      1
    ${client_three} =    Get From List      ${objects_list}      2
	${client_four} =     Get From List      ${objects_list}      3 

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three}
	Set Test Variable    ${client4}    ${client_four}      


Serial Execution
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3 
    Import Library			  ${CURDIR}/../../ManhattanLibrary/lib/ManhattanComponent.py        ${port4}          WITH NAME      client4 

    ${client_one}=    Get library instance      client1   
    ${client_two}=    Get library instance      client2
    ${client_three}=  Get library instance      client3
	${client_four}=  Get library instance      client4  

    Set Test Variable    ${client1}    ${client_one}
    Set Test Variable    ${client2}    ${client_two}
    Set Test Variable    ${client3}    ${client_three}
	Set Test Variable    ${client4}    ${client_four} 
    
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  5
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}

Parallel Teardown
    Close Applications with 4

Serial Teardown
    Run Keywords    call method      ${client1}      close_browser         AND      call method      ${client2}      close_browser    AND      call method      ${client3}      close_browser    AND      call method      ${client4}      close_browser            

*** Test cases ***
MH15_operator_consultOnACall_on_theTopOfStack
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
# userB called to userA
    Call Contact By DoubleClick with ${client2} and ${user01.first_name} ${user01.last_name}

# userA answers the call
    Place End Call with ${client1} and recv and ${EMPTY}

# userD called to userA
    Call Contact By DoubleClick with ${client4} and ${user01.first_name} ${user01.last_name}

# userA answers the call
    Place End Call with ${client1} and recv and ${EMPTY}
    Check Status Of Call InStack with ${client1} and firstCall and ${user02.first_name} ${user02.last_name}

# unhold userB's call
    Show Verify ContactCard with ${client1} and CallDashboard and ${EMPTY} and ${user02.first_name} ${user02.last_name}
    Place End Call with ${client1} and unHold and ${EMPTY}    
# search for userC    
    Show Verify ContactCard with ${client1} and Sdirectory and yes and ${user03.first_name} ${user03.last_name}

# drag the userB's call and drop it to userC
    Drag The Call And Hover with ${client1} and ${user03.first_name} ${user03.last_name} and In_call and ${user02.first_name} ${user02.last_name} and ${EMPTY}

# select consult conference option from contexual menu
    Transfer Call Via ContexualMenu with ${client1} and ConsltConf

# verify the two legs of call where leg1 have hold call and leg2 have consult call info
    verify_holdCall_and_consultCall with ${client1} and no and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}

# check incoming call from userA and receive the call
    Check Incoming Call with ${client3}
    Place End Call with ${client3} and recv and ${EMPTY}

# select complete conference option at userA to conference
    Complete Consult Call with ${client1} and conference

# ending the call at userD
    Place End Call with ${client4} and end and ${EMPTY}
 
# verify conference call at userA, userB and userC
    Verify Users In A Dashboard In Call with ${client1} and two_users and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Verify Users In A Dashboard In Call with ${client2} and two_users and ${user03.first_name} ${user03.last_name} and ${user01.first_name} ${user01.last_name}
    Verify Users In A Dashboard In Call with ${client3} and two_users and ${user01.first_name} ${user01.last_name} and ${user02.first_name} ${user02.last_name}

# end calls at userC and userA
    Place End Call with ${client3} and end and ${EMPTY}
    Place End Call with ${client1} and end and ${EMPTY}