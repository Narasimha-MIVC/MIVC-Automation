*** Settings ***
Documentation     Keywords supported for ECC portal
...               developer- Afzal Pasha
...               Comments:

Library    Collections


*** Keywords ***
I click on eccactivate button
    [Arguments]    &{Settings}
    run keyword  ecc_activate_click    &{Settings}

I click on eccreview button
    [Arguments]    &{Settings}
    run keyword  ecc_activate_review_click    &{Settings}

I click on OK button of ECC Activate_Submit
    run keyword  ecc_ok_click

I click on recurring tab button
    run keyword  report_recurring_tab_click

I click on onetime tab button
    run keyword  report_onetime_tab_click

I Click on recurring report add button
    run keyword  recurring_report_add_click

I Click on onetime report add button
    run keyword  onetime_report_add_click

I enter all field values
    [Arguments]    &{ReportValues}
    run keyword  report_enter_fieldvalues    &{ReportValues}

I select entities
    run keyword  report_select_entities

I choose report type as daily weekly monthly or one time basis
    [Arguments]    &{ReportValues}
    run keyword  report_select_reporttype    &{ReportValues}

I select date and time format
    run keyword  report_select_datetime

I select report format and file type
    [Arguments]    &{ReportValues}
    run keyword  report_select_formatfile    &{ReportValues}

I enter report delivery details
    [Arguments]    &{ReportValues}
    run keyword  report_enter_delivery_details    &{ReportValues}

I click on next page
    run keyword  report_next_click

I click on Report finish button
    ${result}=      run keyword  report_finish_click
    should be true   ${result}

I Verify Recurring Report exits
    [Arguments]    &{ReportValues}
    run keyword  recurring_report_exists_check    &{ReportValues}

I Verify OneTime Report exits
    [Arguments]    &{ReportValues}
    run keyword  onetime_report_exists_check    &{ReportValues}

I select recurring report to edit
    [Arguments]    &{ReportValues}
    run keyword  select_recurring_report_to_edit    &{ReportValues}

I select onetime report to edit
    [Arguments]    &{ReportValues}
    run keyword  select_onetime_report_to_edit    &{ReportValues}

I click on recurring edit button
    run keyword  recurring_report_edit_click

I click on onetime edit button
    run keyword  onetime_report_edit_click

I select recurring report to delete
    [Arguments]    &{ReportValues}
    run keyword  select_recurring_report_to_delete    &{ReportValues}

I select onetime report to delete
    [Arguments]    &{ReportValues}
    run keyword  select_onetime_report_to_delete    &{ReportValues}

I click on recurring delete button to delete report
    ${result}=      run keyword  recurring_report_delete_click
    should be true   ${result}

I click on onetime delete button to delete report
    run keyword  onetime_report_delete_click

I verify recurring report details
    [Arguments]    &{ReportValues}
    ${result}=      run keyword  recurring_report_verification    &{ReportValues}
    should be true   ${result}

I verify onetime report details
    [Arguments]    &{ReportValues}
    ${result}=      run keyword  onetime_report_verification    &{ReportValues}
    should be true   ${result}

I select recurring report to copy
    [Arguments]    &{ReportValues}
    run keyword  select_recurring_report_to_copy    &{ReportValues}

I select onetime report to copy
    [Arguments]    &{ReportValues}
    run keyword  select_onetime_report_to_copy    &{ReportValues}

I click on recurring copy button
    run keyword  recurring_report_copy_click

I click on onetime copy button
    run keyword  onetime_report_copy_click

I click on recurring copy button by giving report name
    [Arguments]    &{ReportValues}
    ${result}=      run keyword  recurring_report_copy_click_by_giving_report_name    &{ReportValues}
    should be true   ${result}

I click on onetime copy button by giving report name
    [Arguments]    &{ReportValues}
    ${result}=      run keyword  onetime_report_copy_click_by_giving_report_name    &{ReportValues}
    should be true   ${result}

I select recurring report to edit after copy
    [Arguments]    &{ReportValues}
    run keyword  select_recurring_report_to_edit_after_copy    &{ReportValues}

I select onetime report to edit after copy
    [Arguments]    &{ReportValues}
    run keyword  select_oneTime_Report_to_edit_after_copy    &{ReportValues}