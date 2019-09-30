*** Variables ***
${message}     Extension is a required field. Please select an extension
#################################################
#Pickup Group
#Keys: pickupgpname, PGExtn, extnlistname, pickuploc
&{Pickupgroup_Add}	 pickupgpname=Boss_Pickup_{rand_str}    PGExtn=''
&{Pickupgroup2_Add}	 pickupgpname=Boss_Pickup2_{rand_str}    PGExtn=''
&{Pickupgroupwithoutlocation}	 PGExtn=''     extnlistname=Boss_ExtnList_01
&{Pickupgroup_edit}
&{Pickupgroup}	 pickupgpname=Boss_Pickup_{rand_str}    PGExtn=''     extnlistname=Boss_ExtnList_01     pickuploc=AutoTest_location_avospYbb
&{PickupgroupPM}	 pickupgpname=Boss_Pickup_{rand_str}    PGExtn=''     extnlistname=Boss_ExtnList_01     pickuploc=AutoTest_location_avospYbb

#########################################
#Paging Group
&{PagingGroup}    Pg_Name=Boss_Paging_{rand_str}     Pg_Location=random
&{PagingGroupPM}    Pg_Name=Boss_Paging_{rand_str}     Pg_Location=random

&{Paginggroupedit}	 Pg_Name=Edited_Boss_Paging_{rand_str}    extnlistname=Boss_ExtnList_01    Pg_Extension=''   sync_delay=    mode=   Remove_Extn=     Remove_Name=   Remove_Location=    Make_extn_private=     No_Ans_Rings=    Include_in_sys_dir=     Pg_Location=
&{Paginggroupedit_DM}	 Pg_Name=Edit_Paging_DM_{rand_str}    extnlistname=Boss_ExtnList_01     Pg_Location=random     extn_list=
&{Paginggroupedit_PM}	 Pg_Name=Edit_Paging_PM_{rand_str}    extnlistname=Boss_ExtnList_01     Pg_Location=random     extn_list=

###########################################
#Extention List
&{Extensionlist01}	 extnlistname=Boss_ExtnList_01_{rand_str}
&{Extensionlist02}	 extnlistname=Boss_ExtnList_02_{rand_str}
&{Extensionlist_staff}	 extnlistname=Boss_ExtnList_staff_{rand_str}
&{EditExtensionlist01}	 extnlistname=Boss_ExtnList_{rand_str}
&{EditExtensionlist}	 extnlistname=
&{DMUserProfile}    au_firstname=auto_test_dm_{rand_str}   au_lastname=Auto    au_businessmail=boss_auto_dm_{rand_str}@shoretel.com     au_username=boss_auto_dm_{rand_str}@shoretel.com    au_password=Shoretel1$     au_confirmpassword=Shoretel1$       ap_phonetype=Connect CLOUD Advanced     ap_phonenumber=random    ap_activationdate=today    hw_addhwphone=False    hw_type=Sale New    hw_model=ShoreTel IP420g - Sale     hw_power=False    hw_power_type=ShoreTel IP Phones Power Supply - Sale    role=Decision Maker
&{DMUserProfile1}    au_firstname=newauto_test_dm_{rand_str}   au_lastname=Auto    au_businessmail=newboss_auto_dm_{rand_str}@shoretel.com     au_username=newboss_auto_dm_{rand_str}@shoretel.com    au_password=Shoretel1$     au_confirmpassword=Shoretel1$       ap_phonetype=Connect CLOUD Advanced     ap_phonenumber=random    ap_activationdate=today    hw_addhwphone=False    hw_type=Sale New    hw_model=ShoreTel IP420g - Sale     hw_power=False    hw_power_type=ShoreTel IP Phones Power Supply - Sale    role=Decision Maker

#############################################
#CustomeSchedule

&{CustomSchedule01}	 customScheduleName=DM_Custom_01_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_01    customDate=07/25/2017    startTime=01:00 AM    stopTime=11:00 PM
&{CustomSchedule02}	 customScheduleName=PM_Custom_01_{rand_str}    timeZone=Eastern Standard Time    customName=Custom_02    customDate=07/25/2017    startTime=09:00 AM    stopTime=06:00 PM
&{CustomSchedule03}	 customScheduleName=DM_Custom_03_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_03    customDate=07/25/2017    startTime=01:00 AM    stopTime=11:00 PM
&{CustomSchedule04}	 customScheduleName=   timeZone=Pacific Standard Time      customName=Custom_03    customDate=07/25/2017    startTime=01:00 AM    stopTime=11:00 PM
&{CustomSchedule05}	 customScheduleName=DM_Custom_04_{rand_str}    timeZone=      customName=Custom_03    customDate=07/25/2017    startTime=01:00 AM    stopTime=11:00 PM
&{CustomSchedule06}	 customScheduleName=DM_Custom_05_{rand_str}    timeZone=      customName=Custom_03    customDate=07/25/2017    startTime=01:00 AM    stopTime=11:00 PM
&{CustomSchedule_staff}	 customScheduleName=staff_Custom_01_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_01    customDate=07/25/2017    startTime=01:00 AM    stopTime=11:00 PM

&{EditCustomSchedule04}	 customScheduleName=Edit_PM_Custom_01_{rand_str}    timeZone=Pacific Standard Time    customName=Custom_02    customDate=9/30/2017   startTime=09:00 AM    stopTime=06:00 PM
&{EditCustomSchedule03}	 customScheduleName=Edit_DM_Custom_01_{rand_str}    timeZone=Eastern Standard Time      customName=Custom_01    customDate=9/30/2017    startTime=01:00 AM    stopTime=11:00 PM
&{EditCustomSchedule01}	 customScheduleName=Edit_DM_Custom_01_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_01    customDate=07/25/2017    startTime=02:00 AM     stopTime=03:00 PM    deletevcfeday=
&{EditCustomSchedule02}	 customScheduleName=Edit_PM_Custom_01_{rand_str}    timeZone=Eastern Standard Time    customName=Custom_02    customDate=07/25/2017   startTime=10:00 AM    stopTime=07:00 PM       deletevcfeday=
&{EditCustomSchedule05}	 customScheduleName=Edit_DM_Custom_01_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_01    customDate=07/25/2017    startTime=02:00 AM    stopTime=02:00 AM
&{EditCustomSchedule06}	 customScheduleName=Edit_PM_Custom_01_{rand_str}    timeZone=Eastern Standard Time    customName=Custom_02    customDate=07/25/2017   startTime=10:00 AM    stopTime=10:00 AM

&{CopyCustomSchedule_staff}	 customScheduleName=Copy_staff_Custom_01_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_01    customDate=09/30/2017    startTime=02:00 AM    stopTime=10:00 PM
&{CopyCustomSchedule01}	 customScheduleName=Copy_DM_Custom_01_{rand_str}    timeZone=Pacific Standard Time      customName=Custom_01    customDate=09/30/2017   startTime=02:00 AM     stopTime=03:00 PM
&{CopyCustomSchedule02}	 customScheduleName=Copy_PM_Custom_01_{rand_str}    timeZone=Eastern Standard Time    customName=Custom_02    customDate=09/30/2017    startTime=10:00 AM    stopTime=07:00 PM

#######################################################################
#Auto Attendant
&{EditAA01}    customScheduleName=DM_Custom_01_{rand_str}
&{EditAA02}    Location=Testloc_{rand_str}
&{EditAA03}    customScheduleName=     Location=    Aa_Name=    MDT=    Aa_Extn=     prompt=    neg=True
&{EditAA04}    Assign_vcfe_component=     Assign_vcfe_Name=     Location=    Aa_Name=    MDT=    Aa_Extn=     prompt=   verify_interactive_diagram=     neg=False   filePath=${EXECDIR}${/}Test_files${/}AA-audio.wav  Remove_Operations=  Monitor=    Multiple_Digit_Operation=   MDO_Extension=   Adjust_Timeout=
&{EditAA05}    vcfe_name=       Validate_vcfe_name=     neg=False
&{AA_staff}    Aa_Name=AA_staff_{rand_str}
&{AA_DM}    Aa_Name=AA_DM_{rand_str}
&{AA_PM}    Aa_Name=AA_PM_{rand_str}

###################################################
#On-Hours Schedule
&{OnHoursSchedule01}   scheduleName=VCFE_OHS_01_{rand_str} 	timezone=Pacific Standard Time
&{OnHoursSchedule02}   scheduleName=VCFE_OHS_02_{rand_str}     timezone=Pacific Standard Time
&{OnHoursSchedule03}   scheduleName=VCFE_OHS_03_{rand_str}     timezone=Pacific Standard Time

&{EditOnHoursSchedule01}    timezone=Central Pacific Standard Time
&{EditOnHoursSchedule02}    scheduleName=Edit_VCFE_OHS_{rand_str}
&{EditOnHoursSchedule03}    scheduleName=Edit_VCFE_OHS_{rand_str}   timePeriod=change   StartTime=9:00 AM       StopTime=6:00 PM
&{EditOnHoursSchedule04}    scheduleName=Remove
&{EditOnHoursSchedule05}    scheduleName=Edit_VCFE_OHS_{rand_str}   timePeriod=change   StartTime=9:00 AM       StopTime=9:00 AM

&{CopyOnHoursSchedule01}    scheduleName=Copy_VCFE_OHS_{rand_str}   timezone=Central Pacific Standard Time

#############################################
#HuntGroup
#Keys: HGname, HGBckupExtn
&{HuntgroupStaff}    HGname=HG_staff_{rand_str}    HGBckupExtn=8900
&{HuntgroupStaff2}    HGname=HG_staff2_{rand_str}    HGBckupExtn=8900
&{HuntgroupDM}    HGname=HG_DM_{rand_str}    HGBckupExtn=8900
&{HuntgroupDM2}    HGname=HG_DM2_{rand_str}    HGBckupExtn=8900
&{HuntgroupPM}    HGname=HG_PM_{rand_str}    HGBckupExtn=8900
&{HuntgroupPM2}    HGname=HG_PM2_{rand_str}    HGBckupExtn=8900
&{HuntgroupEdit}   HGname=    HGBckupExtn=    Off_hours_or_holiday_destination=    no_answer=    Make_extension_private=    On_hours_schedule=    Holiday_schedule=    call_stack_full=    Skip_member_if_already_on_a_call=    Call_member_when_forwarding_all_calls=    Rings_per_Member=    No_answer_number_of_rings=    Distribution_pattern=

#############################################

#Emergency HuntGroup
#Keys: Location, Country, Address01, city, state, Zip
&{geolocation_US}     Location=Testloc_{rand_str}    Country=United States   Address01=1385 Broadway  city=New York  state=New York  Zip=10018
&{EmergencyHG}
&{EmergencyHuntGroup1}     Location=Auto_hg_loc_{rand_str}    Country=United States   Address01=1385 Broadway  city=New York  state=New York  Zip=10018
&{EmergencyHuntGroup2}      Location=   Extn=
&{EmergencyHG_Edit2}    grp_member=     Distribution_pattern=   up_down_grp_member=1000     verify_up_down_button=
&{EmergencyHG_Edit}     grp_member=     Distribution_pattern=

#############################################
#Holidays Schedule
#Keys: scheduleName, timeZone, holidayName, date
&{HolidayScheduleStaff}	 scheduleName=Staff_Holiday_{rand_str}    timeZone=India Standard Time    holidayName=Holiday_01    date=11/24/2017    error_msg=
&{HolidayScheduleStaff2}	 scheduleName=Staff2_Holiday_{rand_str}
&{HolidayScheduleDM}	 scheduleName=DM_Holiday_{rand_str}    timeZone=India Standard Time    holidayName=Holiday_01    date=11/24/2017    error_msg=
&{HolidayScheduleDM2}	 scheduleName=DM2_Holiday_{rand_str}
&{HolidaySchedulePM}	 scheduleName=PM_Holiday_{rand_str}    timeZone=India Standard Time    holidayName=Holiday_02    date=11/24/2017    error_msg=
&{HolidaySchedulePM2}	 scheduleName=PM2_Holiday_{rand_str}
&{HolidayScheduleEdit}	 scheduleName=    timeZone=    holidayName=    date=
&{HolidaySchedule01}	scheduleName=VCFE_HS_{rand_str} 	timeZone=India Standard Time	holidayName=Holiday1	date=10/24/2017
&{HolidaySchedule02}	scheduleName=VCFE_HS2_{rand_str} 	timeZone=India Standard Time	holidayName=Holiday2	date=10/24/2017

&{CopyHolidayScheduleStaff}	 scheduleName=Copy_staff_Holiday_{rand_str}    timeZone=India Standard Time    holidayName=Holiday_02    date=12/14/2017    error_msg=
&{CopyHolidayScheduleDM}	 scheduleName=Copy_DM_Holiday_{rand_str}    timeZone=India Standard Time    holidayName=Holiday_02    date=12/14/2017    error_msg=
&{CopyHolidaySchedulePM}	 scheduleName=Copy_PM_Holiday_{rand_str}    timeZone=India Standard Time    holidayName=Holiday_01    date=12/14/2017    error_msg=