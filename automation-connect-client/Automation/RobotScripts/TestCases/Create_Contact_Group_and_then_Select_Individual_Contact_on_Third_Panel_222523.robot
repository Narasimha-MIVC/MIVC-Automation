*** Settings ***
Documentation     Create_Contact_Group_and_then_Select_Individual_Contact_on_Third_Panel
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1

Test Timeout      5 minutes
Test Teardown     call method      ${client1}      close_browser
*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   

*** Test cases ***
Create_Contact_Group_and_then_Select_Individual_Contact_on_Third_Panel
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
    Sleep     2s
#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}

#UserA creates two groups
    Invoke Dashboard Tab with ${client1} and people

# Open new group creation form and enter group name
    Enter Group Name with ${client1} and TestGroup

# Drag and drop contacts to group and create group
    Drag Drop Contact To Group with ${client1} and TestGroup and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Sleep    2s

# Verify that group is created and all the members are listed
    Invoke Dashboard Tab with ${client1} and people
    Select People View with ${client1} and compact
    Select Group Options with ${client1} and TestGroup and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY}
