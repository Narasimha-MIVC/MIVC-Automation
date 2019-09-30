*** Settings ***
Documentation     Login to BOSS portal and add new MOH file as staff user
...               dev-Mayura
...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keywords    Test case PostCondition
Suite Teardown    Close The Browsers

Resource          ../../../automation-boss/RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot


Library			  ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}
Library           ../../../automation-boss/lib/DirectorComponent.py
Library          ../../../Framework/phone_wrappers/phone_4xx/PPhoneInterface.py  WITH NAME       w2
Library  String

*** Test Cases ***
Login to the boss portal as Staff user and add new MOH file

    [Tags]  MT AT Sanity

	&{params1}=  create dictionary
#	set to dictionary  ${params1}  get_account_id  ${True}
#	And I retrieve account details  ${params1}
#	log to console    ${params1}
	Then I switch to "phone_systems_on_hold_music" page
	Set to Dictionary    ${on_hold_music_staff_add}    verify    True
	and I add on hold music    &{on_hold_music_staff_add}
#	Verification
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify music on hold "${on_hold_music_staff_add['musicDescription']}" is set for ${AccName}
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



Test case PreCondition

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${AccName} with ${AccWithoutLogin} option

Test case PostCondition
    and I log off
