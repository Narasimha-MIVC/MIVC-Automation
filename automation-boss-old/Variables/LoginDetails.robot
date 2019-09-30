*** Variables ***
#BOSS PORTAL INFO
#${URL}                    http://10.197.108.13/
#${URL1}                   http://10.198.105.68
#${bossUsername}           staff@shoretel.com
#${bossPassword}           Abc123!!
#${bossUser}               Staff User
#${bossCluster1}           BOSS QA
#${bossCluster}            MTA
#${platform}               COSMO
#${BROWSER}                chrome
##${SCOCosmoAccount}        Test_contract_user_bPdVADHI
#${country}                US    #Australia or US or UK
#${AccWithoutLogin}        --> Switch account without logging in as someone else
#
##D2 Portal details
#${D2IP}                   10.197.108.10
#${D2User}                 alogin1@shoretel.com
#${D2Password}             changeme1#

${URL}                    http://10.197.145.190/
${URL1}                   http://10.198.105.68
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            BAU
${platform}               COSMO
${BROWSER}                chrome
#${SCOCosmoAccount}        Test_contract_user_bPdVADHI
${country}                US    #Australia or US or UK
${AccWithoutLogin}        --> Switch account without logging in as someone else

#D2 Portal details
${D2IP}                   10.197.145.186
${D2User}                 admin@auto.com
${D2Password}             Shoreadmin1#

${KramerD2IP}                   10.32.128.10
${KramerD2User}                 RArlitt@shoretel.qa
${KramerD2Password}             R0chesterNY20!7

#email server detail
&{emailDetail}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=Abcdef123!
&{emailDetail1}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=zaxqsc!123     setPassword=zaxqsc!123

#&{emailDetail}            emailToReset=vasuja.k@mitel.com   emailPassword=Abc123!!     emailServer=outlook.office365.com      setPassword=Abc123!!
#&{emailDetail1}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=outlook.office365.com      setPassword=zaxqsc!123

#Phone info
&{phoneDMUser01}    user_email=auser3@shoretel.com   password=Abc123!!
&{phonePMUser01}    user_email=auser2@shoretel.com    password=Abc123!!

&{Phone01}   ip=10.198.34.92     extension=4000      phone_type=p8cg        PPhone_mac=001049454B07
&{Phone02}   ip=10.198.32.213    extension=4001      phone_type=p8        PPhone_mac=001049335AC9
&{Phone03}   ip=10.198.33.58     extension=4002      phone_type=p8        PPhone_mac=001049335ADA

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


#Transfer Phone number detail

&{PhoneTransfer}    phone=16462075{rand_int}   accountName=Boss Test   AccountID=14387     filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf     verifyPhone=1 (646) 207-5{rand_int}      userName=AutoTest_Acc_vds7fCJE
&{LNP_service}      requestedBy=boss automation     source=Email    serviceClass=projectmgt     index=12            #Index is the index number of LNP service