*** Settings ***
Documentation     Login to BOSS portal and Verify Programming Profile will be removed after removing AA from VCFE
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

#1 Login as DM and Verify Programming Profile will be removed after removing AA from VCFE
#    [Tags]    Regression    AA
#    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${AA_DM}    Aa_Location    ${locationName}
#    ${extn_num}=    And I add Auto-Attendant    &{AA_DM}
#    Set to Dictionary    ${AA_DM}    AA_Extension    ${extn_num}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${AA_DM['Aa_Name']}" is present in profiles tab
##    And I log off
##    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Then I delete vcfe entry for ${AA_DM['AA_Extension']}
#    And I log off
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    When I switch to "primary_partition" page
#    And I move to "profiles" tab
#    Then I verify "${AA_DM['Aa_Name']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert
#
#2 Login as PM and Verify Programming Profile will be removed after removing AA from VCFE
#    [Tags]    Regression    AA
#    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Set to Dictionary    ${AA_PM}    Aa_Location    ${locationName}
#    ${extn_num}=    And I add Auto-Attendant    &{AA_PM}
#    Set to Dictionary    ${AA_PM}    AA_Extension    ${extn_num}
##    And I log off
##    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
##    When I switch to "switch_account" page
##    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
##    When I switch to "primary_partition" page
##    And I move to "profiles" tab
##    Then I verify "${AA_PM['Aa_Name']}" is present in profiles tab
##    And I log off
##    Given I login to ${URL} with ${PMemail} and ${PMpassword}
#    when I switch to "Visual_Call_Flow_Editor" page
#    Then I delete vcfe entry for ${AA_PM['AA_Extension']}
#    And I log off
#    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    When I switch to "switch_account" page
#    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
#    When I switch to "primary_partition" page
#    And I move to "profiles" tab
#    Then I verify "${AA_PM['Aa_Name']}" is not present in profiles tab
#    [Teardown]  run keywords   I log off
#   ...                       I check for alert

1 Login as Staff user and Verify Programming Profile will be removed after removing AA from VCFE
    [Tags]    Regression    AA    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${AA_staff}    Aa_Location    ${locationName}
    ${extn_num}=    And I add Auto-Attendant    &{AA_staff}
    Set to Dictionary    ${AA_staff}    AA_Extension    ${extn_num}
    Then I switch to "Visual_Call_Flow_Editor" page
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${AA_staff['Aa_Name']}" is present in profiles tab
    when I switch to "Visual_Call_Flow_Editor" page
    Then I delete vcfe entry for ${AA_staff['AA_Extension']}
    When I switch to "primary_partition" page
    And I move to "profiles" tab
    Then I verify "${AA_staff['Aa_Name']}" is not present in profiles tab
    [Teardown]  run keywords  I log off
    ...                       I check for alert



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${geolocationDetails}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    ${AA_staff}

    : FOR    ${key}    IN    @{AA_staff.keys()}
    \    ${updated_val}=    Replace String    ${AA_staff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AA_staff}    ${key}    ${updated_val}

    Set suite variable    ${AA_DM}

    : FOR    ${key}    IN    @{AA_DM.keys()}
    \    ${updated_val}=    Replace String    ${AA_DM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AA_DM}    ${key}    ${updated_val}

    Set suite variable    ${AA_PM}

    : FOR    ${key}    IN    @{AA_PM.keys()}
    \    ${updated_val}=    Replace String    ${AA_PM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AA_PM}    ${key}    ${updated_val}