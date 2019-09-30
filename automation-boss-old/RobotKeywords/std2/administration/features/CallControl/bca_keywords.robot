*** Settings ***

Documentation   Suite description

*** Keywords ***
I create New STD2 BCA User
    [Arguments]  ${bca_user_name}   ${backup_phone_number}  ${enable_did}   ${std2_user_did}
    &{params}=  Create Dictionary  user_name=${bca_user_name}  ph_num=${backup_phone_number}    enable_did=${enable_did}    user_did=${std2_user_did}
    ${extn}  ${bca_user_name}     ${result} =  run keyword     add std2 bca user    &{params}
    should be true  ${result}
    [Return]        ${extn}     ${bca_user_name}

I verify STD2 BCA USER
    [Arguments]  ${user_name}
    ${result}=  run keyword  verify std2 bca user  ${user_name}
    should be true  ${result}

I delete STD2 BCA User
    [Arguments]  ${user_name}
    ${result}=  run keyword  delete std2 bca user  ${user_name}
    should be true  ${result}


I update STD2 BCA User
    [Arguments]     ${user_name}   ${updated_name}   ${extension}   ${did_update}   ${did_value}
    &{params}=   Create Dictionary  User_Name=${user_name}  UpdatedName=${updated_name}  Extension=${extension}    updateDid=${did_update}    didVal=${did_value}
    ${updated_bca_name}   ${result}=  run keyword  update std2 bca user  &{params}
    should be true  ${result}
    [Return]   ${updated_bca_name}
