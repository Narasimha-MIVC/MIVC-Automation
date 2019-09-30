*** Settings ***
Documentation     MH15_compress_uncompress_dashB_for_workGSuprwsor_verify_WrkGrp_colrChange
...               Indresh Tripathi
Resource          ../variables/Variables.robot
Resource          ../keywords/ManhattanComponentKeywords.robot
Library			  ../../ManhattanLibrary/lib/ManhattanComponent.py      ${port1}          WITH NAME      client1

Test Timeout     4 minutes
Test Teardown    call method      ${client1}      close_browser
*** Variables ***
# Moved to Test Variables file 

*** Keyword ***
Keyword 1
    [Arguments]       ${client1}   

*** Test cases ***
MH15_compress_uncompress_dashB_for_workGSuprwsor_verify_WrkGrp_colrChange
    ${client1}=  Get library instance      client1

    Run Keyword If  ${conf.user_provision} == 1  Keyword 1   ${client1}
    #Sleep     2s
# Login to the Manhattan Client from ST_Users   
    Login with ${client1} and ${user02.client_id} and ${user02.client_password} and ${user02.server}

# check all the tab present in the dashboard as people, recent, event, workgroup.
    Tab Check People Recent Event Workgroup with ${client1} and People
    Tab Check People Recent Event Workgroup with ${client1} and Recent
    Tab Check People Recent Event Workgroup with ${client1} and Event
    Tab Check People Recent Event Workgroup with ${client1} and WorkGroup
                        
# compressed the dashboard and verify it
    Compress Uncompress Dashboard with ${client1} and compress and ${EMPTY}
    Compress Uncompress Dashboard with ${client1} and check and compressed
           
# select login option inside workgroup tab in second panel
    Invoke Dashboard Tab with ${client1} and workgroups
    Handle Workgroup Login with ${client1} and yes and yes and ${Workgroup01.first_name}

# select wrapUp option in workgroup tab in second panel
    Workgroup Verify Select WrapUp with ${client1} and select
    Verify CompUncmp Workgroup Icon ${client1} and compressed and yellow

# Workgroup Logout
    Handle Workgroup Logout with ${client1}
    Handle Workgroup Logout with ${client1}

# compress/uncompress the dashboard and verify it
    Compress Uncompress Dashboard with ${client1} and uncompress and ${EMPTY}
    Compress Uncompress Dashboard with ${client1} and check and uncompressed