*** Settings ***
Documentation    Validation of loc delete sync SC with Filter as failed - Success of EventPropagator-
...              eventpropagator to SC Failed
...              Author: Priyanka Mishra

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/SummitCloudKeywords.robot

Resource           ../../Variables/EnvVariables.robot
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
Validation of loc delete sync SC with Filter as failed - Success of EventPropagator-eventpropagator to SC Failed

    [Tags]    DEBUG     SC

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    # Log-in to BOSS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

    # create an Geographic location
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "accountdetails" page
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    log many  ${params}
    And I switch to "geographic_locations" page
    And I create geographic location    &{geolocation_US}
    Then I verify location "${geolocation_US['Location']}" with "Registered" state
    sleep   10

    # connect to and fetch the Location uuid details from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${params["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}
    ${query}=  set variable  select LocationUuid from Location where AccountId=${params["account_id"]} and Name=\'${geolocation_US['Location']}\';
    @{data_m5db_locationdata}=  I query db  ${query}
    log many  @{data_m5db_locationdata}

    #close the container loc
    # Get Detail of UC DBCONNECT
    &{Uc_Details}=  copy dictionary  ${UC_VM_LOGIN}
    ${data_uc}=  create dictionary  fetched_data=${None}
    set to dictionary  ${Uc_Details}  uc_db_data=${data_uc}

   # stop container LOC
    I stop docker container  ${LOC_CONTAINER_ID}  &{Uc_Details}
    log many  &{Uc_Details}
    sleep  2

    #close the Location from Geographic location
    I switch to "order" page
    I close open order for location "${geolocation_US['Location']}"
    I switch to "geographic_locations" page

    Then I close the location "${geolocation_US['Location']}" requested by "${request_by}"

    # connect to and fetch the  details from m5db eventpropagation
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_locationdata[0]['LocationUuid']}\'
    @{data_m5db_EventPropagation}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation}

    log many  ${data_m5db_EventPropagation[0]}
    log many  ${data_m5db_EventPropagation[1]}

    ${query}=  set variable  select Payload from log_EventPropagation where EntityGuid=\'${data_m5db_locationdata[0]['LocationUuid']}\'
    @{data_m5db_EventPropagation_payload}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload}


    # Verify the Location related log in UC-LOC
    And I verify log details of summitcloud db  loc  ${data_m5db_locationdata[0]['LocationUuid']}  &{UC_VM_LOGIN}

     # fetch the data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Locations"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info1}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Locations
    set to dictionary  ${url_info1}  condition  ?${temp}
    set to dictionary  ${url_info1}  option  failed
    set to dictionary  ${url_info1}  StartDate  ${data_m5db_EventPropagation[0]['DateCreated']}
    set to dictionary  ${url_info1}  EndDate  ${data_m5db_EventPropagation[1]['DateModified']}

    @{data_uc_backsync}=  I fetch data from back sync db  &{url_info1}
    log many  @{data_uc_backsync}

# Commented below Validaton Need to Confirm before Adding
#    # start the container loc
#    I start docker container  &{Uc_Details}
#    sleep   10
#
#    # fetch the data from UC it should not logged to DB
#    # Request Format - "http://default:1234@10.32.128.43:18085/locations/913c8445-fb33-4a40-adb0-628d3747c188"
#    &{url_info}=  copy dictionary    ${UC_LOC_TBL_LOCATIONS_URL}
#    set to dictionary  ${url_info}  condition  ${data_m5db_locationdata[0]['LocationUuid']}
#    @{data_uc_LOC}=  I fetch data from summit cloud db  &{url_info}
#    log many  @{data_uc_LOC}
#
#    # Verify the UC data
#    set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationdata[0]['LocationUuid']}
#    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
#    Then I compare and varify ${test_data} with ${data_uc_LOC} for table locations



    [Teardown]  Run Keywords  I start docker container  &{Uc_Details}
    ...                       AND  I log off
    ...                       AND  I check for alert


*** Keywords ***

Set Init Env
    ${uni_str}=     Generate Random String    8    [LETTERS][NUMBERS]
    Set suite variable      ${geolocation_US}
    Set suite variable    ${uni_str}

    : FOR    ${key}    IN    @{geolocation_US.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_US["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${geolocation_US}    ${key}    ${updated_val}




