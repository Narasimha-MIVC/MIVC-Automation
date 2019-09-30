*** Settings ***
Documentation    Event Persistence - Validation of idms logging - Failure of Summit Cloud - idms
...              Author: Priyanka Mishra
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
#Library           ../../../Framework/provisioning_wrappers/boss_wrappers/boss_api.py    WITH NAME    BOSS


#Built in library
Library  String
Library  Collections

*** Variables ***
&{test_data}  UserUuid=${None}

*** Test Cases ***
Event Persistence - Validation of idms logging - Failure of Summit Cloud - idms
    [Tags]    DEBUG

    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    # Get Detail of UC DBCONNECT
    &{Uc_Details}=  copy dictionary  ${UC_VM_LOGIN}
    ${data_uc}=  create dictionary  fetched_data=${None}
    set to dictionary  ${Uc_Details}  uc_db_data=${data_uc}

    # stop container IDMS
    I stop docker container  ${IDMS_CONTAINER_ID}  &{Uc_Details}
    log many  &{data_uc}
    sleep  10
    ################### Login to Boss URL and Add user ###############
    set to dictionary  ${TestUser}    au_userlocation    ${locationName}
    Set to Dictionary  ${TestUser}    request_by    ${request_by}
    Set to Dictionary  ${TestUser}    request_source    Email
    Set to Dictionary  ${TestUser}    role    Technical
#    set to Dictionary  ${TestUser}    ph_num_chk_box   Yes
#    Set to Dictionary  ${TestUser}    assign_new_number    ${True}
    Set to Dictionary  ${TestUser}    skip_add_phone  ${True}

    # Log-in to BOSS and a particular account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
   # Add user
    When I switch to "users" page
    ${phone_num}  ${extn} =  I add user   &{TestUser}
    I verify that User exist in user table   &{TestUser}

    ##############################################################################

    # connect to M5DB and fetch the UserUuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select UserUuid from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db}=  I query db  ${query}
    log many  @{data_m5db}
    #  fetch the isSuccess value from m5db.[log_EventPropagation] table
    ${query}=  set variable  select * from log_EventPropagation where EntityGuid=\'${data_m5db[0]['UserUuid']}\'
    @{data_m5db_EventPropagation}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation}
    log  ${data_m5db_EventPropagation[0]['IsSuccess']}
    ${value}=  Evaluate  $data_m5db_EventPropagation[0].get("IsSuccess")
    # verify the isSuccess value from M5DB.log_EventPropagation for new User and it should be False i.e 0
    should be equal  ${data_m5db_EventPropagation[0]['IsSuccess']}  ${False}
    # Verify the log in UC-TDS

    And I verify log details of summitcloud db  idms  ${data_m5db[0]['UserUuid']}  &{UC_VM_LOGIN}


    [Teardown]  Run Keywords  I start docker container  &{Uc_Details}
    ...                       AND  I switch to "users" page
    ...                       AND  I delete user ${TestUser["au_username"]} as user "${request_by}"
    ...                       AND  I log off
    ...                       AND  I check for alert

*** Keywords ***
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



