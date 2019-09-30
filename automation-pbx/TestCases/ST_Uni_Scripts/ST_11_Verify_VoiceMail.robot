*** Settings ***
Documentation     Phone Automation : Verify VoiceMail
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone03}    WITH NAME    Phone03

Test Setup		Run Keywords	Test case PreCondition         Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Verify VoiceMail

    [Tags]  ST Sanity

    Log          STEP - 1: Verify the Voice Mail Count
    ${before_vm_send} =  Get Unread Voice Mail Count from ${Phone03}
    log to console  ${before_vm_send}

    Log          STEP - 2: Make call Phone01 to Phone03
	Using ${Phone01} I dial the digits ${Phone03.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s

	Log          STEP - 3: Click on Voice Mail Button
    press key Calltovm from ${Phone03}
	BuiltIn.sleep  20s

    Log          STEP - 4: Phone01 Send a Voice Mail
	Using ${Phone01} I dial the digits #
	BuiltIn.sleep   5s
	Using ${Phone01} I dial the digits #
	BuiltIn.sleep   5s
	press key BottomKey1 from ${Phone01}
	BuiltIn.sleep   10s

	Log          STEP - 5 : Verify the Voice Main Count
    ${after_vm_send} =  Get Unread Voice Mail Count from ${Phone03}
    log to console  ${after_vm_send}

    ${count}     set variable  1
    verify count ${Phone01} ${before_vm_send} ${after_vm_send} ${count}
    BuiltIn.sleep   5s

    Log          STEP - 6 : Login to Voice Mail, Play and Delete
    press key VoiceMail from ${Phone03}
    BuiltIn.sleep   5s
    Using ${Phone03} I dial the digits ${Phone03.phone_obj.phone.authCode}
    BuiltIn.sleep   2s
    press key vmlogin from ${Phone03}
    BuiltIn.sleep   10s
    press key BottomKey1 from ${Phone03}
    BuiltIn.sleep   15s
    press key vmdelete from ${Phone03}
    BuiltIn.sleep   2s
    press key Quit from ${Phone03}
    BuiltIn.sleep   20s

    Log          STEP - 7 : Verify the Voice Main Count
    ${after_vm_delete} =  Get Unread Voice Mail Count from ${Phone03}
    log to console  ${after_vm_delete}

    verify count ${Phone01} ${after_vm_delete} ${after_vm_send} ${count}

*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone03}=  Get library instance      Phone03

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone03}
    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone03}
    BuiltIn.sleep   2s