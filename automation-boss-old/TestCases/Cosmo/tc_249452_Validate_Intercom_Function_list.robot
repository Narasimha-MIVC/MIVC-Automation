*** Settings ***
Documentation    Validate Intercom in Function list

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource          ../Cosmo/Variables/Cosmo_Variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py  browser=${BROWSER}

#Built in library
Library  String

# Login to the server as staff user
# Swich account as DM/PM user
# Phone System > Users
# Select any user with IP phone
# Click on 'Service/Phone Name' of the selected user
# Prog Buttons > IP Phone
# Select any Programme button line
# Select Type 'Telephony'
# Verify if you could select Function Select box 'Intercom'


*** Test Cases ***
Validate Intercom in Function list
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${CosmoAccountName} with ${CosmoDMUser} option
    And I go to "Phone_system_tab1" -> "Users_link1"

    ### Actions:
    When I click on "Service_Phone_name_link" button/link
    And I click on "Prog_Buttons_tab" button/link
    And I click on "Prog_Buttons_IP_Phones_tab" button/link
    And I select "Telephony" in "IP_Phones_Type_selection"

    ### Verification
    Then I select "Intercom" in "IP_Phones_Function_selection"
    And I stop impersonating

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***