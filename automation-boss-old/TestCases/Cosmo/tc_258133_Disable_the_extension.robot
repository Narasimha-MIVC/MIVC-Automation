*** Settings ***
Documentation    Disabling the extension for Shared Call Appearance

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
# Switch to a PM user
# Click on Home > Setting > Phone Settings
# Click on Shared Call Appearance under Feature
# Select Disabled and Save it


*** Test Cases ***
Disable the Phone system extension
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${CosmoAccountName} with ${CosmoPMUser} option
    And I go to "Home_tab1" -> "Home_Phone_Settings_link"

    ### Actions:
    When I click on "Shared_Call_Appearance_list" button/link
    And I click on "Shared_Call_Appearance_dropdown" button/link
    And I select "Disabled" in "Shared_Call_Appearance_dropdown"

    ### Verification
    Then I click on "Shared_Call_Appearance_submit" button/link
    And I click on "Shared_Call_Appearance_ok" button/link
    And I stop impersonating

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***