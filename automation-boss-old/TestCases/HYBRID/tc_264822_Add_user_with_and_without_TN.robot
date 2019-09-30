*** Settings ***
Documentation    Create Non-User Profile(BCA) with TN in D2

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/std2/std2Keywords.robot
Resource           ../../RobotKeywords/std2/administration/users/users_users_Keywords.robot
Resource           ../../RobotKeywords/std2/administration/features/CallControl/CallcontrolKeywords.robot
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

1. Create STD2 user without TN
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

    # 3. Add user without TN

    ${user_first_name}=    generate_user_name

    #4. Switch to Admin->user
	And I switch to "Administration/Users/Users" page on std2

    #5. Create User in STD2 without  TN and verify that
    ${phone_number}  ${first_name}  ${last_name}=  I create New STD2User  ${user_first_name}    ${None}
    Then I verify STD2 USER    ${first_name}
    ${user_name} =    Set Variable  ${first_name}${SPACE}${last_name}
   # 6.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2

    I sync now data between STD2 and Boss
    #7. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}
    #8. Check the user on BOSS
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s
    #9. move to phone system -> on site partition -> Add-on feature
    ${Partition}=  set variable  (BOSS_AUTO_HYB_PREM) BOSS_AUTO_HYB_PREM
    And I switch to "Users" in partition ${Partition}
    sleep  5s
    #10 check for the user in Boss after sync

    I check user info in Boss after sync with STD2    ${user_name}   ${phone_number}   ${None}    add_user

    #11.. Navigate back to D2 and delete the created user
    set to dictionary  ${login}  TabName  T1
    I switch tab on browser  ${login}
    I switch to "Administration/Users/Users" page on std2
    I delete STD2 User     ${first_name}

    [Teardown]

    Run Keywords  I log off
    ...           I check for alert
    ...           Close The Browsers

2. Create STD2 User with TN
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

    #3. Create STD2 user with TN
    ${user_first_name}=    generate_user_name

    #4. Switch to Admin->user
	And I switch to "Administration/Users/Users" page on std2

    #5. Create User in STD2 with TN and verify that
    ${phone_number}  ${first_name}  ${last_name}=  I create New STD2User  ${user_first_name}    True
    Then I verify STD2 USER    ${first_name}
    ${user_name} =    Set Variable  ${first_name}${SPACE}${last_name}
   # 6.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2

    I sync now data between STD2 and Boss
    #7. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}

    #8. Check the user on BOSS
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s
    #9. move to phone system -> on site partition -> Add-on feature
    ${Partition}=  set variable  (BOSS_AUTO_HYB_PREM) BOSS_AUTO_HYB_PREM
    And I switch to "Users" in partition ${Partition}
    sleep  5s
    #10.check for the user in Boss after sync

    I check user info in Boss after sync with STD2    ${user_name}   ${phone_number}   ${None}    add_user

    #11. Navigate back to D2 and delete the created user
    set to dictionary  ${login}  TabName  T1
    I switch tab on browser  ${login}
    I switch to "Administration/Users/Users" page on std2
    I delete STD2 User     ${first_name}
    # 12.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2

    I sync now data between STD2 and Boss
    [Teardown]

    Run Keywords  I log off
    ...           I check for alert
    ...           Close The Browsers


*** Keywords ***
generate_user_name
    [Documentation]  The keyword generates random user name
    ${name}=  Generate Random String  4  [LOWER]
    [Return]  ${name}