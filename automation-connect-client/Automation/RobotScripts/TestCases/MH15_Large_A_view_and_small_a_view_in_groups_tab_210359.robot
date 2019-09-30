*** Settings ***
Documentation     MH15_Large_A_view_and_small_a_view_in_groups_tab
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1

Test Timeout        6 minutes
Test Teardown     call method      ${client1}      close_browser
*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   

*** Test cases ***
MH15_Large_A_view_and_small_a_view_in_groups_tab
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
    #Sleep     2s
#Login to the Manhattan Client
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}

# open people tab
    Invoke Dashboard Tab with ${client1} and people
    Select People View with ${client1} and list

#create new groups : groupA, groupB, groupC, groupD, groupE
    Create New Group with ${client1} and groupA and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Create New Group with ${client1} and groupB and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Create New Group with ${client1} and groupC and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Create New Group with ${client1} and groupD and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Create New Group with ${client1} and groupE and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}

# check created groups
    Check Created Groups with ${client1} and groupA and groupB and groupC and groupD and groupE

# change the group view from list view to compact view
    Select People View with ${client1} and compact

# verify the group
    Check Created Groups with ${client1} and groupA and groupB and groupC and groupD and groupE

# change the group view from compact to list view
    Select People View with ${client1} and list

# verify the group
    Check Created Groups with ${client1} and groupA and groupB and groupC and groupD and groupE