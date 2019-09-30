*** Settings ***
Documentation     Basic call between USerA to UserB
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone03}    WITH NAME    Phone03

Suite Setup		Run Keywords	Test case PreCondition   Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Basic call between USerA to UserB

    [Tags]  DemoPhones

    Log          STEP - 1 : Make call Phone02 to Phone03
	Using ${Phone02} I dial the digits ${Phone03.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   10s

	Log          STEP - 2: Verify the caller name
    verify ring notifications on ${Phone03}
	BuiltIn.sleep  1s

    Log          STEP - 3 : Phone03 will answer the call
	answer the incoming call on ${Phone03}
	BuiltIn.sleep   40s

    Log          STEP - 4: Verify the caller name
    verify ${Phone03} on display of ${Phone02.phone_obj.phone.extensionNumber}
    verify ${Phone02} on display of ${Phone03.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   1s

    Log          STEP - 5 : Phone03 End the call
    disconnect the call from ${Phone02}
    BuiltIn.sleep   5s


*** Keywords ***
Test case PreCondition

    ${Phone02}=  Get library instance      Phone02
    ${Phone03}=  Get library instance      Phone03

   Set suite variable     ${Phone02}
   Set suite variable     ${Phone03}
   BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone02}
    Check Phone Sanity of ${Phone03}
    BuiltIn.sleep   2s