*** Settings ***
Documentation    BOSS Sanity Test Cases Phase 2
...                 Verify destination type in Phone numbers page.
...              Palla Surya Kumar

Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource          ../../Variables/AutoAttendantInfo.robot
Resource           ../../Variables/PhoneNumberInfo.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
*** Test Cases ***
As a DM verify destination type in Phone numbers page.
    [Tags]    Sanity_Phase2    Regression
    Given I login to ${URL} with ${DMemail} and ${DMpassword}

    When I switch to "Visual_Call_Flow_Editor" page
    ${aa_extn_num}=    I add Auto-Attendant    &{AA_01}
    When I switch to "phone_number" page
    #assigning available number to auto attendant
#    ${Phone_num_Type}=  Set Variable    Domestic
    ${aa_name}=  Set Variable    Test_AA${SPACE}x${aa_extn_num}

    ${ph_number}=    I find phone number with required status  Available  country=USA (+1)

    I assign phone number to Auto Attendant  ${aa_name}
    ${aa_name}=  Set Variable    Test_AA${SPACE}AA${SPACE}x${aa_extn_num}
    And I find element on phone number page  ${ph_number}  Active  Auto Attendant  ${aa_name}  ${True}
#    When I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...         AND  sleep  3s
    ...         AND  I delete vcfe entry for ${aa_extn_num}
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
