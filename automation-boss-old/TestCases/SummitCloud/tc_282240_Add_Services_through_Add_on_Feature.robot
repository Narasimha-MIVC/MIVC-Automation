*** Settings ***
Documentation    Publish Service creation to UC-SES - Add Services through Add-on-Feature
...              Author: Prasanna Kumar Tripathy

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot
Resource          ../Contract/Variables/contract_variables.robot
Resource          ../../Variables/PhoneNumberInfo.robot
Resource          ../../Variables/UserInfo.robot

#Variable files
Variables          Variables/SummitCloud_variables.py

#BOSS Component
Library           ../../lib/BossComponent.py  browser=${BROWSER}  country=${country}
Library           ../../lib/DirectorComponent.py
Library           ../../lib/DBComponent.py
Library           ../../lib/SummitCloud.py

#Built in library
Library  String

*** Variables ***
&{test_data}  uuid=${None}

*** Test Cases ***
Publish Service creation to UC-SES - Add Services through Add-on-Feature
    [Tags]    DEBUG     SC

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    set to dictionary  ${TestContract}  class  access
    set to dictionary  ${TestContract}  product  MiCloud Connect Telephony
    set to dictionary  ${TestContract}  get_account_info  ${True}

    # Log-in to BOSS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

    # add and confirm a new contract
    When I switch to "accounts" page
    And I add contract    &{TestContract}
    And I verify grid contains "Ordered" value

    # confirm the contract
    When I click on "${TestContract["accountType"]}" link in "contract_grid"
    ${order_number}=   I confirm the contract with instance "${bossCluster} (${platform})" and location "${TestContract["locationName"]}"
    should not be equal  ${order_number}  ${None}
    And verify_account  ${TestContract}

    sleep  2

    # Auto Provision the initial orders
    When I switch to "order" page
    And I provision initial order

    sleep  2
    ${request_user}=  Set Variable  ${TestContract["firstName"]}${SPACE}${TestContract["lastName"]}
    # Add just one Phone number
    When I switch to "phonenumber" page
    set to dictionary  ${PhoneNumberDetails}  range  0
    set to dictionary  ${PhoneNumberDetails}  requestedBy  ${request_user}
    I add PhoneNumber    &{PhoneNumberDetails}
    and I set PhoneNumber state    &{PhoneNumberDetails}
    Then I verify PhoneNumber state    &{PhoneNumberDetails}

    sleep  2

    # Add an user
    When I switch to "users" page
    #set to dictionary  ${TestUser}  ap_phonetype  MiCloud Connect Elite
    set to dictionary  ${TestUser}  request_by  ${request_user}
    set to dictionary  ${TestUser}  request_source  Email

    ${phone_num}  ${extn} =  I add user   &{TestUser}
    I verify that User exist in user table   &{TestUser}
    sleep  2

    # Activate the services
    When I switch to "services" page
    sleep  2
    And I activate all service
    sleep  2
    ${request_user}=  Set Variable  ${TestContract["firstName"]}${SPACE}${TestContract["lastName"]}
    set to dictionary  ${ADD_ON_FEATURE}  RequestedBy  ${request_user}
    # Activate the add on feature Connect Archiving
    When I switch to "addonfeatures" page
    set to dictionary  ${ADD_ON_FEATURE}  RequestedBy  ${request_user}
    And I activate Add-On features  &{ADD_ON_FEATURE}
    sleep  2

    # connect to and fetch the Account Uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${TestContract["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}

    # fetch the service details from m5db
    ${query}=  set variable  select * from service_service where AccountId=${TestContract["account_id"]}
    @{data_m5db_servicedata}=  I query db  ${query}
    log many  @{data_m5db_servicedata}

    # Verify the service related log in UC-SES
    And I verify log details of summitcloud db  ses  ${data_m5db_servicedata[0]['ServiceUuid']}  &{UC_VM_LOGIN}

    # fetch the service data from UC
    # Request Format - "http://default:1234@10.32.128.43:18086/v2/services/services:access:cosmo:telephony"
    &{url_info}=  copy dictionary  ${UC_SES_TBL_SERVICES_URL}
    ${condition}=  set variable  services:access:cosmo:telephony/tenants/${data_m5db_accountguid[0]['AccountGuid']}
    set to dictionary  ${url_info}  condition  ${condition}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  ServiceUuid  ${data_m5db_servicedata[0]['ServiceUuid']}
    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table services

    [Teardown]  Run Keywords  I close orders and contract
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
I close orders and contract

    When I switch to "order" page
    sleep  2
    And I close all order
    When I switch to "accounts" page
    sleep  2
    And I close contract  ${TestContract["accountName"]}   ${TestContract["firstName"]}${SPACE}${TestContract["lastName"]}
    #    Then I verify contract "${TestContract["accountName"]}" is deleted

Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${TestContract}=    create dictionary
    ${PhoneNumberDetails}=    create dictionary
    ${TestUser}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    ${TestContract}
    Set suite variable    ${PhoneNumberDetails}
    Set suite variable    ${TestUser}

    set to dictionary  ${TestUser}  &{AccPMProfUser}

    Run keyword if    '${country}' == 'Australia'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}  &{Contract_Aus}
            ...    AND set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_AUS}


            ...    ELSE IF    '${country}' == 'UK'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}  &{Contract_UK}
            ...    AND  set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_UK}


            ...    ELSE IF    '${country}' == 'US'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}   &{Contract_US}
            ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_US}
            ...    AND    log to console     "==============DEBUG================"
            ...    AND    log to console     ${TestContract}
            ...    ELSE
            ...    log  Please enter a valid Country name like US, UK or Australia

    : FOR    ${key}    IN    @{TestContract.keys()}
    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{PhoneNumberDetails.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{TestUser.keys()}
    \    ${updated_val}=    Replace String    ${TestUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestUser}    ${key}    ${updated_val}

