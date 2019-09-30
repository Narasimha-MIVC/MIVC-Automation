*** Settings ***
Documentation     Verify build in Monitoring Service
...               Dev: Lavanya


#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot


Library           ../../lib/PBXComponent.py


*** Test Cases ***

Monitoring Service

      [Tags]  MT AT Sanity


      In D2 ${D2IP} I login with ${D2User} and ${D2Password}
      I verify the ${build} present in monitoring service of configuration
