*** Settings ***
Documentation    Create Account in BOSS to push to UC-TDS - Add Account
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
Add account as staff user
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    set to dictionary  ${TestContract}  get_account_info  ${True}

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

    # Get the tenant info from D2 and verify
#    And I connect db  &{log_info_d2db}
#    ${query}=  set variable  SELECT TenantGUID FROM tenants WHERE TenantName=\'${TestContract["accountName"]}\'
#    @{data_d2db}=  I query db  ${query}

    # verify the UUID from M5DB and D2DB
#    should be equal  ${data_m5db[0]['AccountGuid']}  ${data_d2db[0]['TenantGUID']}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  tds  ${data_m5db[0]['AccountGuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/tenants/245c68a4-425a-4acf-a6a6-113b480b20ce"
    &{url_info}=  copy dictionary  ${UC_TDS_TBL_TENANTS_URL}
    set to dictionary  ${url_info}  condition  ${data_m5db[0]['AccountGuid']}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  uuid  ${data_m5db[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table tenants

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

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