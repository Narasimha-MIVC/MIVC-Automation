*** Settings ***
Documentation     BOSS BCO Sanity suite for execution on system that does not require
...               to create Contract,Partition(Single Partition), Site.
...               These variable would be defined in the 'Set Init Env' keyword


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

#BOSS Component
Library           ../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library           PPhoneInterface

*** Test Cases ***
05 Create users and verify that the users are created
    and I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    Then I verify "company_name" contains "Auto"
    When I switch to "users" page

    Log    ${DMUser}    console=yes
    and I add user    &{DMUser}
    Then I verify that User exist in user table    &{DMUser}

   Log    ${LocPMUser}    console=yes
   When I add user    &{LocPMUser}
    Then I verify that User exist in user table    &{LocPMUser}

    Log    ${AccPMUser}    console=yes
    When I add user    &{AccPMUser}
    Then I verify that User exist in user table    &{AccPMUser}
##
##    ${r_str}=    Generate Random String    4    [LETTERS]
##    @{role_list}=    Create List    Billing    Technical    Emergency
##    ${InitUser}=    Copy Dictionary    ${GenUser}
##    : FOR    ${role_name}    IN    @{role_list}
##    \    ${GenUser}=    Copy Dictionary    ${InitUser}
##    \    ${updated_role}=    Replace String    ${GenUser["role"]}    {role}    ${rolename}
##    \    ${updated_uname}=    Replace String    ${GenUser["au_username"]}    {rand_str}    ${updated_role}_${r_str}
##    \    ${updated_bmail}=    Replace String    ${GenUser["au_businessmail"]}    {rand_str}    ${updated_role}_${r_str}
##    \    Set to Dictionary    ${GenUser}    role    ${updated_role}
##    \    Set to Dictionary    ${GenUser}    au_username    ${updated_uname}
##    \    Set to Dictionary    ${GenUser}    au_businessmail    ${updated_bmail}
##    \    Append To List    ${user_list}    ${GenUser}
##    \    When I add user    &{GenUser}
##    \    Then I verify that User exist in user table    &{GenUser}
    and I log off
##
##    #LOGIN AS LOC PM AND CREATE USER
##    When I login to ${KramerURL} with ${LocPMUser["au_username"]} and ${LocPMUser["au_password"]}
##    and I change password to ${KramerPassword}
##
##    When I switch to "users" page
##    ${r_str}=    Generate Random String    4    [LETTERS]
##    @{role_list}=    Create List    Technical    Emergency    Phone Manager
##    : FOR    ${role_name}    IN    @{role_list}
##    \    ${GenUser}=    Copy Dictionary    ${InitUser}
##    \    Log To Console    ${GenUser}
##    \    Log To Console    ${GenUser["au_username"]}
##    \    ${updated_role}=    Replace String    ${GenUser["role"]}    {role}    ${rolename}
#    \    ${updated_uname}=    Replace String    ${GenUser["au_username"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
#    \    ${updated_bmail}=    Replace String    ${GenUser["au_businessmail"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
#
#    \    Set to Dictionary    ${GenUser}    role    ${updated_role}
#    \    Set to Dictionary    ${GenUser}    au_username    ${updated_uname}
#    \    Set to Dictionary    ${GenUser}    au_businessmail    ${updated_bmail}
#    \    When I add user    &{GenUser}
#    \    Then I verify that User exist in user table    &{GenUser}
#    and I log off
#
#    #LOGIN AS ACC PM AND CREATE USER
#    When I login to ${KramerURL} with ${AccPMUser["au_username"]} and ${AccPMUser["au_password"]}
#    and I change password to ${KramerPassword}
#    and I switch to "users" page
#    ${r_str}=    Generate Random String    4    [LETTERS]
#    @{role_list}=    Create List    Technical    Emergency    Phone Manager
#    #${InitUser}=    Copy Dictionary    ${GenUser}
#    : FOR    ${role_name}    IN    @{role_list}
#    \    ${GenUser}=    Copy Dictionary    ${InitUser}
#    \    Log To Console    ${GenUser}
#    \    Log To Console    ${GenUser["au_username"]}
#    \    ${updated_role}=    Replace String    ${GenUser["role"]}    {role}    ${rolename}
#    \    ${updated_uname}=    Replace String    ${GenUser["au_username"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
#    \    ${updated_bmail}=    Replace String    ${GenUser["au_businessmail"]}    {rand_str}    ${updated_role.replace(' ','_')}_${r_str}
#    \    Set to Dictionary    ${GenUser}    role    ${updated_role}
#    \    Log To Console    ${GenUser}
#    \    Set to Dictionary    ${GenUser}    au_username    ${updated_uname}
#    \    Set to Dictionary    ${GenUser}    au_businessmail    ${updated_bmail}
#    \    Log To Console    ${GenUser}
#    \    When I add user    &{GenUser}
##    \    Then I verify that User exist in user table    &{GenUser}

06 Login with Users with different roles and verify the available tabs
##    When I log off
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    Then I verify tabs exist    @{StaffUserTab}
    And I log off
    When I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    Then I verify tabs exist    @{DMUserTab}
    And I log off
    When I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
    Then I verify tabs exist    @{PMUserTab}
    And I log off
    When I login to ${KramerURL} with ${KramerTechUser} and ${KramerPassword}
    Then I verify tabs exist    @{TechnicalUserTab}
    And I log off
    When I login to ${KramerURL} with ${KramerBillUser} and ${KramerPassword}
    Then I verify tabs exist    @{BillingUserTab}
    And I log off
    When I login to ${KramerURL} with ${KramerEmerUser} and ${KramerPassword}
    Then I verify tabs exist    @{EmergencyUserTab}
    And I log off
##    : FOR    ${role_name}    IN    @{user_list}
##    \    Log to console    ${role_name}
##    \    When I login to ${KramerURL} with ${role_name["au_username"]} and ${role_name["au_password"]}
##    \    and I change password to ${KramerPassword}
##    \    Run Keyword If    '${role_name['role']}' == 'Technical'    I verify tabs exist    @{TechnicalUserTab}
##    \    Run Keyword If    '${role_name['role']}' == 'Billing'    I verify tabs exist    @{BillingUserTab}
##    \    Run Keyword If    '${role_name['role']}' == 'emergency'    I verify tabs exist    @{EmergencyUserTab}
##    \    And I log off

07 Login as DM user and create users with profiles
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    and I log off
    and I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    Then I verify "company_name" contains "Auto"

    When I switch to "users" page
    ${phone_num}  ${extn}=    and I add user    &{DMProfUser}
    Set to Dictionary    ${DMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${DMProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{DMProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{DMProfUser}

    When I switch to "users" page
    ${phone_num}  ${extn}=    and I add user    &{LocPMProfUser}
    Set to Dictionary    ${LocPMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfUser}

    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{AccPMProfUser}
    Set to Dictionary    ${AccPMProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfUser}

    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{BillingProfUser}
    Set to Dictionary    ${BillingProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${BillingProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{BillingProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{BillingProfUser}

    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{TechnicalProfUser}
    Set to Dictionary    ${TechnicalProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${TechnicalProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{TechnicalProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{TechnicalProfUser}

    When I switch to "users" page
    ${phone_num}    ${extn}=    I add user    &{EmergencyProfUser}
    Set to Dictionary    ${EmergencyProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${EmergencyProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{EmergencyProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{EmergencyProfUser}
    And I log off

08 Login as Account PM and create users with profiles
    When I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
#    and I change password to ${KramerPassword}
    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{LocPMProfPMUser}
    Set to Dictionary    ${LocPMProfPMUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfPMUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfPMUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfPMUser}
    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{LocPMProfBillingUser}
    Set to Dictionary    ${LocPMProfBillingUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfBillingUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfBillingUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfBillingUser}
    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{LocPMProfTechnicalUser}
    Set to Dictionary    ${LocPMProfTechnicalUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${LocPMProfTechnicalUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{LocPMProfTechnicalUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{LocPMProfTechnicalUser}
    And I log off

09 Login as Account PM and create users with profiles
    When I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
#    and I change password to ${KramerPassword}
#    When I switch to "users" page
    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{AccPMProfPMUser}
    Set to Dictionary    ${AccPMProfPMUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfPMUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfPMUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfPMUser}
    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{AccPMProfBillingProfUser}
    Set to Dictionary    ${AccPMProfBillingProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfBillingProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfBillingProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfBillingProfUser}
    When I switch to "users" page
    ${phone_num}  ${extn}=    I add user    &{AccPMProfTechnicalProfUser}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    ap_phonenumber    ${phone_num}
    Set to Dictionary    ${AccPMProfTechnicalProfUser}    ap_extn    ${extn}
    Then I verify that User exist in user table    &{AccPMProfTechnicalProfUser}
    and I switch to "services" page
    and I verify profile updated in service table    &{AccPMProfTechnicalProfUser}
    And I log off

10 Login as Staff and add invoice group
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    When I switch to "switch_account" page
    And I switch to account ${KramerAccount} with ${AccWithoutLogin} option
    when I switch to "Invoices_and_Payments" page
    and I create invoice group    &{Invoice01}
    Then I move to "tab_invoices_groups" tab
    and I verify grid contains "${Invoice01["invoiceName"]}" value
    When I click on "${Invoice01["invoiceName"]}" link in "invoice_Groups_Grid"
    Then I verify that Invoice group is associated with location    &{Invoice01}
    [Teardown]  run keyword  I log off

11 Login as DM and add emergency hunt group
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    when I switch to "Visual_Call_Flow_Editor" page
    and I create emergency hunt group    &{Invoice01}
    Then I verify location "${Invoice01["Location"]}" with "Registered" state
    And In D2 ${KramerD2IP} I Login With ${KramerD2User} And ${KramerD2Password}
    And in D2 I verify emergency hunt group "Emergency - ${Invoice01['Location']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert


12 Login as PM and add emergency hunt group
    #When I check for alert
    When I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
    and I switch to "geographic_locations" page
    and I create geographic location    &{geolocation01}
    Then I verify location "${geolocation01['Location']}" with "Registered" state
    When I switch to "Visual_Call_Flow_Editor" page
    and I create emergency hunt group    &{geolocation01}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify emergency hunt group "Emergency - ${geolocation01['Location']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert

23 Create Extension list
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${KramerACCDMExt}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    #And I log off
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And In D2 I verify extension list "${Extensionlist01['extnlistname']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert
    ...                       And I log off

13 Login as DM and create Hunt group with mandatory inputs

    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup01}    hglocation    ${KramerLoc}
    ${extn_num}=    Then I create hunt group    &{Huntgroup01}
    Set to Dictionary    ${Huntgroup01}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup01['HGname']}" with extension "${Huntgroup01['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert

14 As DM create Hunt group with mandatory inputs + group members
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup02}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup02}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup02}
    Set to Dictionary    ${Huntgroup02}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup02['HGname']}" with extension "${Huntgroup02['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert

15 As DM create Hunt group with mandatory inputs + group members + custom extension
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup03}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup03}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    I create hunt group    &{Huntgroup03}
    Set to Dictionary    ${Huntgroup03}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup03['HGname']}" with extension "${Huntgroup03['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert

16 As DM create Hunt group with mandatory inputs + group members + private extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup04}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup04}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup04}
    Set to Dictionary    ${Huntgroup04}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup04['HGname']}" with extension "${Huntgroup04['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I check for alert
    ...                       I switch to "Visual_Call_Flow_Editor" page
    ...                       I check for alert


17 As DM create Hunt group with mandatory inputs + group members + Phone number
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup05}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup05}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup05}
    Set to Dictionary    ${Huntgroup05}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup05['HGname']}" with extension "${Huntgroup05['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert

18 Login as PM and create Hunt group with mandatory inputs
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPMUser} and ${KramerPassword}
    when I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup06}    hglocation    ${KramerLoc}
    ${extn_num}=    Then I create hunt group    &{Huntgroup06}
    Set to Dictionary    ${Huntgroup06}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup06['HGname']}" with extension "${Huntgroup06['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

19 As PM create Hunt group with mandatory inputs + group members
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup07}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup07}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup07}
    Set to Dictionary    ${Huntgroup07}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup07['HGname']}" with extension "${Huntgroup07['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

20 As PM create Hunt group with mandatory inputs + group members + custom extension
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup08}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup08}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup08}
    Set to Dictionary    ${Huntgroup08}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup08['HGname']}" with extension "${Huntgroup08['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

21 As PM create Hunt group with mandatory inputs + group members + private extension
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup09}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup09}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup09}
    Set to Dictionary    ${Huntgroup09}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup09['HGname']}" with extension "${Huntgroup09['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

22 As PM create Hunt group with mandatory inputs + group members + Phone number
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Huntgroup10}    hglocation    ${KramerLoc}
    Set to Dictionary    ${Huntgroup10}    grp_member    ${KramerACCDMExt}
    ${extn_num}=    Then I create hunt group    &{Huntgroup10}
    Set to Dictionary    ${Huntgroup10}    HGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify hunt group "${Huntgroup10['HGname']}" with extension "${Huntgroup10['HGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert

24 Login as DM and create Pickup group
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup01}    pickuploc    ${KramerLoc}
    ${extn_num}=    I create pickup group    &{Pickupgroup01}
    Set to Dictionary    ${Pickupgroup01}    PGExtn    ${extn_num}
    log to console    ${Pickupgroup01}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify pickup group "${Pickupgroup01['pickupgpname']}" with extension "${Pickupgroup01['PGExtn']}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert

25 Login as PM and create Pickup group
    #When I check for alert
    When I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${Pickupgroup02}    pickuploc    ${KramerLoc}
    ${extn_num}=    I create pickup group    &{Pickupgroup02}
    Set to Dictionary    ${Pickupgroup02}    PGExtn    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    And in D2 I verify pickup group "${Pickupgroup02['pickupgpname']}" with extension "${Pickupgroup02['PGExtn']}" is set for "${KramerACCDMName}"
    #And I log off
    [Teardown]  run keywords  I log off
    ...                      I check for alert

26 Login as DM to the boss portal and add an auto-attendant with default values
    When I check for alert
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_01["Aa_Name"]}" with extension "${AA_01["AA_Extension"]}" is set for "${KramerACCDMName}"


27 Login as DM to the boss portal and add an auto-attendant with custom-extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_02}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_02["Aa_Name"]}" with extension "${AA_02["AA_customExtension"]}" is set for "${KramerACCDMName}"

28 Login as DM to the boss portal and add an auto-attendant with extension labeled private
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_03}
    Set to Dictionary    ${AA_03}    AA_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_03["Aa_Name"]}" with extension "${AA_03["AA_Extension"]}" is set for "${KramerACCDMName}"

29 Login as DM to the boss portal and add an auto-attendant with extension labled private and having a custom extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_04}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_04["Aa_Name"]}" with extension "${AA_04["AA_customExtension"]}" is set for "${KramerACCDMName}"

30 Login as DM to the boss portal and add an auto-attendant and assign a DID
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_05}
    Set to Dictionary    ${AA_05}    AA_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_05["Aa_Name"]}" with extension "${AA_05["AA_Extension"]}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert

31 Login as PM to the boss portal and add an auto-attendant with default values
    When I check for alert
    Given I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_06}
    Set to Dictionary    ${AA_06}    AA_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_06["Aa_Name"]}" with extension "${AA_06["AA_Extension"]}" is set for "${KramerACCDMName}"

32 As PM to the boss portal and add an auto-attendant with custom-extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_07}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_07["Aa_Name"]}" with extension "${AA_07["AA_customExtension"]}" is set for "${KramerACCDMName}"

33 Login as PM to the boss portal and add an auto-attendant with extension labeled private
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_08}
    Set to Dictionary    ${AA_08}    AA_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_08["Aa_Name"]}" with extension "${AA_08["AA_Extension"]}" is set for "${KramerACCDMName}"

34 Login as PM to the boss portal and add an auto-attendant with extension labled private and having a custom extension
    When I check for alert
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_09}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_09["Aa_Name"]}" with extension "${AA_09["AA_customExtension"]}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I switch to "Visual_Call_Flow_Editor" page
    ...                      I check for alert

35 Login as PM to the boss portal and add an auto-attendant and assign a DID
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Auto-Attendant    &{AA_10}
    Set to Dictionary    ${AA_10}    AA_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify AA "${AA_10["Aa_Name"]}" with extension "${AA_10["AA_Extension"]}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords  I log off
    ...                      I check for alert

36 As a DM create custom schedule
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule01}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    Then In D2 I verify custom schedule "${CustomSchedule01["customScheduleName"]}" is set for ${KramerACCDMName}
    #And I log off
    [Teardown]  run keywords  I log off
    ...                      I check for alert

37 As a PM create custom schedule
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
	when I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule02}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and In D2 I verify custom schedule "${CustomSchedule02["customScheduleName"]}" is set for ${KramerACCDMName}
    #And I log off
    [Teardown]  run keywords  I log off
    ...                      I check for alert

38 Login as DM to the boss portal and add an paging-group with default values
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerACCDMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_01}
    Set to Dictionary    ${Pg_01}    Pg_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_01["Pg_Name"]}" with extension "${Pg_01["Pg_Extension"]}" is set for "${KramerACCDMName}"
    [Teardown]  run keywords           I check for alert

39 Login as DM to the boss portal and add an paging-group with private extension
    #When I check for alert
    #Given I login to ${KramerURL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_02}
    Set to Dictionary    ${Pg_02}    Pg_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_02["Pg_Name"]}" with extension "${Pg_02["Pg_Extension"]}" is set for "${KramerACCDMName}"

40 Login as DM to the boss portal and add an paging-group with custom extension
    When I check for alert
    #Given I login to ${KramerURL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_03}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_03["Pg_Name"]}" with extension "${Pg_03["Pg_Extension"]}" is set for "${KramerACCDMName}"

41 Login as DM to the boss portal and add an paging-group with custom extension and private extension
    #When I check for alert
    #Given I login to ${KramerURL} with ${Contract01["email"]} and ${Contract01["password"]}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_04}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_04["Pg_Name"]}" with extension "${Pg_04["Pg_Extension"]}" is set for "${KramerACCDMName}"
    And I log off

42 Login as PM to the boss portal and add an paging-group with default values
    When I check for alert
    Given I login to ${KramerURL} with ${KramerACCPMUser} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_05}
    Set to Dictionary    ${Pg_05}    Pg_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_05["Pg_Name"]}" with extension "${Pg_05["Pg_Extension"]}" is set for "${KramerACCDMName}"

43 Login as PM to the boss portal and add an paging-group with private extension
    When I check for alert
    #Given I login to ${KramerURL} with "pm1@user1.com" and "zaqwsx123!@#$"
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_06}
    Set to Dictionary    ${Pg_06}    Pg_Extension    ${extn_num}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_06["Pg_Name"]}" with extension "${Pg_06["Pg_Extension"]}" is set for "${KramerACCDMName}"

44 Login as PM to the boss portal and add an paging-group with custom extension
    When I check for alert
    #Given I login to ${KramerURL} with "pm1@user1.com" and "zaqwsx123!@#$"
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_07}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_07["Pg_Name"]}" with extension "${Pg_07["Pg_Extension"]}" is set for "${KramerACCDMName}"

45 Login as PM to the boss portal and add an paging-group with custom extension and private extension
    #When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPM['user']} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    And I add Paging Group    &{Pg_08}
    Then In D2 ${KramerD2IP} I login with ${KramerD2User} and ${KramerD2Password}
    and in D2 I verify PG "${Pg_08["Pg_Name"]}" with extension "${Pg_08["Pg_Extension"]}" is set for "${KramerACCDMName}"
    And I log off

46 Reset the login password by right clicking on user
    When I check for alert
    Given I login to ${KramerURL} with ${KramerAccPM['user']} and ${KramerPassword}
    When I switch to "users" page
    and I go to change password page for user "${KramerAccPM['first']} ${KramerAccPM['last']}"
    then I change password to ${KramerAccPM['temp_password']}
    and I log off
    then I login to ${KramerURL} with ${KramerAccPM['user']} and ${KramerAccPM['temp_password']}
    and I log off

47 Reset password from user profile page
    Given I login to ${KramerURL} with ${KramerAccPM['user']} and ${KramerAccPM['temp_password']}
    When I switch to "users" page
    then I click on user name and go to password change page "${KramerAccPM['first']} ${KramerAccPM['last']}"
    and I update password to ${KramerPassword} from ${KramerAccPM['temp_password']}
    and I log off

48 Reset password from home page
    #In QA setup
    Given I open login page with ${KramerURL}
    And I change password from home page  &{emailDetail}
    then I login to ${KramerURL} with ${emailDetail['emailToReset']} and ${emailDetail['setPassword']}
    and I log off
    And I change password from home page  &{emailDetail1}

49 Close user
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    and I switch to "switch_account" page
    then I switch to account ${KramerAccount} with ${AccWithoutLogin} option
    then I switch to "users" page
    When I delete user ${LocPMUser["au_username"]} as user "${KramerFirstName} ${KramerLastName}"
    and I log off
    ##[Teardown]  run keywords  I log off

50 Login as PM and delete VCFE Component
    Given I login to ${KramerURL} with ${KramerAccPM['user']} and ${KramerPassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I delete VCFE entry with name "${Huntgroup01['HGname']}" and extn "${Huntgroup01['HGExtn']}"
    Then I verify if VCFE entries with name "${Huntgroup01['HGname']}" and extn "${Huntgroup01['HGExtn']}" are deleted
    #and I log off
    [Teardown]  run keywords  I log off

51 Login to BOSS as DM and add a Silent Coach with default values
    Given I login to ${KramerURL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    set to dictionary  ${proginfo01}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo01}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo01}
    #And I add prog button "Silent Monitor" with extension "7932" and email "${Contract01["email"]}"
    #And I log off
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
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	log to console  ${btninfo}
	List should contain value   ${btninfo}    ${proginfo01["longlabel"]}
	Pphone handset disconnect call	   ${Phone01}
	Pphone Handset Down	${Phone03}
	Pphone Force Idle State	${Phone01}   ${Phone02}   ${Phone03}

52 Login to BOSS as DM and add a Silent Monitor with default values
    #Given I login to ${KramerURL} with ${Contract01["email"]} and ${Contract01["password"]}
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
    Given I login to ${KramerURL} with ${Contract01["email"]} and ${Contract01["password"]}
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
    #Given I login to ${KramerURL} with ${Contract01["email"]} and ${Contract01["password"]}
    set to dictionary  ${proginfo07}    extension  ${Phone02["extension"]}
    set to dictionary  ${proginfo07}    user_email  ${phoneDMUser01["user_email"]}
    And I add prog button    &{proginfo07}
    Log		Using handset device for validation
    ${btninfo}=    pphone get progbutton info    ${Phone03}    1
	 log to console  ${btninfo}
	 List should contain value   ${btninfo}    ${proginfo07["longlabel"]}
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
    And I log off
    #[Teardown]  run keywords  I log off

55 Login to BOSS as PM and add a Silent Coach with default values
    Given I login to ${KramerURL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}

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
    #Given I login to ${KramerURL} with ${Contract04["email"]} and ${Contract04["password"]}
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
    #Given I login to ${KramerURL} with ${Contract04["email"]} and ${Contract04["password"]}
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
   #Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
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
   And I log off
  # [Teardown]  run keywords  I log off

59 Close geo location
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    and I switch to "switch_account" page
    and I switch to account ${KramerAccount} with ${AccWithoutLogin} option
    then I switch to "geographic_locations" page
    then I create geographic location    &{geolocation02}
    then I switch to "order" page
    and I close open order
    then I switch to "geographic_locations" page
    and I close the location
    and i log off
    #[Teardown]  run keywords  I log off

60 Login as staff user and delete contract
    Given I login to ${KramerURL} with ${KramerStaffUser} and ${KramerPassword}
    and I switch to "switch_account" page
    When I switch to account ${KramerACCDMUser} with ${AccWithoutLogin} option
    When I switch to "contracts" page
    And I delete contract "${KramerACCDMUser}"
    Then I verify contract "${KramerACCDMUser}" is deleted
    [Teardown]  run keywords  I log off

*** Keywords ***
Set Init Env
    @{user_list}=    Create list
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    @{user_list}
    Set suite variable    &{Contract02}

    #User Configuration on Boss Portal
    set to dictionary  ${Contract02}      email     ${KramerACCDMUser}
    set to dictionary  ${Contract02}      accountName       ${KramerAccount}
    set to dictionary  ${Contract02}      locationName      ${KramerLoc}
    set to dictionary  ${Contract02}      location      ${KramerLoc}

    : FOR    ${key}    IN    @{Contract02.keys()}
    \    ${updated_val}=    Replace String    ${Contract02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Contract02}    ${key}    ${updated_val}

    Set suite variable    &{Invoice01}
    : FOR    ${key}    IN    @{Invoice01.keys()}
    \    ${updated_val}=    Replace String    ${Invoice01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Invoice01}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup01}
    : FOR    ${key}    IN    @{Huntgroup01.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup01}    ${key}    ${updated_val}

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

    Set suite variable    &{Partition01}
    : FOR    ${key}    IN    @{Partition01.keys()}
    \    ${updated_val}=    Replace String    ${Partition01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Partition01}    ${key}    ${updated_val}

    Set suite variable    &{PhoneNumber01}
    : FOR    ${key}    IN    @{PhoneNumber01.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumber01["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumber01}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${PhoneNumber01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PhoneNumber01}    ${key}    ${updated_val}

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

    Set suite variable    &{geolocation01}
    : FOR    ${key}    IN    @{geolocation01.keys()}
    \    ${updated_val}=    Replace String    ${geolocation01["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${geolocation01}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${geolocation01["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${geolocation01}    ${key}    ${updated_val}

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