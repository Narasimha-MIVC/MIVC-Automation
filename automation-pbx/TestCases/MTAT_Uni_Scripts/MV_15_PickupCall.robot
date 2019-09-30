*** Settings ***
Documentation     PickUP Call
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone04}    WITH NAME    Phone04

Suite Setup		Run Keywords	Test case PreCondition    Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
PickUP Call

    [Tags]  MT AT Sanity

    Log          STEP - 1 : Make call Phone01 to Phone02
	Using ${Phone01} I dial the digits ${Phone04.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   4s

    Log          STEP - 2: Park the call to Phone04
    press key BottomKey1 from ${Phone02}
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits ${Phone04.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   2s
    press key BottomKey1 from ${Phone02}
    BuiltIn.sleep   10s

    Log          STEP - 3: Verify the caller name
    verify ${Phone01} on display of ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   1s

    Log          STEP - 4 : Phone04 End the call
    disconnect the call from ${Phone01}
    BuiltIn.sleep   5s


*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02
    ${Phone04}=  Get library instance      Phone04

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    Set suite variable     ${Phone04}

    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    Check Phone Sanity of ${Phone04}
    BuiltIn.sleep   2s