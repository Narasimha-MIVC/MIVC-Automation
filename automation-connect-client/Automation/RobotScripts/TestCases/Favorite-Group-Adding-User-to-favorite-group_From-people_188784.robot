*** Settings ***
Documentation     Favorite-Group-Adding-User-to-favorite-group_From-people
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
Favorite-Group-Adding-User-to-favorite-group_From-people
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
    #Sleep     2s
#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    Cleanup Favorites with ${client1}
    
# UserA verifies that white Favorite symbol is present for UserB
    Check Favourite Symbol From Search ${client1} and ${user02.first_name}**${user02.last_name}

# UserA adds UserB to favourite list
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user02.first_name}**${user02.last_name} and add
# UserA verifies that contact card of UserB is not opened
    Verify Contact Card with ${client1} and absent and ${user02.first_name}**${user02.last_name} and ${Empty}

# UserA verifies that white Favorite symbol is present present for UserC
    Close Panel with ${client1} and second_search
    Check Favourite Symbol From Search ${client1} and ${user04.first_name}**${user04.last_name}
# UserA adds UserC to favourite list
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user04.first_name}**${user04.last_name} and add
# UserA verifies that contact card of UserC is not opened
    Verify Contact Card with ${client1} and absent and ${user04.first_name}**${user04.last_name} and ${Empty}

# UserA opens people tab
    Invoke Dashboard Tab with ${client1} and people

# UserA verifies that UserB and UserC are listed in Favorite group
    Check Favourite Symbol From Search ${client1} and ${user02.first_name}**${user02.last_name}
    Close Panel with ${client1} and second_search

    Check Favourite Symbol From Search ${client1} and ${user04.first_name}**${user04.last_name}
    Close Panel with ${client1} and second_search

# UserA removes userB and UserC to favourite list
    Add Or Delete To Favorite Group with ${client1} and ${user02.first_name}**${user02.last_name} and remove
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user04.first_name}**${user04.last_name} and remove
