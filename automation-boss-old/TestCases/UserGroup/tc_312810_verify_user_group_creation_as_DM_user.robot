*** Settings ***
Documentation     Login to BOSS portal and Verify User group creation as DM user
...               dev-Vasuja
...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/EnvVariables.robot
Resource           ../../Variables/UserGroupInfo.robot


Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Login to the boss portal as DM user and create User Group
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
	Given I login to ${URL} with ${DMemail} and ${DMpassword}
	Then I switch to "usergroup" page
	and I create User Group   &{UsergroupDM}
	Then I switch to "users" page
	And I assign User "${DMemail}" in user group "${UsergroupDM['userGroupName']}"
#	Verification
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
#    And In D2 I verify user group ${UsergroupDM['userGroupName']} is set for ${accountName1}
    And In D2 I verify user group ${UsergroupDM['userGroupName']} is set for ${params['partition_id']}
    Then I switch to "users" page
    And I assign User "${DMemail}" in user group "${Usergroup_edit['userGroupName']}"
    Then I switch to "usergroup" page
    [Teardown]  run keywords   I delete user group ${UsergroupDM['userGroupName']}
    ...                        I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{UsergroupDM}

    : FOR    ${key}    IN    @{UsergroupDM.keys()}
    \    ${updated_val}=    Replace String    ${UsergroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${UsergroupDM}    ${key}    ${updated_val}

