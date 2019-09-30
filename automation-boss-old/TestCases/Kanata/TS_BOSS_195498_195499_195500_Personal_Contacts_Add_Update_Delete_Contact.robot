*** Settings ***
Documentation  TC 195498 Personal Contacts - Add Contact,  TC 195499 Personal Contacts - Update Contact, TC 195500 Personal Contacts - Delete Contact

#Keywords1 Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable filesot
Resource          ../../Variables/EnvVariables.robot
Resource          ../../Variables/PersonalContactInfo.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String


*** Test Cases ***
#test case 195498
01 Log into Portal as Staff Member, and switch to a Cosmo account, and impersonate a user of that account that has the Decision Maker roll.
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195498_Acoount} with ${TC_195498_User} option
    Then I verify "User_Options" contains "${TC_195498_User}"

02 Navigate to Home -> Contacts -> Personal Contacts
    When I switch to "home_personalContacts" page
    Then I verify "personal_contacts_menu" contains "Personal Contacts"

03 Click on the 'Add Group' button.
    When I click element by xpath "add_contact_group_button"
    Then I verify "contacts_add_group_form_OK_button" contains "OK"

04 Enter a group name and click 'OK' button.
    When I input "${New_Contact_Group_Name}" in "new_contacts_group_name_input"
    and I click element by xpath "contacts_add_group_form_OK_button"
    Then I verify "contact_group_list" contains "${New_Contact_Group_Name}"

05 Click on 'Add' button
    When I click element by xpath "add_contact_button"
    Then I verify "add_contacts_form_OK_button" contains "OK"

06 Keep mandatory field blank and click 'OK' button
    When I click element by xpath "add_contacts_form_OK_button"
    Then I verify "${Mandatory_field_required_message}" is displayed on screen

07 Select the new group from Step 4 from the Group dropdown, and fill in all the fields, and click on 'OK' button
    When I do select "${New_Contact_Group_Name}" in "new_contact_group_drop_down"
    and I input "${New_Contact_First_Name}" in "new_contact_first_name_input"
    and I input "${New_Contact_Last_Name}" in "new_contact_last_name_input"
    and I input "${New_Contact_Compnay_Name}" in "new_contact_company_name_input"
    and I input "${New_Contact_Department_Name}" in "new_contact_deportment_name_input"
    and I input "${New_Contact_Business_Phone_Number}" in "new_contact_business_phone_input"
    and I input "${New_Contact_Mobile_Phone_Number}" in "new_contact_mobile_phone_input"
    and I input "${New_Contact_Home_Phone_Number}" in "new_contact_home_phone_input"
    and I do select "${New_Default_Number}" in "new_contact_default_number_drop_down"
    and I input "${New_Contact_Email}" in "new_contact_email_input"
    and I click element by xpath "add_contacts_form_OK_button"
    Then I verify "contact_group_list" contains "${New_Contact_First_Name}"
    Then I verify "contact_group_list" contains "${New_Contact_Last_Name}"
    Then I verify "contact_group_list" contains "${New_Contact_Compnay_Name}"
    Then I verify "contact_group_list" contains "${New_Contact_Business_Phone_Number}"
    Then I verify "contact_group_list" contains "${New_Contact_Home_Phone_Number}"
    Then I verify "contact_group_list" contains "${New_Contact_Mobile_Phone_Number}"


08 Type any word matching from Contact's details in the search field of the particular column
    When I input "${New_Contact_Compnay_Name}" in "contact_search_company_input"
    and I input "${New_Contact_First_Name}" in "contact_search_first_name_input"
    and I input "${New_Contact_Last_Name}" in "contact_search_last_name_input"
    Then I verify "contact_group_list" contains "${New_Contact_First_Name}"

#09 Access the HQ SQL database on the Cosmo server. Search for the new Personal Contact entry on the Buddies table (list of personal contacts).

#test case 195499
10 Select one of the Personal Contacts, and click the 'Update' button.
    #serach to limit this one as only entry
    When I input "${New_Contact_Compnay_Name}" in "contact_search_company_input"
    and I input "${New_Contact_First_Name}" in "contact_search_first_name_input"
    and I input "${New_Contact_Last_Name}" in "contact_search_last_name_input"
    #click update
    and I click element by xpath "contact_first_entry_select_box"
    and I click element by xpath "contact_update_contact_button"
    Then I verify "contacts_update_contact_form_OK_button" contains "OK"

11 Change the information in all of the fields, then click the 'OK' button.
    #change the contact info
    When I input "${Modified_Contact_First_Name}" in "update_contact_first_name_input"
    and I input "${Modified_Contact_Last_Name}" in "update_contact_last_name_input"
    and I input "${Modified_Contact_Compnay_Name}" in "update_contact_company_name_input"
    and I input "${Modified_Contact_Department_Name}" in "update_contact_deportment_name_input"
    and I input "${Modified_Contact_Business_Phone_Number}" in "update_contact_business_phone_input"
    and I input "${Modified_Contact_Mobile_Phone_Number}" in "update_contact_mobile_phone_input"
    and I input "${Modified_Contact_Home_Phone_Number}" in "update_contact_home_phone_input"
    and I do select "${Modified_Default_Number}" in "update_contact_default_number_drop_down"
    and I input "${Modified_Contact_Email}" in "update_contact_email_input"
    and I click element by xpath "update_contacts_form_OK_button"
    #search this entry
    and I input "${Modified_Contact_Compnay_Name}" in "contact_search_company_input"
    and I input "${Modified_Contact_First_Name}" in "contact_search_first_name_input"
    and I input "${Modified_Contact_Last_Name}" in "contact_search_last_name_input"
    Then I verify "contact_group_list" contains "${Modified_Contact_First_Name}"
    Then I verify "contact_group_list" contains "${Modified_Contact_Last_Name}"
    Then I verify "contact_group_list" contains "${Modified_Contact_Compnay_Name}"
    Then I verify "contact_group_list" contains "${Modified_Contact_Business_Phone_Number}"
    Then I verify "contact_group_list" contains "${Modified_Contact_Home_Phone_Number}"
    Then I verify "contact_group_list" contains "${Modified_Contact_Mobile_Phone_Number}"

#12 Access the HQ SQL database on the Cosmo server. Search for the Personal Contact entry that was changed on the Buddies table (list of personal contacts).

#test case 195500
13 Select one of the Personal Contacts, and click the 'Delete' button.
    #serach to limit this one as only entry
    When I input "${Modified_Contact_Compnay_Name}" in "contact_search_company_input"
    and I input "${Modified_Contact_First_Name}" in "contact_search_first_name_input"
    and I input "${Modified_Contact_Last_Name}" in "contact_search_last_name_input"
    #click update
    and I click element by xpath "contact_first_entry_select_box"
    and I click element by xpath "contact_delete_contact_button"
    Then I verify "contacts_delete_contact_confirm_yes_button" contains "Yes"

14 Click the 'Yes' button, then the 'OK' button on the confirmation popup.
    When I click element by xpath "contacts_delete_contact_confirm_yes_button"
    #serach to limit this deleted entry
    and I input "${Modified_Contact_Compnay_Name}" in "contact_search_company_input"
    and I input "${Modified_Contact_First_Name}" in "contact_search_first_name_input"
    and I input "${Modified_Contact_Last_Name}" in "contact_search_last_name_input"
    Then I verify "contact_group_list" does not contain "${Modified_Contact_First_Name}"
    Then I verify "contact_group_list" does not contain "${Modified_Contact_Last_Name}"
    Then I verify "contact_group_list" does not contain "${Modified_Contact_Compnay_Name}"
    Then I verify "contact_group_list" does not contain "${Modified_Contact_Business_Phone_Number}"
    Then I verify "contact_group_list" does not contain "${Modified_Contact_Home_Phone_Number}"

15 Delete Contact Group Created in this test case
    When I right click on element contains text "${New_Contact_Group_Name}" in "contact_group_list" and select "delete_contact_group_li"
    and I click element by xpath "delete_contact_group_confirm_yes_button"
    Then I verify "contact_add_group_grid" does not contain "${New_Contact_Group_Name}"

#15 Access the HQ SQL database on the Cosmo server. Search for the Personal Contact entry that was changed on the Buddies table (list of personal contacts).
