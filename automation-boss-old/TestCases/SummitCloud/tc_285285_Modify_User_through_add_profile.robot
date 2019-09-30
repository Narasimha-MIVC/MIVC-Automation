*** Settings ***
Documentation    Publish updates to IDMS schema attributes to IDMS for a given user - Modify User through add profile
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
Publish updates to IDMS schema attributes to IDMS for a given user - Modify User through add profile
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

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

    # connect to and fetch the Profile information from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Profile where BoblEmail=\'${TestUser["au_username"]}\'
    @{data_m5db_profile_old}=  I query db  ${query}
    # connect to and fetch the UserUuid from m5db
    ${query}=  set variable  select UserUuid from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db_uuid_old}=  I query db  ${query}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  idms  ${data_m5db_uuid_old[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info}  condition  ${TestUser["au_username"]}?${temp}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_uuid_old[0]['UserUuid']}
    And I compare and varify ${test_data} with ${data_uc} for table users

    # Now modify the Extension number in user profile in BOSS
    # Operations -> Primary Partitions -> Profiles -> edit
    # Get an available phone number. We need a valid exetension
    When I switch to "phone_systems_phone_numbers" page
    ${ph_number}=  I find phone number with required status  Available  Domestic  ${locationName}
    log  ${ph_number[-4:]}
    &{profile_data}=  create dictionary  email=${TestUser["au_username"]}  extension=${ph_number[-4:]}
#    &{profile_data}=  create dictionary  email=boss_auto_bill_mQa3VPTL@shoretel.com  extension=${ph_number[-4:]}
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    And I edit user profiles  &{profile_data}
    sleep  2

    # Again querying the M5DB and get the extension and the date of modification of the profile data
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Profile where BoblEmail=\'${TestUser["au_username"]}\'
    @{data_m5db_profile_new}=  I query db  ${query}
    # connect to and fetch the UserUuid from m5db
    ${query}=  set variable  select UserUuid from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db_uuid_new}=  I query db  ${query}

    # Verify that the date and time of modification for the profile and the extension
    log many  @{data_m5db_profile_old}
    log many  @{data_m5db_profile_new}

#    # Get the tenant info from D2 and verify
#    And I connect db  &{log_info_d2db}
#    ${query}=  set variable  select * from users where GuiLoginName=\'${TestUser["au_username"]}\'
#    @{data_d2db}=  I query db  ${query}

    # verify the UUID from M5DB and D2DB
#    should be equal  ${data_m5db[0]['AccountGuid']}  ${data_d2db[0]['TenantGUID']}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  idms  ${data_m5db_uuid_new[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info}  condition  ${TestUser["au_username"]}?${temp}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_uuid_new[0]['UserUuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table users

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