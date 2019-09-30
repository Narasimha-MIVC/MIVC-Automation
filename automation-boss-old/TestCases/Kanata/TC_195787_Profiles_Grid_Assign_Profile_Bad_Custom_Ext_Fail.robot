*** Settings ***
Documentation  TC 195787 Profiles Grid - Assign Profile with Bad Custom Ext Fail

Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot
Resource    ../../Variables/ErrorStrings.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections



*** Variables ***
# We are making assumptions here with regqards to extension, digits, trunk access digits etc
# We really should create keywords to determine what are valid extension digits
${extension_three_digit_number} =                     333
${extension_five_digit_number} =                      55555
${extension_number_starting_with_op_access} =         0123
${extension_number_starting_with_out_access_digit} =  9991
${extension_number_starting_with_non_digits} =        1*11

# Test case description from AL
#Step 1 Requires a Cosmo Account with an assigned profile with an extension.
#Step 2
#Login to the QA Portal, switch accounts to the Cosmo account, and navigate to Operations > IP PBX > Primary Partitions > Profiles tab.The Profiles grid displays.
#Step 3*** Keywords ***
#Note the extension of another profile.
#Step 4
#Click the 'Add' button.
#The Add User wizard displays.
#Step 5
#Check the checkbox next to the Extension, and enter the other profile's extension in the extension field.

#You should get an error message that states that the extension is not valid.
#Step 6
#Change the extention to a random 3 digit number.
#You should get an error message that states that the extension is too short.

#Step 7
#Change the extension to a random 5 digit number.
#You should get an error message that states that the extension is not valid.
#Step 9
#Enter an extension with a letter or a special character.
#An error displays saying 'Please enter only digits'.
#Step 10
#Enter an extension that starts with a 0 and then one with a 9.
#It displays an error that says the extension is not valid.
#Step 11
#Click the 'Cancel' button.
#The Numbers grid reloads without any additional profiles.

*** Test Cases ***
TC 195787 Profiles Grid - Assign Profile with Bad Custom Ext Fail
    Given I login to Cosmo Account and go to Primary Partition page
    And I switch to "primary_partition_profiles" page

    ${extension_duplicate_number} =  I select an existing extension from current profile
    When I populate a new profile to add          &{user_profile_data}

    # extension validation is generic, these checks are done in multiple test cases so
    # it would be nice to generalize this into a generic keyword that can be used
    # for various extension elements
    And I Enter an invalid profile extension   ${extension_three_digit_number}
    Then I verify the profile extension error message  ${ERR_EXT_TOO_SHORT}

    And I enter an invalid profile extension   ${extension_five_digit_number}
    Then I verify the profile extension error message  ${ERR_EXT_IN_USE_OR_NOT_VALID}

    And I enter an invalid profile extension   ${extension_duplicate_number}
    Then I verify the profile extension error message  ${ERR_EXT_IN_USE_OR_NOT_VALID}

    And I enter an invalid profile extension   ${extension_number_starting_with_op_access}
    Then I verify the profile extension error message  ${ERR_EXT_IN_USE_OR_NOT_VALID}

    And I enter an invalid profile extension   ${extension_number_starting_with_out_access_digit}
    Then I verify the profile extension error message  ${ERR_EXT_IN_USE_OR_NOT_VALID}

    And I enter an invalid profile extension   ${extension_number_starting_with_non_digits}
    Then I verify the profile extension error message  ${ERR_EXT_NON_DIGITS}

    And When I cancel out of the add profile wizard
    Then I verify the profile is not in the profile grid  &{user_profile_data}

*** Keywords ***

Set Init Env
    ${pr_firstName}=    Generate Random String    8    [LETTERS]
    ${pr_lastName}=     Generate Random String    8    [LETTERS]
    ${pr_email}=     Generate Random String    4    [LETTERS]
    ${user_profile_data}=    Create Dictionary
    Set to Dictionary   ${user_profile_data}     profileLocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile_data}     phoneNumberlocation     ${ProfileGridLocation}
    Set to Dictionary   ${user_profile_data}     firstName   ${pr_firstName}
    Set to Dictionary   ${user_profile_data}     lastName    ${pr_lastName}
    Set to Dictionary   ${user_profile_data}     email   ${pr_email}${pr_firstName}@${pr_lastName}.com
    Set suite variable  ${user_profile_data}
