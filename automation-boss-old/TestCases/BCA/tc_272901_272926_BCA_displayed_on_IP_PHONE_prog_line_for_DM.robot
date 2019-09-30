*** Settings ***
Documentation    1. Create BCA on Phone System -> Users -> Settings -> Prog Buttons -> IP-PHONES
...              2. Verify that the BCA is selected on the program line successfully
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
Validate the bca on program button line
    [Tags]    Regression   FAILED

    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    sleep  5s

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
    set to dictionary  ${localbcainfo}  AssignFromLocation  Choose from selected location

    # Start --- for creating and selecting BCA on program button lines
    set to dictionary  ${localbcainfo}  SelectType  Telephony
    set to dictionary  ${localbcainfo}  SelectFunction  Bridged Call Appearance
    set to dictionary  ${localbcainfo}  SelectLongLabel  abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel  abcd
    set to dictionary  ${localbcainfo}  CreateBcaUsingProgButton  ${true}
    set to dictionary  ${localbcainfo}  SelectBCA  ${True}
    # End

    ### Actions:
    #1. Switch to the Users page
    When I switch to "users" page
    #2. Regenerate the x-paths for the locator elements on IP-Phones program button page
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
    #3. Create BCA on the available program button line on IP-Phones
    And I create bca from programming button page   ${localbcainfo}
    #4. verify the BCA on BCA page
    And I switch to "bridged_call_appearances" page
    And I verify BCA  &{localbcainfo}

    #5. Again moved to the program button line and select the BCA on the line
    And I switch to "users" page
    #6. Regenerate the element locators on programming box page
#    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}
    #7. Select the BCA on programming button page
    And I select bca on user prog buttons page  &{localbcainfo}

    ### Verification:
    # Again move to the respective program button line and verify that the BCA is listed on the line
    Then I switch to "account_home" page
    And I switch to "users" page
#    And I move to the required line on program button page  ${PMUser}  IP Phones
    And I move to the required line on program button tab  ${PMUser}  Button Box 1
    And I verify BCA on program button line  &{localbcainfo}

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


