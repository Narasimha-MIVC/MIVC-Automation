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

Testing Button Programming - Part 1
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
    set to dictionary  ${proginfo101}    function  Transfer Blind
    set to dictionary  ${proginfo101}    longlabel  TxBlind
    set to dictionary  ${proginfo101}    shortlabel  TB
    Set suite variable    &{proginfo101}

    ${proginfo102}=    Create Dictionary
    set to dictionary  ${proginfo102}    extension  4000
    set to dictionary  ${proginfo102}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo102}    button  3
    set to dictionary  ${proginfo102}    type  Telephony
    set to dictionary  ${proginfo102}    function  Transfer Consultative
    set to dictionary  ${proginfo102}    longlabel  TxCons
    set to dictionary  ${proginfo102}    shortlabel  TC
    Set suite variable    &{proginfo102}

    ${proginfo103}=    Create Dictionary
    set to dictionary  ${proginfo103}    extension  4000
    set to dictionary  ${proginfo103}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo103}    button  4
    set to dictionary  ${proginfo103}    type  Telephony
    set to dictionary  ${proginfo103}    function  Transfer Intercom
    set to dictionary  ${proginfo103}    longlabel  TxInt
    set to dictionary  ${proginfo103}    shortlabel  TI
    Set suite variable    &{proginfo103}

    ${proginfo104}=    Create Dictionary
    set to dictionary  ${proginfo104}    extension  4000
    set to dictionary  ${proginfo104}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo104}    button  5
    set to dictionary  ${proginfo104}    type  Telephony
    set to dictionary  ${proginfo104}    function  Transfer To Mailbox
    set to dictionary  ${proginfo104}    longlabel  TxMBox
    set to dictionary  ${proginfo104}    shortlabel  TMB
    Set suite variable    &{proginfo104}

    ${proginfo105}=    Create Dictionary
    set to dictionary  ${proginfo105}    extension  4000
    set to dictionary  ${proginfo105}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo105}    button  6
    set to dictionary  ${proginfo105}    type  Telephony
    set to dictionary  ${proginfo105}    function  Transfer Whisper
    set to dictionary  ${proginfo105}    longlabel  TxW
    set to dictionary  ${proginfo105}    shortlabel  TW
    Set suite variable    &{proginfo105}
