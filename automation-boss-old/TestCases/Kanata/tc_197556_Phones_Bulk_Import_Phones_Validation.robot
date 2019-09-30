*** Settings ***
Documentation   TC 197556 Phones Bulk Import Phones Validation
...             dev-Jane Knickle

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 197556 Phones - Bulk Import Phones Validation
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${TC_197556_Account} with ${TC_197556_DecisionMaker} option
    When I switch to "phone_system_phones" page
    And I select a location on the phone system phones page
    And I click the Import button on the phone system phones page
    And I specify the file to be uploaded and then press the Open button    &{file_upload_info}
    And I import the phones into the phones page
    Then I verify the errors in the phones spreadsheet
    Then I close the phone import dialog
    Then I remove the imported phone to clean up

*** Keywords ***
Set Init Env
    ${filePath}=    set variable    ${EXECDIR}${/}Test_files${/}Phone_Import_TC_197556.csv
    ${file_upload_info}=    Create Dictionary
    Set to Dictionary   ${file_upload_info}     browseButton    Phones_import_browse_button
    Set to Dictionary   ${file_upload_info}     filePath    ${filePath}
    set suite variable   ${file_upload_info}





