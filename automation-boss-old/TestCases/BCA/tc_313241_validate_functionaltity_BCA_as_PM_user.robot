*** Settings ***
Documentation    Validate functionaltity BCA as PM user
...               dev-Vasuja
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
Validate functionaltity BCA with PM user
    [Tags]    Regression    Sanity_Phase2

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  5s

    # call the clean up function
    #clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}

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
    ${ph_number}=  I assign phone number to bca  Available  ${bca_name}

    ### Verification:
    #3. Verifying that the number is now in active state and it's assigned to the BCA
    Then I find element on phone number page
    ...  ${ph_number}  Active  Bridged Call Appearance  ${None}  ${True}
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