*** Settings ***
Documentation    Event Persistence - Validation of loc logging - Failure of Summit Cloud - loc
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
Event Persistence - Validation of loc logging - Failure of Summit Cloud - loc
    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    # Get Detail of UC DBCONNECT
    &{Uc_Details}=  copy dictionary  ${UC_VM_LOGIN}
    ${data_uc}=  create dictionary  fetched_data=${None}
    set to dictionary  ${Uc_Details}  uc_db_data=${data_uc}

   # stop container LOC
    I stop docker container  ${LOC_CONTAINER_ID}  &{Uc_Details}
    log many  &{Uc_Details}
    sleep  2

    # Log-in to BOSS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    # create an acount
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

    # connect to and fetch the uuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select AccountGuid from Account where Id=${params["account_id"]}
    @{data_m5db_accountguid}=  I query db  ${query}
    log many  @{data_m5db_accountguid}

    # fetch the Location details from m5db
    ${query}=  set variable  select Name,LocationUuid from Location where AccountId=${params["account_id"]} and Name=\'${geolocation_US['Location']}\';
    @{data_m5db_locationdata}=  I query db  ${query}
    log many  @{data_m5db_locationdata}

    #  fetch the isSuccess value from m5db.[log_EventPropagation] table
    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db_locationdata[0]['LocationUuid']}\'
    #${query}=  set variable  SELECT [Location].Name, * FROM [Location] INNER JOIN [log_EventPropagation] on [Location].LocationUuid =[log_EventPropagation].EntityGuid where [Location].Name=\'${geolocation_US['Location']}\';
    @{data_m5db_EventPropagation}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation}
    log  ${data_m5db_EventPropagation[0]['IsSuccess']}

    # Check whether column IsSuccess exists in table log_EventPropagation
    ${value}=  Evaluate  $data_m5db_EventPropagation[0].get("IsSuccess")

    # verify the isSuccess value from M5DB.log_EventPropagation for new Location and it should be False i.e 0
    should be equal  ${data_m5db_EventPropagation[0]['IsSuccess']}  ${False}

    # Verify the Location related log in UC-LOC
    And I verify log details of summitcloud db  loc  ${data_m5db_locationdata[0]['LocationUuid']}  &{UC_VM_LOGIN}

    [Teardown]  Run Keywords  I start docker container  &{Uc_Details}
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
    ${uni_str}=     Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable      ${geolocation_US}
    Set suite variable    ${uni_str}

    : FOR    ${key}    IN    @{geolocation_US.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_US["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${geolocation_US}    ${key}    ${updated_val}

