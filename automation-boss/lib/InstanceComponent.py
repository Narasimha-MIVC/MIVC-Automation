"""Module for Instances page
   Developer: Rohit Arora
"""


class InstanceComponent(object):
    ''' Module for users page
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def add_global_country_to_smr_instance(self, **params):
        '''
        `Description:` This Function will verify adding a global country's access numbers to an SMR instance
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Rohit Arora
        '''
        try:
            result = self.boss_page.instance.add_global_country_to_smr_instance(params)
            return result
        except:
            print("Add global country to SMR instance failed!!", self.add_global_country_to_smr_instance().__doc__)
            raise AssertionError("Add global country to SMR instance failed!!")


    def update_global_country_of_smr_instance(self, **params):
        '''
        `Description:` This Function will verify updating a global country's access numbers for an already set-up country of an SMR instance
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Rohit Arora
        '''
        try:
            result = self.boss_page.instance.update_global_country_of_smr_instance(params)
            return result
        except:
            print("Update global country of SMR instance failed!!", self.update_global_country_of_smr_instance().__doc__)
            raise AssertionError("Update global country of SMR instance failed!!")


    def verify_existence_show_configured_link(self, **params):
        '''
        `Description:` This Function will verify existence of 'Show Configured' link for an SMR instance where global country(ies) have been set up
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Rohit Arora
        '''
        try:
            result = self.boss_page.instance.verify_existence_show_configured_link(params)
            return result
        except:
            print("Verification of existence of Show Configured link failed!!", self.verify_existence_show_configured_link().__doc__)
            raise AssertionError("Verification of existence of Show Configured link failed!!")