*** Settings ***
Documentation     verify IM Status
...               dev-Maha
...               Contact : Mahabaleshwar Hegde

#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

# Component
Library           ../../lib/PBXComponent.py

*** Test Cases ***
01 verify IM Status

    [Tags]  MT AT Sanity

    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    In D2 I verify all IM switch status is set for ${UCBIm_Name}
    In D2 I verify all IM switch status is set for ${UCBConf_Name}

