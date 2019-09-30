*** Settings ***
Documentation    Publish Service update to UC-SES - User level service update
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
Publish Service update to UC-SES - User level service update
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}
    &{log_info_ucdb}=  copy dictionary  ${UCDB_CONN_INFO}

    set to dictionary  ${TestUser}    au_userlocation    ${locationName}
    Set to Dictionary  ${TestUser}    request_by    ${request_by}
    Set to Dictionary  ${TestUser}    request_source    Email
    Set to Dictionary  ${TestUser}    role    Technical
    Set to Dictionary  ${TestUser}    assign_new_number    ${True}

    # Log-in to BOSS and a particular account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    # Add user
    When I switch to "users" page
    ${phone_num}  ${extn} =  I add user   &{TestUser}
    I verify that User exist in user table   &{TestUser}
    ${ph}=  set variable  ${phone_num[3:6]}${phone_num[8:11]}${phone_num[-4:]}

    # connect to and fetch the UserUuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select UserUuid from Person where Username=\'${TestUser["au_username"]}\'
#    ${query}=  set variable  select UserUuid from Person where Username=\'boss_auto_bill_FLzNUzyb@shoretel.com\'
    @{data_m5db_useruuid}=  I query db  ${query}

    # Again fetch service uuid from m5db
    ${query}=  set variable  select ServiceUuid from service_Service where TN=\'${ph}\'
#    ${query}=  set variable  select ServiceUuid from service_Service where TN=\'4083005266\'
    log  ${query}
    @{data_m5db_serviceuuid}=  I query db  ${query}

    # Verify the log in UC-SES
    And I verify log details of summitcloud db  ses  ${data_m5db_serviceuuid[-1]['ServiceUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC SES -
    # Request Format - "http://default:1234@10.32.128.43:18086/v2/services/services:access:cosmo:telephony"
    &{url_info}=  copy dictionary  ${UC_SES_TBL_SERVICES_URL}
    set to dictionary  ${url_info}  condition  services:access:cosmo:telephony
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  ServiceUuid  ${data_m5db_serviceuuid[-1]['ServiceUuid']}
    # Prasanna: Need to check if the following validation fro UserUuid is required
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_useruuid[0]['UserUuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table services

    [Teardown]  Run Keywords  I switch to "users" page
    ...                       AND  I delete user ${TestUser["au_username"]} as user "${request_by}"
    ...                       AND  I log off
    ...                       AND  I check for alert

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