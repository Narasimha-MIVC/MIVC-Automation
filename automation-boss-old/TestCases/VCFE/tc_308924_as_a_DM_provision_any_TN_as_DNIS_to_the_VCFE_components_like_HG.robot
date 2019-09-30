*** Settings ***
Documentation     Login to BOSS portal and validate TN is assigned to Hunt group after Save
...               dev-Vasuja
...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/EnvVariables.robot
Variables          ../BCA/Variables/BCA_Variables.py
Resource           ../VCFE/Variables/Vcfe_variables.robot


Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Login to the boss portal as DM user and validate TN is assigned to Hunt group after Save
    [Tags]    Sanity_Phase2    Regression    Generic
    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    ### Actions:
    #1. Switch to VCFE page and create Hunt group
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
    Set to Dictionary    ${HuntgroupDM}    HGExtn    ${extn_num}
    #2. Switch to the phone system -> phone numbers page and assign an available phone number to Hunt group
    And I switch to "phone_systems_phone_numbers" page
    ${phone_no}=    I find phone number with required status  Available  country=USA (+1)
    set to dictionary  ${HuntgroupDM}  hunt_Group    ${HuntgroupDM['HGname']} x${HuntgroupDM['HGExtn']}
    Then I assign phone number to vcfe component  &{HuntgroupDM}
    sleep  2s
    [Teardown]
    Run Keywords  I log off
    ...           I check for alert

*** Keywords ***

Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HuntgroupDM}

    : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}