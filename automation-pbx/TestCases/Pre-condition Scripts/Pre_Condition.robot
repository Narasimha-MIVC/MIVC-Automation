*** Settings ***
Documentation     Phone Automation : Mitel_Create_Phone_Dictionary	
...               author - neeraj.narwaria@mitel.com

...          	DESCRIPTION:

#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

#Component
Library           Dialogs
Library		      ../../lib/PBXComponent.py

*** Test Cases ***
01.Mitel_Create_Phone_Dictionary

    ${D2_Login_IP} =   Get Value From User   Give D2 Login IP :    10.32.129.70:5478
    #In Varibale file D2Details.robot I update key D2IP with value ${D2_Login_IP}
    ${D2_Login_Username} =   Get Value From User   Give D2 Login Username :    admin@shoretel.com
    #In Varibale file D2Details.robot I update key D2User with value ${D2_Login_Username}
    ${D2_Login_Password} =   Get Value From User   Give D2 Login Password :    Shoreadmin1#
    #In Varibale file D2Details.robot I update key D2Password with value ${D2_Login_Password}

    ${BOSS_Acc_Name} =   Get Value From User   Give BOSS Account Name :    SVLAutomation-RUM-TEST1
    #In Varibale file LoginDetails.robot I update key AccName with value ${BOSS_Acc_Name}
	
	Log to console  STEP - 0 : Login to D2
    In D2 ${D2_Login_IP} I login with ${D2_Login_Username} and ${D2_Login_Password}

	${numberofPhones} =   Get Value From User   Number of Phones Used :    6
    ${numberofPhones}=  Evaluate  ${numberofPhones} + 1
	: FOR    ${INDEX}    IN RANGE    1    ${numberofPhones}
    \   ${PhoneID}=   Catenate   DemoPhone${INDEX}
	\	Set suite Variable	${PhoneID}
	\   ${EXTN} =   Get Value From User   Give Phone ${INDEX} Extension :    2410
	\   set suite variable  ${EXTN}
	\	&{result}=		I fetch phone details for extension ${EXTN} under ${BOSS_Acc_Name} Tenant
	\	Set suite Variable  &{result}
	\	Log to console 	STEP - ${INDEX} : Update ${file_to_be_update} file with follwong parameters &{result}
	\	${bool}=    Run Keyword And Return Status    Should Contain    ${result.phoneModel}    IP
	\	Run Keyword If    ${bool} == True	Update file for IP4XX Phone
	\	...			ELSE	Update file for Mitel Phone
	
*** Keywords ***
Update file for IP4XX Phone
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field phoneModel to value phone_4xx
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field ip to value ${result.ipAddress}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field phoneName to value ${result.phoneName}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field extension to value ${EXTN}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field phone_model to value ${result.phone_model}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field PPhone_mac to value ${result.mac}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field hq_rsa to value hq_rsa
	#In Varibale file ${file_to_be_update} I update existing key ${PhoneID} with field extensionNumber to new key value extension

Update file for Mitel Phone
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field phoneModel to value Mitel${result.phoneModel}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field ipAddress to value ${result.ipAddress}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field phoneName to value ${result.phoneName}
	In Varibale file ${file_to_be_update} I update key ${PhoneID} with field extensionNumber to value ${EXTN}

