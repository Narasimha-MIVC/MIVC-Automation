*** Settings ***
Documentation     verify Trunk Group Status
...               dev-Maha
...               Contact : Mahabaleshwar Hegde


#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

#D2 Component
Library           ../../lib/PBXComponent.py


*** Test Cases ***
Verify Trunk Groups Status

    [Tags]  MT AT Sanity


    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
	In D2 I verify trunk in use ${AnalogLoopStartInUse} and trunk in service ${AnalogLoopStartInService} for trunk group ${AnalogLoopStart} with trunk type ${AnalogLoopStartType} and site ${Site_Name}
	In D2 I verify trunk in use ${Trunk02.trunk_in_use} and trunk in service ${Trunk02.trunk_in_service} for trunk group ${Trunk02.trunk_name} with trunk type ${Trunk02.trunk_type} and site ${Site_Name}
	In D2 I verify trunk in use ${Trunk03.trunk_in_use} and trunk in service ${Trunk03.trunk_in_service} for trunk group ${Trunk03.trunk_name} with trunk type ${Trunk03.trunk_type} and site ${Site_Name}
