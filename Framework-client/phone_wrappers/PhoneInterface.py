"""
Interface to mitel and/or shoretel pphones
"""
__author__ = "nitin.kumar-2@mitel.com"

import sys
from phone_4xx import PPhoneInterface
from phone_69xx.ip_phone import IP_Phone

class PhoneInterface(PPhoneInterface):


    def __init__(self, **args):
        """
        It is mandatory to call pphone_sanity_check immediately to create the phone objects for mitel phones
        :param args:
        """

        self.phone_type = None
        if args['phone_type'].lower() == "shoretel".lower():
            self.phone_type = 'shoretel'
            PPhoneInterface.__init__(self)
        elif args['phone_type'].lower() == "mitel".lower():
            self.phone_type = 'mitel'
            self.obj = IP_Phone()

    def pphone_sanity_check(self,*args):
        if self.phone_type == "shoretel":
            PPhoneInterface.pphone_sanity_check(self, *args)
            pass
        elif self.phone_type == "mitel":
            self.phones = [self.obj.get_object(phone_info[0],phone_info[1:]) for phone_info in (args)]
            self.phones[0].connectToPhone()
            self.phones[1].connectToPhone()
            # self.phones[2].connectToPhone()
            return self.phones

    def pphone_make_call(self, *args):
        print(args)
        if self.phone_type == "shoretel":
            PPhoneInterface.pphone_make_call(self, *args)
        elif self.phone_type == "mitel":
            args[0].callToAnExtension(args[1])
            # self.phones[0].pressOffhook()



if __name__ == "__main__":
    import robot.utils.dotdict
    # phone_type = 'mitel'
    phone_type = 'shoretel'
    Phone01_m = ['Mitel6920',"Mitel6920", False, "28", "123", "Test Extension", "10.198.33.98", "", "", "", "", "", "", "10.211.41.40"]
    Phone02_m = ['Mitel6920', "Mitel6920", False, "29", "123", "Test Extension", "10.198.34.66", "", "", "", "", "", "","10.211.41.40"]
    Phone03_m = ['Mitel6920', "Mitel6920", False, "3802", "123", "Test Extension", "10.198.33.255", "", "", "", "", "", "","10.211.41.40"]
    Phone01_s = robot.utils.dotdict.DotDict(ip= "10.198.18.108", extension= "1007", phone_type= "p8cg", PPhone_mac= "001049454A97")
    Phone02_s = robot.utils.dotdict.DotDict(ip= "10.198.18.189", extension= "1008", phone_type= "p8cg", PPhone_mac= "001049454AF9")
    Phone03_s = robot.utils.dotdict.DotDict(ip= "10.198.33.255" , extension= "1009", phone_type= "p8cg", PPhone_mac= "001049454A71")
    if phone_type == 'shoretel':
        Phone01, Phone02, Phone03 = Phone01_s, Phone02_s, Phone03_s
        o = PhoneInterface(phone_type=phone_type)
        o.pphone_sanity_check(Phone01, Phone02, Phone03)
    else:
        Phone01, Phone02, Phone03 = Phone01_m, Phone02_m, Phone03_m
        o = PhoneInterface(phone_type=phone_type)
        Phone01, Phone02, Phone03 = o.pphone_sanity_check(Phone01, Phone02, Phone03)

    o.pphone_make_call(Phone01,Phone02,'right_line1')

