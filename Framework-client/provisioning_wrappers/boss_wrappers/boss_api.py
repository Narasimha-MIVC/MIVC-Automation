__author__ = "nkumar@soretel.com"

import sys, requests, os, logging, datetime, ast, time, re
import xml.etree.ElementTree as ET
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))
from utils.decorators import func_logger
from vcfe import Vcfe
from get_details import GetDetails
log = logging.getLogger("boss_api")

class parse_xml(object):
    '''
    This class carries the responsibility to parse the params from the config xml file. All the optional params required to call a
    api are placed in the xml based config file.
    '''

    def __init__(self, filename):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()

    @func_logger
    def getparams(self, api_name):
        '''
        This function will create the list of params for the api call. The format is mentioned below.
        :param api_name: the name of the api
        :return: dict of param in the format {"val1":"abc",
                                                "val2":"def",
                                                    "val3":"ghi"}
        '''
        d = {}
        for api in self.root:
            if api.attrib['name'] == api_name:
                for p in api[0]:
                    if p.attrib.get("dt") == 'int':
                        d[p.tag] = int(p.text)
                    if p.attrib.get("dt") == 'None':
                        d[p.tag] = ""
                    else:
                        d[p.tag] = p.text
                break
        return d

    def getparams_frmt_1(self, api_name):
        '''
        This function will create the list of params for the api call. The format is mentioned below.
        :param api_name: the name of the api
        :return: dict of param in the format {"val1":"{"subval11":"a","subval12":"b"}",
                                                "val2":"{"subval21":"c","subval22":"d"}",
                                                    "val3":"{"subval31":"e","subval32":"f"}"}
        '''
        p = {}
        d = {}
        for api in self.root:
            if api.attrib["name"] == api_name:
                for b in api[0]:
                    p[b.tag] = b.text
                    if len(b):
                        for c in b:
                            # preserving the integers
                            if c.attrib.get("dt") == 'int':
                                d[c.tag] = int(c.text)
                            elif c.attrib.get("dt") == 'None':
                                d[c.tag] = ""
                            else:
                                d[c.tag] = c.text
                        p[b.tag] = str(d)
                        d = {}
                break
        return p

    def get_build_config_xml(self, req_build):
        '''
        This function will select a config file based on build number supplied
        :param req_build: The current boss build number
        :return: The name of the selected config file
        '''
        filename = None
        for build in self.root:
            l_build = build.attrib['lower_range']
            u_build = build.attrib['upper_range']
            if self.is_build_between(req_build, l_build, u_build):
                filename = build[0][0].text
                break
        return filename

    def is_build_between(self, build, l_range, u_range):
        '''
        This function will verify whether a given build is between a given build range.
        :param build: Current build
        :param l_range: Lower range
        :param u_range: Upper range
        :return: True if build is between the range
        '''
        build = [int(x) for x in build.split('.')]
        l_range = [int(x) for x in l_range.split('.')]
        u_range = [int(x) for x in u_range.split('.')]
        status = False
        if build == l_range or build == u_range:
            status = True
        else:
            for b,l,u in zip(build, l_range, u_range):
                if b >  l and b < u:
                    status = True
                    break
                elif b <  l or b > u:
                    status = False
                    break
                elif b == l or b == u:
                    status = True
        return status

    def update_boss_url(self, new_url):
        """
        Update the boss url in config file, if the url supplied by user is different from the one present in config

        :param new_url: boss url passed by user
        :return: None
        """
        from lxml import etree
        tree = etree.parse(self.filename)
        dinfo = tree.docinfo
        old_url = None
        for item in dinfo.internalDTD.iterentities():
            if item.name == "BOSSURL":
                old_url = item.content
        if old_url != new_url:
            try:
                log.info("Updating url in config file from <%s> to <%s>" % (old_url, new_url))
                fp = open(self.filename, 'r')
                content = fp.readlines()
                fp.close()
                for line in content:
                    if "--" not in line and "BOSSURL" in line:
                        x = re.sub(old_url, new_url, line)
                        content[2] = x
                        break
                fp = open(self.filename, 'w')
                fp.writelines(content)
                fp.close()
                return True
            except:
                log.error("Could not update url in config file from <%s> to <%s>.Please, change it manually." % (old_url, new_url))



class boss_api(object, Vcfe, GetDetails):
    """
    Web Apis to perform actions on the BOSS portal. e.g. creating user, assigning phone, creating hunt group etc.
    """

    def __init__(self, build = None):
        '''
        To parse the config xml after selecting the config file based on given build number.
        :param build: Current build number
        '''
        self.config_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config"))
        # calculating the correct config file based on the passed build number
        # will default to the BOSSAPIConfiguration.xml
        self.config_file = "BOSSAPIConfiguration.xml"
        if build:
            self.config_file = self.get_config_based_on_build(build)
        log.info("Config file picked for <%s> is <%s>"%(build,self.config_file))
        self.config = parse_xml(os.path.join(self.config_path, self.config_file))
        self.session_cookie = None
        self.headers = None
        # self.accountId will be set in the call to switch_account
        self.accountId = None
        self.part_id = None

    @func_logger
    def login(self, url = None, UserName = None, Password = None):
        '''
        This function will login to the boss portal with provided credentials.
        :param login_url: The boss url to login
        :param user: user name to login
        :param pwd: password for the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        # editing the boss url in config file
        if self.config.update_boss_url(url.split("//")[-1].split("/")[0]):
            self.config = parse_xml(os.path.join(self.config_path, self.config_file))
        params_xml = self.config.getparams("login")
        params = self.get_param_to_use(params_xml, url = url, UserName = UserName, Password = Password)
        log.info("Effective params for login are <%s>" % params)
        url = params.pop("url")
        ret = requests.post(url, data = params)
        if ret.status_code == 200 and "M5Portal" in ret.text:
            log.info("Login to <%s> with data <%s> is successful" % (url, params))
            self.session_cookie = ret.request.headers['Cookie']
            self.headers = {"Cookie": self.session_cookie}
            result = True
        else:
            log.error("Login to <%s> with data <%s> is not successful" % (url, params))
        return result, ret

    @func_logger
    def switch_account(self, act_name=None):
        '''
        This function will switch to the account mentioned.
        :param act_name: The boss url to login
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams("switch_account")
        act_id = self.get_account_detail(act_name = act_name)
        log.info("Switching to account <%s> with act id <%s>" % (act_name, act_id))
        url = params.pop("url")
        params["accountId"] = act_id
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and act_name in ret.text:
            log.info("Successfully switched account to <%s>" % act_name)
            self.accountId = act_id
            result = True
        else:
            log.error("Could not switch account to <%s>" % act_name)
        return result, ret

    @func_logger
    def create_tenant(self, **params):
        '''
        This function will create a new tenant with the given details.
        :param act_name: The required params to create a new tenant. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: CompanyName
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_tenant")
        params = self.get_param_to_use(params_xml, **params)
        log.info("Creating a tenant with args <%s>"%params)
        url = params.pop("url")
        for opt in ["FirstName","LastName","PhoneNumber"]:
            params[opt] = ""
        data_to_send = {"accountId":1, "values":str(params)}
        ret = requests.post(url, data = data_to_send, headers = self.headers)
        if ret.status_code == 200 and params["CompanyName"] in ret.text:
            log.info("Successfully created account with name <%s>.\nMessage from server : <%s>" % (params["CompanyName"],ret.text))
            result = True
        else:
            log.error("Could not create account with name <%s>.\nMessage from server : <%s>" % (params["CompanyName"],ret.text))
        return result, ret

    @func_logger
    def add_user(self, **params):
        '''
        This function will add a new user with the given details to a given tenant. If profile order should also be created then
        PhoneType should be passed with some valid value.

        :param params: A dictionary of parameters. Refer BOSSAPIConfiguration.xml for more info on available params

        requestedSource = [Case 1 Email 2 Phone 3]
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_user")
        params = self.get_param_to_use(params_xml, **params)
        # getting loc_id and part_id from the provided loc_name and partition name
        params["accountId"] = self.accountId
        params["Person_FirstName"] = params["Person_FirstName"]
        params["Person_LastName"] = params["Person_LastName"]
        params["Person_Username"] = params["Person_BusinessEmail"]
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Person_LocationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["Phone_LocationId"] = params["Person_LocationId"]
        params["User_LocationId"] = params["Person_LocationId"]
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["SU_Email"])
        params["PersonProfileExtension"] = params_xml["Person_Profile_Extension"]
        params["ActivationDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params["ProfileOptions"] = '[{"ProductId":474,"Name":"Connect CLOUD Instant Messaging"},{"ProductId":434,"Name":"Connect CLOUD Teamwork"}]'
        params["UserGroup"] = "4"
        url = params.pop("url")
        log.info("Adding a user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("Successfully added user username <%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
            result = True
        else:
            log.error("Could not add user with username <%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
        return result, ret

    @func_logger
    def update_person_details(self, id, value,**params):
        '''
        This function will edit  a exsiting user with the given details to a given tenant.
        :param SU_Email: The email of the super user or the one which is capable of adding other users
        other params are obvious

        requestedSource = [Case 1 Email 2 Phone 3]
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_person_details")
        params = self.get_param_to_use(params_xml, **params)
        # getting loc_id and part_id from the provided loc_name and partition name
        params["accountId"] = self.accountId
        params["Person_LocationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["personId"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        params["id"] = id
        params["value"] = value
        url = params.pop("url")
        log.info("Editting a user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and params["value"] in ret.text:
            log.info("Successfully Edited user username <%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
            result = True
        else:
            log.error("Could not add user with username <%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
        return result, ret


    def add_tn_to_user(self, **params):
        '''
        This function will assign a tn and extension to an already created user.
        Note: Provide a keyword param "prod_name" during function call if you want to change the product

        :param params: A dictionary of parameters. Refer BOSSAPIConfiguration.xml for more info on available params
        :return: A tuple of a boolean status flag and the return object from the requested url

        The following call will assign a tn and extension to a user with username = sh12@bbqsqqassh.com
        Usage: obj.add_tn_to_user(part_name="HQ1",Person_FirstName="abc3",Person_LastName="xyz",Person_BusinessEmail="sh12@bbqsqqassh.com",loc_name="loc1",SU_Email="shi@sh.com",Person_Profile_Extension="1025",Profile_TnId="+16462016017")
        '''
        result = False
        # the api is same as add user so reading the same params
        params_xml = self.config.getparams("add_tn_to_user")
        params = self.get_param_to_use(params_xml, **params)
        # getting loc_id and part_id from the provided loc_name and partition name
        params["accountId"] = self.accountId
        params["Person_Username"] = params["Person_BusinessEmail"]
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Person_LocationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["Phone_LocationId"] = params["Person_LocationId"]
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["SU_Email"])
        params["ActivationDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params["UserGroup"] = "4"
        params["personId"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_Username"])
        # the product details
        prods = {"ConnectCLOUD Essentials": "351", "Connect CLOUD Standard": "352", "Connect CLOUD Advanced": "356",
         "Connect CLOUD Telephony": "354", "Connect CLOUD Voicemail Only": "399", "Programming": "-1",
         "Test Profile": "-2"}
        if params.has_key("prod_name"):
            prod_id = prods["prod_name"]
            prod_name = params["prod_name"]
            params["ProfileOptions"] = '[{"ProductId":%s,"Name":"%s"}]'%(prod_id, prod_name)
        else:
            params["ProfileOptions"] = '[{"ProductId":474,"Name":"Connect CLOUD Instant Messaging"},{"ProductId":434,"Name":"Connect CLOUD Teamwork"}]'

        url = params.pop("url")
        log.info("Assigning tn/extension to user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200:
            log.info("Successfully assigned tn to user.\nMessage from server : <%s>" % (
            ret.text))
            result = True
        else:
            log.error("Could not assigned tn to user.\nMessage from server : <%s>" % (
            ret.text))
        return result, ret

    def change_password(self, **params):
        '''
        This function will change the password for a given user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("change_password")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["personID"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        if params.has_key("NewPersonPassword"):
            params["ConfirmPersonPassword"] = params["NewPersonPassword"]
        url = params.pop("url")
        log.info("Modifying the password with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200:
            log.info("Successfully changed the password for the user<%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
            result = True
        else:
            log.error("Could not change the password for the user <%s>.\nMessage from server : <%s>" % (
            params["Person_BusinessEmail"], ret.text))
        return result, ret

    def assign_role(self, **params):
        '''
        This function will change the password for a given user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :param role_name: The role name to assign to the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams_frmt_1("assign_role")
        params["accountId"] = self.accountId
        params["personID"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        roles = {"Decision Maker":"1","Phone Manager":"2","Billing":"3","Emergency":"4","Partner":"7","Technical":"8"}
        for role in roles.keys():
            if role == params["role_name"]:
                rd = ast.literal_eval(params["rolesData"])
                rd["Id"] = roles[role]
                rd["Name"] = role
        # converting the rolesData to a list
        temp = []
        temp.append(rd)
        params["rolesData"] = str(temp)
        url = params.pop("url")
        log.info("Assigning role to the user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("Assigned role <%s> to user.\nMessage from server : <%s>" % (
                params["role_name"], ret.text))
            result = True
        else:
            log.error("Could not assign role <%s>.\nMessage from server : <%s>" % (
                params["role_name"], ret.text))
        return result, ret

    def unassign_role(self, **params):
        '''
        This function will change the password for a given user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :param role_name: The role name to assign to the user
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams_frmt_1("assign_role")
        params["accountId"] = self.accountId
        params["personID"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        # roles = {"Decision Maker":"1","Phone Manager":"2","Billing":"3","Emergency":"4","Partner":"7","Technical":"8"}
        # for role in roles.keys():
        #     if role == role_name:
        #         rd = ast.literal_eval(params["rolesData"])
        #         rd["Id"] = roles[role]
        #         rd["Name"] = role
        # # converting the rolesData to a list
        # temp = []
        # temp.append(rd)
        # params["rolesData"] = str(temp)
        url = params.pop("url")
        log.info("Deleting all the assigned roles with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("Deleted all the roles assigned to the user.\nMessage from server : <%s>" % (
                 ret.text))
            result = True
        else:
            log.error("Could not delete assigned roles to the user.\nMessage from server : <%s>" % (
                 ret.text))
        return result, ret

    def close_user(self, **params):
        '''
        This function will close the user.
        :param part_name: The name of the partition required to get the perposn id
        :param Person_BusinessEmail: The email of the user required to get the perposn id
        :param requestedby: The
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("close_user")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["personId"] = self.get_person_detail(self.accountId, params["part_name"], params["Person_BusinessEmail"])
        # params["requestedById"] = self.get_person_detail(self.accountId, part_name, Person_BusinessEmail)
        params["requestedById"] = params["personId"]
        params["billCeaseDate"] = (datetime.date.today()+datetime.timedelta(days=36)).strftime("%m/%d/%Y")
        url = params.pop("url")
        log.info("closing the user with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("Successfully closed the user.\nMessage from server : <%s>" % (
                 ret.text))
            result = True
        else:
            log.error("Could not close the user.\nMessage from server : <%s>" % (
                 ret.text))
        return result, ret

    @func_logger
    def add_tn(self, **params):
        '''
        This function will add a telephone string to an account.
        :param act_name: The required params to add a tn string. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: tnstring,tenant,requestedBy
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_tn")
        params = self.get_param_to_use(params_xml, **params)
        log.info("Adding telephone numbers with args <%s>" % params)
        params["accountId"] = self.accountId
        params["TnAccountId"] = params["accountId"]
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["username"])
        url = params.pop("url")
        for opt in ["CaseNumber","ExtensionConflicts"]:
            params[opt] = ""

        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and str(params["accountId"]) in ret.text:
            log.info("Successfully added tn to the account with name <%s>.\nMessage from server : <%s>" % (
            params["act_name"], ret.text))
            result = True
        else:
            log.error("Could not add tn to account with name <%s>.\nMessage from server : <%s>" % (
            params["act_name"], ret.text))
        return result, ret

    def reassign_tn(self, **params):
        '''
        This function will reassign a tn or extension to a user
        :param act_name: The required params to add a tn string. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: tnstring,tenant,requestedBy
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("reassign_tn")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["profileId"] = self.get_profile_detail(self.accountId,params["part_name"],params["username"])
        url = params.pop("url")
        log.info("Reassigning tn to user with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["message"] == "Number was re-assigned":
            log.info("Successfully reassigned tn/extension to the user.\nMessage from server : <%s>" % (
            ret.text))
            result = True
        else:
            log.error("Could not reassign tn/extension to the user.\nMessage from server : <%s>" % (
            ret.text))
        return result, ret

    def add_edit_phone(self, **params):
        '''
        This function will add a given phone to an account.
        :param loc_name: location name in which the phone needs to be added
        :param mac_address: mac address of the phone to be added  e.g.  11:11:11:11:11:11
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_edit_phone")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["Phone_LocationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["Phone_MacAddress"] = params["mac_address"]
        log.info("Adding a new phone with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == u'Note: Adding this phone does not constitute purchase or shipment of a phone from Shoretel. If you want to do so, please use the Add Services screen.':
            log.info("Successfully added phone.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        elif ret.status_code == 200 and ret.json()["message"] == u'Note: Editing this phone does not constitute purchase or shipment of a phone from Shoretel. If you want to do so, please use the Add Services screen.':
            log.info("Successfully edited phone.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not add phone.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def remove_phone_entry(self, **params):
        '''
        This function will remove an added telephone.
        :param mac_address: mac address of the phone to be added  e.g.  11:11:11:11:11:11
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("remove_phone_entry")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["macAddress"] = params["mac_address"]
        log.info("Removing phone with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json()["message"] == u'Phone With Mac Address %s has been successfully deleted.'%mac_address:
            log.info("Successfully removed phone.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not remove phone.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def check_extension_availability(self, **params):
        '''
        This function will check if an extension is available or not
        :param part_name: The partition name
        :param extension: The extension number to check
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("check_extension_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["extension"] = params["extension"]
        url = params.pop("url")
        log.info("Reassigning tn to user with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and str(ret.json()) == str(params["extension"]):
            log.info("Extension <%s> is available.\nMessage from server : <%s>" % (
                params["extension"], ret.text))
            result = True
        elif ret.status_code == 200 and str(ret.json()) != str(params["extension"]):
            log.info("Extension <%s> already in use.Suggested extension is <%s>.\nMessage from server : <%s>" % (
                params["extension"], ret.json(),ret.text))
            result = True
        else:
            log.error("Could not reassign tn/extension to the user.\nMessage from server : <%s>" % (
            ret.text))
        return result, ret

    def check_usergroup_availability(self, **params):
        '''
        This function will check if an extension is available or not
        :param part_name: The partition name
        :param ug_name: The name of the user group created
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        is_available = False
        params_xml = self.config.getparams("check_usergroup_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["userGroupName"] = params["ug_name"]
        url = params.pop("url")
        log.info("Checking availability of user group with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("result"):
            log.info("User group name is available.\nMessage from server : <%s>" % (
                ret.text))
            is_available = True
        else:
            log.error("User group name is not available.\nMessage from server : <%s>" % (
            ret.text))

        return is_available

    def check_username_availability(self, **params):
        '''
        This function will check if a user name is available or not
        :param user_name: The user name to be checked
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        is_available = False
        params_xml = self.config.getparams("check_username_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["username"] = params["user_name"]
        url = params.pop("url")
        log.info("Checking availability of user name with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.text == 'true':
            log.info("User name is available.\nMessage from server : <%s>" % (
                ret.text))
            is_available = True
        else:
            log.error("User name is not available.\nMessage from server : <%s>" % (
            ret.text))

        return is_available

    def check_mac_address_availability(self, **params):
        '''
        This function will check if a macAddress is available or not
        :param macAddress: The macAddress to be checked
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        is_available = False
        params_xml = self.config.getparams("check_mac_address_availability")
        params = self.get_param_to_use(params_xml, **params)
        params["macAddress"] = params["macAddress"]
        url = params.pop("url")
        log.info("Checking availability of macAddress with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.text == 'true':
            log.info("macAddress is available.\nMessage from server : <%s>" % (
                ret.text))
            is_available = True
        else:
            log.error("macAddress is not available.\nMessage from server : <%s>" % (
            ret.text))

        return is_available

    @func_logger
    def update_tn(self, **params):
        '''
        This function will update a tn status.
        :param tnstring: the tn string to update. don't use the + sign
        :param params: The required params to update a tn string. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: state,type
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        tn_ends = '.840.1'
        type = {"Real":"1"}
        state = {"Available":"4"}
        # converting string to corresponding ints and overriding them in param
        params["Type"] = type[params["type"]] if params.get("type") else 1
        params["State"] = state[params["state"]] if params.get("state") else 4
        params["PortOutDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params_xml = self.config.getparams("update_tn")
        # assigning not required param to ""
        for opt in ["TnCountryId", "TnAccountId", "ExtensionConflicts"]:
            params_xml[opt] = ""
        params = self.get_param_to_use(params_xml, **params)
        # mandatory param
        if "-" in params["tnstring"]:
            tn_range = params["tnstring"].split("-")
            tn_range[1] = tn_range[0][:-4] + tn_range[1] + tn_ends
            params["TnsString"] = tn_range[0]+tn_ends+'|'+tn_range[1]+tn_ends
        else:
            params["TnsString"] = params["tnstring"] + tn_ends
        params["accountId"] = self.accountId
        url = params.pop("url")

        log.info("Updating telephone numbers with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and str(params["accountId"]) in ret.text:
            log.info("Successfully updated tn <%s>.\nMessage from server : <%s>" % (
                params["TnsString"], ret.text))
            result = True
        else:
            log.error("Could not update tn <%s>.\nMessage from server : <%s>" % (
                params["TnsString"], ret.text))
        return result, ret

    def add_contract(self, **params):
        '''
        This method will add a new contract.
        :param company_name: the name of the company to be used while adding the contract
        :param params: The required params to add a new contract. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.Frequently used params are: CompanyName
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params = self.config.getparams_frmt_1("add_contract")
        url = params.pop("url")
        # updating the values provided by the user
        temp_val = ast.literal_eval(params["accountValues"])
        temp_val["CompanyName"] = params["company_name"]
        params["accountValues"] = str(temp_val)
        # modifying format of some params to suit the api demand
        d =  ast.literal_eval(params["locationsValues"])
        t= d["ValidationResult"]
        p = ast.literal_eval(t)
        d["ValidationResult"] = p
        params["locationsValues"] = d
        # modifying the details of the contract pdf file
        contract = ast.literal_eval(params["contractValues"])
        if os.path.isfile(params["file_path"]):
            contract["ContractFileName"] = os.path.basename(params["file_path"])
        else:
            raise Exception("File <%s> does not exist"%params["file_path"])
        contract["ContractFilePath"] = str(self.upload_pdf(params["file_path"]))
        params["contractValues"] = str(contract)
        # converting productValues and locationValues to lists
        temp = []
        temp.append(params["locationsValues"])
        params["locationsValues"] = str(temp)
        temp = []
        temp.append(ast.literal_eval(params["productsValues"]))
        params["productsValues"] = str(temp)
        # removing quotes from the text
        params["accountValues"] = params["accountValues"].replace('\'null\'','null')
        log.info("Adding contract with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and "New Contract successfully added " in ret.text:
            log.info("Successfully added new contract with id <%s>.\nMessage from server : <%s>" % (
                ast.literal_eval(ret.text)["newAccountId"], ret.text))
            result = True
        else:
            log.error("Could not add new contract.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def update_billing_location(self,account_name, billing_locationName):
        '''

        :param account_name:
        :param billing_locationName:
        :return:
        '''
        result = False
        params = self.config.getparams_frmt_1("update_billing_location")
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["contractId"] = self.get_contract_detail(self.accountId)
        params["billingLocationId"] = self.get_location_detail(self.accountId, billing_locationName)
        log.info("Updating the billing location for account <%s>" % account_name)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "Contract billing location successfully updated." in ret.text:
            log.info("Successfully updated billing location <%s> for account <%s>.\nMessage from server : <%s>" % (
                billing_locationName, account_name, ret.text))
            result = True
        else:
            log.error("Could not update billing location <%s> for account <%s>.\nMessage from server : <%s>" % (
                billing_locationName, account_name, ret.text))
        return result, ret

    def add_instance_to_contract(self, **params):
        '''
        This function will add an instance to the contract
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_instance_to_contract")
        url = params_xml.pop("url")
        params_xml["AccountId"] = self.accountId
        params_xml["ClusterId"] = self.get_cluster_detail(params_xml["Cluster"].split()[0])
        params["newValues"] = str(params_xml)
        log.info("Adding instance to the contract with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["Id"] != None:
            log.info("Successfully added instance to the contract.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not add an instance to the contract.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def add_location_as_site(self, **params):
        '''
        This function will add a given location as a site.
        :param loc_name: location name to be added as site
        :param part_name: partition name
        :param params: The required params to add a location as site. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("assign_location_as_site")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        loc_id = self.get_location_detail(self.accountId, params["loc_name"])
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["siteData"] = '[{"LocationId":"%s", "AreaCode":"auto"}]'%loc_id
        log.info("Adding location as site with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200:
            log.info("Successfully added location <%s> as site.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        else:
            log.error("Could not add location <%s> as site.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def add_location(self, **params):
        '''
        This function will add a given location as a site.
        :param loc_name: location name to be added
        :param part_name: partition name
        :param params: The required params to add a location as site. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Location_Subtenant"] = params["LocationDetails_LocationNameFormatted"] = params["loc_name"]
        params["Location_InvoiceGroupId"] = self.get_suitable_invoice_groups(self.accountId,params["invoice_group"])
        log.info("Adding a new location with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("retValue"):
            log.info("Successfully added location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        else:
            log.error("Could not add location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def update_location(self, **params):
        '''
        This function will update the address of a location
        :param loc_name: location name to be added
        :param part_name: partition name
        :param params: The required params to add a location as site. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["locationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Location_Subtenant"] = params["LocationDetails_LocationNameFormatted"] = params["loc_name"]
        log.info("Updating a location with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("retValue"):
            log.info("Successfully updated location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        else:
            log.error("Could not update location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def close_location(self, **params):
        '''
        This function will close a location. The function will first close the associated order
        :param loc_name: location name to be added
        :param SU_Email: super user or DM
        :param params: The required params to close a location. Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        # closing the order before proceeding to close the location
        order = self.get_order_detail(self.accountId, params["loc_name"])
        self.update_order_details(order)
        # now closing the location
        params_xml = self.config.getparams("close_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["closeLocationId"] = params["locationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["billCeaseDate"] = datetime.date.today().strftime("%m/%d/%Y")
        params["requestedById"] = self.get_dm_detail(self.accountId, params["SU_Email"])
        log.info("Closing a location with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("Successfully closed location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            result = True
        elif ret.json().has_key("error"):
            log.error("Could not close the location <%s>.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return result, ret

    def update_order_details(self, **params):
        '''
        This function will close an order
        :param order_id: the id of the order
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_order_details")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["orderId"] = params["order_id"]
        log.info("Closing the order with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("Successfully closed the order.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        elif len(ret.text) == 2 or ret.json().has_key("error"):
            log.error("Could not close the order.\nMessage from server : <%s>" % (
                ret.text))
        return result, ret

    def validate_canclose_location(self, **params):
        '''
        This function will validate if a location can be closed or not
        :param loc_name: location name to be added
        :param params: Please, refer to BOSSAPIConfiguration.xml for a complete list
        of params which can be passed to this function.
        :return: A boolean status flag
        '''
        can_close = False
        params_xml = self.config.getparams("validate_canclose_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        params["accountId"] = self.accountId
        params["locationId"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["billCeaseDate"] = datetime.date.today().strftime("%m/%d/%Y")
        log.info("Validating if a location can be closed with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("Location <%s> can be closed.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
            can_close = True
        else:
            log.error("Location <%s> can not be closed.\nMessage from server : <%s>" % (
                params["loc_name"], ret.text))
        return can_close

    def validate_location(self, **params):
        '''
        This function will validate a given location.
        :param params: The account name
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        isValid = False
        params_xml = self.config.getparams("validate_location")
        params = self.get_param_to_use(params_xml, **params)
        url = params.pop("url")
        log.info("Validating location with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and len(ret.json()['Errors']) == 0:
            log.info("The given location is valid.Message from server : <%s>"% (ret.text))
            isValid = True
        else:
            log.error("The given location is not valid.Message from server : <%s>"% (ret.text))

        return isValid,ret

    def validate_location_name(self,loc_name, **params):
        '''
        This function will validate a given location.
        :param loc_name: The location name to be validated
        :return: A boolean status flag
        '''
        IsValid = False
        params_xml = self.config.getparams("validate_location_name")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["locationName"] = loc_name
        url = params.pop("url")
        log.info("Validating location name with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()['isValid']:
            log.info("The given location name is valid.Message from server : <%s>"% (ret.text))
            IsValid = True
        else:
            log.error("The given location name is not valid.Message from server : <%s>"% (ret.text))
        return IsValid

    def create_partition(self, **params):
        '''
        This function will create a partition.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_partition")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        if params.has_key("cluster_name"):
            params["ClusterId"] = self.get_cluster_detail(params["cluster_name"])
        params["siteData"] = '[{"LocationId":%s,"AreaCode":"auto"}]'%(self.get_location_detail(self.accountId,params["location_name"]))
        url = params.pop("url")
        log.info("Creating partition with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()['retValue'] == 132:
            log.info("The requested partition has been created.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("The requested partition could not be created.Message from server : <%s>"% (ret.text))

        return result, ret

    def add_profile(self, **params):
        '''
        This function will add a profile.
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("add_profile")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["RequestedByAdd"] = self.get_dm_detail(self.accountId, params["dm_name"])
        params["AddLocationToAssign"] = self.get_location_detail(self.accountId, params["location_name"])
        params["DateLiveAdd"] = datetime.date.today().strftime("%m/%d/%Y")
        url = params.pop("url")
        log.info("Adding profile with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)

        # todo identify the ret.json when it passes without processing in background
        if ret.status_code == 200 and ret.json()['retValue'] == 132:
            log.info("The requested profile has been added.Message from server : <%s>"% (ret.text))
            result = True
        elif "Order has been created, and processing takes longer than expected. It will be processed in the background" in ret.text:
            log.info("The requested profile has been added.Message from server : <%s>" % (ret.text))
            result = True
        else:
            log.error("The requested profile could not be added.Message from server : <%s>"% (ret.text))
        return result, ret

    def validate_assign_profile(self, user_name, **params):
        '''
        This function will validate a profile
        primary Partition -> assign number -> the username entered will be validated
        :return: A boolean result flag
        '''
        isValid = False
        params_xml = self.config.getparams("validate_assign_profile")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["username"] = user_name
        url = params.pop("url")
        log.info("Validating the profile with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["validationResult"]:
            log.info("The requested profile has been validated.Message from server : <%s>"% (ret.text))
            isValid = True
        else:
            log.error("The requested profile could not be validated.Message from server : <%s>"% (ret.text))
        return isValid

    def assign_number(self, **params):
        '''
        This function will assign a number to a user
        primary Partition -> assign number
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("assign_number")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["tn"] = params["tn"]
        params["Email"] = params["user_name"]
        params["LocationToAssign"] = self.get_location_detail(self.accountId, params["loc_name"])
        params["DateLive"] = datetime.date.today().strftime("%m/%d/%Y")
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["dm_name"])
        params["extension"] = params["extension"]
        url = params.pop("url")
        log.info("Assigning the number with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        # todo need to verify the succes case. At present all orders are going in pipeline to process.
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The number has been assigned successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("The number could not be assigned.Message from server : <%s>"% (ret.text))
        return result, ret

    def unassign_number(self, **params):
        '''
        This function will unassign a number to a user
        primary Partition -> assign number
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("unassign_number")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.part_id
        params["ProfileIds"] = params["profileIds"] = self.get_profile_detail(self.accountId,params["part_name"],params["user_name"])
        params["RequestedBy"] = self.get_dm_detail(self.accountId, params["dm_name"])
        url = params.pop("url")
        log.info("Unassigning the number with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("The number has been unassigned successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("The number could not be unassigned.Message from server : <%s>"% (ret.text))
        return result, ret

    def update_cosmo_partition_dialplan(self, **params):
        '''
        This function will update a dial plan
        primary Partition -> dial plan
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_cosmo_partition_dialplan")
        params = self.get_param_to_use(params_xml, **params)
        # params["accountId"] = int(self.accountId)
        # params["partitionId"] = int(self.part_id)
        # params["locationId"] = -1
        # todo for some unknown reason at this point of time, the api works only if url is in below format
        url = params.pop("url") + "?accountId=%d&locationId=%d&partitionId=%d"%(self.accountId, -1, int(self.part_id))
        # url = params.pop("url")
        log.info("Updating dial plan with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json()["success"]:
            log.info("The dial plan has been updated.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not update the dial plan.Message from server : <%s>"% (ret.text))
        return result, ret


    def create_usergroup(self, **params):
        '''
        This function will create a user group

        ProfileTypeId = {"Managed":"2","Courtesy":"5","TelephoneOnly":"7"}
        : param ug_name: The name of user name to be created
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_usergroup")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["Name"] = params["ug_name"]
        url = params.pop("url")
        log.info("Creating user group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("User group created successfully.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not create User group.\nMessage from server : <%s>" % (
                ret.text))

        return result, ret

    def update_usergroup(self, **params):
        '''
        This function will update a user group
        : param ug_name: The name of user name to be updated
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_usergroup")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["Name"] = params["ug_name"]
        params["partitionId"] = self.get_partition_detail(self.accountId, params["part_name"])
        params["groupId"] = self.get_usergroup_detail(self.accountId, params["part_name"],params["ug_name"])
        url = params.pop("url")
        log.info("Updating user group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("User group updated successfully.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not update User group.\nMessage from server : <%s>" % (
                ret.text))

        return result, ret

    def delete_usergroup(self, **params):
        '''
        This function will delete a user group
        : param ug_name: The name of user name to be created
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("delete_usergroup")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["groupIds"] = self.get_usergroup_detail(self.accountId, params["part_name"],params["ug_name"])
        url = params.pop("url")
        log.info("Deleting user group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and (ret.text) == '"success"':
            log.info("User group deleted successfully.\nMessage from server : <%s>" % (
                ret.text))
            result = True
        else:
            log.error("Could not delete User group.\nMessage from server : <%s>" % (
                ret.text))

        return result, ret

    def update_contract_status(self, **params):
        '''
        Make sure to add following to the contract before trying to confirm the status
        add location - update_billing_location
        add instance - add_instance_to_contract
        add partition- create_partition

        These functions are not called from this function to give more flexibility and control.

        This function will update the status of a contract.
        :param params: The account name
        :return: True if location is valid
        '''
        result = False
        params_xml = self.config.getparams("update_contract_status")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = self.accountId
        params["contractId"] = self.get_contract_detail(self.accountId)
        url = params.pop("url")
        log.info("Updating the contract status with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            while not self.get_async_web_job(ret.json()["Id"]) == 100:
                time.sleep(1)
            order_id = self.get_contract_line_item_data(self.accountId,params["contractId"])
            if order_id:
                log.info("The contract has been confirmed.Order id : <%s>"% (order_id))
                result = True
            else:
                log.error("The contract could not been confirmed.Order id : <%s>" % (order_id))
        else:
            log.error("The contract could not been confirmed.Message from server : <%s>"% (ret.text))

        return result, ret

    def get_async_web_job(self, id):
        '''
        This function will return the status of a async web job
        :param id: The id of the job
        :return: % value of the job completed
        '''
        params = self.config.getparams("get_async_web_job")
        url = params.pop("url")
        log.info("Updating the contract status with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("The contract has been confirmed.Message from server : <%s>"% (ret.text))
        else:
            log.error("The contract could not been confirmed.Message from server : <%s>"% (ret.text))
        return int(ret.json()["PercentComplete"])

    def get_contract_line_item_data(self, account_id, contract_id):
        '''
        This function will return the status of the contract
        :param account_id: The id of the account
        :param contract_id: The id of the contract in the account
        :return: the order id
        '''
        order_id = 0
        params = self.config.getparams("get_contract_line_item_data")
        params["accountId"] = account_id
        params["contractId"] = contract_id
        url = params.pop("url")
        log.info("Getting the order id for contract updated with args <%s>" % params)
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200:
            log.info("The contract has been confirmed.Message from server : <%s>"% (ret.text))
        else:
            log.error("The contract could not been confirmed.Message from server : <%s>"% (ret.text))

        # parsing the returned content to get the id
        for loc, details in ret.json().iteritems():
            if loc == "data":
                for d in details:
                    order_id = d["OrderId"]
                    break
        return order_id

    def upload_pdf(self, filepath):
        '''
        This function will upload the pdf contract
        :param params: The param
        :return: The location of the uploaded pdf contract, which should be used while adding a new contract or None if fails
        '''
        uploaded_path = None
        params = self.config.getparams("upload_pdf")
        url = params.pop("url")
        files = {'file': open(filepath, 'rb')}
        log.info("Uploading the pdf contract file <%s>" % params)
        ret = requests.post(url, data=params, files=files, headers=self.headers)
        uploaded_path = ret.json()['filePath']
        if ret.status_code == 200 and ret.json()['message'] == "OK":
            log.info("Successfully uploaded pdf to <%s>" % (uploaded_path))
        else:
            log.error("could not upload the pdf contract file.Message from server: <%s>" % (ret.text))

        return str(uploaded_path)

    def update_cosmo_conference(self, dm_user, **params):
        '''
        This function will activate the collaboration add on
        phone system -> add on --> collaboration
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("update_cosmo_conference")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["partitionId"] = int(self.part_id)
        params["EmailList"] = dm_user
        url = params.pop("url")
        log.info("Activating collaboration add on with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The collaboration has been activated.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not activate the collaboration ad on.Message from server : <%s>"% (ret.text))
        return result, ret

    def create_cosmo_conference_handler(self, user_fullname, **params):
        '''
        This function will get the available users for creating a cosmo conference
        phone system -> add on --> collaboration --> manage
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        profile_id = None
        params_xml = self.config.getparams("create_cosmo_conference_handler")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["partitionId"] = int(self.part_id)
        url = params.pop("url")
        log.info("Getting the users available for creating collaboration with args <%s>" % params)
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "ProfileId" in ret.text:
            log.info("The users have been retrieved for creating collaboration.Message from server : <%s>"% (ret.text))
        else:
            log.error("Could not retrieve users for creating collaboration.Message from server : <%s>"% (ret.text))
        # parsing the returned content to get the act id
        for node in ret.json()["data"]:
            if node["FullName"] == user_fullname:
                profile_id = node["ProfileId"]
                break
        return profile_id

    def get_cosmo_conference_detail_handler(self, act_id, profile_id):
        '''
        This function will get the service id based on profile id

        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        service_id = None
        params = self.config.getparams("get_cosmo_conference_detail_handler")
        params["accountId"] = int(self.accountId)
        url = params.pop("url")
        log.info("Getting the service ids with args <%s>" % params)
        ret = requests.get(url, data = params, headers = self.headers)
        if ret.status_code == 200 and "ProfileId" in ret.text:
            log.info("The service ids have been retrieved successfully.Message from server : <%s>"% (ret.text))
        else:
            log.error("Could not retrieve the service ids.Message from server : <%s>"% (ret.text))
        # parsing the returned content to get the act id
        for node in ret.json()["data"]:
            if node["ProfileId"] == int(profile_id):
                service_id = node["ServiceId"]
                break
        return service_id

    def create_cosmo_conference(self, dm_name, user_fullname, **params):
        '''
        This function will create a cosmo conference
        phone system -> add on --> collaboration --> manage --> Add
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_cosmo_conference")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["RequestedBy"] = self.get_dm_detail(self.accountId, dm_name)
        profile_id = self.create_cosmo_conference_handler(user_fullname)
        params["id_%s"%profile_id] = profile_id
        url = params.pop("url")
        log.info("Creating collaboration with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The conference has been created.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not create the conference.Message from server : <%s>"% (ret.text))

        return result, ret

    def delete_cosmo_conference(self, dm_name, part_name, user_name, **params):
        '''
        This function will delete a cosmo conference
        phone system -> add on --> collaboration --> rt click on the created conference
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("delete_cosmo_conference")
        params = self.get_param_to_use(params_xml, **params)
        params["accountId"] = int(self.accountId)
        params["serviceIds"] = self.get_cosmo_conference_detail_handler(self.accountId,
                            self.get_profile_detail(self.accountId, part_name, user_name))
        params["requestedById"] = self.get_dm_detail(self.accountId, dm_name)
        params["billCeaseDate"] = datetime.date.today().strftime("%m/%d/%Y")
        url = params.pop("url")
        log.info("Deleting collaboration with args <%s>" % params)
        ret = requests.post(url, data = params, headers = self.headers)
        if ret.status_code == 200 and ret.json().has_key("message"):
            log.info("The conference has been deleted successfully.Message from server : <%s>"% (ret.text))
            result = True
        else:
            log.error("Could not delete the conference.Message from server : <%s>"% (ret.text))

        return result, ret


    # def get_param_to_use(self, xml_params, **kwargs ):
    #     '''
    #     Note: The named params in the api definition must be same as expected by the boss http request.
    #
    #     This function will return a list of params which should be used for the http calls. This will compare params picked from the xml file
    #     and override them with the param which were passed by the user during the call from the application.
    #     :param xml_params: A dictonary which holds the values from the xml file
    #     :param args: A list of the param passed to the function from the application
    #     :return: A dictionary with user preferences updated. User provided param will over ride the xml values.
    #     '''
    #
    #     for param in kwargs:
    #         if kwargs[param] is not None:
    #             xml_params[param] = kwargs[param]
    #     return xml_params
    #
    # def get_config_based_on_build(self, build):
    #     '''
    #     To get the correct xml config file based on the build number provided
    #     :param build: the current build number
    #     :return: the file path or exception on failure
    #     '''
    #     build_xml = parse_xml(os.path.join(self.config_path,"build_info.xml"))
    #     build_config_file = build_xml.get_build_config_xml(build)
    #     if build_config_file:
    #         return build_config_file
    #     else:
    #         raise Exception("Incorrect build <%s> or missing range in the build_info.xml" %build)
    #
    # # Following functions are helper functions which are used to get certain details from the server
    #
    # def get_account_detail(self, url = None, act_name = None):
    #     '''
    #     This function will return all the accounts in a acount id.
    #     :param act_name: The account name
    #     :return: the acount id of the specified act name
    #     '''
    #     act_id = None
    #     params = self.config.getparams("get_account_detail")
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "Login" not in ret.text:
    #         log.info("Successfully retrieved all accounts info.")
    #     else:
    #         log.error("Could not retrieve all accounts info.")
    #     # parsing the returned content to get the act id
    #     for node in ret.json()["data"]:
    #         if node["CompanyName"] == act_name:
    #             act_id = node["id"]
    #             break
    #     return act_id
    #
    # def get_suitable_invoice_groups(self, act_id, invoice_group_name):
    #     '''
    #     This function will return all the invoice groups in a account
    #     :param act_name: The account name
    #     :return: the acount id of the specified act name
    #     '''
    #     invoice_group_id = None
    #     params = self.config.getparams("get_suitable_invoice_groups")
    #     url = params.pop("url")
    #     params["accountId"] = act_id
    #     ret = requests.post(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and invoice_group_name in ret.text:
    #         log.info("Successfully retrieved all invoice group info.")
    #     else:
    #         log.error("Could not retrieve all invoice group info.")
    #     # parsing the returned content to get the act id
    #     for grp in ret.json():
    #         if grp["Name"] == invoice_group_name:
    #             invoice_group_id = grp["Id"]
    #             break
    #     return invoice_group_id
    #
    # def get_dm_detail(self, act_id, username):
    #     '''
    #     This function will return the id of the DM in the specified tenant.
    #     :param act_name: The account name
    #     :param dm_name: The name of dm
    #     :return: the DM id in the specified act name
    #     '''
    #     dm_id = None
    #     params = self.config.getparams("dm_details")
    #     params["selectedAccountId"] = act_id
    #     url = params.pop("url")
    #     ret = requests.post(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "Login" not in ret.text:
    #         log.info("Successfully retrieved all accounts info.")
    #     else:
    #         log.error("Could not retrieve all accounts info.")
    #     # parsing the returned content to get the dm id
    #     for node in ret.json():
    #         if node["Username"] == username:
    #             dm_id = node["id"]
    #             break
    #     return dm_id
    #
    # def get_contract_detail(self, accountId):
    #     '''
    #     This function will return the id of the contract in the specified account.
    #     :param accountId: The account id
    #     :return: the contract id in the specified act name
    #     '''
    #     contract_id = None
    #     params = self.config.getparams("get_contract_details")
    #     params["accountId"] = params["selectedAccountId"] = accountId
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "AccountId" in ret.text:
    #         log.info("Successfully retrieved contract info.")
    #     else:
    #         log.error("Could not retrieve all contract info.")
    #     # parsing the returned content to get contract id
    #     for cont, details in ret.json().iteritems():
    #         if cont == "data":
    #             for d in details:
    #                 if d["AccountId"] == int(accountId):
    #                     contract_id = d["id"]
    #                     break
    #
    #     return contract_id
    #
    # def get_order_detail(self, accountId, loc_name):
    #     '''
    #     This function will return the id of the order based on the provided location name.
    #     :param accountId: The account id
    #     :param loc_name: The name of the location
    #     :return: the order id in the specified act name
    #     '''
    #     order_id = None
    #     loc_id = self.get_location_detail(accountId, loc_name)
    #     params = self.config.getparams("get_order_detail")
    #     params["accountId"] = accountId
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and ret.json().has_key("data"):
    #         log.info("Successfully retrieved order info.")
    #     else:
    #         log.error("Could not retrieve all order info.")
    #     # parsing the returned content to get id
    #     for cont, details in ret.json().iteritems():
    #         if cont == "data":
    #             for d in details:
    #                 if d["LocationId"] == int(loc_id):
    #                     order_id = d["Id"]
    #                     break
    #
    #     return order_id
    #
    # def get_location_detail(self, act_id, loc_name):
    #     '''
    #     This function will return the id of the location in the specified tenant.
    #     :param act_id: The account id
    #     :param location_name: The name of location
    #     :return: the location id in the specified act name
    #     '''
    #     loc_id = None
    #     params = self.config.getparams("get_location_detail")
    #     params["accountId"] = act_id
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "FullAddress" in ret.text:
    #         log.info("Successfully retrieved all location info.")
    #     else:
    #         log.error("Could not retrieve all location info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["LabelFormatted"] == loc_name:
    #                     loc_id = d["LocationId"]
    #                     break
    #
    #     return loc_id
    #
    # def get_partition_detail(self, act_id, part_name):
    #     '''
    #     This function will return the id of the partition in the specified tenant.
    #     :param act_id: The account id
    #     :param part_name: The name of partition
    #     :return: the partition id in the specified act name
    #     '''
    #     self.part_id = None
    #     params = self.config.getparams("get_partition_detail")
    #     params["accountId"] = act_id
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "ClusterId" in ret.text:
    #         log.info("Successfully retrieved all partition info.")
    #     else:
    #         log.error("Could not retrieve all partition info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["Cluster"] == part_name:
    #                     self.part_id = d["Id"]
    #                     break
    #
    #     return self.part_id
    #
    # def get_profile_detail(self, act_id, part_name,user_name):
    #     '''
    #     This function will return the id of the profile of a user.
    #     :param act_id: The account id
    #     :param part_name: The name of partition
    #     :param user_name: The user name of the user
    #     :return: the partiton id in the specified act name
    #     '''
    #     profile_id = None
    #     params = self.config.getparams("get_profile_detail")
    #     params["accountId"] = act_id
    #     params["partitionId"] = self.get_partition_detail(act_id,part_name)
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200:
    #         log.info("Successfully retrieved all profile info.")
    #     else:
    #         log.error("Could not retrieve all profile info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["BusinessEmail"] == user_name:
    #                     profile_id = d["ProfileId"]
    #                     break
    #
    #     return str(profile_id)
    #
    # def get_usergroup_detail(self, act_id, part_name, usergroup_name):
    #     '''
    #     This function will return the id of a user group.
    #     :param act_id: The account id
    #     :param part_name: The name of partition
    #     :param usergroup_name: The user name of the user group
    #     :return: the partiton id in the specified act name
    #     '''
    #     usergroup_id = None
    #     params = self.config.getparams("get_usergroup_detail")
    #     params["accountId"] = act_id
    #     params["partitionId"] = self.get_partition_detail(act_id,part_name)
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200:
    #         log.info("Successfully retrieved all user group info.")
    #     else:
    #         log.error("Could not retrieve all user group info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["Name"] == usergroup_name:
    #                     usergroup_id = d["id"]
    #                     break
    #
    #     return str(usergroup_id)
    #
    # def get_person_detail(self, act_id, part_name,BusinessEmail):
    #     '''
    #     This function will return the id of the person in the specified account.
    #     :param act_id: The account id
    #     :param part_name: The name of partition
    #     :param BusinessEmail: The email of the user whose id is required
    #     :return: the partiton id in the specified act name
    #     '''
    #     person_id = None
    #     params = self.config.getparams("get_person_detail")
    #     params["accountId"] = act_id
    #     params["partitionId"] = self.get_partition_detail(act_id,part_name)
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "PersonId" in ret.text:
    #         log.info("Successfully retrieved all person info.")
    #     else:
    #         log.error("Could not retrieve all person info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["BusinessEmail"] == BusinessEmail:
    #                     person_id = d["PersonId"]
    #                     break
    #
    #     return int(person_id)
    #
    # def verify_person_detail(self, act_id, part_name,BusinessEmail, ext=None, tn=None):
    #     '''
    #     This function will verify the details of a person.
    #     :param act_id: The account id
    #     :param part_name: The name of partition
    #     :param BusinessEmail: The email of the user whose id is required
    #     :param ext: The extension to be verified
    #     :param tn: The telephone number to be verified
    #     :return: the partiton id in the specified act name
    #     '''
    #     is_ext_correct = True
    #     is_tn_correct = True
    #     params = self.config.getparams("get_person_detail")
    #     params["accountId"] = act_id
    #     params["partitionId"] = self.get_partition_detail(act_id,part_name)
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "PersonId" in ret.text:
    #         log.info("Successfully retrieved all person info.")
    #     else:
    #         log.error("Could not retrieve all person info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if d["BusinessEmail"] == BusinessEmail:
    #                     if ext is not None:
    #                         if d["Extension"] == ext:
    #                             is_ext_correct = True
    #                         else:
    #                             is_ext_correct = False
    #                     if tn is not None:
    #                         if d["Tn"] == "%s (%s) %s-%s"%(tn[0],tn[1:4],tn[4:7],tn[7:]):
    #                             is_tn_correct = True
    #                         else:
    #                             is_tn_correct = False
    #
    #                     break
    #
    #     return is_ext_correct and is_tn_correct
    #
    # def get_cluster_detail(self, cluster_name):
    #     '''
    #     This function will return the id of the cluster.
    #     :param act_id: The account id
    #     :param part_name: The name of partition
    #     :return: the cluster id in the specified act name
    #     '''
    #     cluster_id = None
    #     params = self.config.getparams("get_cluster_detail")
    #     url = params.pop("url")
    #     ret = requests.get(url, data = params, headers = self.headers)
    #     if ret.status_code == 200 and "ClusterStatus" in ret.text:
    #         log.info("Successfully retrieved all cluster info.")
    #     else:
    #         log.error("Could not retrieve cluster info.")
    #     # parsing the returned content to get the id
    #     for loc,details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if str(d["Name"]) == cluster_name:
    #                     cluster_id = d["Id"]
    #                     break
    #
    #     return str(cluster_id)
    #
    # def get_cosmo_component(self, act_id, part_id, componentType=None,id=None):
    #     """
    #     This function will return the data related to a cosmo component
    #     :param act_id: The account id
    #     :param part_id: The name of partition
    #     :param component_type: The name of the component
    #     :return: the data of the cosmo component
    #     """
    #     params = self.config.getparams("get_cosmo_component")
    #     params["componentType"] = componentType
    #     params["accountId"] = act_id
    #     params["partitionId"] = part_id
    #     if id is not None:
    #         params['id'] = id
    #     url = params.pop("url")
    #     ret = requests.post(url, data=params, headers=self.headers)
    #     if ret.status_code == 200 and "data" in ret.text:
    #         log.info("Successfully retrieved the data about specified cosmo component.")
    #     else:
    #         log.error("Could not retrieve the data about specified cosmo component.")
    #     # returning the data related to the cosmo component
    #     return ret.json()
    #
    # def get_vcfe_detail(self, act_id, part_id, comp_name):
    #     """
    #     This function will return the id of a cosmo component
    #     :param act_id: The account id
    #     :param part_id: The name of partition
    #     :return: the data of the cosmo component
    #     """
    #     comp_id = None
    #     params = self.config.getparams("get_vcfe_detail")
    #     params["accountId"] = act_id
    #     params["partitionId"] = part_id
    #     url = params.pop("url")
    #     ret = requests.get(url, data=params, headers=self.headers)
    #     if ret.status_code == 200 and "data" in ret.text:
    #         log.info("Successfully retrieved the data about all cosmo component.")
    #     else:
    #         log.error("Could not retrieve the data about cosmo components.")
    #     # parsing the returned content to get the id
    #     for loc, details in ret.json().iteritems():
    #         if loc == "data":
    #             for d in details:
    #                 if str(json.loads(d["ComponentData"])[0]) == comp_name:
    #                     comp_id = d["ComponentId"]
    #                     break
    #
    #     return str(comp_id)





if __name__ == "__main__":
    # almost all the methods have been modified to accept all the params as keyword args
    # so to call those functions as shown below, the params must be passed as keyword args
    logging.basicConfig(level=logging.DEBUG)
    obj = boss_api()
    # obj = boss_api("17.9.10.454")
    # obj.login(UserName = "Nitin")
    obj.login(url = "http://10.197.145.190/UserAccount/LogOn")
    # print obj.get_account_detail(act_name="AutoTest_Acc_iW53qRaQ")
    # obj.create_tenant(CompanyName="bosswebapi_4")
    # obj.switch_account(act_name="bosswebapi_1")
    # obj.accountId = 12187
    # obj.get_partition_detail(obj.accountId, "HQ1")
    # obj.get_dm_detail("bosswebapi_4","qw@sh.com")
    # obj.add_tn(TnsString="+16462000507",act_name="bosswebapi_4",username="qw@sh.com")
    # obj.update_tn(tnstring="6462000457",Type="Real",State="Available")
    # obj.get_location_detail("12187","loc1")
    # obj.get_partition_detail("11549","MTA")
    # obj.add_location_as_site("location","MTA")
    # new user without profile
    # obj.add_user(part_name="HQ1", Person_FirstName="nn", Person_LastName="kk", Person_BusinessEmail="sh12sh12@aaqsqqassh.com", loc_name="loc1", SU_Email="shi@sh.com")
    # new user with profile
    # obj.add_user(part_name="HQ1",Person_FirstName="nn",Person_LastName="kk",Person_BusinessEmail="sh12@ddqsqqassh.com",loc_name="loc1",SU_Email="shi@sh.com",PhoneType="355",Person_Profile_Extension="1232")
    # obj.add_contract(company_name="bosswebapi_9",file_path="C:\\Users\\nkumar\\Downloads\\SampleContract_1.pdf")
    # obj.get_contract_detail('11618')
    # obj.update_billing_location("bosswebapi_7","location")
    # obj.add_instance_to_contract()
    # obj.validate_location(Address1="Nitin")
    # obj.upload_pdf("C:\\Users\\nkumar\\Downloads\\SampleContract.pdf")
    # obj.get_cluster_detail("MTA")
    # obj.create_partition("location")
    # obj.update_contract_status()
    # obj.get_person_detail("12187","HQ1","sh12@sh.com")
    # obj.change_password("MTA","qw22@sh.com")
    # obj.assign_role("MTA","qw22@sh.com", "Technical")
    # obj.unassign_role("MTA", "qw22@sh.com", "Technical")
    # obj.close_user("MTA", "qw222@sh.com", "Technical")
    # p = obj.get_profile_detail(obj.accountId,"HQ1","sh4@sh.com")
    # obj.get_usergroup_detail("11549","MTA","System VM Only Group")
    # obj.reassign_tn("MTA", "ff@sh.com",reassignExtension="1003")
    # obj.check_extension_availability("MTA","1013")
    # obj.add_tn_to_user(part_name="HQ1",Person_FirstName="abc3",Person_LastName="xyz",Person_BusinessEmail="sh12@bbqsqqassh.com",loc_name="loc1",SU_Email="shi@sh.com",Person_Profile_Extension="1025",Profile_TnId="+16462016017")
    # obj.check_usergroup_availability("HQ1","ug2")
    # to create a user group with different profile id
    # obj.create_usergroup(part_name="HQ1",ug_name="ug4",ProfileTypeId=5)
    # obj.update_usergroup(part_name="HQ1", ug_name="ug4", ProfileTypeId=5,AllowOverheadPaging=True)
    # to create a user group with default profile id
    # obj.create_usergroup("HQ1","ug4")
    # obj.delete_usergroup("HQ1","ug3")
    # obj.check_username_availability("sh33@sh.com")
    # obj.validate_location_name("loc1")
    # obj.add_location("loc1","HQ1")
    # obj.get_suitable_invoice_groups("12033","bosswebapi_1")
    # obj.update_location("loc11","HQ1",Address_Address2="nitin")
    # obj.validate_canclose_location("loc")
    # obj.close_location("loc5","sh@sh.com")
    # obj.get_order_detail(obj.accountId,"loc11")
    # obj.update_order_details("11217")
    # obj.check_mac_address_availability("11:11:11:11:11:11:11:11")
    # obj.add_edit_phone("loc5","11:11:11:11:11:11")
    # obj.remove_phone_entry("11:11:11:11:11:12")
    # obj.add_profile("loc6", "sh@sh.com")
    # obj.validate_assign_profile("aabbb@sh.com")
    # obj.assign_number("+16462000507","1114","haha12@sh.com","loc22","sh@sh.com")
    # obj.unassign_number("aabb@sh.com","HQ1","sh@sh.com")
    # obj.update_cosmo_partition_dialplan()
    # obj.update_cosmo_conference("sh@sh.com")
    # obj.create_cosmo_conference_handler("abc xyz")
    # obj.create_cosmo_conference("sh@sh.com","abc xyz")
    # obj.get_cosmo_conference_detail_handler(obj.accountId,p)
    # obj.delete_cosmo_conference("sh@sh.com","HQ1","sh4@sh.com")
    # print obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1001")
    # print obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", tn="16462000501")
    # print obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1001","16462000501")
    # print obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1002","16462000501")
    # print obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1001", "16462000502")
    # print obj.verify_person_detail(obj.accountId, "HQ1", "sh4@sh.com", "1002")
    # obj.get_cosmo_component("12187", 528)
    # obj.create_auto_attendant(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', aa_name="aa1", aa_extension='1201')
    # obj.get_vcfe_detail('12187', 528, 'nitin')
    # obj.edit_auto_attendant("nitin2", account_name='bosswebapi_2', part_name='BAU', location_name='loc1', aa_name="nitin")
    # obj.delete_auto_attendant("aa1", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # obj.create_hunt_group(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', hg_name="hg1", hg_extension='1114',hg_backup_extn="1001")
    # obj.edit_hunt_group(hg_to_edit="nitin3",account_name='bosswebapi_1', part_name='BAU', location_name='loc1', hg_name="nitin33", hg_extension='1115', hg_backup_extn="1001")
    # obj.delete_hunt_group(hg_to_delete="hg1", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # obj.create_extension_list(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', el_name="el1", el_extns=['1001','1002'])
    # obj.edit_extension_list(el_to_edit="el221", account_name='bosswebapi_1', part_name='BAU', location_name='loc1', el_name="el2",el_extns=['1001'])
    # obj.delete_extension_list(el_to_delete="el1", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
    # obj.create_paging_group(account_name='bosswebapi_1', part_name='BAU', location_name='loc1', pg_name="pg2", pg_extn_list='el1', pg_extension='1004')
    # obj.edit_paging_group(pg_to_edit="pg22", account_name='bosswebapi_1', part_name='BAU', location_name='loc1', pg_name="pg222", pg_extn_list='el1', pg_extension='1004')
    # obj.delete_paging_group(pg_to_delete="pg222", account_name='bosswebapi_1', part_name='BAU', location_name='loc1')
