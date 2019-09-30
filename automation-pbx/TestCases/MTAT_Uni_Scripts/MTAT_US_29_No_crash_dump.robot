*** Settings ***
Documentation     check for crash dump in ucb
...               Dev: Lavanya


#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot



Library           ../../lib/PBXComponent.py


*** Test Cases ***

No crash dump

    [Tags]  MT AT Sanity

     I check for crash dump in ${UCBConfIP} using ${RPIP}
