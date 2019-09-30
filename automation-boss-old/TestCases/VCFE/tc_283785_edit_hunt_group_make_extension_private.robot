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
Resource           ../../Variables/Hunt_Group_Info.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
1 Login as staff and Edit Hunt Group - Make Extension Private
    [Tags]    Regression    HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupEdit}    Make_extension_private    True
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    And I edit hunt group  &{HuntgroupEdit}
    Then I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    And I verify updated hunt group value  &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    ...                       I log off
    ...                       I check for alert

2 Login as DM and Edit Hunt Group - Make Extension Private
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
    Set to Dictionary    ${HuntgroupDM}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupEdit}    Make_extension_private    True
    Then I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    And I edit hunt group  &{HuntgroupEdit}
    Then I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    And I verify updated hunt group value  &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupDM['HGExtn']}
    ...                       I log off
    ...                       I check for alert


3 Login as PM and Edit Hunt Group - Make Extension Private
    [Tags]    Regression    HG
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupPM}
    Set to Dictionary    ${HuntgroupPM}    HGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupEdit}    Make_extension_private    True
    Then I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    And I edit hunt group  &{HuntgroupEdit}
    Then I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    And I verify updated hunt group value  &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupPM['HGExtn']}
    ...                       I log off
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
