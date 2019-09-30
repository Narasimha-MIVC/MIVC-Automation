*** Settings ***
Documentation    Create user in BOSS to push user to IDMS with new UUID - Add User through add profile

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

*** Variables ***
&{test_data}  uuid=${None}

*** Test Cases ***
Create user in BOSS to push user to IDMS with new UUID - Add User through add profile

    [Tags]    DEBUG

    # Local test case specific variables
    &{log_info_m5db}=  copy dictionary  ${M5DB_CONN_INFO}
    &{log_info_d2db}=  copy dictionary  ${D2DB_CONN_INFO}

     # Log-in to BOSS and a particular account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Set to Dictionary    ${ProfilePageUser}    profile_loc    ${locationName}
    Set to Dictionary    ${ProfilePageUser}    request_by    ${request_by}
    Set to Dictionary    ${ProfilePageUser}    request_source    Email
    ${extn} =  I add user from profiles tab   &{ProfilePageUser}
    When I switch to "users" page
    And I verify the User exist in user table created from profiles page    &{ProfilePageUser}

    # connect to and fetch the UserUuid from m5db
    When I connect db  &{log_info_m5db}
    ${query}=  set variable  select UserUuid from Person where Username=\'${ProfilePageUser["profile_mail"]}\'
    @{data_m5db}=  I query db  ${query}
    log many  @{data_m5db}
    # Get the tenant info from D2 and verify
#    And I connect db  &{log_info_d2db}
#    ${query}=  set variable  select * from users where GuiLoginName=\'${ProfilePageUser["profile_mail"]}\'
#    @{data_d2db}=  I query db  ${query}
#    log many  @{data_d2db}

    # Verify the log in UC-TDS
    And I verify log details of summitcloud db  idms  ${data_m5db[0]['UserUuid']}  &{UC_VM_LOGIN}

    # fetch the data from UC IDMS -
    # Request Format - "http://default:1234@10.32.128.43:18085/v2/users/sample.test72@jj.com?type=username"
    &{url_info}=  copy dictionary  ${UC_IDMS_TBL_USERS_URL}
    ${temp}=  set variable  type=username
    set to dictionary  ${url_info}  condition  ${ProfilePageUser["profile_mail"]}?${temp}
    @{data_uc}=  I fetch data from summit cloud db  &{url_info}
    log many  @{data_uc}

    # Verify the UC data
    set to dictionary  ${test_data}  UserUuid  ${data_m5db[0]['UserUuid']}
    Then I compare and varify ${test_data} with ${data_uc} for table users

    [Teardown]  Run Keywords  I switch to "users" page
    ...                       AND  I delete user ${ProfilePageUser["profile_mail"]} as user "${request_by}"
    ...                       AND  I log off
    ...                       AND  I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${ProfilePageUser}

    : FOR    ${key}    IN    @{ProfilePageUser.keys()}
    \    ${updated_val}=    Replace String    ${ProfilePageUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${ProfilePageUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${ProfilePageUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${ProfilePageUser}    ${key}    ${updated_val}

    log to console  ${ProfilePageUser}