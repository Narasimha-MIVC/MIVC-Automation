*** Settings ***
Documentation     Keywords supported for BOSS portal
...               dev- Kenash, Rahul Doshi, Vasuja
...               Comments:

Library    Collections
Resource   AOBKeywords.robot
Resource   VCFEKeywords.robot
Resource   BCAKeywords.robot
Resource   ECCKeywords.robot
Resource   AddonFeatureKeywords.robot
Resource   UserKeywords.robot
Resource   PhoneNumberKeywords.robot
Resource   DominatorKeywords.robot
Resource   NavigationKeywords.robot

*** Keywords ***
I login to ${url} with ${username} and ${password}
    [Documentation]  This keyword logs into BOSS portal
    ...  URL: portal url, username: login username, password: user password
    ...  return: None
	&{loginCredentials}=    Create Dictionary      username=${username}       password=${password}       URL=${url}
	Run Keyword       Client Login       &{loginCredentials}

I login using separate tab
    [Arguments]  ${loginInfo}
    [Documentation]  This keyword opens a new tab on browser and logs in using
    ...  loginInfo: the dictionary will have
    ...  return: None
    Run Keyword    Login Using New Tab    ${loginInfo}

I get build
    Given I open login page with ${URL}
    and I check the build

I accept agreement
    Accept Agreement

I verify tabs exist
    [Arguments]    @{tab_list}
    ${result}=    Run Keyword    Verify Tabs Exist    @{tab_list}
    should be True    ${result}

I click on user name and go to password change page "${name:[^"]+}"
    ${result} =  Run Keyword      change profile password from user page     ${name}
    Should be true    ${result}

I go to change password page for user "${name:[^"]+}"
    Run Keyword       Right Click   ${name}

I change password to ${password}
    &{new_password}=    Create Dictionary      newpassword=${password}
	Run Keyword       Change Password       &{new_password}

I update password to ${password} from ${oldpassword}
    &{new_password}=    Create Dictionary      newpassword=${password}  oldpassword=${oldpassword}
	Run Keyword       Update Password       &{new_password}

I open login page with ${url}
    Run Keyword      Open Url     ${url}

I do right click and go to close user page for ${email} with user "${name:[^"]+}"
    &{user_details}=    Create Dictionary      email=${email}  name=${name}
    run keyword     Close User  &{user_details}

I do right click and do a close user cancel for ${email} with user "${name:[^"]+}"
    &{user_details}=    Create Dictionary      email=${email}  name=${name}  option=cancel
    run keyword     Close User  &{user_details}

#########
I read email for ${email} and change password to ${password}
    ${result}=  run keyword  reset password via email    ${email}   ${password}
    should be true  ${result}

I close open order
    ${result}=   run keyword  close_open_order
    should be true  ${result}

I close the location
    ${result}=   run keyword     close_location
    should be true  ${result}

I update the location
    [Arguments]  &{geolocationinfo}
    ${result}=  update geo location     &{geolocationinfo}
    [Return]  ${result}

I check emails for ${email} for ${sender}
    run keyword  check_email    ${email}    ${sender}

##########
I delete user ${email} as user "${name:[^"]+}"
  &{closeuser}=    Create Dictionary      email=${email}       name=${name}
    ${result} =    run keyword     close user    &{closeuser}
    Should be true    ${result}

I click on Reset Password Link
    Run Keyword    reset password from home page

I click on Reset Password Link and enter email address ${email} and click submit
    Run Keyword     reset password from home page   ${email}

In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    &{D2loginCredentials}=    Create Dictionary      username=${D2User}       password=${D2Password}    IP=${D2IP}       URL=${url}
	Run Keyword      Director Client Login       &{D2loginCredentials}

In D2 I verify location "${d2location:[^"]+}" is set as site for "${d2account:[^"]+}"
    &{D2location}=    Create Dictionary    exp_location=${d2location}    account=${d2account}
    ${result}=   Run Keyword    Director Verify Tenant Location    &{D2location}
    Should be true    ${result}

I am in "${curpage:[^"]+}" with "${curuser:[^"]+}" account
    &{curPageDescription}=    Create Dictionary       page=${curPage}      content=${curuser}
    ${result} =      Verify Page        ${curPageDescription}
    Should be true      ${result}

I switch to Primary Partitions page
    Run keyword  Switch page primary partition

I switch to "${myNewPage:[^"]+}" page
	&{pageSwitch}=    Create Dictionary       page=${myNewPage}
	Run Keyword       Switch Page      &{pageSwitch}

I verify "${myPage:[^"]+}" contains "${myPageContent:[^"]+}"
	&{pageDescription}=    Create Dictionary       page=${myPage}      exp_content=${myPageContent}
	${result} =      Verify Page        &{pageDescription}
	Should be true      ${result}

I verify "${myPage:[^"]+}" does not contain "${myPageContent:[^"]+}"
	&{pageDescription}=    Create Dictionary       page=${myPage}      exp_content=${myPageContent}
	${result} =      verify_page_does_not_contain        &{pageDescription}
	Should be true      ${result}

I verify location "${loc_name:[^"]+}" with "${exp_state:[^"]+}" state
    &{contract_info}=    Create Dictionary       loc_name=${loc_name}    exp_state=${exp_state}
    ${result} =    Verify loc Status    &{contract_info}
    Should be true      ${result}

I switch to account ${newacc} with ${seloption} option
    &{accSwitch}=    Create Dictionary       newacc=${newacc}    seloption=${seloption}
	Run Keyword       Switch Account      &{accSwitch}

I search for "${search_str:[^"]+}"
    &{searchstring}=    Create Dictionary       search_str=${search_str}
    Run Keyword     Search User     ${search_str}

I switch to "${switchlink:[^"]+}" in partition ${Partition}
     &{switchlink}=      Create Dictionary       switch_link=${switchlink}    partition=${Partition}
     Run Keyword       Switch Link In Partition     &{switchlink}

I add contract
    [Arguments]    &{contractinfo}
    ${result}=   Add Contract    &{contractinfo}
    Should be true    ${result}

I add account
    [Arguments]    &{accountinfo}
    ${result}=   Add Account    &{accountinfo}
    Should be true    ${result}

I add account using connect
    [Arguments]    &{accountinfo}
    ${result}=   Add Account using Connect    &{accountinfo}
    Should be true    ${result}

I retrieve account details
    [Arguments]  ${params}
    ${status}=  run keyword  get account details  ${params}
    should be true  ${status}

I click on "${link_text:[^"]+}" link in "${grid:[^"]+}"
    &{gridinfo}=    Create Dictionary    grid=${grid}    link=${link_text}
    Run Keyword      click link in grid    &{gridinfo}

I verify in "${grid:[^"]+}" grid if value of "${primary:}[^"]+}" in "${column_name:[^"]+}" is "${exp_val:[^"]+}"
    Run Keyword    Verify grid value

I verify contract with ${contract_type} is "${contract_state:[^"]+}" state
     &{contractinfo}=    Create Dictionary    contract_type=${contract_type}    exp_contract_state=${contract_state}
     ${result}=    Verify Contract    &{contractinfo}
     Should be true   ${result}

I verify grid contains "${gridvalue:[^"]+}" value
     &{Gridinfo}=      Create Dictionary       gridvalue=${gridvalue}
     ${result}=     Verify Grid Value     &{Gridinfo}
     should be true    ${result}

I move to "${tabname:[^"]+}" tab
    &{tabName}=    Create Dictionary       tab_name=${tabname}
    Run Keyword       move_to_tab   &{tabName}

I set the default location as site
    Run Keyword       set location as site

I add user
    [Arguments]    &{userinfo}
    Log    "Adding user ${userinfo}"
    ${phone_num}  ${extn}  ${status}=      Add User    &{userinfo}
    Log    "${phone_num} ${extn} ${status}"
    Should be true    ${status}
    [Return]      ${phone_num}    ${extn}   ${status}

I add PhoneNumber
    [Arguments]    &{PhoneNumberInfo}
    Run Keyword    add phonenumber    &{PhoneNumberInfo}

I add partition
    [Arguments]    &{PartitionInfo}
    Run Keyword    Add Partition  &{PartitionInfo}

I verify that Partition is set as Primary
    [Arguments]    &{PartitionInfo}
     ${result}=        Verify Partition      &{PartitionInfo}
     Should be true    ${result}

I verify tab exist
    [Arguments]    @{tab_list}
    ${result}=    Verify Tab Exist   @{tab_list}
    Should be true    ${result}

I verify that User exist in user table
     [Arguments]    &{userinfo}
     Log    "Verifying user ${userinfo}"
     ${result}=        Verify User      &{userinfo}
     Should be true    ${result}

I verify profile updated in service table
    [Arguments]    &{userinfo}
	${result}=   Verify User Profile    &{userinfo}
	Should be true    ${result}

I select "${option:[^"]+}" in "${element:[^"]+}"
    &{options}=    Create Dictionary    option=${option}    element=${element}
    Run Keyword    Select Option    &{options}

I set instance to ${instance_name}
    &{instanceInfo}=    Create Dictionary       instance_name=${instance_name}
	Run Keyword       Add Instance      &{instanceInfo}

I confirm the contract with instance "${instance:[^"]+}" and location "${location:[^"]+}"
    &{contractinfo}=    Create Dictionary       instance=${instance}    location=${location}
	${order_number}=   Run Keyword       Confirm Contract      &{contractInfo}
    [Return]      ${order_number}

I verify contract "${account_name:[^"]+}" with "${exp_state:[^"]+}" state
    &{contract_info}=    Create Dictionary       account_name=${account_name}    exp_state=${exp_state}
    Run Keyword    Verify Contract State    &{contract_info}

I verify account
    [Arguments]  ${params}
    ${result}=  run keyword  Verify Account  ${params}
    should be true  ${result}

I set PhoneNumber state
    [Arguments]    &{phoneinfo}
    Run Keyword    Update Phone State    &{phoneinfo}

I verify PhoneNumber state
    [Arguments]    &{phoneinfo}
    ${result}=   Verify Phone State    &{phoneinfo}
    Should be true    ${result}

I create invoice group
    [Arguments]    &{InvoicesPaymentsinfo}
    Run Keyword    create invoice group   &{InvoicesPaymentsinfo}

I verify that Invoice group is associated with location
    [Arguments]    &{hginfo}
    ${result}=    Run Keyword       verify invoice group location    &{hginfo}
    Should be true    ${result}

I log off
   Run Keyword    log off

Close The Browsers
	Run Keyword     Close The Browser

I create geographic location
   [Arguments]    &{geolocationinfo}
   Run Keyword       add geo location    &{geolocationinfo}

I add location ${params} for ${user} through personal registration
   ${result} =  Run Keyword      add_geo_loc_using_personal_reg  ${user}  &{params}
    Should be true    ${result}

I add prog button
    [Arguments]    &{pbinfo}
    Log    "Adding button ${pbinfo}"
    Add Prog Button    &{pbinfo}

I add prog button bca
    [Arguments]    &{pbinfo}
    Log    "Adding button ${pbinfo}"
    Add Prog Button bca    &{pbinfo}

I add sca prog button 
    [Arguments]    &{pbinfo}
    Log    "Adding button ${pbinfo}"
    Add Prog Button sca    &{pbinfo}

I switch to prog button page
   [Arguments]    ${email}
   ${result} =  Run Keyword      switch prog button  ${email}
I remove prog button
    [Arguments]    &{pbinfo}
    Log    "Adding button ${pbinfo}"
    Remove Prog Button    &{pbinfo}

I check the build
    Run Keyword     Get Build

I update service status
    [Arguments]  &{serviceInfo}
    run keyword  update service status  &{serviceInfo}

I check for alert
   run keyword     check alert

I go to switch user page
    Run Keyword     switch_page_switch_account

I go to personal information page
    ${result} =    run keyword     switch_page_personal_information
    Should be true     ${result}

I delete contract "${name:[^"]+}"
    log  ${name}
    Run Keyword    Delete contract   ${name}

I verify contract "${name:[^"]+}" is deleted
    ${result} =     Run Keyword    Verify contract delete    ${name}
    Should be true    ${result}

I change password from home page
    [Arguments]  &{email}
    ${result}=  run keyword  reset password via email    &{email}
    should be true  ${result}

I close open order for location ${Location}
    ${result}=   run keyword  close_open_order    ${Location}
    should be true  ${result}

I close the location ${Location} requested by "${name:[^"]+}"
    ${result}=   run keyword     close_location    ${Location}    ${name}
    should be true  ${result}

I check for error
    ${result}=  run keyword  check_for_error
    #should be true  ${result}

I add transfer request
    [Arguments]  &{phone}
    ${result}=  run keyword  add_transfer_request    &{phone}
    should be true  ${result}

I verify the transfer request for ${phone}
    ${result}=  run keyword  verify_transfer_request    ${phone}
    should be true  ${result}

I add LNP service
    [Arguments]  &{LNP_service}
    ${order_number}=  run keyword  add_LNP_service      &{LNP_service}
    [Return]    ${order_number}

I activate LNP service for ${order_id} and ${phone}
    ${result}=  run keyword  activate_service   ${order_id}   ${phone}
    should be true   ${result}

I verify "${message:[^"]+}" is displayed on screen
    [Documentation]  This keyword will verfify the message occurs on screen.
    ...   result: status of function True or False
    &{errormsg}=    Create Dictionary    error_message=${message}
    ${result}=   Run Keyword   verify message displayed    &{errormsg}
    should be true  ${result}

I verify "${message:[^"]+}" is not displayed on screen
    &{errormsg}=    Create Dictionary    error_message=${message}
    ${result}=   Run Keyword   verify message displayed    &{errormsg}
    should not be true  ${result}

I verify option "${option}" in Find Me settings
    ${result}=   Run Keyword  verify findme   ${option}
    should be true  ${result}

I click on cancel button
    run keyword  click_cancel

I refresh browser page
    run keyword  refresh_browser

I create User Group
    [Arguments]    &{UserGroupInfo}
    Run Keyword    add usergroup  &{UserGroupInfo}

I block
    Run Keyword     block here

I configure phone number "${label}" and "${phone}" with number "${num}" in call rerouting main settings
    Run Keyword     config phone numbers callrouting    ${label}    ${phone}    ${num}

I configure simultaneous ring "${label}" for number "${num}"
    run keyword     config sim ring     ${label}    ${num}

I configure find me "${label}" for number "${num}"
    run keyword     config find me     ${label}    ${num}

I configure find me "${label}" for external did "${num}"
    run keyword     config oae did    ${label}    ${num}
#I assign User "${userMailid:[^"]+}" in user group "${userGroupName:[^"]+}"
    #&{usergroup}=    create dictionary  usermailid=${userMailid}    userGroupName=${userGroupName}
    #Run Keyword    assign usergroup      &{usergroup}

I assign User ${userMailid} in user group ${userGroupName}
    &{usergroup}=    create dictionary  usermailid=${userMailid}    userGroupName=${userGroupName}
    Run Keyword    assign usergroup      &{usergroup}

In D2 I verify user group ${d2usergroup} is set for ${newacc}
    &{usergroup}=    Create Dictionary    exp_user_group=${d2usergroup}    newacc=${newacc}
    ${result}=   Run Keyword    director verify user groups    &{usergroup}
    Should be true    ${result}

I delete user group ${usergroup_name}
    ${result}=      run keyword  delete_usergroup  ${usergroup_name}
    should be true  ${result}

I provision initial order
    ${result}=      run keyword   provision_initial_order
    should be true    ${result}

I activate all service
    ${result}=      run keyword   activate_all_service
    should be true    ${result}

I close all order
    ${result}=      run keyword   close_all_order
    should be true    ${result}

I close contract
    [Arguments]  ${contract}  ${req_by}=${None}
    ${result}=      run keyword   close_contract  ${contract}  ${req_by}
    should be true    ${result}

I verify turnup service
    [Documentation]   This keyword will verify the presence of turnup service
    [Arguments]  &{global_user}
    ${result}=  Run Keyword     verify_turnup_service     &{global_user}
    Should be true   ${result}

I verify provisioning details of service
    [Documentation]   This keyword will verify the provisioning details of the Global TN service
    [Arguments]   &{global_user}
    ${result}=  Run Keyword     verify_provisioning_details     &{global_user}
    Should be true   ${result}

I close global user service
    [Documentation]   This keyword will close the service
    [Arguments]   &{global_user}
    ${result}=  Run Keyword     close_service     &{global_user}
    Should be true   ${result}

I void global user service
    [Documentation]   This keyword will void the global user service
    [Arguments]   &{global_user}
    ${serviceTn}    ${result}=  run keyword    void_global_user_service    &{global_user}
    Should be true   ${result}
    [Return]      ${serviceTn}

I verify status of ${serviceTn}
    [Documentation]   This keyword will verify the status of Tn
    ${result}=  run keyword    verify_tn_status   ${serviceTn}    &{globaluser_void}
    Should be true   ${result}

I add a global country to smr instance
    [Documentation]   This keyword will verify adding a global country's access numbers to an SMR instance
    [Arguments]   &{Instances}
    ${result}=  Run Keyword  add_global_country_to_smr_instance     &{Instances}
    Should be true   ${result}

I update a global country of smr instance
    [Documentation]   This keyword will verify updating a global country's access numbers of an SMR instance
    [Arguments]   &{Instances}
    ${result}=  Run Keyword  update_global_country_of_smr_instance     &{Instances}
    Should be true   ${result}

I verify existence of show configured link for global smr
    [Documentation]   This keyword will verify existence of 'Show Configured' link for an SMR instance where global country(ies) have been set up
    [Arguments]   &{Instances}
    ${result}=  Run Keyword  verify_existence_show_configured_link     &{Instances}
    Should be true   ${result}

# Personal Contacts Keywords
I add personal contact required fail
    ${result}=  Run Keyword    add_personal_contact_required_fail
    Should be True    ${result}

I add personal contact success
    [Arguments]    &{Contact}
    ${result}=  Run Keyword    add_personal_contact_success    &{Contact}
    Should be True    ${result}

I verify personal contact update button
    [Arguments]    &{Contact}
    ${result}=  Run Keyword    verify_grid_toolbar_update_state     &{Contact}
    Should be true    ${result}

I delete personal contact
    [Arguments]    &{Contact}
    ${result}=  Run Keyword    delete_personal_contact    &{Contact}
    Should be True    ${result}

#Personal Information Keywords
I switch to ${tabName} tab
    ${result}=  Run Keyword    switch_tab  ${tabName}
    Should be True    ${result}

I verify Contact tab
    ${result}=  Run Keyword    verify_contact_tab
    Should be True    ${result}

I verify Roles and Permissions tab
    ${result}=  Run Keyword    verify_roles_permissions_tab
    Should be True    ${result}

I verify Notification Preferences tab
    ${result}=  Run Keyword    verify_notification_preferences_tab
    Should be True    ${result}

I add role ${role}
    ${result}=  Run Keyword    add_role   ${role}
    Should be True    ${result}

I change the location for role ${role} to ${location}
    ${result}=  Run Keyword    change_role_location   ${role}   ${location}
    Should be True    ${result}

I remove the location for role ${role}
    ${result}=  Run Keyword    remove_role_location  ${role}
    Should be True    ${result}

I remove role ${role}
    ${result}=  Run Keyword    delete_role  ${role}
    Should be True    ${result}

I change the first name
    ${result}=  Run Keyword    change_first_name
    Should be True    ${result}

I change the user ${field} to ${value} and ${action}
    ${result}=  Run Keyword    change_user_data   ${field}   ${value}   ${action}
    Should be True    ${result}

I edit personal contact
    [Arguments]    &{Contact}
    ${result}=  Run Keyword    edit_personal_contact    &{Contact}
    Should be True    ${result}

I verify UserFields state
    [Arguments]    ${username}
    ${result}=   Verify User Fields    ${username}
    Should be true    ${result}

I verify UsrField state
    [Arguments]    ${username1}
    ${result}=   Verify Usr Field    ${username1}
    Should be true    ${result}

I set PhoneNumberFields state
    [Arguments]    &{phoneinfo}
    Run Keyword    Update Phone State Fields   &{phoneinfo}


I add mobile number ${num} for ${email}
    &{ninfo}=    Create Dictionary       num=${num}    email=${email}
  	Run Keyword       add mobile number to user      &{ninfo}

I remove mobile number for user ${email}
    &{ninfo}=    Create Dictionary       email=${email}
    Run Keyword       remove mobile number for user      &{ninfo}

I add on hold music
    [Arguments]    &{on_hold_music_Info}
    ${result}=  Run Keyword    add on hold music  &{on_hold_music_Info}
    Should be true   ${result}

I delete on hold music ${moh_name}
    ${result}=      run keyword  delete on hold music  ${moh_name}
    should be true  ${result}

I rename on hold music
    [Arguments]    &{on_hold_music_Info}
    ${result}=  Run Keyword    rename hold music  &{on_hold_music_Info}
    Should be true   ${result}

In D2 I verify music on hold "${d2moh:[^"]+}" is set for ${newacc}
    &{D2moh}=    Create Dictionary    exp_mohdec=${d2moh}    newacc=${newacc}
    ${result}=   Run Keyword    director verify moh    &{D2moh}
    Should be true    ${result}

I go to "${tab}" -> "${link}"
    [Documentation]   This keyword will go to a 'tab' and then goes to a 'link'
    &{options}=    Create Dictionary    tab=${tab}    link=${link}
    run keyword     Click Tab Link      &{options}

I click on "${button}" button/link
    [Documentation]   This keyword clicks on a given link or button. Please use xpath.
    run keyword    Click Button Link  ${button}

I verify "${button}" contains "${text}" text
    [Documentation]   This keyword checks if a 'button' contains a 'text'. Please use xpath.
    ${result}=   Run Keyword    verify_text_similar    ${text}   ${button}
    Should be true    ${result}

I stop impersonating
    [Documentation]   This keyword clicks on 'stop impersonating' link in the menu.
    ${result}=   run keyword     stop_impersonating
    should be true      ${result}

I right click a user with extension "${extension}"
    [Documentation]   This keyword right clicks a user with a valid extension.
    ${result}=  run keyword     right click users   ${extension}
    should be true      ${result}

I perform right click on a "${option}" for user with email "${buisness_email}"
    [Documentation]   This keyword right clicks on a user with a valid email id.
    &{user_inf}=    Create Dictionary    option=${option}    email=${buisness_email}
    ${result}=  run keyword     right click users with option   &{user_inf}
    should be true      ${result}


I enter "${text}" in "${element}" textbox
    [Documentation]   This keyword enters a text in a textbox.
    &{options}=    Create Dictionary    text=${text}    element=${element}
    ${result}=     run keyword    Enter Text   &{options}
    should be true      ${result}

# Profile Grid
I login to Cosmo Account and go to Primary Partition page
    [Documentation]  This keyword will help user to login to portal.
    ...   Variable name: URL1- URL of Boss Portal
    ...   bossUserName: Staff User
    ...   bossPassword: Staff User Password
    ...   ProfileGridAccount: The account name to be used for the profile grid tests
    ...   AccWithoutLogin: Option to be choose while switching account
    ...   Note: has to be placed in EnvVariable.robot file
    I login to ${URL} with ${bossUsername} and ${bossPassword}
    I switch to "switch_account" page
    I switch to account ${ProfileGridAccount} with ${AccWithoutLogin} option
    I switch to "primary_partition" page

I reassign a profile with a TN
    [Documentation]  A keyword to re-assign a profile with a TN
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     reassign_user_profile    &{user_profile}
    Should be true  ${result}

I read a profile in the profile grid
    [Documentation]  This keyword reads a profile selected in the profile list using the email address
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     read_profile_in_profile_grid  ProfileDataGridCanvas   ProfileGridHeaderEmailSearch    &{user_profile}
    [Return]    ${result}

I verify a profile is updated
    [Documentation]  A keyword to verify an updated profile
    [Arguments]   ${created_email}  &{created_profile}
    ${result}=  Run Keyword     verify_profile_updated_in_profile_grid  ProfileDataGridCanvas   ProfileGridHeaderEmailSearch  ${created_email}  &{created_profile}
    Should be true  ${result}

I verify a user profile is updated
    [Documentation]  A keyword to verify an updated profile
    [Arguments]   ${created_email}  &{created_profile}
    I switch to "users" page
    ${result}=  Run Keyword     verify_updated_profile_in_users_grid  UsersDataGridCanvas   email_search  ${created_email}  &{created_profile}
    Should be true  ${result}

I add a profile with a TN
    [Documentation]  This keyword will create a profile with a TN
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     add_user_profile    &{user_profile}
    Should be true  ${result}

I populate a new profile to add
    [Documentation]  This keyword will open and populate the add profile dialog
    [Arguments]  &{user_profile}
    Run Keyword     populate_user_profile    &{user_profile}

I add a profile with an auto assigned extension
    [Documentation]  This keyword will create a profile with an auto assigned extension
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     add_user_profile    &{user_profile}
    Should be true  ${result}

I verify the profile is added to the users table
    [Documentation]  This keyword will verify the suppiled user profile can be found in the users list
    [Arguments]  &{user_profile}
    I switch to "users" page
    ${result}=  Run Keyword     verify_profile_in_users_grid    UsersDataGridCanvas     email_search    &{user_profile}
    Should be true  ${result}

I verify the profile is in the profile grid
    [Documentation]  This keyword will verify the suppiled user profile can be found in the profile list
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     verify_profile_in_profile_grid      ProfileDataGridCanvas   ProfileGridHeaderEmailSearch    &{user_profile}
    Should be true  ${result}

I enter an invalid profile extension
    [Documentation]  This keyword will enter an extension number into the add profile dialog
    [Arguments]  ${extension}
    Run Keyword     enter_profile_extension    ${extension}

I verify the profile extension error message
     [Documentation]  This keyword will verify the error string when entering the extension num of a new profile
     [Arguments]  ${expectedError}
     ${result}=  Run Keyword     verify_extension_error    ${expectedError}

I cancel out of the add profile wizard
    [Documentation]  This keyword will cancel and close the add profile wizard dialog
     Run Keyword     cancel_add_profile

I select one profile in the profile grid
    [Documentation]  This keyword select 1 profile in the profile list using the email address
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     select_profile_in_profile_grid  ProfileDataGridCanvas   ProfileGridHeaderEmailSearch    &{user_profile}

I select multiple profiles in the profile grid
    [Documentation]  This keyword select multiple profile in the profile list using the email address
    [Arguments]     @{profile_list}
    log to console  The profile list is @{profile_list}
    ${result}=  run keyword     select_multiple_profiles_in_profile_grid    ProfileDataGridCanvas   ProfileGridHeaderEmailSearch    @{profile_list}

I click the "${buttonId:[^"]+}" button
    log to console  The button Id is ${buttonId}
    Run Keyword    click_button      ${buttonId}

I change the phone pin and save it
    [Documentation]  This keyword will change the phone pin to the specified value and press the OK button
    [Arguments]  ${pin}
    ${result}=  Run Keyword     change_phone_pin_and_save   ${pin}
    Should be true  ${result}

I verify the phone pin change was successful
    [Documentation]  This keyword will verify that the changing of the phone pin is successful
    [Arguments]  ${pin}
    ${result}=  Run Keyword     verify_phone_pin_change   ${pin}
    Should be true  ${result}

I verify the phone pin change was not successful
    [Documentation]  This keyword will verify that the changing of the phone pin is not successful
    [Arguments]  ${message}
    ${result}=  Run Keyword     verify_phone_pin_change_failed  ${message}
    Should be true  ${result}

I input "${text:[^"]+}" in "${input_id:[^"]+}"
    [Documentation]   This keyword will input ${text} to ${input_id}
     &{input_info}=   Create Dictionary       text=${text}    input_id=${input_id}
     Run Keyword      input_text_in_input_field       &{input_info}

I click element by xpath "${xpath:[^"]+}"
     [Documentation]   This keyword will click ${xpath}
     &{input_info}=    Create Dictionary      element_xpath=${xpath}
	 Run Keyword       click_element_by_xpath       &{input_info}


I do select "${option:[^"]+}" in "${select_id:[^"]+}"
     [Documentation]   This keyword will selecg ${option} by ${select_id}
     &{input_info}=   Create Dictionary       option=${option}    select_id=${select_id}
     Run Keyword      select_option_in_select       &{input_info}

I sleep "${sleep_secconds:[^"]+}" seconds
     [Documentation]   This keyword will sleep ${sleep_secconds}
     &{input_info}=   Create Dictionary       sleep_secconds=${sleep_secconds}
     Run Keyword      sleep_in_seconds       &{input_info}

I click Users in Phone System tab
    Run Keyword    click_on_phone_system_users

I right click on "${link_text:[^"]+}" link in "${grid:[^"]+}" and select "${context_item:[^"]+}"
    &{gridinfo}=    Create Dictionary    grid=${grid}    link=${link_text}      context_item=${context_item}
    Run Keyword     right click link in grid    &{gridinfo}

I select "${tab}" tab and wait for "${tabContent:[^"]+}"
    Run Keyword     select_tab      ${tab}  ${tabContent}

I check it says ${option}
    Run Keyword    check_it_says  ${option}

I adjust voicemail interaction form with extension "${extension}"
    Run Keyword  adjust_voicemail_interaction    ${extension}

I verify voicemail interaction form with extension "${extension}"
    Run Keyword  verify_voicemail_interaction    ${extension}

I open Call Routing for user ${user_email}
    [Documentation]   Select Call Routing option in Phone Settings for a user with given email address
    ${result}=  Run Keyword     select_call_routing_for_user    ${user_email}
    Should be true   ${result}

I open Configure Main Settings with Phone Numbers
    [Documentation]   Configure Main Settings by adding phone numbers.
    ${result}=  Run Keyword     configure_call_routing
    Should be true   ${result}

I Configure Call Forward After Ringing
    [Documentation]   Configure Call Forwarding
    ${result}=  Run Keyword     configure_call_forwarding
    Should be true   ${result}

I verify Call Forward is configured
    [Documentation]   Veirfy Call Forwarding is configured
    ${result}=  Run Keyword     call_forwarding_configured
    Should be true   ${result}

I unassign one profile
    Run Keyword     unassign_profile

I verify the profile is not in the profile grid
    [Documentation]  This keyword will verify the supplied user profile can not be found in the profile list
    [Arguments]  &{user_profile}
    ${result}=  Run Keyword     verify_profile_in_profile_grid      ProfileDataGridCanvas   ProfileGridHeaderEmailSearch    &{user_profile}
    should not be true  ${result}

I verify the profile is not in the users table
    [Documentation]  This keyword will verify the suppiled user profile can not be found in the users list
    [Arguments]  &{user_profile}
    I switch to "users" page
    ${result}=  Run Keyword     verify_profile_in_users_grid    UsersDataGridCanvas     email_search    &{user_profile}
    should not be true      ${result}

I verify a close order is created
    [Documentation]  This keyword will verify the a close order is created when a profile is unassigned
    [Arguments]         ${CloseorderID}                             &{user_profile}
    ${result}=  Run Keyword     verify_close_order_is_created       OrderDataGridCanvas     OrderOrderIDTextSearch              ${CloseorderID}                     &{user_profile}
    should be true      ${result}

I get the latest orderID
    [Documentation]  This keyword will the get the latest order ID in the order page
    [Return]        ${orderID}
    ${orderID}=         Run Keyword     orderID_of_latest_orders

I verify a service status is closed
    [Documentation]  This keyword will verify the services of a profile are closed
    [Arguments]  ${orderID}
    ${result}=  Run Keyword     verify_service_status_closed       ServicesDataGridCanvas     headerRow_OrderId      ${orderID}
    should be true      ${result}

I configure always forward to voicemail
    [Documentation]   Configure Call Forwarding
    ${result}=  Run Keyword     configure_always_forward_to_voicemail
    Should be true   ${result}

I verify always forward to voicemail is configured
    [Documentation]   Verify always forwarding is configured
    ${result}=  Run Keyword     always_forward_to_voicemail_configured
    Should be true   ${result}

I open Operations IP PBX Primary Partition
    run keyword   Open Operations IP PBX Primary Partition

I verify Profiles grid display
    ${result}=  run keyword   Verify Profiles Grid Display
    Should be true   ${result}

I select one profile ${product}
    &{product}=    Create Dictionary      product=${product}
    ${result}=  run keyword   Select one profile    &{product}
    Should be true   ${result}

I get first record from profile
    ${profileData}=  run keyword   Get first record from profile
    [Return]    ${profileData}

I click on ReAssign button
    ${result}=  run keyword   Click reassign button
    [Return]    ${result}

I verify reassign wizard is displayed
    ${result}=  run keyword   Verify reassign wizard display
    Should be true   ${result}

I verify error message ${error_message} when I enter extension ${extension_number}
    &{extension_validtion}=    Create Dictionary      errorMessage=${error_message}     extensionNumber=${extension_number}
	${result}=  Run Keyword       Validate reassigned extension       &{extension_validtion}
    Should be true   ${result}

I click checkbox of first entry by search text "${text}" with canvasId "${canvasId}" and searchColumnId "${searchColumnId}"
    &{searchInfo}=    Create Dictionary    text=${text}    canvasId=${canvasId}      searchColumnId=${searchColumnId}
    Run Keyword       Click checkbox of first entry by search       &{searchInfo}

I verify button "${button_xpath:[^"]+}" is enabled
    &{button_validtion}=    Create Dictionary      button_xpath=${button_xpath}     expect_status=True
	${result}=  Run Keyword       Validate button status       &{button_validtion}
    Should be true   ${result}


I verify button "${button_xpath:[^"]+}" is disabled
    &{button_validtion}=    Create Dictionary      button_xpath=${button_xpath}     expect_status=False
	${result}=  Run Keyword       Validate button status       &{button_validtion}
    Should be true   ${result}

I Configure Find Me Numbers
    [Documentation]   Configure Find Me numbers for Call Routing
    ${result}=  Run Keyword     configure_find_me_numbers
    Should be true   ${result}

I verify Find Me Numbers have been configured
    [Documentation]   To verify that Find Me numbers have been configured
    ${result}=  Run Keyword     find_me_numbers_configured

I click the Import button on the primary partitions profiles page
    I click the "PartitionProfilesDataGridImportButton" button

I verify the Import Profiles form is displayed
    I verify "ImportFormUploadForm" contains "The file must be in the standard format used by the Voice Provisioning team."

I specify the file to be uploaded and then press the Open button
    [Documentation]  This keyword will click the Browse button, specify the file to upload and press open
    [Arguments]     &{file_upload_info}
    ${result}=  Run Keyword     upload_specified_file   &{file_upload_info}
    Should be true  ${result}

I import the profiles into the preview view
    [Documentation]  This keyword will click the Preview button and return True if there are no errors on preview
    ${result}=  Run Keyword     preview_profile_import
    Should be true  ${result}

I import the previewed profiles
    [Documentation]  This keyword imports the profiles that are already in the preview window
    ${result}=  Run Keyword     import_previewed_profiles
    Should be true  ${result}

Read Profiles from File
    [Documentation]  This keyword will read the list of profile from the sepecified file
    [Arguments]     ${file_path}
    ${profiles}=  Run Keyword     read_profiles_from_import_file   ${file_path}
    log to console  ${profiles}
    [Return]    ${profiles}

I verify that the profiles are imported into the profiles grid
    [Documentation]  This keyword will look for each profile in the profile grid
    [Arguments]     @{profile_list}
    I switch to "primary_partition_profiles" page
    ${result}=  Run Keyword     verify_imported_profiles_in_profile_grid    ProfileDataGridCanvas   ProfileGridHeaderEmailSearch    @{profile_list}
    Should be true  ${result}

I verify that the new users are found in the users grid
    [Documentation]  This keyword will verify the profiles can be found in the users list
    [Arguments]  @{profile_list}
    I switch to "users" page
    ${result}=  Run Keyword     verify_imported_profile_in_users_grid    UsersDataGridCanvas     email_search    @{profile_list}
    Should be true  ${result}

I verify Extension-Only is shown @{ProfileExtension}
    ${result}=  run keyword   Verify number  @{ProfileExtension}
    Should be true   ${result}

I verify Extension-and-DID is shown @{ProfileNumber}
    ${result}=  run keyword   Verify number  @{ProfileNumber}
    Should be true   ${result}

I verify all column names in Profiles
    ${result}=  run keyword   Verify all column names in Profiles
    Should be true   ${result}

I verify buttons enabled in Profiles @{expectedEnabledButtonsDefault}
    ${result}=  run keyword   Verify buttons enabled in Profiles  @{expectedEnabledButtonsDefault}
    Should be true   ${result}

I select an existing extension from current profile
     [Documentation]   To open Programmable Buttons link for selected user
     [Return]  ${extension}
     ${extension}=  Run Keyword     read_first_extension_in_profile_grid

I select a profile &{Product}
    ${result}=  run keyword   Select profile  &{Product}

I verify buttons enabled for single profile selection @{expectedEnabledButtonsSingleSection}
    ${result}=  run keyword   Verify buttons enabled in Profiles  @{expectedEnabledButtonsSingleSection}
    Should be true   ${result}

I select another profile &{Product}
    ${result}=  run keyword   Select profile  &{Product}

I verify buttons enabled for two profile selection @{expectedEnabledButtonsTwoSections}
    ${result}=  run keyword   Verify buttons enabled in Profiles  @{expectedEnabledButtonsTwoSections}
    Should be true   ${result}

I verify the errors in the profiles spreadsheet
    [Documentation]  This keyword verifies that there are erors in the import spread sheet
    ${result}=  Run Keyword     verify_errors_in_profile_spreadsheet
    Should be true  ${result}

I open On Hold Music
    run keyword   Open on hold music

I select a On Hold Music file
    ${onHoldMusicData}=  run keyword   Select on hold music file
    [Return]    ${onHoldMusicData}

I click on delete button and confirm
    run keyword   click On Hold Music Delete button and confirm

I verify delete operation is successful
    [Arguments]     @{onHoldMusicData}
    ${result}=  Run Keyword     Verify delete operation is successful  @{onHoldMusicData}
    Should be true   ${result}

I select Programmable Buttons tab for user ${user_email}
    [Documentation]   To open Programmable Buttons link for selected user
    ${result}=  Run Keyword     select_prog_buttons_for_user    ${user_email}

I verify programmed button
    [Documentation]  This keyword will verify the programmed button matches the expected paramaters
    [Arguments]  &{prog_info}
    ${result}=  Run Keyword     verify_programmable_button    &{prog_info}
    Should be true  ${result}

I select a location on the phone system phones page
    [Documentation]  This keyword selects the first location on the phone system phones page
    ${result}=  Run Keyword     select_first_location_on_phones_page
    Should be true  ${result}

I click the Import button on the phone system phones page
    I click the "Phones_import_phones_button" button

I import the phones into the phones page
    I click the "Phones_import_button" button

I verify the errors in the phones spreadsheet
    [Documentation]  This keyword selects the first location on the phone system phones page
    ${result}=  Run Keyword     verify_errors_in_phones_spreadsheet
    Should be true  ${result}

I close the phone import dialog
    I click the "Phones_import_close_button" button

I remove the imported phone to clean up
    [Documentation]  This keyword deleted the imported phone from the phones list
    ${result}=  Run Keyword     delete_imported_phone  00:00:00:00:00:01
    Should be true  ${result}

I clean up by deleting the created profile
    [Arguments]  &{user_profile}
    I switch to "primary_partition" page
    I switch to "primary_partition_profiles" page
    I select one profile in the profile grid     &{user_profile}
    I unassign one profile

I unassign one profile with no TN
    Run Keyword     unassign_profile_with_no_TN

I clean up by deleting the created profile that has no TN
    [Arguments]  &{user_profile}
    I switch to "primary_partition" page
    I switch to "primary_partition_profiles" page
    I select one profile in the profile grid     &{user_profile}
    I unassign one profile with no TN

I clean up by deleting all the created profiles
    [Arguments]  @{user_profile_list}
    I switch to "primary_partition" page
    I switch to "primary_partition_profiles" page
    ${result}=  Run Keyword     delete_all_imported_profiles    @{user_profile_list}
    Should be true  ${result}

I upload a mp3 file to On Hold Music
    [Arguments]     &{file_upload_info}
    ${result}=  run keyword   upload file to On Hold Music   &{file_upload_info}
    Should be true   ${result}

I verify an error message that the file is in the wrong format
    ${result}=  run keyword   Verify wrong file format error message
    Should be true   ${result}

I verify this file was not uploaded to On Hold Music
    [Arguments]     ${filename}
    ${result}=  run keyword   search file On Hold Music  ${filename}
    should not be true   ${result}

I upload a stereo below 8khz wav file to On Hold Music
    [Arguments]     &{file_upload_info}
    ${result}=  run keyword   upload file to On Hold Music   &{file_upload_info}
    Should be true   ${result}

I verify this file was successfully uploaded to On Hold Music
    [Arguments]     &{file_upload_info}
    ${result}=  run keyword   verify on hold music file added  &{file_upload_info}
    Should be true   ${result}

I upload a mono above 8khz wav file to On Hold Music
    [Arguments]     &{file_upload_info}
    ${result}=  run keyword   upload file to On Hold Music   &{file_upload_info}
    Should be true   ${result}

I edit user phone settings
    [Documentation]   To enable or edit user phone settings in user phone settings page
    ...  Params: user mail id, user Group Name/ Shared Call Appearance/ Video Conferencing  etc
    ...  return: status - True/False
    [Arguments]    &{user_ph_setting_Info}
    ${result}=   run keyword     edit user phone settings page    &{user_ph_setting_Info}
    should be true      ${result}

I verify different types of phone numbers
    [Arguments]     &{DiffPhoneNumbers}
    ${result}=      Run keyword  verify type of phone numbers   &{DiffPhoneNumbers}
    should be true  ${result}

I add user from profiles tab
    [Arguments]     &{ProfilePageUser}
    ${extn}  ${result}=      Run keyword  add user from profiles tab   &{ProfilePageUser}
    should be true  ${result}
    [Return]  ${extn}

I add user from numbers tab
    [Arguments]     &{ProfilePageUser}
    ${extn}  ${result}=      Run keyword  add user from numbers tab   &{ProfilePageUser}
    should be true  ${result}
    [Return]  ${extn}

I verify the User exist in user table created from profiles page
    [Arguments]     &{ProfilePageUser}
    ${result}=      Run keyword  verify user created from profiles page   &{ProfilePageUser}
    should be true  ${result}

I assign phone number to Auto Attendant
    [Arguments]  ${aa_name}
    &{component_details}=    Create Dictionary    aa_name=${aa_name}
    ${result}=  run keyword  assign ph number to auto attendant  &{component_details}
    should be true  ${result}

I assign phone number to Hunt Group
    [Arguments]  ${hg_name}
    &{component_details}=    Create Dictionary    hg_name=${hg_name}
    ${result}=  run keyword  assign ph number to hunt group  &{component_details}
    should be true  ${result}

I edit enabled digit from Dial plan
    [Arguments]  ${type}
    ${DialPlanDict}  ${result}=  run keyword   edit enabled digit from dial plan   ${type}
    should be true  ${result}
    [Return]    ${DialPlanDict}

I verify edited dial plan from phone system page
    [Arguments]  &{DialPlanDict}
    ${result}=  run keyword  verify edited dial plan from phone system page    &{DialPlanDict}
    should be true  ${result}

I verify tabs not exist
    [Arguments]    @{tab_list}
    ${result}=    Run Keyword    Verify Tabs Exist    @{tab_list}
    should not be true  ${result}

In D2 I verify user email ${d2user_email} with extension ${extn} is set for ${newacc}
    &{user}=    Create Dictionary    exp_user_email=${d2user_email}    extn=${extn}     newacc=${newacc}
    ${result}=   Run Keyword    director verify users   &{user}
    Should be true    ${result}

I assign profile to the contact with no profile
    [Arguments]    &{userinfo}
    ${phone_num}  ${extn}=     assign profile to contact with no profile    &{userinfo}
    Log  "${phone_num} ${extn}"
    [Return]      ${phone_num}    ${extn}
I configure exchange server name
    [Arguments]    ${ex_server_name}
    ${result}=  Run Keyword    configure exchange server  ${ex_server_name}
    Should be true   ${result}

I verify "${component:[^"]+}" is not present in profiles tab
    &{comp_info}=    Create Dictionary    component_name=${component}
    ${result}=    Run Keyword    verify created components in profile tab   &{comp_info}
    should not be true   ${result}

I verify "${component:[^"]+}" is present in profiles tab
    &{comp_info}=    Create Dictionary    component_name=${component}
    ${result}=    Run Keyword    verify created components in profile tab   &{comp_info}
    Should be true   ${result}

I close services
    [Arguments]  &{service_info}
    ${result}=  run keyword  close service  &{service_info}
    should be true  ${result}
I check user info in Boss after sync with STD2
    [Arguments]     ${user_name}    ${extension}  ${user_email}    ${sync_type}
    &{params}=   Create Dictionary  UserName=${user_name}    Extension=${extension}  Email=${user_email}   sync_type=${sync_type}
    ${result}=  run keyword    verify_synced_user_profile    &{params}
    Should be true   ${result}

I verify sip password in phone settings of user ${user_email}
    [Documentation]   This keyword will verify whether SIP Password is displayed in Phone Settings page of User
    ${result}=  Run Keyword     verify_phone_settings_sip_password    ${user_email}
    Should be true   ${result}

I verify global user loc not in account details page
    [Arguments]  &{global_user_loc}
    ${result}=  run keyword    verify global user loc not in account details page    &{global_user_loc}
    SHOULD BE TRUE  ${result}

I verify radio button "${radiobuttonname:[^"]+}"
    [Documentation]   This Function will verify the radio button in any specified page
    &{buttonName}=    Create Dictionary       radio_btn=${radiobuttonname}
    ${result}=  Run Keyword       verify radio button   &{buttonName}
    Should be true   ${result}

I switch to "${myNewPage:[^"]+}" page for "${componentName:[^"]+}"
	&{pageSwitch}=    Create Dictionary       page=${myNewPage}    compName=${componentName}
	Run Keyword       switch_page      &{pageSwitch}

I edit user profiles
    [Arguments]  &{params}
    ${result}=  run keyword  edit profiles  &{params}
    should be true  ${result}

I edit user personal information
    [Arguments]  &{params}
    ${result}=  run keyword  edit user personal information  &{params}
    should be true  ${result}

I update and verify account website detail with
   [Arguments]    ${siteName}
    ${result}=  run keyword  update_verify_account_website_detail  ${siteName}
    should be true  ${result}

I delete website detail
    ${result}=  run keyword  delete_account_website_detail
    should be true  ${result}

I retrieve service id from service page
    [Arguments]  &{service_info}
    ${serviceid}=    Run Keyword    retrieve service id  &{service_info}
    [Return]      ${serviceid}

I verify service status in service page
    [Arguments]  &{service_info}
    ${result}=  run keyword  verify service status  &{service_info}
    should be true  ${result}

I search mac address ${mac_address} and delete
    search_mac_address_and_delete  ${mac_address}


I select phone option ${call_option}
    Select Phone Setting Options   ${call_option}

I configure main settings ${setting_dict}
    Select Configure Main Setting    ${setting_dict}

I add find me ${Phone}
    Add Find Me    ${Phone}


I configure call forwarding settings with a parameter ${available_state} ${Call_routing_condition} ${Call_forward_condition} ${PhNumber} ${noofrings}
    &{parameter}=    Create Dictionary      available_state=${available_state}   Call_routing_condition=${Call_routing_condition}  Call_forward_condition=${Call_forward_condition}   PhNumber=${PhNumber}  noofrings=${noofrings}
    ${result}=  Run Keyword     configure_availablity_Settings  &{parameter}
    Should be true   ${result}

I create new power routing with a parameter ${rulename} ${prcondition} ${prforward} ${PhNumber} ${deleteflag}
    &{parameter}=    Create Dictionary      rulename=${rulename}   prcondition=${prcondition}  prforward=${prforward}   PhNumber=${PhNumber}   deleteflag=${deleteflag}
    ${result}=  Run Keyword     create_new_power_routing  &{parameter}
    Should be true   ${result}

I select call routing page using extension ${phextension}
    ${result}=  Run Keyword     select_call_routing_using_extension  ${phextension}
    Should be true   ${result}
