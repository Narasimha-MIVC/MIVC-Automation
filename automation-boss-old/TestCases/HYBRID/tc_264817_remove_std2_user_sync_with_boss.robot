*** Settings ***

Documentation    Remove user from D2 and sync with Boss

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/std2/std2Keywords.robot
Resource           ../../RobotKeywords/std2/administration/users/users_users_Keywords.robot
Resource           ../../RobotKeywords/std2/administration/system/hybrid/synchronization.robot


#Variable files
# Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/EnvVariables_Hybrid.robot
Variables          Variables/Hybridsite_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
Remove user from D2 and sync with Boss
    [Tags]    DEBUG

    #1. log into BOSS portal
    &{login}=  copy dictionary  ${Login_Info}
    set to dictionary  ${login}  url  ${URL}
    set to dictionary  ${login}  username  ${bossUsername}
    set to dictionary  ${login}  password  ${bossPassword}

    Given I login using separate tab  ${login}
    log many  &{login}

    sleep  5s

    #2. log into ST D2 (in a different TAB on the browser)
    set to dictionary  ${login}  url  ${STD2IP}
    set to dictionary  ${login}  username  ${STD2User}
    set to dictionary  ${login}  password  ${STD2Password}
    set to dictionary  ${login}  NewTab  ${True}
    set to dictionary  ${login}  TabName  T1

    When I login using separate tab  ${login}



    ${user_first_name}=  generate_user_name

    And I switch to "Administration/Users/Users" page on std2
  #3. Create STD2 user
    ${phone_number}  ${first_name}  ${last_name}=  I create New STD2User  ${user_first_name}    ${None}
    Then I verify STD2 USER    ${first_name}
    Then I switch to "Administration/Features/CallControl/BridgedCallAppearances" page on std2
     ${user_name} =    Set Variable  ${first_name}${SPACE}${last_name}

    #6.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2

    I sync now data between STD2 and Boss
    #6. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}
    #4. Check the user on BOSS
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s
    #5. move to phone system -> on site partition -> Add-on feature
    ${Partition}=  set variable  (BOSS_AUTO_HYB_PREM) BOSS_AUTO_HYB_PREM
    And I switch to "Users" in partition ${Partition}

    #7. Verify user info on boss page
    I check user info in Boss after sync with STD2    ${user_name}   ${phone_number}   ${NONE}    add_user

    #8. Navigate back to D2 and delete the created user
    set to dictionary  ${login}  TabName  T1
    I switch tab on browser  ${login}
    I switch to "Administration/Users/Users" page on std2
    I delete STD2 User     ${first_name}

    #6.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2

    I sync now data between STD2 and Boss
    #6. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}
    #4. Check the user on BOSS
    #5. move to phone system -> on site partition -> Add-on feature
    ${Partition}=  set variable  (BOSS_AUTO_HYB_PREM) BOSS_AUTO_HYB_PREM
    And I switch to "Users" in partition ${Partition}
    I check user info in Boss after sync with STD2    ${user_name}   ${NONE}   ${NONE}   delete_user

  [Teardown]

    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***
generate_user_name
    [Documentation]  The keyword generates random user name
    ${name}=  Generate Random String  4  [LOWER]
    [Return]  ${name}