*** Settings ***
Documentation    Add BCA with default Outbound caller Id or with no options from the select dropdown "'Select Phone Number…'"
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
Create BCA With Default Outbound Call Id
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    ${bca_name}=  generate_bca_name

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2. Create the BCA with default outbound caller Id
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  2s
    ### Verification:
    Then I verify BCA  &{localbcainfo}

    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}