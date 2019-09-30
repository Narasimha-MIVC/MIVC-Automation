"""Director Portal Module
"""
import time
import sys
import stafenv
from D2API import D2API

_DEFAULT_TIMEOUT = 2

class DirectorComponent(object):
    """Component class for the director
    """
    def director_client_login(self, **params):
        """
        This function will login to D@ portal
        :param params:
        :return:
        """
        if params.keys():
            self.director = D2API(params["IP"], params["username"], params["password"])
        else:
            print("Please check that the input parameters have been provided")


    def director_verify_tenant_location(self, **params):
        """
        This function will verify the location created for tenant
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                location_list = self.director.fetch_tenant_specific_sites(params["account"])
                if location_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving the location from D2 failed!")
                return False

            for location in location_list:
                if params["exp_location"] in location:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_emergency_hunt_group(self, **params):
        """
        This function will verify the emergency hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                HG_list = self.director.fetch_tenant_specific_hunt_group(params["newacc"])
                if HG_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving HG from D2 failed!!")
                return False

            for id, hg, extn in HG_list:
                if hg == params["exp_huntgroup"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_hunt_group(self, **params):
        """
        This function will verify the hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                HG_list = self.director.fetch_tenant_specific_hunt_group(params["newacc"])
                if HG_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving the hunt group from D2 failed !!")
                return False

            for id, hg, extn in HG_list:
                if hg == params["exp_huntgroup"] and extn == params["hg_extn"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_hunt_group_member(self, **params):
        """
        This function will verify the hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                hunt_group_members = self.director.fetch_tenant_specific_hunt_group_member(params["newacc"], params["hg_extn"])
                if hunt_group_members:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving the HG member list from D2 Failed!!")
                return False
            for hgmem in hunt_group_members:
                print hgmem
                if hgmem['id'].split('-')[-1] == params["hgmember"]:
                    memid = hgmem['id'].split('-')[-1]
                    print "Group Member id :" +memid+ " is found"
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_Extension_List(self, **params):
        """
        This funtion will veirfy the paging group in D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                Ex_list = self.director.fetch_tenant_specific_Extension_List(params["newacc"])
                if Ex_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving Extension list from D2 Failed!!")
                return False

            for extnName in Ex_list:
                if extnName == params["exp_D2extensionList"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_pickup_group(self, **params):
        """
        This func will verify pick group from D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                PG_list = self.director.fetch_tenant_specific_pickup_group(params["newacc"])
                if PG_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving the pick up group from D2 Failed!!")
                return False
            for pg, extn in PG_list:
                if pg == params["exp_pickupgroup"] and extn == params["pk_extn"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_auto_attendant(self, **params):
        """
        Verify the Auto Attendant in D2 page
        :param params:  ditionary contain auto attendant information
        :return:
        """
        if params.keys():
            for count in xrange(2):
                AA_list = self.director.fetch_tenant_specific_auto_attendant(params["newacc"])
                if AA_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving auto attendant list from D2 Failed !!")
                return False

            for aa, extn in AA_list:
                print(aa, extn)
                if aa == params["Aa_Name"] and extn==params["Aa_Extension"] :
                    print("Match Found")
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_custom_schedule(self, **params):
        """
        Verification of custom schedle in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            for count in xrange(2):
                cs_list = self.director.fetch_tenant_specific_custom_schedule(params["newacc"])
                if cs_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving CS list from D2 Failed!!")
                return False

            for cs in cs_list:
                if cs == params["exp_customschedule"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_paging_group(self,**params):
        """
        Verify the paging group in D2 page
        :param params:  Dictionary of paging group  information
        :return:
        """
        if params.keys():
            for count in xrange(2):
                Pg_list = self.director.fetch_tenant_specific_page_group(params["newacc"])
                if Pg_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving Paging group list from D2 Failed!!")
                return False
            for pg, extn in Pg_list:
                if pg == params["Pg_Name"] and extn==params["Pg_Extension"] :
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_holiday_schedule(self, **params):
        """
        Verification of holiday schedule in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            for count in xrange(2):
                HS_list = self.director.fetch_tenant_specific_holiday_schedule(params["newacc"])
                if HS_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving Holiday Schedule list from D2 Failed!!")
                return False
            for hs, date, timezone in HS_list:
                if hs == params["exp_holidayschedule"] and date == params["exp_date"] and timezone == params["exp_timezone"]:
                    print "Holiday schedule name: ", hs
                    print "Holiday schedule day date: ", date
                    print "Holiday schedule timezone: ", timezone
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_on_hours_schedule(self, **params):
        """
        Verification of on hours schedule in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            for count in xrange(2):
                ohs_list = self.director.fetch_tenant_specific_on_hours_schedule(params["newacc"])
                if ohs_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving Hours schedule list from D2 failed!!")
                return False

            for ohs in ohs_list:
                if ohs == params["exp_on_hours_schedule"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_bridged_call_appearance(self, **params):
        '''
        Description: Verify the Bridged call appearance created in BOSS is reflected in D2
        param: params contains D2 information
        return: status True/False
        Created by: Immani Mahesh Kumar
        Modified by: Prasanna
        '''

        if params.keys():
            for count in xrange(2):
                bca_list = self.director.fetch_tenant_specific_bridged_call_appearance(params["newacc"])
                if bca_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Fetching BCA info from D2 failed!")
                return False

            for bca in bca_list:
                if params["exp_Bca"] in bca:
                    return True
        else:
             print("Please check that the input parameters have been provided")
        return False

    def director_fetch_and_verify_dnis(self, **params):
        '''
        Description: fetch and verify the DNIS associated with BCA/aBCA from D2
        param: params contains D2 information
        return: status True/False
        Created by: Prasanna
        '''

        if params.keys():
            for count in xrange(2):
                dnis_list = self.director.fetch_tenant_specific_dnis(params["tenant"])
                if dnis_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Fetching dnis list from D2 failed!")
                return False
            test_data = "".join(str(params["dnis"]).split(" "))
            test_data = test_data[1:] if "++" in test_data else test_data
            print(test_data)
            for dnis in dnis_list:
                if dnis == test_data:
                    return True
        else:
             print("Please check that the input parameters have been provided")
        return False

    def director_verify_user_groups(self, **params):
        """
        This function will verify the user group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                ug_list = self.director.fetch_tenant_specific_user_groups(params["newacc"])
                if ug_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving user groups list from D2 failed !!")
                return False
            for ug_name in ug_list:
                if ug_name.split('-')[0] == params["exp_user_group"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_moh(self, **params):
        """
        This function will verify the hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            for count in xrange(2):
                moh_list = self.director.fetch_tenant_specific_moh(params["newacc"])
                if moh_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving MOH list from D2 failed!!")
                return False
            for moh_dec in moh_list:
                if moh_dec == params["exp_mohdec"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_users(self, **params):
        '''
        `Description:`   This function will verify the user location in D2 page

        `Param:` : Dictionary contains user information

        `Returns: ` status - True/False

        `Created by:` Palla Surya Kumar
        '''
        if params.keys():
            for count in xrange(2):
                u_list = self.director.fetch_tenant_specific_users(params["newacc"])
                if u_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Retrieving users list from D2 Failed!!")
                return False
            for u_name in u_list:
                if u_name[0] == params["exp_user_email"] and u_name[1] == params["extn"]:
                    return True
        else:
            print("Please check that the input parameters have been provided")
        return False

    def director_verify_tenant_uuid(self, accounts_ids=None, tenants_names=None):
        '''
        Description: Verify the tenant uuid in D2
        account_id: the account id
        tenants_names:
        return: status True/False
        Created by: Prasanna Kumar Tripathy
        '''

        if accounts_ids and tenants_names:
            for count in xrange(2):
                tenants_list = self.director.get_specific_tenants(tenants_names)
                if tenants_list:
                    break
                time.sleep(_DEFAULT_TIMEOUT)
            else:
                print("Fetching from D2 failed!")
                return False

            ids = accounts_ids.split(',')
            return False if accounts_ids != [i for i, j in zip(ids, tenants_list) if i in j] else True
        else:
            print("Please check that the input parameters have been provided")
            return False
