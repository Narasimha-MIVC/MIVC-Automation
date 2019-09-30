"""
Module for BOSS portal functionalities
   Author: Regenrated from Kenash team code by GCO Team
"""

import os
import sys
import time
import telnetlib
from robot.api import logger
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
# import stafenv

from PPhoneInterface import PPhoneInterface

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from selenium.webdriver.remote.command import Command

Interface_Socket = 9005

class LoadPhoneInterface(object):

    def __init__(self):
        self._PPhoneInterface = PPhoneInterface()

    def init_audio(self, user):
        try:
            self._PPhoneInterface.pxcon_init_audio(user)
        except Exception as e:
            print (e)
            raise AssertionError("Audio Init Failed")

    def pphone_sanity_check(self, *args):

        try:
            self._PPhoneInterface.pphone_sanity_check(*args)
        except Exception as e:
            print (e)
            raise AssertionError("Sanity Check is failed")

    def pphone_make_call(self, user_from, user_to, ca_line):
        try:
            self._PPhoneInterface.pphone_make_call(user_from, user_to, ca_line)
        except Exception as e:
            print (e)
            raise AssertionError("Make call Fail")

    def pphone_make_call_number(self, user_from, user_to, ca_line):
        try:
            self._PPhoneInterface.pphone_make_call_number(user_from, user_to, ca_line)
        except Exception as e:
            print (e)
            raise AssertionError("Make call Fail")

    def pphone_answer_call(self, user_callee, user_caller, ca_line, answermode):
        try:
            self._PPhoneInterface.pphone_answer_call(user_callee, user_caller, ca_line, answermode)
            time.sleep(3)
        except Exception as e:
            print (e)
            raise AssertionError("Call Answering Failed")

    def getdm_active_audio_path(self, user):
        try:
            self._PPhoneInterface.getdm_active_audio_path(user)
        except Exception as e:
            print (e)
            raise AssertionError("Audio path failed")

    def pphone_make_national_call(self, user_from, user_to, ca_line):
        try:

            self._PPhoneInterface.pphone_make_national_call(user_from, user_to, ca_line)
        except Exception as e:
            print (e)
            raise AssertionError("National call failed")

    def disconnect_call_via_softkey(self, user_callee):
        try:
            self._PPhoneInterface.disconnect_call_via_softkey(user_callee)
        except Exception as e:
            print (e)
            raise AssertionError("Call Disconnect failed")

    def wait_for_history(self, user_callee):
        try:
            self._PPhoneInterface.wait_for_history(user_callee)
        except Exception as e:
            print (e)
            raise AssertionError("History loading Failed")

    def pphone_star_button(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_star(user)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press STAR Button")

    def pphone_press_softkey2(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_softkey2(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Press Voicemail Button Failed")

    def pphone_press_softkey3(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_softkey3(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("soFtkey3 failed ")

    def pphone_press_softkey4(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_softkey4(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("soFtkey4 failed ")

    def pphone_open_voicemail(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_voicemail(user)
        except Exception as e:
            print (e)
            raise AssertionError("Press Voicemail Button Failed")

    def pphone_enter_digits(self, user, digits):
        try:
            self._PPhoneInterface.pphone_press_button(user, digits)
            time.sleep(1)

        except Exception as e:
            print (e)
            raise AssertionError("Entering digits Failed")

    def pphone_redial_button(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_redial(user)
        except Exception as e:
            print (e)
            raise AssertionError("Error in Redial")

    def pphone_reset_status(self, user):
        try:
            self._PPhoneInterface.pphone_handset_up(user)
            time.sleep(1)
            self._PPhoneInterface.pphone_handset_down(user)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to reset phone status")

    def pphone_hash_button(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_hash(user)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press HASH Button")

    def pphone_press_softkey1(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_softkey1(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press Dial Button")

    def pphone_press_softkey5(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_softkey5(user)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press OK Button")

    def pphone_press_rightLine1(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_rightLine1(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button1 ")

    def pphone_press_rightLine2(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_rightLine2(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button2 ")

    def pphone_press_rightLine3(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_rightLine3(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button3 ")

    def pphone_press_rightLine4(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_rightLine4(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button3 ")

    def pphone_press_leftLine1(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_leftLine1(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press left Button3 ")


    def pphone_press_Speaker(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_speaker(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button1 ")

    def reset_pphone(self, *args):
        try:
            self._PPhoneInterface.pphone_force_idle_state(*args)
        except Exception as e:
            print ("error")

    def pphone_verify_Silent_Monitor_display(self, user_callee):
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            p = "Silent monitor"
            pattern = ".*%s" % p
            resp = self.si_query(user_callee, "getline line0 3")
            if re.match(pattern, resp):
                return 1
            else:
                raise Exception("display should show Silent monitor string")
                return 0
    def pphone_verify_Barge_display(self, user_callee):
        p = "Conference"
        pattern = ".*%s" % p
        resp = self.si_query(user_callee, "getline line0 3")
        if re.match(pattern, resp):
            return 1
        else:
            raise Exception("display should show confernce string")
            return 0

    def pphone_verify_Silent_Coach_display(self, user_callee):
        p = "Silent coach"
        pattern = ".*%s" % p
        resp = self.si_query(user_callee, "getline line0 3")
        if re.match(pattern, resp):
            return 1
        else:
            raise Exception("display should show Silent coach string")
            return 0

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

    def mute_pphone(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_mute(user)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press Mute Button")

    def verify_mute_pphone(self, user):
        try:
            self._PPhoneInterface.verify_pphone_muted(user)
        except Exception as e:
            print (e)
            raise AssertionError("Error in Mute verify")

    def verify_WMI_status(self, user):
        try:
            var = self._PPhoneInterface.getdm_pphone_WMI(user)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("Error in WMI verify")

    def pphone_hold(self, user, ca_line):
        try:
            #import  pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self._PPhoneInterface.pphone_press_button_hold(user)
        except Exception as e:
            print (e)
            raise AssertionError("Error In Hold")

    def press_transfer(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_transfer(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Transfer failed")

    def press_Down(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_Down(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Pressing Down failed")

    def press_conference_key(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_conference(user)
        except Exception as e:
            print (e)
            raise AssertionError("Conference failed")

    def press_Directory_key(self, user):
        try:
            self._PPhoneInterface.pphone_press_button_directory(user)
        except Exception as e:
            print (e)
            raise AssertionError("Conference failed")

    def check_twoway_audio(self, uname1, uname2):
        try:
            self._PPhoneInterface.pphone_check_two_way_audio(uname1, uname2)
        except Exception as e:
            print (e)
            raise AssertionError("Two way Audio not found")

    def check_oneway_audio(self, uname1, uname2):
        try:
            self._PPhoneInterface.pphone_check_one_way_audio(uname1, uname2)
        except Exception as e:
            print (e)
            raise AssertionError("One way Audio not found")

    def phone_display_name(self, uname):
        try:
            var = self._PPhoneInterface.getdm_caller_name(uname)
        except Exception as e:
            print (e)
            raise AssertionError("Text not found")

    def pphone_press_button_rightLine(self,user):
        try:
            var = self._PPhoneInterface.pphone_press_button_rightLine2(user)
        except Exception as e:
            print (e)
            raise AssertionError("Text not found")

    def phone_CHS_state(self, uname):
        try:
            var = self._PPhoneInterface.getdm_CallhandlingState_User(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("Text not found")

    def phone_user_first_name(self, uname):
        try:
            var = self._PPhoneInterface.getdm_caller_name(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("Text not found")

    def phone_voicemail_count(self, uname):
        try:
            var = self._PPhoneInterface.Voicemail_count(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("VM count not able to find")

    def phone_voicemail_count_validation(self, before, after, CountUpOrCountDown):
        try:
            var = self._PPhoneInterface.verify_Voicemail_count_validation(before, after, CountUpOrCountDown)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("VM count not able to validate")

    def getdm_session_count(self, uname):
        try:
            var = self._PPhoneInterface.getdm_session_count(uname)
        except Exception as e:
            print (e)
            raise AssertionError("session not found")

    def user_workgroup_name(self, uname):
        try:
            var = self._PPhoneInterface.getdm_workgroup_name(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("group name not found")

    def user_popup_Messages(self, uname):
        try:
            var = self._PPhoneInterface.getdm_popup_Messages(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("popup not found")

    def user_Connected_Server(self, uname):
        try:
            var = self._PPhoneInterface.getdm_Connected_Server(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("group name not found")

    def user_display_name(self, uname):
        try:
            var = self._PPhoneInterface.getdm_display_name(uname)
            return var
        except Exception as e:
            print (e)
            raise AssertionError("group name not found")

    def wait_for_clear_key(self, user_callee):
        try:
            self._PPhoneInterface.wait_for_clear_key(user_callee)
        except Exception as e:
            print (e)
            raise AssertionError("Clear key loading Failed")

    def search_for_key_position(self, user_callee, key, position):
        try:
            self._PPhoneInterface.search_for_key(user_callee, key, position)
        except Exception as e:
            print (e)
            raise AssertionError("Search Failed for key: " + key)

    def search_and_press_key_position(self, user_callee, key, position):
        try:
            self._PPhoneInterface.search_and_press_key(user_callee, key, position)
        except Exception as e:
            print (e)
            raise AssertionError("Search Failed for key: " + key)

    def check_phone_clear_status(self, user_callee):
        try:
            return self._PPhoneInterface.check_clear_status(user_callee)
        except Exception as e:
            print (e)
            raise AssertionError("Validation failed for Clear function")

    def check_phone_date_time(self, user, option):
        try:
            return self._PPhoneInterface.pphone_cli_date_time(user, option)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to get date OR time")

    def pphone_press_rightLine1(self,user):
        try:
            self._PPhoneInterface.pphone_press_button_rightLine1(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button1 ")

    def pphone_press_Speaker(self,user):
        try:
            self._PPhoneInterface.pphone_press_button_speaker(user)
            time.sleep(1)
        except Exception as e:
            print (e)
            raise AssertionError("Unable to Press right Button1 ")
