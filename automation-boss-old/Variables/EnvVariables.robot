*** Variables ***
#BOSS PORTAL INFO
#####Automation setup - US - #####
${URL}                    http://10.197.108.13/
${URL_connect}            http://10.197.145.190/Connect/Create
${localHost}              http://localhost:56772
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossAccount}            M5Portal Company
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            MTA
${platform}               COSMO
${BROWSER}                chrome
${country}                US
${locationName}           AutoTest_location_7f4e2Fdw
${GlobalUserLocation}     Australia
${GlobalUserBillingLoc}   AutoTest_location_7f4e2Fdw
${BROWSER}                chrome  #canary
${runmode}                normal
${SCOCosmoAccount}        AutoTest_Acc_7f4e2Fdw
${AccWithoutLogin}        --> Switch account without logging in as someone else
${request_by}             autotestdmM3sl Auto
${user_extn}              4649
${user2_extn}             4651
${extnlistname}           Boss_ExtnList_01
#Account Detail:
${accountName1}           AutoTest_Acc_7f4e2Fdw
${DMemail}                boss_auto_dm_M3sl@shoretel.com
${DMpassword}             Abc123!!
${PMemail}                boss_auto_accpm_M3sl@shoretel.com
#${PMemail}                boss_auto_locpmprof_gwBo@shoretel.com
${PMpassword}             Abc123!!
${PMUser}                 autotestaccpmM3sl Auto
${username} =             boss_auto_dm_M3sl@shoretel.com
${globalUser_email}       global@user1.com

#D2 Portal details US
${D2IP}                   10.197.108.10
${D2User}                 alogin1@shoretel.com
${D2Password}             changeme1#
#User login details US
&{phoneDMUser01}    user_email=boss_auto_dm_M3sl@shoretel.com    password=Abc123!!
&{phonePMUser01}    user_email=boss_auto_accpm_M3sl@shoretel.com   password=Abc123!!
&{LNP_service}      requestedBy=boss automation     source=Email    serviceClass=projectmgt     index=12            #Index is the index number of LNP service



#AOB Related Variables
# AOB Login Variables
${AOBAccount}     AOB_REG1
${AOBemail}       aobreg1@aob.com
${AOBUsername}    AOB User1
${salesforceUserName}     sasingh
${salesforcePassword}     Feb@1234
${multi_country_Account}    Aob_Automation
&{AOB_login_dic}       url=${URL}    bossusername=${bossUsername}     bosspassword=${bossPassword}   AOBaccountName=${AOBAccount}    AccWithoutLogin=${AccWithoutLogin}   page=aob

#BOSS PORTAL INFO
####----UK----####
#${URL}                    http://10.32.131.11/
#${bossUsername}           staff@shoretel.com
#${bossPassword}           Abc123!!
#${bossCluster}            MAC
#${country}                UK
#${locationName}           Location1
#${SCOCosmoAccount}        1801 Regression
#${request_by}             dm user
#${user_extn}              2508
#${user2_extn}             2503
#${extnlistname}           Boss_ Extension_List_01
#${accountName1}           1801 Regression
#Account Detail:
#${DMemail}                dm@automation.com
#${DMpassword}             Test123!!
#${PMemail}                priya@sco.com
#${PMpassword}             Test123!!
#${PMUser}                 vishnu priya
#D2 Portal details UK
#${D2IP}                   10.32.131.50
#${D2User}                 vsabusam@mac.shoretel.com
#${D2Password}             Shoretel1$##not working
#User login details UK
#&{phoneDMUser01}    user_email=dm@automation.com    password=Test123!!
#&{phonePMUser01}    user_email=priya@sco.com    password=Test123!!

#BOSS PORTAL INFO
#####----Australia----#####
#${URL}                    http://10.196.7.130/
#${bossUsername}           staff@shoretel.com
#${bossPassword}           Abc234!!
#${bossCluster}            AU2
#${country}                Australia
#${locationName}           Australia One
#${SCOCosmoAccount}        Australia One
#${request_by}             DM User
#${user_extn}              2000
#${user2_extn}             2001
#${extnlistname}           Boss_ExtnList_01
#${accountName1}           Australia One
#Account Detail:
#${DMemail}                dmuser@auto.com
#${DMpassword}             Test123!!
#${PMemail}                pmuser@auto.com
#${PMpassword}             Test123!!
#${PMUser}                 PM User
#D2 Portal details AUS
#${D2IP}                   10.196.7.125
#${D2User}                 admin@au2.com
#${D2Password}             changeme1#
#User login details AUS
#&{phoneDMUser01}    user_email=dmuser@auto.com    password=Test123!!
#&{phonePMUser01}    user_email=pmuser@auto.com    password=Test123!!

# Profile Grid Variables
${ProfileGridAccount}   Automation One
${ProfileGridLocation}   Automation One

${TC_197556_Account}    Automation One
${TC_197556_DecisionMaker}    One user1

${TC_195498_Acoount}        AutoTest_Acc_kmDag0Ko
${TC_195498_User}           autotestdm7uHJ Auto

${TC_195634_Acoount}        AutoTest_Acc_l4RYdNE7
${TC_195634_User}           autotestdmtBt5 Auto

# Exchange server Variables
${exchange_server_name}       outlook.office365.com

#------------------------BOSS US Elvis Regression Login Details-------------------------#
${ElvisURL}               http://portal-qa.shoretelsky.com
${ElvisURL1}              http://portal-qa.shoretelsky.com

#BOSS US D2 Portal details
${ElvisD2IP}                   10.32.128.10
${ElvisD2User}                 RArlitt@shoretel.qa
${ElvisD2Password}             R0chesterNY20!7


#BOSS US Elvis Specific Account Information

${ElvisLoc}            Austin
${ElvisAccount}        Automation_Elvis
${ElvisAccPMUser}      AutoElvisPm@shoretel.com
&{ElvisAccPM}  name=AutoElvisPm acc  user=AutoElvisPm@shoretel.com     first=AutoElvisPm     last=acc    temp_password=PassW0rd!
${ElvisAccDMUser}      Automation_Elvis@shoretel.com
${ElvisAccDMName}      Automation_Elvis Account
${ElvisACCDMExt}
${ElvisLocPMUser}
