*** Settings ***
Documentation    Create BCA with different Phone number with different options for assign from location
...              Immani Mahesh Kuumar
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
verify BCA from destination type filed
    [Tags]    Regression  Functional
    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
    set to dictionary  ${localbcainfo}  OtherSettings  ${True}


    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    ${ph_num}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${profile_name}=  Set Variable  &{localbcainfo}[ProfileName]

    And I verify BCA  &{localbcainfo}
    And I switch to "phone_systems_phone_numbers" page

    ${bca_name}=  Set Variable    ${bca_name}${SPACE}BCA${SPACE}x${extn}
    And I find element on phone number page  ${ph_num}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    And I switch to "bridged_call_appearances" page
    [Teardown]  run keywords  I delete BCA  ${localBCAinfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}