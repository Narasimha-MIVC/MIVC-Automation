*** Settings ***
Documentation     Four way Conference with external Party
...               author - Mahabaleshwar.Hegde@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone_did_01}    WITH NAME    Phone_did_01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone03}    WITH NAME    Phone03
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone04}    WITH NAME    Phone04
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone_did_02}    WITH NAME    Phone_did_02

Suite Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Four way Conference with external Party

    [Tags]  MT AT Sanity

    Log          STEP - 1 : Make call Phone_did_01 to Phone02
    Using ${Phone_did_02} I dial the digits 9
	Using ${Phone_did_02} I dial the digits ${Phone_did_01.phone_obj.phone.trunkISDN}
    BuiltIn.sleep   4s

    Log          STEP - 2 : Phone02 will answer the call
	answer the incoming call on ${Phone_did_01}
	BuiltIn.sleep   2s

    Log          STEP - 3: Verify the caller name
    verify ${Phone_did_01} on display of ${Phone_did_02.phone_obj.phone.trunkISDN}
    BuiltIn.sleep   1s

    Log          STEP - 4: Click on Blind Conference and Add Phone03
    make conference from ${Phone_did_01}
    BuiltIn.sleep   1s
    Using ${Phone_did_01} I dial the digits ${Phone03.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s
    make conference from ${Phone_did_01}
    BuiltIn.sleep   5s

    Log          STEP - 5: Phone03 Answer the call
    answer the incoming call on ${Phone03}
    BuiltIn.sleep   5s

    accept blind conference from ${Phone_did_01}
    BuiltIn.sleep   10s

    Log          STEP - 6: Verify the 2 way consult conference
    verify ${Phone_did_01} on display of Conferenced 2 calls
    verify ${Phone02} on display of Conferenced 2 calls
    verify ${Phone03} on display of Conferenced 2 calls
    BuiltIn.sleep   1s

     Log          STEP - 7: Click on Blind Conference and Add Phone04
    make conference from ${Phone_did_01}
    BuiltIn.sleep   1s
    Using ${Phone_did_01} I dial the digits ${Phone04.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s
    make conference from ${Phone_did_01}
    BuiltIn.sleep   5s

    Log          STEP - 8: Phone04 Answer the call
    answer the incoming call on ${Phone04}
    BuiltIn.sleep   5s

    accept blind conference from ${Phone_did_01}
    BuiltIn.sleep   10s

    Log          STEP - 9: Verify the 2 way consult conference
    verify ${Phone_did_01} on display of Conferenced 3 calls
    verify ${Phone02} on display of Conferenced 3 calls
    verify ${Phone03} on display of Conferenced 3 calls
    verify ${Phone04} on display of Conferenced 3 calls
    BuiltIn.sleep   1s

         Log          STEP - 10: Click on Blind Conference and Add Phone02
    make conference from ${Phone_did_01}
    BuiltIn.sleep   1s
    Using ${Phone_did_01} I dial the digits ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s
    make conference from ${Phone_did_01}
    BuiltIn.sleep   5s

    Log          STEP - 11: Phone_did_02 Answer the call
    answer the incoming call on ${Phone02}
    BuiltIn.sleep   5s

    accept blind conference from ${Phone_did_01}
    BuiltIn.sleep   10s

    Log          STEP - 12: Verify the 2 way consult conference
    verify ${Phone_did_01} on display of Conferenced 4 calls
    verify ${Phone02} on display of Conferenced 4 calls
    verify ${Phone03} on display of Conferenced 4 calls
    verify ${Phone04} on display of Conferenced 4 calls
    verify ${Phone_did_02} on display of Conferenced 4 calls
    BuiltIn.sleep   1s

    Log          STEP - 13: Phone_did_01 End the call
    disconnect the call from ${Phone_did_01}
    BuiltIn.sleep   2s

    Log          STEP - 14: Phone02 End the call
    disconnect the call from ${Phone02}
    BuiltIn.sleep   2s

    Log          STEP - 15: Phone_did_01 End the call
    disconnect the call from ${Phone03}
    BuiltIn.sleep   2s

    Log          STEP - 16: Phone02 End the call
    disconnect the call from ${Phone04}
    BuiltIn.sleep   2s

*** Keywords ***
Test case PreCondition

    ${Phone_did_01}=  Get library instance      Phone_did_01
    ${Phone02}=  Get library instance      Phone02
    ${Phone03}=  Get library instance      Phone03
    ${Phone04}=  Get library instance      Phone04
    ${Phone_did_02}=  Get library instance      Phone_did_02

    Set suite variable     ${Phone_did_01}
    Set suite variable     ${Phone02}
    Set suite variable     ${Phone03}
    Set suite variable     ${Phone04}
    Set suite variable     ${Phone_did_02}

    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone_did_01}
    Check Phone Sanity of ${Phone02}
    Check Phone Sanity of ${Phone03}
    Check Phone Sanity of ${Phone04}
    Check Phone Sanity of ${Phone_did_02}
    BuiltIn.sleep   2s