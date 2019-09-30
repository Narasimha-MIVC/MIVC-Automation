*** Settings ***
Documentation     MH_Editing_a_Group_Do_not_Save_Changes
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
MH_Editing_a_Group_Do_not_Save_Changes
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}


#UserA creates two groups
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and group_202763 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}

# Verify group options and members and open the group for editing
    Edit Group with ${client1} and group_202763 and ${user02.first_name} ${user02.last_name}

# Add another member to the group and change the group name
    Modify Group Add Member with ${client1} and group_202763 and ${user04.first_name} ${user04.last_name} and ${user05.first_name} ${user05.last_name} and cancel and new_group_202763 and yes

# Verify that group has not been modified
    Select Group Options with ${client1} and group_202763 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${user04.first_name} ${user04.last_name} and ${user05.first_name} ${user05.last_name} and ${EMPTY}   