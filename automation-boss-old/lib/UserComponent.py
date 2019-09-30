"""Module for Users page
   Developer: Megha Bansal
"""


class UserComponent(object):
    ''' Module for users page
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def verify_globaluser_location(self, **params):
        '''
        `Description:` This Function will verify the location of global user
        `Param:` Dictionary contains global user information (Name of the user and its country)
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.personal_information.verify_globaluser_location(params)
            return result
        except:
            print("Could not access link", self.verify_globaluser_location.__doc__)
            raise AssertionError("Verify location for GlobalUser failed!!")


    def get_locations_user_location_dropdown(self):
        '''
        `Description:` This Function will get the locations from User Location dropdown while adding a global user
        `Param:` None
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            locList = self.boss_page.user_handler.get_locations_user_location_dropdown()
            return locList
        except:
            print("Could not access link", self.get_locations_user_location_dropdown.__doc__)
            raise AssertionError("Verify user location dropdown failed!!")


    def verify_GU_products_swap(self, **params):
        '''
        `Description:` This Function will verify Global Users products for swap
        `Param:` UserName
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.user_handler.verify_GU_products_swap(params)
            return result
        except:
            print("Could not access link", self.verify_GU_products_swap.__doc__)
            raise AssertionError("Verify GU Products failed!!")

    def swap_global_user(self, **params):
        '''
        `Description:` This Function will swap Global Users
        `Param:` UserName
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.user_handler.swap_global_user(params)
            return result
        except:
            print("Could not access link", self.swap_global_user.__doc__)
            raise AssertionError("Swap Global User failed!!")

