*** Settings ***
Documentation   Personal Information page testcases for Elvis


Resource        ../../RobotKeywords/DominatorKeywords.robot
Resource        ../../RobotKeywords/NavigationKeywords.robot

Resource        ../../RobotKeywords/BOSSKeywords.robot
Resource        ../../Variables/EnvVariables.robot

Library         ../../lib/BossComponent.py     browser=${BROWSER}
Library         JSONLibrary

# Tags allow tests to be run
Default Tags    Dominator     regression    Elvis   Swap

Suite Setup     Initialize Environment
Suite Teardown  Finalize Environment

*** Keywords ***

Initialize Environment
    ${details}=   Load JSON From File       ../Details/Users.json
    Set Suite Variable  ${usersDataGrid}        ${details["usersDataGrid"]}
    Set Suite Variable  ${ElvisSwapWizard}  ${details["ElvisSwapWizard"]}



    #Load the JSON values into a Python Python Dictionary Data Structure
    ${values}=          Load JSON From File         ../Values/Users.json
    #Randomize the Python Dictionary Data Structure values
    ${values}=          Update Random Values        ${values}
    Set Suite Variable  ${ManagedWithoutAddProfile}   ${values["ManagedWithoutAddProfile"]}
    Set Suite Variable  ${swap_select_2}   ${values["swap_select_2"]}
    Set Suite Variable  ${managedwithoutaddons_swap_select}   ${values["managedwithoutaddons_swap_select"]}
    Set Suite Variable  ${swap_summary}   ${values["swap_summary"]}
    Set Suite Variable  ${requestedby_summary}   ${values["requestedby_summary"]}


Finalize Environment
    Log Off
    Close The Browsers


*** Test Cases ***
TC_221559_Swap_Profiles_Courtesy_To_Managed_Without_Adds
    Given I login to ${ElvisURL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    And I switch to account Automation_Elvis with ${AccWithoutLogin} option
    When I move to Users page
    and I filter column headings for ${usersDataGrid} with BusinessEmail in ${ManagedWithoutAddProfile}
    and I show the context menu for ${usersDataGrid} with BusinessEmail in ${ManagedWithoutAddProfile}
    and I can choose the swap item from the grid context menu ${usersDataGrid["contextitems"]}
    And I fill in ${ElvisSwapWizard} form with ${swap_select_2}
    and I Click On "//*[@id='fnMessageBox_Yes']/span" Button/link
    And I click next to move the ${ElvisSwapWizard} to summary
    And I fill in ${ElvisSwapWizard} form with ${swap_summary}
    Then I finish the ${ElvisSwapWizard} without confirmation
    and I filter column headings for ${usersDataGrid} with BusinessEmail in ${ManagedWithoutAddProfile}
    When I show the context menu for ${usersDataGrid} with BusinessEmail in ${ManagedWithoutAddProfile}
    and I can choose the swap item from the grid context menu ${usersDataGrid["contextitems"]}
    And I fill in ${ElvisSwapWizard} form with ${swap_select_2}
    And I fill in ${ElvisSwapWizard} form with ${managedwithoutaddons_swap_select}
    And I click next to move the ${ElvisSwapWizard} to summary
    And I fill in ${ElvisSwapWizard} form with ${swap_summary}
    Then I finish the ${ElvisSwapWizard} without confirmation