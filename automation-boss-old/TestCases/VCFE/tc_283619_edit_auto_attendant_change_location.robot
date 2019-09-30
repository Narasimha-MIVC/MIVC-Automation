*** Settings ***
Documentation  Login To Boss Portal And Edit An Auto Attendant And change Location
...            Mahesh
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files

Resource          ../../Variables/AutoAttendantInfo.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource          ../../Variables/Geolocationinfo.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py


*** Test Cases ***
01 Edit Auto Attendant and change location as a DM user
    [Tags]    AA    Regression    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
#    When I switch to "geographic_locations" page
#    And I create geographic location  &{geolocation01}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA_04}    Location    ${locationName}
    And I edit Auto-Attendant  &{EditAA_04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
     ...                      I log off
     ...                      I check for alert

02 Edit Auto Attendant and change location as a PM user
    [Tags]    AA    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA_04}    Location    ${locationName}
    And I edit Auto-Attendant  &{EditAA_04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
     ...                      I log off
     ...                      I check for alert



*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{geolocation01}

    : FOR    ${key}    IN    @{geolocation01.keys()}
    \    ${updated_val}=    Replace String    ${geolocation01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${geolocation01}    ${key}    ${updated_val}


#    : FOR    ${key}    IN    @{EditAA01.keys()}
#    \    ${updated_val}=    Replace String    ${EditAA01["${key}"]}    {rand_str}    ${uni_str}
#    \    Set To Dictionary    ${EditAA01}    ${key}    ${updated_val}
