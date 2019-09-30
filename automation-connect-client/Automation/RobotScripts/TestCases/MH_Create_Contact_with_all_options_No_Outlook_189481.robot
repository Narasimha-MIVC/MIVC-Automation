*** Settings ***
Documentation     MH_Create_Contact_with_all_options_No_Outlook
...               Aakash
...               Comments:
Default Tags        tc-Suite
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}           WITH NAME      client1
Test Timeout        5 minutes
Test Teardown      call method      ${client1}      close_browser     

*** Variables ***
# Moved to Test Variables file 

*** Keywords ***	     
Keyword 1
    [Arguments]       ${client1}   
    Log   ${client1}
    
*** Test Cases ***
MH_Create_Contact_with_all_options_No_Outlook   
    ${client1}=     Get library instance      client1          
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}   

    #Login to the Manhattan Client from ST_Users/MT_Users   
    :FOR  ${Index}  IN RANGE  1  2
    \   Login with ${client${Index}} and ${user0${Index}.client_id} and ${user0${Index}.client_password} and ${user0${Index}.server}
   
    Delete Contact with ${client1} and USER_022 and LAST_022
    Close Panel with ${client1} and second_search
    
    # Select the checkbox for not opening the outlook for contact creation   
    Open Outlook Tab with ${client1}
    Configure Outlook Tab with ${client1} and contacts and check
    
    # Opens new contact page and verifies the fields
    Go To New Contact with ${client1}
    
    # Adds Home number in contact details of UserB
    Add Contact Number with ${client1} and 1 and Mobile and 9742883712  
    Add Contact Number with ${client1} and 2 and Home and 9880689522  
    Add Contact Number with ${client1} and 3 and Business and 0120945673  
    Add Contact Number with ${client1} and 4 and Fax and 01207890653 
    Add Contact Number with ${client1} and 5 and Pager and 9456094381 
    
    # Adds contact details
    Add Contact Details with ${client1} and USER_022 and LAST_022 and tester@shoretel.com and ${EMPTY} and manhattan_automation and shoretel and ${EMPTY} and ${EMPTY} and ${EMPTY}
    
    # Searches the newly created contact
    Search People Extension with ${client1} and USER_022 LAST_022
    
    # Close the Manhattan Client 
    # Close Application with ${client1}