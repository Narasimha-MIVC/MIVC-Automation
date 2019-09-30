*** Settings ***
Documentation    To edit custom schedule by changing with start and end time
...                 Palla Surya Kumar

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Suite Setup       Set Init Env
#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library     String
*** Test Cases ***
Edit Custom Schedule by changing with start and end time as DM:
    [Tags]    Regression    CS    Generic
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule01}
    Set to Dictionary    ${EditCustomSchedule01}    editName    ${CustomSchedule01["customScheduleName"]}
    and I edit custom schedule    &{EditCustomSchedule01}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify custom schedule "${EditCustomSchedule01["customScheduleName"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${EditCustomSchedule01["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert
Edit Custom Schedule by changing with start and end time as PM:
    [Tags]    Regression        CS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    Then I log off
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule02}
    Set to Dictionary    ${EditCustomSchedule02}    editName    ${CustomSchedule02["customScheduleName"]}
    and I edit custom schedule    &{EditCustomSchedule02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify custom schedule "${EditCustomSchedule02["customScheduleName"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${EditCustomSchedule02["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert
*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{EditCustomSchedule01}
    Set suite variable    &{CustomSchedule02}
    Set suite variable    &{EditCustomSchedule02}

    : FOR    ${key}    IN    @{EditCustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{EditCustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule02}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule02}    ${key}    ${updated_val}
