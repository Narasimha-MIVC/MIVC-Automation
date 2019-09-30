*** Settings ***
Documentation    As a PM user verify already assaigned profile should not list in abca profile drop down
...               dev-Vasuja
Suite Teardown    Close The Browsers
#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component
Library           ../../lib/BossComponent.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
As a PM user verify already assaigned profile should not list in abca profile drop down
    [Tags]    Regression  BCA    test

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  5s

    # call the clean up function
    clean up
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}

    ### Actions:
    #1. Switch to BCA page
    When I switch to "bridged_call_appearances" page
    #2. Add New aBCA
    And I create Bridged Call Appearance  ${localbcainfo}
    set to dictionary  ${localbcainfo}  AssociatedBCAProfile  &{localbcainfo}[AssociatedBCAProfile]
    set to dictionary  ${localbcainfo}  duplicate_aBCAProfile  &{localbcainfo}[AssociatedBCAProfile]
    set to dictionary  ${localbcainfo}  SelectPhoneNumber  &{localbcainfo}[SelectPhoneNumber]

    ### Verifications:
    And I create Bridged Call Appearance  ${localbcainfo}
    [Teardown]    run keywords  I delete BCA  ${localbcainfo}
    ...                    AND  I log off
    ...                    AND  I check for alert