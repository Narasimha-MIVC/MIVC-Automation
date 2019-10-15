*** Settings ***
Documentation     Trunk call between USerA to UserB
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone_did_01}    WITH NAME    Phone_did_01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone_did_02}    WITH NAME    Phone_did_02

Suite Setup		Run Keywords	Test case PreCondition   Phone Sanity Run
#Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Trunk call between USerA to UserB

    [Tags]  ST AT Sanity

    Log          STEP - 1 : Make call Phone_did_01 to Phone_did_02
    Using ${Phone_did_01} I dial the digits 9
	Using ${Phone_did_01} I dial the digits ${Phone_did_02.phone_obj.phone.trunkISDN}
    BuiltIn.sleep   5s

    Log          STEP - 3 : Phone_did_02 will answer the call
	answer the incoming call on ${Phone_did_02}
	BuiltIn.sleep   5s

    Log          STEP - 4 : Phone_did_02 End the call
    disconnect the call from ${Phone_did_01}
    BuiltIn.sleep   3s


*** Keywords ***
Test case PreCondition

    ${Phone_did_01}=  Get library instance      Phone_did_01
    ${Phone_did_02}=  Get library instance      Phone_did_02

    Set suite variable     ${Phone_did_01}
    Set suite variable     ${Phone_did_02}
    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone_did_01}
    Check Phone Sanity of ${Phone_did_02}
    BuiltIn.sleep   2s