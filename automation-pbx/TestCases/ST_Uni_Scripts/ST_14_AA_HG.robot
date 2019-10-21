*** Settings ***
Documentation     Call AA HG
...               author - Narasimha.rao@mitel.com

#Test and Suite Setup and Teardown
Test Setup		Run Keywords	Test case PreCondition
#Test Teardown	 Run Keywords      Phone Sanity Run

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource         ../../Variables/LoginDetails.robot

#Component files
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone04}    WITH NAME    Phone04
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone08}    WITH NAME    Phone08

*** Test Cases ***
Call AA HG

	:FOR 	${INDEX}	 IN RANGE	0	500
		\	Using ${Phone04} I dial the digits ${AADID}
		\	BuiltIn.sleep   4s
		\	verify ${Phone04} on display of Auto-Attendant
		\	BuiltIn.sleep   1s
		\	Using ${Phone04} I dial the digits ${HGExtn}
		\	BuiltIn.sleep   10s
		\	answer the incoming call on ${Phone08}
		\	BuiltIn.sleep   2s
		\	disconnect the call from ${Phone04}
		\	BuiltIn.sleep   5s
		\	Run Keywords	Phone Sanity Run


*** Keywords ***
Test case PreCondition

    ${Phone04}=  Get library instance      Phone04
    ${Phone08}=  Get library instance      Phone08

    Set suite variable     ${Phone04}
    Set suite variable     ${Phone08}
    BuiltIn.sleep   2s

Phone Sanity Run
    Check Phone Sanity of ${Phone04}
    Check Phone Sanity of ${Phone08}
    BuiltIn.sleep   2s

    
