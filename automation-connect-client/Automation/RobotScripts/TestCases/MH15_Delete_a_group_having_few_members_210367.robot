*** Settings ***
Documentation     MH15_Delete_a_group_having_few_members
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1

Test Timeout        4 minutes
Test Teardown     call method      ${client1}      close_browser
*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}
   

*** Test cases ***
MH15_Delete_a_group_having_few_members
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

#Login to the Manhattan Client from ST_Users
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}

#UserA creates a group
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and Group1 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}

# open the group info and delete the group cancel deletion again edit and delete the group
    Delete Group with ${client1} and Group1 and cancel
    #Delete Group with ${client1} and Group1 and delete