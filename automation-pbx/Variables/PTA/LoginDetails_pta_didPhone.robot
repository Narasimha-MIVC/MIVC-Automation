*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.196.7.182/
${URL1}                   http://10.198.105.68
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            PTA
${platform}               COSMO
${BROWSER}                chrome
${SCOCosmoAccount}        Test_contract_user_Ux1nT73V
${country}                US    #Australia or US or UK
${AccName}                MT_PTA_ACC1
${AccId}				  11477
#${AccLocation}
${AccWithoutLogin}        --> Switch account without logging in as someone else
${locationName}           Headquarters
#D2 Portal details
${D2IP}                   10.196.7.180
${D2User}                 admin@team2.com
${D2Password}             Shoreadmin1#

${KramerD2IP}                   10.32.128.10
${KramerD2User}                 RArlitt@shoretel.qa
${KramerD2Password}             R0chesterNY20!7

#email server detail
&{emailDetail}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=Abc123!!146146
&{emailDetail1}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=zaxqsc!123

#Phone info
&{phoneDMUser01}    user_email=user3@gmail.com    password=Abc234!!
&{phonePMUser01}    user_email=user2@gmail.com    password=Abc234!!
#My hyp user
# &{Phone01}   ip=10.198.33.212     extension=3003     phone_type=p8       PPhone_mac=0010493356F2         first_name=dsingh      vm_password=123456#
# &{Phone02}   ip=10.198.33.211   extension=3004     phone_type=p8           PPhone_mac=00104933566B         first_name=dsingh4     vm_password=123456#
# &{Phone03}   ip=10.198.33.211    extension=4889     phone_type=p8          PPhone_mac=00104933566B         first_name=dsingh5     vm_password=123456#
# &{Phone04}   ip=10.198.33.8      extension=4049     phone_type=p8cg        PPhone_mac=001049454AE9         first_name=dsingh2     vm_password=123456#
# &{Phone05}   ip=10.198.33.146    extension=4879     phone_type=p8cg        PPhone_mac=001049336FDA         first_name=dsingh3     vm_password=123456#

# #My PTA user
#&{Phone01}   ip=10.198.33.8      extension=6464     phone_type=p8cg        PPhone_mac=001049454AE9         first_name=dsingh1           last_name=auto1      vm_password=123456#
#&{Phone02}   ip=10.198.33.146    extension=6460     phone_type=p8cg        PPhone_mac=001049336FDA         first_name=dsingh2           last_name=auto2      vm_password=123456#
#&{Phone03}   ip=10.198.33.27    extension=6463      phone_type=p8          PPhone_mac=00104926890D         first_name=dsingh3           last_name=auto3      vm_password=123456#
#&{Phone04}   ip=10.198.33.250   extension=6435     phone_type=p8cg         PPhone_mac=001049337228         first_name=dsingh4            last_name=auto4      vm_password=123456#
#&{Phone05}   ip=10.198.33.30    extension=7654     phone_type=p8cg         PPhone_mac=001049454AC5         first_name=dsingh5           last_name=realDID      vm_password=123456#
#&{New_Phone1}   ip=10.198.32.237    extension=7652     phone_type=p8           PPhone_mac=001049454AD1         first_name=autotestKqZO     vm_password=123456      did=14086107652
#&{New_Phone}   ip=10.198.34.91    extension=6474     phone_type=p8cg           PPhone_mac=001049337255         first_name=autotestKqZO     vm_password=123456      did=14086107652

&{Phone01}   ip=10.198.18.82    extension=6432      phone_type=p8           PPhone_mac=0010493F2DF4         first_name=AT31     vm_password=13579    did=14084953104
&{Phone02}   ip=10.198.17.155     extension=6443      phone_type=p8cg          PPhone_mac=00104940F567         first_name=AT34	  vm_password=13579    did=14084953106
&{Phone03}   ip=10.198.17.38    extension=4422      phone_type=p8cg           PPhone_mac=001049415117         first_name=AT35     vm_password=13579    did=14084953103
&{Phone04}   ip=10.198.18.14     extension=4423     phone_type=p8          PPhone_mac=001049337A3D            first_name=AT36      vm_password=13579    did=14084953102
&{Phone05}   ip=10.198.18.12      extension=7654    phone_type=p8cg        PPhone_mac=001049454AC5            first_name=dsinghreal1    vm_password=135790  did=914086107654
&{Phone06}   ip=10.198.32.233      extension=7655    phone_type=p8cg         PPhone_mac=00104933723E            first_name=Neeraj1        vm_password=13579  did=914086107655

#&{Phone05}   ip=10.198.33.107     extension=       phone_type=p8cg          PPhone_mac=001049454AD9            first_name=           last_name=Test2      vm_password=123456#


#Production Account Information
${ProdUser}        AutoTest_90kMvjH0@shoretel.com
${ProdAccount}      AutoTest_Acc_90kMvjH0
${ProdLocationName}     AutoTest_location_90kMvjH0

#Kramer Specific Information
${KramerURL}            http://10.11.4.168
${KramerLoc}            SanityLoc
${KramerStaffUser}      staff@shoretel.com
${KramerAccount}        AutoSanity
${KramerAccPMUser}      AutoSanity_ACC_PM@shoretel.com
&{KramerAccPM}  name=AutoSanity_ACC_PM  user=AutoSanity_ACC_PM@shoretel.com     first=Auto      last=SanityACCPM    temp_password=PassW0rd!
${KramerAccDMUser}      AutoSanity@shoretel.com
${KramerAccDMName}      AutoSanity
${KramerACCDMExt}       5146
${KramerLocPMUser}      AutoSanity_LOC_PM@shoretel.com
${KramerBillUser}       AutoSanity_Bill@shoretel.com
${KramerEmerUser}       AutoSanity_Emer@shoretel.com
${KramerTechUser}       AutoSanity_Tech@shoretel.com
${KramerPassword}       P@$$W0rd
${myuser}               dsingh3 auto3

#Transfer Phone number detail

&{PhoneTransfer}    phone=16462075{rand_int}   accountName=Boss Test   AccountID=14387     filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf     verifyPhone=1 (646) 207-5{rand_int}      userName=AutoTest_Acc_vds7fCJE
&{LNP_service}      requestedBy=boss automation     source=Email    serviceClass=projectmgt     index=12            #Index is the index number of LNP service
