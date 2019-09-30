*** Settings ***
Documentation   BOSS User Groups
...             SBOSS-2760
...             dev-Jim Wendt

Resource        ../../../RobotKeywords/DominatorKeywords.robot
Resource        ../../../RobotKeywords/NavigationKeywords.robot

Resource        ../../../RobotKeywords/BOSSKeywords.robot
Resource        ../../../Variables/EnvVariables.robot

Library         ../../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    ${details}=   Load JSON From File       DominatorExamples/UserGroups/SBOSS-2760_details.json
    Set Suite Variable  ${grid}             ${details["userGroupGrid"]}
    Set Suite Variable  ${wizard}           ${details["GroupWizard"]}

    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=      Load JSON From File     DominatorExamples/UserGroups/SBOSS-2760_values.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=      Update Random Values    ${values}
    Set Suite Variable    ${properties_ok}              ${values["properties_ok"]}
    Set Suite Variable    ${properties_courtesy_ok}     ${values["properties_courtesy_ok"]}
    Set Suite Variable    ${properties_managed_ok}      ${values["properties_managed_ok"]}
    Set Suite Variable    ${properties_telephony_ok}    ${values["properties_telephony_ok"]}
    Set Suite Variable    ${properties_voicemail_ok}    ${values["properties_voicemail_ok"]}

Finalize Environment
    Log Off
    Close The Browsers

*** Test Cases ***
00 Login and navigate to the User Group Page As DM
	Given I login to ${URL} with ${DMemail} and ${DMpassword}
	Then I move to User Groups page

01 Disable Voicemail callback option for UserType Courtesy while adding or Editing UserGroups
	When I click the ${grid} add button
	Then I fill in ${wizard} form with ${properties_courtesy_ok}
	And I click next to move the ${wizard} to telephony
	And I click next to move the ${wizard} to voicemail
    And I verify ${wizard["fields"]["AllowVoicemailCallBack"]} state is disabled
	And I cancel the ${wizard}

02 Disable Voicemail callback option for UserType Managed while adding or Editing UserGroups
	When I click the ${grid} add button
	And I fill in ${wizard} form with ${properties_managed_ok}
	And I click next to move the ${wizard} to telephony
	And I click next to move the ${wizard} to voicemail
    And I verify ${wizard["fields"]["AllowVoicemailCallBack"]} state is disabled
	And I cancel the ${wizard}

03 Disable Voicemail callback option for UserType Telephony only while adding or Editing UserGroups
	When I click the ${grid} add button
	And I fill in ${wizard} form with ${properties_telephony_ok}
	And I click next to move the ${wizard} to telephony
	And I click next to move the ${wizard} to voicemail
    And I verify ${wizard["fields"]["AllowVoicemailCallBack"]} state is disabled
	And I cancel the ${wizard}

# Am not able to see this option in Profile Type options
# 04 Disable Voicemail callback option for UserType Voicemail while adding or Editing UserGroups
	# When I click the ${grid} add button
	# And I fill in ${wizard} form with ${properties_voicemail_ok}
	# And I click next to move the ${wizard} to telephony
	# And I click next to move the ${wizard} to voicemail
    # And I verify ${wizard["fields"]["AllowVoicemailCallBack"]} state is disabled
	# And I cancel the ${wizard}

# Out of order because this is only fro non staff
06 Verify the Note Contact Mitel Support
	When I click the ${grid} add button
	Then I fill in ${wizard} form with ${properties_ok}
	And I click next to move the ${wizard} to telephony
	And I click next to move the ${wizard} to voicemail
    And I confirm ${wizard} does contain the text Contact Mitel support to change this setting
	And I cancel the ${wizard}

05 Verify should allow only staff User to Edit the Voicemail callback option
    When I Log Off
    Then I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I move to User Groups page
	When I click the ${grid} add button
	Then I fill in ${wizard} form with ${properties_courtesy_ok}
	And I click next to move the ${wizard} to telephony
	And I click next to move the ${wizard} to voicemail
    And I verify ${wizard["fields"]["AllowVoicemailCallBack"]} state is enabled
	And I cancel the ${wizard}