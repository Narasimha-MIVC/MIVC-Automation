*** Settings ***
Library  String
Library	   OperatingSystem

#Environment variable file
Resource   ../../../Variables/EnvVariables.robot

*** Variables ***
################################################################################################################################
#AOB User detail
#Keys: firstName=First Name of User, lastName=Last name of user, email=Email of User, phone=Phone option "Existing" or "None"
# number=Phone number or None, extn=Extention
################################################################################################################################

&{AobUserDetail}       firstName=Test_{rand_str}   lastName=User   email=Test_{rand_str}@shoretel.com   phone=None     number=None   extn={rand_int}
&{EditAobUserDetail}       firstName=Edit_Test_{rand_str}   lastName=Edit_User   email=Edit_Test_{rand_str}@shoretel.com   phone=None     number=None   extn={rand_int}

&{AobUserDetail_to_Clear}       firstName=A   lastName=U  email=a@u1.com   phone=None     number=None   extn={rand_int}
&{multiple_user}       firstName=Auto    lastName=User    email=autouser@shoretel.com    phone=None     number=None   extn=

&{AobPopUpOption}      button=

########################################################################################################################################
#Help url validation detail
#Keys: url= Url, user=Username for salesfoce, pwd=password for salesforce account (Detail should be provided in EnvVariables.robot file
########################################################################################################################################

&{activation_help_url}            url=https://shoretel.my.salesforce.com/articles/Technical_Documentation/Mitel-Easy-Setup-Activating-Locations   user=${salesforceUserName}   pwd=${salesforcePassword}
&{help_url}            url=https://oneview.mitel.com/s/article/Mitel-Easy-Setup-Adding-Users   user=${salesforceUserName}   pwd=${salesforcePassword}
@{url_list}=  https://oneview.mitel.com/s/article/Mitel-Easy-Setup-Adding-Users     https://oneview.mitel.com/s/article/Mitel-Easy-Setup-Setting-Up-Locations   https://shoretel.my.salesforce.com/articles/Technical_Documentation/Setting-Up-ShoreTel-Connect-CLOUD-Service   https://oneview.mitel.com/s/article/ShoreTel-Connect-CLOUD-Profiles   https://oneview.mitel.com/s/article/Mitel-Easy-Setup-Overview
&{url_dict}     url=@{url_list}   user=${salesforceUserName}   pwd=${salesforcePassword}


#Contract Detail for AOB
&{ContractAOB}	  accountType=New Customer  accountName=AOB_AutoTest_Acc_{rand_str}  salesPerson1=Vivek Sabu Sam  salesPerson=${bossUser}  platformType=Connect Cloud  country=United States  firstName=boss  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}  Address1=1385 Broadway  city=New York  state=New York  zip=10018  connectivity=This Location  no_validation=False  class=bundle  product=MiCloud Connect Education Essentials  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days

#Error Messages validation for User page field
${firstName}    First name is required
${lastName}    Last name is required
${extension}    Extension can't be empty
${email}    Email is required


#Phone number detail       clientLocation=AutoTest_Location_OOX5ygne
&{AOBPhoneNumber}	 numberRange=16462016{rand_int}   range=1    serviceUsage=Telephone Number Turnup    tn_type=client   clientAccount=${AOBAccount}    vendorForUS=212803-dash    vendorOrderNumber=1234    requestedBy=${AOBUsername}   requestSource=Email    state=Turned down



#partiton detail
&{PartitionDetails}   partitionName=None

#Transfer Number details
&{AOBTransferPhoneNumber}	 numberRange=16462017{rand_int}   range=0  currentProvider=Verizon      state=Transfer Requested


#Callhandling business hour setup
@{days}=   Sun  Mon  Tues
&{businessHour}   startTime=08:00    endTime=17:00   days=@{days}

&{operatorRings}   ringNum=4  clear=No

