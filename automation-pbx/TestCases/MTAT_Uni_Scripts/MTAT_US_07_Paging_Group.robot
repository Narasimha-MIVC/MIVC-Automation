*** Settings ***
Documentation     Create Paging Group
...               author - Mahabaleshwar.Hegde@mitel.com

#Test and Suite Setup and Teardown
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keywords    Test case PostCondition
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
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone03}    WITH NAME    Phone03


***Test Cases***
Create Paging Group
###################################Create Extension list##############################################

    @{usrlist}=   Create List     ${Phone01.phone_obj.phone.extensionNumber}    ${Phone02.phone_obj.phone.extensionNumber}      ${Phone03.phone_obj.phone.extensionNumber}
    Set suite variable     ${usrlist}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${usrlist}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}

################################Create Paging Group#################################################

    Set to Dictionary    ${PagingGroup}    extnlistname    ${Extensionlist01['extnlistname']}
    ${extn_num}=    I add Paging Group    &{PagingGroup}
    Set suite variable     ${extn_num}
    and I verify the group for ${extn_num}

###################################Phone Verification##############################################
    BuiltIn.sleep   40s
	Using ${Phone01} I dial the digits ${extn_num}
    BuiltIn.sleep   4s
	verify ${Phone02} on display of ${PagingGroup.Pg_Name}
    verify ${Phone03} on display of ${PagingGroup.Pg_Name}
    BuiltIn.sleep   2s
    disconnect the call from ${Phone01}
    BuiltIn.sleep   5s

*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02
    ${Phone03}=  Get library instance      Phone03

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    Set suite variable     ${Phone03}

    BuiltIn.sleep   2s

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${AccName} with ${AccWithoutLogin} option

Test case PostCondition
     I delete vcfe entry for ${extn_num}
     I delete vcfe entry by name ${Extensionlist01['extnlistname']}
     I log off
    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    Check Phone Sanity of ${Phone03}
    BuiltIn.sleep   2s

