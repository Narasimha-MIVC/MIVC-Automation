*** Settings ***
Documentation     Login to BOSS portal and Edit Hunt Group - Changed Name Already in Use
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
1 Login as staff user and Edit Hunt Group - Changed Name Already in Use
    [Tags]    Regression    HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=   Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn1    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff2}    hglocation    ${locationName}
    ${extn_num2}=   Then I create hunt group    &{HuntgroupStaff2}
    Set to Dictionary    ${HuntgroupStaff2}    HGExtn2    ${extn_num2}
    And I select vcfe component by searching extension "${HuntgroupStaff2['HGExtn2']}"
    Set to Dictionary    ${HuntgroupEdit}    HGname    ${HuntgroupStaff['HGname']}
    And I edit hunt group  &{HuntgroupEdit}
    When I switch to "Visual_Call_Flow_Editor" page
    And I select vcfe component by searching extension "${HuntgroupStaff2['HGExtn2']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${HuntgroupEdit['HGname']}" with extension "${HuntgroupStaff2['HGExtn2']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupStaff2['HGExtn2']}
    ...                       I delete vcfe entry for ${HuntgroupStaff['HGExtn1']}
    ...                      I log off
    ...                      I check for alert

2 Login as DM user and Edit Hunt Group - Changed Name Already in Use
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=   Then I create hunt group    &{HuntgroupDM}
    Set to Dictionary    ${HuntgroupDM}    HGExtn1    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM2}    hglocation    ${locationName}
    ${extn_num2}=   Then I create hunt group    &{HuntgroupDM2}
    Set to Dictionary    ${HuntgroupDM2}    HGExtn2    ${extn_num2}
    And I select vcfe component by searching extension "${HuntgroupDM2['HGExtn2']}"
    Set to Dictionary    ${HuntgroupEdit}    HGname    ${HuntgroupDM['HGname']}
    And I edit hunt group  &{HuntgroupEdit}
    When I switch to "Visual_Call_Flow_Editor" page
    And I select vcfe component by searching extension "${HuntgroupDM2['HGExtn2']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${HuntgroupEdit['HGname']}" with extension "${HuntgroupDM2['HGExtn2']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupDM2['HGExtn2']}
    ...                       I delete vcfe entry for ${HuntgroupDM['HGExtn1']}
    ...                      I log off
    ...                      I check for alert

3 Login as PM user and Edit Hunt Group - Changed Name Already in Use
    [Tags]    Regression    HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${extn_num}=   Then I create hunt group    &{HuntgroupPM}
    Set to Dictionary    ${HuntgroupPM}    HGExtn1    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM2}    hglocation    ${locationName}
    ${extn_num2}=   Then I create hunt group    &{HuntgroupPM2}
    Set to Dictionary    ${HuntgroupPM2}    HGExtn2    ${extn_num2}
    And I select vcfe component by searching extension "${HuntgroupPM2['HGExtn2']}"
    Set to Dictionary    ${HuntgroupEdit}    HGname    ${HuntgroupPM['HGname']}
    And I edit hunt group  &{HuntgroupEdit}
    When I switch to "Visual_Call_Flow_Editor" page
    And I select vcfe component by searching extension "${HuntgroupPM2['HGExtn2']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${HuntgroupEdit['HGname']}" with extension "${HuntgroupPM2['HGExtn2']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupPM2['HGExtn2']}
    ...                       I delete vcfe entry for ${HuntgroupPM['HGExtn1']}
    ...                      I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{HuntgroupStaff}
    Set suite variable    &{HuntgroupStaff2}
    Set suite variable    &{HuntgroupDM}
    Set suite variable    &{HuntgroupDM2}
    Set suite variable    &{HuntgroupPM}
    Set suite variable    &{HuntgroupPM2}


    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupStaff2.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff2["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff2}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupDM2.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM2["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM2}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupPM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupPM2.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM2["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM2}    ${key}    ${updated_val}


