*** Settings ***
Documentation     Login to BOSS portal and Edit Pickup Group - Cannot Delete Name
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
1 Login as staff user and Edit Pickup Group - Cannot Delete Name
    [Tags]    Regression    PK
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    Set to Dictionary    ${Pickupgroup_edit}  pickupgpname  Delete
    Set to Dictionary    ${Pickupgroup_edit}  error_message  This field is required
    Then I edit pickup group    &{Pickupgroup_edit}
    And I verify "${Pickupgroup_edit['error_message']}" is displayed on screen
    [Teardown]  run keywords  I click on cancel button
    ...                      I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    ...                      I log off
    ...                      I check for alert

2 Login as DM user and Edit Pickup Group - Cannot Delete Name
    [Tags]    Regression    PK    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    Set to Dictionary    ${Pickupgroup_edit}  pickupgpname  Delete
    Set to Dictionary    ${Pickupgroup_edit}  error_message  This field is required
    Then I edit pickup group    &{Pickupgroup_edit}
    And I verify "${Pickupgroup_edit['error_message']}" is displayed on screen
    [Teardown]  run keywords  I click on cancel button
    ...                      I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    ...                      I log off
    ...                      I check for alert


3 Login as PM user and Edit Pickup Group - Cannot Delete Name
    [Tags]    Regression    PK
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup_Add}    pickuploc    ${locationName}
    Set to Dictionary    ${Pickupgroup_Add}    extnlistname    ${extnlistname}
    ${extn_num}=    I create pickup group    &{Pickupgroup_Add}
    Set to Dictionary    ${Pickupgroup_Add}    PGExtn    ${extn_num}
    Then I select vcfe component by searching extension "${Pickupgroup_Add['PGExtn']}"
    Set to Dictionary    ${Pickupgroup_edit}  pickupgpname  Delete
    Set to Dictionary    ${Pickupgroup_edit}  error_message  This field is required
    Then I edit pickup group    &{Pickupgroup_edit}
    And I verify "${Pickupgroup_edit['error_message']}" is displayed on screen
    [Teardown]  run keywords  I click on cancel button
    ...                      I delete vcfe entry for ${Pickupgroup_Add['PGExtn']}
    ...                      I log off
    ...                      I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{Pickupgroup_Add}
    Set suite variable    &{Pickupgroup_edit}


    : FOR    ${key}    IN    @{Pickupgroup_Add.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_Add["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_Add}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{Pickupgroup_edit.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroup_edit["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroup_edit}    ${key}    ${updated_val}
