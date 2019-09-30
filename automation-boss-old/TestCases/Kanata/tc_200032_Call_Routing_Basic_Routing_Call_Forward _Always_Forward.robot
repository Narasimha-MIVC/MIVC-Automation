*** Settings ***
Documentation  TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority
    Given I login and switch to account AutoTest_Acc_3Dg532wA
    and I switch to "primary_partition" page
    When I switch to "primary_partition_profiles" page
    # Create user 1
    Log    ${user1_properties}    console=yes
    And I add a profile with an auto assigned extension   &{user1_properties}
    And I verify the profile is in the profile grid  &{user1_properties}
    And I verify the profile is added to the users table   &{user1_properties}
    When I open Call Routing for user ${pr_email}
    and I configure always forward to voicemail
    and I verify always forward to voicemail is configured
#    Then I log off

*** Keywords ***
Set Init Env
    ${pr_firstName}=    set variable    FNtestuser1
    ${pr_lastName}=     set variable    LNtestuser1
    ${pr_email}=    set variable    email${pr_firstName}@${pr_lastName}.com
    Set suite variable    ${pr_email}
    ${user1_properties}=    Create Dictionary
    Set suite variable    &{user1_properties}
    Set to Dictionary   ${user1_properties}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user1_properties}     lastName    ${pr_lastName}
    Set to Dictionary   ${user1_properties}     email   ${pr_email}
    Set to Dictionary   ${user1_properties}     profileLocation     AutoTest_location_3Dg532wA
    Set to Dictionary   ${user1_properties}     autoExtn    True

    ${pr_firstName}=    set variable    FNtestuser2
    ${pr_lastName}=     set variable    LNtestuser2
    ${user2_properties}=    Create Dictionary
    Set suite variable    &{user2_properties}
    Set to Dictionary   ${user2_properties}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user2_properties}     lastName    ${pr_lastName}
    Set to Dictionary   ${user2_properties}     email   email${pr_firstName}@${pr_lastName}.com
    Set to Dictionary   ${user2_properties}     profileLocation     AutoTest_location_3Dg532wA
    Set to Dictionary   ${user2_properties}     autoExtn    True
