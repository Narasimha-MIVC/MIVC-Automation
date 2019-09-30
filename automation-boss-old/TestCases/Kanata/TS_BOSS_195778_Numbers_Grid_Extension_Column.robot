*** Settings ***
Documentation  TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority

#Suite Setup and Teardown

#Keywords1 Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable filesot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections

*** Test Cases ***
01 Log into Portal as Staff Member, and switch to a Cosmo account
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195634_Acoount} with ${AccWithoutLogin} option
    Then I verify "Home_page_company_name_div" contains "${TC_195634_Acoount}"

02 navigate to Operations > Primary Partition
    When I switch to "primary_partition" page
    and I click element by xpath "Ph_number_tab"
    Then I verify the page "Phone Numbers"
    and I click checkbox of first entry by search text "Available" with canvasId "ProfileDataGridCanvas" and searchColumnId "PrimaryPartitionExtension"
    and I click element by xpath "primary_partition_assign_button"
    Then I verify button "primary_partition_assign_button" is enabled
    and I verify button "primary_partition_export_button" is enabled