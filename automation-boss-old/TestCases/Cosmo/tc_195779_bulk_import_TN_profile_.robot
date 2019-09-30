*** Settings ***
Documentation    1. Bulk import csv file of TN profile on  Operations > IP PBX > Primary Partitions > Profiles tab
...              2. Verify that the TN profile is present on profile tab as well as phone systems->user

#...               Priyanka
#...               Comments:

Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
#Variables          Variables/BCA_Variables.py

#BOSS Component
Library           ../../lib/BossComponent.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
Bulk import csv file of TN profile
    [Tags]    Sanity-phase2

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    When I switch to "primary_partition" page
    And I move to "Profiles" tab
    And I click the Import button on the primary partitions profiles page
    Then I verify the Import Profiles form is displayed
    And I specify the file to be uploaded and then press the Open button    &{file_upload_info}
    And I import the profiles into the preview view
    And I import the previewed profiles
    And I refresh browser page
    Then I verify that the profiles are imported into the profiles grid     @{profiles_from_file}
    Then I verify that the new users are found in the users grid     @{profiles_from_file}
    Then I clean up by deleting all the created profiles     @{profiles_from_file}
    [Teardown]
    Run Keywords  I log off
    ...           I check for alert
    ...           Close The Browsers


*** Keywords ***

Set Init Env
    ${filePath}=    set variable    ${EXECDIR}${/}Test_files${/}Profiles_Import_TC_195779.csv
    ${file_upload_info}=    Create Dictionary
    Set to Dictionary   ${file_upload_info}     browseButton    ImportBrowseButton
    Set to Dictionary   ${file_upload_info}     filePath    ${filePath}
    set suite variable  ${file_upload_info}

    ${profiles_from_file}=  Read Profiles from File     ${filePath}
    set suite variable  ${profiles_from_file}