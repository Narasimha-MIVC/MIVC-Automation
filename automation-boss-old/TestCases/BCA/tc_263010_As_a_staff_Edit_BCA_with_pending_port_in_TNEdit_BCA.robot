*** Settings ***
Documentation    Create and Delete Bridged Call Appearances with pending in port TN
...              Immani Mahesh Kumar
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
Assign a pending in port TN to BCA as a staff user.
    [Tags]    Regression

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

    # switch to Phone numbers page and get a pending port in number
    I switch to "phone_systems_phone_numbers" page
    ${pending_port_in_no}=  I find phone number with required status    Pending port in

    #switch to BCA page and add BCA with pending port in number
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  AssignFromLocation      Don't assign a number
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}
    set to dictionary  ${localbcainfo}  AssignFromLocation      Choose from all locations
    set to dictionary  ${localbcainfo}  SelectPhoneNumber  ${pending_port_in_no}
    And I edit BCA  ${localbcainfo}
    And I verify BCA  &{localbcainfo}
    And I delete BCA  ${localbcainfo}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}