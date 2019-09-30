*** Settings ***
Documentation     Login to BOSS portal and rename new MOH file as DM user
...               dev-Vasuja
...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/EnvVariables.robot
Resource          ../../Variables/MOHInfo.robot


Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Login to the boss portal as DM user and rename new MOH file
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
	Then I switch to "phone_systems_on_hold_music" page
	Set to Dictionary    ${on_hold_music_DM_rename}    verify    True
	and I add on hold music    &{on_hold_music_DM_rename}
	Then I switch to "phone_systems_on_hold_music" page
	Then I rename on hold music    &{on_hold_music_DM_rename}
#	Verification
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify music on hold "${on_hold_music_DM_rename['rename_musicDescription']}" is set for ${params['partition_id']}
    Then I switch to "phone_systems_on_hold_music" page
    [Teardown]  run keywords   I delete on hold music ${on_hold_music_DM_rename['rename_musicDescription']}
    ...                        I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env

    ${uni_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{on_hold_music_DM_rename}

    : FOR    ${key}    IN    @{on_hold_music_DM_rename.keys()}
    \    ${updated_val}=    Replace String    ${on_hold_music_DM_rename["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${on_hold_music_DM_rename}    ${key}    ${updated_val}
