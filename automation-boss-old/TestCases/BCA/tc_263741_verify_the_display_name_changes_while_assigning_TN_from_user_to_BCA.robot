*** Settings ***
Documentation    Verify the display name changes while assigning TN from user to BCA
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
Verify the display name changes while assigning TN from user to BCA
    [Tags]    Regression  FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    # call the clean up function
    clean up

    #1. Find a global phone number in availabl  e state and assign it to a user
    When I switch to "phone_systems_phone_numbers" page
    ${ph_number}=  I assign phone number to user  Available  Global Inbound

    #2. The phone number should be in active state now
    And I find element on phone number page
    ...  ${ph_number}  Active  ${None}  ${None}  ${True}  Global Inbound

    #3. Create a BCA
    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    And I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    ${extn}=  Set Variable  &{localbcainfo}[Extension]

    #4. Switch to the phone system -> phone numbers page and edit the above DNIS to BCA
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page
    ...  ${ph_number}  Active  User  ${None}  ${True}  Global Inbound
    ${bca_name}=  set variable  ${bca_name}${SPACE}x${extn}

    log  ${bca_name}

    set to dictionary  ${localbcainfo}  bridged_Call_Appearance_name  ${bca_name}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}

    #5. verify that the number is now in active state now and destination type as BCA
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page
    ...  ${ph_number}  Active  Bridged Call Appearance
    ...  ${None}  ${True}  Global Inbound

    #6. Delete the BCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  2s

    #### Verification
    #7. Again verifying that the number is now in available state now
    Then I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${ph_number}  Available  ${None}  ${None}  ${True}  Global Inbound

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert


*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}