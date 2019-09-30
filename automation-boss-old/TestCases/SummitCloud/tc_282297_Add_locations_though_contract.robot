*** Settings ***
Documentation    Create Location in BOSS to Push to UC - Add locations though contract
...              Author: Prasanna Kumar Tripathy

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
Create Location in BOSS to Push to UC - Add locations though contract
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    set to dictionary  ${TestContract}  class  access
    set to dictionary  ${TestContract}  product  Analog Profile
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

    # connect to and fetch the uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${TestContract["account_id"]}
    @{data_m5db_AccountGuid}=  I query db  ${query}

    # Get the location info from m5db
    ${query}=  set variable  select LocationUuid from Location where AccountId=${TestContract["account_id"]} and Name=\'${TestContract["locationName"]}\';
    @{data_m5db_locationUuid}=  I query db  ${query}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  tds  ${data_m5db_AccountGuid[0]['AccountGuid']}  &{UC_VM_LOGIN}
    And I verify log details of summitcloud db  loc  ${data_m5db_locationUuid[0]['LocationUuid']}  &{UC_VM_LOGIN}

    # fetch the location data from UC
    # Request Format - "http://default:1234@10.32.128.43:18089/locations/048bc25d-7039-4d36-9c19-173d543943dc"
    # In this case "048bc25d-7039-4d36-9c19-173d543943dc" is the locationUuid from m5db
    &{url_info}=  copy dictionary  ${UC_LOC_TBL_LOCATIONS_URL}
    set to dictionary  ${url_info}  condition  ${data_m5db_locationUuid[0]['LocationUuid']}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationUuid[0]['LocationUuid']}
    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_AccountGuid[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table locations

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