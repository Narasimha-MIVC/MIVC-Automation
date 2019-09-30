*** Settings ***
Documentation    To add custom schedule with name already in use and validate the error message
...              Saurabh Singh

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String
*** Test Cases ***
Create custom schedule with DM account
    #When I check for alert
    [Tags]    CS    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule01}
    set to dictionary  ${CustomSchedule02}  customScheduleName      ${CustomSchedule01['customScheduleName']}
    Then I create custom schedule    &{CustomSchedule02}
    [Teardown]  run keywords  I delete VCFE entry by name ${CustomSchedule01['customScheduleName']}
    ...                       I log off
    ...                       I check for alert

Create custom schedule with PM account
    #When I check for alert
     [Tags]    Regression       CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule01}
    set to dictionary  ${CustomSchedule02}  customScheduleName      ${CustomSchedule01['customScheduleName']}
    Then I create custom schedule    &{CustomSchedule02}
    [Teardown]  run keywords  I delete VCFE entry by name ${CustomSchedule01['customScheduleName']}
    ...                       I log off
    ...                       I check for alert


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{CustomSchedule02}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}
