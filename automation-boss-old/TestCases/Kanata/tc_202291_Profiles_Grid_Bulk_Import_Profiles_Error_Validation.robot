*** Settings ***
Documentation   TC 202291 Profiles Grid - Bulk Import Profiles Error Validation
...             dev-Jane Knickle

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 202291 Profiles Grid - Bulk Import Profiles Error Validation
    Given I login to Cosmo Account and go to Primary Partition page
    When I switch to "primary_partition_profiles" page
    And I click the Import button on the primary partitions profiles page
    Then I verify the Import Profiles form is displayed
    And I specify the file to be uploaded and then press the Open button    &{file_upload_info}
    And I import the profiles into the preview view
    Then I verify the errors in the profiles spreadsheet

*** Keywords ***
Set Init Env
    ${filePath}=    set variable    ${EXECDIR}${/}Test_files${/}Profiles_Import_TC_202291.csv
    ${file_upload_info}=    Create Dictionary
    Set to Dictionary   ${file_upload_info}     browseButton    ImportBrowseButton
    Set to Dictionary   ${file_upload_info}     filePath    ${filePath}
    set suite variable  ${file_upload_info}




