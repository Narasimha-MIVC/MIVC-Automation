*** Settings ***
Documentation    Verify TN unassigns from an account when Global user service is voided
...               dev-Vasuja
...

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../RobotKeywords/BossKeywords.robot

Resource    ../../Variables/EnvVariables.robot
Resource    ../GlobalUser/Variables/global_variables.robot
Resource    ../../Variables/UserInfo.robot
Resource    ../../Variables/ServiceInfo.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library   string
*** Test Cases ***

1. Global User : Verify TN unassigns from an account when Global user service is voided
    [Tags]    GlobalUser  test    NonSmr
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    And I switch to "phone_systems_phone_numbers" page
    ${phone_num}=    I find phone number with required status    Available  type=Global User  country=AUS (+61)
    I switch to "users" page
    Set to Dictionary    ${DMProfUser}    au_userlocation    ${GlobalUserLocation}
    Set to Dictionary    ${DMProfUser}    au_location    ${GlobalUserBillingLoc}
    Set to Dictionary    ${DMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${DMProfUser}    request_by    ${request_by}
    Set to Dictionary    ${DMProfUser}    request_source    Email
    ${phone_num}  ${extn}=    and I add user    &{DMProfUser}
    Set to Dictionary    ${globaluser_userservice}    parent    ${phone_num}
    Set to Dictionary    ${globaluser_userservice}    serviceStatus    Active
    And I switch to "services" page
    And I update service status     &{globaluser_userservice}
    Then I switch to "services" page
    Set to Dictionary    ${globaluser_service}    servicename    Global User Service
    Set to Dictionary    ${globaluser_service}    parent    ${phone_num}
    ${serviceid}=    And I retrieve service id from service page    &{globaluser_service}
    Set to Dictionary    ${globaluser_close_service}    requested_by    ${request_by}
    And I switch to "services" page
    Set to Dictionary    ${globaluser_close_service}    parent    ${phone_num}
    Set to Dictionary    ${globaluser_close_service}    keepGlobalTn    yes
    And I close global user service     &{globaluser_close_service}
    And I switch to "services" page
    Set to Dictionary    ${globaluser_service}    serviceStatus    Closed
    Set to Dictionary    ${globaluser_service}    serviceid    ${serviceid}
    And I verify service status in service page    &{globaluser_service}
    When I switch to "switch_account" page
    And I switch to account M5Portal Company with ${AccWithoutLogin} option
    And I switch to "phonenumber" page
    then I verify the page "Phone Numbers"
    Set to Dictionary    ${globaluser_void}    expectedTnStatus    Available
    then I verify status of ${phone_num}     &{globaluser_void}
   [Teardown]  run keywords  I log off
   ...                       I check for alert


*** Keywords ***
Set Init Env
    ${usr_str}=    Generate Random String    4    [LETTERS][NUMBERS]
    Set suite variable    &{DMProfUser}
    : FOR    ${key}    IN    @{DMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${DMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${DMProfUser}    ${key}    ${updated_val}

