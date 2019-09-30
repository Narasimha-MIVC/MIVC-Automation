*** Settings ***
Documentation   TC 202292 Profiles Grid - Bulk Import Extension Only Profiles
...             dev-Jane Knickle

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 202292 Profiles Grid - Bulk Import Extension Only Profiles
    Given I login to Cosmo Account and go to Primary Partition page
    When I switch to "primary_partition_profiles" page
    And I click the Import button on the primary partitions profiles page
    Then I verify the Import Profiles form is displayed
    And I specify the file to be uploaded and then press the Open button    &{file_upload_info}
    And I import the profiles into the preview view
    And I import the previewed profiles
    And I refresh browser page
    Then I verify that the profiles are imported into the profiles grid     @{profiles_from_file}
    Then I verify that the new users are found in the users grid     @{profiles_from_file}
    Then I clean up by deleting all the created profiles     @{profiles_from_file}

*** Keywords ***
Set Init Env
    ${filePath}=    set variable    ${EXECDIR}${/}Test_files${/}Profiles_Import_TC_202292.csv
    ${file_upload_info}=    Create Dictionary
    Set to Dictionary   ${file_upload_info}     browseButton    ImportBrowseButton
    Set to Dictionary   ${file_upload_info}     filePath    ${filePath}
    set suite variable  ${file_upload_info}

    ${profiles_from_file}=  Read Profiles from File     ${filePath}
    set suite variable  ${profiles_from_file}