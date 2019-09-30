*** Settings ***
Documentation     Login to BOSS portal and Edit Hunt group with Invalid Extension
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
1 Login as staff user and Edit Hunt Group - Change to Invalid Extension
    [Tags]    Regression    HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=   Then I create hunt group    &{HuntgroupStaff}
    when I switch to "Visual_Call_Flow_Editor" page
    ${extn_num2}=   Then I create hunt group    &{HuntgroupStaff}
    And I select vcfe component by searching extension "${extn_num2}"
    Set to Dictionary    ${HuntgroupEdit}    HGExtn   ${extn_num}
    And I edit hunt group  &{HuntgroupEdit}
    And I click on cancel button
    [Teardown]  run keywords   I delete vcfe entry for ${HuntgroupEdit['HGExtn']}
    ...                        I delete vcfe entry for ${extn_num2}
    ...                        I log off
    ...                        I check for alert

2 Login as DM user and Edit Hunt Group - Change to Invalid Extension
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=   Then I create hunt group    &{HuntgroupDM}
    when I switch to "Visual_Call_Flow_Editor" page
    ${extn_num2}=   Then I create hunt group    &{HuntgroupDM}
    And I select vcfe component by searching extension "${extn_num2}"
    Set to Dictionary    ${HuntgroupEdit}    HGExtn   ${extn_num}
    And I edit hunt group  &{HuntgroupEdit}
    And I click on cancel button
    [Teardown]  run keywords   I delete vcfe entry for ${HuntgroupEdit['HGExtn']}
    ...                        I delete vcfe entry for ${extn_num2}
    ...                        I log off
    ...                        I check for alert

3 Login as DM user and Edit Hunt Group - Change to Invalid Extension
    [Tags]    Regression    HG    Generic
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${extn_num}=   Then I create hunt group    &{HuntgroupPM}
    when I switch to "Visual_Call_Flow_Editor" page
    ${extn_num2}=   Then I create hunt group    &{HuntgroupPM}
    And I select vcfe component by searching extension "${extn_num2}"
    Set to Dictionary    ${HuntgroupEdit}    HGExtn   ${extn_num}
    And I edit hunt group  &{HuntgroupEdit}
    And I click on cancel button
    [Teardown]  run keywords   I delete vcfe entry for ${HuntgroupEdit['HGExtn']}
    ...                        I delete vcfe entry for ${extn_num2}
    ...                        I log off
    ...                        I check for alert


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

