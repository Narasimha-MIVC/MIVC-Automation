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

1. Global Number : Verfiy Display Name is Enabled
   [Tags]    GlobalNumber
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   when I switch to "phone_number" page
   And I select number for Edit    &{PhoneNumber_Edit02}
   then I verify PhoneNumber Operation for Edit   &{PhoneNumber_Edit02}

