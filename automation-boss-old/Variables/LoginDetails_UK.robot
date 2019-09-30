*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.32.131.11
${URL1}                   shttp://10.198.105.68
${bossUsername}           autostaff@qa.shoretel.com
${bossPassword}           Abc234!!
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            MAC
${platform}               COSMO
${BROWSER}                chrome
#${SCOCosmoAccount}        Regression
${country}                UK
${AccWithoutLogin}        --> Switch account without logging in as someone else

#D2 Portal details
${D2IP}                   d2.mac.shoretel.qa
${D2User}                 VK@shoretel.qa
${D2Password}             R0chesterNY20!7

#email server detail
&{emailDetail}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=Abc234!!
&{emailDetail1}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=zaxqsc!123

#Phone info
&{phoneDMUser01}    user_email=dm1@user1.com    password=zaqwsx123!@#$
&{phonePMUser01}    user_email=pm1@user1.com    password=zaqwsx123!@#$

&{Phone01}   ip=10.198.33.64    extension=8002     phone_type=p8    PPhone_mac=0010492863E4
&{Phone02}   ip=10.198.33.88    extension=8004		phone_type=p8        PPhone_mac=001049335837
&{Phone03}   ip=10.198.34.2    extension=8006		phone_type=p8cg        PPhone_mac=001049336FE6

#Production Account Information
${ProdUser}        AutoTest_90kMvjH0@shoretel.com
${ProdAccount}      AutoTest_Acc_90kMvjH0
${ProdLocationName}     AutoTest_location_90kMvjH0