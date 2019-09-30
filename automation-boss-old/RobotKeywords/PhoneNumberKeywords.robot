*** Settings ***
Documentation     Keywords supported for Phone Numbers in the Phone System tab in the portal
...               dev- Megha , Tantri Tanisha
...               Comments:

Library    Collections

*** Keywords ***
I create DNIS with Save
    [Documentation]  This keyword will help user to create DNIS in phone numbers  page.
    [Arguments]    &{PhoneNumber_operation}
    ${result}    ${selectedTn}  ${selectedDestType}=  run keyword    create_DNIS_with_Save    &{PhoneNumber_operation}
    Should be true  ${result}
    [Return]      ${selectedTn}     ${selectedDestType}

I create DNIS with Cancel
    [Documentation]  This keyword will help user to set information to create DNIS with cancel in phone numbers  page.
    [Arguments]    &{PhoneNumber_operation}
    ${result}=  run keyword    create_DNIS_with_Cancel    &{PhoneNumber_operation}
    Should be true  ${result}

I select number for Edit
    [Documentation]  This keyword will help user to select a number for edit in phone numbers  page.
    [Arguments]    &{PhoneNumber_operation}
    run keyword    select_number_for_Edit    &{PhoneNumber_operation}

I verify PhoneNumber Operation
    [Documentation]  This keyword will help user to verify assign window in phone numbers  page.
    [Arguments]    &{PhoneNumber_operation}
    ${result}=  run keyword    verify_PhoneNumber_Operation    &{PhoneNumber_operation}
    Should be true  ${result}

I verify PhoneNumber Operation for Edit
    [Documentation]  This keyword will help user to verify edit window in phone numbers  page.
    [Arguments]    &{PhoneNumber_operation}
    ${result}=  run keyword    verify_PhoneNumber_Operation_for_Edit    &{PhoneNumber_operation}
    Should be true  ${result}

I refresh grid
    [Documentation]  This keyword will help user to refresh grid in phone numbers  page.
    run Keyword    refresh_grid

I verify Destination Type of ${selectedTn}
     [Documentation]  This keyword will help user to verify Destination type of DNIS created in phone numbers  page.
     ${result}=  run keyword    verify_destination_type     ${selectedTn}    &{PhoneNumber_Assign_BCA}
     Should be true   ${result}

I verify Destination ${selectedDestType} and Status of ${selectedTn}
     [Documentation]  This keyword will help user to verify Destination name and status of the created DNIS in phone numbers  page.
     ${result}=  run keyword    verify_destination_and_status     ${selectedTn}    ${selectedDestType}     &{PhoneNumber_Assign_BCA}
     Should be true   ${result}

I verify availability of tns of ${locList}
     [Documentation]  This keyword will help to verify availability of TNs of the countryList
     ${result}=  run keyword    verify_available_tns     ${locList}
     Should be true   ${result}
