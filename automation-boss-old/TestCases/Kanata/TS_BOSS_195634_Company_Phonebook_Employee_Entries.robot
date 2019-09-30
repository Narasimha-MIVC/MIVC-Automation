*** Settings ***
Documentation  TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority

#Suite Setup and Teardown
Suite Setup       Set Init Env

#Keywords1 Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable filesot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections

*** Test Cases ***
01 Log into Portal as Staff Member, and switch to a Cosmo account with an available number(s) to assign a profile to
    Log    ${user_properties}    console=yes
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195634_Acoount} with ${AccWithoutLogin} option
    Then I verify "Home_page_company_name_div" contains "${TC_195634_Acoount}"

02 Create a user when next available phone number,
    When I switch to "users" page
    # Create user
    Set to Dictionary   ${user_properties}     au_firstname   FNuser105634
    Set to Dictionary   ${user_properties}     au_lastname    LNuser105634
    Set to Dictionary   ${user_properties}     au_businessmail   FNuser105634.LNuser105634@workemail.com
    Set to Dictionary   ${user_properties}     au_personalmail   FNuser105634.LNuser105634@homeemail.com
    Set to Dictionary   ${user_properties}     au_username    FNuser105634.LNuser105634@workemail.com
    Set to Dictionary   ${user_properties}     au_cellphone    4125551234
    Set to Dictionary   ${user_properties}     au_homephone    6135553214
    Set to Dictionary   ${user_properties}     request_by     ${TC_195634_User}
    ${phone_num}  ${extn}=    and I add user    &{user_properties}
    ${phoneinfo}=    Create Dictionary
    Set suite variable    &{phoneinfo}
    Set to Dictionary   ${phoneinfo}     phone_num   ${phone_num}
    Set to Dictionary   ${phoneinfo}     extn   ${extn}
    Log    ${phoneinfo["phone_num"]}    console=yes
    Log    ${phoneinfo["extn"]}    console=yes
    Then I verify that User exist in user table    &{user_properties}

03 Log into Portal as Staff Member, and switch to a Cosmo account, and impersonate a user of that account that has the Decision Maker roll.
    When I log off
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195634_Acoount} with ${TC_195634_User} option
    Then I verify "User_Options" contains "${TC_195634_User}"

04 Navigate to Home -> Contacts -> Company Phonebook.
    When I switch to "home_companyPhonebook" page
    Then I verify "company_phonebook_menu" contains "Company Phonebook"

05 Type the first or last name in the column filter fields.
    When I input "${user_properties["au_firstname"]}" in "company_phonebook_search_first_name_input"
    and I input "${user_properties["au_lastname"]}" in "company_phonebook_search_last_name_input"
    Then I verify "company_phonebook_entry_list" contains "${user_properties["au_firstname"]}"
    and I verify "company_phonebook_entry_list" contains "${user_properties["au_lastname"]}"
    and I verify "company_phonebook_entry_list" contains "${phoneinfo["phone_num"]}"

06 Close the user created above
    When I stop impersonating
    and I log off
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195634_Acoount} with ${AccWithoutLogin} option
    Then I verify "Home_page_company_name_div" contains "${TC_195634_Acoount}"
    When I switch to "users" page
    and I delete user ${user_properties["au_username"]} as user "${user_properties['au_firstname']} ${user_properties['au_lastname']}"
    Then I verify "au_datagrid_usersDataGrid" does not contain "${user_properties["au_username"]}"

*** Keywords ***
Set Init Env
    ${user_password}=    set variable    MitelRocks!666
    ${user_location}=    set variable    AutoTest_location_l4RYdNE7
    ${billing_location}=    set variable    AutoTest_location_l4RYdNE7
    ${user_properties}=    Create Dictionary
    Set suite variable    &{user_properties}
    Set to Dictionary   ${user_properties}     au_userlocation    ${user_location}
    Set to Dictionary   ${user_properties}     au_location    ${billing_location}
    Set to Dictionary   ${user_properties}     au_password    ${user_password}
    Set to Dictionary   ${user_properties}     au_confirmpassword    ${user_password}
    Set to Dictionary   ${user_properties}     ap_phonetype    MiCloud Connect Essentials
    Set to Dictionary   ${user_properties}     ap_phonenumber    random
    Set to Dictionary   ${user_properties}     ap_activationdate    today

    Set to Dictionary   ${user_properties}     hw_addhwphone    False
    Set to Dictionary   ${user_properties}     hw_type    Sale New
    Set to Dictionary   ${user_properties}     hw_model    ShoreTel IP420 - Sale
    Set to Dictionary   ${user_properties}     hw_power    False
    Set to Dictionary   ${user_properties}     hw_power_type    ShoreTel IP Phones Power Supply - Sale

    Set to Dictionary   ${user_properties}     role    Phone Manager
    Set to Dictionary   ${user_properties}     scope    Account
    Set to Dictionary   ${user_properties}     request_by    boss automation
    Set to Dictionary   ${user_properties}     request_source    Email
