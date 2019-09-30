*** Settings ***
Documentation    1. Select Phone System -> Users -> User -> Phone number -> Prog Buttons
...              2. Click on any of button box or IP phones and click on create New
...              3. No SCA option should be present for DM and PM
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
verify aBCA radio button with DM User
    [Tags]    Regression    FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    sleep  5s

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}

    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}
    set to dictionary  ${localbcainfo}  CreateBcaUsingProgButton     ${True}
    set to dictionary  ${localbcainfo}  VerifyRadioButton     ${True}
    set to dictionary  ${localbcainfo}  SelectType      All
    set to dictionary  ${localbcainfo}  SelectFunction      Bridged Call Appearance
    set to dictionary  ${localbcainfo}  SelectLongLabel    abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel    abcd

    ### Actions:
    #1.
    I switch to "users" page

    #2. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}

    #6. Create a new BCA on programming button page
    I verify bca radio button on add bca page  ${localbcainfo}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert

verify aBCA radio button with PM User
    [Tags]    Regression  FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  5s

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}

    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}
    set to dictionary  ${localbcainfo}  CreateBcaUsingProgButton     ${True}
    set to dictionary  ${localbcainfo}  VerifyRadioButton     ${True}
    set to dictionary  ${localbcainfo}  SelectType      All
    set to dictionary  ${localbcainfo}  SelectFunction      Bridged Call Appearance
    set to dictionary  ${localbcainfo}  SelectLongLabel    abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel    abcd

    ### Actions:
    #1.
    I switch to "users" page

    #2. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}

    #6. Create a new BCA on programming button page
    I verify bca radio button on add bca page  ${localbcainfo}

    [Teardown]  Run Keywords  I log off
    ...         AND  I check for alert


