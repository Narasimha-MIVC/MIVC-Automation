*** Settings ***
Documentation     Voicemail-Feature
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot           
Library             Collections
Test Timeout        12 minutes
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
Voicemail-Feature
    Run Keyword If  ${conf.parallel_execution} == 1  Parallel Execution    ELSE  Serial Execution
    Run Keyword If  ${conf.user_provision} == 1  User Provision
    
    Cleanup Voicemails with ${client2}
    #Play VM through phone
        # UserA opens contact card of UserB
        Search People Extension with ${client1} and ${user02.first_name}**${user02.last_name}

        # UserA checks details of UserB
        Check User Detail Attribute with ${client1} and call and positive

        # UserA starts a call to UserB 
        Call Control with ${client1} and start and ${EMPTY} and ${EMPTY}

        # UserB moves the call to voicemail
        Call Control with ${client2} and toVoiceMail and ${EMPTY} and ${EMPTY}
        Sleep     10s

        # UserA ends the call
        Call Control with ${client1} and end and ${EMPTY} and ${EMPTY}

        # UserB opens voicemail tab
        Invoke Dashboard Tab with ${client2} and voicemail
        Sleep     2s

        # UserB plays voicemail from phone
        Check Badge Count with ${client2} and voicemail
        Play Unread Voicemails Via Phone with ${client2}

    #record/reply vm through phone
        # UserB records and replies the voicemail
        Reply Forward Voicemail with ${client2} and reply and default and ${EMPTY} and phone and none
        Close Panel with ${client2} and second
        
        #Check on User A for the VM badge increase
        Sleep     2s
        Check Badge Count with ${client1} and voicemail

    #play Vm through comp speakers
        # UserB plays same voicemail from computer
        Invoke Dashboard Tab with ${client2} and voicemail
        Play Pause Read Vms with ${client2} and recent and play and 1 and computer

    #Record & fwd Vm through comp speakers
        # UserB records and forwards the voicemail to 3rd user
        Reply Forward Voicemail with ${client2} and forward and default and ${user03.first_name} ${user03.last_name} and computer and none
        # UserC verifies voicemail forward
        Check Badge Count with ${client3} and voicemail
    #delete VM
        # UserB deletes the Voicemail sent by UserA
        Delete Voicemails with ${client2} and read and ${user01.first_name} ${user01.last_name}
    #Restore VM
        # UserB restores the deleted voicemail 
        Restore Voicemail with ${client2} and ${user01.first_name} ${user01.last_name} and unread
    
    #Save/unsave voicemail
        # # UserA opens voicemail tab
        # Check Badge Count with ${client1} and voicemail
        # Invoke Dashboard Tab with ${client1} and voicemail
        
        # # UserA saves voicemail & checks that it is in Saved folder
        # Save Unsave Voicemail with ${client1} and save and unheard and ${user02.first_name} ${user02.last_name}
        
        # # UserA unsaves voicemail & checks that it is not in Saved folder
        # Save Unsave Voicemail with ${client1} and unsave and unheard and ${user02.first_name} ${user02.last_name}