*** Settings ***
Documentation    Remove STD2 BCA  user DID and sync the data with Boss portal

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
Remove BCA User DID
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
    #6. I Retrieve STD2 user DID
     ${DID_number} =  I Retrieve STD2 user DID    ${first_name}

    #7. Create non-profile(BCA)user and verify under Admin->Feature->Callcontrol->BCA page
    Then I switch to "Administration/Features/CallControl/BridgedCallAppearances" page on std2
    ${bca_user_name}=  generate_user_name
    ${bca_phone_number}     ${bca_std2_user_name} =    I create New STD2 BCA User    ${bca_user_name}    ${phone_number}    True    ${DID_number}
    Then I verify STD2 BCA USER  ${bca_std2_user_name}

    # 8.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2
    I sync now data between STD2 and Boss
    # Remove BCA DID
    I switch to "Administration/Features/CallControl/BridgedCallAppearances" page on std2
    ${updated_bca_user_name}=  I update STD2 BCA User    ${bca_user_name}    ${None}    ${None}    Remove    ${None}

    #9.  do "SYNC NOW"
    Then I switch to "Administration/System/Hybrid/Synchronization" page on std2
    I sync now data between STD2 and Boss

    #10. Delete Non-profile user and STD2 user(STD2 user should be delete after BCA user deletion)
    I switch to "Administration/Features/CallControl/BridgedCallAppearances" page on std2
    I delete STD2 BCA User    ${updated_bca_user_name}
    And I switch to "Administration/Users/Users" page on std2
    I delete STD2 User    ${first_name}

    [Teardown]

    Run Keywords  I log off
    ...           I check for alert
    ...           Close The Browsers

*** Keywords ***
generate_user_name
    [Documentation]  The keyword generates random user name
    ${name}=  Generate Random String  4  [LOWER]
    [Return]  ${name}