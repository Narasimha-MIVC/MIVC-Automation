*** Settings ***
Documentation     Toggle-Favorites-and-Groups
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
Toggle-Favorites-and-Groups
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
   
#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    Cleanup Favorites with ${client1}

#UserA creates two groups
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and Group1 and save and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name}
    Create New Group with ${client1} and Group2 and save and ${user04.first_name} ${user04.last_name} and ${user05.first_name} ${user05.last_name}

# UserA adds 4 users to Favorite group
    Add Or Delete To Favorite Group with ${client1} and ${user02.first_name}**${user02.last_name} and add
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user03.first_name}**${user03.last_name} and add
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user04.first_name}**${user04.last_name} and add
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user05.first_name}**${user05.last_name} and add

#Verifies that Favorites button is appearing with orange colour and verify all the users are part of Favorites
    Invoke Dashboard Tab with ${client1} and people
    Check Favorite Symbol with ${client1} and true and ${user02.first_name} ${user02.last_name}
    Check Favorite Symbol with ${client1} and true and ${user03.first_name} ${user03.last_name}
    Check Favorite Symbol with ${client1} and true and ${user04.first_name} ${user04.last_name}
    Check Favorite Symbol with ${client1} and true and ${user05.first_name} ${user05.last_name}

# Opens contact card of one user
    Open Contact Card with ${client1} and favorites and ${user02.first_name} ${user02.last_name}
# Verifies that contact card is opened
    Verify Contact Card with ${client1} and present and ${user02.first_name} ${user02.last_name} 

# Verifies that users added to Group1 are present
    Select Group Options with ${client1} and Group1 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY}

# Opens contact card of one user
    Open Contact Card with ${client1} and groups and ${user02.first_name} ${user02.last_name}

# Verifies that contact card is opened
    Verify Contact Card with ${client1} and present and ${user02.first_name} ${user02.last_name} 

# Verifies that all the users added to Favorite are present in Favorite group
    Check Favorite Symbol with ${client1} and true and ${user02.first_name} ${user02.last_name}
    Check Favorite Symbol with ${client1} and true and ${user03.first_name} ${user03.last_name}
    Check Favorite Symbol with ${client1} and true and ${user04.first_name} ${user04.last_name}
    Check Favorite Symbol with ${client1} and true and ${user05.first_name} ${user05.last_name}

# Verifies that users added to Group2 are present
    Select Group Options with ${client1} and Group2 and ${user04.first_name} ${user04.last_name} and ${user05.first_name} ${user05.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY}

# Verifies that all the users added to Favorite are present in Favorites
    Check Favorite Symbol with ${client1} and true and ${user02.first_name} ${user02.last_name}
    Check Favorite Symbol with ${client1} and true and ${user03.first_name} ${user03.last_name}
    Check Favorite Symbol with ${client1} and true and ${user04.first_name} ${user04.last_name}
    Check Favorite Symbol with ${client1} and true and ${user05.first_name} ${user05.last_name}

# Verifies that users added to Group1 are present
    Select Group Options with ${client1} and Group1 and ${user02.first_name} ${user02.last_name} and ${user03.first_name} ${user03.last_name} and ${EMPTY} and ${EMPTY} and ${EMPTY}

# Remove users from favorites
    Add Or Delete To Favorite Group with ${client1} and ${user02.first_name}**${user02.last_name} and remove
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user03.first_name}**${user03.last_name} and remove
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user04.first_name}**${user04.last_name} and remove
    Close Panel with ${client1} and second_search
    Add Or Delete To Favorite Group with ${client1} and ${user05.first_name}**${user05.last_name} and remove
