*** Settings ***
Documentation     Dial VoiceMail Extn
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone04}    WITH NAME    Phone04

Test Setup		Run Keywords	Test case PreCondition
#Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Dial VoiceMail Extn

    [Tags]  DemoPhones

    Log          STEP - 1: Verify the Voice Mail Count
    ${before_vm_send} =  Get Unread Voice Mail Count from ${Phone04}
    log to console  ${before_vm_send}


    Log          STEP - 2: Make call Phone01 to Phone04
	Using ${Phone01} I dial the digits ${Phone04.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s

	Log          STEP - 3: Click on Voice Mail Button
    press key Calltovm from ${Phone04}
	BuiltIn.sleep  2s

    Log          STEP - 4: Phone01 Send a Voice Mail
	Using ${Phone01} I dial the digits #
	BuiltIn.sleep   5s
	Using ${Phone01} I dial the digits #
	BuiltIn.sleep   5s
	press key BottomKey1 from ${Phone01}
	BuiltIn.sleep   20s

	In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    ${vm_extn}=  In D2 I get vm_login_dn extension system
    log to console   ${vm_extn}

    Log          STEP - 5: Verify the Voice Mail Count
    ${before_vm_delete} =  Get Unread Voice Mail Count from ${Phone04}
    log to console  ${before_vm_delete}

    ${count}     set variable  1
    verify count ${Phone01} ${before_vm_send} ${before_vm_delete} ${count}

    Log          STEP - 6 : Login to Voice Mail, Play and Delete
    Using ${Phone04} I dial the digits ${vm_extn}
    BuiltIn.sleep   10s
    Using ${Phone04} I dial the digits ${Phone04.phone_obj.phone.authCode}
    #Using ${Phone04} I dial the digits 123456
    BuiltIn.sleep   2s
    Using ${Phone04} I dial the digits #
    BuiltIn.sleep   15s
    Using ${Phone04} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone04} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone04} I dial the digits 1
    BuiltIn.sleep   10s
    Using ${Phone04} I dial the digits 3
    BuiltIn.sleep   5s
    quit voice mail from ${Phone04}
    BuiltIn.sleep   2s

    Log          STEP - 7 : Verify the Voice Main Count
    ${after_vm_delete} =  Get Unread Voice Mail Count from ${Phone04}
    log to console  ${after_vm_delete}

    verify count ${Phone01} ${after_vm_delete} ${before_vm_delete} ${count}

*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone04}=  Get library instance      Phone04

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone04}
    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone04}
    BuiltIn.sleep   2s
