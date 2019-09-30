*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify DNIS can be edited and changed from Auto Attendant to Bridge Call Appearance.
...              Palla Surya Kumar

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

Suite Teardown    Close The Browsers

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../../Variables/AutoAttendantInfo.robot
Variables         ../BCA/Variables/BCA_Variables.py

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String

*** Test Cases ***
As DM verify DNIS can be edited and changed from Auto Attendant to Bridge Call Appearance.
    [Tags]    Sanity_Phase2    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
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

    #creating Auto Attendant
    When I switch to "Visual_Call_Flow_Editor" page
    ${aa_extn_num}=    I add Auto-Attendant    &{AA_01}

    #assigning available number to auto attendant
    When I switch to "phone_number" page
    ${aa_name}=  Set Variable    Test_AA${SPACE}x${aa_extn_num}
#    ${ph_number}=    I find phone number with required status    Available  ${None}  ${None}  USA (+1)
    ${ph_number}=    I find phone number with required status  Available  country=USA (+1)
    I assign phone number to Auto Attendant  ${aa_name}

    #verify created vcfe component
    And When I switch to "phone_number" page
    ${aa_name}=  Set Variable    Test_AA${SPACE}AA${SPACE}x${aa_extn_num}
    And I find element on phone number page  ${ph_number}  Active  Auto Attendant  ${aa_name}  ${True}

    #edit vcfe to BCA and verify the BCA.
    &{bcainfo}=  copy dictionary  ${localbcainfo}
    Set to Dictionary       ${bcainfo}       bridged_Call_Appearance_name      ${localbcainfo['ProfileName']} x${localbcainfo['Extension']}
    I edit DNIS from Phone Numbers Page     ${bcainfo}
    And I find element on phone number page  ${ph_number}  Active  Bridged Call Appearance  ${localbcainfo['ProfileName']} BCA x${localbcainfo['Extension']}  ${True}
    sleep  5s
    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  sleep  3s
    ...         AND  I delete BCA  ${bca}
    ...         AND  I switch to "Visual_Call_Flow_Editor" page
    ...         AND  sleep  3s
    ...         AND  I delete vcfe entry for ${aa_extn_num}
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}

