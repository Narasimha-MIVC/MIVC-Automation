geoLocation_US = {
    'Location': 'LocationBca1',
    'Country': 'United States',
    'Country_abbreviation': 'US',
    'Address01': '474 Boston Post Road',
    'Address02': '',
    'city': 'North Windham',
    'state': 'Connecticut',
    'state_abbreviation': 'CT',
    'Zip': '06256',
    'by_pass': 'True'
}

geoLocation_AUS = {
    'Location': 'LocationBca1',
    'Country': 'Australia',
    'Country_abbreviation': 'AUS',
    'streetNo': '441',
    'streetName': 'st kilda',
    'streetType': 'Road',
    'City': 'Melbourne',
    'state': 'Victoria',
    'state_abbreviation': 'VIC',
    'postcode': '3004',
    'firstName': 'Tracy',
    'lastName': 'Victor',
    'phoneNumber': '+61224220250',
    'timeZone': 'AUS Eastern Standard Time',
    'areaCode': '2',
    'by_pass': 'True'
}

geoLocation_UK = {
    'Location': 'LocationBca1',
    'Country': 'United Kingdom',
    'Country_abbreviation': 'UK',
    'buildingName': 'Inspired',
    'streetName': 'Easthampstead Road',
    'postalTown': 'Bracknell',
    'Postcode': 'RG12 1YQ',
    'timeZone': 'GMT Standard Time',
    'areaCode': '28',
    'state': None,
    'by_pass': 'True'
}

connect_archiving = {
    'add_on_feature': 'Connect Archiving',
    'Option': 'MiCloud Connect IM Archive',
    'Location': None,
    'RequestedBy': None,
    'RequestSource': 'Case',
    'CaseNumber': '1234',
    'ReturnSuccessIfNoRowSelected': True,
}

Connect_Call_Recording = {
    'add_on_feature': 'Connect Call Recording',
    'Option': 'MiCloud Connect IM Archive',
    'RequestedBy': None,
    'RequestSource': 'Case',
    'CaseNumber': '1234',
    'ReturnSuccessIfNoRowSelected': True
}

m5db_connect_info = {
    'hostname': '10.197.145.189',
    'port': 1433,
    'username': 'M5Portal',
    'password': '1234',
    'dbname': 'm5db',
    'db_type': 'mssql',
}

d2db_connect_info = {
    'hostname': '10.197.145.186',
    'port': 4308,
    'username': 'shoreadmin',
    'password': 'passwordshoreadmin',
    'dbname': 'shoreware',
    'db_type': 'mysql',
}

ucdb_connect_info = {
    'hostname': '10.197.145.234',
    'port': 18086,
    'username': 'default',
    'password': '1234',
    'dbname': 'ses',
    'db_type': 'postgres',
}

uc_url = {
    'username': 'default',
    'password': '1234',
    'ip': '10.197.145.234',
    'version': 'v2',
    'condition': None
}

uc_tds_tbl_tenants_url = {
    'port': '18087',
    'table': 'tenants'
}

uc_idms_tbl_users_url = {
    'port': '18085',
    'table': 'users'
}

uc_ses_tbl_services_url = {
    'port': '18086',
    'table': 'services'
}

uc_loc_tbl_locations_url = {
    'port': '18089',
    'table': 'locations'
}
uc_back_sync_details = {
    'port': '3002',
    'api_name':  'ReliableEventData',
    'api_type':  'Events'
}
uc_vm_login_details = {
    'ip': '10.197.145.234',
    'user_name': 'root',
    'password': 'Shoreadmin1#'
}


def update_url():
    uc_tds_tbl_tenants_url.update(uc_url)
    uc_idms_tbl_users_url.update(uc_url)
    uc_ses_tbl_services_url.update(uc_url)
    uc_loc_tbl_locations_url.update(uc_url)
    uc_back_sync_details.update(uc_url)


event_propagator_container_id = "eventpropagatorapi"
tds_cont_id = "tds"
idms_cont_id = "idms"
ses_cont_id = "ses"
loc_cont_id = "loc"

# --BEGIN--
def get_variables(**params):
    update_url()
    variables = {
        'ADD_ON_FEATURE': connect_archiving,
        'ADD_ON_FEATURE_2': Connect_Call_Recording,
        'M5DB_CONN_INFO': m5db_connect_info,
        'D2DB_CONN_INFO': d2db_connect_info,
        'UCDB_CONN_INFO': ucdb_connect_info,
        'UC_TDS_TBL_TENANTS_URL': uc_tds_tbl_tenants_url,
        'UC_IDMS_TBL_USERS_URL': uc_idms_tbl_users_url,
        'UC_SES_TBL_SERVICES_URL': uc_ses_tbl_services_url,
        'UC_LOC_TBL_LOCATIONS_URL': uc_loc_tbl_locations_url,
        'UC_VM_LOGIN': uc_vm_login_details,
        'GEO_LOC_US': geoLocation_US,
        'GEO_LOC_AUS': geoLocation_AUS,
        'GEO_LOC_UK': geoLocation_UK,
        'UC_BACK_SYNC_SERVICES_URL': uc_back_sync_details,
        'EVENT_PROP_CONTAINER_ID': event_propagator_container_id,
        'TDS_CONTAINER_ID': tds_cont_id,
        'IDMS_CONTAINER_ID': idms_cont_id,
        'SES_CONTAINER_ID': ses_cont_id,
        'LOC_CONTAINER_ID': loc_cont_id,
    }

    return variables
# --End of "get_variables()"--
