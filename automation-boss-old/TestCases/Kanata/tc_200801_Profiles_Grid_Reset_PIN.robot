*** Settings ***
Documentation   TC 200801 Profiles Grid Reset PIN
...             dev-Jane Knickle

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 200801 Profiles Grid - Reset PIN
    Given I login to Cosmo Account and go to Primary Partition page
    When I switch to "primary_partition_profiles" page
    And I add a profile with a TN   &{user_profile1}
    Then I verify the profile is in the profile grid  &{user_profile1}

    #Select 1 profile and click the reset PIN button
    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridResetPinButton" button
    And I change the phone pin and save it  ${pin1}
    Then I verify the phone pin change was successful   ${pin1}

    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridResetPinButton" button
    And I change the phone pin and save it  1111
    Then I verify the phone pin change was not successful   Enter a valid phone PIN.

    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridResetPinButton" button
    And I change the phone pin and save it  369
    Then I verify the phone pin change was not successful   Please enter at least 4 characters.

    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridResetPinButton" button
    And I change the phone pin and save it  28393827634568767
    Then I verify the phone pin change was not successful   Please enter not more than 16 characters.

    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridResetPinButton" button
    And I change the phone pin and save it  abcd
    Then I verify the phone pin change was not successful   Enter a valid phone PIN.

    And I change the phone pin and save it  ${pin2}
    Then I verify the phone pin change was successful   ${pin2}

    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridResetPinButton" button
    And I change the phone pin and save it  default
    Then I verify the phone pin change was successful   default

    Then I clean up by deleting the created profile     &{user_profile1}

*** Keywords ***
Set Init Env
    ${pr_firstName1}=    Generate Random String    4    [LETTERS]
    ${pr_lastName1}=     Generate Random String    8    [LETTERS]
    ${pr_email1}=    Generate Random String    4    [LETTERS]
    ${user_profile1}=    Create Dictionary
    Set to Dictionary   ${user_profile1}     profileLocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile1}     phoneNumberlocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile1}     phoneNumber     random
    Set to Dictionary   ${user_profile1}     firstName   autotest${pr_firstName1}
    Set to Dictionary   ${user_profile1}     lastName    ${pr_lastName1}
    Set to Dictionary   ${user_profile1}     email      ${pr_email1}${pr_firstName1}@${pr_lastName1}.com
    set suite variable  ${user_profile1}

    ${pin1}=     Generate Random String    4    [NUMBERS]
    set suite variable  ${pin1}

    ${pin2}=     Generate Random String    4    [NUMBERS]
    set suite variable  ${pin2}