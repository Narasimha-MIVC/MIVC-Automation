*** Settings ***
Documentation    On the Partition's Profiles grid Re-Assign the TN of a profile, between TN's at the same location.

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../RobotKeywords/BCAKeywords.robot
#Env file
Resource          ../../Variables/EnvVariables.robot

#libraries
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library             String
Library             Collections

*** Test Cases ***
BOSS Login

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And Log Dictionary  ${user_profile}
    log to console  ${created_email}
    And I switch to "switch_account" page
    And I switch to account ${ProfileGridAccount} with ${AccWithoutLogin} option
    And I switch to Primary Partitions page
    And I go to profiles tab on primary partitions page
    And I add a profile with a TN   &{user_profile}
    Then I verify the profile is in the profile grid  &{user_profile}
    And I select one profile in the profile grid     &{user_profile}
    ${created_profile}=  I read a profile in the profile grid  &{user_profile}
    log to console  ${created_profile}
    And I reassign a profile with a TN  &{user_profile}
    And I verify a profile is updated  ${created_email}  &{created_profile}
    And I verify a user profile is updated  ${created_email}   &{created_profile}

*** Keywords ***

Set Init Env

    ${pr_firstName}=    Generate Random String    4    [LETTERS]
    ${pr_lastName}=     Generate Random String    8    [LETTERS]
    ${pr_email}=        Generate Random String    4    [LETTERS]
    ${custom_ext}=      Generate Random String    4    [NUMBERS]
    ${user_profile}=    Create Dictionary
    Set to Dictionary   ${user_profile}     profileLocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile}     phoneNumberlocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile}     phoneNumber     random
    Set to Dictionary   ${user_profile}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user_profile}     lastName    ${pr_lastName}
    Set to Dictionary   ${user_profile}     email   ${pr_email}${pr_firstName}@${pr_lastName}.com
    set suite variable  ${user_profile}
    ${created_email}=  Get from Dictionary  ${user_profile}  email
    set suite variable  ${created_email}
