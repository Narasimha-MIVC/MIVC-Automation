*** Settings ***
Documentation   TC 200802 Profiles Grid - Edit
...             dev-Jane Knickle

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 200802 Profiles Grid - Edit
    Given I login to Cosmo Account and go to Primary Partition page
    When I switch to "primary_partition_profiles" page
    And I add a profile with a TN   &{user_profile1}
    Then I verify the profile is in the profile grid  &{user_profile1}

    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I add a profile with a TN   &{user_profile2}
    Then I verify the profile is in the profile grid  &{user_profile2}

    #Select 1 profile and click the edit button
    Then I refresh browser page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I click the "partitionProfilesDataGridEditButton" button
    Then I verify "personGeneralDetails" contains "${pr_lastName1}"

    # Select 2 profiles and click the edit button
    Then I switch to "primary_partition" page
    And I switch to "primary_partition_profiles" page
    And I select multiple profiles in the profile grid     @{profile_list}
    And I click the "partitionProfilesDataGridEditButton" button
    Then I verify "editProfilesForm" contains "Edit Profiles"
    And I click the "editProfilesFormCancelButton" button

    #Select 1 profile and click the edit button
    Then I refresh browser page
    Then I switch to "primary_partition" page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid    &{user_profile2}
    And I click the "partitionProfilesDataGridEditButton" button
    Then I verify "personGeneralDetails" contains "${pr_lastName2}"

    Then I clean up by deleting the created profile     &{user_profile1}
    Then I clean up by deleting the created profile     &{user_profile2}

*** Keywords ***
Set Init Env
    # create profile 1
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
    set suite variable  ${pr_lastName1}

    # create profile 2
    ${pr_firstName2}=    Generate Random String    4    [LETTERS]
    ${pr_lastName2}=     Generate Random String    8    [LETTERS]
    ${pr_email2}=    Generate Random String    4    [LETTERS]
    ${user_profile2}=    Create Dictionary
    Set to Dictionary   ${user_profile2}     profileLocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile2}     phoneNumberlocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile2}     phoneNumber     random
    Set to Dictionary   ${user_profile2}     firstName   autotest${pr_firstName2}
    Set to Dictionary   ${user_profile2}     lastName    ${pr_lastName2}
    Set to Dictionary   ${user_profile2}     email   ${pr_email2}${pr_firstName2}@${pr_lastName2}.com
    set suite variable  ${user_profile2}
    set suite variable  ${pr_lastName2}

    @{profile_list}=    Create List     ${user_profile1}   ${user_profile2}
    set suite variable  @{profile_list}