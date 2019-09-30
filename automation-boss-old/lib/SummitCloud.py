"""
    Module for Summit Cloud utilities
    Author: Prasanna Kumar Tripathy
"""

import requests
import json
import ast
import datetime


def uc_db_connect(fun):
    """ Decorator for all UC DB accessing functions"""
    def wrapper_uc_db_connect(*args, **kwargs):
        """
        wrapper function
        :param args:
        :param login_credentials:
        :return:
        """
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        username = kwargs.get('username', 'root')
        password = kwargs.get('password', 'Shoreadmin1#')
        server_ip = kwargs.get('ip', None)

        if not server_ip:
            return False
        try:
            ssh.connect(server_ip, 22, username, password)
        except Exception as e:
            print(e)
            return False
        # invoke the actual verification function
        status = fun(ssh, *args, **kwargs)
        ssh.close()
        return status
    return wrapper_uc_db_connect


@uc_db_connect
def verify_db_log(ssh, db_id, data, **kwargs):
    """
    :param db_id: the required db id
    :param data: data to be verified in log
    :param ssh: secured shell session
    :param: kwargs:
    :return: True / False
    :Author: Prasanna
    """
    try:
        if db_id == 'loc':
            db_id = 'loc_'

        # Get all the containers currently running
        cmd = 'docker ps | grep ' + db_id
        _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        if not ssh_stdout:
            print(ssh_stderr)
            raise Exception("command to fetch container info failed!")

        container_name = ssh_stdout.readlines()[0].split(" ")[-1].rsplit('\n')[0]
        if not container_name:
            raise Exception("container name not found!")

        cmd = 'docker logs --details ' + container_name + ' | grep '
        if db_id == 'tds' or 'idms' or 'ses' or 'loc':
            uuid = data
            cmd += uuid

        _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        if not ssh_stdout:
            print(ssh_stderr)
            raise Exception("No log found!")
        # If the test case need the log data
        if kwargs.get('uc_db_data', None):
            print("Updating the fetched data")
            kwargs['uc_db_data'].update({'fetched_data': ssh_stdout.readlines()})
        else:
            for line in ssh_stdout.readlines():
                print(line)
                if 'ERROR' in line:
                    raise Exception("Error in the log!")
        return True
    except Exception as e:
        print(e)
        return False


@uc_db_connect
def uc_container_manipulation(ssh, db_id, operation, **kwargs):
    """

    :param ssh:
    :param db_id:
    :param operation:
    :param kwargs:
    :return:
    """
    try:
        if db_id == 'loc':
            db_id = 'loc_'

        if operation != 'start':
            # Get the required container
            cmd = 'docker ps | grep ' + db_id
            _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
            if not ssh_stdout:
                print(ssh_stderr)
                raise Exception("command to fetch container info failed!")

            # container_id = ssh_stdout.readlines()[0].split(" ")[0]
            container_name = ssh_stdout.readlines()[0].split(" ")[-1].rsplit('\n')[0]
            if not container_name:
                raise Exception("container name not found!")

        if operation == 'stop':
            cmd = 'docker stop ' + container_name
        elif operation == 'start':
            # if kwargs.get('uc_db_data', None):
            #     cmd = 'docker start ' + kwargs['uc_db_data']['fetched_data'][0].rsplit('\n')[0]
            # else:
            #     raise Exception("Container name is not provided")
            # Prasanna: Just restart all stopped containers
            cmd = 'docker start $(docker ps -a -q -f status=exited)'

        _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        if kwargs.get('uc_db_data', None):
            kwargs['uc_db_data'].update({'fetched_data': ssh_stdout.readlines()})

        for line in ssh_stdout.readlines():
            print(line)
        return True
    except Exception as e:
        print(e)
        return False


@uc_db_connect
def uc_db_query(ssh, db_name, query, **kwargs):
    """
    The API executes the uc db queries
    :param ssh:
    :param db_name: name of the db which is being queried
    :param query: The query which needs to be sent to the DB. It has to be formed by the caller of this API
    :param kwargs:
    :return: True / False
    """
    try:
        # Get the container name that hosts the postgres data services
        cmd = 'docker ps | grep uc_postgres_datasvc'
        _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        if not ssh_stdout:
            print(ssh_stderr)
            raise Exception("command to fetch container info failed!")

        container_name = ssh_stdout.readlines()[0].split(" ")[-1].rsplit('\n')[0]
        if not container_name:
            raise Exception("container name not found!")

        # get to the DB. Chaining of commands to get the query done in single go
        # cmd = 'docker exec -ti ' + container_name + ' psql -U postgres ' + db_name + ' -c ' + '"' + query + '"'
        cmd = 'docker exec -ti autosumitcloud_uc_postgres_datasvc_1 psql -U postgres tds -c \\"select * from tenants\\"'
        # Execute the command
        # _, ssh_stdout, ssh_stderr = ssh.exec_command('touch x.sh')
        # _, ssh_stdout, ssh_stderr = ssh.exec_command('echo ' + cmd + ' > x.sh')
        # _, ssh_stdout, ssh_stderr = ssh.exec_command('sh x.sh > y.txt')
        _, ssh_stdout, ssh_stderr = ssh.exec_command('sh x.sh &')
        import time
        time.sleep(3)
        sftp_client = ssh.open_sftp()
        remote_file = sftp_client.open('y.txt')
        print("*"*40)
        try:
            for line in remote_file:
                print(line)
        finally:
            remote_file.close()
        # _, ssh_stdout, ssh_stderr = ssh.exec_command('ls')
        # _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        if not ssh_stdout:
            print(ssh_stderr)
            raise Exception("command to fetch container info failed!")

        # returning the data to the caller of the API to verify
        # if kwargs.get('uc_db_data', None):
        #     kwargs['uc_db_data'].update({'fetched_data': ssh_stdout.readlines()})
        for line in ssh_stdout.readlines():
            print(line)
        return True
    except Exception as e:
        print(e)
        return False


def convert_to_dict(src_str, dest_dict=None):
    """
    The function converts a response string from db to a list of dictionaries of items
    :param src_str: db response string
    :param dest_dict: list of item dictionaries
    :Author:  Prasanna Kumar Tripathy
    """
    # convert from list to a complete string
    src_str = ''.join(src_str)

    if "false" in src_str:
        src_str = src_str.replace("false", "\"false\"")
    if "true" in src_str:
        src_str = src_str.replace("true", "\"true\"")
    d = ast.literal_eval(src_str)
    if type(d) == dict:
        dest_dict.update(d)
    if type(d) == list:
        # [dest_dict.update(i) for i in d if type(i) == dict]
        return d


def get_data_verification_fun(table):
    """
    Closure to return the required function for data verification
    :param table: The db table id
    :return: function to verify data
    :Author: Prasanna
    """

    # --- Start: "verify_users_data"
    def verify_users_data(db_data, test_data):
        """ User data verification """
        status = True
        print("verifying the users data")
        if not db_data or not test_data:
            raise Exception("No users data provided!!")

        # Convert the "db_data" to a list of dictionaries
        db_items = dict()
        convert_to_dict(db_data, db_items)

        # implement the logic here
        if (test_data.get('UserUuid', None) and test_data['UserUuid'] != db_items.get('uuid', None)) or \
                (test_data.get('AccountGuid', None) and test_data['AccountGuid'] != db_items.get('tenant_id', None)) or \
                (test_data.get('LocationUuid', None) and test_data['LocationUuid'] != db_items.get('location_id', None)) or \
                (test_data.get('address_type', None) and db_items.get('user_addresses', None) and test_data['address_type'] != db_items['user_addresses'][0]['address_type']) or \
                (test_data.get('country', None) and db_items.get('user_addresses', None) and test_data['country'] != db_items['user_addresses'][0]['country']) or \
                (test_data.get('state', None) and db_items.get('user_addresses', None) and test_data['state'] != db_items['user_addresses'][0]['state']):
            return False

        return status
   # --- End: "verify_users_data"

    # --- Start: "verify_tenants_data"
    def verify_tenants_data(db_data, test_data):
        """ Tenant data verification """
        status = True
        print("verifying the tenant data")
        if not db_data or not test_data:
            raise Exception("No tenant data provided!!")

        # Convert the "db_data" to a list of dictionaries
        db_items = dict()
        convert_to_dict(db_data, db_items)

        # implement the logic here (convert the string to dictionary before comparing)
        if test_data.get('uuid', None) and test_data['uuid'] != db_items.get('uuid', None):
            status= False
        if test_data.get('Name', None) and test_data['Name'] != db_items.get('name', None):
            status= False
        if test_data.get('WebSite', None) and test_data['WebSite'] != db_items.get('website', None):
            status= False

        return status

    # --- End: "verify_tenants_data"

    # --- Start: "verify_services_data"
    def verify_services_data(db_data, test_data):
        """ Services data verification """
        status = True
        print("verifying the Services data")
        if not db_data or not test_data:
            raise Exception("No services data fetched from the DB!!")

        # Convert the "db_data" to a list of dictionaries
        db_items = convert_to_dict(db_data, None)

        # implement the logic here
        # first get the dictionary which contains the service details
        temp_dict = dict()
        if test_data.get('ServiceUuid', None):
            [temp_dict.update(i) for i in db_items if i.get('service_instance_id', None) and
             test_data['ServiceUuid'] == i['service_instance_id']]
            if (not temp_dict) or (test_data.get('UserUuid', None)
                                   and test_data['UserUuid'] != temp_dict.get('user_uuid', None)):
                return False
            if (not temp_dict) or (test_data.get('AccountGuid', None)
                                   and test_data['AccountGuid'] != temp_dict.get('tenant_uuid', None)):
                return False
        return status

    # --- End: "verify_services_data"

    # --- Start: "verify_locations_data"
    def verify_locations_data(uc_db_data, test_data):
        """ Locations data verification """
        status = True
        print("verifying the Locations data")
        if not uc_db_data or not test_data:
            raise Exception("No Locations data fetched from the DB!!")

        # Convert the "db_data" to a list of dictionaries
        db_items = dict()
        convert_to_dict(uc_db_data, db_items)

        if (test_data.get('LocationUuid', None) and test_data['LocationUuid'] != db_items.get('uuid', None)) or \
                (test_data.get('AccountGuid', None) and test_data['AccountGuid'] != db_items['tenant_id']) or \
                (test_data.get('status', None) and test_data['status'] != db_items.get('location_status', None)) or \
                (test_data.get('city', None) and test_data['city'] != db_items['city']) or \
                (test_data.get('country', None) and test_data['country'] != db_items['country']) or \
                (test_data.get('state', None) and test_data['state'] != db_items['state']):
            return False

        return status

    # --- End: "verify_locations_data"
    # return the appropriate function
    if table == 'users':
        return verify_users_data
    elif table == 'tenants':
        return verify_tenants_data
    elif table == 'services':
        return verify_services_data
    elif table == 'locations':
        return verify_locations_data


class SummitCloud(object):
    """The utilities for testing summit cloud"""

    def sc_fetch_data(self, url=None, **url_components):
        """
        Method to fetch data from db
        If 'url' is None then we have to construct it from the 'url_components'
        :param url: url to fetch data from
        :param url_components: information to build an URL
        :return: True/False and the Data fetched
        :Author: Prasanna
        """
        status = True
        data = None
        try:
            if not url and not url_components:
                raise Exception("mandatory input parameters missing")
            if url_components and not url:
                username = url_components.get('username', 'default')
                password = url_components.get('password', '1234')
                server_ip = url_components.get('ip', None)
                server_port = url_components.get('port', None)
                api_version = url_components.get('version', 'v2')
                table = url_components.get('table', None)
                condition = url_components.get('condition', None)

                if not table or not server_ip or not server_port:
                    raise Exception("mandatory url parameters missing")

                # construct the url:
                url = r'http://' + username + ':' + password + '@' + server_ip + ':' + server_port + '/'
                if table != 'locations':
                    url = url + api_version + '/'
                url = url + table + '/'
                if condition:
                    url = url + condition
                print(url)
            self.session = requests.session()
            data = self.session.get(url)
        except Exception as e:
            print(e)
            status = False
        return status, data

    def sc_verify_db_data(self, test_data=None, db_data=None, table=None, **url_component):
        """
        :param test_data: data to be verified
        :param db_data: data fetched from db
        :param table: db table id
        :param url_component: the detailed url info
        :return: True / False
        :Author: Prasanna
        """

        try:
            # 1. Fetch db data
            if url_component and not db_data:
                table = url_component.get('table', None)
                _, result = self.sc_fetch_data(**url_component)
                if not result:
                    raise Exception("db fetch failed !!")
                db_data = json.loads(result.text)

            # 2. verify fetched data
            if db_data and test_data:
                # get the required function for verification
                verify_data = get_data_verification_fun(table)
                return verify_data(db_data, test_data)
            else:
                raise Exception("Data verification failed !!")

        except Exception as e:
            print(e)
            return False

    def sc_verify_db_log(self, db_id, data=None, **kwargs):
        """
        :param db_id: the required db id
        :param data: data to be verified in log
        :param kwargs: credentials for the DB log in
        :return: True / False
        :Author: Prasanna
        """
        try:
            status = verify_db_log(db_id, data, **kwargs)
        except:
            return False
        return status

    def sc_query_uc_db(self, db_name, query, **kwargs):
        """
        The method executes the corresponding uc db query and returns the fetched data to the caller
        :param db_name: The name of the db
        :param query: The query that needs to be sent to the DB
        :param kwargs:
        :return:
        """
        try:
            status = uc_db_query(db_name, query, **kwargs)
        except:
            return False
        return status

    def sc_uc_container_manipulation(self, db_id, operation, **kwargs):
        """

        :param db_id:
        :param operation:
        :param kwargs:
        :return:
        """
        try:
            status = uc_container_manipulation(db_id, operation, **kwargs)
        except:
            return False
        return status

    def backsync_fetch_data(self, url=None, **url_components):
         """
        Method to fetch data from backsync DB
        If 'url' is None then we have to construct it from the 'url_components'
        :param url: url to fetch data from Back Sync
        :param url_components: information to build an URL
        :return: True/False and the Data fetched
        Author: Priyanka
        """
         status = True
         data = None
         try:
                if not url and not url_components:
                    raise Exception("mandatory input parameters missing")
                if url_components and not url:
                    server_ip = url_components.get('ip', None)
                    server_port = url_components.get('port', None)
                    api_name = url_components.get('api_name', None)
                    api_type = url_components.get('api_type', None)
                    condition = url_components.get('condition', None)
                    option = url_components.get('option', None)
                    skip = url_components.get('skip', None)
                    top = url_components.get('top', None)
                    orderby = url_components.get('orderby', None)
                    spl_char = url_components.get('spl_char', None)
                    StartDate = url_components.get('StartDate', None)
                    EndDate = url_components.get('EndDate', None)
                    updated_starttime = datetime.datetime.strptime(StartDate, '%Y-%m-%d %H:%M:%S.%f')
                    updated_starttime = updated_starttime.strftime("%Y-%m-%dT %H:%M:%S.%fZ")
                   # print(updated_starttime)
                    updated_endtime = datetime.datetime.strptime(EndDate, '%Y-%m-%d %H:%M:%S.%f')
                    updated_endtime = updated_endtime.strftime("%Y-%m-%dT %H:%M:%S.%fZ")
                    #print(updated_endtime)
                    if not api_name or not server_ip or not server_port:
                        raise Exception("mandatory url parameters missing")

                    # construct the url:
                    url = r'http://' + server_ip + ':' + server_port + '/' + 'api' + '/' + api_name + '/' + \
                          api_type
                    # + '?'
                    if condition:
                        url = url + condition + '&'
                    else:
                        raise Exception("mandatory condition as Type=Users/Location  parameters missing")

                    new_start_time = datetime.datetime.strptime(StartDate, '%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(minutes=15)
                    #print(new_start_time)
                    new_start_time = new_start_time.strftime("%Y-%m-%dT %H:%M:%S.%fZ")
                    #print(new_start_time)
                    # Reconstruct URL with StartDate,EndDate and option
                    url = url + 'StartDate=' + new_start_time + '&' + 'EndDate=' + updated_endtime + '&' + \
                          'option=' + option
                    if (skip):
                        url = url + '&' + 'skip=' + skip
                    if (top):
                        url = url + '&' + "top=" + top
                    if (orderby):
                        url = url + '&' + "orderby=" + orderby
                    if (spl_char):
                        url = url + '&' + spl_char
                    print(url)
                self.session = requests.session()
                data = self.session.get(url)
         except Exception as e:
             print(e)
             status = False
         return status,data
