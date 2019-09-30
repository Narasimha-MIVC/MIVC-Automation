*** Settings ***
Documentation  Profile Reassign Extension Validation (tc 200813)

Suite Setup       Set Init Env

Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}

#Built in library
Library  String

*** Test Cases ***
Profile Reassign Extension Validation (tc 200813)

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option

    When I open Operations IP PBX Primary Partition
    Then I verify Profiles grid display

    When I select a profile &{Product}
    @{profileData}=  and I get first record from profile
    and I click on ReAssign button

    Then I verify reassign wizard is displayed
    and I verify error message ${error_message_for_three_digit_number} when I enter extension ${extension_three_digit_number}
    and I verify error message ${error_message_for_five_digit_number} when I enter extension ${extension_five_digit_number}
    ${extension_duplicate_number} =  Set Variable  @{profileData}[${extension_index_in_profile_record}]
    and I verify error message ${error_message_for_duplicate_number} when I enter extension ${extension_duplicate_number}
    and I verify error message ${error_message_for_number_starting_with_zero} when I enter extension ${extension_number_starting_with_zero}
    and I verify error message ${error_message_for_number_starting_with_nine} when I enter extension ${extension_number_starting_with_nine}

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${Product}=    Create Dictionary
    Set to Dictionary   ${Product}     product    MiCloud Connect Essentials
    Set to Dictionary   ${Product}     minNumber   1
    Set suite variable    &{Product}

    # Note: Error message does not match testcase.
    ${error_message_for_three_digit_number}=    set variable    Extension is too short.
    Set suite variable    ${error_message_for_three_digit_number}
    ${extension_three_digit_number}=    set variable    333
    Set suite variable    ${extension_three_digit_number}
    # Note: Error message does not match testcase.
    ${error_message_for_five_digit_number}=    set variable     Extension is in use or not valid.
    Set suite variable    ${error_message_for_five_digit_number}
    ${extension_five_digit_number}=    set variable     55555
    Set suite variable    ${extension_five_digit_number}
    # Note: Error message does not match testcase.
    ${error_message_for_duplicate_number}=    set variable  Extension is in use or not valid.
    Set suite variable    ${error_message_for_duplicate_number}
    ${extension_index_in_profile_record}=    set variable   4
    Set suite variable    ${extension_index_in_profile_record}
    ${error_message_for_number_starting_with_zero}=    set variable     Extension is in use or not valid.
    Set suite variable    ${error_message_for_number_starting_with_zero}
    ${extension_number_starting_with_zero}=    set variable     0123
    Set suite variable    ${extension_number_starting_with_zero}
    ${error_message_for_number_starting_with_nine}=     set variable      Extension is in use or not valid.
    Set suite variable    ${error_message_for_number_starting_with_nine}
    ${extension_number_starting_with_nine}=    set variable     9123
    Set suite variable    ${extension_number_starting_with_nine}
