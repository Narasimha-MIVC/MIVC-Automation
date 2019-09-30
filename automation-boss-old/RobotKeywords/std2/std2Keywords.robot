*** Settings ***
Documentation    Keyword supported for the BCA feature of BOSS


Library    Collections

Resource  administration/administrationKeywords.robot
Resource  maintenance/maintenance.robot

*** Keywords ***

I switch to "${page:[^"]+}" page on std2
    run keyword  switch to page  ${page}

I switch tab on browser
    [Arguments]  ${login_info}
    ${status}=      Run Keyword     switch to tab    ${login_info}

I checked the topology
    run keyword  test_topology_page_component