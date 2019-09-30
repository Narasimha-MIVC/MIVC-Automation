Login_Info = {
    'url': None,
    'username': None,
    'password': None,
    'NewTab': False,
    'TabName': 'main_page',
    'windows_handles': {}
}

On_Site_User_Info = {
    "SelectAll": False,
    "Users": [],
    "Req_By": None,
    "Req_Src": None
}

On_Site_Fax_Info = {
    "SelectAll": False,
    "Users": [],
    "FaxNumberSelectAll": False,
    "FaxNumbers": [],
    "Req_By": None,
    "Req_Src": None
}

Location_US = {
    "locationName": "Hybrid_Loc_{rand_str}",
    "country": "United States",
    "Address1": "1385 Broadway",
    "city": "New York",
    "state": "New York",
    "zip": "10018"
}

Location_AUS = {
    "locationName": "Hybrid_Loc_{rand_str}",
    "country": "Australia",
    "streetNo": "441",
    "streetName": "st kilda",
    "streetType": "Road",
    "city": "Melbourne",
    "state": "Victoria",
    "zip": "3004"
}

emergency_reg = {
    "locfirstName": "Tracy",
    "loclastName": "Victor",
    "phoneNumber": "+61224220250"
}

New_Account = {
    "accountType": "Test",
    "accountName": "Hybrid_Account_{rand_str}",
    "firstName": "DM",
    "lastName": "User",
    "email": "Hybrid_Mail_{rand_str}@shoretel.com",
    "password": "Abc123!!",
    "confirmPassword": "Abc123!!",
    "location": None,
    "emergencyReg": None,
    "no_validation": True,
    "areaCode": None,
    "currency": None,
    "create_partition_flag": True,
    "clusterInstance": "AUS",
    "timezone": "AUS Central Standard Time"
}


# --BEGIN--
def get_variables(**params):
    country = params.get('country', 'AUS')
    if country == 'US':
        New_Account.update({'location': Location_US})
    elif country == 'AUS':
        New_Account.update({'location': Location_AUS,
                            'emergencyReg': emergency_reg})
    else:
        pass
    variables = {
        'Hybrid_Account': New_Account,
        'Login_Info': Login_Info,
        'On_Site_User_Info': On_Site_User_Info,
        'On_Site_Fax_Info': On_Site_Fax_Info
    }
    return variables
# --End of "get_variables()"--