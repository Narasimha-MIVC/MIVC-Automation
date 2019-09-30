*** Settings ***
Documentation     Login to BOSS portal and Edit Emergency Hunt Group and add hunt group as a group member
...               dev-Immani Mahesh Kumar


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/Geolocationinfo.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot


#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String
*** Test Cases ***
Edit Emergency Hunt Group and add hunt group as a group member with DM User
    [Tags]    Regression    EHG    Generic
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
#    and I go to "Emergency_Hunt_Group" page
#    ${loc_status}=  I check for text "Auto_hg_loc" in dropdown "Emergency_hg_loc_dropdown"
#    run keyword if   '${loc_status}' == 'False'   run keyword  I switch to "geographic_locations" page
#    run keyword if   '${loc_status}' == 'False'   run keyword  I create geographic location    &{geolocation01}
#    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${EmergencyHuntGroup2}    Location    ${locationName}
    ${extn}    ${location}=    I create emergency hunt group   &{EmergencyHuntGroup2}
    And I select vcfe component by searching extension "${extn}"
    set to dictionary  ${EmergencyHG_Edit}     grp_member   ${extn_num}
    set to dictionary  ${EmergencyHG_Edit}  Distribution_pattern     Top_down
    Then I edit emergency hunt group    &{EmergencyHG_Edit}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I delete vcfe entry for ${extn}
    ...                       I log off
    ...                       I check for alert


Edit Emergency Hunt Group and add hunt group as a group member with PM User
    [Tags]    Regression    EHG
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
#    and I go to "Emergency_Hunt_Group" page
#    ${loc_status}=  I check for text "Auto_hg_loc" in dropdown "Emergency_hg_loc_dropdown"
#    run keyword if   '${loc_status}' == 'False'   run keyword  I switch to "geographic_locations" page
#    run keyword if   '${loc_status}' == 'False'   run keyword  I create geographic location    &{geolocation01}
#    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${EmergencyHuntGroup2}    Location    ${locationName}
    ${extn}    ${location}=    I create emergency hunt group   &{EmergencyHuntGroup2}
    log to console  ${extn}
    And I select vcfe component by searching extension "${extn}"
    set to dictionary  ${EmergencyHG_Edit}     grp_member   ${extn_num}
    set to dictionary  ${EmergencyHG_Edit}  Distribution_pattern     Top_down
    Then I edit emergency hunt group    &{EmergencyHG_Edit}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I delete vcfe entry for ${extn}
    ...                       I log off
    ...                       I check for alert

Edit Emergency Hunt Group and add hunt group as a group member with Staff User
    [Tags]    Regression    EHG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
#    and I go to "Emergency_Hunt_Group" page
#    ${loc_status}=  I check for text "Auto_hg_loc" in dropdown "Emergency_hg_loc_dropdown"
#    run keyword if   '${loc_status}' == 'False'   run keyword  I switch to "geographic_locations" page
#    run keyword if   '${loc_status}' == 'False'   run keyword  I create geographic location    &{geolocation01}
#    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${EmergencyHuntGroup2}    Location    ${locationName}
    ${extn}    ${location}=    I create emergency hunt group   &{EmergencyHuntGroup2}
    log to console  ${extn}
    And I select vcfe component by searching extension "${extn}"
    set to dictionary  ${EmergencyHG_Edit}     grp_member   ${extn_num}
    set to dictionary  ${EmergencyHG_Edit}  Distribution_pattern     Top_down
    Then I edit emergency hunt group    &{EmergencyHG_Edit}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...                       I delete vcfe entry for ${extn}
    ...                       I log off
    ...                       I check for alert





*** Keywords ***
Set Init Env
     ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
     ${uni_num}=    generate random string    5    [NUMBERS]

      Set suite variable    ${uni_str}

      Set suite variable    &{EmergencyHuntGroup2}


    : FOR    ${key}    IN    @{geolocation01.keys()}
    \    ${updated_val}=    Replace String    ${geolocation01["${key}"]}    {rand_str}    ${uni_num}
    \    Set To Dictionary    ${geolocation01}    ${key}    ${updated_val}

     : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}