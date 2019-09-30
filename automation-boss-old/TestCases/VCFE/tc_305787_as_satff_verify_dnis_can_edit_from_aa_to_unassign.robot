*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify DNIS can be edited and changed from Auto Attendant to Unassign.
...              Palla Surya Kumar

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

Suite Teardown    Close The Browsers

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource          ../../Variables/AutoAttendantInfo.robot
Variables          ../BCA/Variables/BCA_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
1. Login as staff user and Verify DNIS can be edited and changed from Auto Attendant to Unassign.
    [Tags]    Sanity_Phase2    Regression    Generic

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3s
    &{localaainfo}=  copy dictionary  ${BCA_INFO}

    #creating Auto Attendant
    When I switch to "Visual_Call_Flow_Editor" page
    ${aa_extn_num}=    I add Auto-Attendant    &{AA_01}

    When I switch to "phone_number" page
    #assigning available number to auto attendant
    ${aa_name}=  Set Variable    Test_AA${SPACE}x${aa_extn_num}

    ${ph_number}=    I find phone number with required status  Available  country=USA (+1)

    I assign phone number to Auto Attendant  ${aa_name}
    And When I switch to "phone_number" page
    ${aa_name}=  Set Variable    Test_AA${SPACE}AA${SPACE}x${aa_extn_num}
    And I find element on phone number page  ${ph_number}  Active  Auto Attendant  ${aa_name}  ${True}

    set to dictionary  ${localaainfo}  Unassign    True
    And I edit DNIS from Phone Numbers Page   ${localaainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${ph_number}  Available  ${None}  -  ${True}
    sleep  5s
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...         AND  sleep  3s
    ...         AND  I delete vcfe entry for ${aa_extn_num}
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
