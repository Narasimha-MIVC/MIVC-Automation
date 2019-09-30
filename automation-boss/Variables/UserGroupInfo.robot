*** Variables ***
#################################################
#User Group
#Keys: userGroupName, profileType, holdMusic, directedIntercom, whisperPage, Barge, silentMonitor, classOfService, accountCodeMode
&{Usergroup_staff}	 userGroupName=SystemUserGrop_DM_{rand_str}    profileType=Managed    holdMusic=Default Music    directedIntercom=InitiateAndReceive    whisperPage=InitiateAndReceive    Barge=InitiateAndReceive    silentMonitor=InitiateAndReceive    classOfService=International    accountCodeMode=Required
&{UsergroupDM}	 userGroupName=SystemUserGrop_DM_{rand_str}    profileType=Managed    holdMusic=Default Music    directedIntercom=InitiateAndReceive    whisperPage=InitiateAndReceive    Barge=InitiateAndReceive    silentMonitor=InitiateAndReceive    classOfService=International    accountCodeMode=Required
&{UsergroupPM}	 userGroupName=SystemUserGrop_PM_{rand_str}    profileType=Managed    holdMusic=Default Music    directedIntercom=InitiateAndReceive    whisperPage=InitiateAndReceive    Barge=InitiateAndReceive    silentMonitor=InitiateAndReceive    classOfService=International    accountCodeMode=Required
&{Usergroup_edit}	 userGroupName=System Managed Worker Group