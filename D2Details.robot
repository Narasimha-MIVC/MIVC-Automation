*** Variables ***
${D2DetailsFileName}       D2Details.robot

#D2 Portal details
${URL}                    http://10.211.44.90:5478/director/login
${BROWSER}                chrome
${D2IP}                         10.211.44.90
${D2User}                       admin
${D2Password}                   changeme
${build}						22.10.2600.0

#D2 Appliances Info
${HQ}                   WinHQ
${LDVS}                 LinuxDVS
${WINDVS}               WinDVS
${PSwitch}              vPhone
${UCBConf}              vCollab
#${UCBIm}                vCollab
#${TSwitch}              vTrunk

#D2 Appliances IP Info
@{HQIP}                   10.211.44.90
@{LDVSIP}                 10.211.44.92        
@{PSwitchIP}              10.211.44.63
#@{TSwitchIP}              192.168.101.37
#@{UCBImIP}                192.168.101.46
@{UCBConfIP}              10.211.44.65
@{WINDVSIP}               10.211.44.91

#D2 Appliances DNS Name Info
${HQ_Name}				Headquarters
${Site_Name}            Headquarters
@{LDVS_Name}            LDVS-SERVER       
@{PSwitch_Name}         HQ-vPhone        
#@{TSwitch_Name}         mt1ptavtks01qav
#@{UCBIm_Name}           mt1ptaimsv02qav
@{UCBConf_Name}         vUCb

#DID Ranges Page
${trunkgrpName}           ATF1_Temp
${basephno}               +1 (308) 600-8000
${noofphones}             10
${destinationdn}          4700


#D2 Appliances Status
${InService}           In Service
@{passStatus}          In Service     IP Phones Out of Service     FTP booted
@{failStatus}          Lost Communication   Unknown

#D2 Voicemail Info
${mailbox_count}	0
${vm_messages}      0

#D2 Trunk Group Info
${AnalogLoopStart}		Analog Loop Start
${AutomationTrunk}		Automation_trunk
${DigitalLoopStart}		Digital Loop Start
${Sky-Connect}			Sky-Connect SIP-Tie

${AnalogLoopStartType}	  Analog Loop Start
${AutomationTrunkType}	  SIP
${DigitalLoopStartType}	  Digital Loop Start
${Sky-ConnectType}		  SIP

${AnalogLoopStartInUse}		0
${AutomationTrunkInUse}		0
${DigitalLoopStartInUse}	0
${Sky-ConnectInUse}			0

${AnalogLoopStartInService}		0
${AutomationTrunkInService}		0
${DigitalLoopStartInService}	0
${Sky-ConnectInService}			0

#Trunk Group Details
&{Trunk01}	trunk_name=Analog Loop Start	    trunk_type=Analog Loop Start	    trunk_in_use=0 	 trunk_in_service=0
&{Trunk02}	trunk_name=Digital Loop Start		trunk_type=Digital Loop Start		trunk_in_use=0	 trunk_in_service=0
&{Trunk03}	trunk_name=Sky-Connect SIP-Tie	    trunk_type=SIP					    trunk_in_use=0	 trunk_in_service=0

&{MakeMeConf1}	active_calls=0	 in_use_ports=0		free_ports=12
