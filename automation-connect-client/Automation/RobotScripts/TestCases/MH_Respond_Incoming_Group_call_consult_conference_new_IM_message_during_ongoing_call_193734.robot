*** Settings ***
Documentation     MH_Respond_Incoming_Group_call_consult_conference_new_IM_message_during_ongoing_call
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot

Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port2}          WITH NAME      client2
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port3}          WITH NAME      client3
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port4}          WITH NAME      client4
Test Timeout        6 minutes
Test Teardown       Run Keywords    call method      ${client1}      close_browser          AND      call method      ${client2}      close_browser        AND      call method      ${client3}      close_browser       AND       call method      ${client4}      close_browser      
  


*** Variables ***
# Moved to Test Variables file 

*** Keyword ***	    
Keyword 1
    [Arguments]       ${client1}    ${client2}     ${client3}    ${client4}      
    
*** Test cases ***
MH_Respond_Incoming_Group_call_consult_conference_new_IM_message_during_ongoing_call
    ${client1}=  Get library instance      client1   
    ${client2}=  Get library instance      client2
    ${client3}=  Get library instance      client3
    ${client4}=  Get library instance      client4
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   ${client2}   ${client3}    ${client4}
    
    #Login to the Manhattan Client from ST_Users/MT_Users   
    :FOR  ${Index}  IN RANGE  1  5
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    \   End Voicemail Call with ${client${Index}}
    
    # Search extension and open third panel
    Search People Extension with ${client3} and ${user02.first_name} ${user02.last_name}
    
    # Check Info button in third panel
    Check User Detail Attribute with ${client3} and info and positive
    Check User Detail Attribute with ${client3} and call and positive
    Check User Detail Attribute with ${client3} and min and positive
    
    # Place call from USER_DB1_01 third pane to USER_PSP_02_188428
    Place End Call with ${client3} and start and ${EMPTY}
    
    # Check incoming call options
    Check Incoming Call with ${client2}
    
    # Answer call
    Place End Call with ${client2} and recv and ${EMPTY}
    
    Blind Audio Conference Call with ${client3} and conference and ${user04.first_name} ${user04.last_name} 
    Place End Call with ${client4} and recv and ${EMPTY}
    Sleep    3
    Blind Audio Conference Call with ${client2} and Consult and ${user01.first_name} ${user01.last_name}
    
    # Check incoming call options
    Check Incoming Call with ${client1}
    
    Click Send Cannedresponse Incall with ${client1} and hellotisisuser1
    
    #Invoke messages Tab
    Invoke Dashboard Tab with ${client2} and messages
    Sleep    2s

    #verify_default_call_panel_click_vm
    Place End Call with ${client3} and end and ${EMPTY}
    Place End Call with ${client4} and end and ${EMPTY}

    # wait for IM to appear
    Sleep    1s
    Search People Extension with ${client2} and ${user01.first_name} ${user01.last_name}
    Click Filter Message with ${client2} and Messages
    Received IMB with ${client2} and true and hellotisisuser1

    
    
