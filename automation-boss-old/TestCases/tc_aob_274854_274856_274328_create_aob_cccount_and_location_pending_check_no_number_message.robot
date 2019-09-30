*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot

#Variable filesot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***
Login as Staff with +QA and Kramer account
    [Tags]  Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "accounts" page
    log to console   ${ContractAOB["filePath"]}
    and I add contract    &{ContractAOB}
    Then I verify "company_name" contains "${ContractAOB["accountName"]}"
    Log  "Account ${ContractAOB["accountName"]} created"
    and I verify grid contains "Ordered" value
    When I click on "${ContractAOB["accountType"]}" link in "contract_grid"
    ${order_number}=   I confirm the contract with instance "${bossCluster} (${platform})" and location "${ContractAOB["locationName"]}"
    Set suite variable    ${order_number}
    Then I switch to "contracts" page
    #and I verify contract "${ContractAOB["accountName"]}" with "Confirmed" state
    then I check if mitel easy setup link enable

Location Pending
    [Tags]  Regression
    When I switch to "geographic_locations" page
    And I verify location status of "${ContractAOB["locationName"]}"
    then I check if mitel easy setup link enable

Add Users - Phone Number - Selection and Text Change on No Available TNs
    [Tags]  Regression
    When I switch to "aob" page
    Then I verify the page "Welcome"
    When I navigate to Location and user page
    and I verify the page "Locations and User"
    Then I go to add user page
    and I verify the page "Users for"
    and I verify "There are no available numbers" is displayed on screen
*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    4    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}

    Set suite variable    &{ContractAOB}
    : FOR    ${key}    IN    @{ContractAOB.keys()}
    \    ${updated_val}=    Replace String    ${ContractAOB["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${ContractAOB}    ${key}    ${updated_val}

    Set suite variable    &{ContractAOB}
    : FOR    ${key}    IN    @{ContractAOB.keys()}
    \    ${updated_val}=    Replace String    ${ContractAOB["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${ContractAOB}    ${key}    ${updated_val}