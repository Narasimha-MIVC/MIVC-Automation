*** Settings ***
Documentation    Verify global user service is able to close
...               dev-Vasuja
...
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot

Resource    ../GlobalUser/Variables/global_variables.robot
Resource    ../../Variables/UserInfo.robot
Resource    ../../Variables/ServiceInfo.robot


Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***

1. Global User : Verify global user service is able to close
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    Then I switch to "users" page
    Set to Dictionary    ${DMProfUser}    au_userlocation    ${GlobalUserLocation}
    Set to Dictionary    ${DMProfUser}    au_location    ${GlobalUserBillingLoc}
    Set to Dictionary    ${DMProfUser}    request_by    ${request_by}
    Set to Dictionary    ${DMProfUser}    request_source    Email
    ${phone_num}  ${extn}=    and I add user    &{DMProfUser}
    Set to Dictionary    ${globaluser_userservice}    parent    ${phone_num}
    Set to Dictionary    ${globaluser_userservice}    serviceStatus    Active
    And I switch to "services" page
    And I update service status     &{globaluser_userservice}
    Set to Dictionary    ${globaluser_close_service}    requested_by    ${request_by}
    And I switch to "services" page
    Set to Dictionary    ${globaluser_close_service}    parent    ${phone_num}
    Set to Dictionary    ${globaluser_close_service}    keepGlobalTn    verify
    And I close global user service     &{globaluser_close_service}
   [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${usr_str}=    Generate Random String    4    [LETTERS][NUMBERS]
    Set suite variable    &{DMProfUser}
    : FOR    ${key}    IN    @{DMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${DMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${DMProfUser}    ${key}    ${updated_val}


