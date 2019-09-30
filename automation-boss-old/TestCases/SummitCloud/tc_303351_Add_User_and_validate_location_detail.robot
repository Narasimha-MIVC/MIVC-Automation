*** Settings ***
Documentation    Enhancements to Location data propagation to UC - Add User and validate the country=US, state=CA,tn=+12345

...              Author: Priyanka Mishra

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/Geolocationinfo.robot
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
&{test_data}  UserUuid=${None}

*** Test Cases ***
Enhancements to Location data propagation to UC - Add User and validate the country=US, state=CA,tn=+12345

    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    # Log-in to BOSS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

    # create an acount
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "geographic_locations" page
    And I create geographic location    &{geolocation_US}
    Then I verify location "${geolocation_US['Location']}" with "Registered" state

    # create user with new Geo Location
    set to dictionary  ${TestUser}    au_userlocation    ${geolocation_US['Location']}
    Set to Dictionary  ${TestUser}    request_by    ${request_by}
    Set to Dictionary  ${TestUser}    request_source    Email
    Set to Dictionary  ${TestUser}    role    Technical
    set to Dictionary  ${TestUser}    ph_num_chk_box   Yes
#    Set to Dictionary  ${TestUser}    assign_new_number    ${True}
    Set to Dictionary  ${TestUser}    skip_add_phone  ${True}

    Set to Dictionary  ${geolocation_US}    country_code    US
    Set to Dictionary  ${geolocation_US}    state_code    NY

    When I switch to "users" page
    ${phone_num}  ${extn} =  I add user   &{TestUser}
    I verify that User exist in user table   &{TestUser}

    # connect to and fetch the UserUuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select UserUuid from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db_user}=  I query db  ${query}

    # fetch the Location details from m5db
    ${query}=  set variable  select LocationUuid from Location where Name=\'${geolocation_US['Location']}\';
    @{data_m5db_locationdata}=  I query db  ${query}
    log many  @{data_m5db_user}
    log many  @{data_m5db_locationdata}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  idms  ${data_m5db_user[0]['UserUuid']}  &{UC_VM_LOGIN}
    # Verify the Location related log in UC-LOC
    And I verify log details of summitcloud db  loc  ${data_m5db_locationdata[0]['LocationUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info}  condition  ${TestUser["au_username"]}?${temp}
    @{data_uc_IDMS}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc_IDMS}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_user[0]['UserUuid']}
    #set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationdata[0]['LocationUuid']}
    Then I compare and varify ${test_data} with ${data_uc_IDMS} for table users

    # fetch the data from location table of UC LOC -
    # Request Format - "http://default:1234@10.32.128.43:18089/locations/048bc25d-7039-4d36-9c19-173d543943dc"
    # In this case "048bc25d-7039-4d36-9c19-173d543943dc" is the locationUuid from m5db
    &{url_info1}=  copy dictionary  ${UC_LOC_TBL_LOCATIONS_URL}
    set to dictionary  ${url_info1}  condition  ${data_m5db_locationdata[0]['LocationUuid']}
    @{data_uc_loc}=  I fetch data from summit cloud db  &{url_info1}
    log many  @{data_uc_loc}

    # Verify the UC data
    set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationdata[0]['LocationUuid']}
    set to dictionary  ${test_data}  city  ${geolocation_US['city']}
    set to dictionary  ${test_data}  state  ${geolocation_US['state_code']}
    set to dictionary  ${test_data}  country  ${geolocation_US['country_code']}
    log many  &{geolocation_US}
    Then I compare and varify ${test_data} with ${data_uc_loc} for table locations

    [Teardown]  Run Keywords  I switch to "users" page
    ...                       AND  I delete user ${TestUser["au_username"]} as user "${request_by}"
    ...                       AND  I close orders and location
    ...                       AND  I log off
    ...                       AND  I check for alert

*** Keywords ***
I close orders and location
    When I switch to "order" page
    And I close open order for location "${geolocation_US['Location']}"
    I switch to "geographic_locations" page
    Then I close the location "${geolocation_US['Location']}" requested by "${request_by}"
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_str2}=     Generate Random String    8    [LETTERS][NUMBERS]

    ${TestUser}=    create dictionary
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_str2}
    Set suite variable    ${uni_num}
    Set suite variable    ${TestUser}
    Set suite variable      ${geolocation_US}

    : FOR    ${key}    IN    @{geolocation_US.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_US["${key}"]}    {rand_str}    ${uni_str2}
    \    Set To Dictionary    ${geolocation_US}    ${key}    ${updated_val}

    set to dictionary  ${TestUser}  &{BillingProfUser}

    : FOR    ${key}    IN    @{TestUser.keys()}
    \    ${updated_val}=    Replace String    ${TestUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestUser}    ${key}    ${updated_val}

    log to console  ${TestUser}
