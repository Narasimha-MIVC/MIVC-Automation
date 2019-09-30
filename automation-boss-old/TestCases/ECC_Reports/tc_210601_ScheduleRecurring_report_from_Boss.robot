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
1. Login to Portal as DM and Schedule a Recurring ECC Report
    [Tags]    ECCReports
    Given I login to ${URL} with ${eccSupervisorUsername} and ${eccSupervisorPassword}
    And I switch to "eccreports" page
    And I Click on recurring report add button
    And I enter all field values   &{ReportValues}
    And I click on next page
    And I select entities
    And I click on next page
    And I choose report type as daily weekly monthly or one time basis   &{ReportValues}
    And I click on next page
    And I select date and time format
    And I click on next page
    And I select report format and file type   &{ReportValues}
    And I click on next page
    And I enter report delivery details   &{ReportValues}
    And I click on Report finish button
    And I Verify Recurring Report exits   &{ReportValues}


*** Keywords ***
Set Init Env
    ${unique_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    : FOR    ${key}    IN    @{ReportValues.keys()}
    \    ${updated_val}=    Replace String    ${ReportValues["${key}"]}    {rand_str}    ${unique_str}
    \    Set To Dictionary    ${ReportValues}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${ReportValues["${key}"]}    {type_of_report}    daily
    \    Set To Dictionary    ${ReportValues}    ${key}    ${updated_val}