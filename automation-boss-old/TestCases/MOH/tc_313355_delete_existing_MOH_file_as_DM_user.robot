*** Settings ***
Documentation     Login to BOSS portal and delete existing MOH file as DM user
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
Login to the boss portal as DM user and add new MOH file
    [Tags]    Sanity_Phase2    Regression
	Given I login to ${URL} with ${DMemail} and ${DMpassword}
	Then I switch to "phone_systems_on_hold_music" page
	Set to Dictionary    ${on_hold_music_DM_delete}    verify    True
	and I add on hold music    &{on_hold_music_DM_delete}
    Then I switch to "phone_systems_on_hold_music" page
    And I delete on hold music ${on_hold_music_DM_delete['musicDescription']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env

    ${uni_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{on_hold_music_DM_delete}

    : FOR    ${key}    IN    @{on_hold_music_DM_delete.keys()}
    \    ${updated_val}=    Replace String    ${on_hold_music_DM_delete["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${on_hold_music_DM_delete}    ${key}    ${updated_val}
