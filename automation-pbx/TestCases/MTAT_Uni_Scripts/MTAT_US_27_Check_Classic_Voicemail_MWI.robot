*** Settings ***
Documentation     Callsic VoiceMail MWI
...               author - Mahabaleshwar.Hegde@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02

Test Setup		Run Keywords	Test case PreCondition         Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Callsic VoiceMail MWI

    [Tags]  MT AT Sanity

   verify led 57 state off of ${Phone02}

    Log          STEP - 1: Make call Phone01 to Phone02
	Using ${Phone01} I dial the digits ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s

	Log          STEP - 2: Click on Voice Mail Button
    press key Calltovm from ${Phone02}
	BuiltIn.sleep  20s

    Log          STEP - 3: Phone01 Send a Voice Mail
	Using ${Phone01} I dial the digits #
	BuiltIn.sleep   5s
	Using ${Phone01} I dial the digits #
	BuiltIn.sleep   5s
	press key BottomKey1 from ${Phone01}
	BuiltIn.sleep   10s

	In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    ${vm_extn}=  In D2 I get vm_login_dn extension system
    log to console   ${vm_extn}

    verify Message wait led state of ${Phone02}
    #verify led 15 state blink of ${Phone02}

    Log          STEP - 4 : Login to Voice Mail, Play and Delete
    Using ${Phone02} I dial the digits ${vm_extn}
    #Using ${Phone02} I dial the digits 8991
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits ${Phone02.phone_obj.phone.authCode}
    #Using ${Phone02} I dial the digits 123456
    BuiltIn.sleep   2s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   15s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits 1
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits 3
    BuiltIn.sleep   5s
    quit voice mail from ${Phone02}
    BuiltIn.sleep   10s

    #verify led 57 state off of ${Phone02}


*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    BuiltIn.sleep   2s
