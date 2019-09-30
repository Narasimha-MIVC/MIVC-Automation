*** Settings ***
Documentation    Edit  Bridged Call Appearance to another  Bridged Call Appearance profile
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
1. Login as staff user and edit Bridged Call Appearance to another Bridged Call Appearance profile
    [Tags]    Regression  FAILED

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
    &{localbcainfo_old}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo_old}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo_old}
    And I verify BCA  &{localbcainfo_old}

    ${bca_name2}=  generate_bca_name2
    log  ${bca_name2}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name2}
#    set to dictionary  ${localbcainfo}  AssignFromLocation  Don't assign a number

    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}


    Set to Dictionary    ${localbcainfo}    BCAExtn    ${localbcainfo['Extension']}

    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  bridged_Call_Appearance_name    ${localbcainfo['ProfileName']} x${localbcainfo['BCAExtn']}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${localbcainfo_old['SelectPhoneNumber']}  Active  Bridged Call Appearance  ${bca_name2}  ${True}
#    And I switch to "bridged_call_appearances" page
#    And I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo_old}
    ...         AND  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  I log off
    ...         AND  I check for alert

2. Login as DM user and edit Bridged Call Appearance to another Bridged Call Appearance profile
    [Tags]    Regression   FAILED

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
    &{localbcainfo_old}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo_old}  ProfileName  ${bca_name}
    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo_old}
    And I verify BCA  &{localbcainfo_old}

    ${bca_name2}=  generate_bca_name2
    log  ${bca_name2}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name2}
#    set to dictionary  ${localbcainfo}  AssignFromLocation  Don't assign a number

    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}


    Set to Dictionary    ${localbcainfo}    BCAExtn    ${localbcainfo['Extension']}

    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  bridged_Call_Appearance_name    ${localbcainfo['ProfileName']} x${localbcainfo['BCAExtn']}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${localbcainfo_old['SelectPhoneNumber']}  Active  Bridged Call Appearance  ${bca_name2}  ${True}
#    And I switch to "bridged_call_appearances" page
#    And I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo_old}
    ...         AND  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  I log off
    ...         AND  I check for alert

3. Login as PM user and edit Bridged Call Appearance to another Bridged Call Appearance profile
    [Tags]    Regression   FAILED

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
    &{localbcainfo_old}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo_old}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo_old}
    And I verify BCA  &{localbcainfo_old}

    ${bca_name2}=  generate_bca_name2
    log  ${bca_name2}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name2}
#    set to dictionary  ${localbcainfo}  AssignFromLocation  Don't assign a number

    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}


    Set to Dictionary    ${localbcainfo}    BCAExtn    ${localbcainfo['Extension']}

    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  bridged_Call_Appearance_name    ${localbcainfo['ProfileName']} x${localbcainfo['BCAExtn']}
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${localbcainfo_old['SelectPhoneNumber']}  Active  Bridged Call Appearance  ${bca_name2}  ${True}
#    And I switch to "bridged_call_appearances" page
#    And I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo_old}
    ...         AND  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}

generate_bca_name2
    [Documentation]  The keyword generates random bca name
    ${name2}=  Generate Random String  8  [LOWER]
    [Return]  ${name2}

Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HuntgroupStaff}

    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}
