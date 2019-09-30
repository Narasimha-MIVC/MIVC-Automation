*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify DNIS can be edited and changed from Hunt Group to Unassign.
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          ../BCA/Variables/BCA_Variables.py
Resource           ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String
*** Test Cases ***
1. Login as DM user and Verify DNIS can be edited and changed from Hunt Group to Unassign.
    [Tags]    Sanity_Phase2    Generic

    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}

    &{localhginfo}=  copy dictionary  ${BCA_INFO}

    #creating Hunt Group
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${hg_extn}=    I create hunt group    &{HuntgroupDM}

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

    set to dictionary  ${localhginfo}  Unassign    True
    And I edit DNIS from Phone Numbers Page   ${localhginfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${ph_number}  Available  ${None}  -  ${True}
    sleep  5s
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...         AND  sleep  3s
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
