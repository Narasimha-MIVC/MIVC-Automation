*** Settings ***
Documentation    Verify the display name changes while assigning TN from BCA to User
Suite Teardown    Close The Browsers
#...               dev-Vasuja
#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component

Library           ../../lib/BossComponent.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
Verify the display name changes while assigning TN from BCA to User
    [Tags]    Regression   FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    # call the clean up function
    clean up

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1. Create BCA
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    ${ph_number}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${profile_name}=  Set Variable  &{localbcainfo}[ProfileName]

    #2. Switch to the phone system -> phone numbers page and assign an available phone number to BCA
    And I switch to "phone_systems_phone_numbers" page
    ${bca_name}=  set variable  ${bca_name}${SPACE}x${extn}
    ${ph_number}=  I assign phone number to bca  Available  ${bca_name}  Global${SPACE * 2}Inbound

    #3. Verifying that the number is now in active state and it's assigned to the BCA
    And I find element on phone number page
    ...  ${ph_number}  Active  Bridged Call Appearance  ${None}  ${True}  Global${SPACE * 2}Inbound

    #4. Edit the DNIS
    set to dictionary  ${localbcainfo}  User  ${TRUE}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}

    #5. verify that the number is now in active state now
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${ph_number}  Active  User  ${None}  ${True}  Global${SPACE * 2}Inbound

    #6. Edit the DNIS to destination type as Unassign
    set to dictionary  ${localbcainfo}  Unassign  ${TRUE}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}

    #7. Again verifying that the number is now in available state now
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${ph_number}  Available  -  -  ${True}  Global${SPACE * 2}Inbound

    #8. Deleting the BCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  2s

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}