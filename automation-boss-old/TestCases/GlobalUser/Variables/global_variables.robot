*** Variables ***
#AccountDetails
#${accountName1}    AutoTest_Acc_JgmrbI2y
#Contract
&{Contract_GU}	  accountType=New Customer   accountName=AutoTest_Acc_{rand_str}   salesPerson=Staff User   platformType=Connect Cloud   country=United States   firstName=boss   lastName=automation   password=Abc123!!   confirmPassword=Abc123!!   email=AutoTest_{rand_str}@shoretel.com   locationName=AutoTest_location_{rand_str}   Address1=1385 Broadway   city=New York   state=New York   zip=10018   connectivity=This Location  no_validation=False  class=bundle  product=Connect CLOUD Standard   quantity=1   location=AutoTest_location_{rand_str}   MRR=12   NRR=23   class01=projectmgt   product01=Global User TN Service   quantity01=1   location01=AutoTest_location_{rand_str}   MRR01=12   NRR01=23   contractNumber=369   forecastDate=today   notes=Not Required   filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf   termVersion=Version 3.0   termLength=36 Months   termRenewalType=Automatic   termInstall=90 Days

#PhoneNumber
&{PhoneNumber_US}	 numberRange=16462{rand_int}   range=1    serviceUsage=Telephone Number Turnup    tn_type=client   clientAccount=GlobalUsersAutomation    clientLocation=loc   vendor=212803-dash    vendorOrderNumber=1234    requestedBy=Automation Users   requestSource=Email    state=Available
&{PhoneNumber_Global}	 numberRange=61433{rand_int}   range=1    serviceUsage=Global User Number Turnup    tn_type=client   clientAccount=GlobalUsersAutomation   clientLocation=loc   vendor=21803-Voxbone    vendorOrderNumber=1234    requestedBy=Automation Users   requestSource=Email    state=Available

#Users
# Modified By: Palla Surya Kumar
# removed hardcoded values ,so they can be given at test case level
&{DMUser}    au_firstname=autotestdm{rand_str}   au_lastname=Auto    au_businessmail=boss_auto_dm_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=    au_location=   au_username=boss_auto_dm_{rand_str}@shoretel.com    au_password=Shoretel1$     au_confirmpassword=Shoretel1$   ap_phonetype=MiCloud Connect Essentials     ap_phonenumber=random    ap_activationdate=today    hw_addhwphone=False    hw_type=Sale New    hw_model=ShoreTel IP420g - Sale     hw_power=False    hw_power_type=ShoreTel IP Phones Power Supply - Sale    role=Decision Maker   scope=Account   request_by=    request_source=Email
&{LocPMUser}    au_firstname=auto_test_locpm_{rand_str}   au_lastname=Auto    au_businessmail=boss_auto_locpm_{rand_str}@shoretel.com  au_userlocation=     au_username=boss_auto_locpm_{rand_str}@shoretel.com    au_password=Shoretel1$     au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials     ap_phonenumber=random    ap_activationdate=today       hw_addhwphone=False    hw_type=Sale New    hw_model=ShoreTel IP420g - Sale     hw_power=False    hw_power_type=ShoreTel IP Phones Power Supply - Sale    role=Phone Manager    scope=Account   request_by=    request_source=Email


#mobilityAdd
&{add_mobility_addon}       gu_name=Newzealand user2
&{add_mobility_profile}       gu_name=Newzealand user1          feature_name=Connect CLOUD Mobility      activationDate=today
&{add_user_global}       au_firstname=auto_test_dm_{rand_str}   au_lastname=Auto    au_businessmail=boss_auto_dm_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=Australia    au_location=location2   au_username=boss_auto_dm_{rand_str}@shoretel.com    au_password=Shoretel1$     au_confirmpassword=Shoretel1$   ap_phonetype=Connect CLOUD Essentials     ap_phonenumber=random    ap_activationdate=today

#Turnupservice
&{globalservice}       serviceName=Global User Number Turnup

#user-> swap
&{globaluser_swap}          username=Newzealand user2

#Global TN service
&{globaluser_service}       servicename=Global User TN Service

#GlobalUser user service
&{globaluser_userservice}       servicename=Global User Service      servicestatus=Active

#globalUser_location verification
# changed the name so it will be uniques
&{testglobaluser_location}       username=Newzealand user2        country=NewZealand

#close global user
&{globaluser_close_yes}          email=canada@user1.com      name=DM User       keepGlobalTn=yes
&{globaluser_close_no}           email=canada@user2.com      name=DM User       keepGlobalTn=no

#close global service
&{globaluser_close_service}      serviceName=Global User Service      serviceStatus=Active     name=DM User

#void global user
&{globaluser_void}       serviceName=Global User service      serviceStatus=Provisioning        newStatus=VOID         keepGlobalTn=no        expectedTnStatus=Turned Down

#Instances
&{Instances}        smr_instance_name=ERTSMR

# below variable is referred by existing test case , but not mentioned in any avriable file,so adding here
#Global countries list
${global_countries}    ['Australia']