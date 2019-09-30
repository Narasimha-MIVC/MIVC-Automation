*** Settings ***
Documentation    Create aBCA and verify the aBCA Edit page title
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
Validate Edit aBCA Page
    [Tags]    Regression  Functional

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    &{bcainfo}=  copy dictionary  ${BCA_INFO}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page

    #2.  Create an Associated BCA
    ${profile_name}=  get required abca profile  ${PMUser}
    set to dictionary  ${bcainfo}  AssociatedBCAProfile  ${profile_name}
    set to dictionary  ${bcainfo}  AssociatedBCA  ${True}
    set to dictionary  ${bcainfo}  Location  ${locationName}
    log  ${profile_name}

    And I create Bridged Call Appearance  ${bcainfo}
    sleep  2s

    ### Verification: verifying the copy BCA page of an already created aBCA
    @{name}=  split string from right  ${profile_name}  ${SPACE}-${SPACE}
    set to dictionary  ${bcainfo}  AssociatedBCAProfile  @{name}[1]
    Then I verify BCA  &{bcainfo}
    And I verify copy bca page  &{bcainfo}

    [Teardown]  run keywords  I delete BCA  ${bcainfo}
    ...         AND  sleep  2s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}