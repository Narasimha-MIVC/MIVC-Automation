*** Settings ***
Documentation  TC 195783 Profiles Grid - Unassign Profile

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 195783 Profiles Grid - Unassign Profile - One Profile
    Given I login to Cosmo Account and go to Primary Partition page
    When I switch to "primary_partition_profiles" page
    ${pr_firstName}=    Generate Random String    4    [LETTERS]
    ${pr_lastName}=     Generate Random String    8    [LETTERS]
    ${pr_email}=    Generate Random String    4    [LETTERS]
    ${user_profile1}=    Create Dictionary
    Set to Dictionary   ${user_profile1}     profileLocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile1}     phoneNumberlocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile1}     phoneNumber     random
    Set to Dictionary   ${user_profile1}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user_profile1}     lastName    ${pr_lastName}
    Set to Dictionary   ${user_profile1}     email   ${pr_email}${pr_firstName}@${pr_lastName}.com
    And I add a profile with a TN   &{user_profile1}
    And I switch to "order" page
    ${AddorderID}=             I get the latest orderID
    And I switch to "primary_partition" page
    And I switch to "primary_partition_profiles" page
    And I select one profile in the profile grid     &{user_profile1}
    And I unassign one profile
    And I refresh browser page
    And I switch to "primary_partition_profiles" page
    Then I verify the profile is not in the profile grid        &{user_profile1}
    And I verify the profile is not in the users table               &{user_profile1}
    And I switch to "order" page
    ${CloseorderID}=             I get the latest orderID
    And I verify a close order is created                       ${CloseorderID}                             &{user_profile1}
    And I switch to "services" page
    And I verify a service status is closed         ${AddorderID}
    And I log off

