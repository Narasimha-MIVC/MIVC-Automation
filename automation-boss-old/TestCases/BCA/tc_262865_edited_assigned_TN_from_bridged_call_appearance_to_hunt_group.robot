*** Settings ***
Documentation    Edited Assigned TN from Bridged Call Appearance to Hunt Group
#...               dev-Vasuja
#...               Comments:
Suite Teardown    Close The Browsers
#Suite Setup and Teardown
Suite Setup       Set Init Env

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py
Resource           ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
#Library           ../../lib/BossComponentBCA.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
1. Login as staff user and edit Assigned TN from Bridged Call Appearance to Hunt Group
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}

    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  ${None}  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  hunt_Group    ${HuntgroupStaff['HGname']} x${HuntgroupStaff['HGExtn']}
    set to dictionary  ${localbcainfo}  HGname    ${HuntgroupStaff['HGname']}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  Active  Hunt Group  &{localbcainfo}[HGname]  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  5s
    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

2. Login as DM user and edit Assigned TN from Bridged Call Appearance to Hunt Group
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    sleep  5s
    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}

    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  ${None}  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  hunt_Group    ${HuntgroupStaff['HGname']} x${HuntgroupStaff['HGExtn']}
    set to dictionary  ${localbcainfo}  HGname    ${HuntgroupStaff['HGname']}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  Active  Hunt Group  &{localbcainfo}[HGname]  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  5s
    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

3. Login as PM user and edit Assigned TN from Bridged Call Appearance to Hunt Group
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  5s
    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}

    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  ${None}  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  hunt_Group    ${HuntgroupStaff['HGname']} x${HuntgroupStaff['HGExtn']}
    set to dictionary  ${localbcainfo}  HGname    ${HuntgroupStaff['HGname']}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  &{localbcainfo}[SelectPhoneNumber]  Active  Hunt Group  &{localbcainfo}[HGname]  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  ${localbcainfo}
    sleep  5s
    [Teardown]  Run Keywords  I log off
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
    Set suite variable    ${uni_num}

    Set suite variable    &{HuntgroupStaff}

    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}
