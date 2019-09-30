*** Settings ***
Library  String
Library	   OperatingSystem

Resource   LoginDetails.robot

*** Variables ***
&{Contract01}     accountType=New Customer  accountName=Test_contract_user7  salesPerson=Staff User  platformType=Connect Cloud  country=United States  firstName=DM1  lastName=User1  password=zaqwsx123!@#$  confirmPassword=zaqwsx123!@#$  email=dm1@user1.com   locationName=test_location  Address1=960 stewart dr  city=Sunnyvale  state=California  zip=94085-3912  connectivity=This Location  no_validation=True  class=bundle  product=Connect Cloud Essentials  quantity=1  location=test_location  MRR=12  NRR=23  contractNumber=369  forecastDate=04/17/2017  notes=Not Required  filePath=C:\\Users\\kkanakaraj\\Perforce\\kkanakaraj_KKANAKARAJ-3470_9628_BOSS\\BOSS\\trunk\\tools\\BossAutomationTestCases\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{Contract02}	  accountType=New Customer  accountName=AutoTest_Acc_{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=United States  firstName=boss  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}  Address1=1385 Broadway  city=New York  state=New York  zip=10018  connectivity=This Location  no_validation=False  class=bundle  product=MiCloud Connect Premier  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{ContracttoDelete}	  accountType=New Customer  accountName=AutoTest_Acc_to_delete{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=United States  firstName=boss  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_Acc_to_delete{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}  Address1=1385 Broadway  city=New York  state=New York  zip=10018  connectivity=This Location  no_validation=False  class=bundle  product=MiCloud Connect Premier  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{Contract03}	  accountType=New Customer  accountName=Test_contract_user_Ux1nT73V  salesPerson=Staff User  platformType=Connect Cloud  country=United States  firstName=boss  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_0rfgLBwf@shoretel.com  locationName=test_location_Ux1nT73V  Address1=960 stewart dr  city=Sunnyvale  state=California  zip=94085-3912  connectivity=This Location  no_validation=True  class=bundle  product=Connect Cloud Essentials  quantity=1  location=test_location_Ux1nT73V  MRR=12  NRR=23  contractNumber=369  forecastDate=04/17/2017  notes=Not Required  filePath=C:\\Users\\kkanakaraj\\Perforce\\kkanakaraj_KKANAKARAJ-3470_9628_BOSS\\BOSS\\trunk\\tools\\BossAutomationTestCases\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{Contract04}     accountType=New Customer  accountName=Test_contract_user7  salesPerson=Staff User  platformType=Connect Cloud  country=United States  firstName=boss  lastName=automation  password=zaqwsx123!@#$   confirmPassword=zaqwsx123!@#$  email=pm1@user1.com   locationName=test_location  Address1=960 stewart dr  city=Sunnyvale  state=California  zip=94085-3912  connectivity=This Location  no_validation=True  class=bundle  product=Connect Cloud Essentials  quantity=1  location=test_location  MRR=12  NRR=23  contractNumber=369  forecastDate=04/17/2017  notes=Not Required  filePath=C:\\Users\\kkanakaraj\\Perforce\\kkanakaraj_KKANAKARAJ-3470_9628_BOSS\\BOSS\\trunk\\tools\\BossAutomationTestCases\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days

&{Contract05}     accountType=New Customer  accountName=Test_contract_user7  salesPerson=Staff User  platformType=Connect Cloud  country=United States  firstName=shoretel  lastName=user  password=zaxqsc!123   confirmPassword=zaxqsc!123  email=shoretel@user1.com   locationName=test_location  Address1=960 stewart dr  city=Sunnyvale  state=California  zip=94085-3912  connectivity=This Location  no_validation=True  class=bundle  product=Connect Cloud Essentials  quantity=1  location=test_location  MRR=12  NRR=23  contractNumber=369  forecastDate=04/17/2017  notes=Not Required  filePath=C:\\Users\\kkanakaraj\\Perforce\\kkanakaraj_KKANAKARAJ-3470_9628_BOSS\\BOSS\\trunk\\tools\\BossAutomationTestCases\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{Contract06}     accountType=New Customer  accountName=Test_contract_user7  salesPerson=Staff User  platformType=Connect Cloud  country=United States  firstName=test  lastName=boss  password=shorechangeme   confirmPassword=shorechangeme  email=rodadmin@shoretel.com   locationName=test_location  Address1=960 stewart dr  city=Sunnyvale  state=California  zip=94085-3912  connectivity=This Location  no_validation=True  class=bundle  product=Connect Cloud Essentials  quantity=1  location=test_location  MRR=12  NRR=23  contractNumber=369  forecastDate=04/17/2017  notes=Not Required  filePath=C:\\Users\\kkanakaraj\\Perforce\\kkanakaraj_KKANAKARAJ-3470_9628_BOSS\\BOSS\\trunk\\tools\\BossAutomationTestCases\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{Contract07}     accountType=New Customer  accountName=Test_contract_user7  salesPerson=Staff User  platformType=Connect Cloud  country=United States  firstName=User  lastName=Delete  password=shorechangeme   confirmPassword=zaxqsc!123  email=user@user1.com   locationName=test_location  Address1=960 stewart dr  city=Sunnyvale  state=California  zip=94085-3912  connectivity=This Location  no_validation=True  class=bundle  product=Connect Cloud Essentials  quantity=1  location=test_location  MRR=12  NRR=23  contractNumber=369  forecastDate=04/17/2017  notes=Not Required  filePath=C:\\Users\\kkanakaraj\\Perforce\\kkanakaraj_KKANAKARAJ-3470_9628_BOSS\\BOSS\\trunk\\tools\\BossAutomationTestCases\\Test_files\\cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days
&{Contract_Aus}	  accountType=New Customer  accountName=AutoTest_Acc_{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=Australia  firstName=boss  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}    streetNo=441    streetName=st kilda    streetType=Road    city=Melbourne    state=Victoria    zip=3004    locfirstName=Tracy    loclastName=Victor    phoneNumber=+61224220250    no_validation=False  connectivity=This Location    class=bundle  product=Connect CLOUD Standard  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days    localAreaCode=2
&{Contract_UK}	  accountType=New Customer  accountName=AutoTest_Acc_{rand_str}  salesPerson=${bossUser}  platformType=Connect Cloud  country=United Kingdom  firstName=boss  lastName=automation  password=Abc123!!  confirmPassword=Abc123!!  email=AutoTest_{rand_str}@shoretel.com  locationName=AutoTest_location_{rand_str}    buildingName=Inspired    streetName=Easthampstead Road    city=Bracknell    zip=RG12 1YQ    connectivity=This Location    no_validation=False  class=bundle  product=Connect CLOUD Standard  quantity=1  location=AutoTest_location_{rand_str}  MRR=12  NRR=23  contractNumber=369  forecastDate=today  notes=Not Required  filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf  termVersion=Version 3.0  termLength=36 Months  termRenewalType=Automatic  termInstall=90 Days    localAreaCode=28
###### Account and Contract info US
&{Contract_US}	  accountType=New Customer
...               accountName=AutoTest_Acc_{rand_str}
...               salesPerson=Staff User
...               partnerType=No Partner
...               platformType=Connect Cloud
...               country=United States
...               SelectExistingUser=PM User
...               firstName=boss_{rand_str}
...               lastName=automation
...               password=Abc123!!
...               confirmPassword=Abc123!!
...               email=AutoTest_{rand_str}@shoretel.com
...               locationName=AutoTest_location_{rand_str}
...               Address1=1385 Broadway
...               city=New York
...               state=New York
...               zip=10018
...               connectivity=This Location
...               no_validation=True
...               class=bundle
...               product=MiCloud Connect Essentials
...               quantity=1
...               location=AutoTest_location_{rand_str}
...               MRR=12
...               NRR=23
...               contractNumber=369
...               forecastDate=today
...               notes=Not Required
...               filePath=${EXECDIR}${/}Test_files${/}cmdref.pdf
...               termVersion=Version 3.0
...               termLength=36 Months
...               termRenewalType=Automatic
...               termInstall=90 Days
...               create_partition_flag=True
...               clusterInstance=BAU
...               timezone=Pacific Standard Time
...               Failure_Add_Locations_Scenario=False
...               Error_No_Address=False
...               Error_Invalid_Address=False
...               Failure_Add_Products_Scenario=False
...               Error_No_MRR=False
...               Error_No_NRR=False
...               Error_No_Contract_Upload=False
...               Error_Msg=None