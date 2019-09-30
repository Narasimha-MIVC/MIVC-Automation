*** Settings ***
Documentation  On Hold Music - Delete (tc 194621)

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Env file
Resource          ../../Variables/EnvVariables.robot

#libraries
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           Collections

*** Variables ***
#Note: As a precondition, at least one On Hold Music file must exists.

*** Test Cases ***

On-Hold Music - Delete (tc 194621)
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I open On Hold Music
    @{onHoldMusicData}=  and I select a On Hold Music file
    and I click on delete button and confirm
    Then I verify delete operation is successful  @{onHoldMusicData}

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

