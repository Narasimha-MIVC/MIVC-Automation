*** Settings ***
Documentation     Video-Feature
...               Aakash
...               Comments:

Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}           WITH NAME      client1
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port4}           WITH NAME      client2

Test Timeout        6 minutes
Test Teardown       Run Keywords    call method      ${client1}      close_application         AND      call method      ${client2}      close_application       
*** Variables ***
# Moved to Test Variables file 

*** Keywords ***	     
Keyword 1
    [Arguments]       ${client1}     ${client2}     
    Log   ${client1}
    
*** Test Cases ***
Video-Feature 
    ${client1}=     Get library instance      client1          
    ${client2}=     Get library instance      client2          
              
   
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}     ${client2}      
    
    #Login to the Manhattan Client from ST_Users/MT_Users   
    :FOR  ${Index}  IN RANGE  1  3
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    \   Select Phone Type with ${client${Index}} and soft_phone and ${EMPTY}
    
    # Enable soft phone option in both the clients for video calling
    # Select Phone Type with ${client1} and soft_phone and ${EMPTY}
    # Select Phone Type with ${client2} and soft_phone and ${EMPTY}
 
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    Sleep      1s

    # user A calls user B
    Place End Call with ${client1} and start and ${EMPTY}
    
    # User B receives the call
    Place End Call with ${client2} and recv and ${EMPTY}
    Sleep      2s
    #Enable video feature
    Place End Call with ${client1} and video and ${EMPTY}
    Sleep      2s
    Place End Call with ${client2} and video and ${EMPTY}
    Sleep      1s
    
    # Click on call entry in dashboard
    Verify Click User Dashboard with ${client1} and ${user02.first_name} ${user02.last_name}
    Sleep      2s
    Verify Click User Dashboard with ${client2} and ${user01.first_name} ${user01.last_name}
    
    #check in user A whether video call is happening
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and videoCall and ${EMPTY} and ${EMPTY}
    #check in user B whether video call is happening
    Check Client Panel with ${client2} and ${user01.first_name} ${user01.last_name} and videoCall and ${EMPTY} and ${EMPTY}
    
    #user A holds the call
    Place End Call with ${client1} and hold and ${EMPTY}
    Sleep      1s
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onHold and ${EMPTY} and ${EMPTY}
    
    #user A unholds the call
    Place End Call with ${client1} and unHold and ${EMPTY}
    Sleep      1s
    
    #user A checks the call is in progress
    Check Client Panel with ${client1} and ${user02.first_name} ${user02.last_name} and onCall and ${EMPTY} and ${EMPTY}
    
    #User A ends call
    Place End Call with ${client1} and end and ${EMPTY}    
       
    Select Phone Type with ${client2} and desk_phone and ${EMPTY}
    Sleep      2s
    Select Phone Type with ${client1} and desk_phone and ${EMPTY}
    Sleep      2s
    
    