*** Settings ***
Documentation     AnyPhone using 731
...               author - Mahabaleshwar.Hegde@mitel.com

#Keywords Definition file
Resource            ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone02

Test Setup		Run Keywords	Test case PreCondition
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run


*** Test Cases ***
AnyPhone using 731

    [Tags]  MT AT Sanity

    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    ${vm_extn}=  In D2 I get vm_login_dn extension system
    log to console   ${vm_extn}
##
    Log          STEP - 1 : Login to Voice Mail, Play and Delete
    Using ${Phone02} I dial the digits ${vm_extn}
    #Using ${Phone02} I dial the digits 8991
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   2s
    Using ${Phone02} I dial the digits ${Phone01.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits ${Phone01.phone_obj.phone.authCode}
    #Using ${Phone02} I dial the digits 123456
    BuiltIn.sleep   1s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   15s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits 7
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits 3
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits 1
    BuiltIn.sleep   30s

    verify ${Phone02} on display extn of ${Phone01.phone_obj.phone.extensionNumber}

    verify ${Phone01} on display of Anonymous
#
    Log          STEP - 2 : Login to Voice Mail, Play and Delete
    Using ${Phone02} I dial the digits ${vm_extn}
    #Using ${Phone02} I dial the digits 8991
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   2s
    Using ${Phone02} I dial the digits ${Phone01.phone_obj.phone.extensionNumber}
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits ${Phone01.phone_obj.phone.authCode}
    #Using ${Phone02} I dial the digits 16079
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits #
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits 7
    BuiltIn.sleep   10s
    Using ${Phone02} I dial the digits 3
    BuiltIn.sleep   5s
    Using ${Phone02} I dial the digits 2
    BuiltIn.sleep   30s

    verify ${Phone02} on display extn of ${Phone02.phone_obj.phone.extensionNumber}

    verify ${Phone01} on display of ${Phone01.phone_obj.phone.extensionNumber}


*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    BuiltIn.sleep   2s
