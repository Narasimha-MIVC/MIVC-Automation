*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource    ../../RobotKeywords/BossKeywords.robot

#Variable files
Resource          ../GlobalUser/Variables/global_variables.robot
Resource    ../../Variables/EnvVariables.robot

#Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections
*** Test Cases ***
1. Global User : Void Global User - KeepTn - no
    [Tags]    GlobalUser    NonSmr
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    And I switch to "phone_systems_phone_numbers" page
    ${phone_num}=    I find phone number with required status    Available  country=AUS (+61)  type=Global User

    # adding global user
    And I switch to "users" page
    Log    ${DMUser}    console=yes
    #Setting varaiables to dictionary
    set to dictionary   ${DMUser}   global_countries    ${global_countries}
    set to dictionary   ${DMUser}   au_userlocation    ${GlobalUserLocation}
    Set to Dictionary   ${DMUser}   ap_phonenumber    ${phone_num}
    set to dictionary   ${DMUser}   au_location    ${GlobalUserBillingLoc}
    set to dictionary   ${DMUser}   request_by    ${request_by}
    ${phone_num}  ${extn}=    and I add user    &{DMUser}

    And I switch to "services" page
    then I verify the page "services"
    set to dictionary   ${globaluser_void}   parent    ${phone_num}
    ${serviceTn}=  I void global user service   &{globaluser_void}

    And I switch to "switch_account" page
    And I switch to account ${systemAccount} with ${AccWithoutLogin} option
    And I switch to "phonenumber" page
    then I verify the page "Phone Numbers"
    # while voiding expectedTnStatus will be Turned Down for pending port in numbers,
    #here we are taking available number
    set to dictionary   ${globaluser_void}   expectedTnStatus    Pending port out
    then I verify status of ${serviceTn}     &{globaluser_void}
    [Teardown]  run keywords  I log off
    ...                      I check for alert
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{DMUser}
    : FOR    ${key}    IN    @{DMUser.keys()}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}


