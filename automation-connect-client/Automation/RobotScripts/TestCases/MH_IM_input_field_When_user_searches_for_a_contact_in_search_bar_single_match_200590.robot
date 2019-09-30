*** Settings ***
Documentation     MH_IM_input_field_When_user_searches_for_a_contact_in_search_bar_single_match
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot

Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1
Test Timeout        3 minutes
Test Teardown       call method      ${client1}      close_browser          

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1} 
    
    
*** Test cases ***
MH_IM_input_field_When_user_searches_for_a_contact_in_search_bar_single_match      
    ${client1}=  Get library instance      client1     
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   

    #Login to the Manhattan Client from ST_Users/MT_Users     
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    
    # UserA opens contact card of UserB
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}

    # select messages tab in third panel
    Click Filter Message with ${client1} and messages
    
    Verify Im Textarea Check Sent Text with ${client1}    
    
    
    
    
    
    