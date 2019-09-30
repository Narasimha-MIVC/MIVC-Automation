*** Settings ***
Documentation     SoftPhone-Feature
...               Aakash
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}           WITH NAME      client1
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}           WITH NAME      client2

Test Timeout        6 minutes
Test Teardown       Run Keywords    call method      ${client1}      close_application         AND      call method      ${client2}      close_application       
*** Variables ***
# Moved to Test Variables file 

*** Keywords ***	     
Keyword 1
    [Arguments]       ${client1}     ${client2}     
    Log   ${client1}
    
*** Test Cases ***
SoftPhone-Feature
    ${client1}=     Get library instance      client1          
    ${client2}=     Get library instance      client2          
              
   
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}     ${client2}      
    
    #Login to the Manhattan Client from ST_Users/MT_Users   
    :FOR  ${Index}  IN RANGE  1  3
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    \   End Voicemail Call with ${client${Index}} 
    
    # Select SoftPhone of USERA
    Select Phone Type with ${client1} and soft_phone and yes
    
    #Search USERB for making a call to deskphone of USERB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    #Sleep      2s   
    
    # UserA places a call to UserB
    Place End Call with ${client1} and start and ${EMPTY}
    #Sleep      2s   
    
    # UserB receives call
    Place End Call with ${client2} and recv and ${EMPTY}
    #Sleep       2s
    
    #user A holds call
    Place End Call with ${client1} and hold and ${EMPTY}
    #Sleep       2s
    
    #user A checks the call is on hold
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onHold and ${EMPTY} and ${EMPTY}
    #Sleep       2s
    
    #user A unholds the call
    Place End Call with ${client1} and unHold and ${EMPTY}
    #Sleep       2s
    
    #user A checks the call is in progress
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY} 
    
    #user A ends call
    Place End Call with ${client1} and end and ${EMPTY}
    
    # Select SoftPhone of USERA
    Select Phone Type with ${client2} and soft_phone and yes
    Close Panel with ${client2} and second
    
    #Search USERB for making a call via softphone of USERB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    #Sleep      2s
    
    # User A makes call to User B
    Place End Call with ${client1} and start and ${EMPTY}
    #Sleep      2s
    
    #user b receives call
    Place End Call with ${client2} and recv and ${EMPTY}
    #Sleep      2s
    #user A holds call
    Place End Call with ${client1} and hold and ${EMPTY}
    #Sleep      2s
    
    #user A checks the call is on hold
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onHold and ${EMPTY} and ${EMPTY} 
    #Sleep      2s
    #user A unholds the call
    Place End Call with ${client1} and unHold and ${EMPTY}
    #Sleep      2s
    
    #user A checks the call is in progress
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY}
    #Sleep      1s
    #user A ends call
    Place End Call with ${client1} and end and ${EMPTY}
    #Sleep      2s
    
    #user B assigned back to deskphone from softphone
    Select Phone Type with ${client2} and desk_phone and ${EMPTY}
    Sleep      1s
    # Close Panel with ${client2} and second    
    Select Phone Type with ${client1} and desk_phone and ${EMPTY}
    Sleep      1s
    # Close Panel with ${client1} and second     
    
    
    # Close the Manhattan Client 
    # Close Application with ${client3}
    # Close Application with ${client2}
    # Close Application with ${client1}