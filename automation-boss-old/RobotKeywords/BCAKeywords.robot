*** Settings ***
Documentation    Keyword supported for the BCA feature of BOSS

Library    Collections

*** Keywords ***
I retrieve user phone number
    [Arguments]  ${user_name}
    ${result}  ${phone_number}=  Retrieve Phone Number  ${user_name}
    should be true  ${result}
    [Return]  ${phone_number}

verify phone numbers and their status
    [Arguments]  &{Phone_Numbers}
    ${result}=  Verify Phone Number  &{Phone_Numbers}
    [Return]  ${result}

verify geographic location
    [Arguments]  ${location}
    ${result}=  Verify Geo Location  ${location}
    [Return]  ${result}

add geographic location
    [Arguments]  &{location}
    ${result}=  run keyword  add geo location   &{location}
    [Return]  ${result}

I create Bridged Call Appearance
    [Arguments]  ${bca_info}
    ${result}=  run keyword  create bca  ${bca_info}
    should be true  ${result}

I verify BCA
    [Arguments]  &{bca_info}
    ${result}=  run keyword  verify bca  &{bca_info}
    should be true  ${result}

I delete BCA
    [Arguments]  ${bca_info}
    ${result}=  run keyword  bca deletion   ${bca_info}
    should be true  ${result}

I verify deletion of BCA
    [Arguments]  &{bca_info}
    ${result}=  run keyword  Verify Deletion Of Bca   &{bca_info}
    should be true  ${result}

I varify Bridged Call Appearance page
    [Arguments]  ${tenant}
    ${result}=  run keyword  Verify Bca Page  ${tenant}
    should be true  ${result}

I varify Add BCA page
    ${result}=  run keyword  Verify Add Bca Page
    should be true  ${result}

I varify bca m5portal bread crumb
    [Arguments]  ${tenant}
    ${result}=  run keyword  Verify Bca M5portal Bread Crumb  ${tenant}
    should be true  ${result}

I varify cfbusy options on add bca page
    ${result}=  run keyword  Verify Call Forward Busy Field Options
    should be true  ${result}

I varify cf no answer options on add bca page
    ${result}=  run keyword  Verify Call Forward No Answer Field Options
    should be true  ${result}

I varify conferencing options on add bca page
    ${result}=  run keyword  Verify Conferencing Field Options
    should be true  ${result}

I varify enable tone checkbox on add bca page
    ${result}=  run keyword  Verify Enable Tone Check Box
    should be true  ${result}

I select bca on user prog buttons page
    [Arguments]  &{bcainfo}
    ${result}=  run keyword  Select BCA On Prog Buttons Page  &{bcainfo}
    should be true  ${result}

I copy BCA
    [Arguments]  ${bcainfo}
    ${result}=  run keyword  Copy Bca  ${bcainfo}
    should be true  ${result}

I edit BCA
    [Arguments]  ${bcainfo}
    ${result}=  run keyword  Edit Bca  ${bcainfo}
    should be true  ${result}

I verify show less settings in add bca page
    ${result}=  run keyword  Verify Show Less Settings
    should be true  ${result}

I verify show more settings in add bca page
    ${result}=  run keyword  Verify Show More Settings
    should be true  ${result}

I select and verify user on phone system users page
    [Arguments]  ${user_name}  ${params}=${None}
    ${params}=  evaluate  {} if ${params} is None else ${params}
    ${result}=
    ...  run keyword  select and verify user on phone system users  ${user_name}  &{params}
    should be true  ${result}

I enable SCA
    [Arguments]  &{sca_info}
    ${result}=  run keyword  Enable SCA  &{sca_info}
    should be true  ${result}

I verify aBCA
    [Arguments]  &{sca_info}
    ${result}=  run keyword  Verify ABCA  &{sca_info}
    should be true  ${result}

I verify copy bca page
    [Arguments]  &{bca_info}
    ${result}=  run keyword  Verify Copy Bca Page  &{bca_info}
    should be true  ${result}

I verify edit bca page
    [Arguments]  &{bca_info}
    ${result}=  run keyword  Verify Bca Edit Page  &{bca_info}
    should be true  ${result}

get required abca profile
    [Arguments]  ${name}
    ${result}  ${profile_name}=  run keyword  Get Abca Profile Name  ${name}
    should be true  ${result}
    [Return]  ${profile_name}

I find element on phone number page
    [Arguments]  ${ph_num}  ${ph_status}  ${dest_type}  ${dest}  ${expected}  ${type}=Domestic
    &{params}=  Create Dictionary  PhNum=${ph_num}  Status=${ph_status}
    ...  DestType=${dest_type}  Destination=${dest}  Type=${type}  Expected_status=${expected}
    ${result}  ${phone_state}=  run keyword  Find Entry On Phone Number Page  &{params}
    should be equal  ${result}  ${expected}
    [Return]  ${phone_state}

clean up
    [Arguments]  ${cleanAll}=${FALSE}
    run keyword  Clean Bca Suite  ${cleanAll}

I get an available line on user programming button box
    [Arguments]  ${user_name}  ${button_box}
    ${line_no}=  run keyword  Get Available Program Button Line  ${user_name}  ${button_box}
    [Return]  ${line_no}

generate element locators on program box page
    [Arguments]  ${username}  ${button_box}  ${line_no}
    ${result}  ${line_no}=  run keyword  Regenerate Programming Page Element Locators  ${username}  ${button_box}  ${line_no}
    should be true  ${result}
    [Return]  ${line_no}

I move to the required line on program button tab
    [Arguments]  ${username}  ${button_box}
    ${result}=  run keyword  Move To Line On Prog Button Page  ${username}  ${button_box}
    should be true  ${result}

I verify BCA on program button line
    [Arguments]  &{bca_info}
    ${result}=  run keyword  Verify BCA On Required Prog Button Line  &{bca_info}
    should be true  ${result}

I assign phone number to bca
    [Arguments]  ${ph_status}  ${bca_name}  ${type}=Domestic
    ${result}  ${ph_number}=  run keyword  Assign Ph Number To Bca  ${ph_status}  ${bca_name}  ${type}
    should be true  ${result}
    [Return]  ${ph_number}

I assign phone number to user
    [Arguments]  ${ph_status}  ${type}=Domestic
    ${result}  ${ph_number}=  run keyword  Assign Ph Number To User  ${ph_status}  ${type}
    should be true  ${result}
    [Return]  ${ph_number}

I select programming button function
    [Arguments]

I find bca entry on primary partition profile page
    [Arguments]     ${first_name}  ${last_name}  ${extn}  ${ph_num}  ${expected_result}
    &{param}=   Create Dictionary  FirstName=${first_name}  LastName=${last_name}
    ...  Extension=${extn}  PhoneNumber=${ph_num}
    ${result}=  run keyword  Verify Element On Primary Partition Profile Page  &{param}
    should be equal  ${result}  ${expected_result}

I go to profiles tab on primary partitions page
    ${result}=  run keyword  Switch To Profiles Tab On Primary Partition Profile Page
    should be true  ${result}

I find phone number with required status
    [Arguments]  ${ph_status}  ${type}=Domestic  ${location}=${None}  ${country}=${None}  ${destination}=-
    ${ph_number}=  run keyword  get phone number with required status  ${ph_status}  ${type}  ${location}  ${country}  ${destination}
    should not be equal  ${ph_number}  ${None}
    [Return]  ${ph_number}

I verify DNIS in D2
    [Arguments]  ${dnis}  ${tenant}  ${expected_result}
    &{dnis_info}=  Create Dictionary  dnis=${dnis}  tenant=${tenant}
    ${result}=   Run Keyword  director fetch and verify dnis  &{dnis_info}
    should be equal  ${result}  ${expected_result}

setting up the test suite
    run keyword  settingup suite

cleaning up the test suite
    run keyword  clean up

#################################################################
######
# Start -- Mahesh
######
#################################################################

I create bca from programming button page
    [Arguments]  ${bca_info}
    ${result}=
    ...  run keyword  create bca from programmable button page   ${bca_info}
    should be true  ${result}

#In D2 I verify bridged call appearance "${d2Bca:[^"]+}" is set for ${newacc}
In D2 I verify bridged call appearance ${d2Bca:[^"]+} is set for ${newacc:[^"]+} ${expected_result}
    &{D2BCA}=    Create Dictionary    exp_Bca=${d2Bca}    newacc=${newacc}
    ${result}=   Run Keyword    director verify bridged call appearance   &{D2BCA}
    should be equal  ${result}  ${expected_result}

I verify bca radio button on add bca page
    [Arguments]  ${bca_info}
    ${result}=
    ...  run keyword  create bca from programmable button page   ${bca_info}
    should not be true  ${result}
#################################################################
######
# End -- Mahesh
######
#################################################################

#################################################################
######
# Start -- Vasuja
######
#################################################################

I verify the "${buttonName:[^"]+}" button in bca
    ${result}=  run keyword  Verify Bca Page   ${buttonName}
    should be true  ${result}

I edit DNIS from Phone Numbers Page
    [Arguments]  ${info}
    ${result}=  run keyword  edit dnis on phone numbers page  ${info}
    should be true  ${result}
#################################################################
######
# End -- Vasuja
######
#################################################################