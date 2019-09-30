*** Settings ***
Documentation    Verify the Edit page of aBCA
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
Verify UI of Edit page for aBCA
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

    set to dictionary  ${localbcainfo}  AssociatedBCAProfile  &{localbcainfo}[AssociatedBCAProfile]
    set to dictionary  ${localbcainfo}  SelectPhoneNumber  &{localbcainfo}[SelectPhoneNumber]
    set to dictionary  ${localbcainfo}  AssociatedBCAExtn  &{localbcainfo}[Extension]
    set to dictionary  ${localbcainfo}  Location  ${locationName}

    And I verify BCA  &{localbcainfo}

    ### Verifications:
    #3. Verify the Edit aBCA page
#    Then I switch to "bridged_call_appearances" page
    And I verify edit bca page  &{localbcainfo}

    [Teardown]  run keywords  I delete BCA  ${localbcainfo}
    ...         AND  sleep  2s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


