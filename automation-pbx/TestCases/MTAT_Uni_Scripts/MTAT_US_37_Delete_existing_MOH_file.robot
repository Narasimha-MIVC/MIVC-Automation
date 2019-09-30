*** Settings ***
Documentation     Login to BOSS portal and delete existing MOH file as staff user
...               dev-Mayura
...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keywords    Test case PostCondition
Suite Teardown    Close The Browsers

Resource          ../../../automation-boss/RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/LoginDetails.robot
Resource           ../../Variables/MOHInfo.robot


Library			  ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}
Library           ../../../automation-boss/lib/DirectorComponent.py
Library          ../../../Framework/phone_wrappers/phone_4xx/PPhoneInterface.py  WITH NAME       w2
Library  String

*** Test Cases ***
Login to the boss portal as Staff user and delete existing MOH file

    [Tags]  MT AT Sanity


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




Test case PreCondition

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${AccName} with ${AccWithoutLogin} option

Test case PostCondition
    and I log off
