*** Settings ***
Documentation    Enable and then disable Scribe for ST and cloud users
#...              Prasanna

Suite Setup       Set Init Env

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/std2/std2Keywords.robot

#Variable files
#Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/EnvVariables_Hybrid.robot
Variables          Variables/Hybridsite_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
Enable Hybrid Connect
    [Tags]    DEBUG

    &{login}=  copy dictionary  ${Login_Info}
    set to dictionary  ${login}  url  ${URL}
    set to dictionary  ${login}  username  ${bossUsername}
    set to dictionary  ${login}  password  ${bossPassword}

    Given I login using separate tab  ${login}
    When I switch to "accounts" page

    #1. Create an account on BOSS portal
    And I add account    &{TestAccount}
    sleep  3

    #2. Switch to the new account
    And I switch to "switch_account" page
    And I switch to account ${TestAccount["accountName"]} with ${AccWithoutLogin} option
    sleep  3

    #3. Activate "Shoretel Connect Hybrid" for the account
    And I switch to "addonfeatures" page
    sleep  3
    And I activate shoretel connect hybrid

    #4. Get the Account Id and Token from BOSS
    And I switch to "accountdetails" page
    &{params}=  create dictionary
    And I retrieve account details  ${params}
    log many  ${params}

    #5. Update the previously obtained Account Id and Token in ST D2
    set to dictionary  ${login}  url  ${STD2IP}
    set to dictionary  ${login}  username  ${STD2User}
    set to dictionary  ${login}  password  ${STD2Password}
    set to dictionary  ${login}  NewTab  ${True}
    set to dictionary  ${login}  TabName  T1

    When I login using separate tab  ${login}
    And I switch to "Administration/System/Hybrid/Synchronization" page on std2

    #6. Hybrid Synchronization in ST D2
    And I synchronize account id and account token in STD2  &{params}

    #7. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}

*** Keywords ***
Set Init Env

    &{TestAccount}=  copy dictionary  ${Hybrid_Account}

    Set suite variable    ${TestAccount}

    ${random_str}=  Generate Random String    5    [LETTERS][NUMBERS]

    ${updated_val}=    Replace String    ${TestAccount["accountName"]}    {rand_str}    ${random_str}
    Set To Dictionary    ${TestAccount}    accountName    ${updated_val}
    ${updated_val}=    Replace String    ${TestAccount["email"]}    {rand_str}    ${random_str}
    Set To Dictionary    ${TestAccount}    email    ${updated_val}
    ${updated_val}=    Replace String    ${TestAccount["location"]["locationName"]}    {rand_str}    ${random_str}
    Set To Dictionary    ${TestAccount["location"]}    locationName    ${updated_val}
