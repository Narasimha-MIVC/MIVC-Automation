*** Settings ***
Documentation     Mute and Hold
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02

Suite Setup		Run Keywords	Test case PreCondition    Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Mute and Hold

    [Tags]  DemoPhones

    Log          STEP - 1 : Make call Phone01 to Phone02
	Using ${Phone01} I dial the digits ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   4s

    Log          STEP - 2 : Phone02 will answer the call
	answer the incoming call on ${Phone02}
	BuiltIn.sleep   2s

    Log          STEP - 3: Verify the caller name
    verify ${Phone01} on display of ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s

    Log          STEP - 4: Mute the call
    press key Mute from ${Phone01}
    BuiltIn.sleep   5s

    Log          STEP - 5: Verify Mute
    verify Mute state of ${Phone01}
    BuiltIn.sleep   2s

    Log          STEP - 6: un-Mute the call
    press key Mute from ${Phone01}
    BuiltIn.sleep   2s

    Log          STEP - 7: Verify the caller name
    verify ${Phone01} on display of ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   1s

    Log          STEP - 8: Hold the call
    press key Hold from ${Phone01}
    BuiltIn.sleep   2s

    Log          STEP - 9: Verify Hold
    verify Hold state of ${Phone01}
    BuiltIn.sleep   2s

    Log          STEP - 10: un-Mute the call
     press key Hold from ${Phone01}
    BuiltIn.sleep   2s

    Log          STEP - 11 : Phone02 End the call
    disconnect the call from ${Phone02}
    BuiltIn.sleep   2s

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
    BuiltIn.sleep   5s