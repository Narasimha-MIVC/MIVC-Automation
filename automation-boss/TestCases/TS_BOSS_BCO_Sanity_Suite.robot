*** Settings ***
Documentation     BOSS BCO Sanity suite
...               dev-Kenash, Rahul, Vasuja


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../Variables/LoginDetails.robot
Resource          ../Variables/ContractInfo.robot
Resource          ../Variables/PartitionInfo.robot
Resource          ../Variables/PhoneNumberInfo.robot
Resource          ../Variables/UserInfo.robot
Resource          ../Variables/UserTabList.robot
Resource          ../Variables/InvoicesPaymentsinfo.robot
Resource          ../Variables/Geolocationinfo.robot
Resource          ../Variables/ExtensionListInfo.robot
Resource          ../Variables/PickupGroupInfo.robot
Resource          ../Variables/Hunt_Group_Info.robot
Resource          ../Variables/AutoAttendantInfo.robot
Resource          ../Variables/CustomScheduleInfo.robot
Resource          ../Variables/PageGroupInfo.robot
Resource          ../Variables/ProgBtnInfo.robot
Resource          ../Variables/IpphoneInfo.robot
Resource          ../Variables/serviceInfo.robot
Resource          ../Variables/ErrorStrings.robot

#BOSS Component
Library           ../lib/BossComponent.py    browser=${BROWSER}    country=${country}
Library           ../lib/DirectorComponent.py
Library           PPhoneInterface

*** Test Cases ***
01 Login to the boss portal and create contract
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "accounts" page
    log to console   ${TestContract["filePath"]}
    and I add contract    &{TestContract}
    Then I verify "company_name" contains "${TestContract["accountName"]}"
    Log  "Account ${TestContract["accountName"]} created"
    and I verify grid contains "Ordered" value
    When I click on "${TestContract["accountType"]}" link in "contract_grid"
    ${order_number}=   and I confirm the contract with instance "${bossCluster} (${platform})" and location "${TestContract["locationName"]}"
    Set suite variable    ${order_number}
    Then I switch to "contracts" page
    and I verify contract "${TestContract["accountName"]}" with "Confirmed" state
    #and I log off

#01a As a staff update service status
#    #Given I login to ${URL} with ${bossUsername} and ${bossPassword}
#    #When I switch to "switch_account" page
#    #And I switch to account ${TestContract["accountName"]} with ${AccWithoutLogin} option
#	Then I switch to "services" page
#	Set to Dictionary    ${service01}    orderId    ${order_number}
#	log to console    ${service01}
#	And I update service status     &{service01}

02 Create primary partition
    #Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "account_details" page
    sleep  3
    set to dictionary  ${params}  get_account_id  ${True}
    And I retrieve account details  ${params}
    When I switch to "partitions" page
    #and I add Partition    &{PartitionDetails}
    Then I verify that Partition is set as Primary    &{PartitionDetails}
    #And I log off

03 Set default location as site
    When I move to "sites" tab
    and I set the default location as site
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and In D2 I verify location "${TestContract["locationName"]}" is set as site for "${params['partition_id']}"

04 Provision the required TN
    When I switch to "phonenumber" page
    I add PhoneNumber    &{PhoneNumberDetails}
    and I set PhoneNumber state    &{PhoneNumberDetails}
    Then I verify PhoneNumber state    &{PhoneNumberDetails}

05 Create users and verify that the users are created
    When I log off
    and I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    and I accept agreement
    and I log off
    and I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    Then I verify "company_name" contains "${TestContract["accountName"]}"
    When I switch to "users" page
    Set to Dictionary    ${DMUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${DMUser}    login_user    DM
    Log    ${DMUser}    console=yes
    and I add user    &{DMUser}
    Then I verify that User exist in user table    &{DMUser}
    Set to Dictionary    ${LocPMUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${LocPMUser}    login_user    DM
    Log    ${LocPMUser}    console=yes
    When I add user    &{LocPMUser}
    Then I verify that User exist in user table    &{LocPMUser}
    Set to Dictionary    ${AccPMUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${AccPMUser}    login_user    DM
    Log    ${AccPMUser}    console=yes
    When I add user    &{AccPMUser}
    Then I verify that User exist in user table    &{AccPMUser}

    ${r_str}=    Generate Random String    4    [LETTERS]
    @{role_list}=    Create List    Billing    Technical    Emergency
    ${InitUser}=    Copy Dictionary    ${GenUser}
    : FOR    ${role_name}    IN    @{role_list}
    \    ${GenUser}=    Copy Dictionary    ${InitUser}
    \    ${updated_role}=    Replace String    ${GenUser["role"]}    {role}    ${rolename}
    \    ${updated_uname}=    Replace String    ${GenUser["au_username"]}    {rand_str}    ${updated_role}_${r_str}
    \    ${updated_bmail}=    Replace String    ${GenUser["au_businessmail"]}    {rand_str}    ${updated_role}_${r_str}
    \    ${updated_pmail}=    Replace String    ${GenUser["au_personalmail"]}    {rand_str}    ${updated_role}_${r_str}
    \    Set to Dictionary    ${GenUser}    add_user_error    ${request_submitted}
    \    Set to Dictionary    ${GenUser}    login_user    DM
    \    Set to Dictionary    ${GenUser}    role    ${updated_role}
    \    Set to Dictionary    ${GenUser}    au_username    ${updated_uname}
    \    Set to Dictionary    ${GenUser}    au_businessmail    ${updated_bmail}
    \    Set to Dictionary    ${GenUser}    au_personalmail    ${updated_pmail}
    \    Set to Dictionary    ${GenUser}    au_userlocation    ${TestContract["locationName"]}
    \    Set to Dictionary    ${GenUser}    au_location    ${TestContract["locationName"]}
    \    Append To List    ${user_list}    ${GenUser}
    \    When I add user    &{GenUser}
    \    Then I verify that User exist in user table    &{GenUser}
    and I log off

    #LOGIN AS LOC PM AND CREATE USER
    When I login to ${URL} with ${LocPMUser["au_username"]} and ${LocPMUser["au_password"]}
    and I change password to ${bossPassword}
    When I switch to "users" page
    ${r_str}=    Generate Random String    4    [LETTERS]
    @{role_list}=    Create List    Technical    Emergency    Phone Manager
    log to console  ${InitUser}
    : FOR    ${role_name}    IN    @{role_list}
    \    ${GenUser}=    Copy Dictionary    ${InitUser}
    \    Log To Console    ${GenUser}
    \    Log To Console    ${GenUser["au_username"]}
    \    ${updated_role}=    Replace String    ${GenUser["role"]}    {role}    ${rolename}
    \    ${updated_uname}=    Replace String    ${GenUser["au_username"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
    \    ${updated_bmail}=    Replace String    ${GenUser["au_businessmail"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
    \    ${updated_pmail}=    Replace String    ${GenUser["au_personalmail"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}

    \    Set to Dictionary    ${GenUser}    role    ${updated_role}
    \    Set to Dictionary    ${GenUser}    au_username    ${updated_uname}
    \    Set to Dictionary    ${GenUser}    au_businessmail    ${updated_bmail}
    \    Set to Dictionary    ${GenUser}    au_personalmail    ${updated_pmail}
    \    Set to Dictionary    ${GenUser}    au_userlocation    ${TestContract["locationName"]}
    \    Set to Dictionary    ${GenUser}    au_location    ${TestContract["locationName"]}
    \    Set to Dictionary    ${GenUser}    add_user_error    ${request_submitted}
    \    Set to Dictionary    ${GenUser}    login_user    DM
    \    When I add user    &{GenUser}
    \    Then I verify that User exist in user table    &{GenUser}
    and I log off

    #LOGIN AS ACC PM AND CREATE USER
    When I login to ${URL} with ${AccPMUser["au_username"]} and ${AccPMUser["au_password"]}
    and I change password to ${bossPassword}
    and I switch to "users" page
    ${r_str}=    Generate Random String    4    [LETTERS]
    @{role_list}=    Create List    Technical    Emergency    Phone Manager
    #${InitUser}=    Copy Dictionary    ${GenUser}
    : FOR    ${role_name}    IN    @{role_list}
    \    ${GenUser}=    Copy Dictionary    ${InitUser}
    \    Log To Console    ${GenUser}
    \    Log To Console    ${GenUser["au_username"]}
    \    ${updated_role}=    Replace String    ${GenUser["role"]}    {role}    ${rolename}
    \    ${updated_uname}=    Replace String    ${GenUser["au_username"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
    \    ${updated_bmail}=    Replace String    ${GenUser["au_businessmail"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
    \    ${updated_pmail}=    Replace String    ${GenUser["au_personalmail"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
    \    Set to Dictionary    ${GenUser}    role    ${updated_role}
    \    Log To Console    ${GenUser}
    \    Set to Dictionary    ${GenUser}    au_username    ${updated_uname}
    \    Set to Dictionary    ${GenUser}    au_businessmail    ${updated_bmail}
    \    Set to Dictionary    ${GenUser}    au_personalmail    ${updated_pmail}
    \    Set to Dictionary    ${GenUser}    au_userlocation    ${TestContract["locationName"]}
    \    Set to Dictionary    ${GenUser}    au_location    ${TestContract["locationName"]}
    \    Log To Console    ${GenUser}
    \    Set to Dictionary    ${GenUser}    add_user_error    ${request_submitted}
    \    Set to Dictionary    ${GenUser}    login_user    DM
    \    When I add user    &{GenUser}
    \    Then I verify that User exist in user table    &{GenUser}

06 Login with Users with different roles and verify the available tabs
    When I log off
    And I login to ${URL} with ${bossUsername} and ${bossPassword}
    Then I verify tabs exist    @{StaffUserTab}
    And I log off
    When I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    Then I verify tabs exist    @{DMUserTab}
    And I log off
    When I login to ${URL} with ${LocPMUser["au_username"]} and ${bossPassword}
    Then I verify tabs exist    @{PMUserTab}
    And I log off
    : FOR    ${role_name}    IN    @{user_list}
    \    Log to console    ${role_name}
    \    When I login to ${URL} with ${role_name["au_username"]} and ${role_name["au_password"]}
    \    and I change password to ${bossPassword}
    \    Run Keyword If    '${role_name['role']}' == 'Technical'    I verify tabs exist    @{TechnicalUserTab}
    \    Run Keyword If    '${role_name['role']}' == 'Billing'    I verify tabs exist    @{BillingUserTab}
    \    Run Keyword If    '${role_name['role']}' == 'emergency'    I verify tabs exist    @{EmergencyUserTab}
    \    And I log off

07 Login as DM user and create users with profiles
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I log off
    and I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    #and I accept agreement
    Then I verify "company_name" contains "${TestContract["accountName"]}"

    When I switch to "users" page
    Set to Dictionary    ${DMProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${DMProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${DMProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${DMProfUser}    login_user    DM
    ${phone_num}  ${extn}=    and I add user    &{DMProfUser}
    Set to Dictionary    ${DMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${DMProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{DMProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{DMProfUser}

    When I switch to "users" page
    Set to Dictionary    ${LocPMProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${LocPMProfUser}    login_user    DM
    ${phone_num}  ${extn}=    and I add user    &{LocPMProfUser}
    Set to Dictionary    ${LocPMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfUser}

    When I switch to "users" page
    Set to Dictionary    ${AccPMProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${AccPMProfUser}    login_user    DM
    ${phone_num}  ${extn}=    I add user    &{AccPMProfUser}
    Set to Dictionary    ${AccPMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfUser}

    When I switch to "users" page
    Set to Dictionary    ${BillingProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${BillingProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${BillingProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${BillingProfUser}    login_user    DM
    ${phone_num}  ${extn}=    I add user    &{BillingProfUser}
    Set to Dictionary    ${BillingProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${BillingProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{BillingProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{BillingProfUser}

    When I switch to "users" page
    Set to Dictionary    ${TechnicalProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${TechnicalProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${TechnicalProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${TechnicalProfUser}    login_user    DM
    ${phone_num}  ${extn}=    I add user    &{TechnicalProfUser}
    Set to Dictionary    ${TechnicalProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${TechnicalProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{TechnicalProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{TechnicalProfUser}

    When I switch to "users" page
    Set to Dictionary    ${EmergencyProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${EmergencyProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${EmergencyProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${EmergencyProfUser}    login_user    DM
    ${phone_num}    ${extn}=    I add user    &{EmergencyProfUser}
    Set to Dictionary    ${EmergencyProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${EmergencyProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{EmergencyProfUser}
    And I switch to "services" page
    And I verify profile updated in service table    &{EmergencyProfUser}
    #And I log off
    [Teardown]  run keywords  I log off

08 Login as Location PM and create users with profiles
    When I login to ${URL} with ${LocPMProfUser["au_username"]} and ${LocPMProfUser["au_password"]}
    And I change password to ${bossPassword}
    When I switch to "users" page
    Set to Dictionary    ${LocPMProfPMUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfPMUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfPMUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${LocPMProfPMUser}    login_user    PM
    ${phone_num}  ${extn}=    I add user    &{LocPMProfPMUser}
    Set to Dictionary    ${LocPMProfPMUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfPMUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfPMUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfPMUser}
    When I switch to "users" page
    Set to Dictionary    ${LocPMProfBillingUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfBillingUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfBillingUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${LocPMProfBillingUser}    login_user    PM
    ${phone_num}  ${extn}=    I add user    &{LocPMProfBillingUser}
    Set to Dictionary    ${LocPMProfBillingUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfBillingUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfBillingUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfBillingUser}
    When I switch to "users" page
    Set to Dictionary    ${LocPMProfTechnicalUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfTechnicalUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${LocPMProfTechnicalUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${LocPMProfTechnicalUser}    login_user    PM
    ${phone_num}  ${extn}=    I add user    &{LocPMProfTechnicalUser}
    Set to Dictionary    ${LocPMProfTechnicalUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfTechnicalUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfTechnicalUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfTechnicalUser}
    #And I log off
    [Teardown]  run keywords  I log off

09 Login as Account PM and create users with profiles
    When I login to ${URL} with ${AccPMProfUser["au_username"]} and ${AccPMProfUser["au_password"]}
    and I change password to ${bossPassword}
    When I switch to "users" page
    When I switch to "users" page
    Set to Dictionary    ${AccPMProfPMUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfPMUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfPMUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${AccPMProfPMUser}    login_user    PM
    ${phone_num}  ${extn}=    I add user    &{AccPMProfPMUser}
    Set to Dictionary    ${AccPMProfPMUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfPMUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfPMUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfPMUser}
    When I switch to "users" page
    Set to Dictionary    ${AccPMProfBillingProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfBillingProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfBillingProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${AccPMProfBillingProfUser}    login_user    PM
    ${phone_num}  ${extn}=    I add user    &{AccPMProfBillingProfUser}
    Set to Dictionary    ${AccPMProfBillingProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfBillingProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfBillingProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfBillingProfUser}
    When I switch to "users" page
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    au_userlocation    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    au_location    ${TestContract["locationName"]}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    add_user_error    ${request_submitted}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    login_user    PM
    ${phone_num}  ${extn}=    I add user    &{AccPMProfTechnicalProfUser}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfTechnicalProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfTechnicalProfUser}
    #And I log off
    [Teardown]  run keywords  I log off

10 Login as Staff and add invoice group
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${TestContract["accountName"]} with ${AccWithoutLogin} option
    when I switch to "Invoices_and_Payments" page
    Set to Dictionary    ${InvoiceDetails}    Location    ${TestContract["locationName"]}
    and I create invoice group    &{InvoiceDetails}
    Then I move to "tab_invoices_groups" tab
    and I verify grid contains "${InvoiceDetails["invoiceName"]}" value
    When I click on "${InvoiceDetails["invoiceName"]}" link in "invoice_Groups_Grid"
    Then I verify that Invoice group is associated with location    &{InvoiceDetails}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

11 Login as DM and add emergency hunt group
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    and I create emergency hunt group    &{InvoiceDetails}
    Then I verify location "${InvoiceDetails["Location"]}" with "Registered" state
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify emergency hunt group "Emergency - ${InvoiceDetails['Location']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert


12 Login as PM and add emergency hunt group
    #When I check for alert
    When I login to ${URL} with ${AccPMProfUser["au_username"]} and ${bossPassword}
    and I switch to "geographic_locations" page
    and I create geographic location    &{geolocationDetails}
    Then I verify location "${geolocationDetails['Location']}" with "Registered" state
    When I switch to "Visual_Call_Flow_Editor" page
    and I create emergency hunt group    &{geolocationDetails}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify emergency hunt group "Emergency - ${geolocationDetails['Location']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

23 Create Extension list
    #When I check for alert
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${DMProfUser['ap_extn']}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    #And I log off
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify extension list "${Extensionlist01['extnlistname']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert
    ...                       And I log off

13 Login as DM and create Hunt group with mandatory inputs
    #When I check for alert
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup01}    hglocation    ${TestContract["locationName"]}
    ${extn_num}=    Then I create hunt group    &{Huntgroup01}
    Set to Dictionary    ${Huntgroup01}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup01['HGname']}" with extension "${Huntgroup01['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert

14 As DM create Hunt group with mandatory inputs + group members
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup02}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup02}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup02}
    Set to Dictionary    ${Huntgroup02}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup02['HGname']}" with extension "${Huntgroup02['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert

15 As DM create Hunt group with mandatory inputs + group members + custom extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup03}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup03}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    I create hunt group    &{Huntgroup03}
    Set to Dictionary    ${Huntgroup03}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup03['HGname']}" with extension "${Huntgroup03['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert

16 As DM create Hunt group with mandatory inputs + group members + private extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup04}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup04}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup04}
    Set to Dictionary    ${Huntgroup04}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup04['HGname']}" with extension "${Huntgroup04['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert


17 As DM create Hunt group with mandatory inputs + group members + Phone number
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup05}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup05}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup05}
    Set to Dictionary    ${Huntgroup05}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup05['HGname']}" with extension "${Huntgroup05['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

18 Login as PM and create Hunt group with mandatory inputs
    #When I check for alert
    Given I login to ${URL} with ${AccPMProfUser["au_username"]} and ${bossPassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup06}    hglocation    ${TestContract["locationName"]}
    ${extn_num}=    Then I create hunt group    &{Huntgroup06}
    Set to Dictionary    ${Huntgroup06}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup06['HGname']}" with extension "${Huntgroup06['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

19 As PM create Hunt group with mandatory inputs + group members
    #When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup07}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup07}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup07}
    Set to Dictionary    ${Huntgroup07}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup07['HGname']}" with extension "${Huntgroup07['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

20 As PM create Hunt group with mandatory inputs + group members + custom extension
    #When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup08}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup08}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup08}
    Set to Dictionary    ${Huntgroup08}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup08['HGname']}" with extension "${Huntgroup08['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

21 As PM create Hunt group with mandatory inputs + group members + private extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup09}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup09}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup09}
    Set to Dictionary    ${Huntgroup09}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup09['HGname']}" with extension "${Huntgroup09['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

22 As PM create Hunt group with mandatory inputs + group members + Phone number
    #When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup10}    hglocation    ${TestContract["locationName"]}
    Set to Dictionary    ${Huntgroup10}    grp_member    ${DMProfUser['ap_extn']}
    ${extn_num}=    Then I create hunt group    &{Huntgroup10}
    Set to Dictionary    ${Huntgroup10}    HGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify hunt group "${Huntgroup10['HGname']}" with extension "${Huntgroup10['HGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

24 Login as DM and create Pickup group
    #When I check for alert
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup01}    pickuploc    ${TestContract["locationName"]}
    ${extn_num}=    I create pickup group    &{Pickupgroup01}
    Set to Dictionary    ${Pickupgroup01}    PGExtn    ${extn_num}
    log to console    ${Pickupgroup01}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup01['pickupgpname']}" with extension "${Pickupgroup01['PGExtn']}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

25 Login as PM and create Pickup group
    #When I check for alert
    Given I login to ${URL} with ${AccPMProfUser["au_username"]} and ${bossPassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup02}    pickuploc    ${TestContract["locationName"]}
    ${extn_num}=    I create pickup group    &{Pickupgroup02}
    Set to Dictionary    ${Pickupgroup02}    PGExtn    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroup02['pickupgpname']}" with extension "${Pickupgroup02['PGExtn']}" is set for ${params['partition_id']}
    #And I log off
    [Teardown]  run keywords  I log off
    ...                      I check for alert

26 Login as DM to the boss portal and add an auto-attendant with default values
    When I check for alert
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for ${params['partition_id']}


27 Login as DM to the boss portal and add an auto-attendant with custom-extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_02["Aa_Name"]}" with extension "${AA_02["AA_customExtension"]}" is set for ${params['partition_id']}

28 Login as DM to the boss portal and add an auto-attendant with extension labeled private
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_03}
    Set to Dictionary    ${AA_03}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_03["Aa_Name"]}" with extension "${AA_03["AA_Extension"]}" is set for ${params['partition_id']}

29 Login as DM to the boss portal and add an auto-attendant with extension labled private and having a custom extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_04}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_04["Aa_Name"]}" with extension "${AA_04["AA_customExtension"]}" is set for ${params['partition_id']}

30 Login as DM to the boss portal and add an auto-attendant and assign a DID
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_05}
    Set to Dictionary    ${AA_05}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_05["Aa_Name"]}" with extension "${AA_05["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

31 Login as PM to the boss portal and add an auto-attendant with default values
    When I check for alert
    Given I login to ${URL} with ${LocPMProfUser["au_username"]} and ${bossPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_06}
    Set to Dictionary    ${AA_06}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_06["Aa_Name"]}" with extension "${AA_06["AA_Extension"]}" is set for ${params['partition_id']}

32 As PM to the boss portal and add an auto-attendant with custom-extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_07}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_07["Aa_Name"]}" with extension "${AA_07["AA_customExtension"]}" is set for ${params['partition_id']}

33 Login as PM to the boss portal and add an auto-attendant with extension labeled private
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_08}
    Set to Dictionary    ${AA_08}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_08["Aa_Name"]}" with extension "${AA_08["AA_Extension"]}" is set for ${params['partition_id']}

34 Login as PM to the boss portal and add an auto-attendant with extension labled private and having a custom extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_09}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_09["Aa_Name"]}" with extension "${AA_09["AA_customExtension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

35 Login as PM to the boss portal and add an auto-attendant and assign a DID
    #When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_10}
    Set to Dictionary    ${AA_10}    AA_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify AA "${AA_10["Aa_Name"]}" with extension "${AA_10["AA_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

36 As a DM create custom schedule
    #When I check for alert
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule_DM}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify custom schedule "${CustomSchedule_DM["customScheduleName"]}" is set for ${params['partition_id']}
    #And I log off
    [Teardown]  run keywords  I log off
    ...                      I check for alert

37 As a PM create custom schedule
    #When I check for alert
    Given I login to ${URL} with ${LocPMProfUser["au_username"]} and ${bossPassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule_PM}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and In D2 I verify custom schedule "${CustomSchedule_PM["customScheduleName"]}" is set for ${params['partition_id']}
    #And I log off
    [Teardown]  run keywords  I log off
    ...                      I check for alert

38 Login as DM to the boss portal and add an paging-group with default values
    #When I check for alert
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_01}
    Set to Dictionary    ${Pg_01}    Pg_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_01["Pg_Name"]}" with extension "${Pg_01["Pg_Extension"]}" is set for ${params['partition_id']}
    [Teardown]  run keywords           I check for alert

39 Login as DM to the boss portal and add an paging-group with private extension
    #When I check for alert
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_02}
    Set to Dictionary    ${Pg_02}    Pg_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_02["Pg_Name"]}" with extension "${Pg_02["Pg_Extension"]}" is set for ${params['partition_id']}

40 Login as DM to the boss portal and add an paging-group with custom extension
    When I check for alert
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_03}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_03["Pg_Name"]}" with extension "${Pg_03["Pg_Extension"]}" is set for ${params['partition_id']}

41 Login as DM to the boss portal and add an paging-group with custom extension and private extension
    #When I check for alert
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_04}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_04["Pg_Name"]}" with extension "${Pg_04["Pg_Extension"]}" is set for ${params['partition_id']}
    #And I log off
    [Teardown]  run keywords  I log off

42 Login as PM to the boss portal and add an paging-group with default values
    When I check for alert
    Given I login to ${URL} with ${LocPMProfUser["au_username"]} and ${bossPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_05}
    Set to Dictionary    ${Pg_05}    Pg_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_05["Pg_Name"]}" with extension "${Pg_05["Pg_Extension"]}" is set for ${params['partition_id']}

43 Login as PM to the boss portal and add an paging-group with private extension
    When I check for alert
    #Given I login to ${URL} with "pm1@user1.com" and "zaqwsx123!@#$"
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_06}
    Set to Dictionary    ${Pg_06}    Pg_Extension    ${extn_num}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_06["Pg_Name"]}" with extension "${Pg_06["Pg_Extension"]}" is set for ${params['partition_id']}

44 Login as PM to the boss portal and add an paging-group with custom extension
    When I check for alert
    #Given I login to ${URL} with "pm1@user1.com" and "zaqwsx123!@#$"
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_07}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_07["Pg_Name"]}" with extension "${Pg_07["Pg_Extension"]}" is set for ${params['partition_id']}

45 Login as PM to the boss portal and add an paging-group with custom extension and private extension
    When I check for alert
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_08}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and in D2 I verify PG "${Pg_08["Pg_Name"]}" with extension "${Pg_08["Pg_Extension"]}" is set for ${params['partition_id']}
    #And I log off
    [Teardown]  run keywords  I log off

46 Reset the login password by right clicking on user
    When I check for alert
    Given I login to ${URL} with ${LocPMProfUser["au_username"]} and ${bossPassword}
    When I switch to "users" page
    And I go to change password page for user "${LocPMProfUser['au_firstname']} ${LocPMProfUser['au_lastname']}"
    Then I change password to ${LocPMProfUser['au_password']}
    And I log off
    Then I login to ${URL} with ${LocPMProfUser["au_businessmail"]} and ${LocPMProfUser['au_password']}
    #and I log off
    [Teardown]  run keywords  I log off

47 Reset password from user profile page
    Given I login to ${URL} with ${LocPMProfUser["au_businessmail"]} and ${LocPMProfUser['au_password']}
    When I switch to "users" page
    then I click on user name and go to password change page "${LocPMProfUser['au_firstname']} ${LocPMProfUser['au_lastname']}"
    and I update password to ${bossPassword} from ${LocPMProfUser['au_password']}
    #and I log off
    [Teardown]  run keywords  I log off

48 Reset password from home page
    #In QA setup
    Given I open login page with ${URL}
    And I change password from home page  &{emailDetail}
    then I login to ${url} with ${Contract06['email']} and ${bossPassword}
    and I log off
    And I change password from home page  &{emailDetail1}

49 Close user
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    then I switch to account ${TestContract["accountName"]} with ${AccWithoutLogin} option
    then I switch to "users" page
    When I delete user ${LocPMUser["au_username"]} as user "${TestContract['firstName']} ${TestContract['lastName']}"
    #and I log off
    [Teardown]  run keywords  I log off

50 Login as PM and delete VCFE Component
    Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    And I delete vcfe entry for ${Huntgroup01['HGExtn']}
    Then I verify if VCFE entries with name "${Huntgroup01['HGname']}" and extn "${Huntgroup01['HGExtn']}" are deleted
    #and I log off
    [Teardown]  run keywords  I log off

51 Login to BOSS as DM and add a Silent Coach with default values
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    set to dictionary  ${proginfo01}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo01}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo01}
    #And I add prog button "Silent Monitor" with extension "7932" and email "${Contract01["email"]}"
    #And I log off
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo01["longlabel"]}
	Log		Using handset device for validation
	Log		Step 1:

	Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
	pphone Make Call	${Phone01}	${Phone02}	RIGHT_LINE1
	pphone Answer Call		${Phone02}	${Phone01}	RIGHT_LINE1
	pphone Handset Up	${Phone01}
	pphone Handset Up	${Phone02}
#	Pphone Check One Way Audio	${User01}	 ${User02}
#	Pphone Check One Way Audio	${User02}	 ${User01}

	Log		Step 2:
	pphone press button rightLine2		${Phone03}
	Pphone Handset Up	${Phone03}
#	Pphone Check One Way Audio	${User02}	 ${User03}
#	Pphone Check One Way Audio	${User03}	 ${User02}
#	Pphone Check One Way Audio	${User01}	 ${User03}
#	pphone check no audio	${User03}	 ${User01}

	Pphone handset disconnect call	   ${Phone01}
	Pphone Handset Down	${Phone03}
	Pphone Force Idle State	${Phone01}   ${Phone02}   ${Phone03}

52 Login to BOSS as DM and add a Silent Monitor with default values
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    set to dictionary  ${proginfo03}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo03}    user_email  ${phoneDMUser01["user_email"]}

    And I add prog button    &{proginfo03}
    #And I log off
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo03["longlabel"]}
    Log		Using handset device for validation
	Log		Step 1:
	Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
	pphone Make Call	${Phone01}	 ${Phone02}	RIGHT_LINE1
	pphone Answer Call		${Phone02}	${Phone01}	RIGHT_LINE1
	pphone Handset Up	${Phone01}
	pphone Handset Up	${Phone02}
#	Pphone Check One Way Audio	${User01}	 ${User02}
#	Pphone Check One Way Audio	${User02}	 ${User01}

	Log		Step 2:
	pphone press button rightLine2		${Phone03}
	Pphone Handset Up	${phone03}
#	Pphone Check One Way Audio	${User02}	 ${User03}
#	pphone check no audio	${User03}	 ${User02}
#	Pphone Check One Way Audio	${User01}	 ${User03}
#	pphone check no audio	${User03}	 ${User01}
	Pphone handset disconnect call	   ${Phone01}
	Pphone Handset Down	${phone03}
	Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}

53 Login to BOSS as DM and add a Barge In with default values
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    set to dictionary  ${proginfo05}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo05}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo05}
#   And I log off
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo05["longlabel"]}
	Log		Using handset device for validation
	Log		Step 1:
	Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
	pphone Make Call	${Phone01}	${Phone02}	RIGHT_LINE1
	pphone Answer Call		${Phone02}	${Phone01}	RIGHT_LINE1
	pphone Handset Up	${Phone01}
	pphone Handset Up	${Phone02}
#	Pphone Check One Way Audio	${User01}	 ${User02}
#	Pphone Check One Way Audio	${User02}	 ${User01}

	Log		Step 2:
	pphone press button rightLine2		${Phone03}
	Pphone Handset Up	${Phone03}
#	Pphone Check One Way Audio	${User02}	 ${User03}
#	Pphone Check One Way Audio	${User03}	 ${User02}
#	Pphone Check One Way Audio	${User01}	 ${User03}
#	Pphone Check One Way Audio	${User03}	 ${User01}
	Pphone handset disconnect call	   ${Phone01}
	Pphone Handset Down	${Phone03}
	Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}

54 Login to BOSS as DM and add a Pickup with default values
    #Given I login to ${URL} with ${Contract01["email"]} and ${Contract01["password"]}
    set to dictionary  ${proginfo07}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo07}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo07}

    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo07["longlabel"]}

    Log		Using handset device for validation
    Log		Step 1:
    Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
    pphone Make Call	${Phone01}	${Phone02}	RIGHT_LINE1
    pphone Handset Up	${Phone01}
    Log		Step 2:
    pphone press button rightLine2		${Phone03}
    Pphone Handset Up	${Phone03}
#    Pphone Check One Way Audio	${User01}	 ${User03}
#    Pphone Check One Way Audio	${User03}	 ${User01}
    Pphone handset disconnect call	   ${Phone01}
    Pphone Handset Down	${Phone03}
    Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}
    #And I log off
    [Teardown]  run keywords  I log off

55 Login to BOSS as PM and add a Silent Coach with default values
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}

    set to dictionary  ${proginfo02}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo02}    user_email  ${phoneDMUser01["user_email"]}

    And I add prog button    &{proginfo02}
    #And I add prog button "Silent Monitor" with extension "7932" and email "${Contract04["email"]}"
    #And I log off
    Log		Using handset device for validation
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo02["longlabel"]}
	Log		Step 1:
	Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
	pphone Make Call	${Phone01}	${Phone02}  RIGHT_LINE1
	pphone Answer Call		${Phone02}	${Phone01}	RIGHT_LINE1
	pphone Handset Up	${Phone01}
	pphone Handset Up	${Phone02}
#	Pphone Check One Way Audio	${User01}	 ${User02}
#	Pphone Check One Way Audio	${User02}	 ${User01}

	Log		Step 2:
	pphone press button rightLine2		${Phone03}
	Pphone Handset Up	${Phone03}
#	Pphone Check One Way Audio	${User02}	 ${User03}
#	Pphone Check One Way Audio	${User03}	 ${User02}
#	Pphone Check One Way Audio	${User01}	 ${User03}
#	pphone check no audio	${User03}	 ${User01}
	Pphone handset disconnect call	   ${Phone01}
	Pphone Handset Down	${Phone03}
	Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}

56 Login to BOSS as PM and add a Silent Monitor with default values
    #Given I login to ${URL} with ${Contract04["email"]} and ${Contract04["password"]}
    set to dictionary  ${proginfo04}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo04}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo04}
    #And I add prog button "Silent Coach" with extension "7934" and email "${Contract04["email"]}"
    #And I log off
    Log		Using handset device for validation
   ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo04["longlabel"]}
	Log		Step 1:
	Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
	pphone Make Call	${Phone01}	${Phone02}	RIGHT_LINE1
	pphone Answer Call		${Phone02}	${Phone01}	RIGHT_LINE1
	pphone Handset Up	${Phone01}
	pphone Handset Up	${Phone02}
#	Pphone Check One Way Audio	${User01}	 ${User02}
#	Pphone Check One Way Audio	${User02}	 ${User01}

	Log		Step 2:
	pphone press button rightLine2		${Phone03}
	Pphone Handset Up	${Phone03}
#	Pphone Check One Way Audio	${User02}	 ${User03}
#	pphone check no audio	${User03}	 ${User02}
#	Pphone Check One Way Audio	${User01}	 ${User03}
#	pphone check no audio	${User03}	 ${User01}
	Pphone handset disconnect call	   ${Phone01}
	Pphone Handset Down	${Phone03}
	Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}

57 Login to BOSS as PM and add a Barge In with default values
    #Given I login to ${URL} with ${Contract04["email"]} and ${Contract04["password"]}
    set to dictionary  ${proginfo06}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo06}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo06}
    #And I log off
    Log		Using handset device for validation
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	 log to console  ${btninfo}
	 List should contain value   ${btninfo}    ${proginfo06["longlabel"]}
	Log		Step 1:
	Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
	pphone Make Call	${Phone01}	${Phone02}	RIGHT_LINE1
	pphone Answer Call		${Phone02}	${Phone01}	RIGHT_LINE1
	pphone Handset Up	${Phone01}
	pphone Handset Up	${Phone02}
#	Pphone Check One Way Audio	${User01}	 ${User02}
#	Pphone Check One Way Audio	${User02}	 ${User01}

	Log		Step 2:
	pphone press button rightLine2		${Phone03}
	Pphone Handset Up	${Phone03}
#	Pphone Check One Way Audio	${User02}	 ${User03}
#	Pphone Check One Way Audio	${User03}	 ${User02}
#	Pphone Check One Way Audio	${User01}	 ${User03}
#	Pphone Check One Way Audio	${User03}	 ${User01}
	Pphone handset disconnect call	   ${Phone01}
    Pphone Handset Down	${Phone03}
	Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}

58 Login to BOSS as PM and add a Pickup with default values
   #Given I login to ${URL} with ${TestContract["email"]} and ${TestContract["password"]}
    set to dictionary  ${proginfo08}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo08}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo08}
    Log		Using handset device for validation
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo08["longlabel"]}
    Log		Step 1:
    Pphone Sanity Check	${Phone01}	${Phone02}	${Phone03}
    pphone Make Call	${Phone01}	${Phone02}	RIGHT_LINE1
    pphone Handset Up	${Phone01}
    Log		Step 2:
    pphone press button rightLine2		${Phone03}
    Pphone Handset Up	${Phone03}
#   Pphone Check One Way Audio	${User01}	 ${User03}
#   Pphone Check One Way Audio	${User03}	 ${User01}
    Pphone handset disconnect call	   ${Phone01}
    Pphone Handset Down	${phone03}
    Pphone Force Idle State	${Phone01}	${Phone02}	${Phone03}
    #And I log off
   [Teardown]  run keywords  I log off

59 Close geo location
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TestContract["accountName"]} with ${AccWithoutLogin} option
    then I switch to "geographic_locations" page
    then I create geographic location    &{geolocation_close}
    then I switch to "order" page
    and I close open order for location ${geolocation_close["Location"]}
    then I switch to "geographic_locations" page
    And I close the location ${geolocation_close["Location"]} requested by "${TestContract['firstName']} ${TestContract['lastName']}"
    #and i log off
    [Teardown]  run keywords  I log off

60 Login as staff user and delete contract
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    #and I switch to "switch_account" page
    #and I switch to account AutoTest_Acc_gkIAWr2r with ${AccWithoutLogin} option
    When I switch to "accounts" page
    log to console   ${ContracttoDelete["filePath"]}
    and I add contract    &{ContracttoDelete}
    Then I verify "company_name" contains "${ContracttoDelete["accountName"]}"
    Log  "Account ${ContracttoDelete["accountName"]} created"
    and I verify grid contains "Ordered" value
    When I click on "${ContracttoDelete["accountType"]}" link in "contract_grid"
    ${order_number}=   and I confirm the contract with instance "${bossCluster} (${platform})" and location "${ContracttoDelete["locationName"]}"
    Set suite variable    ${order_number}
#    Then I switch to "contracts" page
#    and I verify contract "${ContracttoDelete["accountName"]}" with "Confirmed" state
    When I switch to "order" page
    when I provision initial order
    When I switch to "services" page
    sleep  2s
    When I activate all service
    sleep  2s
    When I switch to "order" page
    And I close all order
    When I switch to "accounts" page
    And I close contract  ${ContracttoDelete["accountName"]}   ${TestContract["firstName"]}${SPACE}${TestContract["lastName"]}
    #And I close contract "AutoTest_Acc_gkIAWr2r"
    #Then I verify contract "AutoTest_Acc_gkIAWr2r" is deleted
    sleep  2s
    Then I verify contract "${ContracttoDelete["accountName"]}" is deleted
    [Teardown]  run keywords  I log off

*** Keywords ***
Set Init Env
    @{user_list}=    Create list
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${TestContract}=    create dictionary
    ${CustomSchedule_DM}=    create dictionary
    ${CustomSchedule_PM}=    create dictionary
    ${PhoneNumberDetails}=    create dictionary
    ${InvoiceDetails}=    create dictionary
    ${geolocationDetails}=    create dictionary
    ${geolocation_close}=    create dictionary
    ${PartitionDetails}=    create dictionary
    &{params}=  create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    @{user_list}
    Set suite variable    ${TestContract}
    Set suite variable    ${CustomSchedule_DM}
    Set suite variable    ${CustomSchedule_PM}
    Set suite variable    ${PhoneNumberDetails}
    Set suite variable    ${InvoiceDetails}
    Set suite variable    ${geolocationDetails}
    Set suite variable    ${geolocation_close}
    Set suite variable    ${PartitionDetails}
    Set suite variable    &{params}

    Run keyword if    '${country}' == 'Australia'
        ...    Run Keywords
        ...    set to dictionary  ${TestContract}  &{Contract_Aus}
        ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_AUS}
        ...    AND    set to dictionary  ${CustomSchedule_DM}   &{CustomScheduleDM_Aus}
        ...    AND    set to dictionary  ${CustomSchedule_PM}   &{CustomSchedulePM_Aus}
        ...    AND    set to dictionary  ${InvoiceDetails}   &{Invoice_AUS}
        ...    AND    set to dictionary  ${geolocationDetails}   &{geolocation_AUS}
        ...    AND    set to dictionary  ${geolocation_close}   &{geolocation_close_AUS}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_AUS}

        ...    ELSE IF    '${country}' == 'UK'
        ...    Run Keywords
        ...    set to dictionary  ${TestContract}  &{Contract_UK}
        ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_UK}
        ...    AND    set to dictionary  ${CustomSchedule_DM}   &{CustomScheduleDM_UK}
        ...    AND    set to dictionary  ${CustomSchedule_PM}   &{CustomSchedulePM_UK}
        ...    AND    set to dictionary  ${InvoiceDetails}   &{Invoice_UK}
        ...    AND    set to dictionary  ${geolocationDetails}   &{geolocation_UK}
        ...    AND    set to dictionary  ${geolocation_close}   &{geolocation_close_UK}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_UK}

        ...    ELSE IF    '${country}' == 'US'
        ...    Run Keywords
        ...    set to dictionary  ${TestContract}   &{Contract02}
        ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_US}
        ...    AND    set to dictionary  ${CustomSchedule_DM}   &{CustomSchedule_DM_US}
        ...    AND    set to dictionary  ${CustomSchedule_PM}   &{CustomSchedule_PM_US}
        ...    AND    set to dictionary  ${InvoiceDetails}   &{Invoice_US}
        ...    AND    set to dictionary  ${geolocationDetails}   &{geolocation_US}
        ...    AND    set to dictionary  ${geolocation_close}   &{geolocation_close_US}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_US}

        ...    ELSE
        ...    log  Please enter a valid Country name like US, UK or Australia


    : FOR    ${key}    IN    @{TestContract.keys()}
    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{InvoiceDetails.keys()}
    \    ${updated_val}=    Replace String    ${InvoiceDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${InvoiceDetails}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup01}
    : FOR    ${key}    IN    @{Huntgroup01.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup01}    ${key}    ${updated_val}

    Set suite variable    &{ContracttoDelete}
    : FOR    ${key}    IN    @{ContracttoDelete.keys()}
    \    ${updated_val}=    Replace String    ${ContracttoDelete["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${ContracttoDelete}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup02}
    : FOR    ${key}    IN    @{Huntgroup02.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup02}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup03}
    : FOR    ${key}    IN    @{Huntgroup03.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup03}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup04}
    : FOR    ${key}    IN    @{Huntgroup04.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup04["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup04}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup05}
    : FOR    ${key}    IN    @{Huntgroup05.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup05["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup05}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{PartitionDetails.keys()}
    \    ${updated_val}=    Replace String    ${PartitionDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PartitionDetails}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{PhoneNumberDetails.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}

    Set suite variable    &{DMUser}
    : FOR    ${key}    IN    @{DMUser.keys()}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMUser}
    : FOR    ${key}    IN    @{LocPMUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${LocPMUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMUser}
    : FOR    ${key}    IN    @{AccPMUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AccPMUser}    ${key}    ${updated_val}
    ${usr_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    &{DMProfUser}
    : FOR    ${key}    IN    @{DMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${DMProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${DMProfUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMProfUser}
    : FOR    ${key}    IN    @{LocPMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${LocPMProfUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMProfUser}
    : FOR    ${key}    IN    @{AccPMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${AccPMProfUser}    ${key}    ${updated_val}

    Set suite variable    &{BillingProfUser}
    : FOR    ${key}    IN    @{BillingProfUser.keys()}
    \    ${updated_val}=    Replace String    ${BillingProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${BillingProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${BillingProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${BillingProfUser}    ${key}    ${updated_val}

    Set suite variable    &{TechnicalProfUser}
    : FOR    ${key}    IN    @{TechnicalProfUser.keys()}
    \    ${updated_val}=    Replace String    ${TechnicalProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${TechnicalProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${TechnicalProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${TechnicalProfUser}    ${key}    ${updated_val}

    Set suite variable    &{EmergencyProfUser}
    : FOR    ${key}    IN    @{EmergencyProfUser.keys()}
    \    ${updated_val}=    Replace String    ${EmergencyProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${EmergencyProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${EmergencyProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${EmergencyProfUser}    ${key}    ${updated_val}
    ${usr_str2}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    &{LocPMProfPMUser}
    : FOR    ${key}    IN    @{LocPMProfPMUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfPMUser["${key}"]}    {rand_str}    ${usr_str2}
    \    Set To Dictionary    ${LocPMProfPMUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMProfBillingUser}
    : FOR    ${key}    IN    @{LocPMProfBillingUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfBillingUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfBillingUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfBillingUser["${key}"]}    {rand_str}    ${usr_str2}
    \    Set To Dictionary    ${LocPMProfBillingUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMProfTechnicalUser}
    : FOR    ${key}    IN    @{LocPMProfTechnicalUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfTechnicalUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfTechnicalUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfTechnicalUser["${key}"]}    {rand_str}    ${usr_str2}
    \    Set To Dictionary    ${LocPMProfTechnicalUser}    ${key}    ${updated_val}
    ${usr_str3}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    &{AccPMProfPMUser}
    : FOR    ${key}    IN    @{AccPMProfPMUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfPMUser["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${AccPMProfPMUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMProfBillingProfUser}
    : FOR    ${key}    IN    @{AccPMProfBillingProfUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfBillingProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfBillingProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfBillingProfUser["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${AccPMProfBillingProfUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMProfTechnicalProfUser}
    : FOR    ${key}    IN    @{AccPMProfTechnicalProfUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfTechnicalProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfTechnicalProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfTechnicalProfUser["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${AccPMProfTechnicalProfUser}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{geolocationDetails.keys()}
    \    ${updated_val}=    Replace String    ${geolocationDetails["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${geolocationDetails}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${geolocationDetails["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${geolocationDetails}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{geolocation_close.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_close["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${geolocation_close}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${geolocation_close["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${geolocation_close}    ${key}    ${updated_val}

    Set suite variable    &{Invoice02}
    : FOR    ${key}    IN    @{Invoice02.keys()}
    \    ${updated_val}=    Replace String    ${Invoice02["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${Invoice02}    ${key}    ${updated_val}
    ${rand_num}=    Generate Random String    4    12345678

    Set suite variable    &{Huntgroup03}
    : FOR    ${key}    IN    @{Huntgroup03.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup03["${key}"]}    {rand_int}    ${rand_num}
    \    Set To Dictionary    ${Huntgroup03}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{Huntgroup08}
    : FOR    ${key}    IN    @{Huntgroup08.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup08["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${Huntgroup08}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_02}
    : FOR    ${key}    IN    @{AA_02.keys()}
    \    ${updated_val}=    Replace String    ${AA_02["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_02}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_04}
    : FOR    ${key}    IN    @{AA_04.keys()}
    \    ${updated_val}=    Replace String    ${AA_04["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_04}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_07}
    : FOR    ${key}    IN    @{AA_07.keys()}
    \    ${updated_val}=    Replace String    ${AA_07["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_07}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_09}
    : FOR    ${key}    IN    @{AA_09.keys()}
    \    ${updated_val}=    Replace String    ${AA_09["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_09}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_03}
    : FOR    ${key}    IN    @{PG_03.keys()}
    \    ${updated_val}=    Replace String    ${PG_03["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_03}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_04}
    : FOR    ${key}    IN    @{PG_04.keys()}
    \    ${updated_val}=    Replace String    ${PG_04["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_04}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_07}
    : FOR    ${key}    IN    @{PG_07.keys()}
    \    ${updated_val}=    Replace String    ${PG_07["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_07}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_08}
    : FOR    ${key}    IN    @{PG_08.keys()}
    \    ${updated_val}=    Replace String    ${PG_08["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_08}    ${key}    ${updated_val}