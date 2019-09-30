*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify DNIS can be edited and changed from Hunt Group to Bridge Call Appearance.
...              Palla Surya Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Variables         ../BCA/Variables/BCA_Variables.py
Resource           ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
*** Test Cases ***
As PM verify DNIS can be edited and changed from Hunt Group to Bridge Call Appearance.
    [Tags]    Sanity_Phase2    Generic
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  3s

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    #switch to BCA page
    &{bca}=  create dictionary
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
    When I switch to "bridged_call_appearances" page

    #add BCA
    And I create Bridged Call Appearance  ${localbcainfo}
    &{bca}=  copy dictionary  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    #creating Hunt Group
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    ${hg_extn}=    I create hunt group    &{HuntgroupPM}

    #assigning available number to Hunt Group
    When I switch to "phone_number" page
    ${hg_name}=  Set Variable    ${HuntgroupPM['HGname']}${SPACE}x${hg_extn}
#    ${ph_number}=    I find phone number with required status    Available  ${None}  ${None}  USA (+1)
    ${ph_number}=    I find phone number with required status  Available  country=USA (+1)
    I assign phone number to Hunt Group  ${hg_name}

    #verify created vcfe component
    And When I switch to "phone_number" page
    ${hg_name}=  Set Variable    ${HuntgroupPM['HGname']}${SPACE}HG${SPACE}x${hg_extn}
    And I find element on phone number page  ${ph_number}  Active  Hunt Group  ${hg_name}  ${True}

    #edit vcfe to BCA and verify the BCA.
    &{bcainfo}=  copy dictionary  ${localbcainfo}
    Set to Dictionary       ${bcainfo}       bridged_Call_Appearance_name      ${localbcainfo['ProfileName']} x${localbcainfo['Extension']}
    I edit DNIS from Phone Numbers Page     ${bcainfo}
    And I find element on phone number page  ${ph_number}  Active  Bridged Call Appearance  ${localbcainfo['ProfileName']} BCA x${localbcainfo['Extension']}  ${True}
    sleep  3s
    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  sleep  3s
    ...         AND  I delete BCA  ${bca}
    ...         AND  I switch to "Visual_Call_Flow_Editor" page
    ...         AND  sleep  3s
    ...         AND  I delete vcfe entry for ${hg_extn}
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}

Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    ${HuntgroupPM}

    : FOR    ${key}    IN    @{HuntgroupPM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM}    ${key}    ${updated_val}
