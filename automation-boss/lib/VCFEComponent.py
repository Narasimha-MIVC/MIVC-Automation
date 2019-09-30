"""Module for VCFE functionalities in BOSS Portal
   Author: Vasuja K
"""

class VCFEComponent(object):
    ''' BOSS Component Interface to interact with the ROBOT keywords
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def create_emergency_hunt_group(self, **params):
        '''
        `Description:` This function will create emergency hunt group

        `Param:` params: Dictionary contains  emergency hunt group Info

        `Returns:` emergency hunt group extension

        `Created by:` Vasuja
        '''
        try:

            extn, location = self.boss_page.VCFE_Handler.create_emergency_hunt_group(params)
            return extn, location
        except:
            print("Please check that the input parameters have been provided",
                    self.Create_Emergency_Hunt_group.__doc__)
            raise AssertionError("Creation of Emergency hunt group Failed!!")

    def add_geo_location(self, **params):
        '''
        `Description:` This function will add Geographic location

        `Param:` params: Dictionary with Geolocationinfo

        `Returns:` status - True/False

        `Created by:` Vasuja
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.VCFE_Handler.add_geo_location(params)
            else:
                print("Please check that the input parameters have been provided",
                      self.add_geo_location.__doc__)
                status = False
        except:
            raise AssertionError("Add location Failed!!")
        return status

    def add_geo_loc_using_personal_reg(self, user_nm,**params):
        """
            `Description:` add loc via personal reg

            `:param1:` Location name

            `:return:` status - True/False

            `Created by:` Priyanka M
        """
        try:
            status = self.boss_page.VCFE_Handler.add_geo_loc_using_personal_reg(user_nm,params)
            return status
        except Exception, e:
            print e
            raise AssertionError("Closing Location Failed!!")

    def create_extension_list(self, **params):
        '''
        `Description:` Create extension list by giving extension list name and extension Number

        'param:' params: Dictionary with ExtensionListInfo

        `Returns:` None

        `Created by:` Vasuja

        `Modified by :` Immani Mahesh, Saurabh Singh
        '''
        try:

            self.boss_page.VCFE_Handler.create_extension_list(params)
        except:
            print("Please check that the input parameters have been provided",
                  self.create_extension_list.__doc__)
            raise AssertionError("Extension list creation Failed!!")

    def create_hunt_group(self, **params):
        '''
        `Description:` Create hunt group with different input parameters

        `Param:` params: Dictionary with Hunt_Group_Info

        `Returns:` Hunt Group Extension Number

        `Created by:` Vasuja
        '''
        try:
            extn = self.boss_page.VCFE_Handler.create_hunt_group(params)
            return extn
        except:
            print("Please check that the input parameters have been provided",
                  self.create_hunt_group.__doc__)
            raise AssertionError("Create hunt group Failed!!")

    def verify_hunt_group(self, **params):
        '''
        `Description:` To verify the presence of created hunt group in VCFE component list by searching extension

        `Param1:' Hunt Group Extension number

        `Returns:` status - True/False

        `Created by:` Vasuja K
        '''
        try:
            status = self.boss_page.VCFE_Handler.verify_hunt_group(params)
            return status
        except:
            print("Please check that the input parameters have been provided",
                  self.verify_hunt_group.__doc__)
            raise AssertionError("Verify hunt group Failed!!")

    def select_vcfe_component_by_extension(self, **params):
        """
        `Description:` Select a particular VCFE component after filtering by extension in VCFE page

        `Param1:' Any VCFE component Extension number - vcfe_comp

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = self.boss_page.VCFE_Handler.select_vcfe_component_by_extension(params)
            return status
        except:
            raise AssertionError("Could not select vcfe component!!")

    def select_vcfe_component_by_name(self, **params):
        """
        `Description:` Select a particular VCFE component after filtering by name in VCFE page

        `Param1:' Any VCFE component Name - vcfe_comp

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = self.boss_page.VCFE_Handler.select_vcfe_component_by_name(params)
            return status
        except:
            raise AssertionError("Could not select vcfe component!!")

    def edit_hunt_group(self, **params):
        """
        `Description:` Edit hunt group with different inputs

        `Param:`  params: Dictionary with Vcfe_variables

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.boss_page.VCFE_Handler.edit_hunt_group(params)

        except:
            print("Please check that the input parameters have been provided",
                  self.edit_hunt_group.__doc__)
            raise AssertionError("Edit hunt group is  Failed!!")

    def verify_updated_hunt_group_value(self, **params):
        """
        `Description:` Verify the given hunt group details

        `Param:`  params: Dictionary with Vcfe_variables

        `Returns:` status: True/False

        `Created by:` Vasuja K
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_updated_hunt_group_value(params)
            return status

        except:
            print("Please check that the input parameters have been provided",
                  self.verify_updated_hunt_group_value.__doc__)
            raise AssertionError("Verify updated hunt group value is Failed!!")

    def delete_vcfe_entry(self, ext):
        """
        `Description:` To delete vcfe entries

        `Param:`  params: Dictionary contains all VCFE component info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.VCFE_Handler.delete_vcfe_entry(ext)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def create_pickup_group(self, **params):
        '''
        `Description:` This function will create pickup group

        `Param:` params: Dictionary contains PickupGroupInfo

        `Returns:` Pickup Group Extension number

        `Created by:` Vasuja

        `Modified by :` Saurabh Singh
        '''
        try:

            extn = self.boss_page.VCFE_Handler.create_pickup_group(params)
            return extn
        except:
            print("Please check that the input parameters have been provided",
                  self.create_pickup_group.__doc__)
            raise AssertionError("Pickup group creation Failed!!")

    def add_auto_attendant(self, **params):
        """
        `Description:` This function will create Auto Attendant

        `Param:` params: Dictionary contains AutoAttendantInfo

        `Returns:` Auto Attendant Extension number

        `Created by:` rdoshi

        `Modified by :` Immani Mahesh
        """
        try:
            if params.keys():
                # import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                extn = self.boss_page.VCFE_Handler.add_Auto_Attendant(params)
                return extn
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Add Auto Attendant Failed!!")

    def create_custom_schedule(self, **params):
        '''
        `Description:` This function will create custom schedule

        `Param:` params: Dictionary contains CustomScheduleInfo

        `Returns:` status - True/False

        `Created by:` Vasuja K

        `Modified by :` Immani Mahesh, Saurabh Singh
        '''
        try:

            status = self.boss_page.VCFE_Handler.create_custom_schedule(params)
        except:
            print("Please check that the input parameters have been provided",
                  self.create_custom_schedule.__doc__)
            raise AssertionError("Create custom schedule Failed!!")
        return status

    def add_paging_group(self, **params):
        """
        `Description:` This function will create Paging Group

        `Param:` params: Dictionary contains PageGroupInfo

        `Returns:` Extension Number

        `Created by:` rdoshi

        `Modified by :` Immani Mahesh Kumar , Saurabh Singh
        """
        try:
            if params.keys():
                extn = self.boss_page.VCFE_Handler.add_Paging_Group(params)
                return extn
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Add paging group Failed!!")

    def delete_vcfe_components(self, **VCFE_entry):
        """
        `Description:` Delete VCFE component

        `:param:` params: VCFE_entry:Dictionary of VCFE entries information

        `:return:` None

        `Created by`  Saurabh Singh
        """
        try:
            self.boss_page.VCFE_Handler.delete_vcfe_entries(VCFE_entry)
        except:
            raise AssertionError("Deletion of VCFE Failed!!")

    def verify_vcfe_components_delete(self, **VCFE_entry):
        """
        `Description:` Verify the VCFE component is deleted

        `:param:` VCFE_entry: Dictionary of VCFE entry  information

        `:return:` status

        `Created by:` rdoshi
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_vcfe_entries_deleted(VCFE_entry)
            return status
        except:
            raise AssertionError("Add paging group Failed!!")

    def verify_pickup_group(self, ext):
        """
        `Description:` This function will verify pickup group by searching extension

        `Param1:` pickup group extension number - ext

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_pickup_group(ext)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_edited_pickup_group(self, **params):
        """
        `Description:` This function will verify the given pickup group details

        `Param:`  params: Dictionary contains pickup group details - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_edited_pickup_group(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_pickup_group(self, **params):
        """
        `Description:` This function will edit pickup group details

        `Param:`  params: Dictionary contains pickup group details - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh

        `Modified by :` Vasuja K
        """
        try:

            status = self.boss_page.VCFE_Handler.edit_pickup_group(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def delete_vcfe_entry(self, ext):
        """
        `Description:` To delete vcfe entries

        `Param:`  params: Dictionary contains all VCFE component info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.VCFE_Handler.delete_vcfe_entry(ext)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_paging_group(self, **params):
        """
            `Description:` Editing the selected paging group

            `:param params: Dictionary contains	info about fields that has to be edited like Name, Location, Sync delay...

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
         """
        try:
            params['vcfe_comp'] = params['Pg_Extension']
            status = self.boss_page.VCFE_Handler.select_vcfe_component_by_extension(params)
            status = self.boss_page.VCFE_Handler.edit_paging_group(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def vcfe_invalid_extention(self, **params):
        """
        `Description:` To check invalid extention for vcfe

        `Param:`  params: Dictionary contains all VCFE component info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:

            status = self.boss_page.VCFE_Handler.vcfe_invalid_extention(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def vcfe_jump_extention_list(self, **params):
        """
        `Description:` To select different extention list

        `Param:` params: Dictionary with ExtensionListInfo

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.VCFE_Handler.vcfe_jump_extention_list(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_custome_schedule(self, **params):
        """
        `Description:` API helps to edit custom schedule like Name,timezone,start time,Stop time,custom date etc...

        `Param:` Params contains info for the custom schedule to be edited.

        `Returns:` status - True/False

        `Created by:` Immani Mahesh Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.edit_custome_schedule(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def delete_vcfe_day_name(self, **params):
        """
        `Description:` This will delete vcfe componenet by day name

        `Param:` params: Dictionary contains vcfe component info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.VCFE_Handler.delete_vcfe_day_name(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_extension_list(self, **params):
        """
        `Description:` API helps to edit extension list like Name,Adding and deleting a member and also
         validating error messages for negative testcases

        `Param:` Params contains info for the extension list to be edited.

        `Returns:` status - True/False

        `Created by:` Immani Mahesh Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.edit_extension_list(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_auto_attendant(self, **params):
        """
        `Description:` Edit Auto Attendant like name, location, Multiple digit Time out etc...

        `:param params: Dictionary contains Auto Attendant info like name, location, Multiple digit Time out etc...

        `return:` Status- True or False

         `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = self.boss_page.VCFE_Handler.edit_auto_attendant(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def delete_vcfe_by_name(self, params):
        """
            `Description:` This Method helps to delete a vcfe component by name Such as Schedules which do not have
                            Extensions

            `:param vcfe_name: Name of the VCFE component to be deleted

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.delete_vcfe_by_name(params)
            return status
        except:
            raise AssertionError("Error occured, vcfe component could not delete!!")

    def create_on_hours_schedule(self, **params):
        """
            `Description:` Create On Hours  schedule

            `:param params: Dictionary contains	On-Hours Schedule info like Schedule Name and TIme zone

            `return:` Schedule name

             `created by:` Immani Mahesh Kumar
        """
        try:
            name = self.boss_page.VCFE_Handler.create_on_hours_schedule(params)
            return name
        except:
            print("Could not create holiday schedule", self.create_on_hours_schedule.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def create_holiday_schedule(self, **params):
        """
        `Description:` Create holiday schedule and return name and date of the holiday schedule

        `Param:`  params: Dictionary contains HolidayScheduleInfo - Vcfe_variables

        `Returns:` name and date of the holiday schedule

        `Created by:` Vasuja K
        """
        try:
            name, date = self.boss_page.VCFE_Handler.create_holiday_schedule(params)
            return name, date
        except:
            print("Could not create holiday schedule", self.create_holiday_schedule.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_holiday_schedule(self, **params):
        """
        `Description:` Edit holiday schedule details

        `Param:`  params: Dictionary contains HolidayScheduleInfo - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = self.boss_page.VCFE_Handler.edit_holiday_schedule(params)
            return status
        except:
            print("Could not edit holiday schedule", self.edit_holiday_schedule.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_holidays_schedule(self, **params):
        """
        `Description:` Verify holiday schedule details

        `Param:`  params: Dictionary contains HolidayScheduleInfo - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_holidays_schedule(params)
            return status
        except:
            print("Could not verify holiday schedule", self.verify_holidays_schedule.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def delete_vcfe_by_name(self, params):
        """
       `Description:` This Method helps to delete a vcfe component by name Such as Schedules which do not have
                       Extensions

       `:param vcfe_name: Name of the VCFE component to be deleted

       `return:` Status- True or False

        `created by:` Immani Mahesh Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.delete_vcfe_by_name(params)
            return status
        except:
            raise AssertionError("Error occured, vcfe component could not delete!!")

    def edit_on_hours_schedule(self, **params):
        """
            `Description:` Edit On Hours  schedule

            `:param params: Dictionary contains	Info for Editing On Hours Schedule like schedule name and timezone

            `return:` Status- True or False

             `created by:` Immani Mahesh Kumar
        """
        try:
            # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status = self.boss_page.VCFE_Handler.edit_on_hours_schedule(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def edit_emergency_hunt_group(self, **params):
        """
        `Description:` Edit emergency hunt group with different inputs

        `Param:`  params: Dictionary contains emergency hunt group info - Vcfe_variables

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.boss_page.VCFE_Handler.edit_emergency_hunt_group(params)

        except:
            print("Please check that the input parameters have been provided",
                    self.edit_emergency_hunt_group.__doc__)
            raise AssertionError("Edit hunt group is  Failed!!")

    def verify_emergency_hunt_group(self, **params):
        """
        `Description:` Verify all given emergency hunt group fields

        `Param:`  params: Dictionary contains emergency hunt group info - Vcfe_variables

        `Returns:` status - True/False

        `Created by:` Vasuja K
        """
        try:
            status=self.boss_page.VCFE_Handler.verify_emergency_hunt_group(params)
            return status

        except:
            print("Please check that the input parameters have been provided",
                    self.verify_emergency_hunt_group.__doc__)
            raise AssertionError("Verify updated hunt group value is Failed!!")

    def create_on_hours_schedule(self, **params):
        """
        This Method will add On Hours Schedule Taking parameters and will
        return the name of the schedule
        :param params:
        :return: Name of the Schedule
        """
        try:
            name= self.boss_page.VCFE_Handler.create_on_hours_schedule(params)
            return name
        except:
            print("Could not create holiday schedule", self.create_on_hours_schedule.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def assign_ph_number_to_vcfe_component(self, **params):
        """
        `Description:` Assign any available phone number to any vcfe component on 'Phone System--> Phone Numbers' page

        `Param:` Type of destination. Eg; Auto Attendant, Hunt Group

        `Returns:` status - True / False

        `Created by:` Vasuja
        """
        # Assumption is that the control is already in Phone System--> Phone Numbers page
        try:
            status = self.boss_page.VCFE_Handler.assign_ph_number_to_vcfe_component(params)
            return status
        except:
            print("Could not assign phone number to vcfe component", self.assign_ph_number_to_vcfe_component.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def go_to_vcfe_page(self, params):
        """
            `Description:` This function will help to go and land in a given vcfe page

            `Param:`  params: page name

            `Created by:` Immani Mahesh kumar
        """
        try:
            self.boss_page.VCFE_Handler.go_to_vcfe_page(params)

        except:
            print("switching to vcfe page has failed", self.go_to_vcfe_page.__doc__)

    def validate_vcfe_component_fields(self, **params):
        """
        `Description:` This function will validate vcfe component fields.

        `Param:` Dictionary contains field values to be validated.

        `Returns:` status - True / False

        `Created by:` Palla Surya Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.validate_vcfe_component_fields(params)
        except:
            raise AssertionError("Validation of vcfe component fields failed!!")
        return status

    def search_vcfe_component_by_extension(self,**params):
        """
        `Description:` This function will search vcfe component by extension.

        `Param:` Dictionary contains values to be searched.

        `Returns:` status - True / False

        `Created by:` Palla Surya Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.search_vcfe_component_by_extension(params)
        except:
            raise AssertionError("Searching of vcfe component failed!!")
        return status

    def search_vcfe_component_by_name(self,**params):
        """
        `Description:` This function will search vcfe component by name.

        `Param:` Dictionary contains values to be searched.

        `Returns:` status - True / False

        `Created by:` Palla Surya Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.search_vcfe_component_by_name(params)
        except:
            raise AssertionError("Searching of vcfe component failed!!")
        return status

    def search_vcfe_component_by_type(self,**params):
        """
        `Description:` This function will search vcfe component by type.

        `Param:` Dictionary contains values to be searched.

        `Returns:` status - True / False

        `Created by:` Palla Surya Kumar
        """
        try:
            status = self.boss_page.VCFE_Handler.search_vcfe_component_by_type(params)
        except:
            raise AssertionError("Searching of vcfe component failed!!")
        return status

    def verify_allignment(self,field_name):
        """
            `Description:` This function will verify Language/Setting field allignment

             `Param:`  None

             `Created by:` Priyanka M
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_allignment(field_name)
        except:
            raise AssertionError("Verifying Allignment Failed for "+ field_name+"!!")
        return status

    def verify_component_sort_order_on_vcfe_grid(self, **params):
        """
        `Description:`This helps to validate the sort operation on extension column in VCFE page

        `Param:`  None

        `Returns:` status - True/False

        `Created by:` Vasuja
        """
        try:
            status = self.boss_page.VCFE_Handler.verify_component_sort_order_on_vcfe_grid(params)
            return status
        except:
            print("Verifying the sort order is failed", self.verify_component_sort_order_on_vcfe_grid.__doc__)


    def vcfe_default_AA(self, params):
        try:
            status = self.boss_page.VCFE_Handler.vcfe_default_AA(params)
            #import sys
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            return status
        except:
            print("Could not assign phone number to vcfe component", self.vcfe_default_AA.__doc__)
            raise AssertionError("Error Found on page, Test Case Failed!!")
