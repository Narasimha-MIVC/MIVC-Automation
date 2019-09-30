*** Settings ***
Documentation    Enable and then disable Scribe for ST and cloud users
...              Prasanna

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot
Resource           ../../RobotKeywords/std2/std2Keywords.robot

#Variable files
# Resource           ../../Variables/EnvVariables.robot
Resource           ../../Variables/EnvVariables_Hybrid.robot
Variables          Variables/Hybridsite_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
264905_Enable Scribe for ST user and cloud user
    [Tags]    DEBUG

    #1. log into BOSS portal
    # &{login}=  copy dictionary  ${Login_Info}
    set to dictionary  ${login}  url  ${URL}
    set to dictionary  ${login}  username  ${bossUsername}
    set to dictionary  ${login}  password  ${bossPassword}

    Given I login using separate tab  ${login}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    sleep  5s

    #2. move to phone system -> on site partition -> Add-on feature
    ${Partition}=  set variable  (BOSS_AUTO_HYB_PREM) BOSS_AUTO_HYB_PREM
    And I switch to "Add-on Features" in partition ${Partition}
    sleep  5s

    #3. Add hybrid scribe users
    # @{users}=  create list
    # append to list  ${users}  abcd st
    &{user_info}=  copy dictionary  ${On_Site_User_Info}
    # set to dictionary  ${user_info}  Users  ${users}
    set to dictionary  ${user_info}  Req_By  DM User
    set to dictionary  ${user_info}  Req_Src  Email

    And I add hybrid scribe users  ${user_info}
    log many  ${user_info}
    @{u}=  copy list  &{user_info}[Users]
    set list value  ${users}  0  @{u}[0]
    log  @{users}[0]

   #4. log into ST D2 (in a different TAB on the browser)
    set to dictionary  ${login}  url  ${STD2IP}
    set to dictionary  ${login}  username  ${STD2User}
    set to dictionary  ${login}  password  ${STD2Password}
    set to dictionary  ${login}  NewTab  ${True}
    set to dictionary  ${login}  TabName  T1

    When I login using separate tab  ${login}

    #5. Switch to "Administration/System/Hybrid/synchronization" page on STD2 and synchronize
    And I switch to "Administration/System/Hybrid/Synchronization" page on std2
    And I sync now data between STD2 and Boss
    sleep  5

    #5. Switch to "Administration/System/Hybrid/Services" page on STD2 and do operations
    And I switch to "Administration/System/Hybrid/Services" page on std2

    #6. verify the status of Hybrid Services
    &{service1}=  create dictionary  name=Connect HYBRID Scribe  status=Enabled
    &{service2}=  create dictionary  name=Connect HYBRID Fax  status=Disabled
    &{service3}=  create dictionary  name=Connect HYBRID Sites  status=Enabled
    &{hybrid_services_status}=  create dictionary  service1=${service1}
    ...  service2=${service2}  service3=${service3}

    #6. Verifying the status of the services
    And I verify the status of the hybrid services  &{hybrid_services_status}

    #7. Verify the status of services on Maintenance -> Hybrid -> Services page
    # And I switch to "Maintenance/Topology" page on std2
    And I switch to "Maintenance/Hybrid/Services" page on std2
    &{service1}=  create dictionary  name=Connect HYBRID Scribe  activated=${True}  active_users=${True}
    &{service2}=  create dictionary  name=Connect HYBRID Fax  activated=${False}  active_users=${False}
    &{service3}=  create dictionary  name=Connect HYBRID Sites  activated=${True}  active_users=${True}
    &{hybrid_services_status}=  create dictionary  service1=${service1}
    ...  service2=${service2}  service3=${service3}

    And I verify hybrid services activation status and number of active users  &{hybrid_services_status}

    ## The following test case will close the service on the BOSS portal. So this is a continuation

264926_Disable Scribe for ST user and cloud user
    [Tags]    DEBUG

    log  @{users}[0]
    ${parent}=  set variable  @{users}[0]
    #8. Navigate back to BOSS portal
    set to dictionary  ${login}  TabName  main_page
    I switch tab on browser  ${login}

    sleep  5s
    #9. Disble the scribe that was added in step 3
    Then I switch to "services" page
    &{service_info}=  create dictionary  serviceName=Connect HYBRID Scribe
    ...  serviceStatus=Active  parent=${parent}  requested_by=DM User  request_source=Email
    And I close services  &{service_info}

*** Keywords ***
Provided precondition
#    Setup system under test

Set Init Env
    &{login}=  copy dictionary  ${Login_Info}
    set suite variable  ${login}

    @{users}=  create list  ${None}  ${None}
    set suite variable  ${users}