*** Settings ***
Documentation    1. Add BCA from BCA page UI and then select it on Phone System -> Users -> User -> Phone number -> Prog Buttons
...              2. Create BCA on Phone System -> Users -> User -> Phone number -> Prog Buttons
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
Select BCA Through Program Buttons
    [Tags]    Regression  Functional

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  3s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s
    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
#    set to dictionary  ${localbcainfo}  OtherSettings  ${True}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  2s
    #3.
    And I verify BCA  &{localbcainfo}
    #4.
    And I switch to "users" page

    #5. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}

    #6. Select a BCA on programming button page

    set to dictionary  ${localbcainfo}  SelectType  All
    set to dictionary  ${localbcainfo}  SelectFunction  Bridged Call Appearance
    set to dictionary  ${localbcainfo}  SelectLongLabel  abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel  abcd
    set to dictionary  ${localbcainfo}  SelectBCA  ${True}
    And I select bca on user prog buttons page  &{localbcainfo}

    [Teardown]  run keywords  I switch to "account_home" page
    ...         AND  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

Select BCA Through Program Buttons_123
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    sleep  1s
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s
    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
#    set to dictionary  ${localbcainfo}  OtherSettings  ${True}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  2s
    #3.
    And I verify BCA  &{localbcainfo}
    #4.
    And I switch to "users" page

    #5. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}

    #6. Select a BCA on programming button page

    set to dictionary  ${localbcainfo}  SelectType  All
    set to dictionary  ${localbcainfo}  SelectFunction  Bridged Call Appearance
    set to dictionary  ${localbcainfo}  SelectLongLabel  abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel  abcd
    set to dictionary  ${localbcainfo}  SelectBCA  ${True}
    And I select bca on user prog buttons page  &{localbcainfo}

    [Teardown]  run keywords  I switch to "account_home" page
    ...         AND  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


