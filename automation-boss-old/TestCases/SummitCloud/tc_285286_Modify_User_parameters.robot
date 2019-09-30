*** Settings ***
Documentation    Publish updates to IDMS schema attributes to IDMS for a given user - Modify User through add profile
...              Author: Priyanka Mishra

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
Library  DateTime

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

    # connect to M5DB and fetch the Person information from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select * from Person where Username=\'${TestUser["au_username"]}\'
    @{data_m5db_person_old}=  I query db  ${query}

    # Verify the log in UC-IDMS
    And I verify log details of summitcloud db  idms  ${data_m5db_person_old[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info}  condition  ${TestUser["au_username"]}?${temp}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_person_old[0]['UserUuid']}
    And I compare and varify ${test_data} with ${data_uc} for table users

    # Right click on user to get personal information
    I perform right click on a "Personal Information" for user with email "${TestUser["au_businessmail"]}"
    # Prasanna: Added this line
    set to dictionary  ${TestUser_updated}  &{TestUser}
    set to dictionary  ${TestUser_updated}    au_lastname    AutoNew
    I edit user personal information    &{TestUser_updated}

  # connect to M5DB and fetch the Person updated information from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select UserUuid,Username,FirstName,LastName,PersonalEmail,BusinessEmail from Person where Username=\'${TestUser_updated["au_username"]}\'
    @{data_m5db_person_new}=  I query db  ${query}
    sleep   5
    log many  @{data_m5db_person_new}
    # verify the User UUID from M5DB for user data and updated user data , it should be same
    should be equal  ${data_m5db_person_old[0]['UserUuid']}  ${data_m5db_person_new[0]['UserUuid']}

    # Verify that the date and time of modification for the Location update and the status
    log many  @{data_m5db_person_new}
    log many  @{data_m5db_person_old}

    # Verify the log in UC-IDMS
    And I verify log details of summitcloud db  idms  ${data_m5db_person_new[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info1}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info1}  condition  ${TestUser_updated["au_username"]}?${temp}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info1}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db_person_new[0]['UserUuid']}
    And I compare and varify ${test_data} with ${data_uc} for table users


    [Teardown]  Run Keywords  I switch to "users" page
    ...                       AND  I delete user ${TestUser["au_username"]} as user "${request_by}"
    ...                       AND  I log off
    ...                       AND  I check for alert

*** Keywords ***
Set Init Env
    ${uni_num1}=    Generate Random String    6    [NUMBERS]
    ${uni_str1}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_num2}=    Generate Random String    6    [NUMBERS]
    ${uni_str2}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${TestUser}=    create dictionary
    ${TestUser_updated}=    create dictionary

    Set suite variable    ${uni_str1}
    Set suite variable    ${uni_num1}
    Set suite variable    ${TestUser}
    Set suite variable    ${TestUser_updated}
    Set suite variable    ${uni_str2}
    Set suite variable    ${uni_num2}

    set to dictionary  ${TestUser}  &{BillingProfUser}
    # Prasanna: Commented the below line
#    set to dictionary  ${TestUser_updated}  &{BillingProfUser}

    : FOR    ${key}    IN    @{TestUser.keys()}
    \    ${updated_val}=    Replace String    ${TestUser["${key}"]}    {rand_str}    ${uni_str1}
    \    Set To Dictionary    ${TestUser}    ${key}    ${updated_val}

    log to console  ${TestUser}
    # Prasanna: Commented the below lines
#     : FOR    ${key}    IN    @{TestUser_updated.keys()}
#    \    ${updated_val}=    Replace String    ${TestUser_updated["${key}"]}    {rand_str}    ${uni_str2}
#    \    Set To Dictionary    ${TestUser_updated}    ${key}    ${updated_val}
#
#    log to console  ${TestUser_updated}