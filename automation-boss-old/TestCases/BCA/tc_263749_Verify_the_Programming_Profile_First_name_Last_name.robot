*** Settings ***
Documentation    Verify the Programming Profile s first name should be
...  the display name, the last name should be  AA or HG or BCA or User
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
Verify The Fist and Last name on Programming Profile page
    [Tags]    Regression  FAILED

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
    set to dictionary  ${localbcainfo}  AssignFromLocation  Don't assign a number
    ### Actions:
    #1. Switch to BCA page
    When I switch to "bridged_call_appearances" page
    #2. Add New BCA
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    ${ph_num}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${profile_name}=  Set Variable  &{localbcainfo}[ProfileName]

    #3. Assign a number to BCA on the Phone System-> Phone Number page
    And I switch to "phone_systems_phone_numbers" page
    ${name}=  set variable  ${bca_name}${SPACE}x${extn}
    ${ph_num}=  I assign phone number to bca  Available  ${name}

    #4. check that the BCA is in the Phone System-> Phone Number page
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${ph_num}  Active  Bridged Call Appearance  ${None}  ${True}

    #5. Checking the BCA as Operations -> Primary Partitions -> Profile -> Programming product type
    And I switch to "primary_partition" page
    And I find bca entry on primary partition profile page  ${bca_name}  BCA  ${None}  ${ph_num}  ${True}

    #6. Now delete the BCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  2s

    ### Verifications:
    #7. Again verify the BCA entry on primary partition profile
    And I switch to "primary_partition" page
    And I find bca entry on primary partition profile page  ${bca_name}  BCA  ${None}  ${ph_num}  ${False}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


