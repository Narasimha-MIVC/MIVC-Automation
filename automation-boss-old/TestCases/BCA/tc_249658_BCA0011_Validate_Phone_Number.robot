*** Settings ***
Documentation    Create BCA with different Phone number with different options for assign from location
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
Create BCA With Phone Number option as Dont Assign
    [Tags]    Regression  Functional

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    ${bca_name}=  generate_bca_name

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  ProfileName  ${bca_name}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localBCAinfo}
    sleep  5s

    ### Verification:
    Then I verify BCA  &{localBCAinfo}

    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localBCAinfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

Create BCA With Phone Number option as Choose from all locations
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ${bca_name}=  generate_bca_name

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  ProfileName  ${bca_name}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Choose from all locations

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localBCAinfo}
    sleep  5s
    ### Verification:
    And I verify BCA  &{localBCAinfo}

    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localBCAinfo}
    ...         AND  sleep  10s
    ...         AND  I log off
    ...         AND  I check for alert

Create BCA With Phone Number option as Choose from selected location
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ${bca_name}=  generate_bca_name

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  ProfileName  ${bca_name}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Choose from selected location

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localBCAinfo}
    sleep  5s
    ### Verification:
    And I verify BCA  &{localBCAinfo}

    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localBCAinfo}
    ...         AND  sleep  10s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}