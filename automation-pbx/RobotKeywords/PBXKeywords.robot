*** Settings ***
Documentation     Keywords supported for BOSS portal
...               dev- Kenash, Rahul Doshi, Vasuja
...               Comments:

Library    Collections
*** Keywords ***

In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    &{D2loginCredentials}=    Create Dictionary      username=${D2User}       password=${D2Password}    IP=${D2IP}       URL=${url}
	Run Keyword      Director Client Login       &{D2loginCredentials}


In D2 I verify switch status @{passStatus} is set for ${appliance} and ${applianceIP}
    &{D2switchstatus}=    Create Dictionary    status=@{passStatus}    appliance=${appliance}   applianceIP=${applianceIP}
    ${result}=   Run Keyword    director verify switch status  &{D2switchstatus}
    Should be true    ${result}


In D2 I verify site status ${siteStatus} is set for ${siteName}
    &{D2switchstatus}=    Create Dictionary    siteStatus=${siteStatus}    siteName=${siteName}
    ${result}=   Run Keyword    director verify site status  &{D2switchstatus}
    Should be true    ${result}

In D2 I verify server status ${status} is set for ${appliance} and ${applianceIP}
    &{D2switchstatus}=    Create Dictionary    status=${status}    appliance=${appliance}   applianceIP=${applianceIP}
    ${result}=   Run Keyword    director verify server status  &{D2switchstatus}
    Should be true    ${result}

#Maha <Start>
In D2 I Add did ranges ${basephno} is set for ${trunkid} with ${noofphones}
    &{D2didranges}=    Create Dictionary    basephno=${basephno}    trunkid=${trunkid}   noofphones=${noofphones}
    ${result}=   Run Keyword    director add did ranges  &{D2didranges}
     Should be true    ${result}

In D2 I verify did ranges ${basephno} is set for ${trunkgrpname} with ${noofphones}
    &{D2didranges}=    Create Dictionary    basephno=${basephno}    trunkgrpname=${trunkgrpname}   noofphones=${noofphones}
    ${didid}=   Run Keyword    director get did ranges  &{D2didranges}
     [Return]    ${didid}

In D2 I Delete did ranges ${didrangesID} for ${basephno}
    &{D2didranges}=    Create Dictionary    didrangesID=${didrangesID}    basephno=${basephno}
    ${result}=   Run Keyword    director delete did ranges  &{D2didranges}
    Should be true    ${result}

In D2 I Add trunk groups ${trunkgrpname} is set for ${destinationdn}
    &{D2trunkgroups}=    Create Dictionary    trunkgrpname=${trunkgrpname}    destinationdn=${destinationdn}
    ${result}=   Run Keyword    director add trunk groups  &{D2trunkgroups}
     Should be true    ${result}

In D2 I verify trunk groups for ${trunkgrpName}
    &{D2trunkgroups}=    Create Dictionary    trunkgrpName=${trunkgrpName}
    ${trunkid}=   Run Keyword    director get trunk groups  &{D2trunkgroups}
     [Return]    ${trunkid}

In D2 I Delete trunk groups ${trunkgrpid} for ${destinationdn}
    &{D2trunkgroups}=    Create Dictionary    trunkgrpid=${trunkgrpid}    destinationdn=${destinationdn}
    ${result}=   Run Keyword    director delete trunk groups  &{D2trunkgroups}
    Should be true    ${result}

In Varibale file I Auto populate the values from ${oldvalue} to ${newvalue} in ${fileName}
	&{AutoPopulate}=		Create Dictionary		oldvalue=${oldvalue}      newvalue=${newvalue}       fileName=${fileName}
	${result}=	Run Keyword		insert values into file	&{AutoPopulate}
	Should be true		${result}

In CSV file I Auto populate the values for ${user} to ${key} and ${value} in ${fileName}
		&{AutoPopulate}=		Create Dictionary		user=${user}      key=${key}      value=${value}       fileName=${fileName}
		${result}=	Run Keyword		insert values into csv	&{AutoPopulate}
		Should be true		${result}

In D2 I get all user details of ${PhoneIP} from ${TenantName}
		&{D2callstatus}=		Create Dictionary			PhoneIP=${PhoneIP}		TenantName=${TenantName}
		#${macid}  ${phonetype}  ${firstname}  ${lastname}  ${extension}=	Run Keyword		director get all user info		&{D2callstatus}
		@{userdetails}=	Run Keyword		director get all user info		&{D2callstatus}
		#[Return]    ${macid} ${phonetype} ${firstname} ${lastname} ${extension}
		[Return]    @{userdetails}
    
#Maha <End>

#Neeraj <Start>

In D2 I verify messages ${vm_messages} and mailbox count ${mailbox_count} for voicemail server ${vm_server} with ip ${vm_server_ip} and site ${locationName}
	&{vm_dict}=		Create Dictionary	 messages=${vm_messages}	mailbox_count=${mailbox_count}	vm_server=${vm_server}	vm_server_ip=${vm_server_ip}	site=${locationName}
	${result}=  director verify voicemail server info	&{vm_dict}
    Should be true  ${result}

In D2 I verify trunk in use ${TrunkInUse} and trunk in service ${TrunkInService} for trunk group ${Trunk} with trunk type ${TrunkType} and site ${locationName}
    &{trunk_group_dict}=    Create Dictionary   TrunkInUse=${TrunkInUse}    TrunkInService=${TrunkInService}     Trunk=${Trunk}   TrunkType=${TrunkType}   site=${locationName}
    ${result}=  director verify trunk groups status     &{trunk_group_dict}
    Should be true  ${result}

In D2 I verify make me conferencing for switch ${switch} with ip ${ip_address} ,switch type ${type}, active calls ${active_calls}, in_use port ${in_use_ports}, free port ${free_ports} and site ${locationName}
    &{make_me_conf}=    Create Dictionary   switch=${switch}    ip_address=${ip_address}    type=${type}    active_calls=${active_calls}    in_use_ports=${in_use_ports}    free_ports=${free_ports}    site=${locationName}
    ${result}=      director verify make me conferencing    &{make_me_conf}
    Should be true  ${result}

In Varibale file ${file} I update key ${key} with field ${oldvalue} to value ${newvalue}
    &{UpdateRecord}=    Create Dictionary   key=${key}  file=${file}    old_val=${oldvalue}     new_val=${newvalue}
    ${result}=  Run Keyword     update values into file     &{UpdateRecord}
    Should be true  ${result}

In Varibale file ${file} I update existing key ${key} with field ${oldvalue} to new key value ${newvalue}
    &{UpdateRecord}=    Create Dictionary   key=${key}  file=${file}    old_val=${oldvalue}     new_val=${newvalue}
    ${result}=  Run Keyword     modify key in file     &{UpdateRecord}
    Should be true  ${result}
        
In Varibale file ${file} I update key ${key} with value ${value}
    &{UpdateValue}=     Create Dictionary   key=${key}  file=${file}    value=${value}
    ${result}=  Run Keyword     update single key value in file     &{UpdateValue}
    Should be true  ${result}    

I normalize did ${did} to number format
    &{did_num}=     Create Dictionary    did=${did}
    ${result}=  Run Keyword   normalize to number    &{did_num}

I fetch phone details for extension ${extn} under ${AccName} Tenant
    &{phone}=     Create Dictionary     extension=${extn}   AccName=${AccName}
    ${result}=  Run Keyword     create phone dictionary     &{phone}
    [Return]    ${result}
        
#Neeraj <End>

#Lavanya <begin>

In D2 I verify audio web switch status for ${appName}
		&{D2switchstatus}=    Create Dictionary     appName=${appName}
		${result}=   Run Keyword	director verify audio web switch status  &{D2switchstatus}
		Should be true    ${result}

In D2 I verify ip phone status ${status} is set for ${phonemac}
		&{D2ipphonestatus}=		Create Dictionary			status=${status}		phonemac=${phonemac}
		${result}=	Run Keyword		director verify ip phone status	      &{D2ipphonestatus}
		Should be true    ${result}

In D2 I verify all IM switch status is set for ${appName}
		&{D2IMswitchstatus}=	Create Dictionary		appName=${appName}
		${result}=	Run Keyword		director verify im switch status	&{D2IMswitchstatus}
		Should be true		${result}

In D2 I verify call streams in call quality for ${extn1} and ${extn2} with ${tenant}
		&{D2callstatus}=		Create Dictionary			extn1=${extn1}		extn2=${extn2}		tenant=${tenant}
		${no_of_calls_UserA_UserB} =	Run Keyword		director verify call streams in call quality		&{D2callstatus}
		[Return]    ${no_of_calls_UserA_UserB}


I verify the ${build} present in monitoring service of configuration
    &{config}=  Create Dictionary    build=${build}
    ${result}    Run Keyword		director monitoring service		&{config}
    Should be True    ${result}

I verify system page in Maintainance
    ${result}    Run Keyword		director system information
    Should be True    ${result}

I check for crash dump in ${UCBIP} using ${RPIP}
    &{pinfo}=		Create Dictionary			ucbip=${ucbip}		rpip=${rpip}
    ${result}    Run Keyword		director verify crash dump	&{pinfo}
    Should be True    ${result}

#Lavanya <End>

In D2 I get phone details for ${phone_mac} with ${AccName}
		&{pinfo}=		Create Dictionary			mac=${phone_mac}		tenant=${AccName}
		${result1}    ${result2}=	Run Keyword		director verify phone details		&{pinfo}
    #Log to console      ${result1}  ${result2}
		[RETURN]      ${result1}    ${result2}
In RP I turn down the switch ${RPIP} with command ${stopcmd}
    &{pinfo}=		Create Dictionary			ip=${RPIP}		cmd=${stopcmd}

    ${result}    Run Keyword    rp ssh cmd  &{pinfo}
    Should be True    ${result}

In RP I turn up the switch ${RPIP} with command ${startcmd}
    &{pinfo}=		Create Dictionary			ip=${RPIP}		cmd=${startcmd}
    ${result}    Run Keyword    rp ssh cmd  &{pinfo}
    Should be True    ${result}

In D2 I get switch id and status for ${sname} and also other switch info
    &{swinfo}=   Create Dictionary    sname=${sname}
    ${result1}    ${result2}    ${result3}  ${result4}=	Run Keyword		director fetch switch information		&{swinfo}
    [RETURN]      ${result1}    ${result2}    ${result3}    ${result4}

In D2 I get the other switch information for ${sname}
    &{swinfo}=   Create Dictionary    sname=${sname}
    ${result1}    ${result2}= Run keyword   director fetch other switch information   &{swinfo}
    [RETURN]      ${result1}    ${result2}
In D2 I change phone ${pid} to switch ${s2id}
    &{pinfo}=		Create Dictionary			pid=${pid}		s2id=${s2id}
    ${result}    Run Keyword		director move phone		&{pinfo}
    Should be True    ${result}

In D2 I get ${voice_mail} extension system
    &{D2voice_mail}=		Create Dictionary		voice_mail=${voice_mail}
    ${vm_extn}=  Run Keyword   director get system extn  &{D2voice_mail}
    [Return]     ${vm_extn}

    Using ${phone} I want to know the total number of phones in test
    call method    ${phone}    print_total_phones



#Maha 69xx Phones

Using ${phone} I dial the extension of ${phone_2}
    call method    ${phone}    make_call    ${phone_2}

verify ring notifications on ${phone}
    call method    ${phone}    verify_notifications_in_ring

verify notifications when connected on ${phone}
    call method    ${phone}    verify_notifications_in_connected

answer the incoming call on ${phone}
    call method    ${phone}    answer_the_call

verify ${phone} on display of ${string}
    call method    ${phone}    verify_phone_display    ${string}

verify ${phone} on display extn of ${string}
    call method    ${phone}    verify_phone_extn    ${string}

disconnect the call from ${phone}
    call method    ${phone}    disconnect_the_call

Check Phone Sanity of ${phone}
    call method  ${phone}    sanity_check

get phone display of ${phone}
    call method  ${phone}    get_phone_display
    get_phone_display

press key ${hard_key} from ${phone}
    call method  ${phone}  press_key   ${hard_key}

make conference from ${phone}
    call method  ${phone}  make_conference

consult conference from ${phone}
    call method  ${phone}  consult_conference

make blind conference from ${phone}
    call method  ${phone}  make_blind_conference

accept consult conference from ${phone}
    call method  ${phone}  accept_conference

accept blind conference from ${phone}
    call method  ${phone}  accept_blind_conference

# Call Transfer
make transfer from ${phone}
    call method  ${phone}  make_transfer

make blind transfer from ${phone}
    call method  ${phone}  make_blind_transfer

make consult transfer from ${phone}
    call method  ${phone}  make_consult_transfer

accept blind transfer from ${phone}
    call method  ${phone}  accept_blind_transfer

accept consult transfer from ${phone}
    call method  ${phone}  accept_consult_transfer

#Park and UnPark
Click on Park from ${phone}
    call method  ${phone}  click_on_park

Park the call from ${phone}
    call method  ${phone}  park_the_call

Click on UnPark from ${phone}
    call method  ${phone}  click_on_unpark

UnPark the call from ${phone}
    call method  ${phone}  unpark_the_call

#Mute and Hold
verify Mute state of ${phone}
    call method  ${phone}  verify_mute_state

verify Hold state of ${phone}
    call method  ${phone}  verify_hold_state

#HIstory and Directory
Call from History ${phone}
    call method  ${phone}  call_from_history

Go to Directory Search in ${phone}
    call method  ${phone}  go_to_directory

Get Unread Voice Mail Count from ${phone}
    ${result} =  call method  ${phone}  get_vm_count
    [Return]     ${result}

verify count ${phone} ${num} ${num2} ${count}
    call method  ${phone}  verify_count    ${num}  ${num2}  ${count}

Call from Directory ${phone}
    call method  ${phone}  call_from_directory

quit voice mail from ${phone}
    call method  ${phone}  quit_voice_mail

Using ${phone_1} I dial the digits ${number}
    call method    ${phone_1}    input_a_number    ${number}

verify led ${led_name} state ${led_state} of ${phone}
    call method    ${phone}     verify_led_state   ${led_name}       ${led_state}

verify Message wait led state of ${phone}
    call method    ${phone}     verify_msgwait_led_state

Verify ${phone} audio is on hold with ${phone_1}
    call method    ${phone}     check_audio_is_on_hold   ${phone_1}

press voice mail soft key on ${phone}
    call method   ${phone}   press_vm_soft_key

press voice mail hard key on ${phone}
    call method     ${phone}    press_vm_hard_key

Login to voicemail on phone ${phone} using password ${pin}
    call method     ${phone}   login_to_voicemail   ${pin}