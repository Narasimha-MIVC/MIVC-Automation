*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify DNIS can be edited and changed from Hunt Group  to Auto Attendant .
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
As staff verify DNIS can be edited and changed from Hunt Group to Auto Attendant.
    [Tags]    Sanity_Phase2    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option

    #creating Hunt Group
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${hg_extn}=    I create hunt group    &{HuntgroupDM}

    #creating Auto Attendant
    When I switch to "Visual_Call_Flow_Editor" page
    ${aa_extn_num}=    I add Auto-Attendant    &{AA_01}
    Set to Dictionary       ${AA_01}       aa_ext_num      ${aa_extn_num}

    When I switch to "phone_number" page
    #assigning available number to hunt group
#    ${Phone_num_Type}=  Set Variable    Domestic
    ${hg_name}=  Set Variable    ${HuntgroupDM['HGname']}${SPACE}x${hg_extn}

#    ${ph_number}=    I find phone number with required status    Available  ${None}  ${None}  USA (+1)
    ${ph_number}=    I find phone number with required status  Available  country=USA (+1)

    I assign phone number to Hunt Group  ${hg_name}
    And When I switch to "phone_number" page
    ${hg_name}=  Set Variable    ${HuntgroupDM['HGname']}${SPACE}HG${SPACE}x${hg_extn}
    And I find element on phone number page  ${ph_number}  Active  Hunt Group  ${hg_name}  ${True}

    &{aainfo}=  copy dictionary  ${AA_01}
    Set to Dictionary       ${aainfo}       auto_Attendant      Test_AA x${AA_01['aa_ext_num']}
    Set to Dictionary       ${aainfo}       AAname      Test_AA${SPACE}AA${SPACE}x${aa_extn_num}
    I edit DNIS from Phone Numbers Page     ${aainfo}
    And I find element on phone number page  ${ph_number}  Active  Auto Attendant  ${aainfo['AAname']}  ${True}
#    When I switch to "Visual_Call_Flow_Editor" page
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

    Set suite variable    ${HuntgroupDM}

    : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}
