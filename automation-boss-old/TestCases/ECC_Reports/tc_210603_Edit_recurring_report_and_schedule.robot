*** Settings ***
#   Developer: Afzal Pasha
Documentation    Suite description

#Suite Setup and Teardown
Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Resource  Files
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../ECC_Reports/Variables/ECC_Valirables.robot
Resource          ../../Variables/ContractInfo.robot
Resource          ../../Variables/EnvVariables.robot


#Library  Files
Library         ../../lib/BossComponent.py    browser=${BROWSER}
Library         ../../lib/DirectorComponent.py



*** Test Cases ***
1. Login to Portal as DM and Edit Recurring ECC Report
    [Tags]    ECCReports
    Given I login to ${URL} with ${eccSupervisorUsername} and ${eccSupervisorPassword}
    And I switch to "eccreports" page
    And I select recurring report to edit   &{ReportValues}
    And I click on recurring edit button
    And I verify recurring report details   &{ReportValues}


*** Keywords ***
Set Init Env
    ${unique_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    : FOR    ${key}    IN    @{ReportValues.keys()}
    \    ${updated_val}=    Replace String    ${ReportValues["${key}"]}    {rand_str}    ${unique_str}
    \    Set To Dictionary    ${ReportValues}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${ReportValues["${key}"]}    {type_of_report}    daily
    \    Set To Dictionary    ${ReportValues}    ${key}    ${updated_val}