*** Settings ***
Documentation    Event Persistence - Validation of tds logging - Failure of EventPropagator
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
Event Persistence - Validation of tds logging - Failure of EventPropagator

    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    set to dictionary  ${TestContract}  get_account_info  ${True}

    # Get Detail of UC DBCONNECT
    &{Uc_Details}=  copy dictionary  ${UC_VM_LOGIN}
    ${data_uc}=  create dictionary  fetched_data=${None}
    set to dictionary  ${Uc_Details}  uc_db_data=${data_uc}

   # stop container TDS
    I stop docker container  ${EVENT_PROP_CONTAINER_ID}  &{Uc_Details}
    log many  &{data_uc}
    sleep  10

    # Log-in to BOSS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

    # create an acount
    When I switch to "accounts" page
    set to dictionary  ${TestContract}  accountType  Vendor
    And I add account    &{TestContract}
    And verify_account  ${TestContract}


    # connect to and fetch the uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${TestContract["account_id"]}
    @{data_m5db}=  I query db  ${query}

    #  fetch the EntityGuid value from m5db.[log_EventPropagation] table and check  New Account Guid should not present
    ${query}=  set variable  select EntityGuid from log_EventPropagation where EntityName in ('Account', 'Profile')
    @{data_m5db_EventPropagation}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation}
    should not contain  ${data_m5db_EventPropagation}    ${data_m5db[0]['AccountGuid']}

    ${query}=  set variable  select EntityGuid from log_EventPropagation where EntityName in ('Account', 'Profile')
    @{data_m5db_EventPropagation_payload}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  tds  ${data_m5db[0]['AccountGuid']}  &{UC_VM_LOGIN}

#Commented the validation and after confirmation will validate
#     # fetch the data from UC
#    # Request Format - "http://default:1234@10.32.128.43:18085/v2/tenants/245c68a4-425a-4acf-a6a6-113b480b20ce"
#    &{url_info}=  copy dictionary  ${UC_TDS_TBL_TENANTS_URL}
#    set to dictionary  ${url_info}  condition  ${data_m5db[0]['AccountGuid']}
#    ${data_uc_tds}=  I fetch data from summit cloud db  &{url_info}
#    log   ${data_uc_tds}
#    should be true  "404" in """${data_uc_tds}"""

    [Teardown]  Run Keywords  I start docker container  &{Uc_Details}
    ...                       AND  I log off
    ...                       AND  I check for alert

*** Keywords ***
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