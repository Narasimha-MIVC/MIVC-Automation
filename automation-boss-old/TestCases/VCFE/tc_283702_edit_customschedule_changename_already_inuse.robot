*** Settings ***
Documentation    To edit custom schedule with changing name already in use
...                 Palla Surya Kumar

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library     String

*** Test Cases ***
Edit Custom Schedule Change Name Already in USe as DM:
    [Tags]    Regression    CS    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule01}
    I create custom schedule    &{CustomSchedule03}
    Set to Dictionary    ${CustomSchedule01}    editName    ${CustomSchedule03["customScheduleName"]}
    and I edit custom schedule    &{CustomSchedule01}
    [Teardown]  run keywords  I delete vcfe entry by name ${CustomSchedule01["customScheduleName"]}
    ...                      I delete vcfe entry by name ${CustomSchedule03["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert

Edit Custom Schedule Change Name Already in USe as PM:
    [Tags]    Regression     CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule02}
    I create custom schedule    &{CustomSchedule05}
    Set to Dictionary    ${CustomSchedule02}    editName    ${CustomSchedule05["customScheduleName"]}
    and I edit custom schedule    &{CustomSchedule02}
    [Teardown]  run keywords  I delete vcfe entry by name ${CustomSchedule02["customScheduleName"]}
    ...                      I delete vcfe entry by name ${CustomSchedule05["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{CustomSchedule02}
    Set suite variable    &{CustomSchedule03}
    Set suite variable    &{CustomSchedule05}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule02}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule03.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule03}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule05.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule05["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule05}    ${key}    ${updated_val}
