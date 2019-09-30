*** Settings ***
Documentation     Login to BOSS portal and validate TN is assigned to Auto Attendant after Save
...               dev-Vasuja
...               Comments:

#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../../Variables/EnvVariables.robot
Variables          ../BCA/Variables/BCA_Variables.py
Resource           ../VCFE/Variables/Vcfe_variables.robot
Resource          ../../Variables/AutoAttendantInfo.robot


Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Login to the boss portal as DM user and validate TN is assigned to Auto Attendant after Save
    [Tags]    Sanity_Phase2    Regression    Generic

    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    ### Actions:
    #1. Switch to VCFE page and create Auto-Attendant
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    #2. Switch to the phone system -> phone numbers page and assign an available phone number to Auto Attendant
    And I switch to "phone_systems_phone_numbers" page
    ${phone_no}=    I find phone number with required status  Available  country=USA (+1)
    set to dictionary  ${AA_01}  auto_Attendant    ${AA_01['Aa_Name']} x${AA_01['AA_Extension']}
    Then I assign phone number to vcfe component  &{AA_01}
    sleep  2s
    [Teardown]
    Run Keywords  I log off
    ...           I check for alert