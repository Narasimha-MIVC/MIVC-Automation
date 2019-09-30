*** Settings ***
Documentation    Publish updates to Location + Address to UC -Update location from Personal Emergency Location
...              Author: Prasanna Kumar Tripathy

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/UserInfo.robot

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
Publish updates to Location + Address to UC -Update location from Personal Emergency Location
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}
    ${dm_user}=  create dictionary  email=${None}  profileId=${None}

    set to dictionary  ${TestUser}    au_userlocation    ${locationName}
    Set to Dictionary  ${TestUser}    request_by    ${request_by}
    Set to Dictionary  ${TestUser}    request_source    Email
    Set to Dictionary  ${TestUser}    role    Technical

    # Log-in to BOSS and a particular account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "accountdetails" page
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    log many  ${params}

    # Note:Username and Buisness email should be same to pass this test case
    # retrieve the first DM user info
    When I switch to "users" page
    And I retrive the first DM user info  ${dm_user}
    log many  &{dm_user}
    ${e_address_info}=  create dictionary  emergency_location=${True}
    ...               personal_address=${True}
    ...               select_using_text=Create New Address...
    ...               Address_1=474 Boston Post Rd
    ...               City=North Windham
    ...               State=Connecticut
    ...               Zip=06256
    log many  &{e_address_info}
    And I edit user phone settings  &{e_address_info}

     # connect to and fetch the Account Guid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${params["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}

    # connect to and fetch the UserUuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Person where BusinessEmail=\'${dm_user['email']}\'
    @{data_m5db}=  I query db  ${query}
    log many  @{data_m5db}

    Set to Dictionary  ${e_address_info}    country_code    US
    Set to Dictionary  ${e_address_info}    state_code    CT

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  idms  ${data_m5db[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info}  condition  ${data_m5db[0]['Username']}?${temp}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db[0]['UserUuid']}
    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
    set to dictionary  ${test_data}  state  ${e_address_info['state_code']}
    set to dictionary  ${test_data}  country  ${e_address_info['country_code']}
    Then I compare and varify ${test_data} with ${data_uc} for table users

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${TestUser}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    ${TestUser}

    set to dictionary  ${TestUser}  &{BillingProfUser}

    : FOR    ${key}    IN    @{TestUser.keys()}
    \    ${updated_val}=    Replace String    ${TestUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestUser}    ${key}    ${updated_val}

    log to console  ${TestUser}