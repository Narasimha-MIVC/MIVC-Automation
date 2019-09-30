*** Settings ***
Documentation     verify Call Quality
...               dev-Lavanya
...               Contact : Lavanya Nagaraj

#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

#Component files
Library           ../../lib/PBXComponent.py
Library           BuiltIn
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone01}    WITH NAME    Phone01
Library           ../../../Framework/phone_wrappers/PhoneInterface.py  ${Phone02}    WITH NAME    Phone0

Suite Setup		Run Keywords	Test case PreCondition   Phone Sanity Run
Test Teardown	Run Keyword unless  '${TEST STATUS}'=='PASS'   Phone Sanity Run

*** Test Cases ***

Verify call quality

    [Tags]  MT AT Sanity

    ${no_of_calls}     set variable  1

    BuiltIn.sleep   150s

    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    ${no_of_calls_UserA_UserB_before} =  In D2 I verify call streams in call quality for ${Phone01.extension} and ${Phone02.extension} with ${AccName}
    Log to console    ${no_of_calls_UserA_UserB_before}

    : FOR    ${INDEX}    IN RANGE     ${no_of_calls}

    \   Log to console  This is ${INDEX} call out of ${no_of_calls}
    \   Log          STEP - 1 : Make call Phone01 to Phone02
    \   Using ${Phone01} I dial the digits ${Phone02.phone_obj.phone.extensionNumber}
    \   BuiltIn.sleep   2s

    \    Log          STEP - 2 : Phone02 will answer the call
    \    nswer the incoming call on ${Phone02}
    \    BuiltIn.sleep   30s

    \   Log          STEP - 3: Verify the caller name
    \      verify ${Phone02} on display of ${Phone01.phone_obj.phone.extensionNumber}
    \      verify ${Phone01} on display of ${Phone02.phone_obj.phone.extensionNumber}
    \    BuiltIn.sleep   1s

    \    Log          STEP - 4 : Phone02 End the call
    \    disconnect the call from ${Phone01}
    \    BuiltIn.sleep   1s

    BuiltIn.sleep   150s

    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    ${no_of_calls_UserA_UserB_after} =  In D2 I verify call streams in call quality for ${Phone01.extension} and ${Phone02.extension} with ${AccName}
    Log to console    ${no_of_calls_UserA_UserB_after}

    verify count ${Phone01} ${no_of_calls_UserA_UserB_before} ${no_of_calls_UserA_UserB_after} ${no_of_calls}
    
*** Keywords ***
Test case PreCondition

    ${Phone01}=  Get library instance      Phone01
    ${Phone02}=  Get library instance      Phone02

    Set suite variable     ${Phone01}
    Set suite variable     ${Phone02}
    BuiltIn.BuiltIn.sleep   2s

Phone Sanity Run

    Check Phone Sanity of ${Phone01}
    Check Phone Sanity of ${Phone02}
    BuiltIn.BuiltIn.sleep   2s
