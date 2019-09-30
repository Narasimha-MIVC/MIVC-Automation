*** Settings ***
Documentation     New User Creation and assign to phone
...                dev - Maha
...               Contact : Mahabaleshwar Hegde

#Suite Setup and Teardown
Suite Setup       Set Init Env
Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keywords    Test case PostCondition
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../../automation-boss/RobotKeywords/BOSSKeywords.robot
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

#Component files
Library           ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}    country=${country}     WITH NAME   Boss
Library          ../../lib/PBXComponent.py
Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone001}    WITH NAME    Phone001

*** test Cases ***
New User Creation and assign to phone

    When I switch to "users" page
    set to dictionary  ${GenUser}  login_user   staff
    ${phone_num}  ${extn}   ${status}=      I add user    &{GenUser}
	Log to Console		phone no , extnesion and status ${phone_num} ${extn} ${status}
    BuiltIn.sleep
    Then I verify that User exist in user table    &{GenUser}
    BuiltIn.sleep
    When I switch to "users" page
    And I assign User ${GenUser["au_businessmail"]} in user group ${GenUser['userGroupName']}
    Log to console    did for new created user is ${phone_num}
#    ${phone_num}   set variable  14087138017
#    ${NewAccId}    set variable  16079

    Log to console		phone enter cloud credentials did= ${phone_num} and password= ${NewAccId}
    Using ${Phone001} I dial the digits ${phone_num}
    BuiltIn.sleep   5s
	press key ScrollDown from ${Phone001}
	BuiltIn.sleep   5s
    Using ${Phone001} I dial the digits ${NewAccId}
    BuiltIn.sleep  2s
    Log to console    phone with did= ${phone_num} press ok button(softkey 5)
    press key Quit from ${Phone001}
    BuiltIn.sleep  30s

    Using ${Phone001} I dial the digits 123456
    BuiltIn.sleep   5s
    press key ScrollDown from ${Phone001}
    Using ${Phone001} I dial the digits 123456
    BuiltIn.sleep   2s
    press key Quit from ${Phone001}


    verify ${Phone001} on display of ${GenUser["au_firstname"]}

    When I switch to "phone_system_phones" page
    I search mac address ${Phone001.phone_obj.phone.macAddress} and delete


    
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

   Set suite variable     &{GenUser}
    : FOR    ${key}    IN    @{GenUser.keys()}
    \    ${updated_val}=    Replace String    ${GenUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${GenUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${GenUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary   ${GenUser}    ${key}    ${updated_val}

Test case PreCondition
    ${Phone001}=  Get library instance      Phone001
    Set suite variable     ${Phone001}
    BuiltIn.sleep   2s

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${NewAccName} with ${AccWithoutLogin} option

Test case PostCondition
    and I log off