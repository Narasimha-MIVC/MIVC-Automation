
#TCID: 203457Title: COSMO - As a DM-PM I should be able to set Transfer Line ButtonsPriority: 2 - Med
#Description
#As a DM-PM I should be able to set Transfer Blind/Transfer Consultative/Transfer Intercom/Transfer to Mailbox/Transfer Whisper Line Buttons.
#Design Steps
#StepDescriptionExpected
#
#Step 1
#Pre-Requisites: A valid COSMO account with at least two users provisioned.
#
#Login as yourself so you can determinte who is a DM/PM on the account you decide to use.  You can verify this by clicking on Phone System -> Users  Pay attention to the DM/PM columns.  Whoever has a check next to their name you can use.  If you don't want to log all the way out and back in, simply impersonate the user by clicking on the gear in the upper right hand corner of the screen...switch back to the account you are currently in...select person to log in as...select a DM or PM from the drop down list.
#The home page for the chosen account will appear
#Step 2
#Go to Phone Systems > Users
#All of the users for the partition will appear.
#Step 3
#Left click on the chosen user under the Service/Phone Name column
#This will bring you to the phone settings for that user.
#Step 4
#Navigate to the Prog Buttons tab
#This will bring up the Program Buttons for the user. If none have been set, they will all be set to Call Appearance.
#
#*To remove a Program Button, set them back to Call Appearance and hit Save. After about 5 seconds, the programmed button will disappear.*
#Step 5
#Set the program buttons as follows:
#
#1 - (Cannot Change)
#2 - Transfer Blind
#3 - Transfer Consultative
#4 - Transfer Intercom
#5 - Transfer to Mailbox
#6 - Transfer Whisper
#Under the the target column the following should appear:
#
#Transfer Blind: Extension or External
#Transfer Consultative: Extension or External
#Transfer Intercom: Extension
#Transfer to Mailbox: Extension
#Transfer Whisper: Extension
#Step 6
#Put in a Long Label and Short Label for each button (except 1)
#
#Where it says Exntesion or External put in in a valid external TN. Where it says extension ONLY put in a valid extension.
#
#NOTE - The extension needs to be provisioned to be valid.
#
#Click Save
#The changes should save, no errors should appear.
#Step 7
#Go into Director and confirm the changes have been saved there as well.
#
#To Do This:
#1. Log Into Director
#2. Click on the Wrench Icon (Administration)
#3. Under Users, Click Programmable Buttons
#4. In the top right corner, make sure your account is selected
#5. Select your user
#The changes made in BOSS should be reflected in Director as well.





*** Settings ***
Documentation    sample test description

Resource    ../RobotKeywords/BOSSKeywords.robot
Resource    ../Variables/EnvVariables.robot
Resource    ../Variables/ProgBtnInfo.robot

#libraries
Library     ../lib/BossComponent.py    browser=${BROWSER}



*** Test Cases ***
203457 COSMO - As a DM-PM I should be able to set Transfer Line Buttons
    [Tags]    DEBUG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account AutoTest_Acc_PaS0PwXJ with ${AccWithoutLogin} option

    @{ITEMS}    Create List    ${proginfo101}   ${proginfo102}    ${proginfo103}   ${proginfo104}  ${proginfo105}
    :FOR    ${proginfo}    IN    @{ITEMS}
    \    Log    ${proginfo}
    \    set to dictionary  ${proginfo}    extension  5144
    \    set to dictionary  ${proginfo}    user_email  boss_auto_locpm_BOXQ@shoretel.com
    \    And I add prog button    &{proginfo}
    \    And I verify programmed button    &{proginfo}
