*** Settings ***
Documentation    Verify the status of Unassinged TN from BCA to Unassign
Suite Teardown    Close The Browsers
#...               dev-Vasuja
#...               Comments:

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


*** Test Cases ***
1. Login as staff user and Verify the status of Unassinged TN from BCA to Unassign
    [Tags]    Regression  Sanity_Phase2

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    #Get the account info
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  AssignFromLocation  Don't assign a number

    ### Actions:
    #1. Switch the BCA page and add a BCA
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    #2. Go to the phonesystem -> phone number page and assign a number to the BCA
    And I switch to "phone_systems_phone_numbers" page
    ${extn}=  set variable  &{localbcainfo}[Extension]
    ${bca_name}=  set variable  ${bca_name}${SPACE}x${extn}
    ${ph_number}=  I assign phone number to bca  Available  ${bca_name}
    set to dictionary  ${localbcainfo}  SelectPhoneNumber  ${ph_number}
    sleep  3s
    #3. Verify that the phone number is now in D2 DNIS
    ${dnis}=  Replace String  &{localbcainfo}[SelectPhoneNumber]  ${SPACE}(  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
    ${dnis}=  set variable  +${dnis}
    log  ${dnis}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${True}

    #4. Unassign the phone number from the BCA
    When I switch to "phone_systems_phone_numbers" page
    ${phone_state}=  I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  Active  Bridged Call Appearance  ${None}  ${True}
    set to dictionary  ${localbcainfo}  Unassign    True
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s

    #5. Verify that the element is in required state
    And I switch to "operations_phone_numbers" page
    &{ph_num}=  copy dictionary  ${PHONE_INFO}
    set to dictionary  ${ph_num}  numberRange  ${None}
    run keyword if  '${phone_state}' == 'Pending Port In'  set to dictionary  ${ph_num}  state  Pending Port In
    ...         ELSE  set to dictionary  ${ph_num}  state  Available
    ${result}=  verify phone numbers and their status  &{ph_num}
    should be true  ${result}
    sleep  5s

    #6. Checking that the phone number in not in the list of DNIS in D2
    ${dnis}=  Replace String  ${localbcainfo['SelectPhoneNumber']}  ${SPACE}(  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
    ${dnis}=  set variable  +${dnis}
    log  ${dnis}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${False}

    [Teardown]  Run Keywords  I switch to "bridged_call_appearances" page
    ...                       AND  I delete BCA  ${localbcainfo}
    ...                       AND  sleep  2s
    ...                       AND  I log off
    ...                       AND  I check for alert

#2. Login as DM user and Verify the status of Unassinged TN from BCA to Unassign
#    [Tags]    Regression  Sanity_Phase2
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    sleep  3
#    &{params}=  create dictionary
#    set to dictionary  ${params}  get_account_id  ${True}
#    And I retrieve account details  ${params}
#    Then I log off
#
#    log many  &{params}
#    ### Pre Conditions:
#    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    sleep  5s
#    # call the clean up function
#    #clean up
#
#    # Retrieve and use the user phone number which needs a BCA
#    ${phone_number}=  I retrieve user phone number  ${PMUser}
#    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}
#
#    ${bca_name}=  generate_bca_name
#    log  ${bca_name}
#    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
#    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
#
#    ### Actions:
#    #1.
#    When I switch to "bridged_call_appearances" page
#    #2.
#    And I create Bridged Call Appearance  ${localbcainfo}
#    And I verify BCA  &{localbcainfo}
#    And I switch to "phone_systems_phone_numbers" page
#    ${phone_state}=  I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
#    set to dictionary  ${localbcainfo}  Unassign    True
#    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
#    sleep  5s
#    ### Verification:
#    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  Available  ${None}  ${None}  ${True}
#
#    # Check if the phone number is now in available state
#    # Modified by: Prasanna - In case of PM / DM user no operations tab available
##    And I switch to "operations_phone_numbers" page
##    &{ph_num}=  copy dictionary  ${PHONE_INFO}
##    set to dictionary  ${ph_num}  numberRange  ${None}
##    run keyword if  '${phone_state}' == 'Pending Port In'  set to dictionary  ${ph_num}  state  Pending Port In
##    ...         ELSE  set to dictionary  ${ph_num}  state  Available
##    ${result}=  verify phone numbers and their status  &{ph_num}
##    should be true  ${result}
##    sleep  5s
#    # Checking the linked phone number in D2
#    ${dnis}=  Replace String  ${localbcainfo['SelectPhoneNumber']}  ${SPACE}(  ${EMPTY}
#    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
#    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
#    ${dnis}=  set variable  +${dnis}
#    log  ${dnis}
#    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
##    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${True}
#    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${True}
#
#    # Now delete the aBCA
#    And I switch to "bridged_call_appearances" page
#    And I delete BCA  ${localbcainfo}
#    sleep  2s
#
#    ### Verifications:
#    # Again Checking the linked phone number in D2
#    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
##    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${False}
#    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${False}
#    [Teardown]  Run Keywords  I log off
#    ...         AND  I check for alert
#
#3. Login as PM user and Verify the status of Unassinged TN from BCA to Unassign
#    [Tags]    Regression  Sanity_Phase2
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    sleep  3
#    &{params}=  create dictionary
#    set to dictionary  ${params}  get_account_id  ${True}
#    And I retrieve account details  ${params}
#    Then I log off
#
#    log many  &{params}
#    ### Pre Conditions:
#    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    sleep  5s
#    # call the clean up function
#    #clean up
#
#    # Retrieve and use the user phone number which needs a BCA
#    ${phone_number}=  I retrieve user phone number  ${PMUser}
#    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}
#
#    ${bca_name}=  generate_bca_name
#    log  ${bca_name}
#    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
#    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
#
#    ### Actions:
#    #1.
#    When I switch to "bridged_call_appearances" page
#    #2.
#    And I create Bridged Call Appearance  ${localbcainfo}
#    And I verify BCA  &{localbcainfo}
#    And I switch to "phone_systems_phone_numbers" page
#    ${phone_state}=  I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
#    set to dictionary  ${localbcainfo}  Unassign    True
#    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
#    sleep  5s
#    ### Verification:
#    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  Available  ${None}  ${None}  ${True}
#
#    # Check if the phone number is now in available state
#    # Modified by: Prasanna - In case of PM / DM user no operations tab available
##    And I switch to "operations_phone_numbers" page
##    &{ph_num}=  copy dictionary  ${PHONE_INFO}
##    set to dictionary  ${ph_num}  numberRange  ${None}
##    run keyword if  '${phone_state}' == 'Pending Port In'  set to dictionary  ${ph_num}  state  Pending Port In
##    ...         ELSE  set to dictionary  ${ph_num}  state  Available
##    ${result}=  verify phone numbers and their status  &{ph_num}
##    should be true  ${result}
##    sleep  5s
#    # Checking the linked phone number in D2
#    ${dnis}=  Replace String  ${localbcainfo['SelectPhoneNumber']}  ${SPACE}(  ${EMPTY}
#    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
#    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
#    ${dnis}=  set variable  +${dnis}
#    log  ${dnis}
#    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
##    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${True}
#    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${True}
#
#    # Now delete the aBCA
#    And I switch to "bridged_call_appearances" page
#    And I delete BCA  ${localbcainfo}
#    sleep  2s
#
#    ### Verifications:
#    # Again Checking the linked phone number in D2
#    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
##    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${False}
#    And I verify DNIS in D2  ${dnis}  ${params['partition_id']}  ${False}
#    [Teardown]  Run Keywords  I log off
#    ...         AND  I check for alert


*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}