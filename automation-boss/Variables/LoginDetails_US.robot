*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.198.105.68/       #http://10.196.7.130/
${URL1}                    http://10.198.105.68
${bossUsername}           staff@shoretel.com
${bossPassword}           Shoreadmin1$
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            HQ1
${platform}               COSMO
${BROWSER}                chrome
${SCOCosmoAccount}        Test_contract_user_Ux1nT73V
${country}                us         #Australia or US or UK
${AccWithoutLogin}        --> Switch account without logging in as someone else

#D2 Portal details
${D2IP}                   10.198.104.236
${D2User}                 admin1@qa.shoretel.com
${D2Password}             changeme

#email server detail
&{emailDetail}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=Abc123!!
&{emailDetail1}            emailToReset=rodadmin@shoretel.com   emailPassword=ROD#12345     emailServer=relay.shoretel.com      setPassword=zaxqsc!123

#Phone info
&{phoneDMUser01}    user_email=dmuser@automation.com    password=Abc123!!
&{phonePMUser01}    user_email=pmuser@automation.com    password=Abc123!!

&{Phone01}   ip=10.198.33.71     extension=7933      phone_type=p8        PPhone_mac=001049335AC9
&{Phone02}   ip=10.198.32.103     extension=7935      phone_type=p8        PPhone_mac=001049335ADA
&{Phone03}   ip=10.198.33.48     extension=7636      phone_type=p8        PPhone_mac=001049335676

#Production Account Information
${ProdUser}        AutoTest_90kMvjH0@shoretel.com
${ProdAccount}      AutoTest_Acc_90kMvjH0
${ProdLocationName}     AutoTest_location_90kMvjH0