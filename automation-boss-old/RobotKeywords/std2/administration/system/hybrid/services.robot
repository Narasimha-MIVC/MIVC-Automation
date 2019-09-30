*** Settings ***
Documentation    Key words for the administration -> system -> hybrid -> services page

*** Keywords ***

I verify the status of the hybrid services
    [Arguments]  &{hybrid_services}
    ${status}=  run keyword  verify hybrid services status  ${hybrid_services}
    should be true  ${status}