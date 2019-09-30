*** Settings ***

Documentation    Update Non-User Profile(BCA) with TN in D2

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
Create Non-User Profile(BCA) with TN in D2 test case
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
    #4. Create BCA user
    I switch to "Administration/Features/CallControl/BridgedCallAppearances" page on std2

    ${bca_user_name}=  generate_user_name
    ${bca_phone_number}     ${bca_std2_user_name} =    I create New STD2 BCA User     ${bca_user_name}     ${phone_number}    ${None}    ${None}
    Then I verify STD2 BCA USER  ${bca_std2_user_name}
    #5. delete non-user profile in STD2
    I delete STD2 BCA User     ${bca_user_name}

    #6.  do "SYNC NOW"
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