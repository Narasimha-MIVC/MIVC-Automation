*** Settings ***
Documentation     Keywords supported for Add-on Features
...               developer- Megha Bansal
...               Comments:

Library    Collections


*** Keywords ***

I click on manage button of "${myfeature:[^"]+}"
    [Documentation]   This keyword will click on manage button of add on feature page of the specified feature
    &{feature}=    Create Dictionary       feature=${myfeature}
	Run Keyword       click_on_manage_button      &{feature}

I add global user to mobility
    [Documentation]   This keyword will add mobility profile to a global user via Add on Features page
    [Arguments]     &{global_user}
    ${result}=  Run Keyword     add_globaluser_mobility     &{global_user}
    Should be true   ${result}

I provision scribe feature to user
    [Documentation]   This keyword will add connect to a global user via Add on Features page
    [Arguments]     &{global_user}
    ${result}=  Run Keyword     add_globaluser_mobility     &{global_user}
    Should be true   ${result}
    
I add hybrid scribe users
    [Arguments]  ${user_info}
    ${status}=  Run Keyword  add on feature manage connect scribe hybrid   ${user_info}
    should be true  ${status}

I activate and manage cloud hybrid fax
    [Arguments]  &{params}
    ${status}=  run keyword  add on feature activate and manage cloud hybrid fax  &{params}
    should be true  ${status}

I activate shoretel connect hybrid
    ${status}=  run keyword  add_on_feature_activate_shoretel_connect_hybrid
    should be true  ${status}

I activate Add-On features
    [Arguments]  &{params}
    ${status}=  run keyword  activate_add_on_feature  &{params}
    should be true  ${status}