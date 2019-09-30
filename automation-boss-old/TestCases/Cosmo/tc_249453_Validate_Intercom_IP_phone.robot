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
# Select Type 'Telephony' and Select Function 'Intercom'
# Enter Long label and short label
# Enter Extension of second user whose ip phone is registred and Save It
# Verify the Long Label appears on first user phone

*** Test Cases ***
Verify Long Label Appears
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${CosmoAccountName} with ${CosmoDMUser} option
    And I go to "Phone_system_tab1" -> "Users_link"

    ### Actions:
    When I click on "Service_Phone_name_link" button/link
    And I click on "Prog_Buttons_tab" button/link
    And I click on "Prog_Buttons_IP_Phones_tab" button/link
    And I select "Telephony" in "IP_Phones_Type_selection"
    And I select "Intercom" in "IP_Phones_Function_selection"
    And I enter "Longlabel331" in "IP_Phones_LongLabel_textbox" textbox
    And I enter "tests" in "IP_Phones_ShortLabel_textbox" textbox
    And I enter "1007" in "IP_Phones_Extension_textbox" textbox
    And I click on "Prog_Buttons_save_button" button/link

    ### Verification
    Then I verify "Prog_Buttons_IP_Phones_Longlabel_cell" contains "Longlabel331" text
    #And I stop impersonating

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***