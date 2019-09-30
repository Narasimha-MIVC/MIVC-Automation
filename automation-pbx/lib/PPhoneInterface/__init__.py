import os
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger
# from robot.libraries.Telnet import Telnet
import telnetlib
import psutil
import shutil
import subprocess
import time
import re
import sys
from sys import platform as _platform
import collections
event_timeout = 7
kNumSoftKeys = 5
MAX_ONEWAY_RETRY = 8

########################################################
#     PPHONE KBD SERVER COMMANDS
########################################################

kDevice_Handset = 0
kDevice_Speaker = 1
kDevice_Headset = 2

deviceMap = {'handset': 0,'speaker':1,'headset':2}
halAudioMap = ['handset','speaker','headset']

########################################################
#     PPHONE KBD SERVER COMMANDS
########################################################
kKbd_Socket = 5666

kButton_Softkeys = ['a','b','c','d','e']

kButton_Softkey1 = "a"
kButton_Softkey2 = "b"
kButton_Softkey3 = "c"
kButton_Softkey4 = "d"
kButton_Softkey5 = "e"

kButton_Pound = "#"
kButton_Hash = "#"
kButton_Star = "*"
kButton_Conference = "C"
kButton_Directory = "D"
kButton_Headset = "E"
kButton_Hold = "H"
kButton_Hookswitch_Up = '\'K_\''
kButton_Hookswitch_Down = '\'K-\''

kButton_LeftLine1 = "("
kButton_LeftLine2 = "\\"
kButton_LeftLine3 = "["
kButton_LeftLine4 = "/"
kButton_RightLine1 = ")"
kButton_RightLine2 =  "}"
kButton_RightLine3 = "]"
kButton_RightLine4 = "\\"

kButton_Up = "^"
kButton_Down = ","
kButton_Left = "<"
kButton_Right = ">"

kButton_Mute = "M"
kButton_Redial = "R"
kButton_Enter = "."
kButton_Fire = "."
kButton_Backspace = "e"
kButton_Speaker = "S"
kButton_Transfer = "T"
kButton_VolumeDown = "-"
kButton_VolumeUp = "+"
kButton_voicemail = "V"
########################################################
#     PPHONE SOCKET INTERFACE COMMANDS
########################################################
Interface_Socket = 9005



kSoftkey_1 = "sk0"
kSoftkey_2 = "sk1"
kSoftkey_3 = "sk2"
kSoftkey_4 = "sk3"
kSoftkey_5 = "sk4"

kLedColor_Black = "0"
kLedColor_Red = "1"
kLedColor_Green = "2"
kLedColor_Yellow = "3"
kLedColor_Blue = "4"
kLedColor_Magenta = "5"
kLedColor_Cyan = "6"
kLedColor_White = "7"

kMap_CaIcon = "0"
kMap_caBackground = "1"
kMap_CaLabel = "2"
kMap_CaTimer = "3"

# kButton_RightLine1 = "line0"
# kButton_RightLine2 = "line1"
# kButton_RightLine3 = "line2"
# kButton_RightLine4 = "line3"
# kButton_LeftLine1 = "line4"
# kButton_LeftLine2 = "line5"
# kButton_LeftLine3 = "line6"
# kButton_LeftLine4 = "line7"

kCallAppearance_idleCall = '/images/callappearance/idle.png'
#kCallAppearance_dialingCall = '/images/callappearance/dialing_selected.p'
kCallAppearance_p8_dialingCall = '/images/callappearance/dialing_selected.p'
kCallAppearance_p8cg_dialingCall = '/images/callappearance/dialing.png'
kCallAppearance_p8cg_incomingCall = '/images/callappearance/incoming.png'
kCallAppearance_connectedCall = '/images/callappearance/connected.png'
kCallAppearance_localHold = '/images/callappearance/local_hold.png'
kCallAppearance_remoteHold = '/images/callappearance/remote_hold.png'

kCallAppearance_p8_incomingCall = '/images/callappearance/incoming_selected'

kCallAppearance_p2_incomingCall = '/images/callappearance/incoming_selected.png'
kCallAppearance_p2_dialingCall = '/images/callappearance/dialing_selected.png'


WIN_ATF_PATH = "C:\\Robot-ATF\\Automation_Framework\\"
MAC_ATF_PATH = "populate_me"
LINUX_ATF_PATH = "populate_me"
OS_ATF_PATH = ""

# mvilleda - Pphone CLI lib
class PPhoneInterface(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        global OS_ATF_PATH
        print "DEBUG: In PPhoneTelnetInterface init ***"
        if _platform == "linux" or _platform == "linux2":
            # linux
            OS_ATF_PATH = LINUX_ATF_PATH
        elif _platform == "darwin":
            OS_ATF_PATH = MAC_ATF_PATH
            # OS X
        elif _platform == "win32":
            # Windows...
            OS_ATF_PATH = WIN_ATF_PATH
            print(OS_ATF_PATH)
        # logger.warn("Loading %s robot parameters from %s" % (_platform,OS_ATF_PATH))

    def pphone_util_shell_cmd(self, user, cmd):
        """Runs cmd dm_query using phoneutil.exe on user

        :param user: User dict
        :type user: type dict
        :param cmd: phoneutil cmd
        :type cmd: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not dm_query does not match
        """
        global OS_ATF_PATH
        pphoneutil_path = OS_ATF_PATH + 'util\pphoneutil\phoneutil.exe'
        pphoneutil_hq_rsa = OS_ATF_PATH + 'util\pphoneutil\\rsa_keys\hq_rsa'
        sys_cmd = pphoneutil_path + " -ip " + user.ip + " -rsa " + pphoneutil_hq_rsa + " -shell \"" + cmd + "\""
        print "Running phoneutil cmd: \"%s\"" % sys_cmd
        result = subprocess.check_output(sys_cmd, shell=True)
        return result

    def pphone_util(self, user, cmd, dm_query):
        """Runs cmd dm_query using phoneutil.exe on user

        :param user: User dict
        :type user: type dict
        :param cmd: phoneutil cmd
        :type cmd: type str
        :param dm_query: Run dm_query
        :type dm_query: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not dm_query does not match
        """
        global OS_ATF_PATH
        pphoneutil_path = OS_ATF_PATH + 'util\pphoneutil\phoneutil.exe'
        pphoneutil_hq_rsa = OS_ATF_PATH + 'util\pphoneutil\\rsa_keys\hq_rsa'
        sys_cmd = pphoneutil_path + " -ip " + user.ip + " -rsa " + pphoneutil_hq_rsa + " -shell \"" + cmd + " " + dm_query + "\""
        print "Running phoneutil cmd: \"%s\"" % sys_cmd
        result = subprocess.check_output(sys_cmd, shell=True)
        print "cmd output: %s" % result
        matchObj = re.match( r'.*->(.*)->Terminated.*', result, re.DOTALL)
        if matchObj:
           dm_pair = matchObj.group(1).rstrip('\r\n')
           dm_pair = dm_pair.split("=")
           if re.match(dm_query, dm_pair[0]):
               print "\"%s\" matched returning \"%s\"" % (dm_query, dm_pair[1])
               return dm_pair[1].strip()
           else:
               raise Exception("%s did not match %s in pphone_util" % (dm_query, dm_pair[0]))
        else:
            raise Exception("Pphone util: \"%s\" match not found in result %s." % (dm_query, result))

    def getdm_session_count(self, user):
        """Returns number of sessions

        :param user: User dict
        :type user: type dict
        :return ret_val: Number of sessions on phone
        :rtype: int
        """
        val = None
        for i in range(3):
            try:
                val = int(self.pphone_util(user, "cli -c getdm", "callstackdm.sessionCount"))
            except:
                pass
            print "********%s %s"%(val,type(val))
            # val = ""
            if val is not None and val != "":
                if int(val) >= 0:
                    print "********Value found"
                    break
                    #return int(val)
            else:
                #waiting for the session count to update
                print "==========Checking for sessionCount:%s" % i
                print "---------Checking for session:%s" % i
                time.sleep(1)
        else:
            print "Value not found"

        return val

    def getdm_active_audio_path(self, user):
        """Returns active audio path

        :param user: User dict
        :type user: type dict
        :return ret_val: Active audio path, kDevice_Handset 0, kDevice_Speaker 1, kDevice_Headset 2
        :rtype: str
        """
        return self.pphone_util(user, "cli -c getdm", "audio.activeDevice")

    def pphone_get_progbutton_info(self, user, btn=1):
        """Returns active audio path

        :param user: User dict
        :type user: type dict
        :rtype: str
        """
        btninfo = self.pphone_util(user, "cli -c getdm", "progbuttons.0.%s.param"%btn).split(';')
        return btninfo

    def getdm_pphone_muted(self, user):
        """Returns (on/off) if phone is muted

        :param user: User dict
        :type user: type dict
        :return ret_val: On if phone muted else off
        :rtype: str
        """
        return self.pphone_util(user, "cli -c getdm", "audio.muteOn")


    def getdm_caller_number(self, user, ca):
        """Returns (on/off) if phone is muted

        :param user: User dict
        :type user: type dict
        :param ca: Call appearance
        :type ca: type string
        :return ret_val:  Returns calle number on ca
        :rtype: str
        """
        logger.warn("In getdm_callee_number. TODO map ca to session number")
        return self.pphone_util(user, "cli -c getdm", "callstackdm.session1.iden.displaynumber")


    def getdm_caller_name(self, user):
        """Returns (on/off) if phone is muted

        :param user: User dict
        :type user: type dict
        :param ca: Call appearance
        :type ca: type string
        :return ret_val:  Returns calle number on ca
        :rtype: str
        """
        #logger.warn("In getdm_callee_number. TODO map ca to session number")
        return self.pphone_util(user, "cli -c getdm", "user.userFirstName")


    def verify_pphone_idle(self, user):
        """Verifies if phone user is idle

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not idle
        """
        sessioncount = self.getdm_session_count(user)
        if  sessioncount == 0:
            print "verify_pphone_idle: Pphone is idle"
        else:
            raise Exception("verify_pphone_idle: Session count = \"%s\" pphone is not idle" % sessioncount)

    def verify_pphone_muted(self, user):
        """Verifies if phone user is mutes

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if not muted
        """
        if self.getdm_pphone_muted(user) == "on":
            print "MUTE verified"
        else:
            raise Exception("verify_pphone_muted: Pphone is not muted")

    def verify_pphone_active_audio_path(self, user, audiopath):
        """Verifies if phone user is idle

        :param user: User dict
        :type user: type dict
        :param audiopath: 0, 1, 2
        :type audiopath: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        path = int(self.getdm_active_audio_path(user))
        if path == audiopath:
            print "Audio path verified"
        else:
            raise Exception("verify_pphone_active_audio_path: Audio path \"%s\" did not match \"%s\"" % (audiopath,path))

 ########################################################
 #     PPHONE KBD SERVER METHODS
 ########################################################

    def pphone_press_button(self, user, button):
        """Press Button on Pphone via kbd socket

        :param user: User dict
        :type user: type dict
        :param button: Char value for button mapping
        :type button: type str
        :return ret_val: none
        """
        print "Running kbd socket cmd \"%s\" on phone %s" % (button, user.ip)
        tn = telnetlib.Telnet(user.ip, kKbd_Socket)
        tn.write(str(button) + "\n")

    def pphone_press_button_raw(self, user, button):
        """Press Button on Pphone via kbd socket

        :param user: User dict
        :type user: type dict
        :param button: Char value for button mapping
        :type button: type str
        :return ret_val: none
        """
        print "Running kbd socket cmd \"%s\" on phone %s" % (button, user.ip)
        tn = telnetlib.Telnet(user.ip, kKbd_Socket)
        tn.write(button + "\n")

    def pphone_dial_digits(self, user, digits):
        """Dial Digits via kbd socket

        :param user: User dict
        :type user: type dict
        :param digits: string of digits
        :type digits: type str
        :return ret_val: none
        """
        print "Running kbd socket cmd \"%digits\" on phone %s" % (digits, user.ip)
        tn = telnetlib.Telnet(user.ip, kKbd_Socket)
        tn.write(str(digits) + "\n")

    def pphone_press_button_pound(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Pound)

    def pphone_press_button_hash(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hash)

    def pphone_press_button_star(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Star)

    def pphone_press_button_conference(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Conference)

    def pphone_press_button_directory(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Directory)

    def pphone_press_button_headset(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Headset)

    def pphone_press_button_hold(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hold)

    def pphone_handset_up(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button_raw(user, kButton_Hookswitch_Up)

    def pphone_handset_down(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Hookswitch_Down)

    def pphone_handset_disconnect_call(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_handset_up(user)
        self.pphone_handset_down(user)

    def pphone_press_button_rightLine1(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine1)

    def pphone_press_button_rightLine2(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        self.pphone_press_button(user, kButton_RightLine2)

    def pphone_press_button_rightLine3(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine3)

    def pphone_press_button_rightLine4(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_RightLine4)

    def pphone_press_button_leftLine1(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine1)

    def pphone_press_button_leftLine2(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine2)

    def pphone_press_button_leftLine3(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine3)

    def pphone_press_button_leftLine4(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_LeftLine4)

    def pphone_press_button_up(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Up)

    def pphone_press_button_down(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Down)

    def pphone_press_button_left(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Left)

    def pphone_press_button_right(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Right)

    def pphone_press_button_softkey1(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey1)


    def pphone_press_button_softkey2(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey2)

    def pphone_press_button_softkey5(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey5)

    def pphone_press_button_softkey3(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey3)

    def pphone_press_button_softkey4(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Softkey4)

    #  TODO def pphone_press_button_softkey5(self, user):

    def pphone_press_button_mute(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Mute)

    def pphone_press_button_redial(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Redial)

    def pphone_press_button_enter(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Enter)

    def pphone_press_button_fire(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Fire)

    def pphone_press_button_backspace(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Backspace)

    def pphone_press_button_speaker(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Speaker)

    def pphone_press_button_transfer(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_Transfer)

    def pphone_press_button_voicemail(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_voicemail)

    def pphone_press_button_volumeDown(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_VolumeDown)

    def pphone_press_button_volumeUp(self, user):
        """Press PPhone button via kbd server

        :param user: User dict
        :type user: type dict
        :return ret_val: none
        """
        self.pphone_press_button(user, kButton_VolumeUp)

########################################################
 #     PPHONE SOCKET INTERFACE METHODS
 ########################################################

    def si_query(self, user_from, query):
        """Socket Interface main cmd method

        :param user: User dict
        :type user: type dict
        :param query: Query to be run on socket interface
        :type query: type str
        :return ret_val: Result of query
        """
        #  TODO replace with log level
        print "Running socket cmd: %s on phone %s" % (query, user_from.ip)
        tn = telnetlib.Telnet(user_from.ip, Interface_Socket)
        tn.write(str(query) + "\n")
        return tn.read_some()

    def pphone_search_softkey_text(self, user, text):
        """Searches for softkey text

        :param user: User dict
        :type user: type dict
        :param text: Softkey text to be searched
        :type text: type str
        :return ret_val: Index of softkey, -1 if not found
        """
        pattern = ".*%s" % text
        for i in range(0,kNumSoftKeys):
            cmd = "getsk sk{0}".format(i)
            sk = self.si_query(user, cmd)
            #  Check if sk is empty
            if not re.match(".*png",sk):
                #  TODO  softkey has no image, procees
                #  TODO  remove RS char from sk
                if len(sk.strip()) < 8:
                    print "Skipping empty softkey %s" % sk
                    continue
                sk_text = sk.split("5")[1].strip()
                print sk_text
            else:
                str = sk.split(":")
                sk_img = str[1]
                str = str[0].split("5")
                sk_text =  str[1]
            if re.match(pattern,sk_text):
                print "Text %s found at index %d" % (text,i)
                return i
        print "Text %s not found" % text
        return -1

    def wait_for_call_appearance(self, user_callee, ca_type, ca_line):
        """Polls for ca_type match on line ca_line for timeout time

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_type: Call appearance type
        :type ca_type: type str
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        ca_lines = {'right_line1': 'line0', 'right_line2': 'line1', 'right_line3': 'line2', 'right_line4': 'line3', 'left_line1': 'line4', 'left_line2': 'line5', 'left_line3': 'line6', 'left_line4': 'line7', }

        line = ca_lines[ca_line.lower()]
        cmd = "getline " + line + " 1"
        pattern = ".*%s" % ca_type
        timeout = time.time() + event_timeout
        while True:
            time.sleep(1)
            resp = self.si_query(user_callee, cmd)
            if re.match(pattern, resp):
                print "\"%s\" MATCHED!" % ca_type
                break
            if time.time() > timeout:
                raise Exception("\"%s\" does not re.match with \"%s\"" % (resp, pattern))
                break
            #  TODO replace with log level
            print "sleeping 1 second for pattern %s" % pattern

    def wait_for_idle_call(self, user_callee, ca_line):
        """Polls for idle state match on line ca_line

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_idleCall, ca_line)

    def wait_for_dialing_call(self, user_callee, ca_line):
        """Polls for dialing state match on line ca_line

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        #self.wait_for_call_appearance(user_callee, kCallAppearance_dialingCall, ca_line)
        if user_callee.phone_type == 'p8cg':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8cg_dialingCall, ca_line)
        elif user_callee.phone_type == 'p8':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8_dialingCall, ca_line)
        elif user_callee.phone_type == 'p2':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p2_dialingCall, ca_line)
        else:
            raise Exception("Phone type %s does not exist")

    def wait_for_incoming_call(self, user_callee, ca_line):
        """Polls for icoming state match on line ca_line

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        Vasuja: Added 'kCallAppearance_p8cg_incomingCall'
        """
        if user_callee.phone_type == 'p8cg':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8cg_incomingCall, ca_line)
        elif user_callee.phone_type == 'p8':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p8_incomingCall, ca_line)
        elif user_callee.phone_type == 'p2':
            self.wait_for_call_appearance(user_callee, kCallAppearance_p2_incomingCall, ca_line)
        else:
            raise Exception("Phone type %s does not exist")


    def wait_for_connected_call(self, user_callee, ca_line):
        """Polls for connected state match on line ca_line

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_connectedCall, ca_line)

    def wait_for_local_hold_call(self, user_callee, ca_line):
        """Polls for local hold state match on line ca_line

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_localHold, ca_line)

    def wait_for_remote_hold_call(self, user_callee, ca_line):
        """Polls for remote hold state match on line ca_line

        :param user_callee: User dict
        :type user_callee: type dict
        :param ca_line: Call appearance line
        :type ca_line: type str
        :return ret_val: none
        """
        self.wait_for_call_appearance(user_callee, kCallAppearance_remoteHold, ca_line)


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

    def pphone_verify_caller_number(self, user_callee, user_caller, ca, num_format):
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
            pattern = ".*%s" % user_caller.sip_did

        caller_number = self.getdm_caller_number(user_callee,ca)
        if re.match(pattern, caller_number):
            return 1
        else:
            raise Exception("pphone_verify_caller_number: Pattern %s did not match caller_number \"%s\" for number format %s " % (pattern, caller_number,num_format))
        return 0


    def pphone_make_call(self, user_from, user_to, ca_line):

        """Makes call from user_from to user_to on ca_line

        :param user_from: User dict
        :type user_from: type dict
        :param user_to: User dict
        :type user_to: type dict
        :param ca_line: Call appearance line on which to make call
        :type ca_line: type str
        :return ret_val: none
        """
        tn = telnetlib.Telnet(user_from.ip, kKbd_Socket)
        tn.write(str(user_to.extension) + "\n")
        #check full string then return
        #import pdb;
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        self.wait_for_dialing_call(user_from, ca_line)

    def pphone_make_national_call(self, user_from, user_to, ca_line):

        """Makes call from user_from to user_to on ca_line

        :param user_from: User dict
        :type user_from: type dict
        :param user_to: User dict
        :type user_to: type dict
        :param ca_line: Call appearance line on which to make call
        :type ca_line: type str
        :return ret_val: none"""

        if str(type(user_to.did)) == "<type 'unicode'>":
            user_to.did = str(user_to.did)
        did = ""
        count = 0
        ndid = ""
        for i in user_to.did:
            if int(i) >= 0 and int(i) <= 9:
                did = did + i
        if len(did) <= 10:
            raise ("invalid DID")
            return
        for i in reversed(did):
            if(count >10):
                break
            ndid = i + ndid
            count=+1

        ndid = "9" + ndid
        tn = telnetlib.Telnet(user_from.ip, kKbd_Socket)
        tn.write(ndid  + "\n")
        time.sleep(4)
        #self.wait_for_dialing_call(user_from, ca_line)

    def disconnect_call_via_softkey(self, user_callee):
        """Disconnects user_callee call via softkey

        :param user_callee: User dict
        :type user_callee: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        index = self.pphone_search_softkey_text(user_callee, "Hang Up")
        if index == -1:
            raise Exception("disconnect_call_via_softkey: Failed softkey search for \"Hang Up\"")
        self.pphone_press_button(user_callee, kButton_Softkeys[index])

    def wait_for_history(self, user_callee):
        """Disconnects user_callee call via softkey

        :param user_callee: User dict
        :type user_callee: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        index = self.pphone_search_softkey_text(user_callee, "Dial")
        if index == -1:
            raise Exception("disconnect_call_via_softkey: Failed softkey search for \"Dial\"")
        self.pphone_press_button(user_callee, kButton_Softkeys[index])


    def pphone_disconnect_call(self, user, mode="-1"):
        """Disconnects user call via mode

        :param user: User dict
        :type user: type dict
        :param mode: handset-0, speaker-1, headset-2
        :type mode: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        audiopath = int(self.getdm_active_audio_path(user))
        if mode == "-1":
            if audiopath == kDevice_Handset:
                self.pphone_handset_down(user)
            elif audiopath == kDevice_Speaker:
                self.pphone_press_button(user, kButton_Speaker)
            elif audiopath == kDevice_Headset:
                self.pphone_press_button(user, kButton_Headset)
            else:
                raise Exception("disconnect_call: AudioPath %s does not exist" % audiopath)
        else:
            self.disconnect_call_via_softkey(user)
            # self.pphone_press_button(user_callee, mode)
        if self.getdm_session_count(user) != 0:
            self.disconnect_call_via_softkey(user)
        self.verify_pphone_idle(user)

    def pphone_answer_call(self, user_callee, user_caller, ca_line, answermode="-1"):
        """Disconnects user call via mode

        :param user_callee: User dict
        :type user_callee: type dict
        :param user_caller: User dict
        :type user_caller: type dict
        :param ca_line: Call appearance line to check incoming call
        :type ca_line: type str
        :param answermode: handset-0, speaker-1, headset-2
        :type answermode: type str
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        try:
            self.wait_for_incoming_call(user_callee, ca_line)
            if answermode == "-1":
                self.answer_via_headset(user_callee)
                self.verify_pphone_active_audio_path(user_callee, kDevice_Headset)
            else:
                if answermode == "0":
                    self.pphone_press_button(user_callee, kButton_Hookswitch_Up)
                elif answermode == str(kDevice_Speaker):
                    self.pphone_press_button(user_callee, "S")
                elif answermode == kDevice_Headset:
                    self.pphone_press_button(user_callee, kButton_Headset)
                else:
                    raise Exception("answer_call:  AudioPath %s does not exist" % answermode)
                    return
        except Exception as e:
            print e
            raise e

    def pphone_verify_call_duration (self, user_caller):
        pass

    def pphone_hold_call(self,user, ca_line):
        """Holds and verifies call on user

        :param user: User dict
        :type user: type dict
        :param ca_line: Call appearance line to check call hold
        :type ca_line: type str
        :return ret_val: none
        """
        self.pphone_press_button_hold(user)
        self.wait_for_local_hold_call(user, ca_line)


# Audio devices
#  kDevice_Handset 0
#  kDevice_Speaker 1
#  kDevice_Headset 2

    def pxcon_init_audio(self, user):
        print "Initializing modules to play audio via pxcon"
        print "This function need run only one time unless the phone is reboot"
        self.pphone_util_shell_cmd(user, "/bin/ash /bin/pxaudio_init.sh" )

    def pxcon_create_audio_inject_handle(self, user, audioPath):
        mode = "repeat"
        syncType = "sync"
        filename = ""

        device = deviceMap[audioPath]

        if device == 0:
            filename = "16k_500.pcm"
            self.pphone_util_shell_cmd(user,"pxcon /bin/pxinject_audiohandset.sh")
        elif device == 1:
            filename = "16k_3k.pcm"
            self.pphone_util_shell_cmd(user,"pxcon /bin/pxinject_audiospeaker.sh")
        elif device == 2:
            filename = "16k_1k.pcm"
            self.pphone_util_shell_cmd(user,"pxcon /bin/pxinject_audioheadset.sh")
        else:
            print "Device %s is not known!" % device
        print "Preparing to inject \\etc\\apt\\%s on device: %s mode: %s" % (filename, device, mode)

    def pxcon_create_audio_capture_handle(self, user, audioPath):
        mode = "truncate"
        syncType = "sync"
        filename = ""

        device = deviceMap[audioPath]

        if device == 0:
            filename = "/tmp/handsetcapture.pcm"
            self.pphone_util_shell_cmd(user,"pxcon /bin/pxcapture_audiohandset.sh")
        elif device == 1:
            filename = "/tmp/speakercapture.pcm"
            self.pphone_util_shell_cmd(user,"pxcon /bin/pxcapture_audiospeaker.sh")
        elif device == 2:
            filename = "/tmp/headsetcapture.pcm"
            self.pphone_util_shell_cmd(user,"pxcon /bin/pxcapture_audioheadset.sh")
        else:
            print "Device %s is not known!" % device
        print "Preparing to capture %s on device: %s mode: %s" % (filename, device, mode)


    def pxcon_sync_enable_audio(self, user):
        print "Playing/Enabling audio on %s..." % user.ip
        self.pphone_util_shell_cmd(user,"killall pxcon; pxcon /bin/pxsync_enable.sh")

    def pxcon_sync_disable_audio(self, user):
        print "Audio Stopped/Disabled on %s " % user.ip
        self.pphone_util_shell_cmd(user,"killall pxcon; pxcon /bin/pxsync_disable.sh")

    def pxcon_remove_audio_handles(self, user):
        print "Removing pxcon audio handles"
        self.pphone_util_shell_cmd(user,"killall pxcon; pxcon /bin/pxrm_audioh.sh; rm /tmp/*capture.pcm")
        print "Pxcon audio utils flushed and removed"

    def pphone_check_one_way_audio( self, user_inject, user_capture ):
        #import pdb;
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        inj_activeAudioDevice = int(self.getdm_active_audio_path(user_inject))
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        device = halAudioMap[inj_activeAudioDevice]
        other_device = halAudioMap[cap_activeAudioDevice]

        for i in range(0,MAX_ONEWAY_RETRY):
            time.sleep(6)
            audioPassed = 1
            self.pxcon_create_audio_inject_handle(user_inject, device)
            self.pxcon_create_audio_capture_handle(user_capture, other_device)

            self.pxcon_sync_enable_audio(user_inject)
            self.pxcon_sync_enable_audio(user_capture)
            time.sleep(3)
            self.pxcon_sync_disable_audio(user_capture)
            self.pxcon_sync_disable_audio(user_inject)

            freq = self.get_estimated_frequency(user_capture)

            self.pxcon_remove_audio_handles(user_inject)
            self.pxcon_remove_audio_handles(user_capture)

            if "2666" in freq:
                print "2k Hz sine tone detected on handset"
                if inj_activeAudioDevice != 0:
                    audioPassed = 0
                    print "Audio is not playing from injector handset"
            elif "4000" in freq:
                print "3k Hz sine tone detected on speaker"
                if inj_activeAudioDevice != 1:
                    audioPassed = 0
                    print "Audio is not playing from injector speaker"
            elif "500" in freq:
                print "500 Hz sine tone detected on headset"
                if inj_activeAudioDevice != 2:
                    audioPassed = 0
                    print "Audio is not playing from injector headset"
            else:
                audioPassed = 0
                print "Unkown frequency detected"
            if audioPassed == 1:
                print "Audio check PASSED"
                return
        if audioPassed == 0:
            raise Exception("One-way audio check FAILED")


    def pphone_check_no_audio( self, user_inject, user_capture ):
        inj_activeAudioDevice = int(self.getdm_active_audio_path(user_inject))
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        device = halAudioMap[inj_activeAudioDevice]
        other_device = halAudioMap[cap_activeAudioDevice]

        for i in range(0,MAX_ONEWAY_RETRY):
            audioPassed = 1
            self.pxcon_create_audio_inject_handle(user_inject, device)
            self.pxcon_create_audio_capture_handle(user_capture, other_device)

            self.pxcon_sync_enable_audio(user_inject)
            self.pxcon_sync_enable_audio(user_capture)
            time.sleep(3)
            self.pxcon_sync_disable_audio(user_capture)
            self.pxcon_sync_disable_audio(user_inject)

            #Check below should not detect any frequency
            freq = self.get_estimated_frequency(user_capture)

            self.pxcon_remove_audio_handles(user_inject)
            self.pxcon_remove_audio_handles(user_capture)

            if "2666" in freq:
                print "2k Hz sine tone detected"
                audioPassed = 0
            elif "4000" in freq:
                print "3k Hz sine tone detected"
                audioPassed = 0
            elif "500" in freq:
                print "500 Hz sine tone detected"
                audioPassed = 0
            else:
                # audioPassed = 0
                print "Frequency: %s detected" % freq

            if audioPassed == 1:
                print "Audio check PASSED"
                return
        if audioPassed == 0:
            raise Exception("No audio check FAILED")

    def pphone_check_two_way_audio( self, user, other_user ):
        self.pphone_check_one_way_audio(user, other_user)
        self.pphone_check_one_way_audio(other_user, user)

    def get_estimated_frequency( self, user_capture ):
        samplerate = 16000
        skip_samples = 10000
        cap_activeAudioDevice = int(self.getdm_active_audio_path(user_capture))

        files = ["/tmp/handsetcapture.pcm", "/tmp/speakercapture.pcm", "/tmp/headsetcapture.pcm"]
        filename = files[cap_activeAudioDevice]

        cmd = "estimate_freq " + str(samplerate) + " " + str(skip_samples) + " < " + filename
        print "Running cmd \"%s\"" % cmd
        result = self.pphone_util_shell_cmd(user_capture, cmd)
        print "estimated freq: %s" % result
        return result

 ########################################################
 #     PPHONE SANITY CHECKS
 ########################################################


    def pphone_reset_callstack(self,user):
        logger.info("Resetting callstack order")
        maxAttempts = 2
        attempt = 0

        result = self.pphone_util_shell_cmd(user, "cli -c sortSessionAvailableList")

        # Todo - Add loop to check result
        logger.info(result)
        if attempt == maxAttempts:
            raise Exception("Error in ResetCallstack: Method was unable to reset call stack in MAX num attempts")

    def pphone_force_idle_state(self,*args):
        """Forces pphone to idle state

        :param args: List of user dicts mapped to real pphones
        :type args: type list
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        for user in args:
            print user.ip
            self.pphone_reset_callstack(user)
            if self.getdm_session_count(user) != 0:
                index = self.pphone_search_softkey_text(user, "Hang Up")
                if index == -1:
                    #TODO check popup message and handle call hold
                    self.pphone_handset_up(user)
                    time.sleep(1)
                    self.pphone_handset_down(user)
            else:
                #  Check if softkey text Exit or Cancel are found
                index = self.pphone_search_softkey_text(user, "Exit")
                if index == -1:
                    index = self.pphone_search_softkey_text(user, "Cancel")
                    # if index == -1:
                        # raise Exception("phone_sanity_check: Sanity Check Failed")

            if index != -1:
                self.pphone_press_button(user, kButton_Softkeys[index])

            #Check again
            if self.getdm_session_count(user) != 0:
                index = self.pphone_search_softkey_text(user, "Hang Up")
                if index == -1:
                    #TODO check popup message and handle call hold
                    self.pphone_handset_up(user)
                    time.sleep(1)
                    self.pphone_handset_down(user)
            else:
                #  Check if softkey text Exit or Cancel are found
                index = self.pphone_search_softkey_text(user, "Exit")
                if index == -1:
                    index = self.pphone_search_softkey_text(user, "Cancel")
                    # if index == -1:
                        # raise Exception("phone_sanity_check: Sanity Check Failed")

            if index != -1:
                self.pphone_press_button(user, kButton_Softkeys[index])

            self.verify_pphone_idle(user)

    def pphone_sanity_check(self,*args):
        """Runs Sanity Check functions

        :param args: List of user dicts mapped to real pphones
        :type args: type list
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        self.pphone_force_idle_state(*args)

    def search_and_press_key(self, user_callee, key, position):
        """Disconnects user_callee call via softkey

        :param user_callee: User dict
        :type user_callee: type dict
        :return ret_val: none
        :raises ExceptionType: Raises robot exception if no match
        """
        if str(type(position)) == "<type 'unicode'>":
            position = int(position)
        index = self.pphone_search_softkey_text(user_callee, key)
        if index != position:
            raise Exception("Failed softkey search for \"key\"")
        self.pphone_press_button(user_callee, kButton_Softkeys[index])


if __name__ == '__main__':
    pp_obj = PPhoneInterface()
    #pp_obj.getdm_session_count({'ip': '10.198.18.108'})
    #pp_obj.verify_pphone_idle({'ip': '10.198.17.136'})
