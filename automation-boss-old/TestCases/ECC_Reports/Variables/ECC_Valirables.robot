*** Variables ***
#BOSS Portal Variables
${URL}                    http://10.23.173.8/
${eccSupervisorUsername}           LButters@southparkut.com
${eccSupervisorPassword}           Shoreadmin1#
${eccCluster}             KRAMER_ECC
${ECCActivatedAccount}      amit test contract2

#Settings
${activateIvrDbIntrgration}       False
${activateAdditionalPorts}       False
${additionalIVRPorts}           1
${timeZone}              America/Jujuy


# Add Report Details
${reportNameFormat}           Auto_Report
${basereport}                 Agent by Date
${reportType}                 report_type
${textFileName}               Test
${reportFormatType}           xls
${emailFrom}                  afzal.pasha@testmitel.com
${emailTo}                    afzal.pasha@testmitel.com
${emailSubject}               Auto Report Subject
${standardDateOption}         DurationByDay
${standardTimeoption}         DurationByHour
${standardRecurringReportType}         Daily
${standardOneTimeReportType}         OneTimeNow

#Edit Report Details
${recurringReportName_ToEdit}           Auto_Report_Kmu3
${oneTimeReportName_ToEdit}           Auto_Report_8QvN

#Copy Report Details
${reportNameCopyFormat}         Auto_Copy
${recurringReportToCopy}        Auto_Copy_2A1v
${oneTimeReportToCopy}          Auto_Copy_Fzwq

#Delete Report Details
${recurringReportName_ToDelete}           Delete1
${oneTimeReportName_ToDelete}           Auto_Report_qDlS

${AccWithoutLogin}        --> Switch account without logging in as someone else

&{Contract_ECC}	  accountType=New Customer   accountName=AutoTest_ECCAcc_{rand_str}   salesPerson=Staff User   platformType=Connect Cloud   country=United States   firstName=boss   lastName=automation   password=Abc123!!   confirmPassword=Abc123!!   email=AutoTest_{rand_str}@shoretel.com   locationName=AutoTest_location_{rand_str}   Address1=1385 Broadway   city=New York   state=New York   zip=10018   connectivity=This Location  no_validation=False  class=bundle  product=Connect CLOUD Education Essentials   quantity=1   location=AutoTest_location_{rand_str}   MRR=12   NRR=23   class01=projectmgt   product01=Global User TN Service   quantity01=1   location01=AutoTest_location_{rand_str}   MRR01=12   NRR01=23   contractNumber=369   forecastDate=today   notes=Not Required   filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf   termVersion=Version 3.0   termLength=36 Months   termRenewalType=Automatic   termInstall=90 Days
&{Settings}   activateIvrDbIntrgration=${activateIvrDbIntrgration}   activateAdditionalPorts=${activateAdditionalPorts}   ports=${additionalIVRPorts}   eccClutster=${eccCluster}   eccTimeZone=${timeZone}
&{ReportValues}   reportName=${reportNameFormat}_{rand_str}     copyReportName=${reportNameCopyFormat}_{rand_str}   basereport=${basereport}      textFileName=${textFileName}        emailTo=${emailTo}      emailSubject=${emailSubject}        emailFrom=${emailFrom}        reportType=${reportType}_{type_of_report}        reportFormatType=${reportFormatType}        standardRecurringReportType=${standardRecurringReportType}        standardOneTimeReportType=${standardOneTimeReportType}        standardDateOption=${standardDateOption}        standardTimeoption=${standardTimeoption}        recurringReportToCopy=${recurringReportToCopy}        oneTimeReportToCopy=${oneTimeReportToCopy}     recurringReportName_ToDelete=${recurringReportName_ToDelete}     oneTimeReportName_ToDelete=${oneTimeReportName_ToDelete}     recurringReportName_ToEdit=${recurringReportName_ToEdit}     oneTimeReportName_ToEdit=${oneTimeReportName_ToEdit}