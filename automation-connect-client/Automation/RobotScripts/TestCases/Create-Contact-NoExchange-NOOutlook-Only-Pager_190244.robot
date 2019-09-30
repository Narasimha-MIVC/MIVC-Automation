*** Settings ***
Documentation     Create-Contact-NoExchange-NOOutlook-Only-Pager
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
Create-Contact-NoExchange-NOOutlook-Only-Pager
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

#Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}

# Select the checkbox for not opening the outlook for contact creation
    Open Outlook Tab with ${client1}
    Configure Outlook Tab with ${client1} and contacts and check

# User Opens new contact page and verifies the fields
# Adds Pager number
# User Fills first name and last name for creating new contact
    Create New Contact with ${client1} and 1 and Pager and 04087890653 and First11 and Last11 and ${Empty} and ${EMPTY} and ${EMPTY}
    #Close Panel with ${client1} and third
# Checks that newly created contact is displayed under contact page
    Search People Extension with ${client1} and First11**Last11

# Verifies contact information on cantact card    
    Verify Contact Pager Info with ${client1} and present and 04087890653