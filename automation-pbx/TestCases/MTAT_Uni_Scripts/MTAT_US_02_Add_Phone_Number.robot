*** Settings ***
Documentation     Provision the required TN
...               dev-Diksha,Neeraj,Lavanya,Maha

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
#Resource          ../../../Variables/PhoneNumberInfo.robot

#Component files
Library           ../../../automation-boss/lib/BossComponent.py    browser=${BROWSER}    country=${country}     WITH NAME   Boss
Library          ../../../Framework/phone_wrappers/phone_4xx/PPhoneInterface.py  WITH NAME       w2
Library          ../../lib/PBXComponent.py

*** Test Cases ***
Provision the required TN

    [Tags]  MT AT Sanity



    When I switch to "switch_account" page
    And I switch to account ${NewAccName} with ${AccWithoutLogin} option
    When I switch to "phonenumber" page
    I add PhoneNumber    &{PhoneNumber}
    and I set PhoneNumber state    &{PhoneNumber}
    Then I verify PhoneNumber state    &{PhoneNumber}

    In Varibale file LoginDetails.robot I update key PhoneNumber with field numberStart to value ${PhoneNumber.numberRange}
    
    
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
 
    ${uni_str}   Set variable    ${uni_str}
    ${uni_num}   Set variable    ${uni_num}

    Set suite variable     &{PhoneNumber}
    : FOR    ${key}    IN    @{PhoneNumber.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumber["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumber}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${PhoneNumber["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PhoneNumber}    ${key}    ${updated_val}

Test case PreCondition
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}

Test case PostCondition
    and I log off