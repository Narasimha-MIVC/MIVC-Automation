*** Settings ***
Documentation     Login to BOSS portal and edit Hunt group
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

1 Login as Staff user and Edit Hunt Group - Edit Call Forward Settings - Off-hours or Holiday destination
    [Tags]    Regression    HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    Set to Dictionary    ${HuntgroupEdit}    Off_hours_or_holiday_destination    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    Then I edit hunt group  &{HuntgroupEdit}
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    user_name    ${request_by}
    Then I verify updated hunt group value    &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


2 Login as DM and Edit Hunt Group - Edit Call Forward Settings - Off-hours or Holiday destination
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    Set to Dictionary    ${HuntgroupEdit}    Off_hours_or_holiday_destination    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
    Set to Dictionary    ${HuntgroupDM}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    Then I edit hunt group  &{HuntgroupEdit}
    Then I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    user_name    ${request_by}
    Then I verify updated hunt group value    &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    I delete vcfe entry for ${HuntgroupDM['HGExtn']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


3 Login as PM and Edit Hunt Group - Edit Call Forward Settings - Off-hours or Holiday destination
    [Tags]    Regression    HG
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    Set to Dictionary    ${HuntgroupEdit}    Off_hours_or_holiday_destination    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupPM}
    Set to Dictionary    ${HuntgroupPM}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    Then I edit hunt group  &{HuntgroupEdit}
    Then I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    user_name    ${request_by}
    Then I verify updated hunt group value    &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    I delete vcfe entry for ${HuntgroupPM['HGExtn']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{HuntgroupStaff}
    Set suite variable    &{HuntgroupDM}
    Set suite variable    &{HuntgroupPM}

    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupPM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM}    ${key}    ${updated_val}
