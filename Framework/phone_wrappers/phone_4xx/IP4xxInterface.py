__author__ = "milton.villeda@mitel.com"

import os
import sys
import telnetlib
import psutil
import shutil
import subprocess
import time
import re
import ftplib
import socket
import base64
from sys import platform as _platform

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from kbd_server import *
from socket_interface import *
import vm_codes
# import CeleryRemote

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger
# from robot.libraries.Telnet import Telnet

class IP4xxInterfacebase(object):
    def __init__(self, ip4xx_user) :
        self.extensionNumber = ip4xx_user['extension']
        self.phoneName = ip4xx_user['phoneName']
        self.authCode = ip4xx_user['vm_password']
        self.trunkISDN = ip4xx_user['did']
        self.macAddress = ip4xx_user['PPhone_mac']

class IP4xxInterface(object):
    """ IP4xx Interface
    """
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_LIBRARY_VERSION = VERSION
    
    def __init__(self, ip4xx_user,is_mt="true"):
        self.os_atf_path = ""
        self.ip4xx_user = ip4xx_user
        self.ip4xx_user['phone_model'] = 'p8cg'
        print (ip4xx_user)
        
        self.is_mt = is_mt.lower()
        # logger.warn("MT enabled: %s " % self.is_mt )
        
        if _platform == "linux" or _platform == "linux2":
            # linux
            self.os_atf_path = LINUX_ATF_PATH
        elif _platform == "darwin":
            self.os_atf_path = MAC_ATF_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            self.os_atf_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.kNumSoftKeys = 5
        self.event_timeout = 7
        self.max_oneway_retry = 2
        self.force_idle_timeout = 15

        # self.phone = self.ip4xx_user
        #
        # for key in self.ip4xx_user:
        #     #print key
        #     setattr(self, key, self.ip4xx_user[key])
        # print (self.ip4xx_user.extension)

        self.phone = IP4xxInterfacebase(self.ip4xx_user)

        self.pphone_hq_rsa = os.path.join(self.os_atf_path, 'phone_wrappers','rsa_keys',ip4xx_user['hq_rsa'])

    def extensionNumber(self):
         extensionNumber = self.phone['extension']
         return (extensionNumber)
        
    def pphone_user_ssh_cmd(self, user, cmd):
        """Runs cmd via ssh on pphone user
        
        :param user: user dict
        :type user: type dict
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(user['ip'],username="admin",key_filename=self.pphone_hq_rsa)

        logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, user['ip']))
        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result     
        
    def scp_put(self, file):
        """Runs cmd via ssh on pphone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        logger.warn(file)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip4xx_user['ip'],username="admin",key_filename=self.pphone_hq_rsa)

        with SCPClient(ssh.get_transport()) as scp:
           scp.put(file)
          
        if ssh:
            ssh.close()
              
    def scp_get(self, file):
        """Runs cmd via ssh on pphone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        logger.warn(file)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip4xx_user['ip'],username="admin",key_filename=self.pphone_hq_rsa)

        with SCPClient(ssh.get_transport()) as scp:
           scp.get(file)

        if ssh:
            ssh.close()
                        
    def pphone_ssh_cmd(self, cmd):
        """Runs cmd via ssh on pphone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip4xx_user['ip'],username="admin",key_filename=self.pphone_hq_rsa)

        logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.ip4xx_user['ip']))
        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result
        
    def pphone_ssh_su_cmd(self, cmd):
        """Runs cmd via ssh as su on pphone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip4xx_user['ip'],username="admin",key_filename=self.pphone_hq_rsa)
    
        pswd = 'U2hvcmVUZWw='
        cmd = "echo " + base64.b64decode(pswd) + " | su -c \"" + cmd + "\""
        logger.info("Running ssh cmd: \"%s\"" % cmd)
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result

    def pphone_ssh_dm(self, cmd, dm_query, user=None):
        """Runs cmd dm_query using ssh on pphone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :param dm_query: Run dm_query
        :type dm_query: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not dm_query does not match
        """
        sys_cmd = ' '.join([cmd,dm_query])
        for i in range(0,3):
            if user is None:
                result = self.pphone_ssh_cmd(sys_cmd)
            else:
                result = self.pphone_user_ssh_cmd(user, sys_cmd)
                
            if isinstance(result, list):
                result = ''.join(result)
            matchObj = re.match(r'.*->(.*)->Terminated.*', result, re.DOTALL)
            if matchObj:
               dm_pair = matchObj.group(1).rstrip('\r\n')
               dm_pair = dm_pair.split("=")
               
               if "PPhoneDM" in dm_query:
                   dm_query = dm_query.split('.')[1]
               if dm_query in dm_pair[0].strip():
                   print("\"%s\" matched returning \"%s\"" % (dm_query, dm_pair[1]))
                   return dm_pair[1].strip()
               else:
                   raise Exception("%s did not match %s in pphone_ssh_dm" % (dm_query, dm_pair[0]))
             
        raise Exception("pphone_ssh_dm: \"%s\" match not found in result %s." % (dm_query, result))

    def pphone_reboot_phone(self):
        """ Reeboots pphone
        
        """
        self.pphone_ssh_cmd("/sbin/reboot")
            
    def pphone_cloudboot(self, dns_ip):
        """ Performs cloudboot on pphone
        
        :param dns_ip: dns ip
        :type dns_ip: type string
        """
        import socket
        try:
            socket.inet_aton(dns_ip)
        except:
            raise Exception("DNS IP %s is not valid"%dns_ip)

        replace_dns_cmd = "sed -i 's/dnsAddress.*/dnsAddress=%s/g' /nvdata/config/pphone.conf" % dns_ip
        result = self.pphone_ssh_su_cmd(replace_dns_cmd)
        
        clear_svc_cmd = "sed -i 's/svcLocationCache.*/svcLocationCache=/g' /nvdata/config/pphone.conf"
        result = self.pphone_ssh_su_cmd(clear_svc_cmd)

        rm_hq_cert_cmd = "rm /nvdata/config/cert/hq/hq_*"
        result = self.pphone_ssh_su_cmd(rm_hq_cert_cmd)
        #reboot phone
        self.pphone_reboot_phone()
        
        # os this stepo necessary
        # catch {file delete -force "phoneutil/rsa_keys/backdoor"}
                
    def pphone_begin_vm_code_capture(self):
        """Starts vmcodeserver

        :return ret_val: ssh cmd result
        :rtype: str
        """
        self.pphone_end_vm_code_capture()
        
        # Make sure PCMU8000 codec is used
        #config InitializeUCBCodec

        cmd = 'vmcodeserver >/var/log/vmcodeserver.log 2>&1 &'
        return self.pphone_ssh_su_cmd(cmd)
        
    def pphone_end_vm_code_capture(self):
        """Stop the VM capture by killing the process
        
        :return ret_val: ssh cmd result
        :rtype: str
        """
        cmd = '"kill -9 `pidof vmcodeserver`"'
        return self.pphone_ssh_su_cmd(cmd)
                        
    def wait_for_crypto_key(self, ca):
        """This function waits for the crypto key to be present.
        
        :param ca: Specify the Call appearance number
        :type ca: type int
        :return ret_val: returns the Crypto key
        :rtype: str
        """
        # NOTE other implementation needs cryto key
        # For now it is ok for crypto key to be empty
        str = ""
        
        return str
      
    def pphone_wait_for_vm_code(self, vmcode, ca="RIGHT_LINE1", mode="separate"):
        """This function waits for VM code in the ca specified
        
        :param vmcode: Specify the Vm code
        :type vmcode: type int
        :param ca: Specify the call appearance
        :type ca: type str
        :param ca: Specify the mode
        :type ca: type str
        :return ret_val: None
        :rtype: None
        """
        try: 
            port = 5667
            timeout = 12000
            vmcode = vm_codes.VMCODES[vmcode]
            
            mode = int(mode == "inline")
            crypto_key = self.wait_for_crypto_key(ca)
            
            cmd= "%s,%s,%s,%s" % (crypto_key,vmcode,timeout,mode)
            logger.info("Sending vmcode command: %s"% cmd)
           
            tn = telnetlib.Telnet(self.ip4xx_user['ip'], port)
            tn.write(str(cmd))

            line = ""
            timeout = time.time() + timeout
            while True:
                if time.time() > timeout:
                    break
                line =  tn.read_eager()
                # line =  tn.read_very_eager()
                if line != "":
                    break 
                time.sleep(0.2)

            tn.close()
            if line != "1":
                logger.warn("Vmcode %s NOT Found: FAIL:" % vmcode)
                raise Exception()
            logger.info("Vmcode %s Found: PASS" % vmcode)
        except Exception as err:
            tn.close()
            raise Exception("func '%s' - err: '%s'!" % (sys._getframe().f_code.co_name, err))
        tn.close()

    def pphone_get_popup(self):
        """Returns last popup displayed on the phone
            This method always retains the last popup
            that was displayed on the phone


        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        return str(self.pphone_ssh_dm( "cli -c getdm", "PPhoneDM.QA_TEST_MONITOR_popMessages"))
   
    def getdm_session_count(self):
        """Returns number of sessions
        
        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        return int(self.pphone_ssh_dm( "cli -c getdm", "callstackdm.sessionCount"))
   
        
    def getdm_conference_session_count(self):
        """Returns number of sessions in conference
        
        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        # reimplement to allow use case of more than one conf
        session_count = -1
        for i in range(1,6):
            dm_query = "callstackdm.session%s.iden.displayname"%i
            display = self.pphone_ssh_dm("cli -c getdm", dm_query)
            if "Conference" in display:
                dm_query = "callstackdm.session%s.conferencelistdm.sessionCount"%i
                session_count = self.pphone_ssh_dm("cli -c getdm", dm_query)
                break

        return session_count

    def getdm_call_handling_mode(self):
        """Returns call handling mode
        
        :return ret_val: call handling mode
        :rtype: str
        """
        return self.pphone_ssh_dm("cli -c getdm", "user.callHandlingMode")
   
    def verify_pphone_call_handling_mode(self, mode):
        """Returns call handling mode
        
        :return ret_val: call handling mode
        :rtype: str
        """
        themode = self.getdm_call_handling_mode()
        if themode != mode:
            raise Exception('chm mode actual "%s" did not match expected "%s"' % (mode,themode))

    def getdm_active_audio_path(self, user=None):
        """Returns active audio path
        
        :return ret_val: Active audio path, kDevice_Handset 0, kDevice_Speaker 1, kDevice_Headset 2
        :rtype: str
        """
        if user is None:
            return self.pphone_ssh_dm( "cli -c getdm", "audio.activeDevice")
        return self.pphone_ssh_dm( "cli -c getdm", "audio.activeDevice", user)
		
    def pphone_get_progbutton_info(self, btn=1):
        """Returns active audio path
        
        :rtype: str
        """
        btninfo = self.pphone_ssh_dm( "cli -c getdm", "progbuttons.0.%s.param"%btn).split(';')
        return btninfo		
        	
        
    def getdm_pphone_muted(self):
        """Returns (on/off) if phone is muted
        
        :return ret_val: On if phone muted else off
        :rtype: str
        """
        return self.pphone_ssh_dm( "cli -c getdm", "audio.muteOn")

    def verify_pphone_held(self):
        sessioncount = self.getdm_session_count()
        print "getdm session count : %s "%sessioncount
        phonestate = self.pphone_ssh_dm("cli -c getdm", "callstackdm.session%s.QA_TEST_MONITOR_HOLD_STATE"%sessioncount)
        print "getdm phone state : %s "%phonestate
        if phonestate == "isHeld":
            print "Hold verified"
            return 1
        else:
            raise Exception("verify_pphone_held: Pphone is not held")
        
                
    def getdm_caller_number(self, ca):
        """Returns (on/off) if phone is muted
        
        :param ca: Call appearance
        :type ca: type string
        :return ret_val:  Returns caller number on ca
        :rtype: str
        """
        session = self._pphone_get_callstackdm_session(ca)
        cmd = "callstackdm."+session+".iden.displaynumber"
        
        return self.pphone_ssh_dm("cli -c getdm", cmd)

    def verify_pphone_idle(self):
        """Verifies if phone user is idle
        
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not idle
        """
        sessioncount = self.getdm_session_count()
        if  sessioncount == 0:
            print("verify_pphone_idle: Pphone is idle")
        else:
            raise Exception("verify_pphone_idle: Session count = \"%s\" pphone is not idle" % sessioncount)
        
    def verify_pphone_muted(self):
        """Verifies if phone user is mutes
        
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not muted
        """
        if self.getdm_pphone_muted() == "on":
            print("MUTE verified")
        else:
            raise Exception("verify_pphone_muted: Pphone is not muted")
        
    # def verify_pphone_active_audio_path(self, audiopath):

    def get_pphone_active_audio_path(self):
        """Verifies if phone user is idle
        
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        path = int(self.getdm_active_audio_path())
        return path

 ########################################################
 #     PPHONE KBD SERVER METHODS
 ########################################################
    
    def pphone_press_button(self, button):
        """Press Button on Pphone via kbd socket
        
        :param button: Char value for button mapping
        :type button: type str
        :return ret_val: none
        """
        logger.info("Running kbd socket cmd \"%s\" on phone %s" % (button, self.ip4xx_user['ip']))
        tn = telnetlib.Telnet(self.ip4xx_user['ip'], kKbd_Socket)
        tn.write(str(button))
        time.sleep(1)
            
    def pphone_press_button_raw(self, button):
        """Press Button on Pphone via kbd socket
        
        :param button: Char value for button mapping
        :type button: type str
        :return ret_val: none
        """
        print("Running kbd socket cmd \"%s\" on phone %s" % (button, self.ip4xx_user['ip']))
        tn = telnetlib.Telnet(self.ip4xx_user['ip'], kKbd_Socket)
        tn.write(button + "\n")
        time.sleep(1)

        
    def pphone_dial_digits(self, digits):
        """Dial Digits via kbd socket
        
        :param digits: string of digits
        :type digits: type str
        :return ret_val: none
        """
        print("Running kbd socket cmd \"%s\" on phone %s" % (digits, self.ip4xx_user['ip']))
        tn = telnetlib.Telnet(self.ip4xx_user['ip'], kKbd_Socket)
        tn.write(str(digits) + "\n")

    def pphone_press_button_pound(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Pound)
        
    def pphone_press_button_hash(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Hash)
        
    def pphone_press_button_star(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Star)
        
    def pphone_press_button_conference(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Conference)
        
    def pphone_press_button_directory(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Directory)
        
    def pphone_press_button_headset(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Headset)
        
    def pphone_press_button_hold(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Hold)
        
    def pphone_handset_up(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Hookswitch_Up)
        
    def pphone_handset_down(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button( kButton_Hookswitch_Down)
                
    def pphone_handset_disconnect_call(self):
        """Press PPhone button via kbd server

        :return ret_val: none
        """
        self.pphone_handset_up()
        self.pphone_handset_down()
        
    def pphone_press_button_rightLine1(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_RightLine1)
        
    def pphone_press_button_rightLine2(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_RightLine2)
        
    def pphone_press_button_rightLine3(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_RightLine3)
        
    def pphone_press_button_rightLine4(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_RightLine4)
        
    def pphone_press_button_leftLine1(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_LeftLine1)
        
    def pphone_press_button_leftLine2(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_LeftLine2)
        
    def pphone_press_button_leftLine3(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_LeftLine3)
        
    def pphone_press_button_leftLine4(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_LeftLine4)
        
    def pphone_press_button_up(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Up)
        
    def pphone_press_button_down(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Down)
        
    def pphone_press_button_left(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Left)
        
    def pphone_press_button_right(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Right)
        
    def pphone_press_button_softkey1(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Softkey1)
        
    def pphone_press_button_softkey2(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Softkey2)
        
    def pphone_press_button_softkey3(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Softkey3)
        
    def pphone_press_button_softkey4(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Softkey4)
        
    #  TODO def pphone_press_button_softkey5(self):
        
    def pphone_press_button_mute(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Mute)
        
    def pphone_press_button_redial(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Redial)
        
    def pphone_press_button_enter(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Enter)
        
    def pphone_press_button_fire(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Fire)
        
    def pphone_press_button_backspace(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Backspace)
        
    def pphone_press_button_speaker(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Speaker)
        
    def pphone_press_button_transfer(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_Transfer)
        
    def pphone_press_button_voicemail(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        # self.pphone_press_button(kButton_Voicemail)
        self.pphone_press_button("V")
        
    def pphone_press_button_volumeDown(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_VolumeDown)
        
    def pphone_press_button_volumeUp(self):
        """Press PPhone button via kbd server
        
        :return ret_val: none
        """
        self.pphone_press_button(kButton_VolumeUp)
         
########################################################
 #     PPHONE SOCKET INTERFACE METHODS
 ########################################################
   
    def si_query(self, user_from, query):
        """Socket Interface main cmd method
        
        :param query: Query to be run on socket interface
        :type query: type str
        :return ret_val: Result of query
        """
        #  TODO replace with log level
        logger.info("Running socket cmd: %s on phone %s" % (query, user_from['ip']))
        tn = telnetlib.Telnet(user_from['ip'], Interface_Socket)
        tn.write(str(query) + "\n")
        return tn.read_some()
        
    def pphone_get_led_state(self, socket_led, state):
        """
        :param socket_led: LED state
        :type socket_led: type str
        :param state: state (color or pattern)
        :type state: type str
        :return ret_val: None
        """
        if state == "color":
            ret = socket_led[2]
        elif state == "pattern":
            ret = socket_led[3]
        else:
            logger.warn("State {} does not exist".format(state))
            raise Exception("")
        return ret     
        
    def pphone_verify_led_color(self, socket_led, color):
        """
        :param socket_led: LED state
        :type socket_led: type str
        :param colot: LED color
        :type color: type str
        :return ret_val: None
        """
        if kLED_Colors[color] != self.pphone_get_led_state(socket_led, "color"):
            raise Exception("LED state {} color is not {}:{}".format(socket_led,color,kLED_Colors[color]))
        return None  
         
    def pphone_verify_led_pattern(self, socket_led, led_pattern):
        """
        :param socket_led: LED state
        :type socket_led: type str
        :param led_pattern: pattern (on, off, blinking)
        :type led_pattern: type str
        :return ret_val: None
        """
        if led_pattern == "blinking":
            if "_" not in self.pphone_get_led_state(socket_led, "pattern"):
                raise Exception("LED state {} LED is not blinking".format(socket_led,led_pattern))
        elif led_pattern not in self.pphone_get_led_state(socket_led, "pattern"):
            raise Exception("LED state {} LED is not {}".format(socket_led,led_pattern))
        return None
        
    def pphone_verify_led_state(self, ca, color, led_pattern):
        """
        :param ca: call appearance
        :type ca: type str
        :param color: LED color
        :type color: type str
        :param led_pattern: pattern (on, off, blinking)
        :type led_pattern: type str
        :return ret_val: None
        """
        query = " ".join(["getline",kCA_lines[ca.lower()],kPos_LED])
        tn = telnetlib.Telnet(self.ip4xx_user['ip'], Interface_Socket)
        tn.write(str(query) + "\n")
        result = tn.read_some()    
        
        socket_led = result.split('\x1e')
        
        self.pphone_verify_led_color(socket_led, color)
        self.pphone_verify_led_pattern(socket_led, led_pattern)
        
        return None

    def pphone_search_softkey_text(self, text):
        """Searches for softkey text
        
        :param text: Softkey text to be searched
        :type text: type str
        :return ret_val: Index of softkey, -1 if not found
        """
        pattern = ".*%s" % text
        for i in range(0,self.kNumSoftKeys):
            cmd = "getsk sk{0}".format(i) 
            sk = self.si_query(self.ip4xx_user,cmd)
            #  Check if sk is empty
            if not re.match(".*png",sk):
                #  TODO  softkey has no image, procees
                #  TODO  remove RS char from sk
                if len(sk.strip()) < 8:
                    print("Skipping empty softkey %s" % sk)
                    continue
                sk_text = sk.split("5")[1].strip()
                print sk_text
            else:
                str = sk.split(":")
                sk_img = str[1]
                str = str[0].split("5")
                sk_text =  str[1]
            if re.match(pattern,sk_text): 
                print("Text %s found at index %d" % (text,i))
                return i
        print("Text %s not found" % text)
        return -1
        

    def wait_for_active_audio_device(self, audio_device):
        """Polls for ca_type match on line ca_line for timeout time
        
        :param audio_device: Audio device path
        :type audio_device: string
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        num_tries = 3
        for i in range(0,num_tries):
            time.sleep(1)
            logger.info("wait_for_active_audio_device %s attempt: %s" % (audio_device, i))
            path = self.get_pphone_active_audio_path()

            if path == audio_device:
                logger.info("Audio device \"%s\" matched \"%s\"" % (audio_device,path))
                return
            else:
                if audio_device == kDevice_Handset:
                    self.pphone_press_button(kButton_Hookswitch_Up)
                elif audio_device == kDevice_Speaker:
                    self.pphone_press_button(kButton_Speaker)
                elif audio_device == kDevice_Headset:
                    self.pphone_press_button(kButton_Headset)
                else:
                    raise Exception("wait_for_active_audio_device:  AudioPath %s does not exist" % audio_device)
        raise Exception("wait_for_active_audio_device: Audio path expected \"%s:%s\". Does not match actual \"%s:%s\"" % (deviceMap[audio_device],audio_device,deviceMap[path],path))
		
    def wait_for_call_appearance(self, ca_type, ca_line):
        """Polls for ca_type match on line ca_line for timeout time
        
        :param ca_type: Call appearance type
        :type ca_type: type str
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        ca_lines = {'right_line1': 'line0', 'right_line2': 'line1', 'right_line3': 'line2', 'right_line4': 'line3', 'left_line1': 'line4', 'left_line2': 'line5', 'left_line3': 'line6', 'left_line4': 'line7', }
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        line = ca_lines[ca_line.lower()]
        cmd = "getline " + line + " 1"
        pattern = ".*%s" % ca_type
        timeout = time.time() + self.event_timeout
        while True:
            time.sleep(1)
            resp = self.si_query(self.ip4xx_user, cmd)
            
            # TODO - workaround since returned val cuts off chars (ie. return .p instead of .png)
            resp = resp.split('images')[1]
            if resp.strip() in pattern:
                break
            if time.time() > timeout:
                raise Exception("Actual: \"%s\" is not in Expected: \"%s\"" % (resp, pattern))
                break
            #  TODO replace with log level
            print("sleeping 1 second for pattern %s" % pattern)

    def wait_for_idle_call(self, ca_line):
        """Polls for idle state match on line ca_line
        
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(kCallAppearance_idleCall, ca_line)
     
    def wait_for_dialing_call(self, ca_line):
        """Polls for dialing state match on line ca_line
        
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        if self.ip4xx_user['phone_model'] == 'p8cg':
            self.wait_for_call_appearance(kCallAppearance_p8cg_dialingCall, ca_line)
        elif self.ip4xx_user['phone_model'] == 'p8':
            self.wait_for_call_appearance(kCallAppearance_p8_dialingCall, ca_line)
        elif self.ip4xx_user['phone_model'] == 'p2':
            self.wait_for_call_appearance(kCallAppearance_p2_dialingCall, ca_line)
        else:
		    raise Exception("Phone type %s does not exist")
     
    def wait_for_incoming_call(self, ca_line):
        """Polls for icoming state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        if self.ip4xx_user['phone_model'] == 'p8cg':
            self.wait_for_call_appearance(kCallAppearance_p8cg_incomingCall, ca_line)
        elif self.ip4xx_user['phone_model'] == 'p8':
            self.wait_for_call_appearance(kCallAppearance_p8_incomingCall, ca_line)
        elif self.ip4xx_user['phone_model'] == 'p2':
            self.wait_for_call_appearance(kCallAppearance_p2_incomingCall, ca_line)
        else:
		    raise Exception("Phone type %s does not exist")
     
     
    def wait_for_connected_call(self, ca_line):
        """Polls for connected state match on line ca_line
        
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(kCallAppearance_connectedCall, ca_line)
             
    def wait_for_local_hold_call(self, ca_line):
        """Polls for local hold state match on line ca_line
        
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(kCallAppearance_localHold, ca_line)
        
    def wait_for_remote_hold_call(self, ca_line):
        """Polls for remote hold state match on line ca_line
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(kCallAppearance_remoteHold, ca_line)
        

    def answer_via_headset(self, user_callee):
        """Answers call via headset
        
        :param user_callee: User dict
        :type user_callee: type dict
        :return ret_val: none
        """
        self.pphone_press_button_headset(user_callee)
       
    def pphone_verify_caller_name(self, user_callee, user_caller):
        """Verifies if user_caller is called by user_callee
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: 1 if matched else 0
        :raises ExceptionType: Raises robot exception if no match
        """
        pattern = ".*%s" % user_caller.first_name
        resp = self.si_query(user_callee, "getline line0 3")
        if re.match(pattern, resp):
            return 1
        else:
            raise Exception("answer_verify_caller: user %s was not matched" % user_caller.first_name)
        return 0
     
    def pphone_si_verify_caller_number(self, user_callee, user_caller, ca, num_format):
        """Verifies if user_caller is called by user_callee
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: 1 if matched else 0
        :raises ExceptionType: Raises robot exception if no match
        """
        if num_format == "extension":
            pattern = ".*%s" % user_caller.extension
        if num_format == "sip_trunk_did":
            pattern = "%s" % user_caller.sip_did
            logger.info("Looking for user %s number %s" %(user_caller.first_name,pattern))
            reNum = re.search(r'^(\d?)(\d{3})(\d{3})(\d{4})$',pattern)
            pattern = "\("+ reNum.group(2) + "\)"+ reNum.group(3) + "-" + reNum.group(4) 


        resp = self.si_query(user_callee, "getline line0 3")
        pnum = resp.split('\x1e')[2]
        logger.info("Socket Interface returned number %s" % pnum)
        if re.match(pattern, pnum):
            return 1
        else:
            raise Exception("pphone_si_verify_caller_number: user %s did not match re pattern %s with %s" % (user_caller.first_name, pattern, resp))
        return 0

    def _pphone_get_callstackdm_session(self, call_appearance):
        """Returns the callstackdm session number
        
        :param call_appearance: Call appearance
        :type call_appearance: type string
        :return ret_val:  Returns session number
        :rtype: str
        """
        ca_lines = {'right_line1': '0', 'right_line2': '1', 'right_line3': '2', 'right_line4': '3', 'left_line1': '4', 'left_line2': '5', 'left_line3': '6', 'left_line4': '7', }

        ca_num = ca_lines[call_appearance.lower()]

        #Get list of session numbers
        result = self.pphone_ssh_cmd( "cli -c getdm callstackdm|grep callAppearance" )
        # logger.warn(result)
        # result = result.splitlines()
        for line in result:
            if "session" in line:
               #Cycle through sessions
                session_num = line.split('.')[1]
                ca = line.split('=')[1]
                if ca_num in ca:
                    #logger.warn("PASS: session found \"%s\"" % session_num)
                    return session_num
        logger.warn("FAIL: session not found")
        raise Exception("_pphone_get_callstackdm_session: Session num \"%s\" not found" % ca_num)

    def pphone_verify_caller_number(self, user_callee, ca='RIGHT_LINE1', num_format='extension'):
        """Verifies if user_caller is called by user_callee
        
        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: 1 if matched else 0
        :raises ExceptionType: Raises robot exception if no match
        """
        if num_format == "extension":
            pattern = ".*%s" % user_callee['extension']
        if num_format == "sip_trunk_did":
            pattern = ".*%s" % user_callee['sip_did']

        caller_number = self.getdm_caller_number(ca)
        if re.match(pattern, caller_number):
            return 1
        else:
            raise Exception("pphone_verify_caller_number: Pattern %s did not match caller_number \"%s\" for number format %s " % (pattern, caller_number,num_format))
        return 0
              
    def pphone_make_call(self, user_to, ca_line="RIGHT_LINE1"):
        """Makes call from user_from to user_to on ca_line
        
        :param user_to: User dict
        :type user_to: type dict
        :param ca_line: Call appearance line on which to make call
        :type ca_line: type str
        :return ret_val: none
        """
        tn = telnetlib.Telnet(self.ip4xx_user['ip'], kKbd_Socket)
        tn.write(str(user_to['extension']) + "\n") 

    def pphone_disconnect_call_via_softkey(self):
        """Disconnects user_callee call via softkey
        
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        index = self.pphone_search_softkey_text("Hang Up")
        if index == -1:
            raise Exception("disconnect_call_via_softkey: Failed softkey search for \"Hang Up\"")
        self.pphone_press_button(kButton_Softkeys[index])

    def pphone_disconnect_call(self, mode="-1"):
        """Disconnects user call via mode
        
        :param mode: handset-0, speaker-1, headset-2
        :type mode: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        audiopath = int(self.getdm_active_audio_path())
        if mode == "-1":
            if audiopath == kDevice_Handset:
                self.pphone_handset_down()
            elif audiopath == kDevice_Speaker:
                self.pphone_press_button(kButton_Speaker)
            elif audiopath == kDevice_Headset:
                self.pphone_press_button(kButton_Headset)
            else:
                raise Exception("disconnect_call: AudioPath %s does not exist" % audiopath)
        else:
            self.pphone_disconnect_call_via_softkey()
            # self.pphone_press_button(user_callee, mode)
        if self.getdm_session_count() != 0:
            self.pphone_disconnect_call_via_softkey()

    def pphone_answer_call(self, ca_line="RIGHT_LINE1", audio_path="-1"):
        """Disconnects user call via mode
        
        :param ca_line: Call appearance line to check incoming call
        :type ca_line: type str
        :param audio_path: handset-0, speaker-1, headset-2
        :type audio_path: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        self.wait_for_incoming_call(ca_line)
        if audio_path == "-1":
            audio_path = kDevice_Handset

        logger.info("audio path is %s" % audio_path)
        if audio_path == kDevice_Handset:
            self.pphone_press_button( kButton_Hookswitch_Up)
        elif audio_path == kDevice_Speaker:
            self.pphone_press_button( kButton_Speaker)
        elif audio_path == kDevice_Headset:
            self.pphone_press_button( kButton_Headset)
        else:
            raise Exception("answer_call:  AudioPath %s does not exist" % audio_path)
            return
        self.wait_for_active_audio_device( audio_path)
        
    def pphone_verify_call_duration	(self, user_caller):
        pass

    def pphone_hold_call(self, ca_line):
        """Holds and verifies call held
        
        :param ca_line: Call appearance line to check call hold
        :type ca_line: type str
        :return ret_val: none
        """
        self.pphone_press_button_hold()
        self.wait_for_local_hold_call(ca_line)
        
        
# Audio devices
#  kDevice_Handset 0
#  kDevice_Speaker 1
#  kDevice_Headset 2

    def pphone_pxcon_init_audio(self):
        # Initializing modules to play audio via pxcon
        # This function need run only one time unless the phone is reboot
        self.pphone_ssh_cmd( "/bin/ash /bin/pxaudio_init.sh" )

    def pxcon_create_audio_inject_handle(self, user, audioPath):
        mode = "repeat"
        syncType = "sync"
        filename = ""

        device = deviceMap[audioPath]

        if device == 0:
            filename = "16k_500.pcm"
            self.pphone_user_ssh_cmd(user, "pxcon /bin/pxinject_audiohandset.sh")
        elif device == 1:
            filename = "16k_3k.pcm"
            self.pphone_user_ssh_cmd(user, "pxcon /bin/pxinject_audiospeaker.sh")
        elif device == 2:
            filename = "16k_1k.pcm"
            self.pphone_user_ssh_cmd(user, "pxcon /bin/pxinject_audioheadset.sh")
        else:
            print("Device %s is not known!" % device)
        print("Preparing to inject \\etc\\apt\\%s on device: %s mode: %s" % (filename, device, mode))

    def pxcon_create_audio_capture_handle(self, user, audioPath):
        mode = "truncate"
        syncType = "sync"
        filename = ""

        device = deviceMap[audioPath]

        if device == 0:
            filename = "/tmp/handsetcapture.pcm"
            self.pphone_user_ssh_cmd(user, "pxcon /bin/pxcapture_audiohandset.sh")
        elif device == 1:
            filename = "/tmp/speakercapture.pcm"
            self.pphone_user_ssh_cmd(user, "pxcon /bin/pxcapture_audiospeaker.sh")
        elif device == 2:
            filename = "/tmp/headsetcapture.pcm"
            self.pphone_user_ssh_cmd(user, "pxcon /bin/pxcapture_audioheadset.sh")
        else:
            print("Device %s is not known!" % device)
        print("Preparing to capture %s on device: %s mode: %s" % (filename, device, mode))

    def pxcon_sync_enable_audio(self, user):
        print("Playing/Enabling audio on %s..." % self.ip4xx_user['ip'])
        self.pphone_user_ssh_cmd(user, "killall pxcon; pxcon /bin/pxsync_enable.sh")

    def pxcon_sync_disable_audio(self, user):
        print("Audio Stopped/Disabled on %s " % self.ip4xx_user['ip'])
        self.pphone_user_ssh_cmd(user, "killall pxcon; pxcon /bin/pxsync_disable.sh")

    def pxcon_remove_audio_handles(self, user):
        print("Removing pxcon audio handles")
        self.pphone_user_ssh_cmd(user, "killall pxcon; pxcon /bin/pxrm_audioh.sh; rm /tmp/*capture.pcm")
        print("Pxcon audio utils flushed and removed")

    def pphone_check_one_way_audio(self, user_capture):
        inj_activeAudioDevice = int(self.getdm_active_audio_path(self.ip4xx_user))
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        device = halAudioMap[inj_activeAudioDevice]
        other_device = halAudioMap[cap_activeAudioDevice]

        for i in range(0,self.max_oneway_retry):
            audioPassed = 1
            self.pxcon_create_audio_inject_handle(self.ip4xx_user, device)
            self.pxcon_create_audio_capture_handle(user_capture, other_device)

            self.pxcon_sync_enable_audio(self.ip4xx_user)
            self.pxcon_sync_enable_audio(user_capture)
            time.sleep(3)
            self.pxcon_sync_disable_audio(user_capture)
            self.pxcon_sync_disable_audio(self.ip4xx_user)
 
            freq = self.get_estimated_frequency(user_capture)

            self.pxcon_remove_audio_handles(self.ip4xx_user)
            self.pxcon_remove_audio_handles(user_capture)
        
            if freq == 2666:
                print("2k Hz sine tone detected on handset")
                if inj_activeAudioDevice != 0:
                    audioPassed = 0
                    print("Audio is not playing from injector handset")
            elif freq == 4000:
                print("3k Hz sine tone detected on speaker")
                if inj_activeAudioDevice != 1:
                    audioPassed = 0
                    print("Audio is not playing from injector speaker")
            elif freq == 500:
                print("500 Hz sine tone detected on headset")
                if inj_activeAudioDevice != 2:
                    audioPassed = 0
                    print("Audio is not playing from injector headset")
            else:
                audioPassed = 0
                print("Unkown frequency detected")
            if audioPassed == 1:
                print("Audio check PASSED")
                return
        if audioPassed == 0:
            raise Exception("One-way audio check FAILED")


    def pphone_check_no_audio(self, user_capture): 
        pass
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        # inj_activeAudioDevice = int(self.getdm_active_audio_path(self.ip4xx_user))
        # cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        # device = halAudioMap[inj_activeAudioDevice]
        # other_device = halAudioMap[cap_activeAudioDevice]

        # for i in range(0,self.max_oneway_retry):
            # audioPassed = 1
            # self.pxcon_create_audio_inject_handle(self.ip4xx_user, device)
            # self.pxcon_create_audio_capture_handle(user_capture, other_device)

            # self.pxcon_sync_enable_audio(self.ip4xx_user)
            # self.pxcon_sync_enable_audio(user_capture)
            # time.sleep(3)
            # self.pxcon_sync_disable_audio(user_capture)
            # self.pxcon_sync_disable_audio(self.ip4xx_user)
 
            # #Check below should not detect any frequency
            # freq = str(self.get_estimated_frequency(user_capture))

            # self.pxcon_remove_audio_handles(self.ip4xx_user)
            # self.pxcon_remove_audio_handles(user_capture)

            # if "2666" in freq:
                # print("2k Hz sine tone detected")
                # audioPassed = 0
            # elif "4000" in freq:
                # print("3k Hz sine tone detected")
                # audioPassed = 0
            # elif "500" in freq:
                # print("500 Hz sine tone detected")
                # audioPassed = 0
            # else:
                # # audioPassed = 0
                # print("Frequency: %s detected" % freq)
            
            # if audioPassed == 1:
                # print("Audio check PASSED")
                # return
        # if audioPassed == 0:
            # raise Exception("No audio check FAILED")

    def pphone_check_two_way_audio(self, other_user ):
        """ This function is deprecated in OOP version
            
             call check one way audio instead on 
             each phone     """
        logger.warn("This function is deprecated in OOP version call check one way audio instead on each phone")
        pass
        

    def get_estimated_frequency(self, user_capture):
        samplerate = 16000
        skip_samples = 10000
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        # files = ["/tmp/handsetcapture.pcm", "/tmp/speakercapture.pcm", "/tmp/headsetcapture.pcm"]
        files = [2666,4000,500]
        filename = files[cap_activeAudioDevice]

        # cmd = "estimate_freq " + str(samplerate) + " " + str(skip_samples) + " < " + filename
        # print("Running cmd \"%s\"" % cmd)
        # result = self.pphone_ssh_cmd(user_capture, cmd)
        # print("estimated freq: %s" % result)
        return filename

 ########################################################
 #     VOICEMAIL
 ########################################################

    def pphone_create_new_voicemail(self,user_to, number = 1,length="short",subject="Robot Automation"):
        """Creates new voicemail files on a vm server
        
        :param user_to Voice Mailbox name
        :param subject Specify the subject
        :param number Number of voicemails to create
        :param length Optional short
        :param subject Voice Mail "Robot Automation"

        :return message as string
        """
        # TODO remove hard coded VM PATH
        wav_file = "c:\\ATF_ROBOT\\testdata\\vm_{0}.wav".format(length)
        if not os.path.isfile(wav_file):
            raise Exception("pphone_create_new_voicemail: \"%s\" not found for creating VM" % wav_file)
        
        # TODO Add support for MT
        
        self.pphone_create_voicemail_files(user_to,subject,number)
        if(self.pphone_upload_voicemail_files(user_to,wav_file)):
            self.pphone_run_voicemail_command(user_to)
        else:
            raise Exception("pphone_create_new_voicemail: failed to create VM" % wav_file)
        
        logger.info("Created %s voicemails on %s user %s" % (number,user_to.server,user_to['ip']))
        time.sleep(2)

    def pphone_create_voicemail_files(self,user_to,user_from,subject,number=1,wav_path="DEFAULT"):
        """Create snew voicemail files on a vm server
        
        :param user_to Voice Mailbox name
        :param subject Specify the subject
        :param number Number of voicemails to create
        :param wav_path Optional DEFAULT
        
        :return Nothing
        """
        if os.path.isfile("VM_COMMANDS"):
            os.remove("VM_COMMANDS")
        fh = open("VM_COMMANDS",'w')
        
        if wav_path == "DEFAULT":
            #This is the NAS
            wav_path = "c:\\inetpub\\ftproot\\vm.wav"
        
        for i in range(0,int(number)):
            fh.write("rstmsg2 \"%s\" %s \"%s\" \"%s\"\n" % (wav_path,user_to.extension,self.ip4xx_user.extension,subject))
        
        fh.write("exit")
        fh.close()
        
    def pphone_upload_voicemail_files(self,user_to,wav_file):
        """Uploads the voicemail files on a vm server
        :param user_to user dict
        :param wav_file Specify the audio file to be uploaded
        :return true if the upload is successfull else false
        """
        ftp = ftplib.FTP()
        try:
            ftp.connect(user_to.server)
            ftp.login(user_to.hq_username,user_to.hq_password)
        except socket.error,e:
            print 'unable to connect!,%s'%e
            ftp.quit()
            return 0
        logger.info("FTP CONNECTED")
        
        #create pphone dir to store VM file
        if user_to['ip'] not in ftp.nlst():
            ftp.mkd(user_to['ip'])
        ftp.cwd(user_to['ip'])
        
        res = ftp.storbinary("STOR VM_COMMANDS", open("VM_COMMANDS", "rb"))
        if "complete" not in res:
            raise Exception("pphone_upload_voicemail_files: failed to upload VM command file")
        
        ftp.cwd("..")
        res = ftp.storbinary("STOR vm.wav", open(wav_file, "rb"))
        if "complete" not in res:
            raise Exception("pphone_upload_voicemail_files: failed to upload VM wav file")
            ftp.quit()
            return 0
        ftp.quit()
        return 1

    def pphone_run_voicemail_command(self,user_to,vm_cmd_file="DEFAULT"):
        """This function runs the voice mail command on the HQ
        :param user_to user dict
        :param vm_cmd_file optional DEFAULT
        :return Nothing
        """
        # It looks like cfg.exe can be called without a path
        # TODO remove hard coded VM PATH
        
        # cw = CeleryRemote.CeleryRemote(user_to.server, user_to.hq_username, user_to.hq_password, 'celeryTasks', 'redis://localhost', '6379')
        
        cfg_cmd='cfg.exe -f \"C:\\inetpub\\ftproot\\'+user_to['ip']+'\\VM_COMMANDS\"'
        result = cw.run(cmd=cfg_cmd,task='run_cmd')

########################################################
#     PPHONE SANITY CHECKS
########################################################
 
    def pphone_force_idle_state(self):
        """Forces pphone to idle state
        
        :param args: List of user dicts mapped to real pphones
        :type args: type list
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        end_time = time.time() + self.force_idle_timeout 
        while True:
            # Make sure pphone is idle
            if self.getdm_session_count() == 0:
                #check pphone is not on voicemail or directory page
                index = self.pphone_search_softkey_text("Call VM")
                if index != -1:
                    self.pphone_press_button(kButton_VoiceMail)
                index = self.pphone_search_softkey_text("Open")
                if index != -1:
                    self.pphone_press_button(kButton_Directory)
                break
            else:
                self.pphone_handset_up()
                time.sleep(0.5)
                self.pphone_handset_down()                    
            
            if time.time() > end_time:
                raise Exception("pphone %s was not able to be forced to idle state" % self.ip4xx_user['ip'])
                break
        # Forcing handset up and down
        self.pphone_handset_up()
        time.sleep(1)
        self.pphone_handset_down() 
        logger.info("pphone %s is idle" % self.ip4xx_user['ip'])


    def pphone_sanity_check(self):
        """Runs Sanity Check functions
        
        :param args: List of user dicts mapped to real pphones
        :type args: type list
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        self.pphone_force_idle_state()

    def verify_phone_first_name(self, name="Available"):
        """Neeraj"""
        time.sleep(1)
        result = self.pphone_ssh_dm("cli -c getdm", "userFirstName")

        if result == name:
            logger.console("\n Firstname on phone is : %s" % result)
            return True
        else:
            logger.console(
                "\nERROR: Mismatch found in firstname , Expected name:%s , Resulted name:%s" % (name, result))
            return False

    def verify_phone_extention(self, extn="2490"):
        """Neeraj"""
        time.sleep(1)
        result = self.pphone_ssh_dm("cli -c getdm", "sipExtension")

        if result == extn:
            logger.console("\n extn on phone is : %s" % result)
            return True
        else:
            logger.console(
                "\nERROR: Mismatch found in extn , Expected extn:%s , Resulted extn:%s" % (extn, result))
            return False

    def getdm_unheardVM_count(self):
        """Returns unheard voice mails count.
        :param user: User dict
        :type user: type dict
        :return ret_val:  Returns unheard VMs count
        :rtype: str
        """
        #logger.warn("In getdm_callee_number. TODO map ca to session number")
        VMcount = self.pphone_ssh_dm("cli -c getdm", "numVoiceMailMsgs")
        while VMcount == "{Unknown error}":
            print("INSIDE WHILE LOOP to get VM count.....")
            VMcount = self.pphone_ssh_dm("cli -c getdm", "numVoiceMailMsgs")
        print "VM count is : %s"%VMcount
        return VMcount

    def pphone_verify_MWI(self, state='on'):

        result = self.pphone_ssh_dm("cli -c getdm", "voiceMessageWaiting")
        if result == state or str(result) == state:
            print "MWI is :" + result
            return True
        else:
            logger.console(
                "\nERROR: Mismatch found in the MWI response , Expected state:%s , Resulted state:%s" % (state, result))
            return False


    def bye(self):
        logger.warn("IP4xx bye")

###################################
#     PhoneInterface Translation
###################################

    # def make_call(**kwargs):
    def make_call_1(self, user_dict):
        logger.warn("ip4xx make call to %s" % user_dict['extension'])
        self.pphone_make_call(user_dict)

    def make_call(self, num):
        logger.warn("ip4xx dialing %s" % num)
        self.pphone_dial_digits(num)
        time.sleep(2)
        self.pphone_press_button_softkey1()

    def input_a_number(self, num):
        logger.warn("ip4xx dialing %s" % num)
        self.pphone_dial_digits(num)

    def verify_notifications_when_in_ring(self):
        logger.warn("ip4xx verify_notifications_when_in_connected ")
        self.wait_for_incoming_call('RIGHT_LINE1')

    def answer_the_call(self):
        self.pphone_answer_call()
        
    def disconnect_the_call(self):
        self.pphone_disconnect_call()

    def handset_up(self):
        self.pphone_handset_up()

    def phone_sanity_check(self):
        self.pphone_sanity_check()

    def press_key(self, key, press_count):
        key_map = {'BottomKey1': kButton_Softkey1 ,'BottomKey2': kButton_Softkey2, 'BottomKey3': kButton_Softkey3,
                   'Quit': kButton_Softkey5, 'VoiceMail': "V", 'vmlogin': kButton_Softkey5, 'Mute': kButton_Mute,
                    'vmdelete' : kButton_Softkey3,'Calltovm': kButton_Softkey2, 'Hold': kButton_Hold,
                   'Directory': kButton_Directory, 'CallersList': kButton_Redial, 'ScrollDown': kButton_Down}
        self.pphone_press_button(key_map[key])

    def press_vm_soft_key(self):
        self.pphone_press_button(kButton_Softkey2)

    def quit_voice_mail(self):
        self.pphone_press_button(kButton_Softkey5)

    def call_from_history(self):
        self.pphone_press_button(kButton_Softkey1)

    def press_vm_hard_key(self):
        self.pphone_press_button_voicemail()

    def login_to_voicemail(self,pin):
        self.press_vm_hard_key()
        self.input_a_number(pin)
        self.press_key(kButton_Softkey5)

    def make_conference(self):
        self.pphone_press_button(kButton_Conference)

    def consult_conference(self):
        self.pphone_press_button(kButton_Softkey2)

    def accept_conference(self):
        self.pphone_press_button(kButton_Softkey1)

    def accept_blind_conference(self):
        pass

    def go_to_directory(self):
        pass

    def call_from_directory(self):
        self.pphone_press_button(kButton_Softkey1)

    def make_transfer(self):
        self.pphone_press_button(kButton_Transfer)

    def make_blind_transfer(self):
        self.pphone_press_button(kButton_Softkey1)

    def make_consult_transfer(self):
        self.pphone_press_button(kButton_Softkey2)

    def accept_blind_transfer(self):
        pass

    def accept_consult_transfer(self):
        self.pphone_press_button(kButton_Softkey1)

    def click_on_park(self):
        self.pphone_press_button(kButton_Softkey1)

    def park_the_call(self):
        self.pphone_press_button(kButton_Softkey1)

    def click_on_unpark(self):
        self.pphone_press_button(kButton_Softkey2)

    def unpark_the_call(self):
        self.pphone_press_button(kButton_Softkey1)

    def get_vm_count(self):
        return  self.getdm_unheardVM_count()

    def verify_msgwait_led_state(self):
        self.pphone_verify_MWI()

    def verify_led_state(self, type, mode, timeout):
        self.pphone_verify_MWI(mode)

    def verify_phone_extn(self,extn):
        return self.verify_phone_extention(extn)

    def verify_in_phone_display(self, ext):
        if ext == 'Anonymous':
            return self.verify_phone_first_name("Anonymous")
        elif ext == self.ip4xx_user['extension']:
            return self.verify_phone_extention(ext)
        else:
            pass
        session = self._pphone_get_callstackdm_session('right_line1')
        display2 = ''
        if ext == 'Conferenced 2 calls':
            ext = '2'
            cmd2 = "callstackdm." + session + ".conferencelistdm.sessionCount"
            display2 = self.pphone_ssh_dm("cli -c getdm", cmd2)
        elif ext == 'Conferenced 3 calls':
            ext = '3'
            cmd2 = "callstackdm." + session + ".conferencelistdm.sessionCount"
            display2 = self.pphone_ssh_dm("cli -c getdm", cmd2)
        elif ext == 'Conferenced 4 calls':
            ext = '4'
            cmd2 = "callstackdm." + session + ".conferencelistdm.sessionCount"
            display2 = self.pphone_ssh_dm("cli -c getdm", cmd2)
        else:
            pass
        cmd = "callstackdm." + session + ".iden.displaynumber"
        display = self.pphone_ssh_dm("cli -c getdm", cmd)
        cmd = "callstackdm." + session + ".iden.displayname"
        display1 = self.pphone_ssh_dm("cli -c getdm", cmd)
        if ext == 'Auto-Attendant':
            re.match(ext, display1)
            return 1
        elif ext == 'Boss_Paging':
            re.match(ext, display1)
            return 1
        elif re.match(ext, display) or re.match(self.ip4xx_user['phoneName'], display1) or re.match(ext, display2):
            return 1
        else:
            raise Exception("display should show " + ext)
            return 0

    def verify_mute_state(self):
        self.verify_pphone_muted()

    def verify_hold_state(self):
        self.verify_pphone_held()
        
if __name__ == "__main__":
    import robot.utils.dotdict

    Phone01_s = robot.utils.dotdict.DotDict(ip="10.198.17.185", extension="2411", phone_type="p8cg", hq_rsa="hq_rs")
    #Phone02_s = robot.utils.dotdict.DotDict(ip="10.198.18.189", extension="1008", phone_type="p8cg",
    #                                        PPhone_mac="001049454AF9")
    #Phone03_s = robot.utils.dotdict.DotDict(ip="10.198.33.255", extension="1009", phone_type="p8cg",
     #                                       PPhone_mac="001049454A71")
    x = IP4xxInterface(Phone01_s)
    # x.pphone_sanity_check(Phone01_s,Phone02_s)
    x.pphone_press_button_speaker()

