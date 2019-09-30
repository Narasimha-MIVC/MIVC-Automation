*** Settings ***
Library  String
Library	   OperatingSystem

*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.196.7.182/
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster}            PTA
${platform}               COSMO
${BROWSER}                chrome
${country}                US    #Australia or US or UK
${AccName}                   Maha_UMS
${AccId}                  11553
#${AccLocation}
${AccWithoutLogin}        --> Switch account without logging in as someone else
${locationName}           maha123
${AA_DID}             1 (408) 610-5679

#NewlycreatedTenant Details
${NewAccId}                   11886
${NewAccName}                   Maha_UMS
##This is used 6 PTA Users Paramaters
&{Phone01}  ip=10.198.32.144  extension=2490  phone_type=p8cg  PPhone_mac=001049454AC4  first_name=auto1  last_name=maha  vm_password=123456  did=140849511
&{Phone02}  ip=10.198.32.216  extension=2491  phone_type=p8cg  PPhone_mac=00104940F668  first_name=auto2  last_name=maha  vm_password=11553  did=14084952412
&{Phone03}  ip=10.198.33.118  extension=2492  phone_type=p8cg  PPhone_mac=001049454AE9  first_name=auto3  last_name=maha  vm_password=123456  did=14084952413
&{Phone04}  ip=10.198.32.189  extension=2493  phone_type=p8cg  PPhone_mac=001049454ABE  first_name=auto4  last_name=maha  vm_password=123456  did=14084952414
&{Phone05}  ip=10.198.32.220  extension=2494  phone_type=p8cg  PPhone_mac=001049454ADC  first_name=auto5  last_name=maha  vm_password=123456  did=14084952415
&{Phone06}  ip=10.198.33.250  extension=2495  phone_type=p8cg  PPhone_mac=001049337155  first_name=auto6  last_name=maha  vm_password=123456  did=14084952416

#This is used for New user addition
&{Phone001}  ip=10.198.18.3  extension=2468  phone_type=p8cg  PPhone_mac=001049454AB9  first_name=autotestETJ2LwjB  last_name=Auto  vm_password=123456  did=1 (408) 495-2468

#This is used for did user
&{Phone_did_01}  ip=10.198.32.220  extension=2494  phone_type=p8cg  PPhone_mac=001049454ADC  first_name=auto5  last_name=maha  vm_password=123456  did=14086107659
&{Phone_did_02}  ip=10.198.18.3  extension=2007  phone_type=p8cg  PPhone_mac=001049454AB9  first_name=maha     last_name=did  vm_password=123456  did=14086107657

#This is used for Cases to Run with New User , Jusy copy Phone01 Parameter Value
&{PhoneTemp}  ip=10.198.32.144  PPhone_mac=001049454AC4  phone_type=p8cg  first_name=auto1  last_name=maha  extension=2490

#Enter Current Account location and Requested BY field Values
&{OldGenUser}  au_firstname=tt{rand_str}  au_lastname=Auto  au_businessmail=boss_auto_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=maha123  au_location=maha123  au_username=boss_auto_{rand_str}@shoretel.com  au_password=Shoretel1$  au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials  ap_phonenumber=random  ap_activationdate=today  hw_addhwphone=False  hw_type=Sale  hw_model=ShoreTel IP420g - Sale  hw_power=False  hw_power_type=ShoreTel IP Phones Power Supply - Sale  role=Technical  request_source=Email  userGroupName=SystemUserGrop_DM_3185  request_by=maha ums

#It used for BOSS Cases, Chnage values only for ()
&{Contract}	  accountType=New Customer  accountName=AutoTest_Acc_{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=United States  firstName=DM1_{rand_str}  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}  Address1=1385 Broadway  city=New York  state=New York  zip=10018  connectivity=This Location  no_validation=False  class=bundle  product=MiCloud Connect Essentials  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=C:\\ATF_ROBOT\\automation-boss\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{PhoneNumber}  numberRange=16462{rand_int}  range=10  serviceUsage=Telephone Number turnup  tn_type=client  clientAccount=AutoTest_Acc_iAN2lNtB  clientLocation=AutoTest_location_iAN2lNtB  vendor=212803-dash  vendorOrderNumber=1234  requestedBy=DM1_iAN2lNtB automation  requestSource=Email  state=Available  numberStart=16462978900
&{GenUser}  au_firstname=autotest{rand_str}  au_lastname=Auto  au_businessmail=boss_auto_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=AutoTest_location_iAN2lNtB  au_location=AutoTest_location_iAN2lNtB  au_username=boss_auto_{rand_str}@shoretel.com  au_password=Shoretel1$  au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials  ap_phonenumber=random  ap_activationdate=today  hw_addhwphone=False  hw_type=Sale  hw_model=ShoreTel IP420g - Sale  hw_power=False  hw_power_type=ShoreTel IP Phones Power Supply - Sale  role=Technical  DM1_pDv11b6C automationrDM1_pDv11b6C automationeDM1_pDv11b6C automationqDM1_pDv11b6C automationuDM1_pDv11b6C automationeDM1_pDv11b6C automationsDM1_pDv11b6C automationtDM1_pDv11b6C automation_DM1_pDv11b6C automationbDM1_pDv11b6C automationyDM1_pDv11b6C automation=DM1_pDv11b6C automation  request_source=Email  userGroupName=SystemUserGrop_DM_W6jFHh0S  request_by=DM1_iAN2lNtB automation
&{Usergroup_staff}	 userGroupName=SystemUserGrop_DM_{rand_str}    profileType=Managed    holdMusic=Default Music    directedIntercom=InitiateAndReceive    whisperPage=InitiateAndReceive    Barge=InitiateAndReceive    silentMonitor=InitiateAndReceive    classOfService=International    accountCodeMode=Required
&{AA_01}    Aa_Name=Test_AA     Aa_Location=random
&{EditAA04}    Assign_vcfe_component=     Assign_vcfe_Name=     Location=    Aa_Name=    MDT=    Aa_Extn=     prompt=   verify_interactive_diagram=     neg=False   filePath=${EXECDIR}${/}Test_files${/}AA-audio.wav  Remove_Operations=  Monitor=    Multiple_Digit_Operation=   MDO_Extension=   Adjust_Timeout=
&{Huntgroup}  hglocation=random   HGBckupExtn=5501  first_name=Boss_HG   HGExtn=   grp_member=  HGname=Boss_HG  hg_phonenumber=random  Rings_per_Member=3  No_answer_number_of_rings=6
&{Extensionlist01} 	 extnlistname=Boss_ExtnList_01      extnNumber=
&{PagingGroup}       Pg_Name=Boss_Paging      extnlistname=   Pg_Location=random
&{Pickupgroup01}	extnlistname=  pickupgpname=Boss_Pickup_01  PGExtn=     pickuploc=None


#CSV Varibales  - Client Cases
${CSVFileName}          USERS.csv
${csvfname}             first_name
${csvlname}             last_name
${csvextn}              extension
${csvmac}               mac
${csvemail}             client_email
${csvcid}               client_id
${csvptype}             phone_model