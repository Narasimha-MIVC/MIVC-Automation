*** Settings ***
Documentation     Phone Automation : Verify VoiceMail
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone08}    WITH NAME    Phone08
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone04}    WITH NAME    Phone04

Test Setup		Run Keywords	Test case PreCondition         Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Verify VoiceMail

    [Tags]  ST Sanity

    Log          STEP - 1: Verify the Voice Mail Count
    ${before_vm_send} =  Get Unread Voice Mail Count from ${Phone04}
    log to console  ${before_vm_send}

    Log          STEP - 2: Make call Phone08 to Phone04
	Using ${Phone08} I dial the digits ${Phone04.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s

	Log          STEP - 3: Click on Voice Mail Button
    press key Calltovm from ${Phone04}
	BuiltIn.sleep  20s

    Log          STEP - 4: Phone08 Send a Voice Mail
	Using ${Phone08} I dial the digits #
	BuiltIn.sleep   5s
	Using ${Phone08} I dial the digits #
	BuiltIn.sleep   5s
	press key BottomKey1 from ${Phone08}
	BuiltIn.sleep   10s

	Log          STEP - 5 : Verify the Voice Main Count
    ${after_vm_send} =  Get Unread Voice Mail Count from ${Phone04}
    log to console  ${after_vm_send}

    ${count}     set variable  1
    verify count ${Phone08} ${before_vm_send} ${after_vm_send} ${count}
    BuiltIn.sleep   5s

    Log          STEP - 6 : Login to Voice Mail, Play and Delete
    press key VoiceMail from ${Phone04}
    BuiltIn.sleep   5s
    Using ${Phone04} I dial the digits ${Phone04.phone_obj.phone.authCode}
    BuiltIn.sleep   2s
    press key vmlogin from ${Phone04}
    BuiltIn.sleep   10s
    press key BottomKey1 from ${Phone04}
    BuiltIn.sleep   15s
    press key vmdelete from ${Phone04}
    BuiltIn.sleep   2s
    press key Quit from ${Phone04}
    BuiltIn.sleep   20s

    Log          STEP - 7 : Verify the Voice Main Count
    ${after_vm_delete} =  Get Unread Voice Mail Count from ${Phone04}
    log to console  ${after_vm_delete}

    verify count ${Phone08} ${after_vm_delete} ${after_vm_send} ${count}

*** Keywords ***
Test case PreCondition

    ${Phone08}=  Get library instance      Phone08
    ${Phone04}=  Get library instance      Phone04

    Set suite variable     ${Phone08}
    Set suite variable     ${Phone04}
    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone08}
    Check Phone Sanity of ${Phone04}
    BuiltIn.sleep   2s