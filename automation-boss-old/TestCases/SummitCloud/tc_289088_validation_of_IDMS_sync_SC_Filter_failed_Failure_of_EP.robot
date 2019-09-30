*** Settings ***
Documentation    Validation of idms sync SC with Filter as failed- Failure of EventPropagator
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
Validation of idms sync SC with Filter as failed- Failure of EventPropagator
    [Tags]    DEBUG

    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

    # Get Detail of UC DBCONNECT
    &{Uc_Details}=  copy dictionary  ${UC_VM_LOGIN}
    ${data_uc}=  create dictionary  fetched_data=${None}
    set to dictionary  ${Uc_Details}  uc_db_data=${data_uc}

    # stop container EventPopagator
    I stop docker container  ${EVENT_PROP_CONTAINER_ID}  &{Uc_Details}
    log many  &{Uc_Details}
    sleep  2
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

    # connect to and fetch the UserUuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db}=  I query db  ${query}
    log many  @{data_m5db}
    # connect to and fetch the  details from m5db eventpropagation
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select EntityGuid from log_EventPropagation where EntityName='Person'
    @{data_m5db_EventPropagation}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation}
    ${query}=  set variable  select Payload from log_EventPropagation where EntityName='Person'
    #where EntityGuid=\'${data_m5db[0]['UserUuid']}\'
    @{data_m5db_EventPropagation_payload}=  I query db  ${query}
    log many  @{data_m5db_EventPropagation_payload}
    #Check that Newly created user entries should not have loged in log_EventPRopagation”  Table
    should not contain  ${data_m5db_EventPropagation}    ${data_m5db[0]['UserUuid']}

#Commented the validation and after confirmation will validate
#    # fetch the data from UC IDMS Data should not be present in UC-DB IDMS as EventPropagator is down -
#    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
#    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
#    ${temp}=  set variable  type=username
#    set to dictionary  ${url_info}  condition  ${TestUser["au_username"]}?${temp}
#    ${data_uc_IDMS}=  I fetch data from summit cloud db  &{url_info}
#    log  ${data_uc_IDMS}
#    should be true  "404" in """${data_uc_IDMS}"""

    # Restart container EventPopagator
    I start docker container  &{Uc_Details}
    sleep    10
    # fetch the data from UC Back Sync -
    # Request Format - "http://10.198.104.74:3000/api/GetEvents?Type="Users"&Start="2017-12-05 16:04:16.3330"&End="2017-12-05 20:04:16.3330"&Option="all""
    &{url_info1}=  copy dictionary  ${UC_BACK_SYNC_SERVICES_URL}
    ${temp}=  set variable  Type=Users
    set to dictionary  ${url_info1}  condition  ?${temp}
    set to dictionary  ${url_info1}  option  failed
    set to dictionary  ${url_info1}  StartDate  ${data_m5db[0]['DateCreated']}
    set to dictionary  ${url_info1}  EndDate  ${data_m5db[0]['DateModified']}

    @{data_uc_backsync_db}=  I fetch data from back sync db  &{url_info1}
    log many  @{data_uc_backsync_db}

    # Verify the log in UC-IDMS
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

