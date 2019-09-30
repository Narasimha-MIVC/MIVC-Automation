*** Settings ***
Library  String
Library	   OperatingSystem

*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.196.7.182/
${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
#${URL}                    http://10.32.129.11/
#${bossUsername}           mkumar@cosmo.shoretel.com
#${bossPassword}           Abc123!!
${bossUser}               Staff User
${bossCluster}            PTA
${platform}               COSMO
${BROWSER}                chrome
${country}                US    #Australia or US or UK
# ${AccName}                MT_PTA_ACC1
${AccName}                SVLAutomation-RUM-TEST1
${AccId}                  16079
#${AccLocation}
${AccWithoutLogin}        --> Switch account without logging in as someone else
${locationName}           Headquarters
${AA_DID}                  1 (408) 495-2416
${Call_AA_DID}             14084952416
${RPIP}                  10.196.7.181
${stopcmd}                ./stopstts.sh
${startcmd}               ./startstts.sh

#D2 Portal details
# ${D2IP}                   10.196.7.180
# ${D2User}                 admin@pta.com
# ${D2Password}             Shoreadmin1#

#D2 Portal details
${D2IP}                   10.32.129.70
${D2User}                 admin@shoretel.com
${D2Password}             Shoreadmin1#


# Demo Phone details  
&{DemoPhone1}  extensionNumber=8017  phone_type=Mitel6930  ipAddress=10.198.33.221  phoneName=Auto User7
&{DemoPhone2}  extensionNumber=8008  phone_type=Mitel6920  ipAddress=10.198.33.9  phoneName=Auto User8
&{DemoPhone3}  extension=8007  phone_type=phone_4xx  ipAddress=10.198.17.185  phoneName=Auto user16  PPhone_mac=001049454AC4
&{DemoPhone4}  extension=8016  phone_type=Mitel6940  ip=10.198.17.185  PPhone_mac=001049454AC4  phoneName=Auto User17  ipAddress=10.198.32.160


		 
${numberofPhones}	4
${file_to_be_update}	LoginDetailsNeeraj.robot

#CSV Varibales  - Client Cases
${CSVFileName}          USERS.csv
${csvfname}             first_name
${csvlname}             last_name
${csvextn}              extension
${csvmac}               mac
${csvemail}             client_email
${csvcid}               client_id
${csvptype}             phone_model

${BCA_Extension}                   bca123
${bca_name}                   1350

