*** Settings ***
Documentation     Login to BOSS portal and Edit Emergency Hunt Group - Change No Answer Destination
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

1 Login as DM and Edit Emergency Hunt Group - Change No Answer Destination
    [Tags]    Regression    EHG    Generic
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
#    And I switch to "geographic_locations" page
#    And I create geographic location    &{geolocationDetails}
    Set to Dictionary    ${EmergencyHG_Edit}    no_answer    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${geolocationDetails}    Location    ${locationName}
    ${extn_num}    ${location}=    Then I create emergency hunt group  &{geolocationDetails}
    Set to Dictionary    ${EmergencyHG}    EHGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${EmergencyHG['EHGExtn']}"
    And I edit emergency hunt group  &{EmergencyHG_Edit}
    Then I select vcfe component by searching extension "${EmergencyHG['EHGExtn']}"
    Set to Dictionary    ${EmergencyHG_Edit}    user_name    ${request_by}
    And I verify emergency hunt group  &{EmergencyHG_Edit}
   [Teardown]  run keywords   I delete vcfe entry for ${EmergencyHG['EHGExtn']}
   ...                        I log off
   ...                       I check for alert

2 Login as PM and Edit Emergency Hunt Group - Change No Answer Destination
    [Tags]    Regression    EHG
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${geolocationDetails}    Location    ${locationName}
    ${extn_num}    ${location}=    Then I create emergency hunt group  &{geolocationDetails}
    Set to Dictionary    ${EmergencyHG}    EHGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${EmergencyHG['EHGExtn']}"
    And I edit emergency hunt group  &{EmergencyHG_Edit}
    Then I select vcfe component by searching extension "${EmergencyHG['EHGExtn']}"
    And I verify emergency hunt group  &{EmergencyHG_Edit}
    [Teardown]  run keywords   I delete vcfe entry for ${EmergencyHG['EHGExtn']}
   ...                        I log off
   ...                       I check for alert

3 Login as Staff user and Edit Emergency Hunt Group - Change No Answer Destination
    [Tags]    Regression    EHG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${geolocationDetails}    Location    ${locationName}
    ${extn_num}    ${location}=    Then I create emergency hunt group  &{geolocationDetails}
    Set to Dictionary    ${EmergencyHG}    EHGExtn    ${extn_num}
    And I switch to "Visual_Call_Flow_Editor" page
    Then I select vcfe component by searching extension "${EmergencyHG['EHGExtn']}"
    And I edit emergency hunt group  &{EmergencyHG_Edit}
    Then I select vcfe component by searching extension "${EmergencyHG['EHGExtn']}"
    And I verify emergency hunt group  &{EmergencyHG_Edit}
#    Then I delete vcfe entry for ${EmergencyHG['EHGExtn']}
#    then I switch to "order" page
#    and I close open order for location ${geolocationDetails["Location"]}
#    then I switch to "geographic_locations" page
#    and I close the location ${geolocationDetails["Location"]} requested by "${request_by}"
   [Teardown]  run keywords   I delete vcfe entry for ${EmergencyHG['EHGExtn']}
   ...                        I log off
   ...                       I check for alert



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${geolocationDetails}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    ${geolocationDetails}


    Run keyword if    '${country}' == 'Australia'
        ...    Run Keyword
        ...    set to dictionary  ${geolocationDetails}   &{geolocation_AUS}

        ...    ELSE IF    '${country}' == 'UK'
        ...    Run Keyword
        ...    set to dictionary  ${geolocationDetails}  &{geolocation_UK}

        ...    ELSE IF    '${country}' == 'US'
        ...    Run Keyword
        ...    set to dictionary  ${geolocationDetails}   &{geolocation_US}

        ...    ELSE
        ...    log  Please enter a valid Country name like US, UK or Australia


    : FOR    ${key}    IN    @{geolocationDetails.keys()}
    \    ${updated_val}=    Replace String    ${geolocationDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${geolocationDetails}    ${key}    ${updated_val}
