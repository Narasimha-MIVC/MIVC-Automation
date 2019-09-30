*** Settings ***
Documentation    Suite description

*** Keywords ***
I verify hybrid services activation status and number of active users
    [Arguments]  &{hybrid_service_info}
    ${status}=  run keyword  verify hybrid services activation status and active_users  ${hybrid_service_info}
    should be true  ${status}