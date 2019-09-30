*** Settings ***
Documentation     External-Assignment
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py    ${port1}    WITH NAME    client1
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py    ${port2}    WITH NAME    client2
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py    ${port3}    WITH NAME    client3

Test Timeout     7 minutes
Test Teardown    Run Keywords     call method    ${client1}    select_phone_type    &{params}    AND    call method    ${client1}    close_application    AND    call method    ${client2}    close_application    AND    call method    ${client3}    close_application
*** Variables ***
# Moved to Test Variables file
&{params}     phone_type=desk_phone 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   

*** Test cases ***
External-Assignment
    ${client1}=  Get library instance    client1
    ${client2}=  Get library instance    client2
    ${client3}=  Get library instance    client3

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
   
# Login to the Manhattan Client from ST_Users   
    :FOR  ${Index}  IN RANGE  1  3
    \   login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    login with ${client3} and ${ExtUser01.client_id} and ${ExtUser01.client_password} and ${ExtUser01.server}
# Do external assigment for USER A with option "automatically connect"
    Add New Label with ${client1} and External and ${ExtUser01.sip_trunk_did} and 1 and 8
    Close Panel with ${client1} and second

# - Automatic answer
# UserB search for UserA and Open contact card of UserA
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name}

# User B makes call to User A
    Call Control with ${client2} and start and ${EMPTY} and ${EMPTY}

#Make sure there is no Recieve call botton on userA since he is on Exernal Assignment
    Verify External Assignment with ${client1}


#user C(DID mapped in USERA for external assigment) receives call
    Call Control with ${client3} and recv and ${EMPTY} and ${EMPTY}

    
# Have userA click on dashboard icon toopne contact card of userB
    Verify Click User Dashboard with ${client1} and ${user02.first_name} ${user02.last_name} 

    
#Make sure call is in connected state on userA by verifying the hold button on the conatct card
    Check User Detail Attribute with ${client1} and holdCall and positive
    
 
#user B ends call
    Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}
    
    
# - Press 1 to connect
# Do external assigment for USER A with option "Press 1 to connect"
    Edit Modify Label with ${client1} and 1 and 2
    Close Panel with ${client1} and second
    

# UserB search for UserA and Open contact card of UserA
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name}

# User B makes call to User A
    Call Control with ${client2} and start and ${EMPTY} and ${EMPTY}
    
#Make sure there is no Recieve call botton on userA since he is on Exernal Assignment
    Verify External Assignment with ${client1}

# user C(DID mapped in USERA for external assigment) receives call
    Call Control with ${client3} and recv and ${EMPTY} and ${EMPTY}
 
# Have userA click on dashboard icon to open contact card of userB
    Verify Click User Dashboard with ${client1} and ${user02.first_name} ${user02.last_name} 

    
#Make sure call is still in not in connected state on userA by verifying the hold button
    Check User Detail Attribute with ${client1} and holdCall and negative

# Open Dialpad to press 1 to establish call
    Open Dialpad with ${client3}
	#Sleep    2s
    Click Dialpad Numbers with ${client3} and one
    Close Dialpad Search with ${client3}
    
# Open contact card of UserB
    Verify Click User Dashboard with ${client1} and ${user02.first_name} ${user02.last_name} 
    
#Make sure call is in connected state on userA after pressing 1 
    Check User Detail Attribute with ${client1} and holdCall and positive
   

# user B ends call
    Call Control with ${client2} and end and ${EMPTY} and ${EMPTY}
    #Sleep      2s 

    #user A assigned back to deskphone from softphone
    #Select Phone Type with ${client1} and desk_phone and ${EMPTY}
   
    


