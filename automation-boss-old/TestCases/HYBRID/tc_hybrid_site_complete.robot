*** Settings ***
Documentation    Hybrid site complete E2E scenario

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/std2/std2Keywords.robot

#Variable files
# Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/EnvVariables_Hybrid.robot
Variables          Variables/Hybridsite_Variables.py  country=AUS

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
Hybrid site E2E test case
    [Tags]    DEBUG

    #1. log into BOSS portal
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    And I switch to "switch_account" page
#    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    &{login}=  copy dictionary  ${Login_Info}
    set to dictionary  ${login}  url  ${URL}
    set to dictionary  ${login}  username  ${bossUsername}
    set to dictionary  ${login}  password  ${bossPassword}

    I login using separate tab  ${login}

    log many  &{login_info}

    sleep  5s

   #2. log into ST D2 (in a different TAB on the browser)
    set to dictionary  ${login}  url  ${STD2IP}
    set to dictionary  ${login}  username  ${STD2User}
    set to dictionary  ${login}  password  ${STD2Password}
    set to dictionary  ${login}  NewTab  ${True}
    set to dictionary  ${login}  TabName  T1

    I login using separate tab  ${login}

    #3. Switch to "Administration/Users/Users" page on STD2 and do operations
    I switch to std2 page  Administration/Users/Users

    #4. Get a user info
    &{user_info}=  evaluate  {}
    I find single user info  ${user_info}

    #5. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}

    sleep  5s
    #4. Check the user on BOSS
    #5. Navigate back to D2
    #6. Update the user parameters and do "SYNC NOW"
    #7. Navigate back to BOSS portal and check that the update has been synched up

*** Keywords ***
Provided precondition
#    Setup system under test