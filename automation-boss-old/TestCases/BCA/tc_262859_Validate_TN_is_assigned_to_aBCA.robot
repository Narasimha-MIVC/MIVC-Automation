*** Settings ***
Documentation    Create and Delete Bridged Call Appearances
Suite Teardown    Close The Browsers
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
Validate TN is assigned to aBCA after Save
    [Tags]    Regression  FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    # call the clean up function
    clean up

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}

    ### Actions:
    #1. Create BCA
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}

    ${ph_number}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${profile_name}=  Set Variable  &{localbcainfo}[AssociatedBCAProfile]

    log  ${ph_number}
    log  ${extn}
    log  ${profile_name}
    set to dictionary  ${localbcainfo}  Location  ${locationName}
    And I verify BCA  &{localbcainfo}

    #2. Switch to the phone system -> phone numbers page and assign an available phone number to BCA
    And I switch to "phone_systems_phone_numbers" page
    ${name}=  replace string  ${profile_name}  ${SPACE}  _
    ${bca_name}=  set variable  ${name}_${ph_number[-4:]}${SPACE}x${extn}
    log  ${bca_name}
    ${ph_number}=  I assign phone number to bca  Available  ${bca_name}

    ### Verification:
    #3. Verifying that the number is now in active state and it's assigned to the BCA
    Then I find element on phone number page
    ...  ${ph_number}  Active  Bridged Call Appearance  ${name}  ${True}
    #4. Deleting the BCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  5s
    #5. Again verifying that the number is now in available state now
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${ph_number}  Available  ${None}  ${None}  ${True}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}