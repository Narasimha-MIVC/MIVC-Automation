"""
Module to interact with Mitel phones. This is a base class which will be inherited in other phone model specific
classes.
"""
__author__ = "nitin.kumar-2@mitel.com, milton.villeda@mitel.com"

import sys
import os
import clr
import time
import shutil
import base64
import subprocess
import random
from sys import platform as _platform
from robot.api import logger

# audio imports
from numpy.fft import rfft
from numpy import argmax, mean, diff, log
import numpy
from matplotlib.mlab import find
from scipy.signal import blackmanharris, fftconvolve
from scipy.signal import butter, filtfilt
from scipy import signal 
import soundfile as sf
import parabolic
# end of audio imports

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from phone_constants_69xx import led_mode, led_type, line_state

class Phone6xxxInterface(object):
    """ 6xxx Phone Interface
    """
    def __init__(self, phone_info, **kwargs):
        """
        It is mandatory to call phone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """
        logger.info("Initializing Mitel Phone Base class")
        self.atap_dll_name = "ATAP.dll"
        self.logger_dll_name = "Logger.dll"
        
        if kwargs.get('atap_dll_path', None) is None:
            atap_dll_path = os.path.join(os.path.dirname(__file__), self.atap_dll_name)
            logger_dll_path = os.path.join(os.path.dirname(__file__), self.logger_dll_name)
        self.atap_dll_path = atap_dll_path
        self.logger_dll_path = logger_dll_path
        
        if not os.path.exists(self.atap_dll_path):
            raise Exception("ATAP.dll does not exist in %s" %self.atap_dll_path)
        if not os.path.exists(self.logger_dll_path):
            raise Exception("Logger.dll does not exist in %s" %self.logger_dll_path)

        self.phone_info = phone_info
        # Add reference to the library
        self.copy_dll_to_pythonpath(self.atap_dll_path)
        self.copy_dll_to_pythonpath(self.logger_dll_path)
        self.add_reference_to_dll(self.atap_dll_name)
        self.create_phone(phone_info)
        self.connect_to_phone()
        # retrieving hardphone enums
        self.keys = sys.modules['PhoneHandler'].HardPhone.Keys
        self.ExpansionKeys = sys.modules['PhoneHandler'].HardPhone.ExpansionKeys

    def copy_dll_to_pythonpath(self, dll_path):
        """
        copy dll to the python installation directory
        This dependency which looks like the limitation/bug in .net module could be removed in future
        :param dll_path:
        :return:
        """
        python_installation_dir = os.path.dirname(sys.executable)
        # todo getting exception in copy from robot test case when executed from command line
        try:
            shutil.copy(dll_path, python_installation_dir)
        except:
            pass

    def add_reference_to_dll(self, dll_name):
        """
        Add dll to python namespace and import required modules
        :param dll_name: the name of dll
        :return: None
        """
        clr.AddReference(dll_name.split('.')[0])
        # importing the modules from the dll
        import PhoneHandler
        import Logger
        Logger.Logger.Initialize()

    def create_phone(self, phone_info):
        """
            This function will create a phone object based on the passed phone details.
            
            Valid phone_types: Mitel6940, Mitel6930, Mitel6xxx, etc.
        """

        phoneModel = phone_info["phoneModel"]
        vdpLogin = phone_info.get("vdpLogin", False)
        extensionNumber = phone_info["extensionNumber"]
        authCode = phone_info.get("authCode", "")
        directoryName = phone_info.get("directoryName", "")
        ipAddress = phone_info["ipAddress"]
        macAddress = phone_info.get("macAddress", "")
        phoneName = phone_info.get("phoneName", "")
        trunkISDN = phone_info.get("trunkISDN", "")
        trunkSIP = phone_info.get("trunkSIP", "")
        trunkPrivateISDN = phone_info.get("trunkPrivateISDN", "")
        trunkPrivateSIP = phone_info.get("trunkPrivateSIP", "")
        trunkH323 = phone_info.get("trunkH323", "")
        trunkSIPForcedGW = phone_info.get("trunkSIPForcedGW", "")
        switchIP = phone_info.get("switchIP", "")
        
        self.hq_rsa = phone_info.get("hq_rsa", "hq_rsa")
        self.hq_rsa_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'rsa_keys',self.hq_rsa)
        self.audio_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'audio_analysis')

        self.phone = self.get_object(phoneModel,[phoneModel, vdpLogin, extensionNumber, authCode, directoryName,
                                                 ipAddress, macAddress, phoneName, trunkISDN, trunkSIP, trunkPrivateISDN,
                                                 trunkPrivateSIP, trunkH323, trunkSIPForcedGW,switchIP])
        
    def get_object(self, class_name, params):
        return getattr(sys.modules['PhoneHandler'], class_name)(*params)
        
    def connect_to_phone(self):
        self.phone.connectToPhone()

#############
# Public Methods
#############

    def dial_number(self, num):
        logger.info("Phone6xxxInterface dialing %s" % num)
        self.phone.dialAnumber(num)

    def get_extn_number(self):
        logger.info("Phone6xxxInterface sendig extn")
        return self.phone.extensionNumber
        
    def log_off(self):
        raise NotImplementedError("Implement this function")
        
    def phone_sanity_check(self):
        logger.info("IN BASE SANITY FN")
        
    def make_call(self, phone):
        logger.info("Phone6xxxInterface make call to %s" % phone)

        self.phone.callToAnExtension(phone_info_dict['extensionNumber'])
        
    def answer_call(self):
        logger.info("Phone6xxxInterface answer_the_call")
        self.phone.answerTheCall()


    def verify_phone_display(self, phone_info_dict):
        self.phone.verifyInPhoneDisplay(phone_info_dict['extension'])

    def verify_led_notificaion_when_diversion_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenDiversionActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_diversion_de_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenDiversionDeActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_follow_me_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenFollowMeActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_profile_number(self, profile_number):
        """

        This method ...
        Args:
            profile_number: string

        """
        try:
            self.phone.verifyCallProfileNumber(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l1key(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressL1key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l2key(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressL2key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_offhook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressOffhook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_onhook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.OnHook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey(self, sk_num=1):
        """

        This method ...
        Args:

        """
        try:
            sk_num = int(sk_num)
            if sk_num == 1:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey1)
            elif sk_num == 2:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey2)
            elif sk_num == 3:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey3)
            elif sk_num == 4:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey4)
            elif sk_num == 5:
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey5)
            else:
                raise Exception("FAIL!")
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey_three(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.BottomKey3)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_mute(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.Mute)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_hold(self):
        """

        This method ...
        Args:

        """
        try:
            # Sleep is sometimes necessary
            time.sleep(1)
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.Hold)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_handsfree(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.HandsFree)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumeup(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.IncreaseVolume)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumedown(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DecreaseVolume)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_when_in_ring(self, extension):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            ret_bool = self.phone.verifyDisplayNotificationsWhenInRing(extension)
            if not ret_bool:
                raise Exception("extension %s is not displayed on this phone %s" % (extension, self.phone.extensionNumber))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_when_diversion_activated(self, diversion_category):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            self.phone.verifyDisplayNotificationWhenDiversionActivated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def de_activate_do_not_disturb(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.deActivateDoNotDisturb()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_monitoring(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableMonitoring()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_display_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableDisplayMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_key_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableKeyMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_led_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableLEDMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disable_all_monitors(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.disableAllMonitors()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_line_monitor(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.enableLineMonitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.setToIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_config(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.getConfig()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def connect_to_terminal(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.connectToTerminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_terminal(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.disconnectTerminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_active_audio_device(self):
        """
        This method ...
        Args:
        """
        try:
            cmd = '/voip/eptShow.sh |grep -i "codec"'
            result = self.phone_console_cmd(cmd)
            
            if not result:
                logger.warn("Phone is not in active call to determine active audio device")
                # TODO test hold scenario
                raise Exception("Phone is not in active call to determine active audio device")
                
            cmd = '/voip/eptShow.sh |grep "is active"|grep -o "(.*)"'
            result = str(self.phone_console_cmd(cmd))
            logger.info('active audio device is %s' % result)
            
            if "hf-sbaec" in result:
                # TODO determine if device is headset
                return "speaker"
            elif "hs-hec" in result:
                return "handset"

            raise Exception("Active audio device '%s' is not recognized" % result)

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
    def get_audio_device(self):
        audio_device = 'speaker'
        val = self.get_handsfree_state()
        
        if val == 0:
            audio_device = 'handset'
        elif val == 1: 
            logger.warn("Forcing audio path to headset. Audio testing not supported on headset")
            self.press_handsfree()
            
            val = self.get_handsfree_state()
            if val == 1:
                raise Exception("audio path should be in handsfree")
            audio_device = 'speaker'
        elif val == 2: 
            audio_device = 'speaker'
            
        return audio_device
        
#
# AUDIO
    def format_response(self, response_signal):
        """

        This method ...
        Args:
            response_signal: string

        """
        try:
            self.phone.formatResponse(response_signal)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_hard_key(self, hardkey):
        """

        This method ...
        Args:
            1: HardPhone.Keys

        """
        try:
            if hardkey == '4':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad4)
            elif hardkey == '5':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad5)
            elif hardkey == '7':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad7)
            elif hardkey == '1':
                self.phone.pressHardKey(sys.modules['PhoneHandler'].HardPhone.Keys.DialPad1)

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
##################################################################
#   PHYSICAL BUTTON PRESS using /bin/input command
##################################################################

    def start_bin_input_read(self):
        cmd = "./script -c '/bin/input read' input_read_dump.txt"
        self.phone_console_cmd(cmd, 'su')

    def end_bin_input_read(self):
        cmd = 'killall script'
        self.phone_console_cmd(cmd, 'su')

        # self.tmp_ssh = paramiko.SSHClient()
        # self.tmp_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.tmp_ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        # cmd = '/bin/input read'
        # pswd = 'SkBjcXVlc0NAcnQxZXI='
        # cmd = "echo " + base64.b64decode(pswd) + " | su -c \"" + cmd + "\""
        # logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        # stdin, stdout, stderr = self.tmp_ssh.exec_command(cmd)
        
        # logger.warn('press buttons')
        # time.sleep(10)
        # result = stdout.readlines()
        # logger.warn(result)
        # if  self.tmp_ssh:
             # self.tmp_ssh.close()
        # return result
        
        
    def press_phys_button(self, button_str, options=None):
        """This method presse a physical button
            using /bin/input
        Args:
            button_str: button to be pressed

        """
        try:
            if options is 'multiple_btns':
                cmd = '/bin/input keystr ' + button_str
            else: 
                button = str(self.phone_info['button_map'][button_str.lower()])
                if options is None:
                    cmd = '/bin/input pressrelkey ' + button
                elif options is 'offhook':
                    cmd = '/bin/input setkey ' + button + ' 1'
                elif options is 'on hook':
                    cmd = '/bin/input setkey ' + button + ' 0'
                else:
                    raise Exception("options: '%s' is not supported" % options)
            
            self.phone_console_cmd(cmd, 'su')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
            
##################################################################
#   PHYSICAL BUTTON PRESS       BLOCK END
##################################################################

    def collect_responses(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.collectResponses()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def collect_ack(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.collectACK()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_response_buckets(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.clearResponseBuckets()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request(self, signal_to_be_sent):
        """

        This method ...
        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone.sendRequest(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request_with_fresh_sequence_number(self, signal_to_be_sent):
        """

        This method ...
        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone.sendRequestWithFreshSequenceNumber(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def answer_the_call(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.answerTheCall()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def reject_the_call(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.rejectTheCall()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_the_call(self):
        """

        This method ...
        Args:

        """
        try:
            logger.info("Disconnecting the call")
            self.phone.disconnectTheCall()
        except Exception as err:
            if 'verifyLineNotificaionWhenInIdle - Mismatch in Line status. Expected 0 in' in str(err) and len(self.get_led_buffer()) == 0:
                logger.warn("Trying to disconnect the call when in idle.")
            else:
                fn = sys._getframe().f_code.co_name
                raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def off_hook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.OffHook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def on_hook(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.OnHook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_to_an_extension(self, extension_to_be_called):
        """

        This method ...
        Args:
            extension_to_be_called: HardPhone

        """
        try:
            logger.info("Calling the extension %s"%(extension_to_be_called))
            self.phone.callToAnExtension(extension_to_be_called)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code(self, service_code):
        """

        This method ...
        Args:
            service_code: string

        """
        try:
            self.phone.dialServiceCode(service_code)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enter_a_number(self, terminal_phone):
        """

        This method ...
        Args:
            terminal_phone: HardPhone

        """
        try:
            self.phone.EnterAnumber(terminal_phone)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_anumber(self, number_to_be_dialled):
        """

        This method ...
        Args:
            number_to_be_dialled: string

        """
        try:
            self.phone.dialAnumber(number_to_be_dialled)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    # def dial_anumber(self, string_to_be_verified):
    #     """
    #
    #     This method ...
    #     Args:
    #         string_to_be_verified: string
    #
    #     """
    #     try:
    #         self.phone.dialAnumber(string_to_be_verified)
    #     except Exception as err:
    #         fn = sys._getframe().f_code.co_name
    #         raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_key(self, key_to_be_pressed, press_count=1):
        """

        This method ...
        Args:
            key_to_be_pressed: int

        """
        try:
            if key_to_be_pressed == 'Quit':
                if self.phone.phoneModel == 'Mitel6940':
                    key_to_be_pressed = 'BottomKey6'
                elif self.phone.phoneModel == 'Mitel6930':
                    key_to_be_pressed = 'BottomKey5'
                elif self.phone.phoneModel == 'Mitel6920':
                    key_to_be_pressed = 'BottomKey4'
                else:
                    pass
            elif key_to_be_pressed == 'vmlogin':
                key_to_be_pressed = 'BottomKey1'
                self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
                time.sleep(10)
                key_to_be_pressed = 'ScrollRight'
            elif key_to_be_pressed == 'vmdelete':
                key_to_be_pressed = 'BottomKey3'
                self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
                key_to_be_pressed = 'BottomKey2'
            elif key_to_be_pressed == 'Calltovm':
                key_to_be_pressed = 'BottomKey3'
            else:
                pass
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_vm_soft_key(self):
        try:
            self.phone.pressHardKey(getattr(self.keys,'BottomKey3'), 1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_vm_hard_key(self):
        try:
            self.press_phys_button('VM')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_to_voicemail(self, pin):
        try:
            self.press_phys_button('VM')
            self.dial_anumber(pin)
            self.press_key("BottomKey1")
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_phone_extn(self, extn):
        try:
            self.self.phone.verifyInPhoneDisplay(extn)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def make_conference(self, key_to_be_pressed='BottomKey2', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def consult_conference(self, key_to_be_pressed='BottomKey1', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_conference(self, key_to_be_pressed='BottomKey2', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_blind_conference(self, key_to_be_pressed='BottomKey2', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_transfer(self, key_to_be_pressed='BottomKey3', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_blind_transfer(self, key_to_be_pressed='BottomKey3', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_consult_transfer(self, key_to_be_pressed='BottomKey1', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_blind_transfer(self, key_to_be_pressed='BottomKey3', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_consult_transfer(self, key_to_be_pressed='BottomKey3', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def click_on_park(self, key_to_be_pressed='BottomKey4', press_count=1):
        try:
            if self.phone.phoneModel == 'Mitel6920':
                    self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
                    key_to_be_pressed = 'BottomKey1'
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def park_the_call(self, key_to_be_pressed='BottomKey3', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def click_on_unpark(self, key_to_be_pressed='BottomKey2', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def unpark_the_call(self, key_to_be_pressed='BottomKey1', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def quit_voice_mail(self, key_to_be_pressed='BottomKey1', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_vm_count(self, key_to_be_pressed='VoiceMail', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
            time.sleep(2)
            self.phone.dialAnumber("123456")
            time.sleep(2)
            key_to_be_pressed = 'BottomKey1'
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
            time.sleep(5)
            key_to_be_pressed = 'ScrollDown'
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
            time.sleep(5)
            vm_string = self.get_phone_display()
            try:
                vm_count = int((vm_string.split('Inbox')[1]).split('Voicemail')[0])
            except :
                vm_count = 0
            self.press_key("Quit")
            print vm_count
            return vm_count

        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_history(self, key_to_be_pressed='ScrollUp', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
            time.sleep(2)
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
            key_to_be_pressed = 'ScrollRight'
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
            key_to_be_pressed = 'BottomKey1'
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def go_to_directory(self, key_to_be_pressed='ScrollUp', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
            time.sleep(2)
            key_to_be_pressed = 'BottomKey2'
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_directory(self, key_to_be_pressed='ScrollDown', press_count=1):
        try:
            self.phone.pressHardKey(getattr(self.keys,key_to_be_pressed), press_count)
            time.sleep(2)
            key_to_be_pressed = 'BottomKey1'
            self.phone.pressHardKey(getattr(self.keys, key_to_be_pressed), press_count)
            time.sleep(2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_mute_state(self):
        self.verify_msgwait_led_state('58','17')

    def verify_hold_state(self):
        self.verify_hold_state_packets()
        self.verify_msgwait_led_state('57','14')



    def press_expansion_box_key(self, key_to_be_pressed, press_count=1):
        """

        This method will press a key in the extension box...
        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone.pressHardKeyInExpansionModule(getattr(self.ExpansionKeys,key_to_be_pressed), press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def release_key(self, key_to_be_released):
        """

        This method ...
        Args:
            key_to_be_released: HardPhone.Keys

        """
        try:
            self.phone.releaseKey(key_to_be_released)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def input_a_number(self, string_to_dial):
        """

        This method ...
        Args:
            string_to_dial: string

        """
        try:
            print "string_to_dial"
            print string_to_dial
            self.phone.inputANumber(string_to_dial)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_remote_extension(self, number_r1):
        """

        This method ...
        Args:
            number_r1: HardPhone

        """
        try:
            self.phone.callFromRemoteExtension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_sip_mobile_extension(self, number_r1):
        """

        This method ...
        Args:
            number_r1: HardPhone

        """
        try:
            self.phone.callFromSIPMobileExtension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_ic_sdiversion_with_service_codes(self, diversion_category):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            self.phone.activateICSdiversionWithServiceCodes(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code_and_verify_notifications(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            self.phone.activateDNDwithServiceCodeAndVerifyNotifications(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.activateDNDwithServiceCode()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_dn_dwith_service_code(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.deactivateDNDwithServiceCode()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_group_dn_dwith_service_code(self, group_number):
        """

        This method ...
        Args:
            group_number: string

        """
        try:
            self.phone.deactivateGroupDNDwithServiceCode(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code_and_verify_display(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            self.phone.dialServiceCodeAndVerifyDisplay(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_group_dn_dwith_service_code(self, group_number):
        """

        This method ...
        Args:
            group_number: string

        """
        try:
            self.phone.activateGroupDNDwithServiceCode(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_connection(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.checkPhoneConnection()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def program_follow_me_remotely(self, extension_number_to_be_routed):
        """

        This method ...
        Args:
            extension_number_to_be_routed: string

        """
        try:
            self.phone.programFollowMeRemotely(extension_number_to_be_routed)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def cancel_active_call_back(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.cancelActiveCallBack()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_dual_forking_extension(self, dual_forking_extension_number):
        """

        This method ...
        Args:
            dual_forking_extension_number: string

        """
        try:
            self.phone.loginWithDualForkingExtension(dual_forking_extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_different_extension(self, extension_number):
        """

        This method ...
        Args:
            extension_number: string

        """
        try:
            self.phone.loginWithDifferentExtension(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_back_with_base_extension(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.loginBackWithBaseExtension()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_non_member_of_group(self, extension):
        """

        This method ...
        Args:
            extension: string

        """
        try:
            self.phone.PickCallWithNonMemberOfGroup(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_member_of_group(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.PickCallWithMemberOfGroup()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_state(self,LineStatus, activeLineNum, maxWaitTimeoutInSeconds = 10):
        """

        This method ...
        Args:

        """
        try:
            line_buffer = self.get_line_buffer()
            if activeLineNum in line_buffer.keys() and len(line_buffer) != 0:
                if len(LineStatus) <= 2:
                    return self.phone.verifyLineState(str(LineStatus), str(activeLineNum), int(maxWaitTimeoutInSeconds))
                else:
                    return self.phone.verifyLineState(str(line_state[LineStatus]), str(activeLineNum), int(maxWaitTimeoutInSeconds))
            else:
                logger.warn("Line buffers are empty or the requested active line is not present in the buffer")
                logger.warn("Line buffer is <%s>"%line_buffer)
                return LineStatus == "idle"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_line_buffer(self):
        """This method will return the buffer containing details of all lines on the phone...
        The return values are in decimal

        Args: None

        """
        try:
            dict = {}
            buffers = self.phone.getLINEbuffer()
            for buffer in buffers:
                dict[buffer.Key] = buffer.Value
            return dict
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_state(self,ledtype, mode, timeout = 10):
        """

        his method will verify the status of a led...
        Args: type : type of the led -> Table 8 of atap document
        mode : mode of led -> Table 9 of atap document
        timeout : max time to wait

        Args : Type and mode should be provided in hex format

        """
        try:
            if "Line" in ledtype:
                key_num = ledtype.split("Line")[-1]
                start_num = 23  # as per atap doc as function1 is 24
                hex_key_val = (hex(start_num + int(key_num)))[2:]
                _ledtype = hex_key_val.upper()
            led_buffer = self.get_led_buffer()
            if len(led_buffer) != 0 and str(int(_ledtype,16)) in led_buffer.keys():
                actual_mode = led_buffer[str(int(_ledtype))]
                if mode in ["blink", "blinking", "flash", "flashing"]:
                   return actual_mode in led_mode["blink"]
                #else:
                return actual_mode == str(mode)
            else:
                logger.warn("Led buffers are empty or the requested led is not in the buffer")
                return mode.lower() == "off"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_msgwait_led_state(self,ledtype='57', mode='15', timeout = 10):
        """

        his method will verify the status of a led...
        Args: type : type of the led -> Table 8 of atap document
        mode : mode of led -> Table 9 of atap document
        timeout : max time to wait

        Args : Type and mode should be provided in hex format

        """
        try:
            # if "Line" in ledtype:
            #     key_num = ledtype.split("Line")[-1]
            #     start_num = 23  # as per atap doc as function1 is 24
            #     hex_key_val = (hex(start_num + int(key_num)))[2:]
            #     _ledtype = hex_key_val.upper()
            led_buffer = self.get_led_buffer()
            #print led_buffer
            #print str(int(ledtype))
            #if len(led_buffer) != 0 and str(int(_ledtype,16)) in led_buffer.keys():
            if len(led_buffer) != 0 and str(int(ledtype)) in led_buffer.keys():
                actual_mode = led_buffer[str(int(ledtype))]
                #if mode in ["blink", "blinking", "flash", "flashing"]:
                   # return actual_mode in led_mode["blink"]
                #else:
                return actual_mode == str(mode)
            else:
                logger.warn("Led buffers are empty or the requested led is not in the buffer")
                return mode.lower() == "off"
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def get_led_buffer(self):
        """This method will return the buffer containing details of all leds on the phone...
            The return values are in decimal
        Args: None

        """
        try:
            dict = {}
            buffers = self.phone.getLEDBuffer()
            for buffer in buffers:
                dict[buffer.Key] = buffer.Value
            return dict
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_line_for_hunt_group(self, hunt_group_number):
        """

        This method ...
        Args:
            hunt_group_number: string

        """
        try:
            self.phone.setLineForHuntGroup(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def remove_line_for_hunt_group(self, hunt_group_number):
        """

        This method ...
        Args:
            hunt_group_number: string

        """
        try:
            self.phone.removeLineForHuntGroup(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_message_waiting(self, extension):
        """

        This method ...
        Args:
            extension: string

        """
        try:
            self.phone.enableMessageWaiting(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def intrusion_from_extension(self, extension):
        """

        This method ...
        Args:
            extension: HardPhone

        """
        try:
            self.phone.IntrusionFromExtension(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_pe_ndeactivated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenPENdeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_not_responding(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenNotResponding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_cancel_call(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenCancelCall(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """

        This method ...
        Args:
            vacant_number: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenDialVacantNumber(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyReroutingtoInAttendWhenDialLoggedOffTerminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyPrivateTrunkReroutingtoInAttendWhenNotResponding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_cancel_call(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyPrivateReroutingtoInAttendWhenCancelCall(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """

        This method ...
        Args:
            vacant_number: string

        """
        try:
            self.phone.verifyPrivateReroutingtoInAttendWhenDialVacantNumber(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifyPrivateReroutingtoInAttendWhenDialLoggedOffTerminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_external_call_to_in_attend(self, in_attend_number):
        """

        This method ...
        Args:
            in_attend_number: string

        """
        try:
            self.phone.verifyExternalCallToInAttend(in_attend_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_default(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.setToDefault()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_is_online(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.checkPhoneIsOnline()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def sleep(self, seconds):
        """

        This method ...
        Args:
            seconds: double

        """
        try:
            self.phone.sleep(seconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_delay(self, sec=2):
        """

        This method ...
        Args:
            2.0: double

        """
        try:
            sleep(sec)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_follow_me(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.deactivateFollowMe()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_direct_diversion(self, extension_number):
        """

        This method ...
        Args:
            extension_number: string

        """
        try:
            self.phone.activateDirectDiversion(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_message_contents(self, contents):
        """

        This method ...
        Args:

        """
        try:
            logger.info("verify_display_message_contents")
            return self.phone.verifyInDisplayResponses(contents)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_ring(self):
        """

        This method ...
        Args:

        """
        try:
            logger.info("Verifying the notifications in ring")
            self.phone.verifyNotificationsWhenInRing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_call_back_ring(self, extension_to_be_verified):
        """

        This method ...
        Args:
            extension_to_be_verified: string

        """
        try:
            self.phone.verifyNotificationsWhenCallBackRing(extension_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_ed_ngets_call(self, number_of_responses_to_be_stored):
        """

        This method ...
        Args:
            number_of_responses_to_be_stored: int

        """
        try:
            self.phone.verifyNotificationsWhenEDNgetsCall(number_of_responses_to_be_stored)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notification_when_message_waiting(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationWhenMessageWaiting()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenInIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    # def verify_notifications_when_in_idle(self, str_to_bo_verified):
        # """

        # This method ...
        # Args:
            # str_to_bo_verified: string

        # """
        # try:
            # self.phone.verifyNotificationsWhenInIdle(str_to_bo_verified)
        # except Exception as err:
            # fn = sys._getframe().f_code.co_name
            # raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_busy(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenInBusy()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_notifications_when_in_connected(self):
        """

        This method ...
        Args:

        """
        try:
            logger.info("Verify the notifications when in connected.")
            
            self.phone.verifyLineNotificaionWhenInConnected()
            # self.phone.verifyNotificationsWhenInConnected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_follow_me_activated(self, remote_number):
        """

        This method ...
        Args:
            remote_number: string

        """
        try:
            self.phone.verifyNotificationsWhenFollowMeActivated(remote_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_activated(self, diversion_category):
        """

        This method ...
        Args:
            diversion_category: string

        """
        try:
            self.phone.verifyNotificationsWhenDiversionActivated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_de_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenDiversionDeActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notifications_when_pe_ndeactivated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificationsWhenPENdeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_clearing(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenInClearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenInIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_clearing(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenInClearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_connected(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenInConnected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_out_going(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificaionWhenOutGoing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_in_idle(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLEDNotificaionWhenInIdle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_list_profile(self, profile_number):
        """

        This method ...
        Args:
            profile_number: string

        """
        try:
            self.phone.verifyCallListProfile(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyNotificationsWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notifications_when_do_not_disturb_activated(self):
        """

        This method ...
        Args:

        """
        try:
            self.phone.verifyLineNotificationsWhenDoNotDisturbActivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_contents(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            self.phone.verifyDisplayContents(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_in_phone_display(self, string_to_be_verified):
        """

        This method ...
        Args:
            string_to_be_verified: string

        """
        try:
            logger.info("Verifying %s in the phone display"%string_to_be_verified)
            if string_to_be_verified == 'Conferenced 2 calls':
                string_to_be_verified='Conference'
                return self.phone.verifyInDisplayResponses(string_to_be_verified)
            return self.phone.verifyInDisplayResponses(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_phone_display(self, phone_mode = "non idle"):
        """

        returns everything on the phone display when the phones are in call
        Args:
            None

        """
        try:
            logger.info("Getting the phone display")
            if phone_mode == "idle":
                self.press_key("DecreaseVolume")
            return self.phone.getAllDisplayResponses()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def reboot_terminal(self):
        """
        reboot the phone
        Args:
            None

        """
        try:
            logger.info("Rebooting the phone")
            self.phone.rebootPhone()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_firmware_version(self):
        """
        Firmware version of the phone
        Args:
            Firmware version of the phone

        """
        try:
            return self.phone.FirmwareVersion
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def WaitTillPhoneComesOnline(self, timeOutInSeconds):
        """
        this function will wait till the phone comes back online
        Args:
            timeOutInSeconds : this time will be added to an inbuilt wait of 20 seconds

        """
        try:
            return self.phone.WaitTillPhoneComesOnline(timeOutInSeconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def get_library_version(self):
        """
        Library version of ATAP
        Args:
            Library version of ATAP

        """
        try:
            return self.phone.LibraryVersion
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_sip_traces(self):
        '''
        Clears the sip traces on the phone
        :return: None
        '''
        try:
            self.phone.clearSIPtraces()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_in_messages(self):
        '''
        sip messages received by the phone
        :return: SIP IN messages from the phone
        '''
        try:
            sip_messages = []
            for message in self.phone.SIPMessageRecieved:
                sip_messages.append(message)
            return sip_messages
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_out_messages(self):
        '''
        sip messages sent by the phone
        :return: SIP OUT messages from the phone
        '''
        try:
            sip_messages = []
            for message in self.phone.SIPMessageSent:
                sip_messages.append(message)
            return sip_messages
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_sip_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """

        This method ...
        Args:
            phone2: string

        """
        try:
            self.phone.verifySIPPrivateTrunkReroutingtoInAttendWhenNotResponding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))
     
    def phone_console_cmd(self, cmd, options=None):
        """Runs cmd via phone console
        
        :param cmd:  cmd
        :type cmd: type str
        :return ret_val:  cmd result
        """
        # import rpdb2; rpdb2.start_embedded_debugger('admin1')
        if options is not None and 'su' in options:
            return self.phone_ssh_su_cmd(cmd)
        
        return self.phone_ssh_cmd(cmd)
         
    def phone_ssh_cmd(self, cmd):
        """Runs cmd via ssh on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result
        
    def phone_ssh_su_cmd(self, cmd):
        """Runs cmd via ssh as su on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """
        # logger.info("using rsa %s" % self.hq_rsa_path)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        pswd = 'SkBjcXVlc0NAcnQxZXI='
        cmd = "echo " + base64.b64decode(pswd) + " | su -c \"" + cmd + "\""
        logger.info("Running ssh cmd: \"%s\" on phone %s" % (cmd, self.phone_info['ipAddress']))
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.readlines()
        
        if  self.ssh:
             self.ssh.close()
        return result

    def get_missing_apt_files(self):
        missing_files = []
        files = ['pxaudio_init.sh', \
                'pxcapture_audiohandset.sh', \
                'pxcapture_audioheadset.sh', \
                'pxcapture_audiospeaker.sh', \
                'pxinject_audiohandset.sh', \
                'pxinject_audioheadset.sh', \
                'pxinject_audiospeaker.sh', \
                'pxrm_audio.sh', \
                'pxsync_enable.sh', \
                'pxsync_disable.sh']

        file_list = self.phone_console_cmd('ls .')
        file_list = ''.join(file_list)

        for file in files:
            if file not in file_list:
                missing_files.append(file)

        return missing_files

    def get_missing_pcm_apt_files(self):
        missing_files = []
        files = ['16k_500.pcm', \
                '16k_1k.pcm', \
                '16k_2k.pcm', \
                '16k_3k.pcm']

        file_list = self.phone_console_cmd('ls /tmp/')
        file_list = ''.join(file_list)

        for file in files:
            if file not in file_list:
                missing_files.append(file)

        return missing_files
        
    def upload_apt_files_to_phone(self, files_to_upload):
           
        # check if list is empty
        if not files_to_upload :
            return
            
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)
        
        with SCPClient(ssh.get_transport()) as scp:
            for file in files_to_upload:
                filename = os.path.join(self.audio_path,file)
                try:    
                    scp.put(filename)
                except:
                    raise Exception("An error occured with scp.put(%s) " % filename)
                    
                if "pcm" in file:
                    # Need to move file to tmp dir otherwise
                    # pxcon will not play the file
                    cmd = 'mv ' + file + ' /tmp/' + file
                    self.phone_console_cmd(cmd, 'su')

        if ssh:
            ssh.close()  
    
    def upload_path_confirmation_files(self):
        """scp path confirmation files
        
        :return ret_val: None
        """
        pcm_to_upload = self.get_missing_pcm_apt_files()
        files_to_upload = self.get_missing_apt_files() + pcm_to_upload
        logger.info("Files to upload on phone %s: %s" % (self.phone_info['ipAddress'], files_to_upload))

        self.upload_apt_files_to_phone(files_to_upload)
        
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)
        
        # with SCPClient(ssh.get_transport()) as scp:
            # for file in files_to_upload:
                # filename = os.path.join(self.audio_path,file)
                # try:    
                    # scp.put(filename)
                # except:
                    # raise Exception("An error occured with scp.put(%s) " % filename)
                    
                # if "pcm" in file:
                    # # Need to move file to tmp dir otherwise
                    # # pxcon will not play the file
                    # cmd = 'mv ' + file + ' /tmp/' + file
                    # self.phone_console_cmd(cmd, 'su')

        # if ssh:
            # ssh.close()
            
        cmd = 'chmod 754 pxaudio_init.sh'
        self.phone_console_cmd(cmd, 'su')

        # Remove non-linux chars from file
        cmd = "sed 's/\\r$//g' pxaudio_init.sh > tmpfile"
        self.phone_console_cmd(cmd)
        cmd = " mv tmpfile pxaudio_init.sh"
        self.phone_console_cmd(cmd, 'su')

    def scp_put(self, file):
        """Runs cmd via ssh on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        with SCPClient(ssh.get_transport()) as scp:
           scp.put(file)
          
        if ssh:
            ssh.close()
              
    def scp_get(self, file):
        """Runs cmd via ssh on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: ssh cmd result
        """
        logger.info(file)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.phone_info['ipAddress'],username="admin",key_filename=self.hq_rsa_path)

        with SCPClient(ssh.get_transport()) as scp:
           scp.get(file)
        if ssh:
            ssh.close()     
        
    def pxcon_inject_capture_audio(self, other_phone, file):
        try:    
            # default_audio_path = 'speaker'
            # audio_path = self.get_audio_path()
            # otherPhone_audio_path = other_phone.get_audio_path()
            
            self.run_bash_cmd('sh pxaudio_init.sh')
            other_phone.run_bash_cmd('sh pxaudio_init.sh')
            
            # if default_audio_path == 'speaker':
            self.run_pxcon_script('pxinject_audio_mos_male1.sh')
            other_phone.run_pxcon_script('pxcapture_audio_mos_male1.sh')
            # elif default_audio_path == 'handset':
            # elif default_audio_path == 'speaker':
            # other_phone.run_pxcon_script('pxcapture_audiohandset.sh')
            
            self.run_pxcon_script('pxsync_enable.sh')
            other_phone.run_pxcon_script('pxsync_enable.sh')
            
            # Audio plays for at least a second. No need for a sleep
            time.sleep(5)
            
            self.run_pxcon_script('pxrm_audio.sh')
            other_phone.run_pxcon_script('pxrm_audio.sh')
            
            other_phone.scp_get('/tmp/mos_male1_capture.pcm')
            
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
 
                
    def get_value(self, arg, delim='='):
        if delim in arg:
            value = arg.split(delim)[1].split()
            return value
        return None
        
    def find_key_value(self, arg, key, delim='='):
        for line in arg:
            if key in line: 
                value = line.split(delim)[1].split()
                if isinstance(value, list):
                    return value[0]
                return value
        return None
 
    def verify_two_way_packets(self):
        """
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """        
        cmd = 'cat /proc/ept/rtpstats'

        result = self.run_bash_cmd(cmd) 
        ingress = self.find_key_value(result, 'ingressRtpPkt')
        egress = self.find_key_value(result, 'egressRtpPkt')
        time.sleep(2)
        result = self.run_bash_cmd(cmd) 
        ingresss = self.find_key_value(result, 'ingressRtpPkt')
        egresss = self.find_key_value(result, 'egressRtpPkt')

        if int(ingresss) > int(ingress) and int(egresss) > int(egress):
            return
            
        pckt_list = list(ingesss,ingress, egress, egresss)
        raise Exception("verify_two_way_packets fail! %s" % pckt_list)            
                                           
    def verify_hold_state_packets(self):
        """
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """        
        cmd = 'cat /proc/ept/rtpstats'
        result = self.run_bash_cmd(cmd) 

        # Result is empty when phone is on hold
        if not result:
            return
            
        raise Exception("verify_hold_state_packets fail! %s" % result)            
       
    def check_audio_is_on_hold(self, other_phone, moh_enabled):
        if moh_enabled:
            silence_energy_threshold = 5.0e-10
        else:
            silence_energy_threshold = 9.0e-11
        
        self.verify_hold_state_packets()
        
        filename, self_audio_device = self.run_pxcon_one_way_audio(other_phone)
        energy = self.estimate_energy(filename)
        
        if energy > silence_energy_threshold:
            raise Exception("Energy of %s should be less than threshold %s" % (energy, silence_energy_threshold))            
        
    def verify_codec(self):
        """
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """        
        supported_codecs = ['ILBC30']
        cmd = 'cat /proc/ept/activeAudioCodec'
        result = self.run_bash_cmd(cmd) 
        
        for i,item in enumerate(result):
            if 'stream 0' in item:
                if self.get_value(result[i+1]) in supported_codecs:
                    return 
        raise Exception("Codec verification fail! %s" % result)            
                 

    def check_dtmf(self):
        try:    
            # self_audio_device = 'speaker'
            # audio_path = self.get_audio_path()
            # other_audio_device = other_phone.get_audio_path()
            
            self.run_bash_cmd('sh pxaudio_init.sh')
            
            # if self_audio_device == 'speaker':
            # self.run_pxcon_script('pxcapture_audiospeaker.sh')
            self.run_pxcon_script('pxcapture_audiohandset.sh')
            
            self.run_pxcon_script('pxsync_enable.sh')
            
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def check_pesq_mos_score(self, other_phone, voice):
        """
        Checks MOS score via PESQ algorithm
        """
        voice_files = ['male1.pcm', 'male2.pcm', 'female1.pcm', 'female2.pcm']
        exe = 'pesq.exe'
        mos_score = ''
        
        if voice == '':
            secure_random = random.SystemRandom()
            file = secure_random.choice(voice_files)
        else:
            file = voice
            
        self.pxcon_inject_capture_audio(other_phone, file)
        
        reference = os.path.join(self.audio_path,file)
        exe_path = os.path.join(self.audio_path,exe)
        logger.info("Using voice file %s" % reference)

        degraded = reference
        output = subprocess.Popen([exe_path, '+16000', reference, degraded], stdout=subprocess.PIPE)
        
        out, err = output.communicate()
        out = out.splitlines()
        for line in out:
            if 'MOS-LQO' in line:
                 mos_score = line.split('=')
                 logger.info(mos_score)
        
        if mos_score == '':
            raise Exception('MOS score is not resolved. pesq output %s' % out)     
            
    def update_devnull_permissions(self):
        """Runs cmd via ssh as su on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """        
        cmd = 'chmod a+rw /dev/null'
        
        self.run_bash_cmd(cmd) 
        
    def run_pxcon_script(self, cmd):
        """Runs cmd via ssh as su on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """        
        cmd = 'pxcon ' + cmd
        
        self.phone_console_cmd(cmd, 'su')
            
    def run_bash_cmd(self, cmd):
        """Runs cmd via ssh as su on phone
        
        :param cmd: ssh cmd
        :type cmd: type str
        :return ret_val: result
        """        
        
        self.phone_console_cmd(cmd, 'su')
        
        
#
# AUDIO
#

                
    def freq_from_fft(self, sig, fs):
        """
        Estimate frequency from peak of FFT
        """
        # Compute Fourier transform of windowed signal
        windowed = sig * blackmanharris(len(sig))
        f = rfft(windowed)

        # Find the peak and interpolate to get a more accurate peak
        i = argmax(abs(f))  # Just use this for less-accurate, naive version
        true_i = parabolic.parabolic(log(abs(f)), i)[0]

        # Convert to equivalent frequency
        return fs * true_i / len(windowed)

    def freq_from_crossings(self, sig, fs):
        """
        Estimate frequency by counting zero crossings
        """
        # Find all indices right before a rising-edge zero crossing
        indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

        # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
        # crossings = indices

        # More accurate, using linear interpolation to find intersample
        # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
        crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

        # Some other interpolation based on neighboring points might be better.
        # Spline, cubic, whatever

        return fs / mean(diff(crossings))
        

    def freq_from_autocorr(self, sig, fs):
        """
        Estimate frequency using autocorrelation
        """
        # Calculate autocorrelation (same thing as convolution, but with
        # one input reversed in time), and throw away the negative lags
        corr = fftconvolve(sig, sig[::-1], mode='full')
        corr = corr[len(corr)//2:]

        # Find the first low point
        d = diff(corr)
        start = find(d > 0)[0]

        # Find the next peak after the low point (other than 0 lag).  This bit is
        # not reliable for long signals, due to the desired peak occurring between
        # samples, and other peaks appearing higher.
        # Should use a weighting function to de-emphasize the peaks at longer lags.
        peak = argmax(corr[start:]) + start
        px, py = parabolic.parabolic(corr, peak)

        return fs / px
        
    def butter_highpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y
        
    def estimate_energy(self, raw_audio_file):
        try:
            cutoff = 0
            order = 2
            fs = 16000
            cutoff = 250
                
            logger.info('Reading file "%s"\n' % raw_audio_file)
            raw_audio, fs = sf.read(raw_audio_file, format='RAW', samplerate=fs, channels=1, subtype='PCM_16')
            raw_audio_filt = self.butter_highpass_filter(raw_audio, cutoff, fs, order)
            
            f, p = signal.periodogram(raw_audio_filt, fs)
            signal_energy = numpy.mean(p)
            logger.info("Energy: %s" % signal_energy)
            return signal_energy
                
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
          
    def estimate_frequency(self, file, audiopath):
        try:
            cutoff = 0
            order = 2
            fs = 16000
            
            audiopath = audiopath.lower()
            if audiopath == 'handset':
                cutoff = 1000
            elif audiopath == 'headset':
                cutoff = 250
            elif audiopath == 'speaker':
                cutoff = 2500
            else:   
                logger.info("audiopath %s does not exist" % audiopath)
                raise Exception("Audio path confirmation FAILED")
                
            logger.info('Reading file "%s"\n' % file)
            raw_audio, fs = sf.read(file, format='RAW', samplerate=fs, channels=1, subtype='PCM_16')
            raw_audio_filt = self.butter_highpass_filter(raw_audio, cutoff, fs, order)

            #
            # Leaving two freq estimation methods for testing purposes
            #
            
            # logger.info('Calculating frequency from zero crossings:')
            # start_time = time.time()
            # freq = self.freq_from_crossings(raw_audio_filt, fs)
            # logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            # logger.info('%f Hz' % freq)
            
            # logger.info('Calculating frequency from autocorrelation:')
            # start_time = time.time()
            # freq2 = self.freq_from_autocorr(raw_audio_filt, fs)
            # logger.info('%f Hz' % freq2)
            # logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            
            logger.info('Calculating frequency from FFT:')
            start_time = time.time()
            freq3 = self.freq_from_fft(raw_audio_filt, fs)
            logger.info('%f Hz' % freq3)
            logger.info('Time elapsed: %.3f s\n' % (time.time() - start_time))
            freq = freq3
            
            if audiopath == 'handset':
                if int(freq) >= 1950 and int(freq) <= 2050:
                    logger.info("HANDSET PASS")
                else:
                    logger.info("Handset Freq Check FAILED")
                    raise Exception("Audio path confirmation FAILED")
            elif audiopath == 'headset' and int(freq) == 500:
                # TODO  improve robustness of headset
                if int(freq) >= 450 and int(freq) <= 550:
                    logger.info("HEADSET PASS")
                else:
                    logger.info("Headset Freq Check FAILED")
                    raise Exception("Audio path confirmation FAILED")          
            elif audiopath == 'speaker':
                if int(freq) >= 2900 and int(freq) <= 3000:
                    logger.info("SPEAKER PASS")
                else:
                    logger.info("Speaker Freq Check FAILED")
                    raise Exception("Audio path confirmation FAILED")
                
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def run_pxcon_one_way_audio(self, other_phone):
        try:    
            self_audio_device = self.get_active_audio_device()
            other_audio_device = other_phone.get_active_audio_device()

            self.run_bash_cmd('sh pxaudio_init.sh')
            other_phone.run_bash_cmd('sh pxaudio_init.sh')
            
            # Inject Audio
            if self_audio_device == 'speaker':
                self.run_pxcon_script('pxinject_audiospeaker.sh')
            elif self_audio_device == 'handset': 
                self.run_pxcon_script('pxinject_audiohandset.sh')
            elif self_audio_device == 'headset': 
                self.run_pxcon_script('pxinject_audioheadset.sh')
            else:
                raise Exception("check_one_way_audio audio path fail")
            
            # Capture Audio            
            if other_audio_device == 'speaker':
                other_phone.run_pxcon_script('pxcapture_audiospeaker.sh')
            elif other_audio_device == 'handset': 
                other_phone.run_pxcon_script('pxcapture_audiohandset.sh')
            elif other_audio_device == 'headset': 
                other_phone.run_pxcon_script('pxcapture_audioheadset.sh')
            else:
                raise Exception("check_one_way_audio audio path fail")
            
            self.run_pxcon_script('pxsync_enable.sh')
            other_phone.run_pxcon_script('pxsync_enable.sh')
            # Audio plays for at least a second. No need for a sleep
            self.run_pxcon_script('pxrm_audio.sh')
            other_phone.run_pxcon_script('pxrm_audio.sh')
           
            # move pcm from tmp to /home/admin/
            filename = other_audio_device + "_capture.pcm"
            mv_cmd = 'mv /tmp/' + filename + ' ' + filename
            other_phone.run_bash_cmd(mv_cmd)

            self.get_file_from_phone(other_phone, filename)
            self.remove_file_on_phone(other_phone, filename)

            if "Mitel68" in self.phone_info['phoneModel']:
                filename = os.path.join(str(self.phone_info["tftpServerPath"]), filename)

            return (filename, self_audio_device)
            
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))          
        
    def check_two_way_audio(self, other_phone):
        try:
            self.update_devnull_permissions()
            self.upload_path_confirmation_files()
            
            other_phone.update_devnull_permissions()
            other_phone.upload_path_confirmation_files()
            
            filename, self_audio_device = self.run_pxcon_one_way_audio(other_phone)
            self.estimate_frequency(filename, self_audio_device)
           
            filename, self_audio_device = other_phone.run_pxcon_one_way_audio(self)
            self.estimate_frequency(filename, self_audio_device)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
            
    def get_file_from_phone(self, phone, get_path):
        try:
            phone.scp_get(get_path)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
                      
    def remove_file_on_phone(self, phone, rm_path):
        try:
            phone.phone_console_cmd('rm ' + rm_path, 'su')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
                           
    def check_pesq_mos_score(self, other_phone, voice=''):
        try:
            self.phone_obj.check_pesq_mos_score(other_phone, voice)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
