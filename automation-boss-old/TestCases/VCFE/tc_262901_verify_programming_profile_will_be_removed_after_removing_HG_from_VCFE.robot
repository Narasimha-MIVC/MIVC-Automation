*** Settings ***
Documentation     Login to BOSS portal and Verify Programming Profile will be removed after removing HG from VCFE
#...               dev-Vasuja
#...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot


#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}    country=${country}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***

#1 Login as DM and Verify Programming Profile will be removed after removing HG from VCFE
#    [Tags]    Regression    HG
#    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
#    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
#    Set to Dictionary    ${HuntgroupDM}    HGExtn    ${extn_num}
##    And I log off
##    sleep  2s
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${HuntgroupDM['HGname']}" is present in profiles tab
##    And I log off
##    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Then I delete vcfe entry for ${HuntgroupDM['HGExtn']}
#    And I log off
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    When I switch to "primary_partition" page
#    And I move to "profiles" tab
#    Then I verify "${HuntgroupDM['HGname']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert
#
#2 Login as PM and Verify Programming Profile will be removed after removing HG from VCFE
#    [Tags]    Regression    HG
#    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
#    ${extn_num}=    Then I create hunt group    &{HuntgroupPM}
#    Set to Dictionary    ${HuntgroupPM}    HGExtn    ${extn_num}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${HuntgroupPM['HGname']}" is present in profiles tab
##    And I log off
##    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Then I delete vcfe entry for ${HuntgroupPM['HGExtn']}
#    And I log off
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    When I switch to "primary_partition" page
#    And I move to "profiles" tab
#    Then I verify "${HuntgroupPM['HGname']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert

3 Login as Staff user and Verify Programming Profile will be removed after removing HG from VCFE
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    Then I switch to "Visual_Call_Flow_Editor" page
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${HuntgroupStaff['HGname']}" is present in profiles tab
    when I switch to "Visual_Call_Flow_Editor" page
    Then I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${HuntgroupStaff['HGname']}" is not present in profiles tab
    [Teardown]  run keywords  I log off
    ...                       I check for alert



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${geolocationDetails}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    ${HuntgroupStaff}

    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}

    Set suite variable    ${HuntgroupDM}

    : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}

    Set suite variable    ${HuntgroupPM}

    : FOR    ${key}    IN    @{HuntgroupPM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM}    ${key}    ${updated_val}