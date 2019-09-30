*** Settings ***
Documentation    To add VCFE Pickup Group
...              Immani Mahesh Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String
*** Test Cases ***
01 Create On Hours schedule with DM User
    [Tags]    Regression    AUS    UK    Generic
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
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify On Hours schedule "${OHS_name}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${OnHoursSchedule01['scheduleName']}
     ...                      I log off
     ...                      I check for alert


02 Create On Hours schedule with PM User
    [Tags]    Regression    AUS    UK
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
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify On Hours schedule "${OHS_name}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${OnHoursSchedule02['scheduleName']}
     ...                      I log off
     ...                      I check for alert


03 Create On Hours schedule with Staff User
    [Tags]    Regression    AUS    UK
    Given I login to ${url} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    sleep  3
    &{params}=  create dictionary
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    When I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule03}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify On Hours schedule "${OHS_name}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I delete vcfe entry by name ${OnHoursSchedule03['scheduleName']}
     ...                      I log off
     ...                      I check for alert



*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{OnHoursSchedule01}

    : FOR    ${key}    IN    @{OnHoursSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule01}    ${key}    ${updated_val}

    Set suite variable    &{OnHoursSchedule02}

    : FOR    ${key}    IN    @{OnHoursSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule02}    ${key}    ${updated_val}

    Set suite variable    &{OnHoursSchedule03}

    : FOR    ${key}    IN    @{OnHoursSchedule03.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule03}    ${key}    ${updated_val}