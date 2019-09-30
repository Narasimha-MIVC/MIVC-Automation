*** Settings ***
Documentation     Login to BOSS portal and edit Hunt group and check the functionality of up arrow and
...               arrow button in add member page
...               dev-Immani Mahesh Kumar
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

1 Login as Staff and Edit Hunt Group and check functionality of up arrow and down arrow button
    [Tags]    Regression    HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    set to dictionary  ${HuntgroupEdit}     up_down_grp_member      1000
    set to dictionary  ${HuntgroupEdit}     grp_member      ${request_by}
    set to dictionary  ${HuntgroupEdit}     verify_up_down_button       down
    Then I edit hunt group  &{HuntgroupEdit}
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    ...                       I log off
    ...                       I check for alert


2 Login as DM and Edit Hunt Group and check functionality of up arrow and down arrow button
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
     when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    set to dictionary  ${HuntgroupEdit}     up_down_grp_member      1000
    set to dictionary  ${HuntgroupEdit}     grp_member      ${request_by}
    set to dictionary  ${HuntgroupEdit}     verify_up_down_button       down
    Then I edit hunt group  &{HuntgroupEdit}
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    ...                       I log off
    ...                       I check for alert

3 Login as PM and Edit Hunt Group and check functionality of up arrow and down arrow button
    [Tags]    Regression    HG
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    set to dictionary  ${HuntgroupEdit}     up_down_grp_member      1000
    set to dictionary  ${HuntgroupEdit}     grp_member      ${request_by}
    set to dictionary  ${HuntgroupEdit}     verify_up_down_button       down
    Then I edit hunt group  &{HuntgroupEdit}
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    ...                       I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    &{HuntgroupStaff}


    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}

