*** Settings ***
Documentation     verify all aplliances status
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
Verify voicemail server status

    [Tags]  MT AT Sanity


    In D2 ${D2IP} I login with ${D2User} and ${D2Password}
	In D2 I verify messages ${vm_messages} and mailbox count ${mailbox_count} for voicemail server ${HQ_Name} with ip ${HQIP} and site ${Site_Name}
	In D2 I verify messages ${vm_messages} and mailbox count ${mailbox_count} for voicemail server ${LDVS_Name} with ip ${LDVSIP} and site ${Site_Name}
