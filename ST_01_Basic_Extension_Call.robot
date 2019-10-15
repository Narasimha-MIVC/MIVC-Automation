*** Settings ***
Documentation     Basic call between USerA to UserB
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone05}    WITH NAME    Phone05
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone07}    WITH NAME    Phone07

Suite Setup		Run Keywords	Test case PreCondition   Phone Sanity Run
#Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***
Basic call between USerA to UserB

    [Tags]  DemoPhones

    Log          STEP - 1 : Make call Phone05 to Phone07
	Using ${Phone05} I dial the digits ${Phone07.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   3s

    Log          STEP - 3 : Phone07 will answer the call
	answer the incoming call on ${Phone07}
	BuiltIn.sleep   5s

    Log          STEP - 5 : Phone07 End the call
    disconnect the call from ${Phone05}
    BuiltIn.sleep   3s


*** Keywords ***
Test case PreCondition

    ${Phone05}=  Get library instance      Phone05
    ${Phone07}=  Get library instance      Phone07

   Set suite variable     ${Phone05}
   Set suite variable     ${Phone07}
   BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone05}
    Check Phone Sanity of ${Phone07}
    BuiltIn.sleep   2s