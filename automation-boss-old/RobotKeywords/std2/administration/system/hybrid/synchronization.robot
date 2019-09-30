*** Settings ***
Documentation    Key words for the administration -> system -> hybrid -> synchronization page

*** Keywords ***

I synchronize account id and account token in STD2
    [Arguments]  &{params}
    ${status}=  run keyword  synchronize_ac_id_and_token  &{params}
    should be true  ${status}
    
I sync now data between STD2 and Boss
    ${status}=  run keyword     sync_data_between_STD2_Boss
    should be true  ${status}    