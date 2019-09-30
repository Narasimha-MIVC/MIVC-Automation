*** Settings ***
Documentation     Login to BOSS portal as staff user and verify User group creation
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
Login to the boss portal as staff user and create User Group
    [Tags]    Sanity_Phase2    Regression
	Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
	Then I switch to "usergroup" page
	and I create User Group   &{Usergroup_staff}
	Then I switch to "users" page
	And I assign User "${DMemail}" in user group "${Usergroup_staff['userGroupName']}"
#	Verification
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
#    And In D2 I verify user group ${Usergroup_staff['userGroupName']} is set for ${accountName1}
    And In D2 I verify user group ${Usergroup_staff['userGroupName']} is set for ${params['partition_id']}
    Then I switch to "users" page
    And I assign User "${DMemail}" in user group "${Usergroup_edit['userGroupName']}"
    Then I switch to "usergroup" page
    [Teardown]  run keywords   I delete user group ${Usergroup_staff['userGroupName']}
    ...                        I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Usergroup_staff}

    : FOR    ${key}    IN    @{Usergroup_staff.keys()}
    \    ${updated_val}=    Replace String    ${Usergroup_staff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Usergroup_staff}    ${key}    ${updated_val}
