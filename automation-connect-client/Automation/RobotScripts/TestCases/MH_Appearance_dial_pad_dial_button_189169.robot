*** Settings ***
Documentation     MH_Appearance_dial_pad_dial_button
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1 

Test Timeout        4 minutes   
Test Teardown       call method      ${client1}      close_browser           

*** Variables ***
# Moved to Test Variables file
 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1}     

    
*** Test cases ***
MH_Appearance_dial_pad_dial_button
    ${client1}=  Get library instance      client1      
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}      
    Sleep     2s
    # Login to Clients
    :FOR  ${Index}  IN RANGE  1  2
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    
    #Touch dial-pad button in Manhatten client
    #Sleep     2s
    Open Dialpad with ${client1} 

    #verify dial-pad buttons
    Verify Dialpad with ${client1} 
    
    #Closing the dialpad search
    Close Dialpad Search with ${client1}