*** Settings ***
Documentation    Create and Delete Bridged Call Appearances
Suite Teardown    Close The Browsers
#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
#Library           ../../lib/BossComponentBCA.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
Validate functionaltity BCA
    [Tags]    Regression   FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${user_phone_number}=  I retrieve user phone number  ${PMUser}
    ${outbound_caller_id}=  Set Variable  ${SPACE}${user_phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    And I switch to "phone_systems_phone_numbers" page
    ${Phone_num_Type}=  set variable  Global${SPACE}${SPACE}Inbound
    ${phone_no}=    I find phone number with required status  Available  ${Phone_num_Type}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${outbound_caller_id}
    set to dictionary  ${localbcainfo}  SelectPhoneNumber  ${phone_no}
    set to dictionary  ${localbcainfo}  VerifyGlobalNo  ${True}

    And I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}


    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


