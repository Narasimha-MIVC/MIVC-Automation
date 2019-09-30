*** Settings ***
Documentation    1. Select Phone System -> Users -> User -> Phone number -> Prog Buttons
...              2. Click on any of button box or IP phones and click on create New
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
create BCA Through Program Buttons with PM User
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    sleep  5s

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
    set to dictionary  ${localbcainfo}  OtherSettings  ${True}

    ### Actions:
    #1.
    I switch to "users" page

    #5. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}

    #6. Create a new BCA on programming button page
    set to dictionary  ${localbcainfo}  CreateBcaUsingProgButton     ${True}
    set to dictionary  ${localbcainfo}  SelectType  All
    set to dictionary  ${localbcainfo}  SelectLongLabel  abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel  abcd
    set to dictionary  ${localbcainfo}  SelectFunction  Bridged Call Appearance
    I create bca from programming button page  ${localbcainfo}

    #7. Again switch to users page and regenerate all locators, because after creating a new bca from programming button
    #tab it lands again in phone tab in phone setting page
    I switch to "users" page

    #8. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}


    #9. Select a BCA on programming button page
    And I select bca on user prog buttons page  &{localbcainfo}
    sleep  2s
    Then I switch to "bridged_call_appearances" page

    [Teardown]  run keywords  I switch to "bridged_call_appearances" page
    ...         AND  I delete BCA  ${localbcainfo}
    ...         AND  sleep  5s
    ...         AND  I log off
    ...         AND  I check for alert

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


