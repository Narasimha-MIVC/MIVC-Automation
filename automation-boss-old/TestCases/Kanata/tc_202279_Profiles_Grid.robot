*** Settings ***
Documentation  This is a test file to check if your dependency installations

Suite Setup       Set Init Env

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Env file
Resource          ../../Variables/EnvVariables.robot

#libraries
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           Collections

*** Test Cases ***

Profile Grid (tc 202279)
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I open Operations IP PBX Primary Partition
    Then I verify Extension-Only is shown @{ProfileExtension}
    and I verify Extension-and-DID is shown @{ProfileNumber}
    and I verify all column names in Profiles
    and I verify buttons enabled in Profiles @{expectedEnabledButtonsDefault}
    When I select a profile &{Product}
    Then I verify buttons enabled for single profile selection @{expectedEnabledButtonsSingleSection}
    When I select another profile &{Product}
    Then I verify buttons enabled for two profile selection @{expectedEnabledButtonsTwoSections}

    [Teardown]  Run Keywords  I check for alert

*** Keywords ***
Set Init Env
    ${ProfilesExtension_id}=    set variable    ProfilesExtension
    Set suite variable    ${ProfilesExtension_id}

    ${ProfilesNumber_id}=       set variable    ProfilesNumber
    Set suite variable    ${ProfilesNumber_id}

    # Note: This extension is expected as a precondition for Extension-Only profile.
    ${ProfilesExtension_value}=    set variable     1860
    Set suite variable    ${ProfilesExtension_value}

    # Note: This number is expected as a precondition for Extension-and-DID profile.
    ${ProfilesNumber_value}=       set variable     1 (408) 300-5160
    Set suite variable    ${ProfilesNumber_value}

    @{ProfileExtension}=    Create list     ${ProfilesExtension_id}     ${ProfilesExtension_value}
    Set suite variable    @{ProfileExtension}
    @{ProfileNumber}=   Create list        ${ProfilesNumber_id}        ${ProfilesNumber_value}
    Set suite variable    @{ProfileNumber}

    #Note: Product to filter and the mininum number of records needed.
    ${Product}=    Create Dictionary
    Set to Dictionary   ${Product}     product    MiCloud Connect Essentials
    Set to Dictionary   ${Product}     minNumber   2
    Set suite variable    &{Product}

    # Ids of various buttons on the profiles UI.
    @{expectedEnabledButtonsDefault}=      Create list    partitionProfilesDataGridAddButton  partitionProfilesDataGridImportButton   partitionProfilesDataGridExportBtn
    Set suite variable    @{expectedEnabledButtonsDefault}
    @{expectedEnabledButtonsSingleSection}=     Create list    partitionProfilesDataGridResetPinButton  partitionProfilesDataGridUnassignButton  partitionProfilesDataGridReAssignButton  partitionProfilesDataGridAddButton  partitionProfilesDataGridEditButton  partitionProfilesDataGridImportButton  partitionProfilesDataGridExportBtn
    Set suite variable    @{expectedEnabledButtonsSingleSection}
    @{expectedEnabledButtonsTwoSections}=   Create list     partitionProfilesDataGridUnassignButton  partitionProfilesDataGridAddButton  partitionProfilesDataGridEditButton  partitionProfilesDataGridImportButton  partitionProfilesDataGridExportBtn
    Set suite variable    @{expectedEnabledButtonsTwoSections}
