*** Settings ***
Documentation     Login to BOSS portal and delete existing MOH file as staff user
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
Login to the boss portal as Staff user and delete existing MOH file
    [Tags]    Sanity_Phase2    Regression
	Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
	Then I switch to "phone_systems_on_hold_music" page
	and I add on hold music    &{on_hold_music_staff_delete}
    Then I switch to "phone_systems_on_hold_music" page
    And I delete on hold music ${on_hold_music_staff_delete['musicDescription']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env

    ${uni_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}


    Set suite variable    &{on_hold_music_staff_delete}

    : FOR    ${key}    IN    @{on_hold_music_staff_delete.keys()}
    \    ${updated_val}=    Replace String    ${on_hold_music_staff_delete["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${on_hold_music_staff_delete}    ${key}    ${updated_val}