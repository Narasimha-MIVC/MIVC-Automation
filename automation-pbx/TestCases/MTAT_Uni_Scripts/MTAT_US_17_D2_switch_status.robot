*** Settings ***
Documentation     verify D2 Switch status
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
01 verify switch status

    [Tags]  MT AT Sanity


    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    In D2 I verify switch status @{passStatus} is set for ${HQ} and ${HQIP}
    In D2 I verify switch status @{passStatus} is set for ${LDVS} and @{LDVSIP}
    In D2 I verify switch status @{passStatus} is set for ${PSwitch} and @{PSwitchIP}
    In D2 I verify switch status @{passStatus} is set for ${UCBConf} and @{UCBConfIP}
    In D2 I verify switch status @{passStatus} is set for ${TSwitch} and @{TSwitchIP}
    #In D2 I verify switch status @{passStatus} is set for ${WINDVS} and @{WINDVSIP}
