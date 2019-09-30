*** Settings ***
Documentation    Verify Call Forward No Answer field options on the Add BCA page
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

*** Test Cases ***
Validate Number of Rings for CF No Answer
    [Tags]    Regression  Functional

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    ### Actions:
    When I switch to "bridged_call_appearances" page

    ### Verification
    Then I varify cf no answer options on add bca page

    [Teardown]  Run Keywords  I log off
    ...         AND I check for alert

Create BCA With Non Default Number of Rings for CF No Answer
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  1s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    ${bca_name}=  generate_bca_name
    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  ProfileName  ${bca_name}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number
    set to dictionary  ${localBCAinfo}  CallForwardNoAnswer  8 rings

    ### Actions:
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localBCAinfo}
    sleep  5s
    ### Verification
    Then I verify BCA  &{localBCAinfo}

    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localBCAinfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}