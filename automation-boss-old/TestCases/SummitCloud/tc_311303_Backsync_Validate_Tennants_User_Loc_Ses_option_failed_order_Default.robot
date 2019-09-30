*** Settings ***
Documentation    BackSync - Validate Tenant,User,Service,Location for option failed and order by default
...              Author: Priyanka Mishra

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot
Resource          ../../Variables/ContractInfo.robot
Resource           ../../Variables/UserInfo.robot
Resource           ../../Variables/Geolocationinfo.robot

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
BackSync - Validate Tenant,User,Service,Location for option failed and order by default

    [Tags]    DEBUG     SC

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}


     # Log-in to BOSS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

	################## Add new user ################################
     set to dictionary  ${TestUser}    au_userlocation    ${locationName}
    Set to Dictionary  ${TestUser}    request_by    ${request_by}
    Set to Dictionary  ${TestUser}    request_source    Email
    Set to Dictionary  ${TestUser}    role    Technical
    Set to Dictionary  ${TestUser}    skip_add_phone  ${True}

    # Log-in to BOSS and a particular account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
   # Add user
    When I switch to "users" page
    ${phone_num}  ${extn} =  I add user   &{TestUser}
    I verify that User exist in user table   &{TestUser}
    sleep    10

    #########################Add New Location #################################
    And I switch to "accountdetails" page
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    log many  ${params}
    And I switch to "geographic_locations" page
    And I create geographic location    &{geolocation_US}
    Then I verify location "${geolocation_US['Location']}" with "Registered" state
    sleep   10
    ############################################################################
    # connect to M5DB and fetch the UserUUID and Location uuid details from m5db
    When I connect db  &{log_info_m5db}

	${query}=  set variable  select UserUuid from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db_person}=  I query db  ${query}
    log many  @{data_m5db_person}
    ${query}=  set variable  select LocationUuid from Location where AccountId=${params["account_id"]} and Name=\'${geolocation_US['Location']}\';
    @{data_m5db_locationdata}=  I query db  ${query}
    log many  @{data_m5db_locationdata}

    #####################  Verify SC Log and data from SC for Lacation and Users#############################

    ###########User################
        # Verify the log in UC-TDS
    And I verify log details of summitcloud db  idms  ${data_m5db_person[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info_idms_sc}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info_idms_sc}  condition  ${TestUser["au_username"]}?${temp}
    @{data_uc_idms}=  I fetch data from summit cloud db  &{url_info_idms_sc}
    log many  @{data_uc_idms}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_person[0]['UserUuid']}
    Then I compare and varify ${test_data} with ${data_uc_idms} for table users
   ############Location#################
    # Verify the Location related log in UC-LOC
    And I verify log details of summitcloud db  loc  ${data_m5db_locationdata[0]['LocationUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC
    # Request Format - "http://default:1234@10.32.128.43:18085/locations/913c8445-fb33-4a40-adb0-628d3747c188"
    &{url_info_loc_sc}=  copy dictionary    ${UC_LOC_TBL_LOCATIONS_URL}
    set to dictionary  ${url_info_loc_sc}  condition  ${data_m5db_locationdata[0]['LocationUuid']}
    @{data_uc_loc}=  I fetch data from summit cloud db  &{url_info_loc_sc}
    log many  @{data_uc_loc}

    # Verify the UC data
    set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationdata[0]['LocationUuid']}
    #set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc_loc} for table locations
    #########################################################################################################

    # Now Close the user and check the changes
    When I switch to "users" page
    And I delete user ${TestUser["au_username"]} as user "${request_by}"

	#close the Location from Geographic location
    I switch to "order" page
    I close open order for location "${geolocation_US['Location']}"
    I switch to "geographic_locations" page

    Then I close the location "${geolocation_US['Location']}" requested by "${request_by}"

	####################################Get log frmom M5db_Eventpropagator############################
	When I connect db  &{log_info_m5db}
	${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_person[0]['UserUuid']}\'
    @{data_m5db_EventPropagation_user}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_user}

    log many  ${data_m5db_EventPropagation_user[0]}
    log many  ${data_m5db_EventPropagation_user[1]}

    ${query}=  set variable  select Payload from log_EventPropagation where EntityGuid=\'${data_m5db_person[0]['UserUuid']}\'
    @{data_m5db_EventPropagation_payload_user}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload_user}

    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_locationdata[0]['LocationUuid']}\'
    @{data_m5db_EventPropagation_loc}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_loc}

    log many  ${data_m5db_EventPropagation_loc[0]}
    log many  ${data_m5db_EventPropagation_loc[1]}

    ${query}=  set variable  select Payload from log_EventPropagation where EntityGuid=\'${data_m5db_locationdata[0]['LocationUuid']}\'
    @{data_m5db_EventPropagation_payload_loc}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload_loc}
    ##################### Add New Contract and services ##########

	# add and confirm a new contract
    set to dictionary  ${TestContract}  class  access
    set to dictionary  ${TestContract}  product  MiCloud Connect Telephony
    set to dictionary  ${TestContract}  get_account_info  ${True}

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
    sleep  2
    And I provision initial order
    sleep  2

    # Activate the services
    When I switch to "services" page
    And I activate all service
    sleep  5

    ${request_user}=  Set Variable  ${TestContract["firstName"]}${SPACE}${TestContract["lastName"]}
    set to dictionary  ${ADD_ON_FEATURE}  RequestedBy  ${request_user}
   # Activate the add on feature Connect Archiving
    When I switch to "addonfeatures" page
    And I activate Add-On features  &{ADD_ON_FEATURE}
    sleep  2
##################################################################################
    # connect to and fetch the Account Uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${TestContract["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}

    # fetch the service details from m5db
    ${query}=  set variable  select * from service_service where AccountId=${TestContract["account_id"]}
    @{data_m5db_servicedata}=  I query db  ${query}
    log many  @{data_m5db_servicedata}

    ########################### Verify log and SC Data for Account and Service####################
    # Verify the service related log in UC-SES
    And I verify log details of summitcloud db  ses  ${data_m5db_servicedata[0]['ServiceUuid']}  &{UC_VM_LOGIN}

    # fetch the service data from UC
    # Request Format - "http://default:1234@10.32.128.43:18086/v2/services/services:access:cosmo:telephony"
    &{url_info_ses}=  copy dictionary  ${UC_SES_TBL_SERVICES_URL}
    ${condition}=  set variable  services:access:cosmo:telephony/tenants/${data_m5db_accountguid[0]['AccountGuid']}
    set to dictionary  ${url_info_ses}  condition  ${condition}
    @{data_uc_ses}=  I fetch data from summit cloud db  &{url_info_ses}
    log many  @{data_uc_ses}

    # Verify the UC data
     set to dictionary  ${test_data}  UserUuid  ${None}
    set to dictionary  ${test_data}  ServiceUuid  ${data_m5db_servicedata[0]['ServiceUuid']}
    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc_ses} for table services

    # Verify the Account related log in UC-TDS
    And I verify log details of summitcloud db  tds  ${data_m5db_accountguid[0]['AccountGuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/tenants/245c68a4-425a-4acf-a6a6-113b480b20ce"
    &{url_info_tds}=  copy dictionary  ${UC_TDS_TBL_TENANTS_URL}
    set to dictionary  ${url_info_tds}  condition  ${data_m5db_accountguid[0]['AccountGuid']}
    @{data_uc_tenant}=  I fetch data from summit cloud db  &{url_info_tds}
    log many  @{data_uc_tenant}

    # Verify the UC data
    set to dictionary  ${test_data}  uuid  ${data_m5db_accountguid[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc_tenant} for table tenants

    ################ Close Account and services #####################
    # Close Service Connect Archiving
    Then I switch to "services" page
    &{service_info}=  create dictionary  serviceName=Connect Archiving
    ...  serviceStatus=Active   requested_by=${request_user}  request_source=Email
    ...  ReturnSuccessIfNoRowSelected=${True}
    And I close services  &{service_info}

    #Close Contract/Account
    I close orders and contract
#################################################################################
    # connect M5DB and fetch data from log_eventpropagation table
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_accountguid[0]['AccountGuid']}\'
    @{data_m5db_EventPropagation_account}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_account}

    log many  ${data_m5db_EventPropagation_account[0]}
    log many  ${data_m5db_EventPropagation_account[1]}

    ${query}=  set variable  select Payload from log_EventPropagation where EntityGuid=\'${data_m5db_accountguid[0]['AccountGuid']}\'
    @{data_m5db_EventPropagation_payload_account}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload_account}

  # connect M5DB and fetch data from log_eventpropagation table
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_servicedata[0]['ServiceUuid']}\'
    @{data_m5db_EventPropagation_service}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_service}

    log many  ${data_m5db_EventPropagation_service[0]}
    log many  ${data_m5db_EventPropagation_service[1]}

    ${query}=  set variable  select Payload from log_EventPropagation where EntityGuid=\'${data_m5db_servicedata[0]['ServiceUuid']}\'
    @{data_m5db_EventPropagation_payload_service}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload_service}
   ####################################################################

   # fetch the Users data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Tenants"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info_user1}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Users
    set to dictionary  ${url_info_user1}  condition  ?${temp}
    set to dictionary  ${url_info_user1}  option  failed
	#set to dictionary  ${url_info_user1}  orderby  asc
    set to dictionary  ${url_info_user1}  StartDate  ${data_m5db_EventPropagation_user[0]['DateCreated']}
    set to dictionary  ${url_info_user1}  EndDate  ${data_m5db_EventPropagation_user[1]['DateModified']}

    @{data_uc_backsync_user}=  I fetch data from back sync db  &{url_info_user1}
    log many  @{data_uc_backsync_user}
   ######################################################################
   # fetch the location data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Users"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info_loc1}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Users
    set to dictionary  ${url_info_loc1}  condition  ?${temp}
    set to dictionary  ${url_info_loc1}  option  failed
	#set to dictionary  ${url_info_loc1}  orderby  asc
    set to dictionary  ${url_info_loc1}  StartDate  ${data_m5db_EventPropagation_loc[0]['DateCreated']}
    set to dictionary  ${url_info_loc1}  EndDate  ${data_m5db_EventPropagation_loc[1]['DateModified']}

    @{data_uc_backsync_loc}=  I fetch data from back sync db  &{url_info_loc1}
    log many  @{data_uc_backsync_loc}
    #####################################################################
	# fetch the Account data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Tenants"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info_account1}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Tenants
    set to dictionary  ${url_info_account1}  condition  ?${temp}
    set to dictionary  ${url_info_account1}  option  failed
	#set to dictionary  ${url_info_account1}  orderby  desc
    set to dictionary  ${url_info_account1}  StartDate  ${data_m5db_EventPropagation_account[0]['DateCreated']}
    set to dictionary  ${url_info_account1}  EndDate  ${data_m5db_EventPropagation_account[1]['DateModified']}

    @{data_uc_backsync_account}=  I fetch data from back sync db  &{url_info_account1}
    log many  @{data_uc_backsync_account}

	################################################################
    # fetch the Services data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Services"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info_ses1}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Services
    set to dictionary  ${url_info_ses1}  condition  ?${temp}
    set to dictionary  ${url_info_ses1}  option  failed
	#set to dictionary  ${url_info_ses1}  orderby  asc
    set to dictionary  ${url_info_ses1}  StartDate  ${data_m5db_EventPropagation_service[0]['DateCreated']}
    set to dictionary  ${url_info_ses1}  EndDate  ${data_m5db_EventPropagation_service[1]['DateModified']}

    @{data_uc_backsync_ses}=  I fetch data from back sync db  &{url_info_ses1}
    log many  @{data_uc_backsync_ses}
######################################################################################

     [Teardown]  Run Keywords  I log off
     ...                       I check for alert



*** Keywords ***
I close orders and contract

    When I switch to "order" page
    And I close all order
    When I switch to "accounts" page
    And I close contract  ${TestContract["accountName"]}   ${TestContract["firstName"]}${SPACE}${TestContract["lastName"]}
#    Then I verify contract "${TestContract["accountName"]}" is deleted

Set Init Env
    ${uni_num1}=    Generate Random String    6    [NUMBERS]
    ${uni_str1}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${TestUser}=    create dictionary

    Set suite variable    ${uni_str1}
    Set suite variable    ${uni_num1}
    Set suite variable    ${TestUser}

    set to dictionary  ${TestUser}  &{BillingProfUser}


    : FOR    ${key}    IN    @{TestUser.keys()}
    \    ${updated_val}=    Replace String    ${TestUser["${key}"]}    {rand_str}    ${uni_str1}
    \    Set To Dictionary    ${TestUser}    ${key}    ${updated_val}

    log to console  ${TestUser}

 ################LOCation################################
	${uni_str2}=     Generate Random String    8    [LETTERS][NUMBERS]
    Set suite variable    ${uni_str2}
    Set suite variable      ${geolocation_US}

    : FOR    ${key}    IN    @{geolocation_US.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_US["${key}"]}    {rand_str}    ${uni_str2}
    \    Set To Dictionary    ${geolocation_US}    ${key}    ${updated_val}
	log to console  ${geolocation_US}

##################### Account/Service##################################
    ${uni_num3}=    Generate Random String    6    [NUMBERS]
    ${uni_str3}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${TestContract}=    create dictionary

    Set suite variable    ${uni_str3}
    Set suite variable    ${uni_num3}
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
    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str3}
    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}
