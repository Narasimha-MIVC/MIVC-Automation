*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***

Create primary partition
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    When I switch to account ${AOBAccount} with ${AccWithoutLogin} option
    When I switch to "partitions" page
    set to dictionary  ${PartitionDetails}  partitionName    ${AOBAccount}
    Then I verify that Partition is set as Primary    &{PartitionDetails}
    And I log off

*** Keywords ***
#Set Init Env
#    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
#    ${uni_int}=    Generate Random String    3    0123456789
#    ${ext}=    Generate Random String    4    12345678
#    Set suite variable    ${uni_str}
#    Set suite variable    ${uni_int}
#
#    Set suite variable    &{AOBPhoneNumber}
#    : FOR    ${key}    IN    @{AOBPhoneNumber.keys()}
#    \    ${updated_val}=    Replace String    ${AOBPhoneNumber["${key}"]}    {rand_int}    ${uni_int}
#    \    Set To Dictionary    ${AOBPhoneNumber}    ${key}    ${updated_val}
#
#    Set suite variable    &{AobUserDetail}
#    : FOR    ${key}    IN    @{AobUserDetail.keys()}
#    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_str}    ${uni_str}
#    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}
#
#    Set suite variable    &{AobUserDetail}
#    : FOR    ${key}    IN    @{AobUserDetail.keys()}
#    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_int}    ${ext}
#    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}