*** Settings ***
Documentation     verify IP Phone Status
...               dev-Maha
...               Contact : Mahabaleshwar Hegde


#Keywords Definition files
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

#Component files
Library           ../../lib/PBXComponent.py

*** Test Cases ***
01 verify IP Phone Status

    [Tags]  MT AT Sanity


    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    In D2 I verify ip phone status ${InService} is set for ${Phone01.PPhone_mac}
    In D2 I verify ip phone status ${InService} is set for ${Phone02.PPhone_mac}
    In D2 I verify ip phone status ${InService} is set for ${Phone03.PPhone_mac}
