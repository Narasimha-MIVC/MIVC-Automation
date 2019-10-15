"""
Variables for the BCA feature testing
"""

bca_info = {
    'ProfileName': 'TestNew',
    'Extension': None,         # 4800
    'Location': 'LocationBca1',
    'AssignFromLocation': 'Choose from all locations',
    'VerifyGlobalNo': False,
    'SelectPhoneNumber': None,    # US number - 1 (860) 459-4800, UK - , AUS -
    'OutboundCallerID': "Default",  # if the default outbound caller id is intended
    'OtherSettings': False,
    'Privacy': True,
    'CallForwardBusy': '8 calls',
    'CallForwardBusyExtn': None,
    'CallForwardNoAnswer': '4 rings',
    'CallForwardNoAnswerExtn': None,
    'ConferencingOptions': 'Disable Conferencing',
    'EnableToneWhenPartiesJoinOrLeave': False,
    'AssociatedBCA': False,
    'AssociatedBCAExtn': None,
    'AssociatedBCAProfile': None,
    'BcaCopyProfileName': 'BcaCopy',
    # Start -for creating/ managing Shared Call Appearance
    'ScaUserName': None,
    'ScaEnableFlag': 'Disabled',     # To create SCA on phone settings page
    'ScaExtn': None,
    'ScaSaveOrCancel': 'submit',
    # End - Shared Call Appearance
    # Start -will be used for selecting/ creating BCA on user--> program buttons page
    'BcaUserName': None,
    'CreateBcaUsingProgButton': None,
    'VerifyRadioButton': None,
    'SelectType': None,
    'SelectFunction': None,
    'SelectLongLabel': None,
    'SelectShortLabel': None,
    'SelectBCA': None,
    'SelectCallStackPosition': None,
    'SelectDelayBeforeAudiblyRing': None,
    'SelectShowCallerIDAlert': None,
    'SelectAutoAnswer': None,
    'SelectNoconnectedcallactionAnswerOnly': None,
    'SelectNoconnectedcallactionDialTone': None,
    'SelectNoconnectedcallactionDialExtn': None,
    'SelectNoconnectedcallactionDialExtnInput': None,
    'SelectNoconnectedcallactionDialExtnSearch': None,
    'SelectNoconnectedcallactionDialExternal': None,
    'SelectNoconnectedcallactionDialExternalInput': None,
    'SelectBcaSaveButton': True,
    'SelectBcaResetButton': False,
    # End --- BCA on Programming button page
    # Start --- Editing the phone number on phone numbers page
    'auto_Attendant': None,
    'hunt_Group': None,
    'HGname': None,
    'Aa_Name': None,
    'bridged_Call_Appearance_name': None,
    'User': None,
    'Unassign': None
    # End --- Editing the phone number on phone numbers page
}

phoneNumber_US = {
    'numberRange': '18604594800',
    'range': '20',
    'serviceUsage': 'Telephone Number Turnup',
    'tn_type': 'client',
    'clientAccount': None,
    'clientLocation': None,
    'vendor': '212803-dash',
    'vendorOrderNumber': '4321',
    'requestedBy': 'Auto User2',
    'requestSource': 'Email',
    'state': 'Available'
}

geoLocation_US = {
    'Location': 'LocationBca1',
    'Country': 'United States',
    'Address01': '474 Boston Post Road',
    'Address02': '',
    'city': 'North Windham',
    'state': 'Connecticut',
    'Zip': '06256',
    'by_pass': False
}


# --BEGIN--
def get_variables(**params):
    location = params.get('country', 'US')
    if location == 'US':
        phone_info = phoneNumber_US
        geo_loc = geoLocation_US
    elif location == 'UK':
        pass
    else:
        pass
    variables = {
        'BCA_INFO': bca_info,
        'PHONE_INFO': phone_info,
        'GEO_LOC': geo_loc
    }
    return variables
# --End of "get_variables()"--




# &{geolocation_US}     Location=Testloc_{rand_str}    Country=United States   Address01=1385 Broadway  city=New York  state=New York  Zip=10018
# &{geolocation_close_US}     Location=Testloc_to_close_{rand_str}    Country=United States   Address01=300 State Street    Address02=Rochester, NY 14614, USA    city=Rochester    state=New York    Zip=14614    by_pass=True
# &{geolocation_AUS}    Location=Testloc_{rand_str}     Country=Australia     streetNo=441    streetName=st kilda    streetType=Road    City=Melbourne    state=Victoria    postcode=3004    firstName=Tracy    lastName=Victor    phoneNumber=+61224220250    timeZone=AUS Eastern Standard Time    areaCode=2
# &{geolocation_close_AUS}    Location=Testloc_to_close_{rand_str}    Country=Australia     streetNo=441    streetName=st kilda   streetType=Road    City=Melbourne    state=Victoria    postcode=3004    firstName=Tracy    lastName=Victor    phoneNumber=+61224220250    timeZone=AUS Eastern Standard Time    areaCode=2
# &{geolocation_UK}    Location=Testloc_{rand_str}    Country=United Kingdom    buildingName=Inspired    streetName=Easthampstead Road    postalTown=Bracknell    Postcode=RG12 1YQ    timeZone=GMT Standard Time    areaCode=28
# &{geolocation_close_UK}    Location=Testloc_to_close_{rand_str}    Country=United Kingdom    buildingName=Inspired    streetName=Easthampstead Road    postalTown=Bracknell    Postcode=RG12 1YQ    timeZone=GMT Standard Time    areaCode=28
# &{geolocation01}     Location=Testloc_{rand_str}    Country=United States   Address01=1385 Broadway  city=New York  state=New York  Zip=10018
