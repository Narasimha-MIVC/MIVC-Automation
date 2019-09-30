*** Settings ***
Documentation    Verify Deleting of the phone numbers in D2 after deleting the correponding associated BCA
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
Verify deletion of dnis from D2 after aBCA is deleted
    [Tags]    Regression  Functional

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    log many  &{params}

    # call the clean up function
    #clean up

    # Retrieve and use the user phone number which needs a BCA
#    ${phone_number}=  I retrieve user phone number  ${PMUser}

    ${aBCA_name}=  set variable  ${PMUser}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}
#    set to dictionary  ${localbcainfo}  AssociatedBCAProfile  ${aBCA_name}
#    set to dictionary  ${localbcainfo}  SelectPhoneNumber  ${phone_number}
    set to dictionary  ${localbcainfo}  Location  ${locationName}

    ### Actions:
    #1. Switch to BCA page
    When I switch to "bridged_call_appearances" page
    #2. Add New aBCA
    And I create Bridged Call Appearance  ${localbcainfo}

    ${ph_num}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${profile_name}=  Set Variable  &{localbcainfo}[AssociatedBCAProfile]

    And I verify BCA  &{localbcainfo}

    #3. Switch to the phone system -> phone numbers page and assign an available phone number to aBCA
    And I switch to "phone_systems_phone_numbers" page
    ${name}=  replace string  ${profile_name}  ${SPACE}  _
    log  ${profile_name}
    log  ${name}
    ${bca_name}=  set variable  ${name}_${ph_num[-4:]}${SPACE}x${extn}
    log  ${bca_name}
    ${ph_number}=  I assign phone number to bca  Available  ${bca_name}

    #4. Checking the linked phone number in D2
    ${dnis}=  Replace String  ${ph_number}  ${SPACE}(  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
    ${dnis}=  set variable  +${dnis}
    log  ${dnis}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
#    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${True}
    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${True}

    #4. Now delete the aBCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  2s

    ### Verifications:
    #5. Again Checking the linked phone number in D2
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
#    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${False}
    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${False}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

