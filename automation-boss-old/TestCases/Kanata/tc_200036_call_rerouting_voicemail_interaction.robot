
#Set up the FindMe section to press 1 during greeting on the basic call routing on a Cosmo profile. Verify the changes on D2.
#Design Steps
#StepDescriptionExpected
#
#
#Step 1Requires active account with a partition on the Cosmo cluster with available profiles setup.
#
#Step 2Log in to Portal as an M5 Staff member and attempt to switch accounts to the selected account.
#Portal switches account to selected account.
#
#Step 3Navigate to 'Organization > Phone System > Users', and click the Service/Phone Name of an available profile. Select the Call Routing tab.
#The Call Routing tab of the profile's Phone Settings displays.
#
#Step 4
#Click the 'Set Up Basic Routing' button, then click 'Next' twice.
#
#The FindMe tab of the 'Call Routing: Basic Routing' wizard displays.
#
#Step 5Select 'Enabled: Use my FindMe settings to continue routing the call.' Select 'Play my voicemail greeting first...' Choose two numbers from the number selector drop-down. Click 'Finish'.
#The Call Routing tab displays again and the third rule has changed to 'If callers press 1 while listening to my voicemail greeting try to find me on these numbers sequentially:' then the selected numbers.
#
#Step 6Access the ShoreTel Director on the Cosmo server. Navigate to Administration > Users > Users. Switch the Tenant to the selected account. Select the User of the profile that you edited. Then select the Routing tab in the User details.
#The Routing tab of the profile displays.
#
#Step 7Verify that the routing information matches the changes made.
#The information is accurate.
#
#Step 8In Portal press the 'Change' button next to the third rule.
#The FindMe tab of the 'Call Routing: Basic Routing' wizard displays.
#
#Step 9Select 'Prompt the caller to record their name' check-box under 'Play my voicemail greeting first…' Choose two new numbers from the number selector drop-down. Click 'Finish'.
#The Call Routing tab displays again and the third rule has changed to 'If callers press 1 while listening to my voicemail greeting try to find me on these numbers sequentially and prompt the caller to record their name:' then the selected numbers.
#
#Step 10In Director verify that the routing information matches the changes made.
#The information is accurate.






*** Settings ***
Documentation    sample test description

Resource    ../RobotKeywords/BOSSKeywords.robot
Resource    ../Variables/EnvVariables.robot

#libraries
Library     ../lib/BossComponent.py    browser=${BROWSER}




*** Test Cases ***
Sample test title
    [Tags]    DEBUG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account AutoTest_Acc_PaS0PwXJ with ${AccWithoutLogin} option

    When I click Users in Phone System tab
    and I right click on "autoemerbillBOXQ Auto" link in "au_datagrid_usersDataGrid" and select "PhoneSettingsContextMenuItem"
    and I select "CallRoutingTab" tab and wait for "CallRoutingTab_Availability"
    and I click the "CallRoutingTab_ChangeVoiceMailInteraction" button
    and I adjust voicemail interaction form with extension "5136"


    Then I verify voicemail interaction form with extension "5136"
