*** Settings ***
Documentation     03 Usergroup Creation
...                dev - Maha
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
#Resource          ../../../Variables/UserInfo.robot

#Component files
Library           ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}    country=${country}     WITH NAME   Boss
Library          ../../../Framework/phone_wrappers/phone_4xx/PPhoneInterface.py  WITH NAME       w2
Library          ../../lib/PBXComponent.py

*** Test Cases ***
03 Usergroup creation

    [Tags]  MT AT Sanity


    Then I switch to "usergroup" page
    and I create User Group   &{Usergroup_staff}

   In Varibale file LoginDetails.robot I update key GenUser with field userGroupName to value ${Usergroup_staff.userGroupName}
    
*** Keywords ***

Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
	${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    ${uni_num}   Set variable    ${uni_str}
    ${uni_num}   Set variable    ${uni_num}

    Set suite variable     &{Usergroup_staff}
    : FOR    ${key}    IN    @{Usergroup_staff.keys()}
    \    ${updated_val}=    Replace String    ${Usergroup_staff["${key}"]}    {rand_str}    ${uni_num}
    \    Set To Dictionary    ${Usergroup_staff}    ${key}    ${updated_val}

Test case PreCondition
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${NewAccName} with ${AccWithoutLogin} option

Test case PostCondition
    and I log off