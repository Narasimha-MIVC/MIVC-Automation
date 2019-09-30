*** Settings ***
Documentation     Login to BOSS portal and Verify Programming Profile will be removed after removing Paging Group from VCFE
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

#1 Login as DM and Verify Programming Profile will be removed after removing Paging Group from VCFE
#    [Tags]    Regression    PG
#    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${Paginggroupedit_DM}    extnlistname    ${extnlistname}
#    ${extn_num}=    I add Paging Group    &{Paginggroupedit_DM}
#    Set to Dictionary    ${Paginggroupedit_DM}    Pg_Extension    ${extn_num}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${Paginggroupedit_DM['Pg_Name']}" is present in profiles tab
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
#    Then I verify "${Paginggroupedit_DM['Pg_Name']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert
#
#2 Login as PM and Verify Programming Profile will be removed after removing Paging Group from VCFE
#    [Tags]    Regression    PG
#    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${Paginggroupedit_PM}    extnlistname    ${extnlistname}
#    ${extn_num}=    I add Paging Group    &{Paginggroupedit_PM}
#    Set to Dictionary    ${Paginggroupedit_PM}    Pg_Extension    ${extn_num}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${Paginggroupedit_PM['Pg_Name']}" is present in profiles tab
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
#    Then I verify "${Paginggroupedit_PM['Pg_Name']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert

3 Login as Staff user and Verify Programming Profile will be removed after removing Paging Group from VCFE
    [Tags]    Regression    PG    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${PagingGroup}    extnlistname    ${extnlistname}
    ${extn_num}=    I add Paging Group    &{PagingGroup}
    Set to Dictionary    ${PagingGroup}    Pg_Extension    ${extn_num}
    Then I switch to "Visual_Call_Flow_Editor" page
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${PagingGroup['Pg_Name']}" is present in profiles tab
    when I switch to "Visual_Call_Flow_Editor" page
    Then I delete vcfe entry for ${extn_num}
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${PagingGroup['Pg_Name']}" is not present in profiles tab
    [Teardown]  run keywords  I log off
    ...                       I check for alert



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Paginggroupedit}
    : FOR    ${key}    IN    @{PagingGroup.keys()}
    \    ${updated_val}=    Replace String    ${PagingGroup["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PagingGroup}    ${key}    ${updated_val}

    Set suite variable    &{Paginggroupedit_DM}
    : FOR    ${key}    IN    @{Paginggroupedit_DM.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit_DM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit_DM}    ${key}    ${updated_val}

    Set suite variable    &{Paginggroupedit_PM}
    : FOR    ${key}    IN    @{Paginggroupedit_PM.keys()}
    \    ${updated_val}=    Replace String    ${Paginggroupedit_PM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Paginggroupedit_PM}    ${key}    ${updated_val}
