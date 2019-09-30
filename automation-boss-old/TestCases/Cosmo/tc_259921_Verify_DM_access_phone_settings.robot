*** Settings ***
Documentation    Verify DM access to user phone settings

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
# Swich account as DM user
# Phone System > Users
# Select any user with TN and extension
# Right click on that user
# Verify if the Phone Setting is enabled


*** Test Cases ***
Verify DM access to user phone settings
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${CosmoAccountName} with ${CosmoDMUser} option

    ### Actions:
    When I go to "Phone_system_tab1" -> "Users_link"

    ### Verification
    Then I right click a user with extension "1004"
    And I stop impersonating

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***