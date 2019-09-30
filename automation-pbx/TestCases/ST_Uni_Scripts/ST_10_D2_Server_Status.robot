*** Settings ***
Documentation     verify server status
...               dev-Maha
...               Contact : Narasimha.rao@mitel.com


#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

#Component files
Library           ../../lib/PBXComponent.py

*** Test Cases ***
01 verify server status

    [Tags]  DemoPhones


    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    In D2 I verify server status ${InService} is set for ${HQ} and ${HQIP}
    In D2 I verify server status ${InService} is set for ${LDVS} and ${LDVSIP}
    In D2 I verify server status ${InService} is set for ${UCBConf} and ${UCBConfIP}
