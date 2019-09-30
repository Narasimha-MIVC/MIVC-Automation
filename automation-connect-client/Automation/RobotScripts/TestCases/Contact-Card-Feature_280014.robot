*** Settings ***
Documentation     Contact-Card-Feature
...               Aakash
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1
Library           ../../Framework-client/utils/client_utils.py    WITH NAME    clientUtils
Test Teardown       call method      ${client1}      close_browser          

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   
   

*** Test cases ***
Contact-Card-Feature
    ${client1}=  Get library instance      client1   
    ${clientUtils}=  Get library instance      clientUtils
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}

    #Login to the Manhattan Client from ST_Users   
    :FOR  ${Index}  IN RANGE  1  2
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
    \   Cleanup Favorites with ${client1}
    
    #Delete Contact with ${client1} and USER_01 and LAST_01
    #verify contact card from search,directory,group,favourites
    Search People Extension with ${client1} and ${user02.first_name} ${user02.last_name}
    #Sleep     2s
    
    # verify contact card
    Verify Contact Card with ${client1} and present and ${user02.first_name} ${user02.last_name}
    #Sleep     2s
    
    #Close second panel search,third panel
    Close Panel with ${client1} and second_search
    Close Panel with ${client1} and third
    
    #Click on the 1st user in dashboard
    ${firstname}=    Click First User with ${client1} 
    
    # verify contact card of 1st user
    Verify Contact Card with ${client1} and present and ${firstname}
    
    #Close second panel,third panel
    Close Panel with ${client1} and second_search
    Close Panel with ${client1} and third    
    
    Delete Contact with ${client1} and USER_011 and LAST_011
    Close Panel with ${client1} and second_search
         
    # Select the checkbox for not opening the outlook for contact creation   
    Open Outlook Tab with ${client1}
    Configure Outlook Tab with ${client1} and contacts and check
    
    # Opens new contact page and verifies the fields
    Go To New Contact with ${client1}
    
    # Adds Home number in contact details of UserB
    Add Contact Number with ${client1} and 1 and Mobile and 09880689522 
    Add New Number with ${client1}
    Add Contact Number with ${client1} and 2 and Home and 08022579576  
    
    Add Contact Details with ${client1} and USER_011 and LAST_011 and tester@shoretel.com and ${EMPTY} and manhattan_automation and shoretel and ${EMPTY} and ${EMPTY} and ${EMPTY}
    
    #Adding user to favourites
    Add Or Delete To Favorite Group with ${client1} and USER_011 LAST_011 and add 
    
    #Close second panel
    Close Panel with ${client1} and second_search
    
    #Click on people tab
    #Invoke Dashboard Tab with ${client1} and people
    
    # Opens contact card of user from favourites
    Open Contact Card with ${client1} and favorites and USER_011 LAST_011 
    #Sleep     2s
    
    # Verifies that contact card is opened
    Verify Contact Card with ${client1} and present and USER_011 LAST_011 
    Close Panel with ${client1} and third
    Close Panel with ${client1} and second
    
    #removing user from favourites
    Add Or Delete To Favorite Group with ${client1} and USER_011 LAST_011 and remove
    
    #Close second panel
    Close Panel with ${client1} and second_search
    
    #create a group & add user to the group
    Invoke Dashboard Tab with ${client1} and people
    Create New Group with ${client1} and Group11 and save and ${user02.first_name} ${user02.last_name} and ${EMPTY}
    
    # Opens contact card of user from favourites
    Open Contact Card with ${client1} and groups and ${user02.first_name} ${user02.last_name}
    
    # Verifies that contact card is opened
    Verify Contact Card Status And Image with ${client1} and present and yes and yes and ${user02.first_name} ${user02.last_name} 
    
    #Close second panel & third panels
    Close Panel with ${client1} and third
    
    #Search mnhauto5 for opening contact card
    Search People Extension with ${client1} and USER_011 LAST_011 
    #Sleep      2s
    
    # verify contact card
    Verify Dial Button Dropdown with ${client1} and 09880689522 and 08022579576
    
    Logout with ${client1} and 0
    
    
    
    
    
    
    
    
    
    
    
    
    
    