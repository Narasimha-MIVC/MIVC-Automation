*** Settings ***
Documentation     Auto populate the Login and user details in CSV file
...               dev-Maha
...               Contact : Mahabaleshwar Hegde

#Keywords Definition file
Resource          ../../RobotKeywords/PBXKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/D2Details.robot

#Component files
Library           Dialogs
Library           ../../lib/PBXComponent.py

*** Test Cases ***
Auto populate the Login and user details in CSV file

    ${numberofPhones} =   Get Value From User   Number of Phones Used :    6
    ${numberofPhones}=  Evaluate  ${numberofPhones} + 1
    : FOR    ${INDEX}    IN RANGE    1    ${numberofPhones}
    \   ${PhoneID}=   Catenate   Phone0${INDEX}
    \   ${userID}=   Catenate   USER_0${INDEX}
    \   ${INDEX} =   Get Value From User   Give Phone ${INDEX} IP :    10.198.17.245
    \   In Varibale file LoginDetails.robot I update key ${PhoneID} with field ip to value ${INDEX}
    \   In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    \   @{userdetails}   In D2 I get all user details of ${INDEX} from ${AccName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvmac} and @{userdetails}[0] in ${CSVFileName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvptype} and @{userdetails}[1] in ${CSVFileName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvfname} and @{userdetails}[2] in ${CSVFileName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvlname} and @{userdetails}[3] in ${CSVFileName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvextn} and @{userdetails}[4] in ${CSVFileName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvcid} and @{userdetails}[5] in ${CSVFileName}
    \   In CSV file I Auto populate the values for ${userID} to ${csvemail} and @{userdetails}[5] in ${CSVFileName}
    \    log to console  ${PhoneID} details updated sucessfully.


#    ${numberofPhones}=  Evaluate  ${numberofPhones} + 1
#     : FOR    ${INDEX}    IN RANGE    1    ${numberofPhones}
#    \    ${PhoneID}=   Catenate   Phone0${INDEX}
#    \    ${userID}=   Catenate   USER_0${INDEX}
#    \    @{userdetails}   In D2 I get all user details of ${${PhoneID}_IP} from ${BOSS_Acc_Name}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvmac} and @{userdetails}[0] in ${CSVFileName}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvptype} and @{userdetails}[1] in ${CSVFileName}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvfname} and @{userdetails}[2] in ${CSVFileName}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvlname} and @{userdetails}[3] in ${CSVFileName}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvextn} and @{userdetails}[4] in ${CSVFileName}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvcid} and @{userdetails}[5] in ${CSVFileName}
#    \   In CSV file I Auto populate the values for ${userID} to ${csvemail} and @{userdetails}[5] in ${CSVFileName}



*** Keywords ***


