*** Settings ***
Documentation   TC 195786 Profiles Grid - Assign Profile with an auto assigned Extension
...             dev-Jane Knickle

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 195786 Profiles Grid - Assign Profile with an auto assigned Extension
    Given I login to Cosmo Account and go to Primary Partition page
    When I switch to "primary_partition_profiles" page
    And I add a profile with an auto assigned extension   &{user_profile}
    Then I verify the profile is in the profile grid  &{user_profile}
    Then I verify the profile is added to the users table   &{user_profile}
    Then I clean up by deleting the created profile that has no TN    &{user_profile}

*** Keywords ***
Set Init Env
    ${pr_firstName}=    Generate Random String    4    [LETTERS]
    ${pr_lastName}=     Generate Random String    8    [LETTERS]
    ${pr_email}=    Generate Random String    4    [LETTERS]
    ${user_profile}=    Create Dictionary
    Set to Dictionary   ${user_profile}     profileLocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user_profile}     lastName    ${pr_lastName}
    Set to Dictionary   ${user_profile}     email   ${pr_email}${pr_firstName}@${pr_lastName}.com
    Set to Dictionary   ${user_profile}     autoExtn    True
    set suite variable  ${user_profile}