"""
Module to interact with Mitel phones. This is a base class which will be inherited in other phone model specific
classes.
"""
__author__ = "milton.villeda@mitel.com"

import sys
from robot.api import logger

from mitel_phone_base import Phone6xxxInterface
from . import phone_button_map

class Phone_69xx(Phone6xxxInterface):
    """ 69xx Phone Interface
    """
    def __init__(self, phone_info, **kwargs):
        """
        It is mandatory to call phone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """
        logger.info("Initializing Mitel 69xx Phone class")
        self.phone_type = phone_info['phoneModel']

        if "Mitel6940" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6940_button_map
        elif "Mitel6930" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6930_button_map
        elif "Mitel6920" in self.phone_type:
            phone_info['button_map'] = phone_button_map.phone_6920_button_map

        Phone6xxxInterface.__init__(self, phone_info)

    def log_off(self):
        raise NotImplementedError("Implement this function")