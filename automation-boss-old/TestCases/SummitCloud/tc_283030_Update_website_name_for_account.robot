*** Settings ***
Documentation    Publish updates to Account (or attributes) to UC-TDS - Modify Website name
...              Author: Priyanka Mishra

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot


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
&{test_data}  Name=${None}

*** Test Cases ***
Publish updates to Account (or attributes) to UC-TDS - Modify Website name
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}


    # Log-in to BOSS and a particular account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    When I switch to "account_details" page
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    log many  ${params}
    ${website_name}=  set variable  www.google.com
    # connect to and fetch the website  information of Company table from m5db before update
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Company where Name=\'${accountName1}\'
    @{data_m5db_company_old}=  I query db  ${query}
    #  fetch the uuid from m5db
    ${query}=  set variable  select AccountGuid from Account where Id=${params["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}
    log many  @{data_m5db_company_old}
    And I verify log details of summitcloud db  tds  ${data_m5db_company_old[0]['Name']}  &{UC_VM_LOGIN}

    # Modify Website Details
    I update and verify account website detail with  ${website_name}
    # connect to and fetch the website  information of Company table from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Company where Name=\'${accountName1}\'

    @{data_m5db_company}=  I query db  ${query}

    #verifying the updated name and time i go to personal information page
    log many  @{data_m5db_company_old}
    log many  @{data_m5db_company}
    And I verify log details of summitcloud db  tds  ${data_m5db_company[0]['Name']}  &{UC_VM_LOGIN}

    # fetch the data from UC TDS
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/tenants/245c68a4-425a-4acf-a6a6-113b480b20ce"
    &{url_info}=  copy dictionary  ${UC_TDS_TBL_TENANTS_URL}
    set to dictionary  ${url_info}  condition  ${data_m5db_accountguid[0]['AccountGuid']}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  Name  ${data_m5db_company[0]['Name']}
    set to dictionary  ${test_data}  WebSite  ${data_m5db_company[0]['WebSite']}
    Then I compare and varify ${test_data} with ${data_uc} for table tenants

    I delete Website detail

    [Teardown]  Run Keywords  I delete Website detail
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

