*** Settings ***
Documentation    Verify Programming Profile in operations page is removed after deleting BCA
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
Verify Programming Profile is removed after deleting aBCA
    [Tags]    Regression  Functional

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
    #1. Switch to BCA page
    When I switch to "bridged_call_appearances" page
    #2. Add New aBCA
    And I create Bridged Call Appearance  ${localbcainfo}

    ${ph_num}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${aBCA_name}=  Set Variable  &{localbcainfo}[AssociatedBCAProfile]

    set to dictionary  ${localbcainfo}  Location  ${locationName}
    And I verify BCA  &{localbcainfo}

    #3. Checking the BCA as Operations -> Primary Partitions -> Profile -> Programming product type
    And I switch to "primary_partition" page
    And I find bca entry on primary partition profile page
    ...  ${aBCA_name}  aBCA  ${extn}  ${ph_num}  ${True}

    #4. Now delete the aBCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  2s

    ### Verifications:
    #5. Again verify the BCA entry on primary partition profile
    And I switch to "primary_partition" page
    And I find bca entry on primary partition profile page
    ...  ${aBCA_name}  aBCA  ${extn}  ${ph_num}  ${False}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


