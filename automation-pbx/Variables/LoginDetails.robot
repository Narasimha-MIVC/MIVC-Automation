*** Settings ***
Library  String
Library	   OperatingSystem

*** Variables ***
${file_to_be_update}	LoginDetails.robot
#BOSS PORTAL INFO
${D2IP}                         10.211.44.90

#Auto-Attendant details

${AAExtn}             41875
${AADID}			 98066839210
${AAName}            Nara-HG

#Hunt grp details
${HGExtn}             41876
${HGName}            Nara-HG

#${AA_DID}                  1 (408) 495-2416
#${Call_AA_DID}             14084952416
#${RPIP}                  10.196.7.181
${stopcmd}                ./stopstts.sh
${startcmd}               ./startstts.sh


##This is used 6  Users Paramaters
&{Phone06}  phoneModel=Mitel6910  ipAddress=10.211.46.26  phoneName=Nara 6910  extensionNumber=41704   trunkISDN=14087138017  authCode=123456
&{Phone03}  phoneModel=Mitel6940  ipAddress=10.211.46.56  phoneName=Nara 6940  extensionNumber=41000   trunkISDN=14087138016  authCode=123456
&{Phone05}  phoneModel=Mitel6940  ipAddress=10.211.46.127  phoneName=Testing Nara  extensionNumber=41913   trunkISDN=14087138016  authCode=123456
&{Phone07}  phoneModel=Mitel6920  ipAddress=10.211.46.57  phoneName=Test Nara  extensionNumber=41916   trunkISDN=918066839208  authCode=123456
&{Phone02}  phoneModel=Mitel6930  ipAddress=10.211.46.46  phoneName=Automation 6930  extensionNumber=98066839208   trunkISDN=918066839208  authCode=123456
&{Phone01}  phoneModel=Mitel6920  ipAddress=10.211.46.189  phoneName=Automation 6920  extensionNumber=41815   trunkISDN=14087138008  authCode=123456
&{Phone04}  phoneModel=phone_4xx  ip=10.211.46.36  phoneName=Narasimha MIVC  extension=41709  phone_model=p8cg  PPhone_mac=00104933729A  hq_rsa=hq_rsa  vm_password=12345  did=14087138009
&{Phone08}  phoneModel=phone_4xx  ip=10.211.46.42  phoneName=Nara 6930  extension=41821  phone_model=p8cg  PPhone_mac=0010493f1919  hq_rsa=hq_rsa  vm_password=1234  did=14087138009

#This is used for New user addition
#&{Phone001}  ip=10.198.17.5  extension=2468  phone_type=p8cg  PPhone_mac=001049454A7C  first_name=autotestETJ2LwjB  last_name=Auto  vm_password=123456  did=1 (408) 495-2468  email=auto1@maha.com
&{Phone001}   phoneModel=Mitel6940  ipAddress=10.198.33.117  phoneName=Auto user17  extensionNumber=8017   macAddress=08000FC70E35

#This is used for did user
&{Phone_did_01}  phoneModel=Mitel6920  ipAddress=10.211.46.189  phoneName=Automation 6920  extensionNumber=41815   trunkISDN=14087138008
&{Phone_did_02}  phoneModel=Mitel6930  ipAddress=10.211.46.46   phoneName=Automation 6930  extensionNumber=41814    trunkISDN=8066839210

#This is used for Cases to Run with New User , Jusy copy Phone01 Parameter Value
&{PhoneTemp}  ip=10.198.32.144  extension=2490  phone_type=p8cg  PPhone_mac=001049454AC4  first_name=auto1  last_name=maha  vm_password=123456  did=140849511  email=auto1@maha.com

#Enter Current Account location and Requested BY field Values
#&{Contract}	  accountType=New Customer  accountName=AutoTest_Acc_{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=United States  firstName=DM1_{rand_str}  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}  Address1=1385 Broadway  city=New York  state=New York  zip=10018  connectivity=This Location  no_validation=False  class=bundle  product=MiCloud Connect Essentials  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=C:\\ATF_ROBOT\\automation-boss\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
#&{PhoneNumber}  numberRange=16462{rand_int}  range=10  serviceUsage=Telephone Number turnup  tn_type=client  clientAccount=AutoTest_Acc_7BXTKACQ  clientLocation=AutoTest_location_7BXTKACQ  vendor=212803-dash  vendorOrderNumber=1234  requestedBy=DM1_7BXTKACQ automation  requestSource=Email  state=Available  numberStart=16462599096  au_firstname=autotest{rand_str}  au_lastname=Auto  au_businessmail=boss_auto_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=AutoTest_location_igibZK3O  au_location=AutoTest_location_igibZK3O  au_username=boss_auto_{rand_str}@shoretel.com  au_password=Shoretel1$  au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials  ap_phonenumber=random  ap_activationdate=today  hw_addhwphone=False  hw_type=Sale  hw_model=ShoreTel IP420g - Sale  hw_power=False  hw_power_type=ShoreTel IP Phones Power Supply - Sale  role=Technical  DM1_pDv11b6C automationrDM1_pDv11b6C automationeDM1_pDv11b6C automationqDM1_pDv11b6C automationuDM1_pDv11b6C automationeDM1_pDv11b6C automationsDM1_pDv11b6C automationtDM1_pDv11b6C automation_DM1_pDv11b6C automationbDM1_pDv11b6C automationyDM1_pDv11b6C automation=DM1_pDv11b6C automation  request_source=Email  userGroupName=SystemUserGrop_DM_wrBPIFqW  request_by=DM1_igibZK3O automation  userGroupName=SystemUserGrop_DM_{rand_str}  profileType=Managed  holdMusic=Default Music  directedIntercom=InitiateAndReceive  whisperPage=InitiateAndReceive  Barge=InitiateAndReceive  silentMonitor=InitiateAndReceive  classOfService=International  accountCodeMode=Required
#&{GenUser}  au_firstname=autotest{rand_str}  au_lastname=Auto  au_businessmail=boss_auto_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=AutoTest_location_7BXTKACQ  au_location=AutoTest_location_7BXTKACQ  au_username=boss_auto_{rand_str}@shoretel.com  au_password=Shoretel1$  au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials  ap_phonenumber=random  ap_activationdate=today  hw_addhwphone=False  hw_type=Sale  hw_model=ShoreTel IP420g - Sale  hw_power=False  hw_power_type=ShoreTel IP Phones Power Supply - Sale  role=Technical  DM1_pDv11b6C automationrDM1_pDv11b6C automationeDM1_pDv11b6C automationqDM1_pDv11b6C automationuDM1_pDv11b6C automationeDM1_pDv11b6C automationsDM1_pDv11b6C automationtDM1_pDv11b6C automation_DM1_pDv11b6C automationbDM1_pDv11b6C automationyDM1_pDv11b6C automation=DM1_pDv11b6C automation  request_source=Email  userGroupName=SystemUserGrop_DM_aMRHYscy  request_by=DM1_7BXTKACQ automation
#&{Usergroup_staff}	 userGroupName=SystemUserGrop_DM_{rand_str}    profileType=Managed    holdMusic=Default Music    directedIntercom=InitiateAndReceive    whisperPage=InitiateAndReceive    Barge=InitiateAndReceive    silentMonitor=InitiateAndReceive    classOfService=International    accountCodeMode=Required
#&{AA_01}    Aa_Name=Test_AA     Aa_Location=random
#&{EditAA04}    Assign_vcfe_component=     Assign_vcfe_Name=     Location=    Aa_Name=    MDT=    Aa_Extn=     prompt=   verify_interactive_diagram=     neg=False   filePath=C:\\ATF_ROBOT\\automation-pbx\\Test_files\\AA-audio.wav  Remove_Operations=  Monitor=    Multiple_Digit_Operation=   MDO_Extension=   Adjust_Timeout=
#&{Huntgroup}  hglocation=random   HGBckupExtn=5501  first_name=Boss_HG   HGExtn=   grp_member=  HGname=Boss_HG  hg_phonenumber=random  Rings_per_Member=3  No_answer_number_of_rings=6
#&{Extensionlist01} 	 extnlistname=Boss_ExtnList_01      extnNumber=
#&{PagingGroup}       Pg_Name=Boss_Paging      extnlistname=   Pg_Location=random
#&{Pickupgroup01}	extnlistname=  pickupgpname=Boss_Pickup_01  PGExtn=     pickuploc=None
#&{OnHoursSchedule01}   scheduleName=VCFE_OHS_01_{rand_str} 	timezone=Pacific Standard Time
#&{on_hold_music_staff_delete}	 musicDescription=Staff_music_{rand_str}    rename_musicDescription=Staff_music_rename_{rand_str}    filePath=C:\\ATF_ROBOT\\automation-pbx\\Test_files\\AA-audio_1.wav    verify=
#&{on_hold_music_staff_add}	 musicDescription=Staff_music_{rand_str}    rename_musicDescription=Staff_music_rename_{rand_str}    filePath=C:\\ATF_ROBOT\\automation-pbx\\Test_files\\AA-audio_2.wav    verify=
#&{OldGenUser}  au_firstname=tt{rand_str}  au_lastname=Auto  au_businessmail=boss_auto_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=AutoTest_location_7BXTKACQ  au_location=AutoTest_location_7BXTKACQ  au_username=boss_auto_{rand_str}@shoretel.com  au_password=Shoretel1$  au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials  ap_phonenumber=random  ap_activationdate=today  hw_addhwphone=False  hw_type=Sale  hw_model=ShoreTel IP420g - Sale  hw_power=False  hw_power_type=ShoreTel IP Phones Power Supply - Sale  role=Technical  request_source=Email  userGroupName=SystemUserGrop_DM_aMRHYscy  request_by=DM1_7BXTKACQ automation

#CSV Varibales  - Client Cases
${CSVFileName}          USERS.csv
${csvfname}             first_name
${csvlname}             last_name
${csvextn}              extension
${csvmac}               mac
${csvemail}             client_email
${csvcid}               client_id
${csvptype}             phone_model