*** Settings ***
Library  String
Library	   OperatingSystem

*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.196.7.182/
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster}            HYP
${platform}               COSMO
${BROWSER}                chrome
${country}                US    #Australia or US or UK
${AccName}                Maha_hyp
${AccId}				  12540
${locationName}           Headquarters
${AccWithoutLogin}        --> Switch account without logging in as someone else
${RPIP}                   10.196.7.181
${stopcmd}                ./stopstts.sh
${startcmd}               ./startstts.sh



&{Phone01}   ip=10.198.32.230       extension=5501     phone_type=p8cg        PPhone_mac=001049454ABC         first_name=maha1     last_name=hyp       vm_password=123456   did=14084955501  email=maha1@hyp.com
&{Phone02}   ip=10.198.34.29      extension=5502     phone_type=p8cg        PPhone_mac=001049337155         first_name=maha2     last_name=hyp       vm_password=123456    did=14084955502   email=maha2@hyp.com
&{Phone03}   ip=10.198.33.7       extension=5503     phone_type=p8cg        PPhone_mac=001049454AC9         first_name=maha3     last_name=hyp       vm_password=123456    did=14084955503   email=maha3@hyp.com
&{Phone04}   ip=10.198.32.189       extension=5504     phone_type=p8cg        PPhone_mac=001049454ABE        first_name=maha4     last_name=hyp       vm_password=123456    did=14084955504  email=maha4@hyp.com
&{Phone05}   ip=10.198.32.220       extension=5505     phone_type=p8cg        PPhone_mac=001049454ADC         first_name=maha5     last_name=hyp       vm_password=123456    did=14084955505 email=maha5@hyp.com
&{Phone06}   ip=10.198.33.250        extension=5506     phone_type=p8cg        PPhone_mac=001049337155         first_name=maha6     last_name=hyp       vm_password=123456    did=14084955506 email=maha6@hyp.com
&{Phone_did}   ip=10.198.18.12      extension=7654    phone_type=p8cg        PPhone_mac=001049454AC5            first_name=dsinghreal1    vm_password=135790  did=14086107654   last_name=DID1 email=maha1@hyp.com
&{Phone07}   ip=10.198.32.233      extension=7655    phone_type=p8cg         PPhone_mac=00104933723E            first_name=Neeraj1        vm_password=13579  did=14086107655  last_name=real1b  email=maha1@hyp.com



#BOSS Cases
#BOSS Cases

&{Contract}	  accountType=New Customer  accountName=AutoTest_Acc_{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=United States  firstName=DM1_{rand_str}  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}  Address1=1385 Broadway  city=New York  state=New York  zip=10018  connectivity=This Location  no_validation=False  class=bundle  product=MiCloud Connect Essentials  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=C:\\ATF_ROBOT\\automation-boss\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{PhoneNumber}  numberRange=14802{rand_int}  range=10  serviceUsage=Telephone Number turnup  tn_type=client  clientAccount=Maha_hyp  clientLocation=Mahahyp  vendor=212803-dash  vendorOrderNumber=1234  requestedBy=Maha hyp  requestSource=Email  state=Available  numberStart=16462985864
&{GenUser}  au_firstname=autotest{rand_str}  au_lastname=Auto  au_businessmail=boss_auto_{rand_str}@shoretel.com  au_personalmail=boss_auto_dm_{rand_str}@gmail.com  au_userlocation=Mahahyp  au_location=Mahahyp  au_username=boss_auto_{rand_str}@shoretel.com  au_password=Shoretel1$  au_confirmpassword=Shoretel1$  ap_phonetype=MiCloud Connect Essentials  ap_phonenumber=random  ap_activationdate=today  hw_addhwphone=False  hw_type=Sale  hw_model=ShoreTel IP420g - Sale  hw_power=False  hw_power_type=ShoreTel IP Phones Power Supply - Sale  role=Technical  DM1_pDv11b6C automationrDM1_pDv11b6C automationeDM1_pDv11b6C automationqDM1_pDv11b6C automationuDM1_pDv11b6C automationeDM1_pDv11b6C automationsDM1_pDv11b6C automationtDM1_pDv11b6C automation_DM1_pDv11b6C automationbDM1_pDv11b6C automationyDM1_pDv11b6C automation=DM1_pDv11b6C automation  request_source=Email  userGroupName=SystemUserGrop_DM_nCkor9X9  request_by=DM1_HLCxJDIT automation
&{Usergroup_staff}	 userGroupName=SystemUserGrop_DM_{rand_str}    profileType=Managed    holdMusic=Default Music    directedIntercom=InitiateAndReceive    whisperPage=InitiateAndReceive    Barge=InitiateAndReceive    silentMonitor=InitiateAndReceive    classOfService=International    accountCodeMode=Required

&{AA_01}    Aa_Name=Test_AA     Aa_Location=random
&{EditAA04}    Assign_vcfe_component=     Assign_vcfe_Name=     Location=    Aa_Name=    MDT=    Aa_Extn=     prompt=   verify_interactive_diagram=     neg=False   filePath=${EXECDIR}${/}Test_files${/}AA-audio.wav  Remove_Operations=  Monitor=    Multiple_Digit_Operation=   MDO_Extension=   Adjust_Timeout=
&{Huntgroup}  hglocation=random   HGBckupExtn=5501  first_name=Boss_HG   HGExtn=   grp_member=  HGname=Boss_HG  hg_phonenumber=random  Rings_per_Member=3  No_answer_number_of_rings=6
&{Extensionlist01} 	 extnlistname=Boss_ExtnList_01      extnNumber=
&{PagingGroup}       Pg_Name=Boss_Paging      extnlistname=   Pg_Location=random
&{Pickupgroup01}	extnlistname=  pickupgpname=Boss_Pickup_01  PGExtn=     pickuploc=None

#NewlycreatedTenant
${NewAccId}                   12540
${NewAccName}                   Maha_hyp


#CSV Varibales  - Client Cases
${CSVFileName}          USERS.csv
${csvfname}             first_name
${csvlname}             last_name
${csvextn}              extension
${csvmac}               mac
${csvemail}             client_email
${csvcid}               client_id
${csvptype}             phone_model