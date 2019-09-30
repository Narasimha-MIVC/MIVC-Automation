*** Settings ***
Documentation     Login to BOSS portal and Add new Hunt group with blank name
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
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
1 Login as staff user and Add New Hunt Group - Blank Name
    [Tags]    Regression    HG    AUS    UK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    Set to Dictionary    ${HuntgroupStaff}    grp_member    ${user2_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    HGname    ${HuntgroupEdit['HGname']}
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    Set to Dictionary    ${HuntgroupStaff}  error_message  This field is required
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    And I verify "${HuntgroupStaff['error_message']}" is displayed on screen
    Then I click on cancel button
    [Teardown]  run keywords  I log off
    ...                      I check for alert



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{HuntgroupStaff}


    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}


