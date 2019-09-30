*** Settings ***
Documentation    Keyword supported for the navigation of BOSS pages

Library     Collections

*** Keywords ***

# Generic Navigation via menus
I move to ${page} page
    ${result}=  Run Keyword   navigate_to_page  ${page}
    Should be True    ${result}