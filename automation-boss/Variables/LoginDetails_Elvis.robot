*** Variables ***
#BOSS US Elvis Regression Login Details
${ElvisURL}               http://portal-qa.shoretelsky.com
${ElvisURL1}              http://portal-qa.shoretelsky.com
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}
${platform}               Elvis
${BROWSER}                chrome
${country}                us         #Australia or US or UK
${AccWithoutLogin}        --> Switch account without logging in as someone else

#BOSS US D2 Portal details
${ElvisD2IP}                   10.32.128.10
${ElvisD2User}                 RArlitt@shoretel.qa
${ElvisD2Password}             R0chesterNY20!7


&{Phone01}   ip=10.198.33.71     extension=7933      phone_type=p8        PPhone_mac=001049335AC9
&{Phone02}   ip=10.198.32.103     extension=7935      phone_type=p8        PPhone_mac=001049335ADA
&{Phone03}   ip=10.198.33.48     extension=7636      phone_type=p8        PPhone_mac=001049335676


#BOSS US Elvis Specific Information

${ElvisLoc}            Austin
${ElvisAccount}        Automation_Elvis
${ElvisAccPMUser}      AutoElvisPm@shoretel.com
&{ElvisAccPM}  name=AutoElvisPm acc  user=AutoElvisPm@shoretel.com     first=AutoElvisPm     last=acc    temp_password=PassW0rd!
${ElvisAccDMUser}      Automation_Elvis@shoretel.com
${ElvisAccDMName}      Automation_Elvis Account
${ElvisACCDMExt}
${ElvisLocPMUser}
