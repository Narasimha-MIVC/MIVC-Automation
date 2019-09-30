*** Settings ***
Documentation     Login to BOSS portal and Edit Pickup Group - Change Name
#...               dev-Vasuja
#...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot


#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String
*** Test Cases ***

1 Login as staff user and Edit Pickup Group - Change Name
    [Tags]    Regression    PK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    Set to Dictionary  ${Pickupgroup_edit}  pickupgpname  ${Pickupgroup2_Add["pickupgpname"]}
    Set to Dictionary  ${Pickupgroup_edit}  error_message  Failed updating component. Error: pickupgpname - has already been taken
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    Then I edit pickup group    &{Pickupgroup_edit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    and I verify pickup group    &{Pickupgroup_edit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_edit['pickupgpname']}" with extension "${Pickupgroup_Add['PGExtn']}" is set for ${params['partition_id']}
    Then I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

2 Login as DM and Edit Pickup Group - Change Name
    [Tags]    Regression    PK    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    Set to Dictionary  ${Pickupgroup_edit}  pickupgpname  ${Pickupgroup2_Add["pickupgpname"]}
    Set to Dictionary  ${Pickupgroup_edit}  error_message  Failed updating component. Error: pickupgpname - has already been taken
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    Then I edit pickup group    &{Pickupgroup_edit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    and I verify pickup group    &{Pickupgroup_edit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_edit['pickupgpname']}" with extension "${Pickupgroup_Add['PGExtn']}" is set for ${params['partition_id']}
    Then I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert


3 Login as PM and Edit Pickup Group - Change Name
    [Tags]    Regression    PK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    Set to Dictionary  ${Pickupgroup_edit}  pickupgpname  ${Pickupgroup2_Add["pickupgpname"]}
    Set to Dictionary  ${Pickupgroup_edit}  error_message  Failed creating component. Error: pickupgpname - has already been taken
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    Then I edit pickup group    &{Pickupgroup_edit}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    and I verify pickup group    &{Pickupgroup_edit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup_edit['pickupgpname']}" with extension "${Pickupgroup_Add['PGExtn']}" is set for ${params['partition_id']}
    Then I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    [Teardown]  run keywords  I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{Pickupgroup_Add}
    Set suite variable    &{Pickupgroup2_Add}


    : FOR    ${key}    IN    @{Pickupgroup_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_Add}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{Pickupgroup2_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup2_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup2_Add}    ${key}    ${updated_val}

