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

Testing Button Programming as Conference Lines
    [Tags]    REGRESSION
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${AutomationNew} with ${AccWithoutLogin} option

    @{ITEMS}    Create List    ${proginfo101}    ${proginfo102}    ${proginfo103}
    :FOR    ${proginfo}    IN    @{ITEMS}
    \    And I add prog button    &{proginfo}
    \    And I verify programmed button    &{proginfo}

*** Keywords ***
Set Init Env
    ${proginfo101}=    Create Dictionary
    set to dictionary  ${proginfo101}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo101}    button  2
    set to dictionary  ${proginfo101}    type  Telephony
    set to dictionary  ${proginfo101}    function  Conference Blind
    set to dictionary  ${proginfo101}    longlabel  Conf Blind
    set to dictionary  ${proginfo101}    shortlabel  CB
    set to dictionary  ${proginfo101}    extension  4000
    Set suite variable    &{proginfo101}

    ${proginfo102}=    Create Dictionary
    set to dictionary  ${proginfo102}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo102}    button  3
    set to dictionary  ${proginfo102}    type  Telephony
    set to dictionary  ${proginfo102}    function  Conference Consultative
    set to dictionary  ${proginfo102}    longlabel  Conf Cons
    set to dictionary  ${proginfo102}    shortlabel  Conf C
    set to dictionary  ${proginfo102}    extension  4000
    Set suite variable    &{proginfo102}

    ${proginfo103}=    Create Dictionary
    set to dictionary  ${proginfo103}    user_email  auser1@shoretel.com
    set to dictionary  ${proginfo103}    button  4
    set to dictionary  ${proginfo103}    type  Telephony
    set to dictionary  ${proginfo103}    function  Conference Intercom
    set to dictionary  ${proginfo103}    longlabel  Conf Int
    set to dictionary  ${proginfo103}    shortlabel  Conf I
    set to dictionary  ${proginfo103}    extension  4000
    Set suite variable    &{proginfo103}
