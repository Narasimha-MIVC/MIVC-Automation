"""
Module to interact with Mitel phones. This is a base class which will be inherited in other phone model specific
classes.
"""
__author__ = "milton.villeda@mitel.com"

import sys
import os
import time

import telnetlib
from robot.api import logger

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from mitel_phone_base import Phone6xxxInterface
from . import phone_button_map
from . import phone_68xx_password

class Phone_68xx(Phone6xxxInterface):
    """ 68xx Phone Interface
    """
    def __init__(self, phone_info, **kwargs):
        """
        It is mandatory to call phone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """
        logger.info("Initializing Mitel 68xx Phone class")
        self.phone_type = phone_info['phoneModel']
        
        if "Mitel6867i" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6867i_button_map
            phone_info['telnet_password'] = phone_68xx_password.phone_6867i_telnet_password
            phone_info['ssh_password'] = phone_68xx_password.phone_6867i_ssh_password
        elif "Mitel6865i" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6865i_button_map
            phone_info['telnet_password'] = phone_68xx_password.phone_6865i_telnet_password
            phone_info['ssh_password'] = phone_68xx_password.phone_6865i_ssh_password
        elif "Mitel6863i" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6863i_button_map
            phone_info['telnet_password'] = phone_68xx_password.phone_6863i_telnet_password
            phone_info['ssh_password'] = phone_68xx_password.phone_6863i_ssh_password
        # elif "Mitel6869" in self.phone_type:
            # phone_info['button_map'] = phone_button_map.phone_6869_button_map
            # phone_info['telnet_password'] = phone_68xx_password.phone_6863i_telnet_password
            # phone_info['ssh_password'] = phone_68xx_password.phone_6863i_ssh_password
            # self.phone_obj = PhoneInterface6869()

        Phone6xxxInterface.__init__(self, phone_info)

        self.enable_ssh_on_68xx()
     
    def phone_console_cmd(self, cmd, options=None):
        """Runs cmd via phone console
        
        :param cmd:  command
        :type cmd: type str
        :param options:  command options
        :type cmd: type str
        :return ret_val:  cmd result
        """
        if 'options' in self.phone_info:
            if "cmd_telnet" in self.phone_info['options']:
                return self.phone_telnet_cmd(cmd)
        
        return self.phone_ssh_su_cmd(cmd)
         
    def phone_ssh_su_cmd(self, cmd):
        """ Runs cmd via ssh as su on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.phone_info['ipAddress'], username="root", password=self.phone_info['ssh_password'])

        logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.readlines()
        logger.info("Cmd result: %s" % (result))
        
        if  self.ssh:
             self.ssh.close()
        return result  
        
    def phone_telnet_cmd(self, cmd):
        """ Runs cmd via telnet on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        user = "root"
        password = self.phone_info['telnet_password']
        
        cmd_list = list()
        if type(cmd) is str:
            cmd_list.append(cmd)
        elif type(cmd) is list:
            cmd_list = cmd
        else:   
            raise Exception("cmd type %s is not supported" % type(cmd))
            
        start_time = time.time()
        for command in cmd_list:
            tn = telnetlib.Telnet(self.phone_info['ipAddress'])
            # Hangs if there no sleep
            time.sleep(.1)
            
            # tn.read_until("login: ")
            tn.write(user + "\n")
            if password:
                tn.read_until("Password: ")
                tn.write(password + "\n")
            tn.write(command + '\n')
            tn.write("exit\n")

            result = tn.read_all() 
            logger.info("cmd '%s' ran on phone %s" % (cmd, self.phone_info['ipAddress']))
            tn.close()
        logger.info('Time elapsed for telnet cmd(s): %.3f s\n%s' % ((time.time() - start_time), cmd))

        return result 
   
    def enable_ssh_on_68xx(self):
        """
            THIS FUNCTION MUST USE TELNET
        """
        # Check if dropbear is already running
        cmd = "ps -ef | grep /usr/sbin/dropbear"
        result = self.phone_telnet_cmd(cmd)
        
        if "-r /nvdata/etc/dropbear_rsa_host_key" in result:
            logger.warn("Dropbear SSH is already running")
            return
        
        cmd_list = list()
        
        cmd_list.append("tftp -g -r dropbear_rsa_host_key " + str(self.phone_info['tftpServer']))
        cmd_list.append("tftp -g -r dropbearmulti " + str(self.phone_info['tftpServer']))
        cmd_list.append("chmod a+x dropbearmulti")
        cmd_list.append("mv dropbear_rsa_host_key /nvdata/etc/")
        cmd_list.append("mv dropbearmulti /usr/bin/")
        cmd_list.append("ln -s /usr/bin/dropbearmulti /usr/bin/dropbearconvert")
        cmd_list.append("ln -s /usr/bin/dropbearmulti /usr/bin/dropbearkey")
        cmd_list.append("ln -s /usr/bin/dropbearmulti /usr/sbin/dropbear")
        #run server
        cmd_list.append("/usr/sbin/dropbear -r /nvdata/etc/dropbear_rsa_host_key")
        
        self.phone_telnet_cmd(cmd_list)   
    
    def upload_apt_files_to_phone(self, files_to_upload):
        # check if list is empty
        if not files_to_upload :
            return
            
        for file in files_to_upload:
            tftp_cmd = "tftp -g -r " + file + " " + str(self.phone_info['tftpServer'])
            self.phone_console_cmd(tftp_cmd)

            if "pcm" in file:
                mv_cmd = 'mv ' + file + ' /tmp/' + file
                self.phone_console_cmd(mv_cmd)

    def get_file_from_phone(self, phone, get_path):
        try:
            tftp_cmd = "tftp -p -l " + get_path + " " + str(phone.phone_info['tftpServer'])
            phone.phone_console_cmd(tftp_cmd)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
                      
    def remove_file_on_phone(self, phone, rm_path):
        try:
            rm_cmd = "rm " + rm_path
            phone.phone_console_cmd(rm_cmd)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def verify_hold_state_packets(self):
        """
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        cmd = 'cat /proc/ept/rtpstats'
        result = self.phone_console_cmd(cmd)
        results = result.split('\n')
        
        # Result is not empty for telnet
        # Minimum check for ingressRtpPkt
        for item in results:
            if "ingressRtpPkt" in item:
                raise Exception("verify_hold_state_packets fail! %s" % result)
