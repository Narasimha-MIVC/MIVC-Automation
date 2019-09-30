*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify DNIS can be edited and changed from Auto Attendant to Hunt Group.
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource          ../../Variables/AutoAttendantInfo.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
*** Test Cases ***
As PM verify DNIS can be edited and changed from Auto Attendant to Hunt Group.
    [Tags]    Sanity_Phase2    two    Generic
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    #creating Auto Attendant
    When I switch to "Visual_Call_Flow_Editor" page
    ${aa_extn_num}=    I add Auto-Attendant    &{AA_01}

    #creating Hunt Group
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${hg_extn}=    I create hunt group    &{HuntgroupPM}

    Set to Dictionary       ${HuntgroupPM}       hg_extn_num      ${hg_extn}
    When I switch to "phone_number" page
    #assigning available number to auto attendant
#    ${Phone_num_Type}=  Set Variable    Domestic
    ${aa_name}=  Set Variable    Test_AA${SPACE}x${aa_extn_num}

#    ${ph_number}=    I find phone number with required status    Available  ${None}  ${None}  USA (+1)
    ${ph_number}=    I find phone number with required status  Available  country=USA (+1)

    I assign phone number to Auto Attendant  ${aa_name}
    And When I switch to "phone_number" page
    ${aa_name}=  Set Variable    Test_AA${SPACE}AA${SPACE}x${aa_extn_num}
    And I find element on phone number page  ${ph_number}  Active  Auto Attendant  ${aa_name}  ${True}
    &{hginfo}=  copy dictionary  ${HuntgroupPM}
    Set to Dictionary       ${hginfo}       hunt_Group      ${HuntgroupPM['HGname']} x${HuntgroupPM['hg_extn_num']}
    Set to Dictionary       ${hginfo}       HGname      ${HuntgroupPM['HGname']}
    I edit DNIS from Phone Numbers Page     ${hginfo}
    And I find element on phone number page  ${ph_number}  Active  Hunt Group  ${HuntgroupPM['HGname']}  ${True}
#    When I switch to "Visual_Call_Flow_Editor" page
    sleep  5s
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...         AND  sleep  3s
    ...         AND  I delete vcfe entry for ${aa_extn_num}
    ...         AND  I delete vcfe entry for ${hg_extn}
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    ${HuntgroupPM}

    : FOR    ${key}    IN    @{HuntgroupPM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM}    ${key}    ${updated_val}
