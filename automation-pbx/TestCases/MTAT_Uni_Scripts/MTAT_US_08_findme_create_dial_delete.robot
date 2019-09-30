*** Settings ***
Documentation     6xxx Phone Automation : Find me Creation ,dial and unassign
...               author - Mahabaleshwar.Hegde@mitel.com

#Test and Suite Setup and Teardown
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keywords    Test case PostCondition
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
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone03}    WITH NAME    Phone03
*** Test Cases ***
Find me Creation ,dial and unassign

    When I select call routing page using extension ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   2s
    and I configure phone number "CallRoutingTab_ConfigureMainSettings_AddLabel1" and "CallRoutingTab_ConfigureMainSettings_AddPhone1" with number "${Phone03.phone_obj.phone.extensionNumber}" in call rerouting main settings

    and I configure find me "CallRoutingTab_ConfigureMainSettings_FindMe1" for number "Arun Arun4466 - ${Phone03.phone_obj.phone.extensionNumber} - Connect by answering - Try for 3 rings"

    and I click the "CallRoutingTab_ChangeFindme" button

    Then I verify option "If the caller presses 1 during the greeting then sequentially ring my Find Me numbers" in Find Me settings
    and I click the "CallRoutingTab_Finish" button

    #Call to find me number
    Log to console  STEP:1 Phone1 make call to Phone2
	Using ${Phone01} I dial the digits ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   4s
	
	Log to console	STEP:2 Phone2 press softkey2 for going in voicemail
    press key Calltovm from ${Phone02}
	BuiltIn.sleep  5s
    
    Log to console  STEP-3: Phone1 Press button 1 to call find me number
    Using ${Phone01} I dial the digits 1
    BuiltIn.sleep   8s
    
    Log to console  STEP-4: Phone3 answer the call
	answer the incoming call on ${Phone03}
	BuiltIn.sleep   2s
    
    Log to console  STEP-5: Phone3 Press button 1 to coneect the call
    Using ${Phone03} I dial the digits 1
    BuiltIn.sleep   4s
    
    Log to console  STEP-6: Verifying caller name
    verify ${Phone03} on display of ${Phone01.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s
    
    Log to console  STEP-6: Phone1 ends the call by pressing softkey5
    disconnect the call from ${Phone01}
    BuiltIn.sleep   2s
    
*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02
    ${Phone03}=  Get library instance      Phone03

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    Set suite variable     ${Phone03}

    BuiltIn.sleep   2s

	When I check for alert
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${AccName} with ${AccWithoutLogin} option

Test case PostCondition
    and I configure find me "CallRoutingTab_ConfigureMainSettings_FindMe1" for number "Select Number"
    and I click the "CallRoutingTab_ConfigureMainSettings" button
    and I click the "CallRoutingTab_ConfigureMainSettings_Remove1" button
    and I click the "CallRoutingTab_ConfigureMainSettings_AddFinish" button
    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    Check Phone Sanity of ${Phone03}
    BuiltIn.sleep   2s

