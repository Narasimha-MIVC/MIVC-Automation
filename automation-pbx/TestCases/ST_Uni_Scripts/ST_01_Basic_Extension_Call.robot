*** Settings ***
Documentation     Basic call between USerA to UserB
...               author - Narasimha.rao@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone08}    WITH NAME    Phone08
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone04}    WITH NAME    Phone04

Suite Setup		Run Keywords	Test case PreCondition   Phone Sanity Run
#Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

	
*** Test Cases ***
Basic call between USerA to UserB
	[Tags]  DemoPhones	
	:FOR 	${INDEX}	 IN RANGE	0	2
		
		\	Log          STEP - 1 : Make call Phone08 to Phone04
		\	Using ${Phone08} I dial the digits ${Phone04.phone_obj.phone.extensionNumber}
		\	BuiltIn.sleep   3s
		\	Log          STEP - 3 : Phone04 will answer the call
		\	answer the incoming call on ${Phone04}
		\	BuiltIn.sleep   5s
		\	Log          STEP - 5 : Phone04 End the call
		\	disconnect the call from ${Phone08}
		\	BuiltIn.sleep   3s
		\	Run Keywords 	Phone Sanity Run

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
	
