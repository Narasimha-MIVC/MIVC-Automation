*** Settings ***
Documentation     Login to BOSS portal and Verify Programming Profile will be removed after removing Pickup Group from VCFE
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
#
#1 Login as DM and Verify Programming Profile will be removed after removing Pickup Group from VCFE
#    [Tags]    Regression    PK
#    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
#    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
#    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${Pickupgroup_Add['pickupgpname']}" is present in profiles tab
##    And I log off
##    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Then I delete vcfe entry for ${extn_num}
#    And I log off
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    When I switch to "primary_partition" page
#    And I move to "profiles" tab
#    Then I verify "${Pickupgroup_Add['pickupgpname']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert
#
#2 Login as PM and Verify Programming Profile will be removed after removing Pickup Group from VCFE
#    [Tags]    Regression    PK
#    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
#    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
#    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${Pickupgroup_Add['pickupgpname']}" is present in profiles tab
##    And I log off
##    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Then I delete vcfe entry for ${extn_num}
#    And I log off
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    When I switch to "primary_partition" page
#    And I move to "profiles" tab
#    Then I verify "${Pickupgroup_Add['pickupgpname']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert

3 Login as Staff user and Verify Programming Profile will be removed after removing Pickup Group from VCFE
    [Tags]    Regression    PK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    And I switch to "Visual_Call_Flow_Editor" page
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${Pickupgroup_Add['pickupgpname']}" is present in profiles tab
    when I switch to "Visual_Call_Flow_Editor" page
    Then I delete vcfe entry for ${extn_num}
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${Pickupgroup_Add['pickupgpname']}" is not present in profiles tab
    [Teardown]  run keywords  I log off
    ...                       I check for alert



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Pickupgroup_Add}
    : FOR    ${key}    IN    @{Pickupgroup_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_Add}    ${key}    ${updated_val}
