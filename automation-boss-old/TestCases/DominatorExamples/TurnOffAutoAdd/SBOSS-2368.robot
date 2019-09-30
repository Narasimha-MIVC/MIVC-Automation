*** Settings ***
Documentation   BOSS Turn Off Auto-add
...             SBOSS-2368
...             dev-Jim Wendt

Resource        ../../../RobotKeywords/DominatorKeywords.robot
Resource        ../../../RobotKeywords/NavigationKeywords.robot
Resource        ../../../RobotKeywords/BOSSKeywords.robot

Resource        ../../../Variables/EnvVariables.robot
Resource        ../../AOB/Variables/aob_variables.robot

Library         ../../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment

    ${details}=   Load JSON From File       DominatorExamples/TurnOffAutoAdd/SBOSS-2368_details.json
    Set Suite Variable  ${accountsGrid}     ${details["accountsGrid"]}
    Set Suite Variable  ${ordersGrid}       ${details["accountOrders"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     DominatorExamples/TurnOffAutoAdd/SBOSS-2368_values.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable  ${filters}     ${values["filters"]}


    # Build out Contract AOB
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

Finalize Environment
    Log Off
    Close The Browsers

*** Test Cases ***
Create account with JumpStart
    # Existing Keywords
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    Then I move to accounts page
    When I add contract    &{ContractAOB}
    Then I verify "company_name" contains "${ContractAOB["accountName"]}"
    And I verify grid contains "Ordered" value
    When I click on "${ContractAOB["accountType"]}" link in "contract_grid"
    ${order_number}=   I confirm the contract with instance "${bossCluster} (${platform})" and location "${ContractAOB["locationName"]}"

    # Dominator Keywords
    Set to Dictionary   ${filters}  Id  ${order_number}
    Then I move to orders page
    When I filter column headings for ${ordersGrid} with Id in ${filters}
    Then I can find ${filters["Id"]} in the ${ordersGrid}
    And I can find JumpStart in the ${ordersGrid}
    And I cannot find Fee for local number porting (LNP) in the ${ordersGrid}