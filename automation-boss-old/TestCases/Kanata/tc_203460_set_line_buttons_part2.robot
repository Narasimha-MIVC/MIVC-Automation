*** Settings ***
Documentation    Suite description

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../Kanata/Variables/global_variables.robot

#BOSS ComponentTestCas
Library           ../../lib/BossComponent.py

*** Test Cases ***

Testing Button Programming - Part 2
    [Tags]    REGRESSION
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${AutomationNew} with ${AccWithoutLogin} option

    @{ITEMS}    Create List    ${proginfo101}   ${proginfo102}    ${proginfo103}    ${proginfo104}    ${proginfo105}
    :FOR    ${proginfo}    IN    @{ITEMS}
    \    And I add prog button    &{proginfo}
    \    And I verify programmed button    &{proginfo}

*** Keywords ***
Set Init Env
    ${proginfo101}=    Create Dictionary
    set to dictionary  ${proginfo101}    extension  4000
    set to dictionary  ${proginfo101}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo101}    button  2
    set to dictionary  ${proginfo101}    type  Telephony
    set to dictionary  ${proginfo101}    function  Hotline
    set to dictionary  ${proginfo101}    longlabel  Hotline
    set to dictionary  ${proginfo101}    shortlabel  HL
    set to dictionary  ${proginfo101}    callaction  Intercom
    Set suite variable    &{proginfo101}

    ${proginfo102}=    Create Dictionary
    set to dictionary  ${proginfo102}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo102}    button  3
    set to dictionary  ${proginfo102}    type  Telephony
    set to dictionary  ${proginfo102}    function  Phone Application
    set to dictionary  ${proginfo102}    longlabel  PhoneApp
    set to dictionary  ${proginfo102}    shortlabel  PA
    Set suite variable    &{proginfo102}

    ${proginfo103}=    Create Dictionary
    set to dictionary  ${proginfo103}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo103}    button  4
    set to dictionary  ${proginfo103}    type  Telephony
    set to dictionary  ${proginfo103}    function  Send Digits Over Call
    set to dictionary  ${proginfo103}    longlabel  Send Digits
    set to dictionary  ${proginfo103}    shortlabel  SDOC
    set to dictionary  ${proginfo103}    digits  123
    Set suite variable    &{proginfo103}

    ${proginfo104}=    Create Dictionary
    set to dictionary  ${proginfo104}    extension  4000
    set to dictionary  ${proginfo104}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo104}    button  5
    set to dictionary  ${proginfo104}    type  Telephony
    set to dictionary  ${proginfo104}    function  Silent Coach
    set to dictionary  ${proginfo104}    longlabel  Silent Coach
    set to dictionary  ${proginfo104}    shortlabel  SC
    Set suite variable    &{proginfo104}

    ${proginfo105}=    Create Dictionary
    set to dictionary  ${proginfo105}    extension  4000
    set to dictionary  ${proginfo105}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo105}    button  6
    set to dictionary  ${proginfo105}    type  Telephony
    set to dictionary  ${proginfo105}    function  Silent Monitor
    set to dictionary  ${proginfo105}    longlabel  Silent Mon
    set to dictionary  ${proginfo105}    shortlabel  SM
    Set suite variable    &{proginfo105}
