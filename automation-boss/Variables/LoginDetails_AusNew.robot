*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.196.7.130/
${URL1}                   http://10.198.105.68
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc234!!
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            AU2
${platform}               COSMO
${BROWSER}                chrome
${SCOCosmoAccount}        Test_contract_user_Ux1nT73V
${country}                Australia
${AccWithoutLogin}        --> Switch account without logging in as someone else

#D2 Portal details
${D2IP}                   10.196.7.125
${D2User}                 admin@au2.com
${D2Password}             changeme1#

#D2 Portal details
${KramerD2IP}                   10.32.128.10
${KramerD2User}                 RArlitt@shoretel.qa
${KramerD2Password}             R0chesterNY20!7

#email server detail
&{emailDetail}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=Abc123!!
&{emailDetail1}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=zaxqsc!123

#Phone info
&{phoneDMUser01}    user_email=user3@gmail.com    password=Abc234!!
&{phonePMUser01}    user_email=user2@gmail.com    password=Abc234!!

&{Phone01}   ip=10.198.18.15     extension=2010      phone_type=p8        PPhone_mac=0010492863E4
&{Phone02}   ip=10.198.18.12     extension=2011      phone_type=p8        PPhone_mac=001049335837
&{Phone03}   ip=10.198.17.251     extension=2012      phone_type=p8cg        PPhone_mac=0010493356FE6

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