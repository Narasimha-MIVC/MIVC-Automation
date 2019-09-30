"""Module for Service page
   Developer: Megha Bansal
"""


class ServiceComponent(object):
    ''' Module for Service page
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def close_service(self, **params):
        '''
        `Description:` This Function will close the service
        `Param:` Dictionary contains service information
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.service.close_service(params)
            return result
        except:
            print("Could not access link", self.close_service.__doc__)
            raise AssertionError("Close Service failed!!")


    def void_global_user_service(self, **params):
        '''
        `Description:` This Function will void the global user service
        `Param:` Dictionary contains service information
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            serviceTn, result = self.boss_page.service.void_global_user_service(params)
            return serviceTn, result
        except:
            print("Could not access link", self.void_global_user_service.__doc__)
            raise AssertionError("Void Global user Service failed!!")

    def update_service_status(self, **params):
        '''
        `Description:` To update the service status.
        `Param:` Dictionary contains service information
        `Returns:` result - True/False
        `Created by:` Vasuja
        '''
        try:
            result = self.boss_page.service.update_service_status(params)
            return result
        except:
            print("Could not update service status", self.update_service_status.__doc__)
            raise AssertionError("Failed to update Service status!!")

    def retrieve_service_id(self, **params):
        """
        `Description:` This function retrieves the service id from service page
        `:param1` Dictionary contains service information
        `:return:` serviceId
        `Created by:` Vasuja
        """
        serviceId = None

        try:
            serviceId= self.boss_page.service.retrieve_service_id(params)
        except Exception, e:
            print(e.message)
        return serviceId

    def verify_service_status(self, **params):
        '''
        `Description:` To Verify service status in service page.
        `Param:` Dictionary contains service information (Service id and status)
        `Returns:` result - True/False
        `Created by:` Vasuja
        '''
        try:
            result = self.boss_page.service.verify_service_status(params)
            return result
        except:
            print("Could not verify service status", self.verify_service_status.__doc__)
            raise AssertionError("Failed to verify TN service status!!")
