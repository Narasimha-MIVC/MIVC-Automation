import sys
import requests
import urllib, base64
import re
import json

class D2API():

    def __init__(self, ip,  username, password):
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
        # Retrieve the CSRF token first
        LOGIN_URL = 'http://'+hqIp+':'+pno+'/director/login'
        self.client.get(LOGIN_URL)  # sets cookie
        d2_cookie = self.client.cookies['_director2_session']
        ##print d2_cookie
        csrftoken = re.match('(.+)--',d2_cookie).group(1)
        ##print csrftoken
        csrftoken = urllib.unquote(d2_cookie)
        ##print csrftoken
        csrftoken = base64.b64decode(csrftoken)
        # csrftoken = r'{I"session_id:EFI"%8cb0cc7d1645b236e217e3e35826b9dd; TI"abc; F{:	hostI"localhost; FI"_csrf_token; FI"1lC0TGuAk9D6C0f68Fy9T8UsQ0RaQg9uXiTRnPra+iLE=; F'
        ##print csrftoken
        # csrftoken = re.match('.*_csrf_token.*1(.*=).*', csrftoken).group(1)
        csrftoken = re.match('.*_csrf_token.*\"1(.*=).*', csrftoken).group(1)
        ##print csrftoken

        # 'admin@mt.com', 'changeme'
        self.client.post(LOGIN_URL,data={"user_session[login_name]": username, "user_session[login_password]": password, "authenticity_token": csrftoken})
        # r = client.get(LIST_SWITCH_URL)


    def fetch_tenants_info(self):
        """
        """
        #self.create_connection(ip, username, password)
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

    def get_specific_tenants(self, tenantNames):
        info = self.fetch_tenants_info()
        specificTenants = []
        tenantNamesList = tenantNames.split(",")
        for tname in tenantNamesList:
            for tinfo in info:
                if tname.lstrip(" '").rstrip("'") == tinfo[0]:
                    print("matched")
                    specificTenants.append(tinfo)
                    break
        print "ok",specificTenants
        return specificTenants

    def fetch_tenant_specific_sites(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames)
        sites = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/sites/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22'+str(tenant[1])+r'%22%7D%5D%7D'
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                sites.append(str(userData['cell'][0]))
        print "sites from specific : ", sites
        return sites

    def fetch_tenant_specific_hunt_group(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        hunt_group = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/hunt_groups/list?list=hunt_group&rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                hunt_group.append((str(userData['id']),str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print "hunt_group from specific : ", hunt_group
        return hunt_group

    def fetch_tenant_specific_hunt_group_member(self, tenantNames, hunt_group_extension):

        hunt_groups = self.fetch_tenant_specific_hunt_group(tenantNames)
        #hunt_group_member = []
        id=0
        for hgmember in hunt_groups:
            if hunt_group_extension==hgmember[2]:
                id = hgmember[0]
                print (id)
                break
        specific_hg_url = 'http://'+self.ip+':'+self.pno+'/director/hunt_groups/'+id+'.json'
        print specific_hg_url
        result = self.client.get(specific_hg_url)
        d = json.loads(result.text)
        print d
        for key, value in d['hunt_group'].items():
            if key == "selected_hunt_group_members":
                print(value)
                print "hunt group member details : ", value
                return value
        return False

    def fetch_tenant_specific_pickup_group(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        # LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        pickup_group = []
        for tenant in tList:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/group_pickups/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                pickup_group.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print "pickup_group from specific : ", pickup_group
        return pickup_group

    def fetch_tenant_specific_auto_attendant(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        auto_attendant=[]
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/menus/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            #print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            #print(d)
            for userData in d['rows']:
                auto_attendant.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
            print("auto_attendant from specific : ", auto_attendant)
            return auto_attendant

    def fetch_tenant_specific_page_group(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        paging_groups=[]
        for tenant in tList:
            #LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/paging_groups/list?_search=true&nd=1495616642261&rows=50&page=1&sidx=&sord=asc&filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%'+str(tenant[1])+r'%22%7D%5D%7D'
            LIST_USERS_URL_NEW = r'http://'+self.ip+':'+self.pno+'/director/paging_groups/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                paging_groups.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
            print("auto_attendant from specific : ",paging_groups)
            return paging_groups

    def fetch_tenant_specific_custom_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        custom_schedule = []
        for tenant in tList:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            LIST_USERS_URL_NEW =r'http://'+self.ip+':'+self.pno+'/director/schedules_customs/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                custom_schedule.append(str(userData['cell'][0]))
        print "custom_schedule from specific : ", custom_schedule
        return custom_schedule

    def fetch_tenant_specific_holiday_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        holiday_schedule = []
        for tenant in tList:
            LIST_USERS_URL_NEW =r'http://'+self.ip+':'+self.pno+'/director/schedules_holidays/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                holiday_schedule.append((str(userData['cell'][0]), str(userData['cell'][1]), str(userData['cell'][2])))
        print "Holiday schedule from specific : ", holiday_schedule
        return holiday_schedule

    def fetch_tenant_specific_Extension_List(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        extension_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/extension_lists/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                extension_List.append(str(userData['cell'][0]))
            print("Extension List from specific : ",extension_List)
            return extension_List

    def fetch_tenant_specific_on_hours_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        # LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        on_hours_schedule = []
        for tenant in tList:
            list_users_url_new = r'http://' + self.ip + ':'+self.pno+'/director/schedules_on_hours/list?rows=1000&_filter_tenant_id=' + str(
                tenant[1]) + r'&_filter_system_tenant_id=' + str(tenant[1]) + r''
            print list_users_url_new
            result = self.client.get(list_users_url_new)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                on_hours_schedule.append(str(userData['cell'][0]))
        print "on_hours_schedule from specific : ", on_hours_schedule
        return on_hours_schedule

    def fetch_tenant_specific_users(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':'+self.pno+'/director/users/list'
        user = []
        for tenant in tList:
            LIST_USERS_URL_NEW =r'http://'+self.ip+':'+self.pno+'/director/users/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            print result
            d = json.loads(result.text)
            print d

            for userData in d['rows']:
                user.append((str(userData['cell'][4]), str(userData['cell'][2]).split('-')[-1]))
        print "user from specific Tenant : ", user
        return user

    def fetch_tenant_specific_user_groups(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        ug_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':'+self.pno+'/director/user_groups/list?&rows=1000&_filter_tenant_id='+str(tenant[1])+r''
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



if __name__ == "__main__":
    fo = D2API("10.198.107.66", "admin1@mitel.com", "changeme")
    t=fo.fetch_tenant_specific_cosv("autumation_kumar")
    print ("cos info:",t)