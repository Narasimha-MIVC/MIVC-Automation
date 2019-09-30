*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.198.107.94/
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            HQ1
${platform}               COSMO
${BROWSER}                chrome
${SCOCosmoAccount}        BOSS_AUTO_68
${locationName}           LocationHyb1
${AccWithoutLogin}        --> Switch account without logging in as someone else

#Account Detail:
${accountName1}    BOSS_AUTO_HYB_1
${DMUser}       DM User
${DMemail}      dmuser@hyb1.com
${DMpassword}   Abc123!!
${PMUser}       PM User
${PMemail}      pmuser@hyb1.com
${PMpassword}   Abc123!!

#D2 Portal details
${D2IP}                   10.198.107.93
${D2User}                 admin@aus.local
${D2Password}             ShoreTel123$

#ST D2 Portal details
${STD2IP}                   http://10.198.105.130:5478/director/login
${STD2User}                 adminst@aus.com
${STD2Password}             Changeme1#

#Phone info
&{phoneDMUser01}    user_email=dmuser@automation.com    password=Abc123!!
&{phonePMUser01}    user_email=pmuser@automation.com    password=Abc123!!

