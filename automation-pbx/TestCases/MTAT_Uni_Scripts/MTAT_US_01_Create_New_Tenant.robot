*** Settings ***
Documentation     Login to the boss portal and create contract
...               dev - Diksha,Neeraj,Lavanya,Maha
...               Contact : Mahabaleshwar Hegde

#Suite Setup and Teardown
Suite Setup       Set Init Env
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keywords    Test case PostCondition
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../../automation-boss/RobotKeywords/BOSSKeywords.robot
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
#Resource          ../../../Variables/ContractInfo.robot

#Component files
Library           ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}    country=${country}     WITH NAME   Boss
Library          ../../../Framework/phone_wrappers/phone_4xx/PPhoneInterface.py  WITH NAME       w2
Library          ../../lib/PBXComponent.py

*** Test Cases ***
Login to the boss portal and create contract

    [Tags]  MT AT Sanity


     When I switch to "accounts" page
     and I add contract    &{Contract}
     Then I verify "company_name" contains "${Contract["accountName"]}"
     Log  "Account ${Contract["accountName"]} created"
     and I verify grid contains "Ordered" value
     When I click on "${Contract["accountType"]}" link in "contract_grid"
     ${order_number}=   and I confirm the contract with instance "${bossCluster} (${platform})" and location "${Contract["locationName"]}"
     When I switch to "account_details" page
     &{params1}=  create dictionary
     set to dictionary  ${params1}  get_account_id  ${True}
     And I retrieve account details  ${params1}
     ${AccId}=    Set Variable    ${params1["account_id"]}
     #${AccId}=    Set Variable     11553
     Set suite variable     ${AccId}
     Then I switch to "contracts" page
     #and I verify contract "${Contract["accountName"]}" with "Confirmed" state


    #Update variable files
    In Varibale file LoginDetails.robot I update key NewAccId with value ${AccId}
    In Varibale file LoginDetails.robot I update key NewAccName with value ${Contract["accountName"]}
    In Varibale file LoginDetails.robot I update key PhoneNumber with field clientAccount to value ${Contract["accountName"]}
    In Varibale file LoginDetails.robot I update key PhoneNumber with field requestedBy to value ${Contract["firstName"]} ${Contract["lastName"]}
    In Varibale file LoginDetails.robot I update key PhoneNumber with field clientLocation to value ${Contract["locationName"]}
    # In Varibale file PhoneNumberInfo.robot I update key PhoneNumber_US01 with field numberRange to value 15086008455
    In Varibale file LoginDetails.robot I update key PhoneNumber with field range to value 10
    In Varibale file LoginDetails.robot I update key GenUser with field au_userlocation to value ${Contract["locationName"]}
    In Varibale file LoginDetails.robot I update key GenUser with field au_location to value ${Contract["locationName"]}
    In Varibale file LoginDetails.robot I update key GenUser with field request_by to value ${Contract["firstName"]} ${Contract["lastName"]}

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable     &{Contract}
    : FOR    ${key}    IN    @{Contract.keys()}
    \    ${updated_val}=    Replace String    ${Contract["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Contract}    ${key}    ${updated_val}

Test case PreCondition
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

Test case PostCondition
    and I log off
