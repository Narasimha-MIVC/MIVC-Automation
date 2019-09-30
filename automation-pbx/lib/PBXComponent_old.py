"""Director Portal Module
"""
import re
import os
import time
import sys

import stafenv
from D2API import D2API
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger

_DEFAULT_TIMEOUT = 3

class PBXComponent(object):
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

    def director_verify_switch_status(self, **params):
        """
        Verification of switch status in D2 page
        :param params:
        :return: status
        """

        if params.keys():
            ohs_list = self.director.fetch_switch_info()
            flag=0
            for ohs in ohs_list:
                #print ohs
                for app in params["applianceIP"]:
                    if ohs[1] == params["appliance"]:
                        if ohs[2] == app:
                            if ohs[3] in params["status"]:
                                print "Appliance : %s with IP %s status is %s" %(ohs[1], ohs[2], ohs[3])
                                flag=flag+1
                            else:
                                print "STATUS FAILED  Appliance : %s with IP %s  Current status is %s \n  Expected is %s" % (ohs[1], ohs[2], ohs[3],params["status"])

            if flag == len(params["applianceIP"]):
                     return True
            else:
                    return False
        else:
            print("Please check that the input parameters have been provided")

        # Neeraj <Start>

    def director_verify_site_status(self, **params):
        """
        Description: Verify the audio/web conferencing switch parameters.
        Param: params: Dictionary contains audio/web conferencing switch information
        Returns:  audio/web switch state
        Created by: Neeraj Narwaria
        Modified by:   Lavanya Nagaraj  30-01-2019

        """
        try:
            if params.keys():
                ohs_list = self.director.fetch_site_info()
                # import pdb
                # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                for ohs in ohs_list:
                    if ohs[0] == params["siteName"]:
                        if ohs[1] == params["siteStatus"]:
                            return True
                        else:
                            print("Site " + params["siteName"] + " is not in service")
                            return False
                print("Site " + params["siteName"] + " not found")
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Verify site status failed")
            return False

    def director_verify_server_status(self, **params):
        """
        Verification of switch status in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            ohs_list = self.director.fetch_server_info()
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            flag=0
            for ohs in ohs_list:
                #print ohs
                for app in params["applianceIP"]:
                    if ohs[2] == params["appliance"] and ohs[1] == app and ohs[4] in params["status"]:
                        print "Appliance : %s with IP %s status is %s" %(ohs[2], ohs[1], ohs[4])
                        flag=flag+1
            if flag == len(params["applianceIP"]):
                     return True
            else:
                    return False
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_voicemail_server_info(self, **params):
        """
        Description: Verify the Voice mail server parameters.
        Param: params: Dictionary contains voicemail server information
        Returns:  voicemail server state
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            if params.keys():
                vm_server_list = self.director.fetch_voicemail_server_info()
                for vm_info in vm_server_list:
                    vm_info = vm_info[2:7]
                    if vm_info[0] in params['vm_server']:
                        if vm_info[1] in params['vm_server_ip']:
                            if vm_info[2] == params['site']:
                                if vm_info[3] >= params['mailbox_count']:
                                    if vm_info[4] >= params['messages']:
                                        return True
                                    else:
                                        print("Message count for " + params['vm_server'] + "is less than expected")
                                        print("Current count: " + vm_info[4] + " Expected count: " + params['messages'])
                                else:
                                    print("Mailbox count for " + params['vm_server'] + "is less than expected")
                                    print("Current count: " + vm_info[3] + " Expected count: " + params[
                                        'mailbox_count'])
                            else:
                                print("Site for " + params['vm_server'] + "did not match")
                                print("Current site: " + vm_info[2] + " Expected count: " + params['site'])
                        else:
                            print("IP Address for " + params['vm_server'] + "did not match")
                            print("Current IP Address: " + vm_info[1] + " Expected count: " + params['vm_server_ip'])

                print("Requested VM server " + params['vm_server'] + "not found.")
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Verify voice mail server failed")
            return False

    def director_verify_trunk_groups_status(self, **params):
        """
        Description: Verification of trunk groups status in D2 page
        Param: params: trunk group details
        Returns:  trunk group state
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                trunk_group_list = self.director.fetch_trunk_group_info()
                for trunk_group in trunk_group_list:
                    trunk_group = trunk_group[2:7]
                    print trunk_group
                    if trunk_group[0] == params['Trunk'] and trunk_group[1] == params['TrunkType']:
                        if trunk_group[2] == params['site']:
                            if trunk_group[3] == (params['TrunkInUse'] + "/0"):
                                if trunk_group[4] == (params['TrunkInService'] + "/0"):
                                    return True
                                else:
                                    print("Trunk is not in service")
                                    return False
                            else:
                                print("Number of trunks in use did not match")
                                return False
                        else:
                            print("Trunk group site did not match")
                            print("Current site: " + trunk_group[2] + " Expected site: " + params['site'])
                print("Requested Trunk group not found")
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("trunk group status verification failed")
            return False

    def director_verify_make_me_conferencing(self, **params):
        """
        Description: Verify the make conferencing switch parameters.
        Param: params: Dictionary contains make me conferencing switch name and type
        Returns:   switch state
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019

        """
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            if params.keys():
                make_me_conf_list = self.director.fetch_make_me_conf_info()
                for conf_info in make_me_conf_list:
                    conf_info = conf_info[:6]
                    if conf_info[0] in params['switch'] and conf_info[1] in params['type'] and conf_info[2] in params[
                        'ip_address']:
                        if conf_info[3] == params['active_calls'] and conf_info[4] == params['in_use_ports']:
                            if conf_info[5] == params['free_ports']:
                                return True
                            else:
                                print("Free ports did not match for " + conf_info[0])
                                print("Current ports: " + conf_info[5] + " Expected free ports: " + params[
                                    'free_ports'])
                        else:
                            print("In use active calls, ports did not match for " + conf_info[0])
                            print("Current ports: " + conf_info[4] + " Expected free ports: " + params['in_use_ports'])
                    else:
                        print("Could not find " + conf_info[0])
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Verify make me conference switch status failed")
            return False

    def director_get_did_ranges(self, **params):
        """
        Description:get DID ranges
        Param: params: trunkid, basephno, noofphones
        Returns:   did range id
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                did_ranges_list = self.director.get_did_ranges()
                for did_ranges in did_ranges_list['rows']:
                    if str(did_ranges['cell'][0]) == params['trunkgrpname'] and str(did_ranges['cell'][1]) == params[
                        'basephno'] and str(did_ranges['cell'][2]) == params['noofphones']:
                        return str(did_ranges['id'])
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("getting did range from D2 failed")
            return False

    def director_add_did_ranges(self, **params):
        """
        Description:Add DID ranges in D2 page
        Param: params: trunkid, basephno, noofphones
        Returns:   status
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                did_ranges_list = self.director.add_did_ranges(params['trunkid'], params['basephno'],
                                                               params['noofphones'])
                if str(did_ranges_list['did_range']['TrunkGroupID']) == params['trunkid']:
                    if str(did_ranges_list['did_range']['base_phone_number_input_formatted']) == params['basephno']:
                        if str(did_ranges_list['did_range']['NumPhoneNumbers']) == params['noofphones']:
                            return True
                        else:
                            print("Number of phone numbers is not as expected")
                            print("Current value: " + str(
                                did_ranges_list['did_range']['NumPhoneNumbers']) + " Expected value: " + params[
                                      'noofphones'])
                    else:
                        print("Base phone number is not as expected")
                        print("Current value: " + str(
                            did_ranges_list['did_range']['base_phone_number_input_formatted']) + " Expected value: " +
                              params['basephno'])
                else:
                    print("Added did ranges trunk group ID does not match")
                    print("Current value: " + str(did_ranges_list['did_range']['TrunkGroupID']) + " Expected value: " +
                          params['trunkid'])

                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("DID range addition failed")
            return False

    def director_delete_did_ranges(self, **params):
        """
        Description:Delete DID ranges in D2 Page
        Param: params: didrangesID, description
        Returns:  status
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            plainbasephno = "+" + re.sub('[^0-9]+', '', params['basephno'])
            if params.keys():
                did_ranges_list = self.director.delete_did_ranges(params['didrangesID'])
                for did_ranges in did_ranges_list['deleted']:
                    if str(did_ranges['id']) == params['didrangesID']:
                        if str(did_ranges['description']) == plainbasephno:
                            return True
                        else:
                            print("Base Phone number did not match for given range")
                print("Did range with given trunkid and destinationdn not found")
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Deletion of DID range failed")
            return False

    def director_get_trunk_groups(self, **params):
        """
        Description: get Trunk groups from D2 page
        Param: params: trunkgrpName
        Returns:  Trunk_grp_id
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                trunk_grp_list = self.director.get_trunk_groups()
                for trunk_grp in trunk_grp_list['rows']:
                    if str(trunk_grp['cell'][0]) == params['trunkgrpName']:
                        return str(trunk_grp['id'])
                print("Provided trunk group not found")
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Verify of trunk group failed")
            return False

    def director_add_trunk_groups(self, **params):
        """
        Description: Add trunk group in D2
        Param: params: Trunk group name and  destination
        Returns:  return trunk group creation state
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                trunk_groups_list = self.director.add_trunk_groups(params['trunkgrpname'], params['destinationdn'])
                if str(trunk_groups_list['trunk_group']['TrunkGroupName']) == params['trunkgrpname']:
                    if str(trunk_groups_list['trunk_group']['destination_dn_formatted']) == params[
                        'destinationdn'] + ' : Default':
                        return True
                    else:
                        print("Created Trunkgroup destination is not as expected")
                        return False
                else:
                    print("Created Trunkgroup name is not as expected")
                    return False
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Adding trunk group failed")
            return False

    def director_delete_trunk_groups(self, **params):
        """
        Description: delete trunk group in D2
        Param: params: Trunk group name and  destination
        Returns:  status
        Created by: Mahabaleshwar Hegde
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                trunk_groups_list = self.director.delete_trunk_groups(params['trunkgrpid'])
                if str(trunk_groups_list['trunk_group']['destination_dn_formatted']) == params[
                    'destinationdn'] + ' : Default':
                    return True
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Trunk group deletion failed")
            return False


    def director_verify_audio_web_switch_status(self, **params):
        """
        Description: Verify the audio/web conferencing switch parameters.
        Param: params: Dictionary contains audio/web conferencing switch information
        Returns:  audio/web switch state
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  30-01-2019

        """
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            if params.keys():
                ohs_list = self.director.fetch_audio_web_switch_info()
                no_of_apps=len(params["appName"])
                count=0
                for ohs in ohs_list:
                    if ohs[1] in params["appName"]:
                        if ohs[0] == "up.gif" or ohs[0] == "yup.gif":
                            count += 1
                if count == no_of_apps:
                    return True
                else:
                    print("Not all appliances are in service")
                    print("Out of " + str(no_of_apps) + " IM switches only " + str(count) + " are in service ")
                    return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Verify audio/web switch status failed")
            return False

    def director_verify_im_switch_status(self, **params):
        """
        Description: Verify the IM switch parameters.
        Param: params: Dictionary contains IM switch information
        Returns:  IM switch state
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        # import pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            if params.keys():
                ohs_list = self.director.fetch_im_switch_info()
                no_of_apps=len(params["appName"])
                count=0
                for ohs in ohs_list:
                    #print ohs
                    if ohs[2] in params["appName"]:
                        if ohs[1] == "up.gif" or ohs[1] == "yup.gif":
                            count += 1
                if count == no_of_apps:
                    return True
                else:
                    print("Some of the IM switches are down")
                    print("Out of " + str(no_of_apps) + " IM switches only " + str(count) + " are in service ")
                    return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Verify IM switch status failed")
            return False

    def director_verify_call_streams_in_call_quality(self, **params):
        """
        Description: Verify the call quality option of maintainance.
        Param: params: Dictionary contains call information
        Returns:  presence of call record
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():

                ohs_list = self.director.fetch_calls_info()
                callid_UserA = []
                callid_UserB = []
                callid_OtherUsers = []
                callid_UserA_userB = []
                for ohs in ohs_list:
                    # print ohs[0],ohs[3]
                    if ohs[0] == params["tenant"] and ohs[3] == params["extn1"]:
                        callid_UserA.append(ohs[1])
                    elif ohs[0] == params["tenant"] and ohs[3] == params["extn2"]:
                        callid_UserB.append(ohs[1])
                    else:
                        callid_OtherUsers.append(ohs[1])

                # print "Call ID of User A : " + ','.join(callid_UserA)+"\n len is :" + str(len(callid_UserA))
                # print "Call ID of User B : "+ ','.join(callid_UserB)+"\n len is :" + str(len(callid_UserB))
                # print "Call ID of User Others : " + ','.join(callid_OtherUsers)+"\n len is :" + str(len(callid_OtherUsers))
                print "Call ID of User A  len is :" + str(len(callid_UserA))
                print "Call ID of User B  len is :" + str(len(callid_UserB))
                print "Call ID of User Others  len is :" + str(len(callid_OtherUsers))

                if len(callid_UserA) > len(callid_UserB):
                    final_list = callid_UserA
                else:
                    final_list = callid_UserB

                for item in final_list:
                    if item in callid_UserA and item in callid_UserB and item not in callid_OtherUsers:
                        callid_UserA_userB.append(item)
                print "no.of call between user A And User B : " + str(len(callid_UserA_userB))
                print "Call ID those calls" + ','.join(callid_UserA_userB)

                if len(callid_UserA_userB) >= 0:
                    return len(callid_UserA_userB)
                else:
                    print("Call record was not added in D2")
                return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("call quality verification failed")
            return False

    def director_verify_ip_phone_status(self, **params):
        """
        Description: Verification of ipphone status in D2 page.
        Param: params: ip phone mac address
        Returns: status
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            if params.keys():
                # import pdb
                # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                x_list = self.director.fetch_ip_phone_info(params["phonemac"])
                for x in x_list:
                    if re.sub('[^0-9A-F]+', '', str(x[2])) == params["phonemac"]:
                        if (x[1] == params["status"] or x[1] == "yup.gif"):
                            call_list = self.director.fetch_ip_phone_specific_call_info(params["phonemac"])
                            if call_list:
                                return True
                            else:
                                print("Call list not found for phone")
                                return False
                        else:
                            print("IP Phone not in service")
                            return False
                print("Requested Phone not found")
                return False
            else:
                print("All phones are not in service")
        except AssertionError, e:
            print(e)
            print("IP Phone status verification failed")
            return False

    def insert_values_into_file(self, **params):

        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, '..\Variables\\')

        print "Old Value is : "+params["oldvalue"]
        print "New value is : "+params["newvalue"]
        # print file_path + "Auto_Login.robot"

        with open(file_path + params["fileName"], "r") as f:
            newline = []
            for word in f.readlines():
                    #print word
                    newline.append(word.replace(params["newvalue"], params["oldvalue"]))

        with open(file_path + params["fileName"], "w") as f:
            for line in newline:
                f.writelines(line)

        return True
        
    def update_values_into_file(self, **params):
        """params: Dictionary contains information to be modified corresponding to key
        file : file to be modify
        key: key to be search
        old_val: field's to be modify
        new_val: new value for old_val field
        """
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, '..\Variables\\')
        #logger.console(dir)
        #logger.console(file_path)
        with open(file_path + params["file"], "r") as read_file:
            rf= read_file.readlines()
           
        with open(file_path + params["file"],"w") as write_file:
            check_flag=False
            for line in rf:
                if params["key"] in line:
                    check_flag=True
                    if params["old_val"] in line:
                        import re
                        #spliting for at least 2 whitespaces
                        new_line= re.split(r'\s{2,}', line)
                        container=[]
                        for val in new_line:
                            if params["old_val"] in val:
                                container.append(val.replace(val.split("=")[1],params["new_val"]))
                            else:
                                container.append(val)
                        write_file.write("  ".join(x for x in container)+"\n")
                        del container
                    else: 
                        print "old_val : %s not found adding new_val %s"%(params["old_val"],params["new_val"])
                        write_file.write(line.strip()+"  %s=%s"%(params["old_val"],params["new_val"])+"\n")
                else:
                    write_file.write(line)
            if  not check_flag:
                write_file.write("&{%s}       %s=%s"%(params["key"],params["old_val"],params["new_val"]))
            return True
    
    def update_single_key_value_in_file(self,**params):
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, '..\Variables\\')
        with open(file_path + params["file"], "r") as read_file:
            rf= read_file.readlines()
        
        with open(file_path + params["file"],"w") as write_file:
            check_flag=False
            for line in rf:
                if params["key"] in line:
                    new_line= re.split('\s+', line)
                    write_file.write(new_line[0].strip()+"                   %s\n"%params["value"])
                    check_flag=True
                else:
                    write_file.write(line)
            if not check_flag:
                write_file.write("\n${%s}                   %s"%(params["key"],params["value"]))        
            return True
            
    def modify_key_in_file(self, **params):
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, '..\Variables\\')
        # logger.console(dir)
        # logger.console(file_path)
        with open(file_path + params["file"], "r") as read_file:
            rf = read_file.readlines()

        with open(file_path + params["file"], "w") as write_file:
            check_flag = False
            for line in rf:
                if params["key"] in line:
                    check_flag = True
                    if params["old_val"] in line:
                        import re
                        # spliting for at least 2 whitespaces
                        new_line = re.split(r'\s{2,}', line)
                        container = []
                        for val in new_line:
                            if params["old_val"] in val:
                                container.append(val.replace(val.split("=")[0], params["new_val"]))
                            else:
                                container.append(val)
                        write_file.write("  ".join(x for x in container) + "\n")
                        # logger.console(container)
                        # write_file.write("  ".join(x for x in container))

                        del container
                    else:
                        print "old_val : %s not found adding new_val %s" % (params["old_val"], params["new_val"])
                        write_file.write(line.strip() + "  %s=%s\n" % (params["old_val"], params["new_val"]))
                else:
                    write_file.write(line)
            if not check_flag:
                write_file.write("\n&{%s}       %s=%s" % (params["key"], params["old_val"], params["new_val"]))
            return True


    def normalize_to_number(self,**params):
        print "calling working "
        import re
        print type(params["did"]), str(params["did"])
        phonenum = re.sub('[^0-9]+', '', str(params["did"]))
        print phonenum
        return phonenum

    # Fault Tolerance

    def director_fetch_switch_information(self, **params):
        """
        Description: switch details
        Param: params: switch name
        Returns: current switch and other in service switch details
        Created by: Srisai Palamoor
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            xlist = self.director.fetch_switch_status_D2(params["sname"])
            if xlist:
                print xlist
                return xlist
            else:
                print("Could not fetch record for given switch " + str(params["sname"]))
                return False

        except AssertionError, e:
            print(e)
            print("fetching switch info failed")
            return False

    def director_fetch_other_switch_information(self, **params):

        """
                Description: switch details
                Param: params: switch name
                Returns: any other in service switch info
                Created by: Srisai Palamoor
                Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            xlist = self.director.fetch_other_switch_info(params["sname"])
            if xlist:
                print xlist
                return xlist
            else:
                print("Could not fetch record for given switch " + str(params["sname"]))
                return False

        except AssertionError, e:
            print(e)
            print("fetching switch info failed")


    def director_move_phone(self, **params):
        """
        Description: move phone to another switch
        Param: params: phone mac, switch name
        Returns: status
        Created by: Srisai Palamoor
        Modified by:   Lavanya Nagaraj  30-01-2019
        """
        try:
            xlist = self.director.change_ipphone_switch(params["pid"], params["s2id"])
            return xlist
        except AssertionError, e:
            print(e)
            print("moving phone to another switch failed")
            return False


    def rp_ssh_cmd(self, **params):
        """
                Description: run given cmd on rp ip
                Param: params: rp ip, cmd
                Return: status
                Created by: Srisai Palamoor
                Modified by:   Lavanya Nagaraj  30-01-2019
                """
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(params["ip"], username="admin", password="Shoreadmin1#")

            print("Running ssh cmd: \"%s\"" % params["cmd"])
            stdin, stdout, stderr = self.ssh.exec_command(params["cmd"], get_pty=True)
            result = stdout.readlines()

            if self.ssh:
                self.ssh.close()
            return result
        except AssertionError, e:
            print(e)
            print("executing cmd on rp failed")
            return False




    def director_verify_phone_details(self, **params):
        """
                Description: Fetching info of specific phone
                Param: mac address
                Returns: status
                Created by: Srisai Palamoor
                Modified by:   Lavanya Nagaraj  05-02-2019

                """
        try:
            if params.keys():
                # import pdb
                # pdb.Pdb(stdout=sys.__stdout__).set_trace()
                x_list = self.director.fetch_phone_info(params["mac"], params["tenant"])

                print x_list
                return x_list
        except AssertionError, e:
            print(e)
            print("Fetching specific phone info failed")
            return False

    def insert_values_into_csv(self, **params):
        """
        # print "Old Value is : "+params["oldvalue"]
        # print "New value is : "+params["newvalue"]
        # print file_path + "Auto_Login.robot"
        """
        import csv
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, '..\..\\automation-manhattan\Configuration\\')

        new_rows_list=[]
        with open(file_path + params["fileName"], "rb") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fields = row
                if row["user_name"] == str(params["user"]):
                    row[str(params["key"])] = str(params["value"])
                    new_rows_list.append(row)
                else:
                    new_rows_list.append(row)
        print new_rows_list
        #
        with open(file_path + params["fileName"], "wb") as f1:
            writer = csv.DictWriter(f1,fields)
            writer.writeheader()
            writer.writerows(new_rows_list)
        return True

    def director_get_system_extn(self, **params):
        """
        Verification of Trunk groups in D2 page
        :param params:trunkgrpName
        :return: Trunk_grp_id
        """
        print params['voice_mail']
        vm_key = str(params['voice_mail'])
        if params.keys():
            system_extn_list = self.director.fetch_system_extn_info()
            vm_extn = system_extn_list['system_extensions'][vm_key]['DN']
            return  vm_extn
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_crash_dump(self, **params):
        """
        Description: chech for core files in ucb
        Param: params: rpip, UCBIP
        Returns: status
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  05-02-2019
        """
        try:
            import paramiko
            import time
            import datetime
            from datetime import datetime
            # import pdb
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()

            self.ssh = paramiko.SSHClient()  # connect to proxy
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(params["rpip"], username="admin", password="Shoreadmin1#")
            chan = self.ssh.invoke_shell()
            for ucbip in params["ucbip"]:
                chan.send('ssh admin@' + ucbip + '\n')  # connect to ucb
                buff = ''
                while not buff.endswith('\'s password: '):
                    resp = chan.recv(9999)
                    buff += resp
                chan.send('ShoreTel\n')
                buff = ''
                while not buff.endswith('$ '):
                    resp = chan.recv(9999)
                    buff += resp

                chan.send('cd /cf/core\n')  # move to location
                time.sleep(1)
                buff = ''
                resp = ''
                chan.send('ls -hlrt\n')  # find files
                time.sleep(1)
                buff = chan.recv(9999)
                resp += buff
                m = re.findall('-rw-rw-rw-.(.+?)gz', resp)
                if not m:  # case 0: No files
                    s = re.findall('total 0', resp)
                    if s:
                        return True

                file = m[len(m) - 1]  # case 1: files present
                wordList = re.sub("[^\w]", " ", file).split()
                month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                              'Oct': 10, 'Nov': 11, 'Dec': 12}
                if month_dict[wordList[5]] == datetime.now().month:
                    if int(wordList[6]) == datetime.now().day or int(wordList[6]) - datetime.now().day == 1:
                        print("A core file has been generated today")
                        return False
                else:
                    return True
                chan.send('exit\n')
                chan.send('exit\n')
        except AssertionError, e:
            print(e)
            print("core files checking failed")
            return False

    def director_monitoring_service(self, **params):
        """
        Description: verification of build in monitoring service page
        Param: params: build
        Returns: status
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  05-02-2019
        """
        try:
            if params.keys():
                x_list = self.director.fetch_build_info()
                if x_list:
                    if x_list[4] == str(' ' + params['build'] + ' '):
                        if x_list[0] == "true ":
                            print(str(params['build'])+"Build verified successfully")
                            return True
                        else:
                            print("Not in service")
                            return False
                    else:
                        print("Build did not match")
                        print("Current build: " + str(x_list[4]))
                        return False
                else:
                    print("No record found")
                    return False
            else:
                print("Please check that the input parameters have been provided")
        except AssertionError, e:
            print(e)
            print("Build verification failed")
            return False

    def director_system_information(self):

        """
        Description: verification of system page in maintainance
        Param:
        Returns: status
        Created by: Lavanya Nagaraj
        Modified by:   Lavanya Nagaraj  05-02-2019
        """
        try:
            audio_list, web_list, button = self.director.fetch_system_details()
            if audio_list:
                if web_list:
                    if str(button) == "Create Backup":
                        print("record for audio , web ports and backup button are intact.")
                        return True
                    else:
                        print("Backup button not found")
                        return False
                else:
                    print("Record for web ports not found")
                    return False
            else:
                print("Record for audio ports not found")
                return False
        except AssertionError, e:
            print(e)
            print("System page verification failed")
            return False

    def create_phone_dictionary(self, **params):
        # import pdb;
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        if params.keys():
            phone_info = {}
            tenant_info = self.director.get_specific_tenants(params["AccName"])
            tid = tenant_info[0][1]
            textn = tenant_info[0][2]
            x, user_info = self.director.fetch_tenant_specific_users(tid)
            user_id = self.director.fetch_specific_user_id(params["extension"], textn, user_info)
            user_detail = self.director.fetch_user_detail(user_id)
            mac_add = user_detail['user']['current_port_display']
            phone_data = self.director.fetch_phone_detail(tid, mac_add)
            for i in phone_data['rows']:
                if i['cell'][0] == mac_add:
                    phone_info["phoneName"] = i['cell'][5][1]
                    phone_info["ipAddress"] = i['cell'][4]
                    phone_info["phoneModel"] = i['cell'][7]
                    phone_info["extensionNumber"] = params['extension']
                    phone_info["mac"] = i['cell'][3]
            return phone_info
        else:
            print("Please check that the input parameters have been provided")