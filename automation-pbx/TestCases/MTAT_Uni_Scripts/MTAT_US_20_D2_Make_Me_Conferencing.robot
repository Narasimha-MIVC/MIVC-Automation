*** Settings ***
Documentation     verify Verify Make Me Conferencing
...               dev-Maha
...               Contact : Mahabaleshwar Hegde


#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

#Component files
Library           ../../lib/PBXComponent.py

*** Test Cases ***
Verify Make Me Conferencing

    [Tags]  MT AT Sanity


    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
	In D2 I verify make me conferencing for switch ${PSwitch_Name} with ip ${PSwitchIP} ,switch type ${PSwitch}, active calls ${MakeMeConf1.active_calls}, in_use port ${MakeMeConf1.in_use_ports}, free port ${MakeMeConf1.free_ports} and site ${locationName}
