"""
Module for Call Recording
Autor;krishan Gopal
"""
import os
import sys
import time

import stafenv

#from base import LocalBrowser
#import web_wrappers.selenium_wrappers as base
from web_wrappers.selenium_wrappers import LocalBrowser
from page.CallRecordingComponent import CallRecordingPage
from mapMgr import mapMgr


from log import log

print "import done"

_DEFAULT_TIMEOUT = 3

class CallRecordingComponent(object):
    ''' CallRecording Component Interface to interact with the ROBOT keywords
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, **params):
        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        self.browsertype = params.get('browser', 'chrome').lower()
        self._browser = LocalBrowser(self.browsertype)
        mapMgr.create_maplist("PbxComponent")
        self.mapDict = mapMgr.getMapDict()
        self.callrecording = CallRecordingPage(self._browser)

    def open_url(self,url):
        """
        This function is used to open BOSS portal page
        :param url: URL of boss page
        :return:
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.callrecording.common_func.open_url(url)
        except Exception,e:
            print(e)
            raise e

    def client_login(self, **params):
        """Login to the BOSS portal using the username and password

        :param params: URL, username, password
        :return:
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.callrecording.common_func.client_login(params["username"],params["password"])
            print("DEBUG: Login successful")
        except:
            raise AssertionError("Login Failed!!")

    def client_login_BOSS(self, **params):
        """Login to the BOSS portal using the username and password

        :param params: URL, username, password
        :return:
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.callrecording.common_func.client_login_BOSS(params["username"],params["password"])
            print("DEBUG: Login successful")
        except:
            raise AssertionError("Login Failed!!")

    def get_time_now(self):
        """
        This function is used to get current time
        :return: current time
        """
        try:
            var=self.callrecording.call_recording.get_time_now()
            return var

        except Exception,e:
            print(e)
            raise e

    def switch_page(self, **params):
        """Switch page using the account link on the top of the page

        :param params:
        :return:
        """
        try:
            print("IN MAIN:")
            if params.keys():
                self.callrecording.common_func.switch_page(page=params['page'])
            else:
                print("Please check that the input parameters have been provided",
                        self.switch_page.__doc__)
        except:
            raise AssertionError("Page Switch Failed!!")


    def close_the_browser(self, **params):
        """
        This function will close the browser
        :param params:
        :return:
        """
        try:
            time.sleep(2)
            self.callrecording.common_func.close_browser()
        except:
            raise AssertionError("Close browser Failed!!")


    def load_recent_calls(self):
        try:
            self.callrecording.call_recording.load_recent_calls()
        except Exception as e:
            raise e

    def select_option_tenant(self,t_name):
        try:
            self.callrecording.call_recording.select_option_tenant(t_name)
        except Exception as e:
            raise e

    def call_recording_validate_data(self,**params):
        try:
            #import  pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.callrecording.call_recording.call_recording_data_validation(**params)
        except Exception as e:
            raise e

    def call_recording_data_validation_custom_search(self, extn,extn2,did,**params):
        try:
            self.callrecording.call_recording.call_recording_data_validation_custom_search(extn,extn2,did, **params)
        except Exception as e:
            raise AssertionError("Custom Search data validation API failed")

    def call_recording_custom_search_extension(self,extNum,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_extension(extNum,**params)

        except Exception as e:
            print e
            raise AssertionError("Call Recording:Custom search Extension is failing")

    def call_recording_custom_search_CLID(self,did,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_CLID(did,**params)

        except:
            raise AssertionError("Call Recording:Custom search CLID is failing")

    def call_recording_custom_search_Dialed_Number(self,extNum,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_Dialed_Number(extNum,**params)

        except Exception as e:
            raise AssertionError("Call Recording:Custom search Dialed Number is failing"  + str(e))

    def call_recording_custom_search_Date(self,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_Date(**params)

        except Exception as e:
            raise AssertionError("Call Recording:Custom search -> date is failing" + str(e))

    def call_recording_custom_search_Recording_Duration(self,extNum,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_Recording_Duration(extNum,**params)

        except Exception as e:
            print e
            raise AssertionError("Call Recording:Custom search Recording Duration is failing")

    def call_recording_custom_search_StartTime_and_EndTime(self,extNum,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_StartTime_and_EndTime(extNum,**params)
        except:
            raise AssertionError("Call Recording:Custom search StartTime and EndTime is failing")

    def call_recording_custom_search_Users(self,firstname,lastname,**params):
        try:
            self.callrecording.call_recording.call_recording_custom_search_Users(firstname,lastname,**params)

        except:
            raise AssertionError("Call Recording:Custom search Users is failing")

    def cr_play_logoff(self):
        try:
            self.callrecording.call_recording.cr_play_logoff()
        except:
            raise AssertionError("Unable to log-off cr_play portal")

    def cr_play_boss_logoff(self):
        try:
            self.callrecording.call_recording.cr_play_boss_logoff()
        except:
            raise AssertionError("Unable to log-off cr_play BOSS portal")
