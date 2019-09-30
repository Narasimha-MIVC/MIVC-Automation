"""
This module provides helping methods to get data from D2.
"""


import sys
import requests
import urllib, base64
import re
import json


class D2API:

    def __init__(self, ip,  username, password):
        print "D2API constructor"
        self.client = requests.session()

        if ":" in ip:
            ip_split = ip.split(":")
            self.ip = ip_split[0]
            self.pno = ip_split[-1]
        else:
            self.ip = ip
            self.pno = '5478'
        self.create_connection(self.ip, self.pno, username, password)

    def create_connection(self, hqIp, pno, username, password):
        """
        """
        # Retrieving the CSRF token
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        LOGIN_URL = 'http://'+hqIp+':'+pno+'/director/login'
        r = self.client.get(LOGIN_URL)  # sets cookie
        # print r.status_code
        try:
            d2_cookie = self.client.cookies['_director2_session']
            csrftoken = urllib.unquote(d2_cookie)
            csrftoken = base64.b64decode(csrftoken)
            csrftoken = re.match('.*_csrf_token.*\"1(.*=).*', csrftoken).group(1)
        except:
            # for upgraded D2 -> Automation support for Rails 4 Upgrade
            csrftoken = re.search(r'meta name="csrf-token" content="([\d\D]+?)"', r.text).group(1)
        self.client.post(LOGIN_URL,data={"user_session[login_name]": username, "user_session[login_password]": password, "authenticity_token": csrftoken})

    def fetch_tenants_info(self):
        """
        """
        LIST_TENANTS_URL = 'http://'+self.ip+':'+self.pno+'/director/tenants/list?_search=false&rows=600'
        result = self.client.get(LIST_TENANTS_URL)
        d = json.loads(result.text)
        tInfo = []
        for device in d['rows']:
            tmpList = [str(device['cell'][0]), str(device['cell'][1]), str(device['cell'][2])]
            tInfo.append(tmpList)
        tInfo.pop(0)
        return tInfo

    def get_specific_tenants(self, tenantNames):
        info = self.fetch_tenants_info()
        specificTenants = []
        tenantNamesList = tenantNames.split(",")
        for tname in tenantNamesList:
            for tinfo in info:
                if tname.lstrip(" '").rstrip("'") == tinfo[0]:
                    specificTenants.append(tinfo)
                    break
        print "ok",specificTenants
        return specificTenants

    def fetch_tenant_specific_sites(self, tenantId):
        tenantId = tenantId.strip()
        sites = []
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + '/director/sites/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22' + \
                             str(tenantId) + r'%22%7D%5D%7D'
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            sites.append(str(userData['cell'][0]))
        print("sites from specific : ", sites)
        return sites

    def fetch_tenant_specific_hunt_group(self, tenantId):
        tenantId = tenantId.strip()
        hunt_group = []
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/hunt_groups/list?list=hunt_group&rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            hunt_group.append((str(userData['id']),str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print("hunt_group from specific : ", hunt_group)
        return hunt_group

    def fetch_tenant_specific_hunt_group_member(self, tenantId, hunt_group_extension):
        hunt_groups = self.fetch_tenant_specific_hunt_group(tenantId)
        for hgmember in hunt_groups:
            if hunt_group_extension==hgmember[2]:
                id = hgmember[0]
                print (id)
                break
        else:
            print("hunt group extension does not match!!")
            return False
        specific_hg_url = 'http://'+self.ip+':'+self.pno+'/director/hunt_groups/'+id+'.json'
        print(specific_hg_url)
        result = self.client.get(specific_hg_url)
        d = json.loads(result.text)
        print(d)
        for key, value in d['hunt_group'].items():
            if key == "selected_hunt_group_members":
                print(value)
                print("hunt group member details : ", value)
                return value
        return False

    def fetch_tenant_specific_pickup_group(self, tenantId):
        tenantId = tenantId.strip()
        pickup_group = []
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/group_pickups/list?rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            pickup_group.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))

        print("pickup_group from specific : ", pickup_group)
        return pickup_group

    def fetch_tenant_specific_auto_attendant(self,tenantId):
        tenantId = tenantId.strip()
        auto_attendant=[]
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/menus/list?rows=1000&_filter_tenant_id=' + str(tenantId) + \
                             r'&_filter_system_tenant_id=' + str(tenantId) + r''
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        for userData in d['rows']:
            auto_attendant.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print("auto_attendant from specific : ", auto_attendant)
        return auto_attendant

    def fetch_tenant_specific_page_group(self,tenantId):
        tenantId = tenantId.strip()
        paging_groups=[]
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/paging_groups/list?rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        for userData in d['rows']:
            paging_groups.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print("auto_attendant from specific : ",paging_groups)
        return paging_groups

    def fetch_tenant_specific_custom_schedule(self, tenantId):
        tenantId = tenantId.strip()
        custom_schedule = []
        LIST_USERS_URL_NEW =r'http://' + self.ip + ':' + self.pno + \
                            '/director/schedules_customs/list?rows=1000&_filter_tenant_id=' + \
                            str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            custom_schedule.append(str(userData['cell'][0]))
        print("custom_schedule from specific : ", custom_schedule)
        return custom_schedule

    def fetch_tenant_specific_holiday_schedule(self, tenantId):
        tenantId = tenantId.strip()
        holiday_schedule = []
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/schedules_holidays/list?rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            holiday_schedule.append((str(userData['cell'][0]), str(userData['cell'][1]), str(userData['cell'][2])))
        print("Holiday schedule from specific : ", holiday_schedule)
        return holiday_schedule

    def fetch_tenant_specific_Extension_List(self,tenantId):
        tenantId = tenantId.strip()
        extension_List=[]
        LIST_USERS_URL_NEW=r'http://' + self.ip + ':' + self.pno + \
                           '/director/extension_lists/list?rows=1000&_filter_tenant_id=' + \
                           str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        for userData in d['rows']:
            extension_List.append(str(userData['cell'][0]))
        print("Extension List from specific : ",extension_List)
        return extension_List

    def fetch_tenant_specific_on_hours_schedule(self, tenantId):
        tenantId = tenantId.strip()
        on_hours_schedule = []
        list_users_url_new = r'http://' + self.ip + ':' + self.pno + \
                             '/director/schedules_on_hours/list?rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        print(list_users_url_new)
        result = self.client.get(list_users_url_new)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            on_hours_schedule.append(str(userData['cell'][0]))
        print("on_hours_schedule from specific : ", on_hours_schedule)
        return on_hours_schedule

    def fetch_tenant_specific_users(self, tenantId):
        tenantId = tenantId.strip()
        user = []
        # LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
        #                      '/director/users/list?&rows=2000&_filter_tenant_id=' + str(tenantId) + r''
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/users/list?&rows=2000&_filter_tenant_id=' + str(tenantId) + r''
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        print(result)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            user.append((str(userData['cell'][4]), str(userData['cell'][2]).split('-')[-1]))
        print("user from specific Tenant : ", user)
        return user, d

    def fetch_tenant_specific_user_groups(self, tenantId):
        tenantId = tenantId.strip()
        ug_List=[]
        LIST_USERS_URL_NEW= r'http://' + self.ip + ':' + self.pno + \
                            '/director/user_groups/list?&rows=1000&_filter_tenant_id=' + str(tenantId) + r''
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        for ugData in d['rows']:
            ug_List.append(str(ugData['cell'][0]))
        print("User Group from specific Tenant: ",ug_List)
        return ug_List

    def fetch_tenant_specific_cost(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        cost_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/costs/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for costData in d['rows']:
                cost_List.append(str(costData['cell'][0]))
            print("COST from specific Tenant: ",cost_List)
            return cost_List

    def fetch_tenant_specific_coscp(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        coscp_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/coscps/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for coscpData in d['rows']:
                coscp_List.append(str(coscpData['cell'][0]))
            print("COSCP from specific Tenant: ",coscp_List)
            return coscp_List

    def fetch_tenant_specific_cosv(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        cosv_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/cosvms/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            #print result
            d = json.loads(result.text)
            #print d
            for cosvData in d['rows']:
                cosv_List.append(str(cosvData['cell'][0]))
            print("COSV from specific Tenant: ",cosv_List)
            return cosv_List

    def fetch_switch_info(self):
        """
        """
        LIST_SWITCH_URL = 'http://' + self.ip + ':5478/dm/status_switches/switch_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        #print d['data']['aaData']
        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[2]), str(device[3]), str(device[5]),str(device[7]),str(device[15]),str(device[16])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_tenant_specific_bridged_call_appearance(self, tenantId):
        tenantId = tenantId.strip()
        Bca = []
        LIST_USERS_URL_NEW = r'http://' + self.ip + \
                             ':5478/director/bridged_call_appearances/list?rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        for userData in d['rows']:
            Bca.append(str(userData['cell'][0]))
        print("BCA from specific Tenant : ", Bca)
        return Bca

    def fetch_tenant_specific_dnis(self, tenantId):
        tenantId = tenantId.strip()
        dnis = []
        LIST_DNIS_MAP = r'http://' + self.ip + \
                        ':5478/director/dnis/list?rows=1000&_filter_tenant_id=' + \
                        str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        result = self.client.get(LIST_DNIS_MAP)
        d = json.loads(result.text)
        for userData in d['rows']:
            dnis.append(str(userData['cell'][1]))
        print("DNIS from specific Tenant : ", dnis)
        return dnis

    def fetch_tenant_specific_moh(self, tenantId):
        tenantId = tenantId.strip()
        moh = []
        LIST_USERS_URL_NEW = r'http://' + self.ip + ':' + self.pno + \
                             '/director/moh_resources/list?&rows=1000&_filter_tenant_id=' + \
                             str(tenantId) + r'&_filter_system_tenant_id=' + str(tenantId) + r''
        print(LIST_USERS_URL_NEW)
        result = self.client.get(LIST_USERS_URL_NEW)
        d = json.loads(result.text)
        print(d)
        for userData in d['rows']:
            moh.append(str(userData['cell'][0]))
        print("Music On Hold from specific : ", moh)
        return moh


    def fetch_tenant_specific_AccountCodes(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        account_codes=[]
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/account_codes/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                account_codes.append(str(userData['cell'][1]))
            print("Account Codes from specific : ",account_codes)
            return account_codes

    def fetch_specific_user_id(self, extn, textn, data):

        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()

        for i in data["rows"]:
            # if i["cell"][0] == first_name and i["cell"][1] == last_name:
            if i["cell"][2] == (str(textn) + "-" + str(extn)):
                return i['id']

        return False

    def fetch_user_detail(self, id):

        URL = 'http://' + self.ip + ':' + self.pno + '/director/users/' + str(id) + ".json"
        result = self.client.get(URL)
        d = json.loads(result.text)
        return d

    def fetch_tenant_specific_phones(self, tenantId):

        URL = r'http://' + self.ip + ':' + self.pno + '/director/ip_phones/list?&rows=1000&filter_tenant_id=' + str(tenantId)
        result = self.client.get(URL)
        d = json.loads(result.text)
        return d

    def fetch_phone_detail(self, tenantId, mac_add):

        URL = r'http://' + self.ip + ':' + self.pno + '/director/ip_phones/list?&rows=1000&filter_tenant_id=' + str(tenantId)
        result = self.client.get(URL)
        d = json.loads(result.text)
        return d

		#Lavanya <start>
    def fetch_im_switch_info(self):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_ims/ucb_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        # print d['data']['aaData']
        sInfo = []
        for device in d['data']['aaData']:
            # print device
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_ip_phone_info(self, phonemac):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_ip_phones/ip_phones_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        #print d

        sInfo = []
        for device in d['data']['aaData']:
            phonemac1=re.sub('[^0-9A-F]+','',str(device[3]))
            if phonemac1 == phonemac:
                tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4]), str(device[5]),
                           str(device[6]), str(device[7]), str(device[8]), str(device[9])]
                sInfo.append(tmpList)
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        return sInfo

    def fetch_audio_web_switch_info(self):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_audio_web_confs/ucb_status_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)

        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4])]
            sInfo.append(tmpList)

        return sInfo

    def fetch_calls_info(self):

        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = r'http://' + self.ip + ':'+self.pno+'/dm/call_quality_reports/call_quality_data'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)

        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[6]), str(device[11])]
            sInfo.append(tmpList)

        return sInfo

    def fetch_call_details(self, call_id):

        """
        """
        # self.create_connection(ip, username, password)
        import pdb
        pdb.Pdb(stdout=sys.__stdout__).set_trace()
        LIST_SWITCH_URL = 'http://' + self.ip + ':'+self.pno+'/dm/call_quality_reports/stream_details?call_guid=' + call_id
        swresult = self.client.get(LIST_SWITCH_URL)
        d1 = json.loads(swresult.text)

        sInfo = []
        for device in d1['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4])]
            sInfo.append(tmpList)

        return sInfo

    def fetch_switch_specific_call_info(self):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = r'http://' + self.ip + ':'+self.pno+'/dm/status_audio_web_confs/ucb_calls_list'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        # print d['data']['aaData']
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()

        sInfo = []
        for device in d['data']['aaData']:
            # print device
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4]), str(device[5]), str(device[6]),
                       str(device[7]), str(device[8]), str(device[9])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_ip_phone_specific_call_info(self, phonemac):
        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = r'http://' + self.ip + ':'+self.pno+'/dm/status_ip_phones/ip_phone_calls_list?mac_address=' + phonemac + r''
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)
        #print d['data']['aaData']

        sInfo = []
        for device in d['data']['aaData']:
            # print device
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[4]), str(device[5]), str(device[6]),
                       str(device[7]), str(device[8]), str(device[9])]
            sInfo.append(tmpList)
        return sInfo
#Lavanya <end>

#Maha <Start>

    def add_did_ranges(self,trunkgrpid, basephno, nophonenum):
        ADD_URL='http://'+self.ip+':'+self.pno+'/director/did_ranges.json'
        JSON_DATA={ "did_range":{"NumPhoneNumbers":nophonenum,"TrunkGroupID":trunkgrpid,"base_phone_number_input_formatted":basephno,"site_id":1,"num_of_digits_from_co":12}}

        result = self.client.post(ADD_URL,json=JSON_DATA)
        d = json.loads(result.text)
        return d

    def get_did_ranges(self):
        GET_URL='http://'+self.ip+':'+self.pno+'/director/did_ranges/list'

																															 
        result = self.client.get(GET_URL)
        d = json.loads(result.text)
        return d

    def delete_did_ranges(self,didrangeid):
        DELETE_URL='http://'+self.ip+':'+self.pno+'/director/did_ranges/'+didrangeid+'.json'

																															 
        result = self.client.delete(DELETE_URL)
        d = json.loads(result.text)
        return d

    def add_trunk_groups(self,trunkgrpname, destinationdn):
        ADD_URL='http://'+self.ip+':'+self.pno+'/director/trunk_groups.json'
        JSON_DATA={"collections":{"countries":[]},"trunk_group":{"AccessCode":"T","AreaCode":"408","TenantID":1,"TrunkGroupName":trunkgrpname,"TrunkTypeID":6,"SiteID":1,"TS911":"true","num_digits_from_co":"12","destination_dn_formatted":destinationdn,"Outgoing":"true"},"new_tg":"false","$resolved":"true","new_record":"true"}

        result = self.client.post(ADD_URL,json=JSON_DATA)
        d = json.loads(result.text)
        return d
			 

    def get_trunk_groups(self):
        GET_URL='http://'+self.ip+':'+self.pno+'/director/trunk_groups/list'

        result = self.client.get(GET_URL)
        d = json.loads(result.text)
        return d
							   

    def delete_trunk_groups(self,trunkgrpid):
        DELETE_URL='http://'+self.ip+':'+self.pno+'/director/trunk_groups/'+trunkgrpid+'.json'

        result = self.client.delete(DELETE_URL)
        d = json.loads(result.text)
        return d

#Maha <End>

#Neeraj <Start>
    def fetch_site_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        LIST_SITE_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_sites/site_status_list'
        siteresult = self.client.get(LIST_SITE_URL)
        d = json.loads(siteresult.text)
        # print d['data']['aaData']
        sInfo = []
        for device in d['data']['aaData']:
            # print device
            tmpList = [str(device[1]), str(device[4]), str(device[12])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_server_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        LIST_SERVER_URL = 'http://' + self.ip + ':'+self.pno+'/dm//status_servers/server_status_list'
        srresult = self.client.get(LIST_SERVER_URL)
        d = json.loads(srresult.text)
        # print d['data']['aaData']
        sInfo = []
        for device in d['data']['aaData']:
            # print device
            tmpList = [str(device[1]), str(device[2]), str(device[3]), str(device[5]), str(device[6]), str(device[7])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_ipphone_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        LIST_IPPHONE_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_ip_phones/ip_phones_status_list'
        ipphoneresult = self.client.get(LIST_IPPHONE_URL)
        d = json.loads(ipphoneresult.text)
        print d
        # print d['data']['aaData']
        sInfo = []
        for device in d['data']['aaData']:
            # print device
            tmpList = [str(device[1]), str(device[5]), str(device[6]), str(device[8]), str(device[9]), str(device[11]),
                       str(device[12]), str(device[20])]
            sInfo.append(tmpList)
        return sInfo

    def fetch_voicemail_server_info(self):
        VOICEMAIL_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_voice_mail_servers/vm_server_status_list'
        result = self.client.get(VOICEMAIL_URL)
        json_result = json.loads(result.text)
        vm_server_info = []
        for vm_row in json_result['data']['aaData']:
            tmpList = [str(i) for i in vm_row]
            vm_server_info.append(tmpList)
        return vm_server_info

    def fetch_trunk_group_info(self):
        Trunk_Groups_URL = 'http://' + self.ip + ':'+self.pno+'/dm/status_trunk_groups/trunk_groups_status_list'
        result = self.client.get(Trunk_Groups_URL)
        json_result = json.loads(result.text)
        trunk_group_list = []
        for tg_row in json_result['data']['aaData']:
            tmpList = [str(i) for i in tg_row]
            trunk_group_list.append(tmpList)
        return trunk_group_list

    def fetch_make_me_conf_info(self):
        make_me_conf_url = 'http://' + self.ip + ':'+self.pno+'/dm/status_site_confs/conf_switch_status_list'
        result = self.client.get(make_me_conf_url)
        json_result = json.loads(result.text)
        conf_switch_info = []
        for conf_row in json_result['data']['aaData']:
            tmpList = [str(i) for i in conf_row]
            conf_switch_info.append(tmpList)
        return conf_switch_info
#Neeraj <End>

    def fetch_calls_info(self):

        """
        """
        # self.create_connection(ip, username, password)

        LIST_SWITCH_URL = r'http://' +self.ip+':'+self.pno+'/dm/call_quality_reports/call_quality_data'
        swresult = self.client.get(LIST_SWITCH_URL)
        d = json.loads(swresult.text)

        sInfo = []
        for device in d['data']['aaData']:
            tmpList = [str(device[1]), str(device[2]), str(device[6]), str(device[11])]
            sInfo.append(tmpList)

        return sInfo

    def fetch_phone_info(self, mac, AccName):
        """
        """
        # self.create_connection(ip, username, password)
        #import pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        tenantNames = AccName
        tList = self.get_specific_tenants(tenantNames)
        dnis = []
        for tenant in tList:
            #LIST_DNIS_MAP = r'http://'+self.ip+':5478/director/dnis/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''

            LIST_SWITCH_URL = r'http://' + self.ip + ':5478/director/ip_phones/list?_search=false&sidx=&sord=asc&_filter_tenant_id=' + str(tenant[1])+ '&_filter_system_tenant_id=' +str(tenant[1])+r''
            result = self.client.get(LIST_SWITCH_URL)
            d1 = json.loads(result.text)
            n_rows = d1["records"]
            print n_rows
            ph = []
            import re
            for x in range(n_rows):
                d1["rows"][x]["cell"][0]=re.sub("-", "", d1["rows"][x]["cell"][0])
                if d1["rows"][x]["cell"][0]==mac:
                    tmplist= d1["rows"][x]["id"]
                    ph.append(tmplist)
                    tmplist= d1["rows"][x]["cell"][2][1]
                    ph.append(tmplist)
                    print ph
        return ph


    def fetch_switch_status_D2(self, switch_name):
        #import pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        URL = 'http://' +self.ip+ ':5478/dm/status_switches/switch_status_list?'
        result = self.client.get(URL)
        jresult = json.loads(result.text)
        print jresult
        n_rows = jresult["data"]["iTotalRecords"]
        #print n_rows
        p = []
        for x in range(n_rows):
            if jresult["data"]["aaData"][x][2]==switch_name:
                tmplist = jresult["data"]["aaData"][x][7]
                p.append(tmplist)
                tmplist = jresult["data"]["aaData"][x][18]
                p.append(tmplist)
        for x in range(n_rows):
            if jresult["data"]["aaData"][x][3]=='vPhone' and jresult["data"]["aaData"][x][2]!=switch_name and  jresult["data"]["aaData"][x][7]=='In Service':
                tmplist = jresult["data"]["aaData"][x][2]
                p.append(tmplist)
                tmplist = jresult["data"]["aaData"][x][18]
                p.append(tmplist)
                break
        print p
        return p


    def change_ipphone_switch(self,phoneid,switchid):
        URL ='http://' +self.ip+ ':5478/director/ip_phones/move.json?ids=' +phoneid+ '&site_id=3&switch_id=' +switchid
        JSON_DATA = {}
        result = self.client.post(URL,json=JSON_DATA)
        jresult = json.loads(result.text)
        print jresult
        return True

#Maha - New TC

    def fetch_system_extn_info(self):
        """
        """
        # self.create_connection(ip, username, password)
        LIST_SYSTEM_EXTN_URL = 'http://' + self.ip + ':'+self.pno+'/director/system_extensions.json'
        systemextnresult = self.client.get(LIST_SYSTEM_EXTN_URL)

        d = json.loads(systemextnresult.text)
        return d

    def fetch_build_info(self):
        from bs4 import BeautifulSoup
        url = 'http://' + self.ip + ':5478/dm/monitoring_service'
        result = self.client.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        var = soup.find_all("script", type="text/javascript")

        for x in var:
            if x.contents:
                var2 = x.text
                var2 = var2.encode('ascii', 'ignore')
                var3 = var2[var2.find('aaData') + 13: var2.find(',1]]')]
                var3 = var3.replace('\\"', ' ')
                res = var3.split(',')
                return res
        null = []
        return null

    def fetch_system_details(self):
        from bs4 import BeautifulSoup
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        url = 'http://' + self.ip + ':5478/dm/status_system'
        result = self.client.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        var1 = soup.find_all("script", type="text/javascript")
        var2 = var1[4].text
        var2 = var2.encode('ascii', 'ignore')
        var3 = var2[var2.find('aaData') + 10: var2.find(']}')]
        var3 = var3.replace('\\"', ' ')
        l1 = (var3[:var3.find('],') + 1]).split(',')
        l2 = (var3[var3.find('],') + 1:]).split(',')
        var1 = soup.find_all("button", id="backup_db_command_button", type="button")
        var4 = var1[0].text
        var4 = (var4.encode('ascii', 'ignore')).strip()
        return l1, l2, var4

if __name__ == "__main__":
    # import pdb
    # pdb.Pdb(stdout=sys.__stdout__).set_trace()

    fo = D2API("10.196.7.180", "admin@pta.com", "Shoreadmin1#")
    # t=fo.fetch_tenant_specific_cosv("MT_PTA_ACC1")
    # t = fo.fetch_tenants_info()
    # print t

    t2=fo.get_specific_tenants("MT_PTA_ACC1")

    print "#######",t2
    tid = t2[0][1]
    textn = t2[0][2]
    print "tenant id is :", tid

    x,user_info = fo.fetch_tenant_specific_users(tid)
    print "##user info is ##",user_info




    # user_id= fo.fetch_specific_user_id("4423", textn, user_info)
    # print "##user id is ##", user_id
    #
    # user_detail= fo.fetch_user_detail(user_id)
    # print "##user detail ##", user_detail
    # mac_add = user_detail['user']['current_port_display']
    #
    # tel = fo.fetch_phone_detail(tid, mac_add)
    #
    # print "## phone detail ##"
    # print tel



    #f1 = D2API("10.198.107.144", "admin@pre.com", "changeme")
    #t = f1.fetch_tenant_specific_cosv("VQD_TestAccount1")
    #print ("cos info:", t)