*** Settings ***
Documentation    To edit custom schedule to check day times cannot overlap
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
Edit Custom Schedule to check day times cannot overlap as DM:
    [Tags]    Regression    CS    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule01}
    Set to Dictionary    ${EditCustomSchedule05}    editName    ${CustomSchedule01["customScheduleName"]}
    and I edit custom schedule    &{EditCustomSchedule05}
    [Teardown]  run keywords  I delete vcfe entry by name ${CustomSchedule01["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert

Edit Custom Schedule to check day times cannot overlap as PM:
    [Tags]    Regression    CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule02}
    Set to Dictionary    ${EditCustomSchedule06}    editName    ${CustomSchedule02["customScheduleName"]}
    and I edit custom schedule    &{EditCustomSchedule06}
    [Teardown]  run keywords  I delete vcfe entry by name ${CustomSchedule02["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{EditCustomSchedule05}
    Set suite variable    &{CustomSchedule02}
    Set suite variable    &{EditCustomSchedule06}

    : FOR    ${key}    IN    @{EditCustomSchedule05.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule05["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule05}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{EditCustomSchedule06.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule06["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule06}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule02}    ${key}    ${updated_val}
