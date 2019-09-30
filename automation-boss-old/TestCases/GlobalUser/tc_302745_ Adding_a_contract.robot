*** Settings ***
Documentation    Suite description
#...               dev-Tantri Tanisha ,Susmitha
...

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../GlobalUser/Variables/global_variables.robot
Resource          ../../Variables/ContractInfo.robot


#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}   country=${country}
Library  String
Library  Collections
*** Test Cases ***

02 Login to the boss portal and create contract
    [Tags]    GlobalUser    NonSmr
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "accounts" page
    log to console   ${TestContract["filePath"]}
    log to console   ${TestContract}
    log to console   ${country}
    and I add contract    &{TestContract}
    Then I verify "company_name" contains "${TestContract["accountName"]}"
    Log  "Account ${TestContract["accountName"]} created"
    and I verify grid contains "Ordered" value
    When I click on "${TestContract["accountType"]}" link in "contract_grid"
    ${order_number}=   and I confirm the contract with instance "${bossCluster} (${platform})" and location "${TestContract["locationName"]}"
    Set suite variable    ${order_number}
    Then I switch to "contracts" page
    and I verify contract "${TestContract["accountName"]}" with "Confirmed" state
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${TestContract}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    ${TestContract}

    Run keyword if    '${country}' == 'Australia'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}  &{Contract_Aus}


            ...    ELSE IF    '${country}' == 'UK'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}  &{Contract_UK}


            ...    ELSE IF    '${country}' == 'US'
            ...    Run Keywords
            ...    set to dictionary  ${TestContract}   &{Contract02}
            ...    AND    log to console     "==============DEBUG================"
            ...    AND    log to console     ${TestContract}

            ...    ELSE
            ...    log  Please enter a valid Country name like US, UK or Australia

    : FOR    ${key}    IN    @{TestContract.keys()}
    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}



    