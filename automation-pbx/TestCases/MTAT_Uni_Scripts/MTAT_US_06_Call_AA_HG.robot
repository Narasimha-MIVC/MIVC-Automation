*** Settings ***
Documentation     Call AA HG
...               author - Mahabaleshwar.Hegde@mitel.com

#Test and Suite Setup and Teardown
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	 Run Keywords      Phone Sanity Run
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource        ../../../automation-boss/RobotKeywords/BOSSKeywords.robot
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource         ../../Variables/LoginDetails.robot

#Component files
Library           ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}    country=${country}     WITH NAME   Boss
Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02

*** Test Cases ***
Call AA HG

###################################Create AA ##############################################
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set suite variable     ${extn_num}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component    OnHoursSchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name     On-Hours
    set to dictionary    ${EditAA04}    Multiple_Digit_Operation    TransferToExtension
    set to dictionary    ${EditAA04}    MDO_Extension    ${Phone01.phone_obj.phone.extensionNumber}
    And I edit Auto-Attendant     &{EditAA04}
    BuiltIn.sleep   5s

###################################Phone Verification##############################################
	Using ${Phone01} I dial the digits ${extn_num}
    BuiltIn.sleep   4s
	#press key BottomKey1 from ${Phone01}
	#BuiltIn.sleep   2s
	verify ${Phone01} on display of Auto-Attendant
    BuiltIn.sleep   1s
	Using ${Phone01} I dial the digits ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   10s
	answer the incoming call on ${Phone02}
	BuiltIn.sleep   2s
    verify ${Phone02} on display of ${Phone01.phone_obj.phone.extensionNumber}
    verify ${Phone01} on display of ${Phone02.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   1s
    disconnect the call from ${Phone01}
    BuiltIn.sleep   5s


*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    BuiltIn.sleep   2s

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${AccName} with ${AccWithoutLogin} option

Phone Sanity Run
    I delete vcfe entry for ${extn_num}
    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    BuiltIn.sleep   2s

    
