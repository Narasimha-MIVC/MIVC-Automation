*** Settings ***
Documentation    Presence of Edit Button for BCA

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
# Switch to a tenant
# Click on Phone Systems -> Bridge Call Appearances
# Verify Edit button is present


*** Test Cases ***
Verify Edit Button BCA
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${CosmoAccountName} with ${AccWithoutLogin} option
    And I go to "Phone_system_tab1" -> "Phone_system_BCA_link"

    ### Actions:
    When I click on "BCA_grid_first_item" button/link
    And I click on "BCA_Edit_Button" button/link

    ### Verification
    Then I verify "BCA_Edit_Button_Text" contains "Edit" text

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***