*** Settings ***
Documentation     Keywords supported for AOB portal
...               dev- Saurabh
...               Comments:

Library    Collections

*** Keywords ***
I login to AOB page
    [Documentation]  This keyword will help user to login to AOB portal.
    ...   Variable name: URL1- URL of Boss Portal
    ...   bossUserName: Staff User
    ...   bossPassword: Staff User Password
    ...   AOBAccount: AOB account name
    ...   AccWithoutLogin: Option to be choose while switching account
    ...   Note: has to be placed in EnvVariable.robot file
    I login to ${URL} with ${bossUsername} and ${bossPassword}
    I switch to "switch_account" page
    I switch to account ${AOBAccount} with ${AccWithoutLogin} option
    I switch to "aob" page

I navigate to Location and user page
    [Documentation]  This keyword will help user to go to Location and User page from Welcome Page.
    ${result}=      run keyword   aob_navigateto_locationanduser
    should be true  ${result}

I navigate to transfer numbers page from welcome page
    [Documentation]  This keyword will help user to go to Transfer requests page from Welcome Page.
    ${result}=      run keyword   aob_navigate_to_transfer_requests
    should be true  ${result}

I click Transfer button
    [Documentation]  This keyword will help user to open new Transfer request form.
    run keyword   aob_click_transfer_button

I select other current provider
    [Documentation]  This keyword will help user to select Other (specify) current provider
    run keyword   aob_select_other_current_provider

I insert "${provider_name}" into provider name
    [Documentation]  This keyword will help user to set provider name
    run keyword   aob_set_provider_name  ${provider_name}

I click on authorization checkbox
    [Documentation]  This keyword will help user to authorize transfer request
    run keyword   aob_authorize_transfer_request

I save Transfer request
    [Documentation]  This keyword will help user to save transfer request
    run keyword   aob_save_transfer_request

I check activation date    #i check location activation status
    [Documentation]  This keyword will get the location name and the activation date of location from Location and User page.
    ...   status_list: Status of active location
    ...   date: Activation date of location
    ...   loc_name: Current Active location
    ...   result: status of function True or False
    [Arguments]  @{status_list}
    ${loc_name}  ${date}   ${result}=      run keyword   aob_validate_location_activation_date   @{status_list}
    [Return]  ${loc_name}  ${date}
    should be true  ${result}

I check activation ${date} in geographic page for ${loc_name}  #move to boss
    [Documentation]  This keyword will verify the location's activation date in BOSS portal under Geographic Location page
    ...   date: Activation date of location
    ...   loc_name: Current Active location
    ...   result: status of function True or False
    ${result}=      run keyword   validate_geo_location_date   ${date}  ${loc_name}
    should be true  ${result}

I click back button  #shadow root
    [Documentation]  This keyword will click on Back button in AOB page. (This button is in shadow root, function may be modified in future)
    ...   result: status of function True or False
    ${result}=      run keyword   aob_back_button
    should be true  ${result}

I click save and logout button  #shadow root
    [Documentation]  This keyword will click on Save && Logout button in AOB page. (This button is in shadow root, function may be modified in future)
    ...   result: status of function True or False
    ${result}=      run keyword   aob_save_and_logout_button
    should be true  ${result}

I click logout button  #shadow root
    [Documentation]  This keyword will click on Logout button in AOB location and user page. (This button is in shadow root, function may be modified in future)
    ...   result: status of function True or False
    ${result}=      run keyword   aob_logout_button
    should be true  ${result}

I verify the page "${page_name}"
    [Documentation]  This keyword will verify if correct page  has opened or not. User has to pass heading of page.
    ...   page_name: Name of heading in page
    ...   result: status of function True or False
    ${result}=      run keyword   verify_page_aob  ${page_name}
    should be true  ${result}

I check button name for location and user
    [Documentation]  This keyword will check the correct button name is present on Location and User page or not.
    ...   result: status of function True or False
    ${result}=      run keyword   aob_location_and_user_button
    should be true  ${result}

I go to add user page  #mentioned the from where
    [Documentation]  This keyword will help to go User page for current location from Location and User page.
    ...   result: status of function True or False
    ${result}=      run keyword   aob_user_page
    should be true  ${result}

I create User
    [Documentation]  This keyword will fill the user form in User Page
    ...   AobUserDetail: User detail like first name, last name, extention etc. Detail can be found in aob_variable.robot file.
    ...   result: status of function True or False
    [Arguments]  &{AobUserDetail}
    ${result}=      run keyword   aob_create_user   &{AobUserDetail}
    should be true  ${result}

I Edit AOB User
    [Documentation]  This keyword will edit existing the user fields in User Page.
    ...   EditAobUserDetail: User detail like first name, last name, extention etc. Detail can be found in aob_variable.robot file.
    ...   result: status of function True or False
    [Arguments]  &{EditAobUserDetail}
    ${result}=      run keyword   aob_create_user   &{EditAobUserDetail}
    should be true  ${result}

#I verify "${message}" is displayed on screen  #rename
#    [Documentation]  This keyword will verfify the message occurs on screen.
#    ...   result: status of function True or False
#    ${result}=      run keyword   verify message displayed   ${message}
#     should be true    ${result}

I remove pop up message
    [Documentation]   This keyword will remove error pop up messages by clicking "continue" or "stay on page" button, based on the option provided in dictionary.
    ...   AobPopUpOption: Button name, which need to be clicked. Detail can be found in aob_variable.robot file.
    ...   result: status of function True or False
    [Arguments]  &{AobPopUpOption}
    ${result}=      run keyword   remove_popup      &{AobPopUpOption}
     should be true    ${result}

I verify the Location and User page   #rename to some meaningful its confusing
    [Documentation]   This keyword will count the number of user created in each bundle and matched it with the bundle utilization
    ...   result: status of function True or False
    ${result}=      run keyword   user_page_verification
     should be true    ${result}

I click "${btn}" button
    [Documentation]   This keyword will click on button on User page. If this does not work check if there are other keyword for clicking specific button available
    ...   btn: Name of button "Cancel" or "Save"
    ...   result: status of function True or False
    ${result}=      run keyword   aob_click_button   ${btn}
     should be true    ${result}

I check user field values
    [Documentation]   This keyword will check if all the user field has been reset properly or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_user_field
     should be true    ${result}

I check if location is sorted
    [Documentation]   This keyword will check if locations under location and user page is in sorted order or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_location_label
     should be true    ${result}

I switch bundle and verify text
    [Documentation]   This keyword will traverse through every bundle and verify if bundle switches or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_bundle_switch
     should be true    ${result}

I click on next bundle
    [Documentation]   This keyword will click on next bundle from current bundle
    ...   result: status of function True or False
    ${result}=      run keyword   aob_click_next_bundle
     should be true    ${result}

I check bundle name "${name}"
    [Documentation]   This keyword will check if perticular bundle is present or not
    ...   name: Name of bundle which need to be check
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_bundle_name   ${name}
     should be true    ${result}

I click on skip user button  #check if can be merge with click button
    [Documentation]   This keyword will hide user form and click on Skip button to move to call handling page
    ...   result: status of function True or False
    ...   heading: return the heading of last build
    ${result}   ${heading}=      run keyword   aob_click_skip_user
    [Return]   ${heading}
    should be true    ${result}

I check user name "${name:[^"]+}" for bundle "${bundle_name}"
    [Documentation]   This keyword will check for given user in given bundlename
    ...   name: Name of User
    ...   bundle_name: Bundle name
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_user_name   ${name}  ${bundle_name}
     should be true    ${result}

I check url
    [Documentation]   This keyword will verify if the correct url is opened from help link in AOB page
    ...   url_help: list of url with salesforce user name and password which need to place in EnvVariable.robot file
    ...   result: status of function True or False
    [Arguments]  &{url_help}
    ${result}=      run keyword   aob_help_url   &{url_help}
     should be true    ${result}

I clear "${field_name}" field
    [Documentation]   This keyword will clear the given field in user page
    ...   field_name: name of feild which need to be clear. like: firstName, lastName, Extention, Email etc.
    ...   result: status of function True or False
    ${result}=      run keyword   aob_clear_users_fields   ${field_name}
     should be true    ${result}

I verify AOB error "${message}" for "${field}"
    [Documentation]   This keyword will verify the error message occured after clearing user forms. Shadow root funtion
    ...   field: name of feild which need to be clear. like: firstName, lastName, Extention, Email etc.
    ...   message: Message to verify for perticular field
    ...   result: status of function True or False
    ${result}=      run keyword   aob_error_message   ${message}  ${field}
     should be true    ${result}

I check if user is created
    [Documentation]   This keyword will check if any user is created in AOB page or not.
    ...   (This function is used for checking a condition for edit user not i.e if status True which means user it created and no need to create a user for the test case)
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_created_user
    [Return]  ${result}

I verify edited user "${name}"
    [Documentation]   This keyword will check the title name of user in AOB page
    ...   name: name of user need to verify
    ...   result: status of function True or False
    ${result}=      run keyword   aob_verify_edited_user  ${name}
    should be true    ${result}

I check if user switched
    [Documentation]   This keyword will check that upon saving user, bundle is getting switched or not
    ...   name: name of user need to verify
    ...   result: status of function True or False
    [Arguments]  &{userDictonary}
    ${result}=      run keyword   aob_user_switch   &{userDictonary}
    should be true    ${result}

I get current bundle name
    [Documentation]   This keyword will get the current bundle name
    ...   bundle_name: name of current active bundle
    ...   result: status of function True or False
    ${result}  ${bundle_name}=      run keyword   aob_get_bundle_name
    [Return]  ${bundle_name}
    should be true    ${result}

I check AOB user in Boss page for email "${email}"   #move to boss
    [Documentation]   This keyword will check aob user in boss portal
    ...   email: email of user
    ...   result: status of function True or False
    ${result}=      run keyword   aob_verify_user_inBoss  ${email}
    should be true    ${result}

I cilck button "${button}" to check phone number drop down status
    [Documentation]   This keyword will check the status of phone number drop down upon clicking on Existing and None button
    ...   button: Button name eg. "None" or "Existing"
    ...   result: status of function True or False
    ${result}=      run keyword   aob_enables_disbale_drop_down  ${button}
    should be true    ${result}

I check if user exist with phone number
    [Documentation]   This keyword will check if any user is present in AOB page with phone number.(If not user will get
    ...   created else same user can be used to edit)
    ...   num: phone number of user
    ...   result: status of function True or False
    ${result}   ${num}=      run keyword   aob_check_user_with_profile
    [Return]  ${result}   ${num}
    #should be true    ${result}

I check if phone number "${num}" becomes available
    [Documentation]   This keyword will check if the perticular num is available to use or not
    ...   num: phone number of user
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_if_number_available  ${num}
    should be true    ${result}

I check if phone number "${num}" is not available
    [Documentation]   This keyword will check if the perticular num is available to use or not
    ...   num: phone number of user
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_if_number_available  ${num}
    should not be true    ${result}

I update single phone number state  #move to boss
    [Documentation]   This keyword update the single phone number status
    ...   phone_detail: detail contains phone numbers data
    ...   result: status of function True or False
    [Arguments]  &{phone_detail}
    ${result}=      run keyword   update_single_phonenumber  &{phone_detail}
    should be true    ${result}

I verify location status "${status}" and button "${btn}"
    [Documentation]   This keyword will verify the location status and the button name on location and users page
    ...   loc_status: detail contain status which need to verify and button name
    ...   result: status of function True or False
    &{loc_status}=   Create Dictionary   status=${status}   btn_name=${btn}
    ${result}=      run keyword   aob_validate_location_status  &{loc_status}
    [Return]  ${result}
    #should be true    ${result}     #comment the validation because In complete:activates status need to create user if location status is not present

I create multiple user for one bundle
    [Documentation]   This keyword will create all user for one bundle
    ...   user_detail: detail contain user field values like firstName, lasName etc
    ...   result: status of function True or False
    [Arguments]  &{user_detail}
    ${result}=      run keyword   aob_create_multiple_user  &{user_detail}
    should be true    ${result}

I get current active location name
    [Documentation]   This keyword will get the current location name and return it.
    ...   result: status of function True or False
    ${location}=      run keyword   aob_get_location_name
    [Return]  ${location}

I check initial order for location "${location_name}"  #move to boss
    [Documentation]   This keyword will check the initial order status from order page for the perticular location.
    ...   bundle: detail of initial order in dictionary
    ...   location_name: location name for whichi initial order is needed
    ...   result: status of function True or False
    ${result}  ${bundle}=      run keyword   aob_get_intial_order_detail   ${location_name}
    [Return]  &{bundle}
    should be true    ${result}

I verify initial order in user page
    [Documentation]   This keyword will verify the initial order in user page
    ...   dic: detail of initial order in dictionary
    ...   result: status of function True or False
    [Arguments]  ${dic}
    ${result}=      run keyword   aob_verify_inital_order   ${dic}
    should be true    ${result}

I check for user in current bundle
    [Documentation]   This keyword will check if is there any user can be created or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_user_in_current_budnle
    [Return]  ${result}

I zoom out and zoom in
    [Documentation]   This keyword will Zooom in the page and zoom out
    ...   result: status of function True or False
    ${result}=      run keyword   aob_zoom_in_zoom_out
    should be true  ${result}

I check if mitel easy setup link enable
    [Documentation]   This keyword will check if AOB link is enable or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_aob_link
    should be true  ${result}

I verify location status of "${location}"  #Move to Boss can be inhanced
    [Documentation]   This keyword will chedck if AOB location is Pending State or not
    ...   location: Name of Location
    ...   result: status of function True or False
    ${result}=      run keyword   aob_verify_location_status   ${location}
    should be true  ${result}

I select "${button}" button on call handling page
    [Documentation]   This keyword will click on "Set Up" or "Don't Setup on call handling page
    ...   button: Name of button which need to click on call handling page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_callhandling_setup   ${button}
    should be true  ${result}

I select future date on activate page
    [Documentation]   This keyword will select future date radio button in Activation page. (More radio button related click can be added)
    ...   result: status of function True or False
    ${result}=      run keyword   aob_select_future_day
    should be true  ${result}

I click save & finish button on Activate page
    [Documentation]   This keyword will click on Save and finsih button on activation page. Part of shadow root.
    ...   result: status of function True or False
    ${result}=      run keyword   aob_save_and_finsih
    should be true  ${result}

I create all user for one location
    [Documentation]   This keyword will create all the remaining user for current location.
    ...   user_detail: User detail dictionary
    ...   result: status of function True or False
    [Arguments]  &{user_detail}
    ${result}=      run keyword   aob_create_all_user_in_location  &{user_detail}
    should be true    ${result}

I check "${button}" is present
    [Documentation]   This keyword will check if button is present or not
    ...   button: Name of button
    ...   result: status of function True or False
    ${result}=      run keyword   verify_page_aob  ${button}
    should be true    ${result}

I check text "${text}" is present
    [Documentation]   This keyword will check if text is present on page or not
    ...   button: Name of button
    ...   result: status of function True or False
    ${result}=      run keyword   verify_page_aob  ${text}
    should be true    ${result}

I check current active user on user page
    [Documentation]   This keyword will verify if the new user is field is opened or not at user page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_current_active_user
    should be true    ${result}

I go to "${bundle}" bundle
    [Documentation]   This keyword will go to specific bundle on user page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_go_to_bundle  ${bundle}
    should be true    ${result}

I check "${icon}" is enabled
    [Documentation]   This keyword will check if Callhandling or Activate icon is enabnled not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_activate_icon_state  ${icon}
    should be true    ${result}

I select "${button}" option to setup call handling with phone number
    [Documentation]   This keyword will check if Callhandling or Activate icon is enabnled not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_call_handling_setup_selection  ${button}
    should be true    ${result}

I check if call handling is setup
    [Documentation]   This keyword will check if call handling is configured or not
    ...   button: Name of button
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_call_handling_setup
    [Return]    ${result}

I verify Start/Resume button exists
    [Documentation]   This keyword will check if Welcome page contains Start/Resume button
    ${result}=      run keyword   aob_welcome_page_start_button_exists
    should be true    ${result}

I verify element "${element}" exists
    [Documentation]   This keyword will check if element exists
    ${result}=      run keyword   aob_element_exists  ${element}
    should be true    ${result}

I verify Transfer requests page
    [Documentation]   This keyword will verify transfer requests page
    ${result}=      run keyword   aob_verify_transfer_requests_page
    should be true    ${result}

I open Add User Type modal
    [Documentation]   This keyword will open Add User Type modal
    run keyword   run keyword   aob_click_element  add_user_type_button

I verify Add User Type modal currency fields
    [Documentation]   This keyword will verify currency format on Add User Type modal
    ${result}=      run keyword   aob_verify_add_user_type_modal_currency_fields
    should be true    ${result}

I get first available number
    [Documentation]   This keyword will fetch first available number from the user page
    ...   button: Name of button
    ...   result: status of function True or False
    ${result}   ${num}=      run keyword   aob_get_first_available_number
    [Return]    ${num}

I check "${num}" is available in call handling page
    [Documentation]   This keyword will fetch first available number from the user page
    ...   button: Name of button
    ...   result: status of function True or False
    ${result}=      run keyword   aob_check_available_phone_number_in_call_handling_page   ${num}
    should be true  ${result}

I configure transfer number page
    [Documentation]   This keyword will fetch first available number from the user page
    ...   button: Name of button
    ...   result: status of function True or False
    [Arguments]  &{AOBTransferPhoneNumber}
    ${result}=      run keyword   aob_configure_transfer_more_page   &{AOBTransferPhoneNumber}
    should be true  ${result}

I verify learn more url
    [Documentation]   This keyword verify learn more url in user page
    ...   button: Name of button
    ...   result: status of function True or False
    [Arguments]  &{url_dict}
    ${result}=      run keyword   aob_verify_learn_more_url   &{url_dict}
    should be true  ${result}

I check calendar is present on activation page
    [Documentation]   This keyword verify if caendar is present on activation page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_activationpage_calendar
    should be true  ${result}

I click on calendar in activation page
    [Documentation]   This keyword will click on calendar in activation page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_click_on_calendar
    should be true  ${result}

I check calendar is enable on activation page
    [Documentation]   This keyword verify if caendar is enabled on activation page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_calendar_enabled
    should be true  ${result}

I check calendar is disable on activation page
    [Documentation]   This keyword verify if caendar is enabled on activation page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_calendar_enabled
    should not be true  ${result}

I check transfer number is created
    [Documentation]   This keyword check if any tranfer number request is created or not
    ...   result: status of function True or False
    ${result}=   run keyword   aob_transfer_number_is_created
    [Return]  ${result}

I try to open two section at same time
    [Documentation]   This keyword check two section should not open at same time
    ...   result: status of function True or False
    ${result}=      run keyword   aob_open_two_section
    should be true  ${result}

I check number "${num}" on transfer number page
    [Documentation]   This keyword will check number is present on transfer number page
    ...   result: status of function True or False
    ${result}    ${num}=      run keyword   aob_verify_phone_number_on_transfer_number_page  ${num}
    [Return]  ${num}
    should be true  ${result}

I verify temporary number "${linkText}" on activation page
    [Documentation]   This function will verify if temporary number link is available on Activation page or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_activation_verify_temporary_link  ${linkText}
    should be true  ${result}

I check icon of "${Text}" is present on page
    [Documentation]   This function will check if icon is present on page or not
    ...   result: status of function True or False
    ${result}=      run keyword   aob_activate_icon_visiblity  ${Text}
    should be true  ${result}

I click on tab "${tab}" on aob page
    [Documentation]   This function will click on aob tab
    ...   result: status of function True or False
    ${result}=      run keyword   aob_tab_click  ${tab}
    should be true  ${result}

I get column "${columnName}" values from "${grid}" grid
    [Documentation]   This keyword will fetch first available number from the user page
    ...   button: Name of button
    ...   result: status of function True or False
    ${result}=      run keyword   get_dgrid_values   ${columnName}   ${grid}
    [Return]  5
    should be true  ${result}

I check for currency abbreviations in add user type page
    [Documentation]   This keyword will check the currency abbreviations on add user type page
    ...   Example: USD, AUD
    ...   result: status of function True or False
    [Arguments]  ${currency_info_list}
    ${result}=      run keyword  check_currency_abbreviations   ${currency_info_list}
    should be true  ${result}

I select "${option}" option on call handling summary page
    [Documentation]   This keyword will click on selected option on call handling summary page
    ...   option: Name of option which need to click on call handling summary page
    ...   result: status of function True or False
    ${result}=      run keyword   select_option_on_call_handling_summary_page   ${option}
    should be true  ${result}

I configure business hour in call handling page
    [Documentation]   This keyword will click on selected option on call handling summary page
    ...   option: Name of option which need to click on call handling summary page
    ...   result: status of function True or False
    [Arguments]  &{dict}
    ${result}=      run keyword   aob_ch_setup_business_hour   &{dict}
    should be true  ${result}

I configure rings in operator sections
    [Documentation]   This function will setup rings in operator page and clear the ring based on the flag pass from the dictionary
    ...   option: Name of option which need to click on call handling summary page
    ...   result: status of function True or False
    [Arguments]  &{dict}
    ${result}=      run keyword   aob_ch_setup_operator_rings   &{dict}
    should be true  ${result}

I delete first transfer number entry
    [Documentation]   This function will delete the entry from Transfer number page
    ...   result: status of function True or False
    ${result}=      run keyword   aob_delete_transfer_number_entry
    should be true  ${result}

I check number "${num}" is present on page
    [Documentation]   This keyword will check number is present on transfer number page
    ...   result: status of function True or False
    ${result}    ${num}=      run keyword   aob_verify_phone_number_on_transfer_number_page  ${num}
    [Return]  ${result}
    should not be true  ${result}

I add user with "${extn}" as operator
    [Documentation]   This keyword will add user as an operator on call handling summary page
    ...   extn: Extension of the user which need to be added as operator on call handling summary page
    ...   result: status of function True or False
    ${result}=      run keyword  add_user_as_an_operator    ${extn}
    should be true  ${result}

I add user with "${extn}" for live answer
    [Documentation]   This keyword will add user for live answer on call handling summary page
    ...   extn: Extension of the user which need to be added as operator on call handling summary page
    ...   result: status of function True or False
    ${result}=      run keyword  add_user_as_an_operator    ${extn}
    should be true  ${result}

I add user with "${extn}" for Take a message
    [Documentation]   This keyword will add user for live answer on call handling summary page
    ...   extn: Extension of the user which need to be added as operator on call handling summary page
    ...   result: status of function True or False
    ${result}=      run keyword  add_user_as_an_operator    ${extn}
    should be true  ${result}

I verify tab "${tab}" is opened
    [Documentation]   This keyword will chech if perticula tab is opened or not
    ...   tab: name of tab in ch page
    ...   result: status of function True or False
    ${result}=      run keyword  aob_check_ch_tab_open    ${tab}
    should be true  ${result}

I fetch selected number from call handling page
    [Documentation]   This keyword will chech if perticula tab is opened or not
    ...   tab: name of tab in ch page
    ...   result: status of function True or False
    ${result}=      run keyword  aob_get_number_from_ch_page
    [Return]  ${result}

I select the user bundle type "${type}"
    ${result}=      run keyword   aob_select_bundle_type   ${type}
    [Return]  ${result}
    #should be true    ${result}

I add "${type}" bundle
    ${result}=      run keyword   aob_add_user_bundle   ${type}
    should be true    ${result}

I press confirm if required
    run keyword   add_user_confirm_button

I open a user for edit "${name:[^"]+}"
    ${result}=      run keyword   aob_select_user   ${name}
    should be true    ${result}

I verify number "${number}"
    ${result}=      run keyword   aob check user number   ${number}
    should be true    ${result}

I change number to "${index}"
    ${result}  ${number}=      run keyword    aob_change_user_number    ${index}
    [Return]  ${number}
    should be true    ${result}

I find user bundle type "${name:[^"]+}"
    ${result}   ${bundle_type}=      run keyword   aob_find_user_bundle_type   ${name}
    [Return]  ${bundle_type}
    should be true    ${result}

I Navigate To Location Activation Page
    ${result}=      run keyword   aob_navigateto_locationactivation
    should be true    ${result}

I verify activate now selection
    ${result}=      run keyword   aob_verify_activation
    should be true    ${result}

I Check Get Help Link
    ${result}=      run keyword   aob_activation_gethelp_link
    should be true    ${result}

I check the bundle user count
    ${result}=      run keyword   verify_bundle_user_counter
    should be true    ${result}

I verify location checkmark
    ${result}=      run keyword   verify_location_checkmark
    should be true    ${result}

I click users continue button
    ${result}=      run keyword   click_users_continue_button
    should be true    ${result}

I verify welcome page checkmark
    ${result}=      run keyword     verify_welcome_checkmark
    should be true    ${result}

I check if mitel easy setup link disabled
    ${result}=      run keyword   aob_check_aob_link
    should not be true  ${result}

I click Update Call Handling button
    [Documentation]   This keyword will click the Update Call Handling button
    run keyword    aob_click_and_wait_element  aob_update_save_default_button

I click add button
    [Documentation]  This keyword will click on Add button in AOB page.
    ...   result: status of function True or False
    ${result}=      run keyword   aob_add_button
    should be true  ${result}

I click button with Add text
    [Documentation]  This keyword will click the button with Add text in AOB page.
    run keyword    aob_click_and_wait_element  aob_add_text_button

I click button with Save text
    [Documentation]  This keyword will click on button with Save text in AOB page.
    run keyword    aob_click_and_wait_element  aob_save_text_button

I click deepblue Save button
    [Documentation]  This keyword will click on button with Save text in AOB page.
    run keyword    aob_click_and_wait_element  aob_save_text_deepblue_button

I click primary Save button
    [Documentation]  This keyword will click on button with Save text in AOB page.
    run keyword    aob_click_and_wait_element  aob_save_text_primary_button

I click save inner button  #shadow root
    [Documentation]  This keyword will click on Save button in AOB page. (This button is in shadow root, function may be modified in future)
    ...   result: status of function True or False
    ${result}=      run keyword   aob_saveinner_button
    should be true  ${result}

I verify AOB message "${message}"
    [Documentation]   This keyword will verify the message is displayed in the page
    ...   message: message to verify
    ...   result: status of function True or False
    ${result}=   run keyword   aob_verify_message_displayed   ${message}
    should be true    ${result}

I verify Add Business Hours widgets
    [Documentation]   This keyword will verify if the all the widgets exist in Add Business Hours Screen
    ${result}=      run keyword   aob_verify_add_business_hours_widgets
    should be true    ${result}

I verify Add Business Hours widgets initial state
    [Documentation]   This keyword will verify if the all the widgets exist in Add Business Hours Screen
    ${result}=      run keyword   aob_verify_add_business_hours_widgets_reset
    should be true    ${result}

I remove All Business Hours
    [Documentation]   This keyword will remove all the business hours
    ${result}=   run keyword   aob_remove_business_hours
    should be true    ${result}

I Add Multiple Business Hours
    [Documentation]   This keyword will add multiple business hours
    ${result}=   run keyword   aob_add_multiple_business_hours
    should be true    ${result}

I Add Single Business Hours
    [Documentation]   This keyword will add a single business hours
    ${result}=   run keyword   aob_add_single_business_hours
    should be true    ${result}

I verify Business Hours At all times
    [Documentation]   This keyword will verify Business Hours is "At all times"
    ${result}=   run keyword   aob_verify_business_hours_all_times
    should be true    ${result}

I verify Business Hours Count matches "${count}"
    [Documentation]   This keyword will verify Business Hours matches the parameter
    ${result}=   run keyword   aob_verify_business_hours_count_matches   ${count}
    should be true    ${result}

I get number of elements "${element}"
    [Documentation]   This keyword will fetch the number of elements present
    ...   button: Name of element to find
    ...   result: count of elements found
    ${num}=      run keyword   aob_get_elements_count   ${element}
    [Return]    ${num}

I click Business Hours section
    [Documentation]   This keyword will click the Update Call Handling button
    run keyword    aob_click_and_wait_element  aob_business_hour_selection

I unselect the days in Add Business Hours screen
    [Documentation]   This keyword will unselect the days in the add business hours screen
    ${result}=   run keyword   aob_unselect_add_business_hours
    should be true    ${result}
