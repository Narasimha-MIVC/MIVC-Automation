*** Settings ***
Documentation     Keywords supported for VCFE features in BOSS portal
...               dev- Vasuja K, Immani Mahesh Kumar
...               Comments:

Library    Collections

*** Keywords ***
I add Auto-Attendant
    [Arguments]    &{AA_Info}
    ${extn}=    Run Keyword    add Auto attendant   &{AA_Info}
    [Return]      ${extn}

I add Auto-Attendant with blank extension
    [Arguments]    &{AA_Info}
    ${result}=   Run Keyword    add Auto attendant   &{AA_Info}
    should be true  ${result}

I add Paging Group
    [Arguments]    &{Pg_Info}
    ${extn}=    Run Keyword    add Paging Group   &{Pg_Info}
    [Return]      ${extn}

I create emergency hunt group
    [Arguments]    &{hginfo}
    ${extn_number}    ${location}=    Run Keyword       create emergency hunt group    &{hginfo}
    [Return]      ${extn_number}    ${location}

I Verify the emergency hunt group gets created
    Run Keyword       verify emergency hunt group

I create extension list
    [Arguments]    &{ExtensionListInfo}
    Run Keyword    create extension list    &{ExtensionListInfo}

I create hunt group
    [Arguments]    &{Hunt_Group_Info}
    ${extn_number}=    Run Keyword    create hunt group    &{Hunt_Group_Info}
    [Return]      ${extn_number}

I verify Hunt Group with extension "${hgextn:[^"]+}"
    &{hggroup}=    Create Dictionary    hg_extn=${hgextn}
    Run Keyword    verify hunt group    &{hggroup}

I select vcfe component by searching extension "${vcfecomp:[^"]+}"
    &{vcfe_comp_info}=    Create Dictionary    vcfe_comp=${vcfecomp}
    ${result}=   Run Keyword    select vcfe component by extension    &{vcfe_comp_info}
    Should be true    ${result}

I select vcfe component by searching name "${vcfecomp:[^"]+}"
    &{vcfe_comp_info}=    Create Dictionary    vcfe_comp=${vcfecomp}
    ${result}=   Run Keyword    select vcfe component by name   &{vcfe_comp_info}
    Should be true    ${result}

I edit hunt group
    [Arguments]    &{Vcfe_variables}
    Run Keyword    edit hunt group    &{Vcfe_variables}

I verify updated hunt group value
    [Arguments]    &{Vcfe_variables}
    ${result}=  Run Keyword    verify_updated_hunt_group_value    &{Vcfe_variables}
    Should be true    ${result}

I create pickup group
    [Arguments]    &{PickupGroupInfo}
    ${extn_number}=    Run Keyword    create pickup group    &{PickupGroupInfo}
    [Return]      ${extn_number}
 
I create custom schedule
    [Arguments]    &{CustomScheduleInfo}
    ${result}=   Run Keyword    create custom schedule    &{CustomScheduleInfo}
    should be true  ${result}

I verify the group for ${ext}
    ${result}=  run keyword  verify_pickup_group   ${ext}
    should be true   ${result}

I edit pickup group
    [Arguments]  &{Pickupgroupedit}
    ${result}=  run keyword  edit_pickup_group   &{Pickupgroupedit}
    should be true   ${result}

I edit paging group
    [Arguments]  &{Pickupgroupedit}
    ${result}=  run keyword  edit_paging_group   &{Pickupgroupedit}
    should be true   ${result}

I create pickup group with no location
    [Arguments]  &{Pickupgroupwithoutlocation}
    ${result}=  run keyword  create_pickup_group   &{Pickupgroupwithoutlocation}
    should not be true   ${result}

I delete vcfe entry for ${ext}
    ${result}=      run keyword  delete_vcfe_entry   ${ext}
    should be true  ${result}

I check for invalid extention
    [Arguments]  &{dict}
    ${result}=      run keyword  vcfe_invalid_extention   &{dict}
    should not be true  ${result}

I check for extetion list from paging group
    [Arguments]  &{dict}
    ${result}=      run keyword  vcfe_jump_extention_list   &{dict}
    should be true  ${result}

I edit custom schedule
    [Arguments]  &{dict}
    ${result}=      run keyword  edit_custome_schedule   &{dict}
    should be true  ${result}

I delete custom schedule name
    [Arguments]  &{dict}
    ${result}=      run keyword  delete_vcfe_day_name   &{dict}
    should not be true  ${result}

I edit extension list
    [Arguments]  &{dict}
    ${result}=      run keyword   edit_extension_list  &{dict}
    should be true  ${result}

I edit Auto-Attendant
    [Arguments]  &{dict}
    ${result}=      run keyword  edit_auto_attendant   &{dict}
    should be true  ${result}

I delete vcfe entry by name ${vcfe_name}
    ${result}=      run keyword  delete_vcfe_by_name  ${vcfe_name}
    should be true  ${result}

I create on-hours schedule
    [Arguments]   &{Vcfe_variables}
    ${OHS_name}=  run keyword  create on hours schedule     &{Vcfe_variables}
    log  "${OHS_name}"
    [Return]  ${OHS_name}

In D2 I verify On Hours schedule "${d2onhoursschedule:[^"]+}" is set for ${newacc}
    &{d2onhoursschedule}=    Create Dictionary    exp_on_hours_schedule=${d2onhoursschedule}   newacc=${newacc}
    ${result}=   Run Keyword    director verify on hours schedule    &{d2onhoursschedule}
    Should be true    ${result}

I create holiday schedule
    [Arguments]   &{Vcfe_variables}
    ${holi_name}  ${holi_date} =    Run Keyword    create holiday schedule    &{Vcfe_variables}
    Log  "${holi_name} ${holi_date}"
    [Return]   ${holi_name}  ${holi_date}

I edit holiday schedule
    [Arguments]   &{Vcfe_variables}
    ${result}=    Run Keyword    edit_holiday_schedule    &{Vcfe_variables}
    Should be true    ${result}

I verify holidays schedule
    [Arguments]    &{Vcfe_variables}
    ${result}=    Run Keyword    verify holidays schedule    &{Vcfe_variables}
    Should be true    ${result}

In D2 I verify holiday schedule "${d2holidayschedule:[^"]+}" with date "${hsdate:[^"]+}" and "${hstimezone:[^"]+}" is set for ${newacc}
    &{d2holidayschedule}=    Create Dictionary    exp_holidayschedule=${d2holidayschedule}   exp_date=${hsdate}    exp_timezone=${hstimezone}    newacc=${newacc}
    ${result}=   Run Keyword    director verify holiday schedule    &{d2holidayschedule}
    Should be true    ${result}

In D2 I verify emergency hunt group "${d2huntgroup:[^"]+}" is set for ${newacc}
    &{D2huntgroup}=    Create Dictionary    exp_huntgroup=${d2huntgroup}    newacc=${newacc}
    ${result}=   Run Keyword    Director Verify emergency hunt group    &{D2huntgroup}
    Should be true    ${result}

In D2 I verify emergency hunt group "${d2huntgroup:[^"]+}" is deleted for ${newacc}
    &{D2huntgroup}=    Create Dictionary    exp_huntgroup=${d2huntgroup}    newacc=${newacc}
    ${result}=   Run Keyword    Director Verify emergency hunt group    &{D2huntgroup}
    Should not be true    ${result}

In D2 I verify hunt group "${d2huntgroup:[^"]+}" with extension "${d2hgextn:[^"]+}" is set for ${newacc}
    &{D2huntgroup}=    Create Dictionary    exp_huntgroup=${d2huntgroup}    hg_extn=${d2hgextn}    newacc=${newacc}
    ${result}=   Run Keyword    Director Verify hunt group    &{D2huntgroup}
    Should be true    ${result}

In D2 I verify hunt group "${d2huntgroup:[^"]+}" with extension "${d2hgextn:[^"]+}" is deleted for ${newacc}
    &{D2huntgroup}=    Create Dictionary    exp_huntgroup=${d2huntgroup}    newacc=${newacc}
    ${result}=   Run Keyword    Director Verify hunt group    &{D2huntgroup}
    Should not be true    ${result}

In D2 I verify pickup group "${d2pickupgroup:[^"]+}" with extension "${d2pkextn:[^"]+}" is set for ${newacc}
    &{d2pickupgroup}=    Create Dictionary    exp_pickupgroup=${d2pickupgroup}   pk_extn=${d2pkextn}   newacc=${newacc}
    ${result}=   Run Keyword    Director Verify pickup group    &{d2pickupgroup}
    Should be true    ${result}

In D2 I verify AA "${d2autoattendant:[^"]+}" with extension "${d2aaextn:[^"]+}" is set for ${newacc}
    &{D2autoattendant}=    Create Dictionary    Aa_Name=${d2autoattendant}      Aa_Extension=${d2aaextn}    newacc=${newacc}
    ${result}=   Director Verify Auto Attendant   &{D2autoattendant}
    Should be true    ${result}

I edit on-hours schedule
    [Arguments]  &{dict}
    ${result}=      run keyword  edit_on_hours_schedule   &{dict}
    should be true  ${result}

I edit emergency hunt group
   [Arguments]    &{Vcfe_variables}
   Run Keyword    edit_emergency_hunt_group    &{Vcfe_variables}

I verify emergency hunt group
    [Arguments]    &{Vcfe_variables}
    ${result}=  Run Keyword    verify_emergency_hunt_group    &{Vcfe_variables}
    Should be true    ${result}

I verify pickup group
    [Arguments]    &{Vcfe_variables}
    ${result}=  Run Keyword    verify_edited_pickup_group    &{Vcfe_variables}
    Should be true    ${result}

In D2 I verify PG "${d2pagegroup:[^"]+}" with extension "${d2pgextn:[^"]+}" is set for ${newacc}
    &{D2pagegroup}=    Create Dictionary    Pg_Name=${d2pagegroup}      Pg_Extension=${d2pgextn}    newacc=${newacc}
    ${result}=   Director Verify Paging Group   &{D2pagegroup}
    Should be true    ${result}

In D2 I verify custom schedule "${d2customschedule:[^"]+}" is set for ${newacc}
    &{d2customschedule}=    Create Dictionary    exp_customschedule=${d2customschedule}   newacc=${newacc}
    ${result}=   Run Keyword    director verify custom schedule    &{d2customschedule}
    Should be true    ${result}

I delete VCFE entry with name "${name:[^"]+}" and extn "${extn:[^"]+}"
    &{VCFE_entry}=     Create Dictionary    VCFE_Name=${name}     VCFE_Extn=${extn}
    Run Keyword    Delete vcfe components    &{VCFE_entry}

I verify if VCFE entries with name "${name:[^"]+}" and extn "${extn:[^"]+}" are deleted
    &{VCFE_entry}=     Create Dictionary    VCFE_Name=${name}     VCFE_Extn=${extn}
    ${result} =     Run Keyword    Verify Vcfe Components Delete    &{VCFE_entry}
    Should be true    ${result}

In D2 I verify extension list "${D2extensionList:[^"]+}" is set for ${newacc}
    &{D2extensionList}=    Create Dictionary    exp_D2extensionList=${D2extensionList}    newacc=${newacc}
    ${result}=    director verify Extension List    &{D2extensionList}
    Should be true    ${result}

In D2 I verify hunt group member "${d2hgmember:[^"]+}" for "${d2hgextn:[^"]+}" is set for ${newacc}
    &{D2huntgroupMember}=    Create Dictionary    hgmember=${d2hgmember}    hg_extn=${d2hgextn}    newacc=${newacc}
    ${result}=   Run Keyword    director verify hunt group member    &{D2huntgroupMember}
    Should be true    ${result}

I check for text "${text}" in dropdown "${dropdown}"
    &{dropdown_info}=    Create Dictionary       text=${text}    dropdown_xpath=${dropdown}
    ${result}=  Run Keyword    verify text in dropdown    &{dropdown_info}
    [return]  ${result}

I go to "${vcfe_page}" page
    &{vcfe_page_info}=     create dictionary  page_name=${vcfe_page}
    Run Keyword    go to vcfe page    ${vcfe_page}

I assign phone number to vcfe component
    [Arguments]  &{info}
    ${result}=  run keyword  assign ph number to vcfe component  &{info}
    should be true  ${result}

I validate VCFE component fields
    [Arguments]    &{VCFEFields}
    ${result}=    Run Keyword    validate vcfe component fields    &{VCFEFields}
    should be true   ${result}

I search VCFE component by searching extension "${vcfecomp:[^"]+}"
    &{vcfe_comp_info}=    Create Dictionary    vcfe_comp=${vcfecomp}
    ${result}=    Run Keyword    search vcfe component by extension   &{vcfe_comp_info}
    should be true   ${result}

I search VCFE component by searching name
    [Arguments]    &{AA_01}
    ${result}=    Run Keyword    search vcfe component by name   &{AA_01}
    should be true   ${result}

I search VCFE component by searching type
    [Arguments]    &{AA_01}
    ${result}=    Run Keyword    search vcfe component by type   &{AA_01}
    should be true   ${result}

I add Auto-Attendant with blank multiple digit timeout value
    [Arguments]    &{AA_Info}
    ${result}=   Run Keyword    add Auto attendant   &{AA_Info}
    should be true  ${result}

I verify Allignment in VCFE with ${field_Info}
    ${result}=    Run Keyword    verify allignment    ${field_Info}
    should be true   ${result}

I verify sort order by "${vcfecomp:[^"]+}" on vcfe grid
    &{vcfe_comp_info}=    Create Dictionary    header_name=${vcfecomp}
    ${result}=  run keyword  verify component sort order on vcfe grid    &{vcfe_comp_info}
    should be true  ${result}

I copy custom schedule
    [Arguments]  &{dict}
    ${result}=      run keyword  edit_custome_schedule   &{dict}
    should be true  ${result}

I copy holiday schedule
    [Arguments]   &{dict}
    ${result}=    Run Keyword    edit_holiday_schedule    &{dict}
    Should be true    ${result}

I copy on-hours schedule
    [Arguments]  &{dict}
    ${result}=      run keyword  edit_on_hours_schedule   &{dict}
    should be true  ${result}

I verify global user loc not in VCFE page
    [Arguments]  &{global_user_loc}
    ${result}=  run keyword    validate vcfe component fields    &{global_user_loc}
    SHOULD BE TRUE  ${result}


Extension vcfe default AA
    [Arguments]    ${vcfe_name}
    ${result}=      run keyword   vcfe_default_AA  ${vcfe_name}
    [Return]    ${result}
