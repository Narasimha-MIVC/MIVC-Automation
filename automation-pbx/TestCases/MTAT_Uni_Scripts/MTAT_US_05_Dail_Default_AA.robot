*** Settings ***
Documentation     Default Auto Attendant
...               author - Mahabaleshwar.Hegde@mitel.com

#Test and Suite Setup and Teardown
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource        ../../../automation-boss/RobotKeywords/BOSSKeywords.robot
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource         ../../Variables/LoginDetails.robot

#Component files
Library           ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}    country=${country}     WITH NAME   Boss
Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01


*** Test Cases ***
Default Auto Attendant

    [Tags]  Mitel_6940_Phone

###################################Default  AA ##############################################

    ${AA}=    Set Variable    Tenant Auto-Attendant
    When I switch to "Visual_Call_Flow_Editor" page
    ${text}=    Extension vcfe default AA   ${AA}
    Log To Console   ${text}

###################################Phone Verification##############################################

	Using ${Phone01} I dial the digits ${text}
    BuiltIn.sleep   4s
	#press key BottomKey1 from ${Phone01}
	#BuiltIn.sleep   2s
	verify ${Phone01} on display of Auto-Attendant
    BuiltIn.sleep   1s
    disconnect the call from ${Phone01}
    BuiltIn.sleep   2s

*** Keywords ***
Test case PreCondition
    ${Phone01}=  Get library instance      Phone01
    Set suite variable     ${Phone01}
    BuiltIn.sleep   2s

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${AccName} with ${AccWithoutLogin} option

Phone Sanity Run
    Check Phone Sanity of ${Phone01}
    BuiltIn.sleep   2s


