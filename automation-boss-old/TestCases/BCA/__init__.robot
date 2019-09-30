*** Settings ***
Documentation    setting up the complete test suite directory

#Suite Setup  setup_all
Suite Teardown  clean_up_all

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
#Resource           ../../RobotKeywords/BOSSKeywords_BCA.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Keywords ***
#Provided precondition
#    Setup system under test

setup_all

    ${status}=  Verify Phone Numbers
    log  ${status}

    # If phone numbers are not found then Verify the location
    # If the location is not found add geographic location
    # Then add phone numbers to this geographic location
    run keyword if  ${status}!=True   Add and Verify Location

    Run Keywords  I log off
    ...           I check for alert
clean_up_all
#    cleaning up the test suite
    Close The Browsers

Verify Phone Numbers

    I login to ${URL} with ${bossUsername} and ${bossPassword}
    I switch to "switch_account" page
    I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option

    &{PhoneNumberInfo}=  copy dictionary  ${PHONE_INFO}
    I switch to "operations_phone_numbers" page
    ${status}=  verify phone numbers and their status  &{PhoneNumberInfo}
    [Return]  ${status}

Add and Verify Location
    I switch to "geographic_locations" page
    ${status}=  verify geographic location  &{GEO_LOC}[Location]
    run keyword if  ${status}!=True  Add Location

    ${status}=  Verify Phone Numbers
    log  ${status}
    # if false add phone numbers to this geographic location
    run keyword if  ${status}!=True  Add PhoneNumbers  &{GEO_LOC}[Location]

Add Location
    ${status}=  add geographic location  &{GEO_LOC}
    run keyword if  ${status}==True  Add PhoneNumbers  &{GEO_LOC}[Location]

Add PhoneNumbers
    [Arguments]  ${location}
    &{PhoneNumberInfo}=  copy dictionary  ${PHONE_INFO}
    log many  &{PhoneNumberInfo}

    # change the clientAccount, clientLocation fields
    set to dictionary  ${PhoneNumberInfo}  clientAccount  ${accountName1}
    set to dictionary  ${PhoneNumberInfo}  clientLocation  ${location}

    log many  &{PhoneNumberInfo}

    I switch to "operations_phone_numbers" page
    I add PhoneNumber  &{PhoneNumberInfo}
    I set PhoneNumber state  &{PhoneNumberInfo}