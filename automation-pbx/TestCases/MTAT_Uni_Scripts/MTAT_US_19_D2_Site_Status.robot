*** Settings ***
Documentation     verify site status
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
01 verify site status

    [Tags]  MT AT Sanity

    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    In D2 I verify site status ${InService} is set for ${AccName}

