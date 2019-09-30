*** Settings ***
Documentation     MH_Start_Contact_Search_by_Last_Name_and_then_Cancel_Search
...               Bhupendra Parihar
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library           String
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py        ${port1}          WITH NAME      client1 
Test Timeout      2 minutes
Test Teardown     call method      ${client1}      close_browser

*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1} 

*** Test cases ***
MH_Start_Contact_Search_by_Last_Name_and_then_Cancel_Search
    ${client1}=  Get library instance      client1
    ${firstCharOfLastName}=  Get Substring      ${user02.last_name}    0    1
    
    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
   
    # # Login to Client A
	Login with ${client1} and ${user01.client_id} and ${user01.client_password} and ${user01.server}
    
    Type Value In Extension Search with ${client1} and ${firstCharOfLastName}

    Press Key with ${client1} and DOWN and 2

    Scroll Search Extension Result with ${client1}

    Press Escape with ${client1} and search_extension

    Verify Search People List Closed with ${client1}