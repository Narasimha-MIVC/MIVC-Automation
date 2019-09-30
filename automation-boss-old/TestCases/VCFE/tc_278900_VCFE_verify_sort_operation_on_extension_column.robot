*** Settings ***
Documentation     Login to BOSS portal and VCFE-Verify Sort operation on Extension column
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
Library			  ../../lib/BossComponent.py    browser=${BROWSER}    country=${country}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***

1 Login as staff and VCFE-Verify Sort operation on Extension column
    [Tags]    Regression
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Then I verify sort order by "ExtensionData" on vcfe grid
    [Teardown]  run keywords   I log off
   ...                       I check for alert

2 Login as DM and VCFE-Verify Sort operation on Extension column
    [Tags]    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I verify sort order by "ExtensionData" on vcfe grid
    [Teardown]  run keywords   I log off
   ...                       I check for alert

3 Login as PM and VCFE-Verify Sort operation on Extension column
    [Tags]    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I verify sort order by "ExtensionData" on vcfe grid
    [Teardown]  run keywords   I log off
   ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${geolocationDetails}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

