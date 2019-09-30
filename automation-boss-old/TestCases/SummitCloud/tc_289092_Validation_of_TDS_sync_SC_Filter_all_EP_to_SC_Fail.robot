*** Settings ***
Documentation    Validation of tds sync SC with Filter as all - Success of EventPropagator-
...              eventpropagator to SC Failed

...              Author: Priyanka Mishra

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot
Resource          ../Contract/Variables/contract_variables.robot

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
Validation of tds sync SC with Filter as all - Success of EventPropagator-eventpropagator to SC Fails

    [Tags]    DEBUG


    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    set to dictionary  ${TestContract}  class  access
    set to dictionary  ${TestContract}  product  MiCloud Connect Telephony
    set to dictionary  ${TestContract}  get_account_info  ${True}

    # Get Detail of UC DBCONNECT
    &{Uc_Details}=  copy dictionary  ${UC_VM_LOGIN}
    ${data_uc}=  create dictionary  fetched_data=${None}
    set to dictionary  ${Uc_Details}  uc_db_data=${data_uc}

    # stop container tds
    I stop docker container  ${TDS_CONTAINER_ID}  &{Uc_Details}
    log many  &{Uc_Details}
    sleep  2

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

    # Auto Provision the initial orders
    When I switch to "order" page
    And I provision initial order
    sleep  2

    # Activate the services
    When I switch to "services" page
    sleep  2
    And I activate all service
    sleep  5

    # connect to and fetch the Account Uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${TestContract["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}

    # connect M5DB and fetch data from log_eventpropagation table
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_accountguid[0]['AccountGuid']}\'
    @{data_m5db_EventPropagation}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation}

    ${query}=  set variable  select Payload from log_EventPropagation where EntityGuid=\'${data_m5db_accountguid[0]['AccountGuid']}\'
    @{data_m5db_EventPropagation_payload}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload}

    # fetch the data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Tenants"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Tenants
    set to dictionary  ${url_info}  condition  ?${temp}
    set to dictionary  ${url_info}  option  all
    set to dictionary  ${url_info}  StartDate  ${data_m5db_EventPropagation[0]['DateCreated']}
    set to dictionary  ${url_info}  EndDate  ${data_m5db_EventPropagation[0]['DateModified']}

    @{data_uc_backsync}=  I fetch data from back sync db  &{url_info}
    log many  @{data_uc_backsync}

# Commented below Validaton Need to Confirm before Adding
#    # Restart container tds
#    I start docker container  &{Uc_Details}
#    sleep   10
#
#   # Verify the Account related log in UC-TDS
#    And I verify log details of summitcloud db  tds  ${data_m5db_accountguid[0]['AccountGuid']}  &{UC_VM_LOGIN}
#
#
#     # fetch the data from UC
#    # Request Format - "http://default:1234@10.32.128.43:18085/v2/tenants/245c68a4-425a-4acf-a6a6-113b480b20ce"
#    &{url_info1}=  copy dictionary  ${UC_TDS_TBL_TENANTS_URL}
#    set to dictionary  ${url_info1}  condition  ${data_m5db_accountguid[0]['AccountGuid']}
#  #    @{data_uc_tds}=  I fetch data from summit cloud db  &{url_info1}
#  #    log many   @{data_uc_tds}
#
#    ${data_uc_tds}=  I fetch data from summit cloud db  &{url_info1}
#    log   ${data_uc_tds}
#    should be true  "404" in """${data_uc_tds}"""

#    # Verify the UC data
#    set to dictionary  ${test_data}  uuid  ${data_m5db_accountguid[0]['AccountGuid']}
#    Then I compare and varify ${test_data} with ${data_uc_tds} for table tenants


    [Teardown]  Run Keywords  I start docker container  &{Uc_Details}
    ...                       AND  I close orders and contract
    ...                       AND  I log off
    ...                       AND  I check for alert


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

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    ${TestContract}



    Run keyword if    '${country}' == 'Australia'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}  &{Contract_Aus}


            ...    ELSE IF    '${country}' == 'UK'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}  &{Contract_UK}


            ...    ELSE IF    '${country}' == 'US'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}   &{Contract_US}
            ...    AND    log to console     "==============DEBUG================"
            ...    AND    log to console     ${TestContract}
            ...    ELSE
            ...    log  Please enter a valid Country name like US, UK or Australia

    : FOR    ${key}    IN    @{TestContract.keys()}
    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}