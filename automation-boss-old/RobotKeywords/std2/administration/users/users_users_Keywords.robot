*** Settings ***
Documentation    Suite description
Library    Collections

*** Keywords ***

I find single user info
    [Arguments]  ${user_info}
    ${status}=  run keyword  get single user info from user grid  ${user_info}
    should be true  ${status}
I create New STD2User
    [Arguments]  ${user_name}   ${enable_did}
    ${extn}   ${first_name}   ${last_name}     ${result}=  run keyword     add new std2user    ${user_name}   ${enable_did}
    should be true  ${result}
    [Return]   ${extn}   ${first_name}   ${last_name}

I verify STD2 USER
    [Arguments]  ${user_first_name}
    ${result}=  run keyword         verify std2 user  ${user_first_name}
    should be true  ${result}

I delete STD2 User
    [Arguments]  ${user_first_name}
    ${result}=  run keyword  delete std2 user  ${user_first_name}
    should be true  ${result}

I update STD2User
    [Arguments]     ${user_first_name}   ${updated_first_name}  ${last_name}  ${extension}  ${email_addr}   ${did_update}
     &{params}=   Create Dictionary  User_FirstName=${user_first_name}  UpdatedFirstName=${updated_first_name}  UpdatedLastName=${last_name}
    ...  Extension=${extension}  Email=${email_addr}    updateDid=${did_update}
    ${updated_name}   ${updated_extn}   ${updated_email}    ${result}=  run keyword  update std2 user  &{params}
    should be true  ${result}
    [Return]   ${updated_name}   ${updated_extn}    ${updated_email}

I Retrieve STD2 user DID
    [Arguments]  ${user_first_name}
    ${did}  ${result}=  run keyword         retrieve std2 user did  ${user_first_name}
    should be true  ${result}
    [Return]    ${did}