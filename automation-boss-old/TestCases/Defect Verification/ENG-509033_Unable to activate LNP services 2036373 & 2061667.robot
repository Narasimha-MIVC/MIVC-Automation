*** Settings ***
Documentation     BOSS BCO Sanity suite
...               dev-Kenash, Rahul, Vasuja


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
#Library           PPhoneInterface

*** Test Cases ***

Activate Local number Portability Services
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    When I switch to account ${PhoneTransfer['userName']} with ${AccWithoutLogin} option
    and I switch to "services" page
    ${order_number}=  then I add LNP service    &{LNP_service}
    then I activate LNP service for ${order_number} and ${PhoneTransfer['phone']}
    and I log off

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    3    [NUMBERS]

    Set suite variable    ${uni_num}

    Set suite variable    &{PhoneTransfer}
    : FOR    ${key}    IN    @{PhoneTransfer.keys()}
    \    ${updated_val}=    Replace String    ${PhoneTransfer["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneTransfer}    ${key}    ${updated_val}
