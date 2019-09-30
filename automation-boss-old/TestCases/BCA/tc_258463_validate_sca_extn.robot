*** Settings ***
Documentation    Validate created SCA extension from Phone Setting presence on BCA page
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
Validate SCA Extn On BCA Page
    [Tags]    Regression  FAILED

    ### Pre Conditions:  Log in as PM user
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  3s
    And I switch to "users" page

    &{sca_info}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${sca_info}  ScaUserName  ${PMUser}
    set to dictionary  ${sca_info}  ScaEnableFlag  Enabled

    ### Actions:
    ${extn}=  I enable SCA  &{sca_info}

    ### Verification
    Then I log off
    And I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    Then I switch to "bridged_call_appearances" page
    sleep  2s
    # Verify it as an Associated BCA (aBCA)
    &{aBCA_info}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${aBCA_info}  AssociatedBCA  ${True}
    set to dictionary  ${aBCA_info}  AssociatedBCAProfile  ${PMUser}
    set to dictionary  ${aBCA_info}  AssociatedBCAExtn  ${extn}
    set to dictionary  ${aBCA_info}  Location  ${locationName}

    And I verify BCA  &{aBCA_info}

    [Teardown]  run keywords  I delete BCA  ${aBCA_info}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***