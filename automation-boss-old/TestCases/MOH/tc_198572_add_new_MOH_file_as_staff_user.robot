*** Settings ***
Documentation     Login to BOSS portal and add new MOH file as staff user
...               dev-Vasuja
...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/EnvVariables.robot
Resource           ../../Variables/MOHInfo.robot


Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Login to the boss portal as Staff user and add new MOH file
    [Tags]    Sanity_Phase2    Regression
	Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
	Then I switch to "phone_systems_on_hold_music" page
	Set to Dictionary    ${on_hold_music_staff_add}    verify    True
	and I add on hold music    &{on_hold_music_staff_add}
#	Verification
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify music on hold "${on_hold_music_staff_add['musicDescription']}" is set for ${params['partition_id']}
    Then I switch to "phone_systems_on_hold_music" page
    [Teardown]  run keywords   I delete on hold music ${on_hold_music_staff_add['musicDescription']}
    ...                        I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env

    ${uni_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}


    Set suite variable    &{on_hold_music_staff_add}

    : FOR    ${key}    IN    @{on_hold_music_staff_add.keys()}
    \    ${updated_val}=    Replace String    ${on_hold_music_staff_add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${on_hold_music_staff_add}    ${key}    ${updated_val}