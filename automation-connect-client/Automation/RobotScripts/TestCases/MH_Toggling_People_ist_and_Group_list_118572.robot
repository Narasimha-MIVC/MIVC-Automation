*** Settings ***
Documentation     MH_Toggling_People_ist_and_Group_list
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
MH_Toggling_People_ist_and_Group_list
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}

# Create 2 groups
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and GroupABC and save and ${user02.first_name} ${user02.last_name} and ${EMPTY}
    Create New Group with ${client1} and GroupCBA and save and ${user02.first_name} ${user02.last_name} and ${EMPTY}
    Close Panel with ${client1} and second

# Verify contact listing
    Verify Contact Listing with ${client1}
    Close Panel with ${client1} and second_search

# Verify that groups created above are displayed
    Invoke Dashboard Tab with ${client1} and people
    Display Group List with ${client1} and GroupABC and GroupCBA

# Verify contact listing
    Verify Contact Listing with ${client1}
    Close Panel with ${client1} and second_search
    Close Panel with ${client1} and second

# Verify that groups created above are displayed
    #Invoke Dashboard Tab with ${client1} and people 
    # Display Group List with ${client1} and GroupA and GroupB
    
