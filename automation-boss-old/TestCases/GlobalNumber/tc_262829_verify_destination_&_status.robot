*** Settings ***
Documentation    Suite description

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../GlobalNumber/Variables/GlobalNumber_variable.robot
Resource          ../../Variables/LoginDetails.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}   country=${country}
Library  String
Library  Collections


*** Test Cases ***

1. Global Number : verify destinationcType, destination name and status of the created DNIS
   [Tags]    GlobalNumber
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   when I switch to "phone_number" page
   ${selectedTn}   ${selectedDestType}=  I create DNIS with Save    &{PhoneNumber_Assign_BCA}
   then I verify Destination ${selectedDestType} and Status of ${selectedTn}     &{PhoneNumber_Assign_BCA}
   then I verify Destination Type of ${selectedTn}     &{PhoneNumber_Assign_BCA}

