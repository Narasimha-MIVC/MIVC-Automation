*** Settings ***
Documentation     MH_interacting_with_greetings_allow_VM
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1

Test Teardown     call method      ${client1}      close_browser
*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   
   

*** Test cases ***
MH_interacting_with_greetings_allow_VM
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    
# $client1 command action verify_preferences_call_routing_page component_id=$componentId
    Verify Preferences Call Routing Page with ${client1}

#verify rule change button panel
	Verify Preferences Basic Routing Change Panels with ${client1} and interacting_greeting1	
    Interacting_With Greeting AllowVM with ${client1} and yes