*** Settings ***
Documentation     MH_Verifying_Contact_Search_Result_Adding_contact_to_Favorite_group_from_search_result
...               Aakash
...               Comments:
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot

Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1
Test Timeout        4 minutes
Test Teardown       call method      ${client1}      close_browser      

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***    
Keyword 1
    [Arguments]       ${client1} 
    
    
*** Test cases ***
MH_Verifying_Contact_Search_Result_Adding_contact_to_Favorite_group_from_search_result
    ${client1}=  Get library instance      client1     
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   

    #Login to the Manhattan Client from ST_Users/MT_Users   
    :FOR  ${Index}  IN RANGE  1  2
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    \   Cleanup Favorites with ${client${Index}}     
    
    # UserA adds UserB in Favotites
    Add Or Delete To Favorite Group with ${client1} and ${user02.first_name} ${user02.last_name} and add    
    Close Panel with ${client1} and second_search
    
    # UserA verifies that UserB is present in Favorites
    Invoke Dashboard Tab with ${client1} and people
    Check Favorite Symbol with ${client1} and true and ${user02.first_name} ${user02.last_name} 

    # UserA removes UserB from Favotites
    Add Or Delete To Favorite Group with ${client1} and ${user02.first_name} ${user02.last_name} and remove
    Invoke Dashboard Tab with ${client1} and people
    Check Favorite Symbol with ${client1} and false and ${user02.first_name} ${user02.last_name} 
    
    
    
    
    
    
    
    
    
    
    
   