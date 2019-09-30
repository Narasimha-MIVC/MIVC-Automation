"""
Interface for mitel 6xxx and shoretel ip4xx phones
"""
from __future__ import division

__author__ = "milton.villeda@mitel.com, nitin.kumar-2@mitel.com"

import sys
import time

from phone_4xx import IP4xxInterface
from phone_6xxx.phone_69xx import Phone_69xx
from phone_6xxx.phone_68xx import Phone_68xx

from robot.api import logger

class PhoneInterface(object):
    """ This class is the Phone workflow layer
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    phone_types = ["phone_4xx", "Mitel6940", "Mitel6930", "Mitel6920", "Mitel6910"]
    total_phones = 0
    
    def __init__(self, phone_info, *args):
        """ 
        :param phone_info:    phone_info Dict
        :param args:
        """
        self.phone_type = phone_info['phoneModel']

        if self.phone_type not in self.phone_types:
            raise Exception("Phone type: \"%s\" is not supported. Please use a phone type from the list %s" % (self.phone_type,self.phone_types))

        if "phone_4xx" in self.phone_type:
            self.phone_obj = IP4xxInterface.IP4xxInterface(phone_info)
        elif "Mitel69" in self.phone_type:
            self.phone_obj = Phone_69xx(phone_info)
        elif "Mitel68" in self.phone_type:
            self.phone_obj = Phone_68xx(phone_info)

        PhoneInterface.total_phones += 1
        # self.sanity_check()

    def print_total_phones(self):
        logger.info("Total phones in the test: %s" % PhoneInterface.total_phones)
        

    def enable_ssh_on_68xx(self):
        try:
            self.phone_obj.enable_ssh_on_68xx()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def run_pxcon_one_way_audio(self, other_phone):
        try:
            self.phone_obj.run_pxcon_one_way_audio(other_phone.phone_obj)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_two_way_audio(self, other_phone):
        try:
            self.phone_obj.check_two_way_audio(other_phone.phone_obj)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_audio_is_on_hold(self, other_phone, moh_enabled=False):
        try:
            self.phone_obj.check_audio_is_on_hold(other_phone.phone_obj, moh_enabled)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def scp_put(self, file):
        try:
            self.phone_obj.scp_put(file)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def scp_get(self, file):
        try:
            self.phone_obj.scp_get(file)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
                        
    def upload_path_confirmation_files(self):
        try:
            self.phone_obj.upload_path_confirmation_files()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
                                  
    def update_devnull_permissions(self):
        try:
            self.phone_obj.update_devnull_permissions()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def sanity_check(self):
        try:
            self.phone_obj.phone_sanity_check()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def make_call(self, phone_info_dict):
        try:
            self.phone_obj.make_call(phone_info_dict)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def answer_call(self):
        try:
            self.phone_obj.answer_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def dial_number(self, num):
        try:
            self.phone_obj.dial_number(num)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))

    def enter_a_number(self, num):
        try:
            self.phone_obj.enter_a_number(num)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
       
    def handset_up(self):
        try:
            self.phone_obj.handset_up()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
        
    def get_active_audio_device(self):
        try:
            self.phone_obj.get_active_audio_device()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception("func '%s' - err: '%s'!" % (fn, err))
                  
    def verify_led_notificaion_when_diversion_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_diversion_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_diversion_de_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_diversion_de_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_follow_me_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_follow_me_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_profile_number(self, profile_number):
        """This method ...

        Args:
            profile_number: string

        """
        try:
            self.phone_obj.verify_call_profile_number(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name 
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l1key(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_l1key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_l2key(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_l2key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey(self, sk_num):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_hold()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey(self, sk_num=1):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_softkey(sk_num)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_softkey_three(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_softkey_three()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_mute(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_mute()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_hold(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_hold()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_handsfree(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_handsfree()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_offhook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_offhook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_onhook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_onhook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumeup(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_volumeup()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_volumedown(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.press_volumedown()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_in_ring(self, extension):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.verify_display_notification_when_in_ring(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_notification_when_diversion_activated(self, diversion_category):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.verify_display_notification_when_diversion_activated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def de_activate_do_not_disturb(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.de_activate_do_not_disturb()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_monitoring(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_monitoring()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_display_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_display_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_key_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_key_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_led_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_led_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disable_all_monitors(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.disable_all_monitors()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_line_monitor(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.enable_line_monitor()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_idle(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.set_to_idle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_config(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.get_config()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def connect_to_terminal(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.connect_to_terminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_terminal(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.disconnect_terminal()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def format_response(self, response_signal):
        """This method ...

        Args:
            response_signal: string

        """
        try:
            self.phone_obj.format_response(response_signal)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

##################################################################
#   PHYSICAL BUTTON PRESS using /bin/input command
##################################################################

    def press_phys_button(self, button_str, options=None):
        """This method presse a physical button
            using /bin/input
        Args:
            button_str: button to be pressed
        """
        try:
            # start_time = time.time()
            self.phone_obj.press_phys_button(button_str.lower(), options)
            logger.info('Phone "%s" pressing button "%s" with options "%s"\n' % (self.phone_obj.phone_info['ipAddress'], button_str, options))
            # logger.warn('Time elapsed pressing button "%s" with options "%s": %.3f s\n' % (button_str, options, (time.time() - start_time)))
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_digits(self, digit_str):
        """This method presses digits

        Args: Nonw
        """
        self.press_phys_button(digit_str, 'multiple_btns')

    def end_call(self):
        """This method presses digits

        Args: Nonw
        """
        self.press_phys_button('end')

    def press_hansfree_button(self):
        """This method presses the physical button handsfree

        Args: Nonw

        """
        self.press_phys_button('handsfree')

    def handset_offhook(self):
        """This method simulates going offhook on handset

        Args: Nonw
        """
        self.press_phys_button('hookswitch', 'offhook')
        
    def handset_onhook(self):
        """This method simulates going onhook on handset

        Args: Nonw
        """
        self.press_phys_button('hookswitch', 'onhook')

    def hdndset_up_down(self):
        """This method ...

        Args:

        """
        try:
            self.press_phys_button('hookswitch')
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

##################################################################
#   PHYSICAL BUTTON PRESS       BLOCK END
##################################################################

    def press_hard_key(self):
        """This method ...

        Args:
            1: HardPhone.Keys

        """
        try:
            self.phone_obj.press_hard_key(1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def collect_responses(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.collect_responses()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def collect_ack(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.collect_ack()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_response_buckets(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.clear_response_buckets()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request(self, signal_to_be_sent):
        """This method ...

        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone_obj.send_request(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def send_request_with_fresh_sequence_number(self, signal_to_be_sent):
        """This method ...

        Args:
            signal_to_be_sent: byte[]

        """
        try:
            self.phone_obj.send_request_with_fresh_sequence_number(signal_to_be_sent)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def answer_the_call(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.answer_the_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def reject_the_call(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.reject_the_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def disconnect_the_call(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.disconnect_the_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def off_hook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.off_hook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def on_hook(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.on_hook()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_extension(self, extension_to_be_called):
        """This method ...

        Args:
            extension_to_be_called: HardPhone

        """
        try:
            self.phone_obj.call_to_an_extension(extension_to_be_called)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code(self, service_code):
        """This method ...

        Args:
            service_code: string

        """
        try:
            self.phone_obj.dial_service_code(service_code)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_anumber(self, terminal_phone):
        """This method ...

        Args:
            terminal_phone: HardPhone

        """
        try:
            self.phone_obj.dial_anumber(terminal_phone)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_anumber(self, number_to_be_dialled):
        """This method ...

        Args:
            number_to_be_dialled: string

        """
        try:
            self.phone_obj.dial_anumber(number_to_be_dialled)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_anumber(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            self.phone_obj.dial_anumber(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_key(self, key_to_be_pressed, press_count=1):
        """This method ...

        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone_obj.press_key(key_to_be_pressed, press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_vm_soft_key(self):
        try:
            self.phone_obj.press_vm_soft_key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_vm_hard_key(self):
        try:
            self.phone_obj.press_vm_hard_key()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_to_voicemail(self, pin):
        try:
            self.phone_obj.login_to_voicemail(pin)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def make_conference(self):
        try:
            self.phone_obj.make_conference()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def consult_conference(self):
        try:
            self.phone_obj.consult_conference()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_conference(self):
        try:
            self.phone_obj.accept_conference()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_blind_conference(self):
        try:
            self.phone_obj.accept_blind_conference()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_transfer(self):
        try:
            self.phone_obj.make_transfer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_blind_transfer(self):
        try:
            self.phone_obj.make_blind_transfer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_consult_transfer(self):
        try:
            self.phone_obj.make_consult_transfer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_blind_transfer(self):
        try:
            self.phone_obj.accept_blind_transfer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def accept_consult_transfer(self):
        try:
            self.phone_obj.accept_consult_transfer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def click_on_park(self):
        try:
            self.phone_obj.click_on_park()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def park_the_call(self):
        try:
            self.phone_obj.park_the_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def click_on_unpark(self):
        try:
            self.phone_obj.click_on_unpark()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def unpark_the_call(self):
        try:
            self.phone_obj.unpark_the_call()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_mute_state(self):
        try:
            self.phone_obj.verify_mute_state()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_hold_state(self):
        try:
            self.phone_obj.verify_hold_state()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_history(self):
        try:
            self.phone_obj.call_from_history()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def go_to_directory(self):
        try:
            self.phone_obj.go_to_directory()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_directory(self):
        try:
            self.phone_obj.call_from_directory()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def quit_voice_mail(self):
        try:
            self.phone_obj.quit_voice_mail()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_msgwait_led_state(self):
        try:
            self.phone_obj.verify_msgwait_led_state()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def press_expansion_box_key(self, key_to_be_pressed, press_count=1):
        """This method ...

        Args:
            key_to_be_pressed: int

        """
        try:
            self.phone_obj.press_expansion_box_key(key_to_be_pressed, press_count)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def release_key(self, key_to_be_released):
        """This method ...

        Args:
            key_to_be_released: HardPhone.Keys

        """
        try:
            self.phone_obj.release_key(key_to_be_released)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def input_a_number(self, string_to_dial):
        """This method ...

        Args:
            terminal_phone: string

        """
        try:
            self.phone_obj.input_a_number(string_to_dial)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_remote_extension(self, number_r1):
        """This method ...

        Args:
            number_r1: HardPhone

        """
        try:
            self.phone_obj.call_from_remote_extension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def call_from_sip_mobile_extension(self, number_r1):
        """This method ...

        Args:
            number_r1: HardPhone

        """
        try:
            self.phone_obj.call_from_sip_mobile_extension(number_r1)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_ic_sdiversion_with_service_codes(self, diversion_category):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.activate_ic_sdiversion_with_service_codes(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code_and_verify_notifications(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            self.phone_obj.activate_dn_dwith_service_code_and_verify_notifications(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_dn_dwith_service_code(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.activate_dn_dwith_service_code()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_dn_dwith_service_code(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.deactivate_dn_dwith_service_code()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_group_dn_dwith_service_code(self, group_number):
        """This method ...

        Args:
            group_number: string

        """
        try:
            self.phone_obj.deactivate_group_dn_dwith_service_code(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def dial_service_code_and_verify_display(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            self.phone_obj.dial_service_code_and_verify_display(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_group_dn_dwith_service_code(self, group_number):
        """This method ...

        Args:
            group_number: string

        """
        try:
            self.phone_obj.activate_group_dn_dwith_service_code(group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_connection(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.check_phone_connection()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def connect_to_phone(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.connect_to_phone()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def program_follow_me_remotely(self, extension_number_to_be_routed):
        """This method ...

        Args:
            extension_number_to_be_routed: string

        """
        try:
            self.phone_obj.program_follow_me_remotely(extension_number_to_be_routed)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def cancel_active_call_back(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.cancel_active_call_back()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_dual_forking_extension(self, dual_forking_extension_number):
        """This method ...

        Args:
            dual_forking_extension_number: string

        """
        try:
            self.phone_obj.login_with_dual_forking_extension(dual_forking_extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_with_different_extension(self, extension_number):
        """This method ...

        Args:
            extension_number: string

        """
        try:
            self.phone_obj.login_with_different_extension(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def login_back_with_base_extension(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.login_back_with_base_extension()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_non_member_of_group(self, extension):
        """This method ...

        Args:
            extension: string

        """
        try:
            self.phone_obj.pick_call_with_non_member_of_group(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def pick_call_with_member_of_group(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.pick_call_with_member_of_group()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_state(self,LineStatus, activeLineNum="1", maxWaitTimeoutInSeconds = 10):
        """This method will verify the status of a line...

        Args:

        """
        try:
            return self.phone_obj.verify_line_state(str(LineStatus), str(activeLineNum), maxWaitTimeoutInSeconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_line_buffer(self):
        """This method will return the buffer containing the state of al the lines on the phone...

        Args: None

        """
        try:
            return self.phone_obj.get_line_buffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_state(self,type, mode, timeout = 10):
        """This method will verify the status of a led...

        Args:

        """
        try:
            return self.phone_obj.verify_led_state(str(type), str(mode), timeout)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_led_buffer(self):
        """This method will return the buffer containing details of all leds on the phone...

        Args: None

        """
        try:
            return self.phone_obj.get_led_buffer()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_line_for_hunt_group(self, hunt_group_number):
        """This method ...

        Args:
            hunt_group_number: string

        """
        try:
            self.phone_obj.set_line_for_hunt_group(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def remove_line_for_hunt_group(self, hunt_group_number):
        """This method ...

        Args:
            hunt_group_number: string

        """
        try:
            self.phone_obj.remove_line_for_hunt_group(hunt_group_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def enable_message_waiting(self, extension):
        """This method ...

        Args:
            extension: string

        """
        try:
            self.phone_obj.enable_message_waiting(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def intrusion_from_extension(self, extension):
        """This method ...

        Args:
            extension: HardPhone

        """
        try:
            self.phone_obj.intrusion_from_extension(extension)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_pe_ndeactivated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_pe_ndeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_not_responding(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_not_responding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_cancel_call(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_cancel_call(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """This method ...

        Args:
            vacant_number: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_dial_vacant_number(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_reroutingto_in_attend_when_dial_logged_off_terminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_private_trunk_reroutingto_in_attend_when_not_responding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_cancel_call(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_private_reroutingto_in_attend_when_cancel_call(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_vacant_number(self, vacant_number):
        """This method ...

        Args:
            vacant_number: string

        """
        try:
            self.phone_obj.verify_private_reroutingto_in_attend_when_dial_vacant_number(vacant_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_private_reroutingto_in_attend_when_dial_logged_off_terminal(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_private_reroutingto_in_attend_when_dial_logged_off_terminal(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_external_call_to_in_attend(self, in_attend_number):
        """This method ...

        Args:
            in_attend_number: string

        """
        try:
            self.phone_obj.verify_external_call_to_in_attend(in_attend_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def set_to_default(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.set_to_default()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def check_phone_is_online(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.check_phone_is_online()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def sleep(self, seconds):
        """This method ...

        Args:
            seconds: double

        """
        try:
            self.phone_obj.sleep(seconds)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def make_delay(self, sec):
        """This method ...

        Args:
            2.0: double

        """
        try:
            sleep(sec)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def deactivate_follow_me(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.deactivate_follow_me()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def activate_direct_diversion(self, extension_number):
        """ This method ...
        
        Args:
            extension_number: string

        """
        try:
            self.phone_obj.activate_direct_diversion(extension_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_message_contents(self, contents):
        """This method ...

        Args:

        """
        try:
            return self.phone_obj.verify_display_message_contents(contents)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_in_ring(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_ring()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_notifications_when_call_back_ring(self, extension_to_be_verified):
        """This method ...

        Args:
            extension_to_be_verified: string

        """
        try:
            self.phone_obj.verify_notifications_when_call_back_ring(extension_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_ed_ngets_call(self, number_of_responses_to_be_stored):
        """This method ...

        Args:
            number_of_responses_to_be_stored: int

        """
        try:
            self.phone_obj.verify_notifications_when_ed_ngets_call(number_of_responses_to_be_stored)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notification_when_message_waiting(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notification_when_message_waiting()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_in_idle(self):
        """This method ...

        Args:

        """
        try:
            # import rpdb2; rpdb2.start_embedded_debugger('admin1')

            self.phone_obj.verify_notifications_when_in_idle()
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
            # self.phone_obj.verify_notifications_when_in_idle(str_to_bo_verified)
        # except Exception as err:
            # fn = sys._getframe().f_code.co_name
            # raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_busy(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_busy()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_notifications_in_connected(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_connected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_follow_me_activated(self, remote_number):
        """This method ...

        Args:
            remote_number: string

        """
        try:
            self.phone_obj.verify_notifications_when_follow_me_activated(remote_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_activated(self, diversion_category):
        """This method ...

        Args:
            diversion_category: string

        """
        try:
            self.phone_obj.verify_notifications_when_diversion_activated(diversion_category)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_diversion_de_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_diversion_de_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notifications_when_pe_ndeactivated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notifications_when_pe_ndeactivated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_in_clearing(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_in_clearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_idle(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_in_idle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_clearing(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_in_clearing()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_in_connected(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_in_connected()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notificaion_when_out_going(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notificaion_when_out_going()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_led_notificaion_when_in_idle(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_led_notificaion_when_in_idle()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_call_list_profile(self, profile_number):
        """This method ...

        Args:
            profile_number: string

        """
        try:
            self.phone_obj.verify_call_list_profile(profile_number)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_notifications_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_notifications_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_line_notifications_when_do_not_disturb_activated(self):
        """This method ...

        Args:

        """
        try:
            self.phone_obj.verify_line_notifications_when_do_not_disturb_activated()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_display_contents(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            return self.phone_obj.verify_display_contents(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_phone_display(self, string_to_be_verified):
        """This method ...

        Args:
            string_to_be_verified: string

        """
        try:
            return self.phone_obj.verify_in_phone_display(string_to_be_verified)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_phone_display(self, phone_mode = "non idle"):
        """returns everything on the phone display...

        Args:
            phone_mode : idle if phone is not in use
                       : non idle if the phone is in use i.e. in a call or any key pressed
        """
        try:
            return self.phone_obj.get_phone_display(phone_mode)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_vm_count(self):
        """returns everything on the phone display...

        Args:
            phone_mode : idle if phone is not in use
                       : non idle if the phone is in use i.e. in a call or any key pressed
        """
        try:
            return self.phone_obj.get_vm_count()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def verify_phone_extn(self, extn):
        """returns everything on the phone display...

        Args:
            phone_mode : idle if phone is not in use
                       : non idle if the phone is in use i.e. in a call or any key pressed
        """
        try:
            return self.phone_obj.verify_phone_extn(extn)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


    def get_extn_number(self):
        """returns everything on the phone display...

        Args:
            phone_mode : idle if phone is not in use
                       : non idle if the phone is in use i.e. in a call or any key pressed
        """
        try:
            return self.phone_obj.get_extn_number()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def verify_count(self, num1, num2, count):
        if (int(num2)-int(num1)) == int(count):
            logger.info("Count is Verified")
        else:
            raise Exception("Count is NOT Changed")
            return 0
        return 1

    def reboot_terminal(self, wait_till_online=True, timeout=300):
        '''
        wait_till_online : if true, this function will wait till the phone comes back online
        timeout : this time will be added to an inbuilt wait of 20 seconds
        reboot the phone
        :return: None
        '''
        try:
            self.phone_obj.reboot_terminal()
            if wait_till_online:
                self.phone_obj.WaitTillPhoneComesOnline(timeout)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_firmware_version(self):
        '''
        Firmware version of the phone
        :return: Firmware version of the phone
        '''
        try:
            return self.phone_obj.get_firmware_version()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_library_version(self):
        '''
        Library version of ATAP
        :return: Library version of ATAP
        '''
        try:
            return self.phone_obj.get_library_version()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def clear_sip_traces(self):
        '''
        Clears the sip traces on the phone
        :return: None
        '''
        try:
            return self.phone_obj.clear_sip_traces()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_in_messages(self):
        '''
        sip messages received by the phone
        :return: SIP IN messages from the phone
        '''
        try:
            return self.phone_obj.get_sip_in_messages()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))

    def get_sip_out_messages(self):
        '''
        sip messages sent by the phone
        :return: SIP OUT messages from the phone
        '''
        try:
            return self.phone_obj.get_sip_out_messages()
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))



    def verify_sip_private_trunk_reroutingto_in_attend_when_not_responding(self, phone2):
        """This method ...

        Args:
            phone2: string

        """
        try:
            self.phone_obj.verify_sip_private_trunk_reroutingto_in_attend_when_not_responding(phone2)
        except Exception as err:
            fn = sys._getframe().f_code.co_name
            raise Exception('func "%s" - err: "%s"!' % (fn, err))


        
if __name__ == "__main__":
    import logging
    import robot.utils.dotdict
    logger = logging.getLogger("RobotFramework")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    # phone_2 = PhoneInterface({"phoneModel":"Mitel6930", "ipAddress":"10.198.34.75", "extensionNumber":"4098", "phoneName":"yo1"})
    #phone_1 = PhoneInterface({"phoneModel": "phone_4xx", "ip": "10.198.32.241", "extension":"8009", "phoneName":"Auto user17", "hq_rsa":"hq_rsa"})
    #phone_1 = PhoneInterface({"phoneModel": "Mitel6920", "ipAddress": "10.198.33.9", "extensionNumber":"8008", "phoneName":"yo2"})
    phone_1 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.198.33.3", "extensionNumber": "8007", "phoneName": "yo2"})
    phone_2 = PhoneInterface({"phoneModel": "Mitel6940", "ipAddress": "10.198.33.117", "extensionNumber": "8017", "phoneName": "yo2"})
    # phone_1.press_vm_soft_key()
    # phone_2.press_vm_soft_key()
    #print phone_1.get_phone_display()
    # phone_2.press_key("VoiceMail")
    # time.sleep(2)
    # phone_2.dial_number("16079")
    # time.sleep(2)
    # phone_2.press_key("BottomKey1")
    # time.sleep(5)
    # phone_2.press_key("BottomKey6")
    # time.sleep(2)
    #print phone_2.verify_led_state('63', '1', 10)
    #phone_2.press_hard_key()
    #phone_1.press_vm_hard_key()
    #phone_2.press_vm_hard_key()
    # phone_1.press_phys_button('VM')
    # phone_2.press_key("VoiceMail")
    # time.sleep(2)
    # phone_3.press_key("VoiceMail")
    # time.sleep(2)
    # phone_4.press_key("VoiceMail")
    # time.sleep(2)
    #extn = phone_2.get_extn_number()
    #print (extn)
    #phone_1.make_call(phone_2.phone_obj.phone.extensionNumber)
    #print (phone_1.extension)
    # phone_1.input_a_number(phone_2.phone_obj.phone.extensionNumber)
    # time.sleep(1)
    # phone_1.press_key('BottomKey1')
    # time.sleep(2)
    # phone_3.input_a_number(phone_4.phone_obj.phone.extensionNumber)
    #time.sleep(1)
    #phone_3.press_key('BottomKey1')
    #time.sleep(5)
    #phone_1.verify_notifications_in_ring()
    #phone_1.phone_obj.answer_the_call()
    #phone_1.phone_obj.verify_in_phone_display(phone_3.phone_obj.phone.extensionNumber)
    #phone_1.phone_obj.disconnect_the_call()
    #phone_1.input_a_number(phone_2.phone_obj.phone.extensionNumber)
    #print phone_1['extension']
    # phone_1 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.211.41.206", "extensionNumber":"303", "phoneName":"yo1","hq_rsa":"hq_rsa"})
    # phone_2 = PhoneInterface({"phoneModel": "Mitel6930", "ipAddress": "10.211.41.223", "extensionNumber":"306", "phoneName":"yo3"})
    #phone_1.print_total_phones()
    # press special key
    # phone_1.dial_service_code("*") # input and dial
    #phone_1.input_a_number("4461")  # only input
    # LED and LINE state
    phone_1.call_extension(phone_2.phone_obj.phone)
    time.sleep(5)
    phone_2.answer_the_call()
    time.sleep(5)
    phone_2.press_key("Hold")
    time.sleep(2)
    print phone_2.get_led_buffer()
    phone_2.press_key("Hold")
    time.sleep(2)
    # #print phone_1.get_led_buffer()
    #print phone_2.get_led_buffer()
    # checking message waiting('57') for blinking('15')
    #print phone_1.verify_led_state('39', 'F', 10)
    #print phone_1.verify_led_state('Line1', 'on', 10)
    #print phone_1.verify_led_state('Mute', 'blink', 10)
    #print phone_2.verify_led_state('Line1', 'off', 10)
    # print phone_1.verify_led_state('Line2', 'off', 10)
    #print phone_2.verify_led_state('Line3', 'off', 10)
    # print phone_1.verify_led_state('1D', '1', 10)
    # phone_1.set_to_idle()
    # phone_1.verify_line_notificaion_when_in_idle()
    # print phone_1.verify_led_state('Function1', 'off', 10)
    # print phone_1.verify_line_state(8)
    # print phone_1.verify_line_state("incoming")
    # print phone_1.get_led_buffer()

    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(5)
    # phone_2.answer_the_call()
    # time.sleep(6)
    # print phone_1.get_line_buffer()
    # print phone_2.get_line_buffer()
    # print phone_1.verify_line_state(4)
    # print phone_1.verify_line_state(5)
    # print phone_2.verify_line_state("incoming")
    # print phone_2.verify_line_state("incoming","2")
    # pass

    # making and answering a call
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # phone_2.verify_notifications_in_ring()
    # phone_2.answer_the_call()
    # phone_2.press_offhook()
    # phone_2.verify_phone_display(phone_1.phone_obj.phone.extensionNumber)
    # time.sleep(5)
    # phone_2.disconnect_the_call()

    # press programmable key
    #phone_2.press_key("ProgramKey12")
    # phone_2.press_expansion_box_key("ProgramKey1")

    # get display output
    # when in connected
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(5)
    # phone_2.answer_the_call()
    # time.sleep(2)
    #phone_1.press_key("Directory")
    #phone_2.press_key("Directory")
    #phone_3.press_key("Directory")
    # phone_1.press_key("VoiceMail")
    # time.sleep(2)
    # phone_2.press_key("VoiceMail")
    # time.sleep(2)
    # phone_3.press_key("VoiceMail")
    # time.sleep(2)
    # phone_1.dial_number("123456")
    # time.sleep(2)
    # phone_1.press_key("BottomKey1")
    # time.sleep(5)
    # phone_1.press_key("ScrollRight")
    # time.sleep(2)
    # phone_1.press_key("BottomKey1")
    # time.sleep(2)
    # print phone_1.get_phone_display()
    # print phone_2.verify_display_message_contents("Today")
    #print phone_1.verify_phone_display("Auto-Attendant")

    # when in idle
    # print phone_1.get_phone_display("idle")
    # print phone_2.get_phone_display("idle")

    # audio path verification
    # phone_1.update_devnull_permissions()
    # phone_2.update_devnull_permissions()
    # phone_1.upload_path_confirmation_files()
    # phone_2.upload_path_confirmation_files()
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(3)
    # phone_2.answer_the_call()
    # phone_2.press_offhook()
    # phone_1.press_offhook()
    # phone_1.press_handsfree()
    # phone_2.press_handsfree()
    # time.sleep(5)
    # phone_1.check_two_way_audio(phone_2)

    # sip messages
    # phone_1.clear_sip_traces()
    # phone_2.clear_sip_traces()
    # phone_1.call_extension(phone_2.phone_obj.phone)
    # time.sleep(5)
    # phone_2.answer_the_call()
    # time.sleep(2)
    # print phone_1.get_sip_in_messages()
    # print phone_1.get_sip_out_messages()
    # print phone_2.get_sip_in_messages()
    # print phone_2.get_sip_out_messages()

    # reboot the phone
    # print phone_1.get_firmware_version()
    # print phone_1.get_library_version()
    # phone_1.reboot_terminal()
