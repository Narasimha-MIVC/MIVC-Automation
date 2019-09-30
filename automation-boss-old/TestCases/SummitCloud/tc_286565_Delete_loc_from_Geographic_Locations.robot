*** Settings ***
Documentation    Locations Delete - Delete location from Geographic Locations
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
Close Location as Staff User
    [Tags]    DEBUG

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
    and I switch to "geographic_locations" page
    and I create geographic location    &{geolocation_US}
    Then I verify location "${geolocation_US['Location']}" with "Registered" state


    # connect to and fetch the uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${params["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}

    # fetch the Location details from m5db
    ${query}=  set variable  select * from Location where AccountId=${params["account_id"]} and Name=\'${geolocation_US['Location']}\';
    @{data_m5db_locationdata}=  I query db  ${query}
    log many  @{data_m5db_locationdata}
    # Verify the location related log in UC-LOC
    And I verify log details of summitcloud db  loc  ${data_m5db_locationdata[0]['LocationUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC
    # Request Format - "http://default:1234@10.32.128.43:18085/locations/913c8445-fb33-4a40-adb0-628d3747c188"
    &{url_info}=  copy dictionary    ${UC_LOC_TBL_LOCATIONS_URL}
    set to dictionary  ${url_info}  condition  ${data_m5db_locationdata[0]['LocationUuid']}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationdata[0]['LocationUuid']}
    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table locations

    #close the Location from Geographic location
    I switch to "order" page
    I close open order for location "${geolocation_US['Location']}"
    I switch to "geographic_locations" page

    Then I close the location "${geolocation_US['Location']}" requested by "${request_by}"

    # Again querying the M5DB and get the status of geographic location and the date of modification of the location data
    When I connect db  &{log_info_m5db}
#    ${query}=  set variable  SELECT  [LocationStatus].Name,*
#    ...            FROM [Location]
#    ...            INNER JOIN [LocationStatus]
#    ...            on [LocationStatus].Id =[Location].LocationStatusId
#    ...            where [Location].LocationStatusId= '1' and Name=\'${geolocation_US['Location']}\';
    ${query}=  set variable  select * from Location where AccountId=${params["account_id"]} and Name=\'${geolocation_US['Location']}\';

    @{data_m5db_locationdata_new}=  I query db  ${query}
    #log many  @{data_m5db_locationdata_new}
    # Verify that the date and time of modification for the Location update and the status
    log many  @{data_m5db_locationdata}
    log many  @{data_m5db_locationdata_new}

    # Verify the Location related log in UC-LOC
    And I verify log details of summitcloud db  loc  ${data_m5db_locationdata_new[0]['LocationUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC
    # Request Format - "http://default:1234@10.32.128.43:18085/locations/913c8445-fb33-4a40-adb0-628d3747c188"
    &{url_info1}=  copy dictionary    ${UC_LOC_TBL_LOCATIONS_URL}
    set to dictionary  ${url_info1}  condition  ${data_m5db_locationdata_new[0]['LocationUuid']}
    @{data_uc_new}=  I fetch data from summit cloud db  &{url_info1}
    log many  @{data_uc_new}

    # Check whether column IsSuccess exists in table log_EventPropagation
    ${value}=  Evaluate  $data_m5db_locationdata_new[0].get("LocationStatusId")
    log  ${data_m5db_locationdata_new[0]['LocationStatusId']}
    # verify the isSuccess value from M5DB.log_EventPropagation for new Location and it should be False i.e 0
    #Run Keyword if  should be true  ${value}   1
    set to dictionary  ${test_data}  status  closed
    # Verify the UC data
    set to dictionary  ${test_data}  LocationUuid  ${data_m5db_locationdata_new[0]['LocationUuid']}
    set to dictionary  ${test_data}  AccountGuid  ${data_m5db_accountguid[0]['AccountGuid']}
    log many  &{geolocation_US}
    log many  &{test_data}

    Then I compare and varify ${test_data} with ${data_uc_new} for table locations

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    #${uni_num}=    Generate Random String    6    [NUMBERS]
    #${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_str}=     Generate Random String    8    [LETTERS][NUMBERS]
    Set suite variable      ${geolocation_US}
    Set suite variable    ${uni_str}

    : FOR    ${key}    IN    @{geolocation_US.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_US["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${geolocation_US}    ${key}    ${updated_val}

