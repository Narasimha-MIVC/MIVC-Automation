*** Settings ***
Documentation     Login to BOSS portal and create Hunt group
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
1 Login as staff user and Edit Hunt Group - Edit Group Members - Add New Member
    [Tags]    Regression   HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    grp_member    ${user_extn}
    And I edit hunt group  &{HuntgroupEdit}
    And I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify hunt group member "${HuntgroupEdit['grp_member']}" for "${HuntgroupStaff['HGExtn']}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  And I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    ...                       I log off
    ...                       I check for alert

2 Login as DM user and Edit Hunt Group - Edit Group Members - Add New Member
    [Tags]    Regression   HG    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
    Set to Dictionary    ${HuntgroupDM}    HGExtn    ${extn_num}
    And I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    grp_member    ${user_extn}
    And I edit hunt group  &{HuntgroupEdit}
    And I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify hunt group member "${HuntgroupEdit['grp_member']}" for "${HuntgroupDM['HGExtn']}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  And I delete vcfe entry for ${HuntgroupDM['HGExtn']}
    ...                       I log off
    ...                       I check for alert

3 Login as PM user and Edit Hunt Group - Edit Group Members - Add New Member
    [Tags]    Regression   HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupPM}
    Set to Dictionary    ${HuntgroupPM}    HGExtn    ${extn_num}
    And I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    grp_member    ${user_extn}
    And I edit hunt group  &{HuntgroupEdit}
    And I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify hunt group member "${HuntgroupEdit['grp_member']}" for "${HuntgroupPM['HGExtn']}" is set for ${params['partition_id']}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  And I delete vcfe entry for ${HuntgroupPM['HGExtn']}
    ...                       I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

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
