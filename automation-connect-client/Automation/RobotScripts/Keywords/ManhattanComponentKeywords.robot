*** Settings ***
Documentation     Keywords supported for Teamwork portal
...               dev-aakash
...               Comments:
Library           ../../../../Framework-client/utils/CSVReader.py  USERS.csv   automation-connect-client

*** Variables ***


*** Keywords ***
# StartHubNode
    # Run Process   ${CURDIR}/start.bat
    #Sleep     5s

Login with ${client} and ${username} and ${password} and ${url}        
    &{params}=        Create Dictionary            username=${username}      password=${password}      server_address=${url}    
    call method    ${client}       client_login                    &{params}
    
Search People Extension with ${client} and ${searchitem}
    &{params}=                     Create Dictionary            searchItem=${searchitem}
    call method      ${client}        search_people_extension                  &{params}

Type Value In Extension Search with ${client} and ${searchitem}
    &{params}=                     Create Dictionary            searchItem=${searchitem}
    call method      ${client}        type_value_in_extension_search                  &{params}

Click Filter Message with ${client} and ${filter}
    &{params}=                   Create Dictionary               filter=${filter}
    call method      ${client}          click_filter_message               &{params}
    
Add User To Conversation with ${client} and ${name} and ${checkname}
    &{params}=                   Create Dictionary               name=${name}			checkname=${checkname}  
    call method      ${client}          add_contact_conversation               &{params}
    
Send IM with ${client} and ${message}
    &{params}=                  Create Dictionary                message=${message}
    call method      ${client}          send_IM                      &{params}
    
Invoke Dashboard Tab with ${client} and ${option}
    &{params}=                   Create Dictionary                 option=${option}
    ${runtype}=   call method      ${client}          invoke_dashboard_tab              &{params}
    [return]  ${runtype}
    
Received IMB with ${client} and ${status} and ${message}
    &{params}=                      Create Dictionary                 status=${status}            message=${message} 
    call method      ${client}          received_IMB               &{params}
    
Received IMA with ${client} and ${status} and ${message}
    &{params}=                      Create Dictionary                 status=${status}            message=${message} 
    call method      ${client}          received_IMA               &{params}
    
Create New Group with ${client} and ${groupName} and ${choice} and ${contact1} and ${contact2}
    &{params}=    Create Dictionary    groupName=${groupName}    choice=${choice}    contact1=${contact1}    contact2=${contact2}
    call method    ${client}    create_new_group    &{params}

Create New Group generating members with ${client} and ${groupName} and ${choice} and ${first_grp_member} and ${number}
    &{params}=    Create Dictionary    groupName=${groupName}    choice=${choice}    first_grp_member=${first_grp_member}    number=${number}
    call method    ${client}    create_new_group    &{params}

Enter Group Name with ${client} and ${groupName}
    &{params}=    create Dictionary    groupName=${groupName}
    call method    ${client}    enter_group_name    &{params}

Drag Drop Contact To Group with ${client} and ${groupName} and ${contact1} and ${contact2}
    &{params}=    create Dictionary    groupName=${groupName}    contact1=${contact1}    contact2=${contact2}
    call method    ${client}    drag_drop_contact_to_group    &{params}

Create New Contact with ${client} and ${pos} and ${phType} and ${num} and ${first_name} and ${last_name} and ${company} and ${department} and ${email}
    &{params}=    create Dictionary    pos=${pos}    phType=${phType}    num=${num}    first_name=${first_name}    last_name=${last_name}    company=${company}    department=${department}    email=${email}
    call method     ${client}     create_new_contact     &{params}

Initiate Search Close Dialog with ${client} and ${search_item}
    &{params}=      Create Dictionary     search_item=${search_item}
    call method     ${client}     initiate_search_and_close     &{params}

Select Group Options with ${client} and ${groupName} and ${contact1} and ${contact2} and ${contact3} and ${contact4} and ${option}
    &{params}=             Create Dictionary           groupName=${groupName}           contact1=${contact1}          contact2=${contact2}       contact3=${contact3}       contact4=${contact4}      option=${option} 
    call method      ${client}          select_group_options            &{params}
    
Close Application with ${client}
    call method    ${client}    close_application

Close Presenter with ${client}
    call method    ${client}    close_presenter    

Verify Second Panel with ${client} and ${panelName} and ${option} 
    &{params}=             Create Dictionary              panelName=${panelName}         option=${option}
    call method      ${client}             verify_second_panel          &{params}

Edit Group with ${client} and ${groupName} and ${contact1}
    &{params}=             Create Dictionary              groupName=${groupName}         contact1=${contact1}
    call method      ${client}        edit_group         &{params}
    
Modify Group Add Member with ${client} and ${groupName} and ${contact1} and ${contact2} and ${choice} and ${newGroupName} and ${discardMyChanges}
    &{params}=     Create Dictionary     groupName=${groupName}    contact1=${contact1}    contact2=${contact2}    choice=${choice}    newGroupName=${newGroupName}    discardMyChanges=${discardMyChanges} 
    call method      ${client}          modify_group_add_member         &{params}
    
Verify Third Panel with ${client} and ${option}
    &{params}=             Create Dictionary                 option=${option} 
    call method      ${client}         verify_third_panel             &{params}
    
Close Panel with ${client} and ${panel}
    &{params}=             Create Dictionary                 panel=${panel}
    call method      ${client}         close_panel                &{params}
    
Modify Group Del Member with ${client} and ${groupName} and ${contact1} and ${contact2} and ${choice} and ${discardMyChanges}
    &{params}=             Create Dictionary              groupName=${groupName}         contact1=${contact1}       contact2=${contact2}            choice=${choice}        discardMyChanges=${discardMyChanges} 
    call method      ${client}         modify_group_del_member                &{params}
    
Delete Group with ${client} and ${groupName} and ${option}
    &{params}=              Create Dictionary              groupName=${groupName}         option=${option}
    call method      ${client}            delete_group           &{params}
    
Display Group List with ${client} and ${groupName} and ${groupName1}
    &{params}=              Create Dictionary              groupName=${groupName}         groupName1=${groupName1}
    call method      ${client}             display_group_list           &{params}
    
Check User Detail Attribute with ${client} and ${option} and ${check}
    &{params}=              Create Dictionary              option=${option}          check=${check}
    call method      ${client}            check_user_detail_attribute          &{params}
    
Call Control with ${client} and ${option} and ${user} and ${did}
    &{params}=              Create Dictionary          option=${option}       user=${user}     did=${did}
    call method      ${client}        call_control         &{params}

Place End Call with ${client} and ${option} and ${user}
    &{params}=              Create Dictionary              option=${option}         user=${user}
    call method      ${client}        place_end_call         &{params}

Place End DID Call with ${client} and ${option} and ${did}
    &{params}=              Create Dictionary              option=${option}         did=${did}
    call method      ${client}        place_end_call         &{params}
        
Check Incoming Call with ${client}
    call method      ${client}             check_incoming_call
    
Add Participants For Park Call with ${client} and ${option} and ${user} 
    &{params}=              Create Dictionary              option=${option}        user=${user}
    call method      ${client}                     add_participants_for_park_call           &{params}
    
End Hold Call From Client Pane with ${client} and ${option}
    &{params}=              Create Dictionary              option=${option}
    call method      ${client}        end_hold_call_from_client_pane         &{params}
    
Verify No Ongoing Call with ${client}
    call method      ${client}             verify_no_ongoing_call         
    
Add Canned Message Whitespaces with ${client} and ${message}
    &{params}=              Create Dictionary              message=${message}
    call method      ${client}           add_canned_message_whitespaces         &{params}
    
Cleanup Favorites with ${client} 
    call method    ${client}    cleanup_favorites

Cleanup Voicemails with ${client} 
    call method    ${client}    cleanup_voicemails    
    
Cleanup Groups with ${client} 
    call method    ${client}    cleanup_groups
    
Cleanup Canned Msgs with ${client}
    call method    ${client}    cleanup_canned_msgs
    
Add Canned Message Without Option with ${client} and ${message} 
    &{params}=              Create Dictionary              message=${message}
    call method      ${client}           add_canned_message_without_option         &{params}
 
Verifying Default User Presence with ${client} and ${user_list}
    &{params}=              Create Dictionary              user_list=${user_list}
    call method      ${client}             verifying_default_user_presence         &{params}
    
Verify Contact Card Status with ${client} and ${option} and ${username} and ${status}
    &{params}=              Create Dictionary              option=${option}          username=${username}     status=${status}
     call method      ${client}             verify_contact_card         &{params}

Click Mute Button with ${client} and ${mute} 
    &{params}=              Create Dictionary              mute=${mute}          
    call method      ${client}             click_mute_button         &{params}
    
Click Unmute Button with ${client} and ${unmute} 
    &{params}=              Create Dictionary              unmute=${unmute}          
    call method      ${client}             click_mute_button         &{params}
    
Check Client Panel with ${client} and ${user} and ${callType} and ${noOfCalls} and ${checkhold}
    &{params}=              Create Dictionary              user=${user}          callType=${callType}       noOfCalls=${noOfCalls}        checkhold=${checkhold}
    call method      ${client}             check_client_panel         &{params}

Open Outlook Tab with ${client}
    call method      ${client}    open_outlook_tab
    
Configure Outlook Tab with ${client} and ${option} and ${donot_open_outlook}
    &{params}=              Create Dictionary              option=${option}          donot_open_outlook=${donot_open_outlook}
    call method      ${client}             configure_outlook_tab         &{params}
    
Go To New Contact with ${client}
    call method      ${client}    go_to_new_contact
    
Add Contact Number with ${client} and ${pos} and ${phType} and ${num}
    &{params}=              Create Dictionary              pos=${pos}          phType=${phType}         num=${num}
    call method      ${client}             add_contact_number         &{params}

Add Contact Details with ${client} and ${first_name} and ${last_name} and ${email} and ${title} and ${department} and ${company} and ${address} and ${city} and ${country}
    &{params}=              Create Dictionary              first_name=${first_name}          last_name=${last_name}         company=${company}      department=${department}      email=${email}      title=${title}      address=${address}      city=${city}      country=${country}
    call method      ${client}             add_contact_details         &{params}
    
Call Contact By DoubleClick with ${client} and ${searchitem}
    &{params}=                     Create Dictionary            searchItem=${searchitem}
    call method      ${client}        call_contact_by_doubleclick                  &{params}
    
Check Uncheck Close Contact Card with ${client} and ${click} and ${option} and ${close}
    &{params}=                     Create Dictionary            click=${click}        option=${option}       close=${close}
    call method      ${client}             check_uncheck_close_contact_card           &{params}
    
Verify Hold Unhold In Third Panel with ${client} and ${option}
    &{params}=                     Create Dictionary            option=${option}
    call method      ${client}        verify_hold_unhold_in_third_panel                  &{params}
    
Presence Color Active with ${client} and ${verifycolor} and ${orange} 
    &{params}=                     Create Dictionary            verifycolor=${verifycolor}        orange=${orange}       
    call method      ${client}           presence_color_active                  &{params}
    
Verify Call Behaviour Items with ${client} 
    call method      ${client}    verify_Call_behaviour_items
    
Verify External Assignment with ${client}
    call method       ${client}       verify_external_assignment
    
Blind Audio Conference Call with ${client} and ${option} and ${user}    
    &{params}=                     Create Dictionary            option=${option}        user=${user}       
    call method      ${client}           blind_audio_conference_call                  &{params}

Click Send Cannedresponse Incall with ${client} and ${response} 
    &{params}=                     Create Dictionary            response=${response}             
    call method      ${client}           Click_send_cannedresponse_incall                  &{params}

Press Escape with ${client} and ${option}
    &{params}=       Create Dictionary      option=${option}
    call method      ${client}           press_escape       &{params}

Press Key with ${client} and ${key} and ${times}
    &{params}=       Create Dictionary       key=${key}      times=${times}
    call method      ${client}            press_key         &{params}

Scroll Search Extension Result with ${client}
    call method      ${client}    scroll_search_people_extension_result

Verify Search People List Closed with ${client}
    call method      ${client}    verify_search_people_list_closed

Verify Park Call with ${client}
    call method      ${client}    verify_park_call
     
Verify Park Call In Client with ${client} and ${option}
    &{params}=                     Create Dictionary            option=${option}        
    call method      ${client}             verify_park_call_in_client				&{params}    
     
Verify Click User Dashboard with ${client} and ${contact}
    &{params}=                     Create Dictionary            contact=${contact}               
    call method      ${client}           verify_click_user_dashboard                  &{params}

Verify Hold Consult In Conf Call with ${client} and ${option}
    &{params}=                     Create Dictionary            option=${option}               
    call method      ${client}           verify_hold_consult_in_conf_call                  &{params}

Click Barge Call In Client with ${client} and ${option}    
    &{params}=    Create Dictionary    option=${option}
    call method    ${client}    click_barge_call_in_client    &{params}

Verify Users In A Dashboard In Call with ${client} and ${option} and ${user1} and ${user2}  
    &{params}=    Create Dictionary    option=${option}    user1=${user1}    user2=${user2}    
    call method    ${client}    verify_users_in_a_dashboard_in_call    &{params}

Verify Three Users In A Dashboard In Call with ${client} and ${option} and ${user1} and ${user2} and ${user3}  
    &{params}=    Create Dictionary    option=${option}    user1=${user1}    user2=${user2}    user3=${user3}    
    call method    ${client}    verify_users_in_a_dashboard_in_call    &{params}

Check User Mute In Transfer with ${client} and ${check}
    &{params}=                     Create Dictionary            check=${check}               
    call method      ${client}           check_user_mute_in_transfer                  &{params}

Click Send Any Cannedresponse Incall with ${client}
    call method      ${client}    Click_send_any_cannedresponse_incall 

Verify Default Call Panel Click Vm with ${client}
    call method      ${client}    verify_default_call_panel_click_vm

Check Badge Count with ${client} and ${tab}
    &{params}=                     Create Dictionary            tab=${tab}               
    call method      ${client}           check_badge_count                  &{params}

Verify Hold User Dashboard with ${client} and ${name} and ${option}
    &{params}=                     Create Dictionary            name=${name}        option=${option}       
    call method      ${client}           verify_hold_user_dashboard                  &{params}
 
Add Or Delete To Favorite Group with ${client} and ${peopleName} and ${option}
    &{params}=                     Create Dictionary            peopleName=${peopleName}        option=${option}       
    call method      ${client}           add_or_delete_to_favorite_group                  &{params}

Check Favorite Symbol with ${client} and ${status} and ${peopleName} 
    &{params}=                     Create Dictionary            status=${status}         peopleName=${peopleName}            
    call method      ${client}           check_favorite_symbol                  &{params}

Search People For Multiuser with ${client} and ${searchItem}
    &{params}=                     Create Dictionary            searchItem=${searchItem}               
    call method      ${client}           search_people_for_multiuser                  &{params}

Verify Preferences Power Routing Tab with ${client}
    call method      ${client}           verify_preferences_power_routing_tab

Create New Power Rule with ${client} and ${ruleName}
    &{params}=                     Create Dictionary    ruleName=${ruleName}               
    call method      ${client}           create_new_power_rule    &{params}

Click On My Availabilty with ${client}
    call method      ${client}           click_on_my_availabilty
    
Click Forward Call Button with ${client}
    call method      ${client}           click_forward_call_button

Configure Forward Call with ${client} and ${radio} and ${optionOrText}
    &{params}=                     Create Dictionary            radio=${radio}          optionOrText=${optionOrText}          
    call method      ${client}           configure_forward_call                  &{params}

Create Rule Check Error with ${client} and ${ruleName} and ${tabName}
     &{params}=                     Create Dictionary            ruleName=${ruleName}          tabName=${tabName}          
    call method      ${client}           create_rule_check_error                  &{params}

Remove Rule Option with ${client} and ${option}    
    &{params}=                     Create Dictionary            option=${option}               
    call method      ${client}           remove_rule_option                  &{params}

Edit Rule with ${client} and ${ruleName}
    &{params}=    create Dictionary    ruleName=${ruleName}
    call method    ${client}    edit_rule    &{params}

Edit Rule Check Error with ${client} and ${ruleName} and ${tabName}
    &{params}=    create Dictionary    ruleName=${ruleName}    tabName=${tabName}
    call method    ${client}    edit_rule_check_error    &{params}

Click On Number Matches with ${client}
    call method    ${client}    click_on_number_matches

Add Number Matches with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}    add_number_matches    &{params}

Save Rule with ${client} and ${ruleName}
    &{params}=    create Dictionary    ruleName=${ruleName}
    call method    ${client}    save_rule    &{params}

Configure My Availabilty with ${client} and ${text}
    &{params}=                     Create Dictionary            text=${text}               
    call method      ${client}           configure_my_availabilty                  &{params}

Invoke Dashboard Tab Event with ${client} and ${option} and ${exchange_username} and ${exchange_password}
    &{params}=                   Create Dictionary                 option=${option}           exchange_username=${exchange_username}           exchange_password=${exchange_password}
    call method      ${client}          invoke_dashboard_tab              &{params}

Open New Event with ${client}
    call method    ${client}    open_new_event
    
Events Add Meeting Details with ${client} and ${name} and ${duration}
    &{params}=    Create Dictionary    name=${name}    duration=${duration}
    call method    ${client}    events_add_meeting_details    &{params}

Events Select Meeting Type with ${client} and ${option} 
    &{params}=                     Create Dictionary            option=${option}               
    call method      ${client}           events_select_meeting_type                  &{params}

Verifying Event Details with ${client} and ${entity} and ${label}
    &{params}=                     Create Dictionary            entity=${entity}             label=${label}   
    call method      ${client}           verifying_event_details                  &{params}

Events Meeting Type Add User with ${client} and ${option} and ${username}
    &{params}=                     Create Dictionary            option=${option}             username=${username}   
    call method      ${client}           events_meeting_type_add_user                  &{params}

Events Meeting Type Add Users with ${client} and ${option} and ${username1} and ${username2}
    &{params}=    Create Dictionary    option=${option}    username1=${username1}    username2=${username2}
    call method    ${client}    events_meeting_type_add_user    &{params}

Events Change Meeting Settings with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}    events_change_meeting_settings    &{params}

Configure Meeting Settings with ${client} and ${option} and ${join_audio}
    &{params}=    create Dictionary    option=${option}    join_audio=${join_audio}
    call method    ${client}    configure_meeting_settings    &{params}

Events Create Invite with ${client}
    call method      ${client}    events_create_invite

Send Meeting Request Outlook with ${client} and ${option} and ${meeting_name}
    &{params}=                     Create Dictionary            option=${option}             meeting_name=${meeting_name}   
    call method      ${client}           send_meeting_request_outlook                  &{params}

Change User Telephony Status with ${client} and ${status}
    &{params}=    Create Dictionary    status=${status}
    call method    ${client}    change_user_telephony_status    &{params}

Check User Telephony Presence with ${client} and ${status} and ${color}
    &{params}=          Create Dictionary          status=${status}         color=${color}
    call method       ${client}          check_user_telephony_presence                 &{params}

Search All Groups Contact Member with ${client} and ${contact1} and ${contact2} and ${type}
    &{params}=                     Create Dictionary            contact1=${contact1}             contact2=${contact2}          type=${type}
    call method      ${client}           search_all_groups_contact_member                  &{params}

Scroll search results use keyboard with ${client} and ${scroll_option} and ${search_item}
    &{params}=      Create Dictionary      scroll_option=${scroll_option} search_item=${search_item}
    call method      ${client}           scroll_search_results_use_keyboard                  &{params}
    
Check Presence In Third Panel with ${client} and ${personName} and ${status}
    &{params}=    Create Dictionary    personName=${personName}    status=${status}       
    call method      ${client}           check_presence_in_third_panel                  &{params}    
    
Make call press enter with ${client} and ${searchItem} and ${pressEnter} and ${username}
    &{params}=       Create Dictionary        searchItem=${searchItem}      pressEnter=${pressEnter}       username=${username}
    call method      ${client}           make_call_press_enter                  &{params}

Show Contact Info Right Click with ${client} and ${option} and ${contact_info} and ${info_to_verify}
    &{params}        Create Dictionary        option=${option}        contact_info=${contact_info}       info_to_verify=${info_to_verify}
    call method      ${client}           show_contact_info_right_click                  &{params}

Call By Click Number Searched Contact with ${client}
    call method      ${client}    call_by_click_number_searched_contact

Select Phone Type with ${client} and ${phone_type} and ${soft} 
    &{params}=    Create Dictionary    phone_type=${phone_type}    soft=${soft}            
    call method    ${client}    select_phone_type    &{params}    
    
Call Contact From Recent History with ${client} and ${option} and ${contact_name}
    &{params}=          Create Dictionary         option=${option}      contact_name=${contact_name}     
    call method      ${client}          call_contact_from_recent_history         &{params}

Call Contact From Recent History Without Contact with ${client} and ${option}
    &{params}=          Create Dictionary         option=${option}          
    call method      ${client}          call_contact_from_recent_history         &{params}
    
Create Meeting Outlook with ${client} and ${meeting_name} and ${recipient1} and ${recipient2}
    &{params}=            create Dictionary     meeting_name=${meeting_name}       recipient1=${recipient1}        recipient2=${recipient2}
    call method      ${client}          create_meeting_outlook              &{params}

Play Unread Voicemails Via Phone with ${client}
    call method    ${client}    play_unread_voicemails_via_phone

Reply Forward Voicemail with ${client} and ${option} and ${subject} and ${recipient} and ${recording_device} and ${vm_type}
    &{params}=          create Dictionary       option=${option}     subject= ${subject}    recipient=${recipient}     recording_device=${recording_device}     vm_type=${vm_type}
    call method    ${client}    reply_forward_voicemail    &{params}

Play Pause Read Vms with ${client} and ${panel} and ${option} and ${vmNumber} and ${playingDevice}
    &{params}=     Create Dictionary        panel=${panel}     option=${option}     vmNumber=${vmNumber}      playingDevice=${playingDevice}
    call method    ${client}    play_pause_read_vms     &{params}

Delete Voicemails with ${client} and ${type} and ${sender}
    &{params}=     Create Dictionary     type=${type}     sender=${sender}
    call method     ${client}     delete_voicemails      &{params}

Restore Voicemail with ${client} and ${sender} and ${type} 
    &{params}=     Create Dictionary     sender=${sender}      type=${type}
    call method     ${client}     restore_voicemail      &{params}

Save Unsave Voicemail with ${client} and ${option} and ${vm_to_save} and ${sender}
    &{params}=     Create Dictionary     option=${option}     vm_to_save=${vm_to_save}    sender=${sender}
    call method    ${client}      save_unsave_voicemail      &{params}

Open Contact Card with ${client} and ${option} and ${name}
    &{params}=     Create Dictionary     option=${option}     name=${name}
    call method    ${client}       open_contact_card        &{params} 

Logout with ${client} and ${windowNumber}
    &{params}=     Create Dictionary      windowNumber=${windowNumber}
    call method     ${client}     logout      &{params}

Click Pin with ${client}
    call method     ${Client}     click_pin

Click Pinned with ${client}
    call method     ${client}     click_pinned

Check Pinned with ${client}
    call method      ${client}     check_pinned

Open Own User Detail with ${client}
    call method     ${client}     open_own_user_detail

Send Group Vm with ${client} and ${recording_device} and ${option}
    &{params}     create Dictionary      recording_device=${recording_device}      option=${option}
    call method     ${client}     send_group_vm      &{params}

Open Event Info with ${client} and ${event_name} and ${info}
    &{params}=     create Dictionary    event_name=${event_name}    info=${info}
    call method     ${client}     open_event_info      &{params}

Join Endo Conference with ${client} and ${option} and ${join_on} and ${joining_device}
    &{params}=    create Dictionary    option=${option}    join_on=${join_on}    joining_device=${joining_device}
    call method    ${client}    join_endo_conference    &{params}

Verifying Event Users Avail with ${client} and ${user} and ${user_list}
    &{params}=    create Dictionary    user=${user}    user_list=${user_list}
    call method    ${client}    verifying_event_users_avail    &{params}

Open Conference Panel with ${client} and ${event_name}
    &{params}=    create Dictionary    event_name=${event_name}
    call method    ${client}    open_conference_panel    &{params}

Call Contact By Double Click with ${client} and ${searchItem}
    &{params}=        create Dictionary      searchItem=${searchitem}
    call method     ${client}      call_contact_by_doubleclick       &{params}

Double Click Dashboard Notification with ${client} and ${license_type} and ${notification_type}
    &{params}=        create Dictionary     license_type=${license_type}     notification_type=${notification_type}
    call method     ${client}      double_click_dashboard_notification       &{params}

Handle Workgroup Login with ${client} and ${present} and ${login} and ${workGroupName}
    &{params}=     create Dictionary     present=${present}     login=${login}     workGroupName=${workGroupName}
    call method     ${client}      handle_workgroup       &{params}

Handle Workgroup Logout with ${client}
    call method     ${client}      handle_workgroup_logout

Check Favourite Symbol From Search ${client} and ${peopleName}
    &{params}=     create Dictionary     peopleName=${peopleName}
    call method     ${client}      check_favorite_symbol_from_search      &{params}

Verify Contact Listing with ${client}
    call method     ${client}      verify_contact_listing

Verify Mandatory Contact Fields with ${client} and ${firstName} and ${lastName}
    &{params}=    create Dictionary    firstName=${firstName}    lastName=${lastName}
    call method     ${client}    verify_manditory_contact_fields     &{params}

Verify Contact Info with ${client} and ${status} and ${pager} and ${title} and ${dept} and ${company} and ${address} and ${city} 
    &{params}=     create Dictionary    status=${status}    pager=${pager}     title=${title}      dept=${dept}    company=${company}     address=${address}     city=${city} 
    call method     ${client}    verify_contact_info    &{params}

Delete Contact with ${client} and ${first_name} and ${last_name}
    &{params}=    create Dictionary       first_name=${first_name}       last_name=${last_name}
    call method     ${client}      delete_contact     &{params}

Click verify recent conference call with ${client}
    call method     ${client}      Click_verify_recent_conf_call

Click Filter Under Greeny Button with ${client} and ${filter}
    &{params}=     create Dictionary      filter=${filter}
    call method     ${client}     click_filter_under_greeny_button      &{params}

Click First Visible Result In Search with ${client}
    call method     ${client}     click_first_visible_result_in_search

Click First Result in Directory with ${client}
    call method     ${client}     click_first_result_in_directory

Verify User Notifications with ${client} and ${user}
    &{params}=     create Dictionary      user=${user}
    call method     ${client}     verify_user_notifications      &{params}

Verify User Notifications Click with ${client} and ${user}
    &{params}=     create Dictionary      user=${user}
    call method     ${client}     verify_user_notifications_click      &{params}

Complete the Intercom Transfer with ${client} and ${option}
    &{params}=              Create Dictionary          option=${option}
	call method      ${client}        consult_trans_or_conf_Call          &{params}

Complete Consult Call with ${client} and ${option}
    &{params}=    Create Dictionary    option=${option}
	call method    ${client}    consult_trans_or_conf_Call    &{params}

Search the Member In Groups with ${client} and ${contact1} and ${option}
    &{params}=              Create Dictionary          user=${contact1}          option=${option}
	call method      ${client}        search_member_group          &{params}

Open Compact View In Group with ${client} and ${option}
    &{params}=              Create Dictionary          option=${option}
    call method      ${client}        open_compact_view_in_group		&{params}

Share_Call_Screen with ${client} and ${share} and ${share_option}
    &{params}=     create Dictionary      share=${share}			share_option=${share_option}	
    call method     ${client}     share_call_screen      &{params}

Verify In Call with ${client} and ${user} and ${callprogress} and ${count} and ${callconsult} and ${callhold}
    &{params}=    create Dictionary    user=${user}    callprogress=${callprogress}    count=${count}    callconsult=${callconsult}    callhold=${callhold}
    call method     ${client}     verify_INCALL     &{params}

Place Blind Conf Call with ${client} and ${user} and ${consult}
    &{params}=     create Dictionary     user=${user}     consult=${consult}
    call method     ${client}     place_blind_conf_call      &{params}

Verify Preferences Call Routing Page with ${client}
    call method     ${client}     verify_preferences_call_routing_page

Verify Preferences Basic Routing Change Panels with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}    verify_preferences_basic_routing_change_panels    &{params}

Interacting_With Greeting AllowVM with ${client} and ${allow}
    &{params}=     create Dictionary     allow=${allow}
    call method     ${client}     interacting_with_greeting_allow_VM      &{params}

Click On The Phone with ${client}
    call method    ${client}    click_on_the_phone

Verify Log Files Creation with ${client}
    call method    ${client}    verify_log_files_creation
    
Verify Im Textarea with ${client} and ${content1} and ${Split} 
    &{params}=     create Dictionary     content1=${content1}          Split=${Split}
    call method     ${client}     verify_im_textarea      &{params}
    
Verify Im Textarea Hint Not Present with ${client} and ${IM} and ${option}
    &{params}=     create Dictionary       IM=${IM}          option=${option}
    call method     ${client}     verify_im_textarea_hint_not_present      &{params}
    
Verify Im Textarea Check Sent Text with ${client}
    call method     ${client}     verify_im_textarea_check_sent_text      &{EMPTY}
     
Chat Add Participants with ${client} and ${personname}
    &{params}=     create Dictionary       personname=${personname}
    call method     ${client}     chat_add_participants        &{params}
    
Sub Process ${params}
    &{params}=      Create Dictionary        params=${params}
    ${result}=     Sub Process       &{params}
    [return]      ${result}

Edit Contact Set Blank Values with ${client} and ${title} and ${dept} and ${company} and ${address} and ${city} 
    &{params}=              Create Dictionary              company=${company}       dept=${dept}           title=${title}      address=${address}      city=${city}      
    call method      ${client}             edit_contact_set_blank_values         &{params}
    
Show Verify ContactCard with ${client} and ${mode} and ${search} and ${contact}   
    &{params}=     create Dictionary     mode=${mode}        search=${search}        contact=${contact}
    call method     ${client}      show_verify_contactCard      &{params}
    
Drag The Call And Hover with ${client} and ${searchItem} and ${option} and ${callName} and ${release}
    &{params}=     create Dictionary      searchItem=${searchItem}        option=${option}        callName=${callName}        release=${release}
    call method     ${client}      drag_the_call_and_Hover      &{params}

Call Contact By Doubleclick Search People with ${client} and ${personname} 
    &{params}=     create Dictionary     personname=${personname}
    call method     ${client}      call_contact_by_doubleclick_search_people      &{params}

End Voicemail Call with ${client}
    call method     ${client}      end_voicemail_call

Search Contact Using DID with ${client} and ${searchItem}
    &{params}=     create Dictionary     searchItem=${searchItem}       
    call method     ${client}      search_contact_using_DID      &{params}    
   
Verify Contact Card with ${client} and ${option} and ${username}
    &{params}=     create Dictionary       option=${option}         username=${username}
    call method     ${client}     verify_contact_card        &{params}  

Launch Login with ${user1} and ${user2} and ${user3} and ${user4} and ${client_count} 
    &{params}=      Create Dictionary        user1=${user1}    user2=${user2}    user3=${user3}    user4=${user4}    client_count=${client_count}    
    ${result}=     Launch Login       &{params}
    [return]      ${result}
    
Close Applications with ${params}
    &{params}=     Create Dictionary        params=${params}     
    Close Applications         &{params}          
    
Verify Im Chat Time with ${client}
    call method     ${client}      verify_im_chat_time
      
Verify Im First Chat Time with ${client}
    call method     ${client}      verify_im_first_chat_time
    
Open Dialpad with ${client}
    call method     ${client}      open_dialpad

Click Dialpad Numbers with ${client} and ${dial}
    &{params}=    create Dictionary    dial=${dial}
    call method    ${client}    click_dialpad_numbers    &{params}
    
Verify Dialpad with ${client} 
    call method     ${client}      verify_dialpad
    
Close Dialpad Search with ${client}
    call method     ${client}      close_dialpad_search

Select Play Delete Recent Voicemail with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}     select_play_delete_recent_voicemail    &{params}

Restore Voicemail Recent with ${client} and ${option} and ${choice} and ${sender}
    &{params}=    create Dictionary    option=${option}    choice=${choice}    sender=${sender}
    call method    ${client}    restore_voicemail_recent    &{params}

Check Restored VM with ${client} and ${sender}
    &{params}=    create Dictionary    sender=${sender}
    call method    ${client}    check_restored_vm     &{params}

Select People View with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}    select_people_view    &{params}

Check Created Groups with ${client} and ${groupName1} and ${groupName2} and ${groupName3} and ${groupName4} and ${groupName5}
    &{params}=    create Dictionary    groupName1=${groupName1}    groupName2=${groupName2}    groupName3=${groupName3}    groupName4=${groupName4}    groupName5=${groupName5}
    call method    ${client}    check_created_group    &{params}

Check Created Group Contacts with ${client} and ${contact1} and ${contact2}
    &{params}=    create Dictionary    contact1=${contact1}    contact2=${contact2}
    call method    ${client}    check_created_group    &{params}

Select Tab with ${client} and ${tabName} and ${panelName}
    &{params}=    create Dictionary    tabName=${tabName}    panelName=${panelName}
    call method    ${client}    select_tab    &{params}
    
Verify Find Me Select Number with ${client} and ${dropdown}
    &{params}    create Dictionary    dropdown=${dropdown}
    call method    ${client}    verify_find_me_select_number    &{params}

Verify Find Me Label Number Present1 with ${client}
    call method    ${client}    verify_find_me_label_number_present1

Basic Routing Configure Find Me with ${client} and ${addOrCheck} and ${label2} and ${number1}
    &{params}=    create Dictionary    addOrCheck=${addOrCheck}    label2=${label2}    number1=${number1}
    call method    ${client}    basic_routing_configure_find_me_label_maxlen    &{params}

Verify Findme Panel Number with ${client} and ${number1} and ${number2}
    &{params}=    create Dictionary    number1=${number1}    number2=${number2}
    call method    ${client}    verify_findme_panel_number    &{params}

Open Own User Preferences with ${client}
    call method    ${client}    open_own_user_preferences

Open Notifications Tab with ${client}
    call method    ${client}    open_notifications_tab

Open Preferences Notifications Popup with ${client} 
    call method    ${client}    open_preferences_notifications_popup

Check Uncheck Popup Option with ${client} and ${option} and ${check}
    &{params}=    create Dictionary    option=${option}    check=${check}
    call method    ${client}    check_uncheck_popup_option    &{params}

To Check Incoming IM voiceMail with ${client} and ${option} and ${check}
    &{params}=    create Dictionary    option=${option}    check=${check}
    call method    ${client}    to_check_incoming_IM_voiceMail    &{params}

Telephony Presence Status With Contactlist with ${client} and ${groupName} and ${verifycolor}
    &{params}=    create Dictionary    groupName=${groupName}    verifycolor=${verifycolor}
    call method    ${client}    telephony_presence_status_with_contactlist    &{params}

Tab Check People Recent Event Workgroup with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}    tab_check_ppl_recnt_evnt_wrkgrp    &{params}

Compress Uncompress Dashboard with ${client} and ${option} and ${mode}
    &{params}=    create Dictionary    option=${option}    mode=${mode}
    call method    ${client}    compress_uncompress_dashboard    &{params}

Workgroup Verify Select WrapUp with ${client} and ${wrapUp}
    &{params}=    create Dictionary    wrapUp=${wrapUp}
    call method    ${client}    workgroup_verify_select_wrapUp    &{params}

Verify CompUncmp Workgroup Icon ${client} and ${mode} and ${color}
    &{params}=    create Dictionary    mode=${mode}    color=${color}
    call method    ${client}    verify_compUncmp_workgroup_icon    &{params}

Check Uncheck Routing Slip with ${client} and ${click}
    &{params}=    create Dictionary    click=${click}
    call method    ${client}    check_uncheck_routing_slip    &{params}

Click Verify Routing Slip with ${client} and ${count} and ${is_present} and ${call_type} and ${caller} and ${callee} and ${call} and ${show} and ${hide}
    &{params}=    create Dictionary    count=${count}    is_present=${is_present}    call_type=${call_type}    caller=${caller}    callee=${callee}    call=${call}    show=${show}    hide=${hide}
    call method    ${client}    click_verify_routing_slip    &{params}

Verifying Event Users Available with ${client} and ${user} and ${user_list}
    &{params}=  create Dictionary    user=${user}      user_list={user_list}
    call method     ${client}     Verifying_event_users_avial      &{params}

Create Event with ${client} and ${name} and ${events_select_meeting_type_option} and ${events_meeting_type_add_user_option} and ${username1} and ${username2} and ${events_change_meeting_settings_option} and ${configure_meeting_settings_option} and ${join_audio} and ${send_meeting_request_outlook_option} and ${meeting_name}
    &{params}=    create Dictionary     name=${name}     events_select_meeting_type_option=${events_select_meeting_type_option}     events_meeting_type_add_user_option=${events_meeting_type_add_user_option}     username1=${username1}     username2=${username2}     events_change_meeting_settings_option=${events_change_meeting_settings_option}     configure_meeting_settings_option=${configure_meeting_settings_option}      join_audio=${join_audio}      send_meeting_request_outlook_option=${send_meeting_request_outlook_option}     meeting_name=${meeting_name}
    call method     ${client}    create_event      &{params}

Close Conference Entry with ${client} and ${option}
    &{params}=    create Dictionary    option=${option}
    call method    ${client}    close_conference_entry    &{params}

Add New Label with ${client} and ${label} and ${number} and ${activationType} and ${no_of_rings}
    &{params}=    create Dictionary    label=${label}    number=${number}    activationType=${activationType}    no_of_rings=${no_of_rings}
    call method    ${client}    add_new_label    &{params}

Remove Label with ${client} and ${label_to_remove} and ${label_name}
    &{params}=    create Dictionary    label_to_remove=${label_to_remove}    label_name=${label_name}
    call method    ${client}    remove_label    &{params}

Close Preferences Window with ${client}
    call method    ${client}    close_preferences_window

Check Status Of Call InStack with ${client} and ${verify} and ${callName}
    &{params}=    create Dictionary    verify=${verify}    callName=${callName}
    call method    ${client}    check_status_of_call_inStack    &{params}

Verify Route Slip Third Panel with ${client} and ${caller}
    &{params}=    create Dictionary      caller=${caller}
    call method     ${client}    verify_route_slip_third_panel       &{params}

Edit Modify Label with ${client} and ${label_to_edit} and ${activationType}
    &{params}=    create Dictionary    label_to_edit=${label_to_edit}    activationType=${activationType}
    call method    ${client}    edit_modify_label    &{params}

Share Endo Client Screen with ${client} and ${click_on_screen_share_again} and ${share_option} and ${user_role}
    &{params}=    create Dictionary    click_on_screen_share_again=${click_on_screen_share_again}    share_option=${share_option}     user_role=${user_role}
    call method    ${client}    share_endo_client_screen     &{params}

Permit Share Screen with ${client} and ${click_on_screen_share} and ${first_name} and ${last_name} and ${accept}
    &{params}=    create Dictionary    click_on_screen_share=${click_on_screen_share}    first_name=${first_name}    accept=${accept}   last_name=${last_name}
    call method    ${client}    permit_share_screen    &{params}

Click Away Verify Share Dialog with ${client} and ${user_role}
    &{params}=    create Dictionary      user_role=${user_role}
    call method     ${client}    click_away_verify_share_dialog    &{params}

Accept Screen Share with ${client} and ${join_when} and ${join_how}
    &{params}=    create Dictionary      join_when=${join_when}    join_how=${join_how}
    call method    ${client}    accept_screen_share    &{params}

Verify Screen Share with ${client} and ${option}
    &{params}=    create Dictionary      option=${option}
    call method    ${client}    verify_screen_share    &{params}

Play Pause Close Presenter with ${client} and ${option}
    &{params}=    create Dictionary      option=${option}
    call method    ${client}    play_pause_close_presenter    &{params}

Record Conference with ${client} and ${option}
    &{params}=    create Dictionary      option=${option}
    call method    ${client}    record_conference    &{params}

Click First Ongoing Event with ${client}
    call method    ${client}    click_first_ongoing_event

Play Download Delete Recording with ${client} and ${option}
    &{params}=    create Dictionary      option=${option}
    call method    ${client}    play_download_delete_recording    &{params}

Cancel Event with ${client}
    call method    ${client}    cancel_event

Place Blind Conf Call external with ${client} and ${external} and ${user} 
    &{params}=      create Dictionary        external=${external}        user=${user}
    call method    ${client}           place_blind_conf_call            &{params}
    
Click First User with ${client}
    ${result}=   call method    ${client}    click_first_user 
    [return]      ${result} 

Verify Dial Button Dropdown with ${client} and ${mobile} and ${home}
    &{params}=      create Dictionary        mobile=${mobile}        home=${home}
    call method    ${client}           verify_dial_button_dropdown            &{params}

Verify Contact Card Status And Image with ${client} and ${option} and ${status} and ${image} and ${username}
    &{params}=     create Dictionary       option=${option}        status=${status}        image=${image}         username=${username}
    call method     ${client}     verify_contact_card        &{params}

Verify Contact Pager Info with ${client} and ${status} and ${pager}    
    &{params}=     create Dictionary    status=${status}    pager=${pager}    
    call method     ${client}    verify_contact_info    &{params}  
  
Close Program with ${clientUtils} and ${program}
    &{params}=    create Dictionary    program=${program}
    call method    ${clientUtils}    close_program    &{params}

Uninstall Client with ${clientUtils}
    call method    ${clientUtils}    uninstall_client

Install Client with ${client}
    call method    ${client}    install_client

Install Client Silently with ${clientUtils} and ${version} and ${is_runtype_mt}
	&{params}=    create Dictionary    version=${version}	is_runtype_mt=${is_runtype_mt}
    call method    ${clientUtils}    install_client_silently    &{params}
    
Verify Installation Folder with ${clientUtils} and ${is_runtype_mt}
    &{params}=    create Dictionary    is_runtype_mt=${is_runtype_mt}
    call method    ${clientUtils}    verify_installation_folder    &{params}

Verify Plugins Installation with ${clientUtils}
    call method    ${clientUtils}    verify_client_plugins

Upgrade Client with ${client} and ${username} and ${password} and ${url}
    &{params}=    Create Dictionary    username=${username}    password=${password}    server_address=${url}    
    call method    ${client}    upgrade_client    &{params}

Delete Registry Entry with ${clientUtils}
	call method    ${clientUtils}    delete_registry_entry

Delete Mitel Folder with ${clientUtils}
    call method    ${clientUtils}    delete_mitel_folder

Click Merge Call with ${client} and ${option} and ${merge}    
    &{params}=     create Dictionary    option=${option}    merge=${merge}
    call method     ${client}    click_merge_call    &{params}

Verify ConferenceCall Users Ends Call with ${client} and ${user1} and ${option}
    &{params}=     create Dictionary    user1=${user1}    option=${option}
    call method     ${client}    verify_conferencecall_users_ends_the_call    &{params}

Click First Entry From Recent Tab with ${client} and ${searchItem}
    &{params}=     create Dictionary    searchItem=${searchItem}
    call method     ${client}    click_first_entry_from_recent_tab     &{params}

Check First Recent Call Type with ${client} and ${option}
    &{params}=     create Dictionary    option=${option}
    call method     ${client}    check_first_recent_call_type    &{params}

Third Panel Call Record with ${client} and ${option}
    &{params}=     create Dictionary    option=${option}
    call method     ${client}    thirdpanel_call_record    &{params}

Verify Recent Counter Badge with ${client} and ${badgeNo} and ${tab}
    &{params}=     create Dictionary    badgeNo=${badgeNo}      tab=${tab}
    call method     ${client}    verify_recent_counter_badge     &{params}

Transfer Call Via ContexualMenu with ${client} and ${option}
    &{params}=     create Dictionary    option=${option}
    call method     ${client}    transfer_call_via_contexualMenu    &{params}

verify_holdCall_and_consultCall with ${client} and ${consult_conference_completed} and ${HoldContact} and ${CContact}
    &{params}=     create Dictionary    consult_conference_completed=${consult_conference_completed}    HoldContact=${HoldContact}    CContact=${CContact}
    call method     ${client}    verify_holdCall_and_consultCall     &{params}
    
Get Event with ${client} and ${event_name}
    &{params}=     create Dictionary    event_name=${event_name}        
    ${result}=    call method     ${client}    get_event    &{params}
    [return]      ${result}
    
Join Event By Callme with ${client} and ${option} and ${number} 
    &{params}=     create Dictionary    option=${option}       number=${number}    
    call method     ${client}    join_event_by_callme    &{params}

Get Url with ${client}
    ${result}=    call method     ${client}    get_url    
    [return]      ${result}
    
Launch Url with ${browser} and ${URL}    
    &{params}=     create Dictionary    URL=${URL}        
    call method     ${browser}      launch_url      &{params}
    
Join Exo Event with ${browser} and ${sender}    
    &{params}=     create Dictionary    sender=${sender}        
    call method     ${browser}      join_exo_event      &{params}
    
Close Browser with ${browser}    
    call method     ${browser}      close_browser   

Click On Users For Chat with ${browser} and ${chat_option}
    &{params}=     create Dictionary    chat_option=${chat_option}        
    call method     ${browser}      click_on_users_for_chat      &{params}
    
Send Im Exo with ${browser} and ${message}    
    &{params}=     create Dictionary    message=${message}        
    call method     ${browser}      send_im_exo      &{params}
    
Verify Exo IM with ${browser} and ${verify} and ${ENDOIM}
    &{params}=     create Dictionary    verify=${verify}      ENDOIM=${ENDOIM}       
    call method     ${browser}      verify_Exo_IM      &{params}
    
Share Exo Client Screen with ${browser} and ${share_option} and ${browser_name} and ${event_name} 
    &{params}=     create Dictionary    share_option=${share_option}      browser_name=${browser_name}      event_name=${event_name}     
    call method     ${browser}      share_exo_client_screen      &{params} 
    
Tab Away with ${browser}
    call method     ${browser}      tab_away

Get Event Participant Code with ${client} and ${event_name}       
    &{params}=     create Dictionary    event_name=${event_name}        
    call method     ${browser}      get_event_participant_code      &{params}
    
Verify Events Page with ${client}
    call method     ${client}      verify_events_page
    
Verify Events Avail Upcoming with ${client} and ${entity}
    &{params}=     create Dictionary    entity=${entity}        
    call method     ${client}      verify_events_avail_upcoming      &{params}

Chk Event Creation User with ${client}
    call method     ${client}      chk_event_creation_user    &{EMPTY}

Verify Open Chat Entry with ${client} and ${sender_name1} and ${sender_name2} and ${sender_name3}
    &{params}=     create Dictionary    sender_name1=${sender_name1}   sender_name2=${sender_name2}    sender_name3=${sender_name3}   
    call method     ${client}    verify_open_chat_entry     &{params}
	
Exo Client Communication with ${browser} and ${chat_option} and ${participant}
      &{params}=     create Dictionary    browser=${browser}    chat_option=${chat_option}     participant=${participant}
	  call method     ${browser}     click_on_users_for_chat      &{params}
	  
Create New GroupThreeMembers with ${client} and ${groupName} and ${choice} and ${contact1} and ${contact2} and ${contact3}
    &{params}=    Create Dictionary    groupName=${groupName}    choice=${choice}    contact1=${contact1}    contact2=${contact2}    contact3=${contact3}
    call method    ${client}    create_new_group    &{params}

Open Chat Entry with ${client} and ${sender_name1} and ${sender_name2}
    &{params}=     create Dictionary    sender_name1=${sender_name1}   sender_name2=${sender_name2}   
    call method     ${client}    verify_open_chat_entry     &{params}
	
Remove Converation from IM with ${client} and ${search_im_entry_by} and ${sender_name1} and ${sender_name2}
    &{params}=     create Dictionary    search_im_entry_by=${search_im_entry_by}    sender_name1=${sender_name1}   sender_name2=${sender_name2}     
    call method     ${client}    remove_im_conversation     &{params}

Add Or Remove Select Number In Findme Panel with ${client} and ${labelName} and ${number}
    &{params}=     create Dictionary    labelName=${labelName}   number=${number}
    call method    ${client}    add_or_remove_select_number_in_findme_panel    &{params}

Check Ring My Findme Numbers with ${client}
    call method    ${client}    check_ring_my_findme_numbers

Save Call Routing Setting with ${client}
    call method    ${client}    save_call_routing_setting

Get Badge Count with ${client} and ${tabName}
    &{params}=    create Dictionary    tabName=${tabName}
    ${result}=    call method    ${client}    get_badge_count    &{params}
    [return]      ${result}

Search People By First Name with ${client} and ${searchItem} and ${lastName}
    &{params}=    Create Dictionary    searchItem=${searchItem}    lastName=${lastName}    
    call method    ${client}    search_people_withfirstname_clickUser    &{params}
	
Remove Conversation from Message with ${client} and ${search_im_entry_by} and ${message}
    &{params}=    create Dictionary    search_im_entry_by=${search_im_entry_by}    message=${message}
    call method    ${client}    remove_conversation     &{params}

Check User Detail Attribute1 with ${client} and ${option} and ${check} and ${username} and ${extn}
    &{params}=    Create Dictionary    option=${option}    check=${check}    username=${username}    extn=${extn}
    call method    ${client}    check_user_detail_attribute    &{params}

Verify Info Calls Meassge VM Tabs with ${client}
    call method     ${client}    verify_info_calls_messages_vmtab

Verify Avatar with ${client} and ${fname} and ${lname}
	&{params}=    Create Dictionary      fname=${fname}     lname=${lname}
    call method      ${client}    verify_avatar  &{params}	
    call method      ${client}    verify_avatar  &{params}
	
Mouse Hover for Phone Type with ${client} and ${phone_type}
    &{params}=  create Dictionary    phone_type=${phone_type}
    call method    {client}    mouse_hover_phone_type    &{params}

Click Dropdown Send Intercom with ${client} and ${check}
    &{params}=     create Dictionary    check=${check}        
    call method     ${client}    click_Dropdown_send_Intercom    &{params}

Play Unread Voicemails Via Computer Speaker with ${client}
    call method    ${client}    play_unread_voicemails_via_computer_speaker

People Sort Icon with ${client}
    call method    ${client}    people_sort_icon
	
Verify User Sorted Lastcontact with ${client} and ${peopleName}
    &{params}=     create Dictionary    peopleName=${peopleName}
    call method    ${client}    verify_user_sorted_lastcontact    &{params}

Primary Phone Assignment with ${client} and ${name} and ${number}
    &{params}=    create Dictionary    name=${name}    number=${number}
    call method    ${client}    Primary_phone_assignment    &{params}  

Join External Conference with ${client} and ${number}  
    &{params}=    create Dictionary    number=${number}
    call method    ${client}    Join_external_conference    &{params}

Verify Mouse Over Canned Im with ${client} and ${check} and ${option}
    &{params}=    create Dictionary    check=${check}    option=${option}
    call method    ${client}   mouse_hover_canned_im    &{params}

Search List IM Presence People Extension with ${client} and ${searchitem}
    &{params}=    Create Dictionary    searchItem=${searchitem}
	call method    ${client}    search_list_IM_presence_people_extension    &{params}
		
Verify Im Presence Avatar From SearchList with ${client} and ${username1} and ${username2}
	&{params}=    Create Dictionary    username1=${username1}    username2=${username2}
    call method    ${client}    verify_Im_presence_Avatar_from_SearchList    &{params}
	
Verify Contact Card On Call with ${client} and ${option} and ${username}
    &{params}=     create Dictionary    option=${option}    username=${username}
    call method     ${client}    verify_contact_card_on_call    &{params}

Click Vm Forward with ${client} ${subject}
    &{params}=    create Dictionary    subject=${subject}
    call method    ${client}    click_vm_forward     &{params}
 
Add Contact Vm Conversation Second Panel with ${client} and ${name}
    &{params}=    create Dictionary    name=${name}
    call method  ${client}    add_contact_vm_conversation_second_panel    &{params}
 
Record Vm Reply Second Panel with ${client} and ${recording_device}
    &{params}=    create Dictionary    recording_device=${recording_device}
    call method  ${client}    record_vm_reply_second_panel     &{params}

Verify Users Telephony Presence with ${client} and ${color} and ${status}    
    &{params}=    Create Dictionary		color=${color}    status=${status}       
    call method    ${client}    verify_users_telephony_presence    &{params}
	
Verify Users Availabilty Status with ${client} and ${status}
	&{params}=    create Dictionary    status=${status}
	call method		${client}    verify_users_availabilty_status    &{params}

Connect Always On Top with ${client} 
    call method    ${client}    click_always_on_top
	
Open Notepad with ${client} 
    call method    ${client}    open_notepad
  
Close Notepad with ${client} 
    call method    ${client}    close_notepad_new

Dial in conference using access code with ${client}
    ${result}=    call method     ${client}    get_conference_dial_in    
    [return]      ${result}

Click Verify Any Cannedresponse Incall with ${client}
    call method      ${client}    Click_verify_any_cannedresponse_incall 
	
Check Incoming Call CannedIMarrow with ${client}
    call method    ${client}    check_incoming_call_verify_CannedIMarrow

Send Client Log with ${client} 
    call method     ${client}    send_client_log
	
Unzip Log File with ${client} and ${extension}
    &{params}=    Create Dictionary    extension=${extension}
    call method    ${client}    unzip_log_file    &{params}

Add New Number with ${client}
    call method    ${client}    add_new_number