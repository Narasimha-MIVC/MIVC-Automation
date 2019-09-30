import os
import time
import sys
import re
import autoit
import random
import platform
if re.match(r'^2.7.', sys.version):
    from pathlib2 import Path
else:
    from pathlib import Path

from selenium.webdriver.common.action_chains import ActionChains


client_path = os.path.dirname(os.path.dirname(__file__))
framework_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))))), "Framework-client")
sys.path.append(framework_path)
sys.path.append(os.path.join(framework_path, "log"))
sys.path.append(os.path.join(framework_path, "utils"))
sys.path.append(os.path.join(framework_path, "config"))
sys.path.append(os.path.join(framework_path, "web_wrappers"))
sys.path.append(os.path.join(client_path, "page/ManhattanComponent"))
sys.path.append(os.path.join(client_path, "map/ManhattanComponent"))

from log import log
import selenium_wrappers

from selenium_wrappers import Browser
from selenium_wrappers import WebElementAction
from selenium_wrappers import QueryElement
from selenium_wrappers import AssertElement

from CommonFunctionality import CommonFunctionality
from CreateGroup import CreateGroup
from DefaultPanel import DefaultPanel
from Events import Events
from Messages import Messages
from PeopleGroup import PeopleGroup
from Settings import Settings
from Voicemails import Voicemails
from Recent import Recent
from ThirdPanel import ThirdPanel
from WorkGroup import WorkGroup

from mapMgr import mapMgr
from confMgr import confMgr
import client_utils
from selenium.webdriver.common.keys import Keys
from robot.api.logger import console


class ManhattanComponent():
    # initialize the driver and give the correct application path
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    #ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    def __init__(self, params):
        if params == "parallel":
            pass
        else:
            self.launch_client(params)
        
    def launch_client(self, params):
        self.params = params
        self._browser = Browser(self.params)
        self.webAction = WebElementAction(self._browser)
        self.assertElement = AssertElement(self._browser)
        self.queryElement = QueryElement(self._browser)

        mapMgr.create_maplist(component=self.params["component_type"])
        self.common_func = CommonFunctionality(self._browser)
        self.defaultPanel = DefaultPanel(self._browser)
        self.peopleGroup = PeopleGroup(self._browser)
        self.createGroupclass = CreateGroup(self._browser)
        self.voicemail = Voicemails(self._browser)
        self.event = Events(self._browser)
        self.message = Messages(self._browser)
        self.setting = Settings(self._browser)
        self.recent = Recent(self._browser)
        self.thirdPanel = ThirdPanel(self._browser)
        self.workGroup = WorkGroup(self._browser)

    def client_login(self, **params):
        '''
        client_login():login to the Manhattan Client using username and password
        Parameters: username, Password and server_address
        Ex: client_login username=USER_DB1_02 password=changeme server_address=10.196.4.99
        '''
        try:
            self.common_func.login(params["username"], params["password"], params["server_address"])
            if not self.queryElement.element_not_displayed("default_panel_upgrade_button"):
                self.webAction.execute_javascript("Endo.isShowingMainAppWindow(1)")
            self.webAction.explicit_wait("default_people_tab", 30)
            self.defaultPanel.change_user_status("available")
            log.mjLog.LogReporter("ManhattanComponent", "info", "Client_login"
                                                                " - Login to Manhattan successful")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Client_login"
                                  " - Failed to Login to Manhattan " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error Client_login - Failed to Login to Manhattan")

    def close_application(self):
        """
        Author: UKumar
        close_application(): To logout from connect client and close connect client
        Parameters: no parameter
        Ex: close_application
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            self.logout(**{"windowNumber": "0"})
            time.sleep(1)  # to print the log messages in client log file
            self._browser.quit()
            log.mjLog.LogReporter("ManhattanComponent", "info", "close_application - Connect Client closed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "close_application"
                                                                 " - Unable to close Connect Client" + str(
                sys.exc_info()))
            raise

    def close_browser(self):
        """
        Author: UKumar
        close_browser(): To close browser
        Parameters: no parameter
        Ex: close_browser
        """
        try:
            self._browser.quit()
            log.mjLog.LogReporter("ManhattanComponent", "info", "close_browser - browser closed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "close_browser"
                                                                 " - Unable to close browser " + str(sys.exc_info()))
            return False

    def close_presenter(self):
        """
        Author: Aakash
        close_presenter(): To close shoretel presenter
        Parameters: no parameter
        Ex: close_presenter
        """
        try:            
            os.system('taskkill /f /im ScreenshotCaptureWithMouse.exe')
        except:
            return False    
    
    def check_user_detail_attribute(self, **params):
        '''
           Author: Gautham
           check_user_detail_attribute() - Check if a perticular attribute is available in third panel of user info
           parameters: option: info: to check info button
                               call: to check call button
                               min: to check minimize button
                               timer: to check timer button
                               endCall: to check end call button
                               holdCall: to check hold call button
                               mute: to check mute button
                               video: to check video button
                               share: to check share button
                               conf: to check add conference button
                               transfer: to check transfer button
                               record: to check record button
                               holdIcon: to check On hold icon button when call is on hold
                               unHold: to check if unhold button is visible
                               dropDown: to check the options under drop down filter
                       check: positive: API fails if attribute is not present
                       check: negative: API fails if attribute is present
           ex: check_user_detail_attribute option=info check=positive

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_user_detail_attribute- Checking for the attribute in user info panel ")            
            time.sleep(0.5)
            if params["check"] == "positive":
                self.peopleGroup.check_user_attribute_present(params)
            elif params["check"] == "negative":
                self.peopleGroup.check_user_attribute_not_present(params)
            else:
                raise AssertionError("wrong arguments passed !!")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_user_detail_attribute- Attribute check is successfully completed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_user_detail_attribute- Attribute check failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error check_user_detail_attribute- Attribute check failed")

    def place_end_call(self, **params):
        """
        Author: Gautham
        place_end_call() - To place or end a call through Manhattan Client
        parameters: option: start: to place a call
                               end: to end a call
                               recv: to recieve a call // pos added for answer the 2nd, 3rd call( added by kiran )
                               trans: to transfer a call
                               trans_contact_check : to check transfer call contact options
                               blankTrans: to transfer call without selecting a user
                               conf: to start a conference call
                               hold: to hold a call
                               unHold: to unhold a call
                               endTransfer: to end transferred call
        ex: place_end_call option=start
        ex: place_end_call option=trans user=userC
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "place_end_call - operation to be " + params["option"])
            call_options_without_params = {"start": self.peopleGroup.start_call, "end": self.peopleGroup.end_call,
                                           "end_call_dashboard": self.peopleGroup.end_call_dashboard,
                                           "endCall": self.peopleGroup.end_call_dashboard,
                                           "blankTrans": self.peopleGroup.blank_transfer_call,
                                           "endTransfer": self.peopleGroup.end_transfer_call,
                                           "hold": self.peopleGroup.hold_call,
                                           "unHold": self.peopleGroup.un_hold_call,
                                           "complete_consult": self.peopleGroup.complete_consult,
                                           "cancel_consult": self.peopleGroup.cancel_consult,
                                           "toVoiceMail": self.peopleGroup.to_voice_mail,
                                           "video": self.peopleGroup.video_call,
                                           "cancel_consult_dashboard": self.peopleGroup.cancel_consult_dashboard,
                                           "enter":self.peopleGroup.start_call_by_pressing_enter
                                           }
            call_options_with_params = {"recv": self.peopleGroup.receive_call,
                                        "mute": self.peopleGroup.mute_unmute_call,
                                        "unmute": self.peopleGroup.mute_unmute_call,
                                        "trans": self.peopleGroup.transfer_call,
                                        "did_to_did_trans": self.peopleGroup.did_to_did_transfer,
                                        "trans_contact_check": self.peopleGroup.trans_contact_check,
                                        "conf": self.peopleGroup.conference_call,
                                        "consult_conf": self.peopleGroup.consult_conference_call,
                                        "did_to_did_conf": self.peopleGroup.did_to_did_conference,
                                        "did_to_did_intercom": self.peopleGroup.did_to_did_conference,
                                        "consult": self.peopleGroup.consult_transfer,
                                        "whisper": self.peopleGroup.whisper_transfer,
                                        "intercom_transfer": self.peopleGroup.intercom_transfer,
                                        "intercom_conference": self.peopleGroup.intercom_conference,
                                        "drag_and_move":self.peopleGroup.drag_drop_transfer_call,
                                        }
            if params["option"] in call_options_without_params.keys():
                calling_method = call_options_without_params[params["option"]]
                calling_method()
            elif params["option"] in call_options_with_params.keys():
                calling_method = call_options_with_params[params["option"]]
                calling_method(params)
            else:
                raise AssertionError("wrong arguments passed !!")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "place_end_call - operation %s performed" % params["option"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "place_end_call - Failed to click on call button" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error place_end_call - Failed to click on call button")

    def call_control(self, **params):
        self.place_end_call(**params)

    def check_incoming_call(self):
        '''
           Author: Gautham modified by Uttam
           check_incoming_call() - To check incoming call in manhattan client
           Parameter: No parameter
           Ex: check_incoming_call
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_incoming_call"
                                                                " - Checking incoming call")
            time.sleep(4)  # to wait for answer button, explicit_wait is not working
            self.webAction.explicit_wait("default_recieve_call")
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_incoming_call"
                                                                " - Recieve button is visible")
            self.assertElement.element_should_be_displayed("default_voicemail")
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_incoming_call"
                                                                " - Voice mail button is visible")
            self.assertElement.element_should_be_displayed("default_transfer_call")
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_incoming_call"
                                                                " - call transfer button is visible")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_incoming_call"
                                                                 " - Failed to chack incoming call notification" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error check_incoming_call - Failed to chack incoming call notification")

    def double_click_dashboard_notification(self, **params):
        """
        Author: kalyan
        double_click_dashboard_notification() - This method clicks the dashboard notifications.
        parameters: notification_type,license_type
        ex: double_click_dashboard_notification notification_type=voicemail
        ex: double_click_dashboard_notification notification_type=call license_type=operator
        change log: added log messages(UKumar: 26-Dec-2016)
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "Going to click on default notification")
            if params["notification_type"] == "voicemail":
                status = self.defaultPanel.double_click_voicemail_notification()
                if status == "false":
                    raise
                log.mjLog.LogReporter("ManhattanComponent", "info", "double_click_dashboard_notification"
                                                                    " - double click operation performed on voicemail notification")
            elif params["notification_type"] == "event":
                status = self.defaultPanel.double_click_notfication_on_event()
                if status == "false":
                    raise
                log.mjLog.LogReporter("ManhattanComponent", "info", "double_click_dashboard_notification"
                                                                    " - double click operation performed on event")
            elif params["notification_type"] == "call":
                if params["license_type"] == "operator":
                    status = self.defaultPanel.double_click_operator()
                    if status == "false":
                        raise
                    log.mjLog.LogReporter("ManhattanComponent", "info", "double_click_dashboard_notification"
                                                                        " - double click operation performed to accept call for operator")
                elif params["license_type"] == "non_operator":
                    status = self.defaultPanel.double_click_nonoperator()
                    if status == "false":
                        raise
                    log.mjLog.LogReporter("ManhattanComponent", "info", "double_click_dashboard_notification"
                                                                        " - double click operation performed to accept call for non operator")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "double_click_dashboard_notification -"
                                                                        " Correct option for item to be double clicked missing; operation not performed.")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "double_click_dashboard_notification "
                                                                    "- Incorrect license type. Double click operation not performed.")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "double_click_dashboard_notification - error : " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error double_click_dashboard_notification - error")


    def check_client_panel(self, **params):
        '''
           Author: Gautham
           check_client_panel() - To check attributes in clent pane
           parameters: user: to check presence of a user in client pane
                       noOfCalls: to verify number of current calls in client pane
                       callType: onCall: fail if call type is not ON CALL
                       callType: onHold: fail if call type is not ON HOLD
           ex: check_client_panel user=userB noOfCalls=1 callType=onCall
           Change List: if condition added in params["callType"] =="nocall" (UKumar: 21-June-2016)
        '''
        try: 
            if params["callType"] == "nocall":
                # self.assertElement.element_should_be_displayed("default_group_call_icon")
                if self.queryElement.element_not_displayed("default_client_pane_user"):
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel - user is not on call")
            # here this step will check the voicemail call notification and then ended the call (modified by kiran..)
            elif params["callType"] == "VoiceMailCall":
                self.assertElement.page_should_contain_text("Voice Mail")
                time.sleep(2)
                self.webAction.click_element("Default_EXO_end_call")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_client_panel- The call type is VoiceMailCall is verified and ended the call")
            else:
                
                userName = params["user"]
                name1 = userName.split("*")
                user = " ".join(name1)
                # if self.queryElement.element_not_displayed("default_recieve_call"):
                # log.mjLog.LogReporter("ManhattanComponent","info","check_client_panel- receive call button disappeared after receving the call")
                # else:
                # raise AssertionError("Receive call button is still present")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_client_panel- Checking attributes in clent pane")
                self.webAction.explicit_wait("default_client_pane_timer")

                if "consult" in params.keys():
                    self.assertElement.element_should_be_displayed("default_client_pane_timerconsult")
                    self.assertElement.element_should_contain_text("default_client_pane_userconsult", user)
                else:
                    self.assertElement.element_should_be_displayed("default_client_pane_timer")
                    self.assertElement.element_should_contain_text("default_client_pane_user", user)
                    # self.assertElement.element_should_contain_text("default_client_pane_user",params["user"])
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_client_panel- user name is visible as expected")
                log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel- Timer attribute is visible")
                time.sleep(2)
                if "checkhold" in params.keys():
                    self.assertElement.element_should_be_displayed("default_client_pane_end_call")
                else:
                    # self.assertElement.element_should_be_displayed("default_client_pane_end_button")
                    print("No checkhold")

                log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel - end button is present")
                # self.assertElement.element_should_contain_text("default_client_pane_no_of_call",params["noOfCalls"])
                # log.mjLog.LogReporter("ManhattanComponent","info","check_client_panel- Number of calls is visible as expected")
                if params["callType"] == "onCall":
                    self.assertElement.element_should_be_displayed("default_client_pane_on_call")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel - The call type is ON CALL")

                elif params["callType"] == "onConsult":
                    self.assertElement.element_should_be_displayed("default_client_pane_userconsult")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel - The call type is ON CALL")

                elif params["callType"] == "onHold":
                    self.assertElement.page_should_contain_text("On Hold")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel - The call type is On Hold")
                elif params["callType"] == "parked":
                    self.assertElement.page_should_contain_text("Parked")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_client_panel - The call type is Parked")
                elif params["callType"] == "onHoldRemote":
                    self.assertElement.page_should_contain_text("put you On Hold")
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "check_client_panel - The call type is onHoldRemote")

                elif params["callType"] == "groupCall":
                    # self.assertElement.element_should_be_displayed("default_group_call_icon")
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "check_client_panel - The call type is group call")
                elif params["callType"] == "videoCall":
                    self.assertElement.element_should_be_displayed("TP_video")
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "check_client_panel - The call type is video call")
                else:
                    raise AssertionError("wrong argument passed")


        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_client_panel- Failed to check attributes in client pane" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error check_client_panel- Failed to check attributes in client pane")

    def verify_INCALL(self, **params):
        """
        author:prashanth
        verify_INCALL() - This API verifies that the call is in dashboard & the contact card of the user who is on the call
        parameter: user=user1
        ex: verify_INCALL message="hello"
        """
        try:
            self.peopleGroup.verify_INCALL(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_INCALL - verified successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_INCALL - verification failed" + str(sys.exc_info()))
            return False

    def handle_workgroup(self, **params):
        """
        Author: Uttam
        handle_workgroup() : This API checks for WorkGroup notification
            in dashboard and various attributes of a WorkGroup
        Parameter: present and login
        Ex: handle_workgroup login=yes present=yes workGroupName=abc
            handle_workgroup login=no
        """
        try:
            self.workGroup.check_wk_notification(params["present"])
            if params["login"] == "yes":
                self.workGroup.check_wk_attributes(**params)
                log.mjLog.LogReporter("ManhattanComponent", "info", "handle_workgroup"
                                                                    " - WorkGroup attributes checked")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "handle_workgroup"
                                                                 " - Failed to handle WorkGroup " + str(sys.exc_info()))
            return False

    def handle_workgroup_logout(self):
        """
        author : kalyan
        handle_workgroup_logout() : This API checks for WorkGroup notification in dashboard and various attributes of a WorkGroup
        Parameter: present and logout
        Ex: handle_workgroup present=yes logout=yes workGroupName1=abc
            handle_workgroup present=yes logout=no
            handle_workgroup present=no logout=no
        Change list: Removed self.workGroup.check_wk_notification(params["present"]) and
                     #self.webAction.click_element("default_WK_notify") statements (UKumar: 28-Feb-2017)
        """
        try:
            self.workGroup.check_wk_attributes_logout()
            log.mjLog.LogReporter("ManhattanComponent", "info", "handle_workgroup_logout"
                                                                " - WorkGroup configuration done and sucessfully loggout")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "handle_workgroup_logout"
                                                                 " - Failed to handle WorkGroup logout " + str(
                sys.exc_info()))
            return False

    def tab_check_ppl_recnt_evnt_wrkgrp(self, **params):
        '''
           author : kiran
           tab_check_ppl_recnt_evnt_wrkgrp() - this API verifies all the tabs such as people, recent, event and workgroup.
           parameters: option
           ex1: tab_check_ppl_recnt_evnt_wrkgrp option=People/Recent/Event/WorkGroup

        '''
        try:
            if params["option"] == "People":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "tab_check_ppl_recnt_evnt_wrkgrp- checking people tab")
                self.defaultPanel.tab_check_PeoplePanel()
            elif params["option"] == "Recent":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "tab_check_ppl_recnt_evnt_wrkgrp- checking Recent tab")
                self.defaultPanel.tab_check_RecentPanel()
            elif params["option"] == "Event":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "tab_check_ppl_recnt_evnt_wrkgrp- checking Event tab")
                self.defaultPanel.tab_check_EventPanel()
            elif params["option"] == "WorkGroup":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "tab_check_ppl_recnt_evnt_wrkgrp- checking Workgroup tab")
                self.defaultPanel.tab_check_WorkgroupPanel()
            else:
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "tab_check_ppl_recnt_evnt_wrkgrp- invalid parameter provided")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "tab_check_ppl_recnt_evnt_wrkgrp- failed to check all tabs availabel in dashboard" + str(
                                      sys.exc_info()))
            return False

    def compress_uncompress_dashboard(self, **params):
        '''
           Author: kiran
           compress_uncompress_dashboard() -  this API compressed and uncompressed the dashboard
           parameters: no parameters required
           ex: compress_uncompress_dashboard
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "compress_uncompress_dashboard- going to compressed uncompressed the dashboard")

            if params["option"] == "compress":
                self.defaultPanel.compress_uncompress_dashboard_comprs(params)
            elif params["option"] == "uncompress":
                self.defaultPanel.compress_uncompress_dashboard_UnComprs(params)
            elif params["option"] == "check":
                self.defaultPanel.compress_uncompress_dashboard_Check(params)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "compress_uncompress_dashboard- unable to compress uncompress the dashboard" + str(
                                      sys.exc_info()))
            raise

    def workgroup_verify_select_wrapUp(self, **params):
        '''
           author : kiran
           workgroup_verify_select_wrapUp() - this API verifies/select the wrapup option in workgroup.
           parameters: wrapUp
           ex1: workgroup_verify_select_wrapUp wrapUp=verify/select

        '''
        try:
            if params["wrapUp"] == "verify":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgroup_verify_select_wrapUp- verify wrapUp option")
                self.assertElement.element_should_be_disabled("SPW_wrapUp")
            elif params["wrapUp"] == "select":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "workgroup_verify_select_wrapUp- select wrapUp option")
                self.assertElement._is_element_contains("SPW_wrapUp")
                self.webAction.click_element("SPW_wrapUp")
                time.sleep(5)
                self.assertElement._is_element_contains("FP_compressed_workgrp_yellow_color")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "workgroup_verify_select_wrapUp- invalid parameter provided")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "workgroup_verify_select_wrapUp- successfully verify/select the wrapUp option")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "workgroup_verify_select_wrapUp- failed to check all tabs availabel in dashboard" + str(
                                      sys.exc_info()))
            raise

    def verify_compUncmp_workgroup_icon(self, **params):
        '''
           author : kalyan
           verify_compUncmp_workgroup_icon() - this API verifies workgroup icon color.
           parameters: compressed,green
           ex1: verify_compUncmp_workgroup_icon mode=compressed color=green

        '''
        try:
            if params["mode"] == "compressed":
                self.defaultPanel.workgrp_iconColorCheck_inCompressed(params)
            elif params["mode"] == "uncompressed":
                self.defaultPanel.workgrp_iconColorCheck_inUnCompressed(params)
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_compUncmp_workgroup_icon- invalid paramete mode given")
                return False
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_compUncmp_workgroup_icon- failed to check WG icon color in dashboard" + str(
                                      sys.exc_info()))
            return False

    def verify_hold_unhold_in_third_panel(self, **params):
        """
        Author: Manoj
        verify_hold_unhold_in_third_panel() - This API verifies hold button, retrieve button,
        normal call timer, on hold timer, Put On Hold and On Hold test for a call on hold
        Parameters: option
        Ex: verify_hold_unhold_in_third_panel option=put_on_hold
        Change List: Added documentation, log messages and elif condition for timer_onhold_call (UKumar - 01-June-2016)
        """
        try:
            time.sleep(3)            
            if params["option"] == "put_on_hold":
                text = self.queryElement.get_text("third_panel_transfer_park_held")
                if "put you on hold" in text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_hold_unhold_in_third_panel - 'Put you on Hold' verified")
            elif params["option"] == "resume":
                self.assertElement.page_should_contain_element("third_panel_unhold_call")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_hold_unhold_in_third_panel - retrieve button present")
            elif params["option"] == "timer_normal_call":
                time.sleep(2)
                self.assertElement.page_should_contain_element("Tp_whisper_page")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_hold_unhold_in_third_panel - cal timer present")
            elif params["option"] == "timer_onhold_call":
                text = self.queryElement.get_text("third_panel_transfer_park_held")
                if "On Hold" in text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_hold_unhold_in_third_panel - 'On Hold' verified")
            elif params["option"] == "hold":
                self.assertElement.page_should_contain_element("third_panel_hold_call")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_hold_unhold_in_third_panel - Hold button present")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_hold_unhold_in_third_panel - failed to"
                                                                 " verify on hold call options " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_hold_unhold_in_third_panel - failed to verify on hold call options")

    def verify_no_ongoing_call(self):
        """
        verifies if no ongoing call is in default tab
        """
        try:
            #self.webAction.explicit_wait("default_recieve_call")
            if self.queryElement.element_not_displayed("default_recieve_call"):
                time.sleep(1)
                if self.queryElement.element_not_displayed("default_call_section"):
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_no_ongoing_call- no call is happening currently")
                else:
                    raise AssertionError("call is happening")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_no_ongoing_call - failed to verify ongoing call")
            raise Exception("ManhattanComponent error verify_no_ongoing_call - failed to verify ongoing call")

    def launch_url(self, **params):
        '''
        Author : Prashanth
        launch_url():To launch the url from exo client
        Parameters: URL
        Ex: launch_url URL=http://google.com
        '''
        try:
            self._browser.go_to(params["URL"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "launch_url - launched URL")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "launch_url - Failed to launch url " + str(sys.exc_info()))
            return False

    def get_url(self):
        '''
        Author : Prashanth
        get_url():To get the url dynamically from event

        '''
        try:
            url = self.queryElement.get_text("FP_Event_url")
            actual_url = url
            log.mjLog.LogReporter("ManhattanComponent", "info", "get_url - URL copied")
            return actual_url
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "get_url - Failed to get url " + str(sys.exc_info()))
            return False

    def join_endo_conference(self, **params):
        """
        Author : UKumar
        join_endo_conference(): To join conference from Endo client either in Chat mode or by dial-in  
        Parameters: 
        Ex: join_endo_conference option=web_chat_mode
        Ex: join_endo_conference option=by_dial_in join_on=external_number
        Ex: join_endo_conference option=by_dial_in join_on=internal_number joining_device=deskphone/softphone
        """
        try:
            if params["option"].lower() == "by_dial_in":
                self.event.join_endo_conference_dialin(params)
                log.mjLog.LogReporter("ManhattanComponent", "info", "join_endo_conference - joined event via dial-in")
            else:
                self.event.join_endo_conference_chat()
                log.mjLog.LogReporter("ManhattanComponent", "info", "join_endo_conference - joined event in chat mode")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "join_endo_conference"
                                  " - Failed to join event from endo client " + str(sys.exc_info()))
            return False

    def verify_conference_sucess(self, **params):
        '''
           Author: Upendra
           verify_conference_sucess() - verifies if the conference is successful or not

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_conference_sucess- joined the conference")
            time.sleep(1)
            self.assertElement._is_element_present("events_mute_all")
            time.sleep(5)
            self.assertElement._is_element_present("events_mute_all_on")

            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_conference_sucess- Conference joined successfully ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_conference_sucess- Failed to join the Conference " + str(sys.exc_info()))
            return False

    def logout(self, **params):
        """
        Author:Uttam
        logout() - This API logs out from Manhattan Client
        Parameters: windowNumber
        Ex: logout windowNumber=1
        Extra Info: pass windowNumber=0 if you are at default window
                    pass windowNumber=1 if you are at Preferences window
        """
        try:
            if "close" in params.keys():
                self.webAction.click_element("people_close")
                log.mjLog.LogReporter("ManhattanComponent", "info", "logout - "
                                                                    "clicked on close button of  Manhattan Client")
            else:
                window = params["windowNumber"]
                if window == "1":
                    self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
                    
                self.webAction.click_element("default_user_telephony_color")
                self.webAction.explicit_wait("default_logout")
                self.webAction.click_element("default_logout")
                self.webAction.explicit_wait("Login_Email")
                log.mjLog.LogReporter("ManhattanComponent", "info", "logout - "
                                                                    "Logged out from Manhattan Client")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "logout - "
                                                                 "Failed to logout " + str(sys.exc_info()))
            raise

    def click_people_button_people(self, **params):
        """
        Author: UKumar
        click_people_button_people() - This API clicks on People button in second panel(people panel)
        Parameters: no parameter
        Ex: click_people_button_people
        """
        try:
            self.webAction.click_element("peoples_people_button")
            self.assertElement.element_should_be_displayed("peoples_second_panel_minimized_button")
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_people_button_people"
                                                                "- People button clicked")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_people_button_people"
                                                                 "- failed to click on People button " + str(
                sys.exc_info()))
            return False

    def enter_group_name(self, **params):
        """
        Author: UKumar
        enter_group_name(): This API clicks on New Group button and enters the group name
        Parameters: groupName
        Ex: enter_group_name groupName=newgrp
        """
        try:
            deleteGroupDictionary = { "groupName" : [params["groupName"]]}
            self.delete_group(**deleteGroupDictionary)
            self.webAction.click_element("peoples_group")
            self.peopleGroup.add_new_group_button()
            log.mjLog.LogReporter("ManhattanComponent", "info", "enter_group_name"
                                                                " - Group creation panel opened")
            self.webAction.input_text("peoples_name", params["groupName"])
            self.webAction.click_element("peoples_drang_drop_name")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "enter_group_name - Group creation panel has been updated"
                                  " with group name %s" % params["groupName"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "enter_group_name"
                                                                 " -  error in entering group name")
            return False

    def drag_drop_contact_to_group(self, **params):
        '''
        Author: UKumar
        drag_drop_contact_to_group() - Search a contact and Drag and drop it to new group and save
        Parameters: contact1, contact2 ... and groupName
        Ex: drag_drop_contact_to_group contact1=user_db1_01 contact2=user_db1_02 groupName=newgrp
        Extra Info.: for passing full name, use firstName*lastName
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "drag_drop_contact_to_group"
                                                                " - Drag and drop contact from people tab to  new group and save")
            contactList = []
            for key in params.keys():
                if "contact" in key:
                    contactList.append(params[key].replace('*', ' '))
            self.createGroupclass.drag_drop_contact_to_group(contactList)
            log.mjLog.LogReporter("ManhattanComponent", "info", "drag_drop_contact_to_group"
                                                                " - Drag and drop contacts to group is successful")
            self.webAction.click_element("peoples_save_Changes")
            log.mjLog.LogReporter("ManhattanComponent", "info", "drag_drop_contact_to_group"
                                                                " -  group created successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "drag_drop_contact_to_group"
                                                                 " - Drag and drop contact to group failed " + str(
                sys.exc_info()))
            return False

    def create_new_group(self, **params):
        """
        Author: modified by uttam
        create_new_group() - create new group by giving groupName and contactlist
        Parameters: groupName, contactlist, choice and discardMyChanges
        Ex1: create_new_group groupName=paxterra contact1=User1 contact2=User2 choice=save
        Ex2: create_new_group groupName=paxterra contact1=User1 contact2=User2 choice=cancel discardMyChanges=yes
        Extra info.: choice could be save, cancel or x(to close third panel)
        Change List: used regular expression for groupName,
                removed if condition for Split (UKumar : 10-June-2016)
        """
        try:
            for i in range(0, 2):
                if not self.queryElement.element_not_displayed("TP_close_minimise"):
                    self.webAction.click_element("TP_close_minimise")
                    self.webAction.click_element("people_dscrdChanges_Popup_Yes")
            deleteGroupDictionary = { "groupName" : [params["groupName"]]}
            self.delete_group(**deleteGroupDictionary)
            self.webAction.click_element("peoples_group")
            self.peopleGroup.add_new_group_button()
            if params["groupName"] == "Dummy_check_draft":
                print("providing the dummy group")
                return
            contactlist = []
            # this line has been added : to add multiple members to the group such as 50, 100 members (kiran)
            if "number" in params.keys():
                number = int(params["number"])
                name = params["first_grp_member"].split("_")
                for i in range(1, number):
                    contact = "USER" + str(i) + '_' + name[1]
                    contactlist.append(contact)
            else:
                for key in params.keys():
                    if "contact" in key:
                        contactlist.append(params[key].replace('*', ' '))

                print(contactlist)
            groupName = re.sub("\*", " ", params["groupName"])

            if "discardMyChanges" in params.keys():
                self.createGroupclass.add_new_group(groupName, contactlist,
                                                    params["choice"], params["discardMyChanges"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "create_new_group - group %s"
                                                                    " cancelled" % (params["groupName"]))
            else:
                self.createGroupclass.add_new_group(groupName, contactlist, params["choice"])
                time.sleep(1)
                log.mjLog.LogReporter("ManhattanComponent", "info", "create_new_group"
                                                                    " - group %s added" % (params["groupName"]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "create_new_group - "
                                                                 "group addition failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error create_new_group - group addition failed")

    def select_group_options(self, **params):
        """
        Author : Uttam
        select_group_options() - This API selects a group from second
                    panel and clicks on either group chat, meeting with
                    group or group voicemail
        Parameters : groupName and option
        Ex : select_group_options groupName=Test option=groupChat/meetingWithGroup/groupVM contact1=abc
        """
        try:
            if "noselect" in params.keys():
                print("no selecting the group")
            else:
                self.peopleGroup.group_select(params["groupName"])
            time.sleep(2)
            self.peopleGroup.verify_group_option(params)
            self.assertElement.page_should_contain_element("third_panel_edit_group")
            log.mjLog.LogReporter("ManhattanComponent", "info", "select_group_options - "
                                                                "group options verified")

            if params["option"] == "groupChat":
                self.peopleGroup.select_group_option(params)
                self.webAction.explicit_wait("third_panel_chatBox")
                self.assertElement.element_should_be_displayed("third_panel_chatBox")
            elif params["option"] == "meetingWithGroup":
                self.peopleGroup.select_group_option(params)
                self.assertElement.element_should_be_displayed("events_create_invite")
            elif params["option"] =="groupVM":
                self.peopleGroup.select_group_option(params)
                self.assertElement.element_should_be_displayed("VM_record_option")
                self.assertElement.element_should_be_displayed("TP_GroupVM_Cancel")
                self.assertElement.element_should_be_displayed("VM_record_option")
            else:
                pass
            log.mjLog.LogReporter("ManhattanComponent", "info", " select_group_options - "
                                                                "%s option selected" %params["option"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", " select_group_options - "
                                                                 "Error is : " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error select_group_options")

    def display_group_name(self, **params):
        try:
            self.peopleGroup.group_tab()
            time.sleep(2)
            self.assertElement.page_should_contain_text(params["groupName"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "display_group_name - group %s display_group_name successfully" % (
                                  params["groupName"]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "display_group_name - group %s display_group_name" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error display_group_name")

    def edit_group(self, **params):
        """
        Author: UKumar
        edit_group - Selects a group from second panel and opens it in third panel,
                    verifies group members, edit group button, save button and cancel button
        Parameters: groupName and contacts
        Ex: edit_group groupName=Test contact1=abc
        """
        try:
            self.peopleGroup.group_select(params["groupName"])
            time.sleep(3)  # to wait for third panel to open, explicit_wait is not working
            self.peopleGroup.verify_group_option(params)
            self.peopleGroup.open_edit()
            time.sleep(2)
            contacts = []
            for key in params.keys():
                if "contact" in key:
                    contacts.append(params[key])
            users = self._browser.elements_finder("TP_group_member_field_name")
            userList = []
            for user in users:
                userList.append(user.text)
            for contact in contacts:
                if contact in userList:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "edit_group -"
                                                                        " contact is present in members field")
                else:
                    raise AssertionError("%s is not present in members field" % contact)
            self.assertElement.page_should_contain_element("peoples_save_Changes")
            self.assertElement.page_should_contain_element("TP_delete_group")
            log.mjLog.LogReporter("ManhattanComponent", "info", "edit_group - group is opened for editing")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "edit_group - failed to"
                                                                 " open group for editing " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error edit_group - failed")

    def verifingEdit_group(self, **params):
        try:
            self.assertElement.element_should_be_displayed("peoples_cancel")
            self.assertElement.element_should_be_displayed("third_panel_contact_save")
            self.webAction.clear_input_text("peoples_name")
            # self.personname = params["personname"]
            self.webAction.input_text("peoples_name", params["personname"])
            # self.persongroup = params["persongroup"]
            print("rtyuiortyuiortyui")
            self.webAction.input_text("people_input_contact", params["persongroup"])
            print("**************")
            time.sleep(6)
            self.webAction.click_element("third_panel_contact_save")
            time.sleep(6)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "Failed to save editgroup changes to Manhattan" + str(sys.exc_info()))
            return False

    def modify_group_add_member(self, **params):
        """
        Author: modified by Uttam
        modify_group_add_member() - modify group by adding contact
        Parameters: groupName, contactlist and choice
        Ex: modify_group_add_member groupName=paxterra contact1=User3 contact2=User1
                                    choice=save discardMyChanges=yes
        Extra info: discardMyChanges is optional, call edit_group API before this API
        Change list: added assertion for both conditions(if, else),
                     removed elif condition (UKumar: 7-June-2016)
        """
        try:
            contactlist = []
            for key in params.keys():
                if "contact" in key:
                    #time.sleep(5)
                    contactlist.append(params[key])
            print(contactlist)

            new_group_name = ''
            if "newGroupName" in params.keys():
                new_group_name = params["newGroupName"]
            if "discardMyChanges" in params.keys():
                self.createGroupclass.modify_group_add_contact(new_group_name, contactlist, params["choice"],
                                                               params["discardMyChanges"])
                self.assertElement.page_should_contain_text(params["groupName"])
            else:
                self.createGroupclass.modify_group_add_contact(new_group_name, contactlist, params["choice"])
            if "newGroupName" in params.keys() and params["choice"] == "save":
                self.assertElement.page_should_contain_text(new_group_name)
            else:
                self.assertElement.page_should_contain_text(params["groupName"])
            # time.sleep(7)
            log.mjLog.LogReporter("ManhattanComponent", "info", "modify_group_add_member -"
                                                                " group %s modified Successfully" % params["groupName"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "modify_group_add_member"
                                                                 " - group failed " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error modify_group_add_member - failed")

    def modify_group_del_member(self, **params):
        """
        Author: modified by Uttam-Upendra
        modify_group_del_member() - modify group by deleting contact
        parameters: groupName & contactlist
        Ex: modify_group_del_member groupName=paxterra contact1=User3 contact2=User1
                                    choice=save discardMyChanges=yes
        Extra info: discardMyChanges is optional
        """
        try:
            self.peopleGroup.group_tab()  # selecting the group tab
            self.peopleGroup.group_select(params["groupName"])  # selecting group which is to modified
            # time.sleep(3)
            self.peopleGroup.open_edit()

            contactlist = []
            for key in params.keys():
                if "contact" in key:
                    contactlist.append(params[key])

            print("Contact List in Manhattan Component ", contactlist)
            if "discardMyChanges" in params.keys():
                self.createGroupclass.delete_group_of_contacts(contactlist, params["choice"],
                                                               params["discardMyChanges"])
            else:
                self.createGroupclass.delete_group_of_contacts(contactlist, params["choice"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "modify_group_del_member - "
                                                                "group " + (
                                  params["groupName"]) + " modified Successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "modify_group_del_member"
                                                                 " - group modification failed " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error modify_group_del_member - failed")

    def rename_group_with_add_double_quotes(self, **params):

        '''
           author : surendra
           rename_group_with_add_double_quotes() - rename the group by giving currentGroupName and newGroupName
           parameters: currentGroupName & newGroupName
           ex: rename_group_with_add_double_quotes currentGroupName=paxterra newGroupName=shoretel
        '''
        try:
            self.peopleGroup.group_tab()
            self.peopleGroup.group_select(params["currentGroupName"])
            self.peopleGroup.open_edit()
            self.createGroupclass.rename_group_withdouble_quotes(params["newGroupName"])
            time.sleep(10)
            # self.assertElement.page_should_not_contain_text(params["currentGroupName"])
            # self.assertElement.page_should_contain_text(params["newGroupName"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "rename_group_with_add_double_quotes - group %s rename_group_with_add_and_remove_withspace to %s successfully" % (
                                  params["currentGroupName"], params["newGroupName"]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "rename_group - failed to rename_group_with_add_and_remove_withspace  " + str(
                                      sys.exc_info()))
            return False

    def search_all_groups_contact_member(self, **params):
        """
        Author: UKumar
        search_all_groups_contact_member() - Search for all the given contacts in all the groups present
                                             If no group is present then prints message only(no group present)
        Parameters: contacts and type
        Ex: search_all_groups_contact_member contact1=user1 contact2=user2 type=positive/negative
        Extra Info. : If you want to search that contact is a part of a group then pass type=positive
                      If you want to search that contact is not a part of group then pass type=negative
        """
        try:
            self.peopleGroup.group_tab()
            grouplist = self.peopleGroup.get_group_list()
            if grouplist:
                contacts = list()
                for key in params.keys():
                    if "contact" in key:
                        contacts.append(params[key])
                        # for group in grouplist:
                        # self.peopleGroup.group_select(params["groupName"])
                        # time.sleep(5)
                for contact in contacts:
                    self.createGroupclass.search_group_contact(contact, params["type"])
                    time.sleep(3)
                    log.mjLog.LogReporter("ManhattanComponent", "info", "search_all_groups_contact_member"
                                                                        " - checking contact in the group is Successful")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "search_all_groups_contact_member"
                                                                    " - no group found")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", " search_all_groups_contact_member"
                                                                 " - checking contact in the group Failed " + str(
                sys.exc_info()))
            return False

    def check_order_of_users(self, **params):
        """
        check_order_of_users() - This API checks the order of appearance of two users in the people list
        parameters : groupName, users name
        check_order_of_users groupName=All users=AUser#BUser
        extra info.: for passing more than one user at a time we have to pass users name separated with #
        """
        try:
            self.peopleGroup.group_tab()
            indecesUsers = []
            i = 0
            users = params["users"].split("#")
            userList = self._browser.get_current_browser().find_elements_by_class_name("first-name")

            for user in userList:
                if user.text == users[i]:
                    indecesUsers.append(userList.index(user))
                    i = i + 1
                if i == len(users):
                    break

            if indecesUsers[0] < indecesUsers[1]:
                log.mjLog.LogReporter("ManhattanComponent", "info", "check_order_of_users -"
                                                                    " the order of appearance is " + users[0] + "->" +
                                      users[1])
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "check_order_of_users -"
                                                                    " the order of appearance is " + users[1] + "->" +
                                      users[0])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_order_of_users - error while"
                                                                 " checking the order of appearance of users " + str(
                sys.exc_info()))
            return False

    def delete_group(self, **params):
        """
        Author: Unknown modified by Uttam (26-May-2016)
        delete_group() - This API deletes a group identified by groupName
        Parameter: groupName
        Ex: delete_group groupName=Test option=delete/cancel
        Extra Info.: option is optional (if you want to click on Cancel button after clicking on
                     'Delete Group' button then pass option=no)
        """
        try:
            parameters = {}
            self.groupName = params["groupName"]
            if "option" in params and params["option"] == "cancel":
                parameters.update({"option": params["option"]})
            if isinstance(self.groupName, list):            
                for i in self.groupName:
                    parameters.update({"groupName": re.sub("\*", " ", i)})
                    self.peopleGroup.delete_group(parameters)
                    log.mjLog.LogReporter("ManhattanComponent", "info", "delete_group - "
                                                                    "group %s deleted successfully" % (i))
            else:
                parameters.update({"groupName": re.sub("\*", " ", self.groupName)})
                self.peopleGroup.delete_group(parameters)
                if "option" in params and params["option"] != "cancel":
                    time.sleep(1)
                    # self.assertElement.page_should_not_contain_text(self.groupName)
                log.mjLog.LogReporter("ManhattanComponent", "info", "delete_group - "
                                                                    "group %s deleted successfully" % (self.groupName))

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "delete_group - "
                                                                 "group %s deletion failed" % (self.groupName))
            raise Exception("ManhattanComponent error delete_group - failed")

    def delete_contact(self, **params):         
        """
        Author: bparihar
        delete_contact() - This API deletes a contact identified by contactNumber
        Parameter: searchItem
        Ex: delete_contact contactNumber=Test
        """
        try:
            i = 0
            if "first_name" in params and "last_name" in params:
                self.searchedItem = params["first_name"] + " " + params["last_name"]                
            else:
                self.searchedItem = params["num"]
            
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            self.webAction.input_text("default_search_input", self.searchedItem)
            time.sleep(1)
            contacts = self._browser.elements_finder("peoples_panel_customer_name")
            while(1):
                try:
                    contacts[i].click()
                    self.peopleGroup.delete_contact()
                    time.sleep(1)
                    i += 1
                except:
                    return
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "delete_contact - "
                                                                 "contact %s deletion failed" % (self.searchedItem))

    def search_group_contact_member(self, **params):
        '''
           Author: Gautham
           search_group_contact_member() - search for a contact in an existing group
           parameters: groupName, contact and type
           ex: search_group_contact_member grooupName=group1 contact=user1 type=positive/negative
        '''
        try:
            self.peopleGroup.group_select(params["groupName"])
            time.sleep(2)
            self.createGroupclass.search_group_contact(params["contact"], params["type"])
            # time.sleep(3)
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "search_group_contact_member - checking contact in the group is Successful")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  " search_group_contact_member - checking contact in the group Failed" + str(
                                      sys.exc_info()))
            return False

    def go_to_new_contact(self):
        '''
        Author: Gautham
        go_to_new_contact - To go to new contact page
        ex: go_to_new_contact
        change list: added assertion for all the contact fields(UKumar: 22-July-2016)
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "go_to_new_contact - Opening new contact page")
            self.invoke_dashboard_tab(**{"option":"people"})
            for i in range(0, 2):
                if not self.queryElement.element_not_displayed("TP_close_minimise"):
                    self.webAction.click_element("TP_close_minimise")
                    self.webAction.click_element("people_dscrdChanges_Popup_Yes")
            self.webAction.click_element("peoples_add_button")
            time.sleep(2)           
            # autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            # autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{ENTER}")
            self.webAction.click_element("add_new_contact")
            log.mjLog.LogReporter("PeopleGroup","info","add_new_group_button - creating new group")
            time.sleep(3)
            self.assertElement.page_should_contain_element("people_new_contact_first_name")
            self.assertElement.page_should_contain_element("people_new_contact_last_name")
            self.assertElement.page_should_contain_element("people_new_contact_email")
            self.assertElement.page_should_contain_element("people_new_contact_job_title")
            self.assertElement.page_should_contain_element("people_new_contact_department")
            self.assertElement.page_should_contain_element("people_new_contact_company_name")
            self.assertElement.page_should_contain_element("people_new_contact_address")
            self.assertElement.page_should_contain_element("people_new_contact_city")
            self.assertElement.page_should_contain_element("people_new_contact_state")
            self.assertElement.page_should_contain_element("people_new_contact_zip")
            self.assertElement.page_should_contain_element("people_new_contact_country")
            self.assertElement.page_should_contain_element("third_panel_contact_save")
            self.assertElement.page_should_contain_element("TP_contact_form_close")
            log.mjLog.LogReporter("ManhattanComponent", "info", "go_to_new_contact - PASS")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "go_to_new_contact - FAILED " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error go_to_new_contact - failed")

    def add_new_number(self):
        # click on +Add Number button
        try:
            time.sleep(0.5)
            self.webAction.click_element("outside_of_panel")
            self.webAction.click_element("add_number_button")
            
        except:
            raise Exception("ManhattanComponent error Add new number - failed" + str(sys.exc_info()))

    def add_contact_number(self, **params):
        '''
        Author: Gautham
        add_contact_number - To add contact number. This needs to be added before adding other contact details
        parameters: pos: position of the number
                    phType: phone type to be selected(Mobile,Home,Office,Fax,Assistant)
                    num: number to be added
        ex: add_contact_number pos=1 phType=Mobile num=9977667766

        '''
        try:            
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_contact_number - Add contact number")
            if "editnumber" in params.keys():
                self.peopleGroup.add_contactedit_number("people_new_contact_drop_down_1", "people_new_contact_number_1",
                                                        params["phType"], params["num"])

            # Click the second dropdown            
            elements = self._browser.elements_finder("people_new_contact_add_num")
            (elements[-1]).click()
            
            if params["phType"].lower() == "home":
                self.peopleGroup.add_contact_number("people_new_contact_drop_down_1", "people_new_contact_number",
                                                    params["phType"], params["num"])
            elif params["phType"].lower() == "business":
                self.peopleGroup.add_contact_number("people_new_contact_drop_down_2", "people_new_contact_number", params["phType"], params["num"])
            elif params["phType"].lower() == "fax":
                self.peopleGroup.add_contact_number("people_new_contact_drop_down_3", "people_new_contact_number",
                                                    params["phType"], params["num"])
            elif params["phType"].lower() == "mobile":
                self.peopleGroup.add_contact_number("people_new_contact_drop_down_4", "people_new_contact_number",
                                                    params["phType"], params["num"])
            elif params["phType"].lower() == "pager":
                self.peopleGroup.add_contact_number("people_new_contact_drop_down_5", "people_new_contact_number",
                                                    params["phType"], params["num"])
            else:
                raise AssertionError("Argument value not allowed")
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_contact_number - Number added successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_contact_number - Failed to add number")
            raise Exception("ManhattanComponent error add_contact_number - failed")

    def add_contact_details(self, **params):
        '''
        Author: Gautham
        add_contact_details - To add contact with details like first name, middle name
                              last name, company name, department, business, mobile, pager,
                              home number, job title, address, city, state, zip, country
        parameters: first_name, middle_name, last_name, company, department, business, mobile,
                    pager, home_number, fax, email, IM, title, address, city, state, zip, country, cancel
        ex: add_contact_details first_name=test1 middle_name=test2 last_name=test3 company=test4 department=test5
            business=test6 mobile pager=test7 home_number=test8 fax=test9 email=test10 IM=test11 cancel=yes
        Extra Info: pass cancel=yes if you want to cancel the contact(save as a draft)
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_contact_details - Add contact details")
            self.peopleGroup.add_contact_details(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_contact_details - PASS")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_contact_details -"
                                                                 " FAILED " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error add_contact_details - failed")

    def verify_manditory_contact_fields(self, **params):
        '''
        Author: UKumar
        verify_manditory_contact_fields - Verifies manditory fields for contact creation
        Parameters: firstName, lastName, email, im, phoneNumber
        Ex: verify_manditory_contact_fields firstName=yes lastName=yes
        '''
        try:
            self.webAction.click_element("third_panel_contact_save")
            self.thirdPanel.verify_manditory_contact_fields(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_manditory_contact_fields"
                                                                " - manditory fields verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_manditory_contact_fields"
                                                                 " - FAILED " + str(sys.exc_info()))
            return False

    def edit_contact_set_blank_values(self, **params):
        """
        Author: UKumar
        edit_contact_set_blank_values(): To edit the contact and set the various fields to blank values
        Parameters : title, dept, company, address, city
        Ex: edit_contact_set_blank_values title=blank dept=blank company=blank address=blank city=blank
        """
        try:
            self.thirdPanel.click_edit_contact_button()
            self.thirdPanel.blank_out_contact_fields(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "edit_contact_set_blank_values"
                                                                " - Contact fields have blanked out")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "edit_contact_set_blank_values"
                                                                 " - failed to set blank value for contact fileds")
            return False

    def verify_contact_info(self, **params):
        """
        Author: Uttam
        verify_contact_info() - This API verifies the contact information
                                displayed on third(contact) panel or not
        Parameters: status, email, address, mobile, pager,home, assistant, fax
        Ex: verify_contact_info status=present/absent email=uk@shoretel.com address=Bangalore
                                mobile=9656789833 pager=34567 home=01209874
                                assistant=23456789 fax=123456
        Extra Info: mobile, pager,home, assistant and fax all are optional
                    status=present for checking presence and status=absent
                    for checking that info. is not present
        """
        try:
            self.thirdPanel.verify_contact_info(**params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_info -"
                                                                " contact information verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_contact_info -"
                                                                 " failed to verify contact info")
            raise Exception("ManhattanComponent error verify_contact_info - failed")

    def check_element_onpage(self, **params):
        '''
        check_element_onpage() - check particular element text exist in page by giving elementName
        parameters : elementName
        ex: check_element_onpage elementName=NewContact

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_element_onpage- verifing element existing or not ")
            self.thirdPanel.verify_element_availability_onpage(params["elementName"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_element_onpage - verifing element existing or not" + str(sys.exc_info()))
            return False

    def check_no_element_onpage(self, **params):
        '''
        Author: UKumar
        check_element_onpage() - check that particular element text does not exist in page by giving elementName
        Parameters : elementName
        Ex: check_no_element_onpage elementName=company
        '''
        try:
            element_dict = {"fullname": "TP_contact_fullname", "company": "TP_contact_company", \
                            "title": "TP_contact_title", "dept": "TP_contact_dept", "address": "TP_contact_address"}
            self.thirdPanel.verify_element_non_availability_onpage(element_dict[params["elementName"].lower()])
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_no_element_onpage - element does not exist")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_no_element_onpage - "
                                                                 "failed to verify existence of element" + str(
                sys.exc_info()))
            return False

    def type_value_in_extension_search(self, **params):
        """
        Parameters: searchItem
        Ex1: type_value_in_extension_search searchItem=user1
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "type_value_in_extension_search - Searching people by searchItem provided")
            searchItem = re.sub("\*\*", " ", params["searchItem"]) 
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            log.mjLog.LogReporter("DefaultPanel","debug","type_value_in_extension_search - Clicked on search button")
            self.webAction.input_text("default_search_input",searchItem)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "type_value_in_extension_search - Searching people by name"
                                                                 " failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error type_value_in_extension_search - failed")

    def press_escape(self, **params):
        """
        This API press escape at defined target
        Ex1: press_escape option=search_extension
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info","press_escape - Press Escape")
            option = params["option"]
            if option == "search_extension":
               self.webAction.press_key("default_search_input", "ESCAPE")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info","press_escape - Unable to Press Escape")
    
    def press_key(self, **params):
        """
        This API press escape at defined target
        Ex1: press_escape option=search_extension
        Press Key with ${client1} and key=DOWN and times=2
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info","press_escape - Press Escape")
            key = re.sub("\*\*", " ", params["key"])
            times = params["times"]
            for i in range(0,int(times)):
                print("Going here")
                autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info","press_escape - Unable to Press Key")

    def verify_search_people_list_closed(self):
        """
        This API verifies search people list is closed
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info","verify_search_people_list_closed - Find element")
            searchResultsList=self._browser.elements_finder("FP_search_extension_result")
            if len(searchResultsList) != 0:
                raise Exception("search people list is not closed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info","verify_search_people_list_closed - Unable to verify search people list closed")
    
    def scroll_search_people_extension_result(self):
        """
        This API scrolls the result of search people extension
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info","scroll_search_people_extension_result - Scroll Started")
            self.webAction.scroll("FP_search_extension_result_scrollbar_selector", 100)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info","verify_search_people_list_closed - Unable to scroll")
    
    
    def search_people_extension(self, **params):
        """
        Author : modified by Bhupendra
        search_people_extension() - search people by giving searchItem as name or number and throwException tells to raise exception or not
        Parameters: searchItem
        Ex1: search_people_extension searchItem=user1
        Ex2 : search_people_extension searchItem=123
        Extra Info. : If your searchItem has spaces then pass it like first**second
        """
        try:           
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "search_people_or_extension - Searching people by name ")
                                  
            search_item = re.sub("\*\*", " ", params["searchItem"])            
            
            # Will not throw Exception if contact not found if throwException passed as False
            itemObject = self.defaultPanel.search_people_or_extension(search_item, False)
            # self.peopleGroup.display_person_detail()
            if itemObject == False:
                return False
            else:
                itemObject.click()
                time.sleep(2)
                if "name" in params.keys():
                    search_item = re.sub("\*", " ", params["name"])
                self.assertElement.page_should_contain_text(search_item)
                log.mjLog.LogReporter("ManhattanComponent", "info", "search_people_extension - contact is available")
                if "info" in params.keys():
                    self.peopleGroup.display_person_detailinfo()

                return True
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "search_people_extension - Searching people by name"
                                                                 " failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error search_people_extension - failed")

    def search_people_for_multiuser(self, **params):
        '''
            Author: surendra
            Enter the name in serach bar
            check the contact(or contacts if more
            than one exists with same name) exist  or not
        '''
        try:
            self.searchItem = params["searchItem"]
            self.searchItem = re.sub("\*\*", " ", params["searchItem"])            
            self.webAction.click_element("default_name_number_search")
            # time.sleep(1)
            # self.webAction.click_element("default_name_number_search")
            log.mjLog.LogReporter("DefaultPanel", "debug", "search_people_or_extension : Clicked on search button")
            self.webAction.input_text("default_search_input", params["searchItem"])
            time.sleep(2)
            self.webAction.explicit_wait("peoples_panel_customer_name")
            searchResultsList = self._browser.elements_finder("peoples_panel_customer_name")
            searchResultsList[0].click()
            time.sleep(2)
        except:
            log.mjLog.LogReporter("DefaultPanel", "error",
                                  "search_people_multiplelist-Error while searching people" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error search_people_multiplelist - failed")

    
    def end_voicemail_call(self):
        # To check and terminate an ongoing call in dashbord
        i = 0
		# call_list points to the hangup buttons.
        call_list = self._browser.elements_finder("End_VoiceMail_Call")
        while(1):
            try:
                call_list[i].click()
                time.sleep(1)
                i += 1
            except:
                return
    
    def search_people_match_name(self, **params):
        '''
           Author: Gautham
           search_people_match_name() - Search the person from dashbord by giving a name or number
           parameters: searchName, matchName
           ex: search_people_match_name searchName=will matchName=williams find=yes(if expect to find a name)
           find=no(if don't expect to find a name)

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "search_people_match_name- Search the person from dashboard by giving a name or number")
            # self.peopleGroup.search_people_match_name(params["searchName"],params["matchName"])
            self.peopleGroup.search_people_match_name(params["searchName"], params["matchName"], params["find"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "search_people_match_name- contact available ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "search_people_match_name- Searching people from dashboard failed" + str(
                                      sys.exc_info()))
            return False

    def verify_system_directory(self, **params):
        '''
           Author: kiran modified by kalyan
           verify_system_directory() - this API verify the system directory
           parameters: contact1, contact2, contact3
           ex: verify_system_directory contact1=Auto-Attendant contact2=Voice*Mail*Login contact3=Conference*Ext.
        '''
        try:
            searchItem1 = params["contact1"]
            searchItem2 = params["contact2"]
            searchItem3 = params["contact3"]
            list = self._browser.elements_finder("extension_close_searching")
            if len(list) == 1:
                print("dialler close is present")
                self.webAction.click_element("extension_close_searching")
            self.webAction.click_element("default_name_number_search")
            anchorlist = self._browser.elements_finder("peoples_panel_customer_name")
            print("length of list is:", len(anchorlist))
            searchItem1 = searchItem1.replace('*', ' ')
            searchItem2 = searchItem2.replace('*', ' ')
            searchItem3 = searchItem3.replace('*', ' ')
            for i in anchorlist:
                if i.text.strip() == searchItem1:
                    print("contact1 found")
                    found1 = 1
                elif i.text.strip() == searchItem2:
                    print("contact2 found")
                    found2 = 1
                elif i.text.strip() == searchItem3:
                    print("contact3 found")
                    found3 = 1
                    time.sleep(1)
            if not (found1 and found2 and found3):
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "verify_system_directory - Couldn't find the contact in system directory")
                raise
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_system_directory- unable to verify the system directory" + str(
                                      sys.exc_info()))
            return False

    def show_verify_contactCard(self, **params):
        '''
           author : kiran
           show_verify_contactCard() - this API verifies the contact card name(in favorite list/system directory/recent list) from third panel contact name. and make call according to API
           ex1: show_verify_contactCard
           parameter: mode, contact
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "show_verify_contactCard- show/verify contact card from system directory whole contact which coming in first list")
            if params["mode"] == "Sdirectory":
                status = self.defaultPanel.verify_contactCard_from_systemDirectory(params)
                # if status is False:
                #    raise
            elif params["mode"] == "favList":
                status = self.peopleGroup.verify_contactCard_from_favoriteList(params)
                if status is False:
                    raise
            elif params["mode"] == "CallDashboard":
                status = self.peopleGroup.verify_contactCard_from_CallDashboard(params)
                if status is False:
                    raise
            elif params["mode"] == "GrpContact":
                status = self.peopleGroup.verify_contactCard_from_GrpContact(params)
                if status is False:
                    raise
            else:
                print("invalid parameter mode passed")
                raise
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "show_verify_contactCard- successfully verify/clicked the contactcard/call option")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "show_verify_contactCard- failed to verify contact name" + str(sys.exc_info()))
            return False

    def drag_the_call_and_Hover(self, **params):
        '''
           Author: kiran
           drag_the_call_and_Hover() -  this API drags the call to the directory searched contact/favorite contact/group contact etc
           parameters: searchItem, callName, mode
           ex: drag_the_call_and_Hover searchItem=user2 callName=user5 mode=In_call
        '''
        try:
            self.defaultPanel.click_and_Hold_the_Call(params)
            if params["option"] == "In_call":
                self.defaultPanel.HoverToContact_InCall(params)
            elif params["option"] == "IncomingCall":
                self.defaultPanel.HoverToContact_IncomingCall(params)
            elif params["option"] == "Outgoing_call":
                self.defaultPanel.HoverToContact_OutGoingCall(params)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "drag_the_call_and_Hover - unable to drags the call to directory " + str(
                                      sys.exc_info()))
            return False

    def transfer_call_via_contexualMenu(self, **params):
        '''
           Author: kiran
           transfer_call_via_contexualMenu() -  this API transfers the call to third user as blind/blind conference/park/whisper transfer etc.
           parameters: option
        '''
        try:
            if params["option"] == "BlindTrans":
                self.defaultPanel.BlindTransfer_from_contexualMenu()
            elif params["option"] == "BlindConf":
                self.defaultPanel.BlindConf_from_contexualMenu()
            elif params["option"] == "ConsultTrans":
                self.defaultPanel.ConsultTrans_from_contexualMenu()
            elif params["option"] == "InterCom":
                self.defaultPanel.InterCom_from_contexualMenu()
            elif params["option"] == "InterComConf":
                self.defaultPanel.InterCom_conference_from_contexualMenu()
            elif params["option"] == "Park_and_Intercom":
                self.defaultPanel.park_and_InterCom_from_contexualMenu()
            elif params["option"] == "Park":
                self.defaultPanel.Park_from_contexualMenu()
            elif params["option"] == "WhisperT":
                self.defaultPanel.WhisperT_from_contexualMenu()
            elif params["option"] == "ConsltConf":
                self.defaultPanel.ConsltConf_from_contexualMenu()
            elif params["option"] == "MailBoxT":
                self.defaultPanel.MailBoxTransfer_from_contexualMenu()
            elif params["option"] == "VerifyContextualMenu":
                self.defaultPanel.Verify_contextual_Menu(params["is_present"])
                if "moveMouse" in params.keys():
                    self.webAction.mouse_hover("first_panel_Event_draft_convr")
                    time.sleep(2)
                    self.webAction.click_element("first_panel_Event_draft_convr")
                    time.sleep(3)
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "transfer_call_via_contexualMenu-""blind transfer from contextual menu is successfull")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "transfer_call_via_contexualMenu- unable to drags the call to directory" + str(
                                      sys.exc_info()))
            return False

    def verify_holdCall_and_consultCall(self, **params):
        '''
           author : kiran
           verify_holdCall_and_consultCall() - this API verifies/clicks the transfer option in consult call.
           ex1: verify_holdCall_and_consultCall
           parameters: WContact, CContact
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_holdCall_and_consultCall- verify holdCall and consultCall attributes")
            call_on_hold = self._browser.element_finder("consult_call_top_call")
            call_on_hold_hold_text = self.queryElement.get_text("FP_consult_call_top_call_hold_text")
            if ('consult_conference_completed' in params) and (params["consult_conference_completed"] == "no"):
                call_consulting = self._browser.element_finder("FP_consult_conference_initiated")
                call_consulting_consult_text = self.queryElement.get_text("FP_consult_conference_initiated_text")
            else :
                call_consulting = self._browser.element_finder("consult_call_second_call")
                call_consulting_consult_text = self.queryElement.get_text("FP_consult_call_second_call_consult_text")
            
            HoldContact = params["HoldContact"].replace("*", ' ')
            if HoldContact in call_on_hold.text and "Hold" in call_on_hold_hold_text:
                if "WContact" in params.keys():
                    whisper_contact = params["WContact"].replace("*", ' ')
                    if whisper_contact in call_consulting.text and "Whisper Page" in call_consulting_consult_text:
                        TPContact = self.queryElement.get_text("third_panel_new_contact")
                        if TPContact == whisper_contact:
                            log.mjLog.LogReporter("ManhattanComponent", "info",
                                                  "verify_holdCall_and_consultCall - successfully verify/clicked the transfer consultCall option")
                        else:
                            raise
                    else:
                        raise
                elif "CContact" in params.keys():
                    Con_contact = params["CContact"].replace("*", ' ')
                    if Con_contact in call_consulting.text and "Consulting" in call_consulting_consult_text:
                        TPContact = self.queryElement.get_text("third_panel_new_contact")
                        if TPContact == Con_contact:
                            log.mjLog.LogReporter("ManhattanComponent", "info",
                                                  "verify_holdCall_and_consultCall - successfully verify/clicked the transfer consultCall option")
                        else:
                            raise
                elif "IntContact" in params.keys():
                    Con_contact = params["IntContact"].replace("*", ' ')
                    if Con_contact in call_consulting.text and "Consulting" in call_consulting_consult_text:
                        TPContact = self.queryElement.get_text("third_panel_new_contact")
                        if TPContact == Con_contact:
                            log.mjLog.LogReporter("ManhattanComponent", "info",
                                                  "verify_holdCall_and_consultCall - successfully verify/clicked the transfer consultCall option")
                        else:
                            raise
                    else:
                        raise
                else:
                    raise
            else:
                raise
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_holdCall_and_consultCall"
                                                                 " - failed to verify holdCall and consultCall"
                                                                 " attributes" + str(sys.exc_info()))
            return False

    def consult_trans_or_conf_Call(self, **params):
        '''
           author : kiran
           consult_trans_or_conf_Call() - this API verify the orange border of call dashboard and verifies/clicks the transfer option in consult call.
           parameters: consult
           ex1: consult_trans_or_conf_Call option=conference/complete_transfer
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "consult_trans_or_conf_Call- verify/click option")
            time.sleep(2)
            rgb = self._browser.element_finder("default_consultCalls").value_of_css_property("background-color")
            print("rgb : ", rgb)
            r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
            hex_color = '#%02x%02x%02x' % (r, g, b)
            print(hex_color)
            if "#F39300" in hex_color:
                print("consult conference call border color has been checked", hex_color)
                # else:
                # return False
            if params["option"] == "no_green_icon":
                if (self.queryElement.element_not_displayed("default_complete_conference")):
                    print("green merge icon is not present")
                else:
                    raise
            elif params["option"] == "conference":
                self.assertElement.element_should_be_displayed("default_complete_conference")
                self.webAction.click_element("default_complete_conference")
            else:
                self.assertElement.element_should_be_displayed("FP_transfer_confCall")
                self.webAction.click_element("FP_transfer_confCall")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "consult_trans_or_conf_Call- successfully verify/clicked the transfer consultCall option")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "consult_trans_or_conf_Call- failed to check all tabs availabel in dashboard" + str(
                                      sys.exc_info()))
            return False

    def blind_transfer_from_search_item_to_incoming_call(self, **params):
        """
        Author: kiran
        blind_transfer_from_search_item_to_incoming_call() - This API transfers the call by draging the search item and droping it to incomming call
        Parameter: searchItem, option
        Ex: blind_transfer_from_search_item_to_incoming_call searchIte=user1 option=incoming_call/voiceMailCall/parked_call
        """
        try:
            name = params["searchItem"]
            self.defaultPanel.search_people_or_extension(name)
            contactlist = self._browser.elements_finder("SP_anchor_contact")
            self.webAction.mouse_hover("SP_anchor_contact")
            for i in contactlist:
                if name in i.text:
                    ActionChains(self._browser.get_current_browser()).click_and_hold(i).perform()
                    if params["option"] == "incoming_call":
                        self.defaultPanel.blind_transfer_from_search_item_to_incomingCall(params)
                    if params["option"] == "ConfCall":
                        self.defaultPanel.blind_transfer_from_search_item_to_ConfCall(params)
                    elif params["option"] == "parked_call":
                        self.defaultPanel.blind_transfer_from_search_item_to_ParkedCall(params)
                    elif params["option"] == "voiceMailCall":
                        self.defaultPanel.blind_transfer_from_search_item_to_VMCall(params)
                    elif params["option"] == "IM_notific":
                        self.defaultPanel.blind_transfer_from_search_item_to_IM_notific(params)
                    elif params["option"] == "GRP_DRAFT":
                        self.defaultPanel.blind_transfer_from_search_item_to_GRP_DRAFT(params)
                    elif params["option"] == "EVNT_NOTIF":
                        self.defaultPanel.blind_transfer_from_search_item_to_EVNT_NOTIF(params)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "blind_transfer_from_search_item_to_incoming_call - failed"
                                  " to perform expected operation " + str(sys.exc_info()))
            return False

    def check_created_group(self, **params):
        '''
           Author : kiran
           check_created_group() - Verifies the test case by checking the group name which we passed is same as given by xpath
           parameters : searchItem1
           Ex : check_created_group searchItem1 = groupA
        '''
        try:
            # appending the groupNames passed as a parameter in a list
            if "groupName1" in params.keys():
                grouplist = []
                for key in params.keys():
                    if "groupName" in key:
                        grouplist.append(params[key])
                status = self.createGroupclass.verify_groups_name(grouplist)
                if status is False:
                    raise
            # appending the contacts passed as a parameter in a list
            if "contact1" in params.keys():
                contactlist = []
                for key in params.keys():
                    if "contact" in key:
                        split_name = params[key].split("*")
                        contactName = " ".join(split_name)
                        contactlist.append(contactName)
                status = self.createGroupclass.verify_groupMembers_name(contactlist)
                if status is False:
                    raise
                    # if group list is empty then verifying the group list length
            if "empty" in params.keys():
                grplist = self._browser.elements_finder("peoples_first_group")
                if len(grplist) == 0:
                    log.mjLog.LogReporter("ManhattanComponent", "error", "check_created_group - empty group list found")
                else:
                    raise AssertionError("group list should be empty but there 1 or more group are found")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_created_group - the groups name and member has been verified successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_created_group"
                                                                 " - Error in searching persons " + str(sys.exc_info()))
            raise

    def select_people_view(self, **params):
        '''
           select_people_view() - this API invokes from Big A to small a or vice versa
           Author : kiran
           Modified By: Indresh
           parameters : option
           ex : select_people_view option=smallA/BigA
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "select_people_view - shifting from big A to small a or vice versa")
            # checks the list view and select the compact view
            if params["option"] == "compact":
                self.defaultPanel.select_people_view_compact()
                # checks the compact view and select the list view
            elif params["option"] == "list":
                self.defaultPanel.select_people_view_list()
            else:
                print("invalid parameter passed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "select_people_view - "
                                                                 "peopleList" + str(sys.exc_info()))
            return False

    def transfer_call_by_dragNdrop_cantact_to_inCall(self, **params):
        '''
           Author : kiran
           transfer_call_by_dragNdrop_favContact_to_inCall() - this API, transfers the call by draging the favorite contact and transfer it to in call option
           parameters : searchItem
           ex : transfer_call_by_dragNdrop_favContact_to_inCall favContact=user1
        '''
        try:
            if params["option"] == "search_item":
                self.defaultPanel.search_people_or_extension(params["searchItem"])
                self.defaultPanel.transfer_call_by_dragNdrop_searchContact_to_inCall(params)
            elif params["option"] == "fav_contact":
                self.defaultPanel.transfer_call_by_dragNdrop_favCon_to_inCall(params)
            elif params["option"] == "group_contact":
                self.defaultPanel.transfer_call_by_dragNdrop_grpCon_to_inCall(params)
            elif params["option"] == "group_name":
                self.defaultPanel.transfer_call_by_dragNdrop_grpName_to_inCall(params)
            if "release" in params.keys():
                self.source_ele = self._browser.element_finder("default_OutG_CallName")
                ActionChains(self._browser.get_current_browser()).release(self.source_ele).perform()

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "transfer_call_by_dragNdrop_favContact_to_inCall - failed to drag and transfer call " + str(
                                      sys.exc_info()))
            return False

    def verify_whisperPage_and_SimpleCall(self, **params):
        '''
           author : kiran
           verify_whisperPage_and_SimpleCall() - this API verifies/clicks the transfer option in consult call/whisper page call.
           ex1: verify_whisperPage_and_SimpleCall
           parameters: InCall, WContact
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_whisperPage_and_SimpleCall- verify whisper page call which not including greeny button and another call is simple call")
            callList = self._browser.elements_finder("default_callDashboard")
            for j in callList:
                spl = j.text.split()
                if "WContact" in params.keys():
                    if spl[0] == params["WContact"] and spl[2] == "Whisper" and spl[3] == "Page":
                        TPContact = self.queryElement.get_text("third_panel_new_contact")
                        if TPContact == params["WContact"]:
                            print("second call is on whisper page by default whisper page call contact card is opened")
                        # checking whether green icon is present or not
                        if self.queryElement.element_not_displayed("default_recieve_call"):
                            print("greeny icon is not present")
                        else:
                            raise AssertionError(
                                "greeny icon should not present but it is displayed as we not expect this here")
                            return False
                elif "InCall" in params.keys():
                    if spl[4] == params["InCall"]:
                        TPContact = self.queryElement.get_text("third_panel_new_contact")
                        if TPContact == params["InCall"]:
                            print("second call is on incall by default consult call contact card is opened")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_whisperPage_and_SimpleCall- successfully verify/clicked the transfer consultCall option")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_whisperPage_and_SimpleCall- failed to verify holdCall and consultCall attributes" + str(
                                      sys.exc_info()))
            return False

    def verify_park_call_in_client(self, **params):
        """
        Author: Manoj
        verify_park_call_in_client() - To verify park text in user name
        Ex: verify_park_call_in_client
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_park_call_in_client-  Going to verifying park calling")
            if params["option"] == "park":
                # xplicit wait added by kiran
                self.webAction.explicit_wait("default_client_pane_timer")
                Parked_text = self.queryElement.get_text("default_client_pane_timer")
                print("value from text box : ", Parked_text)
                if 'Park' in Parked_text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_park_call_in_client- successful in verifying the put on hold calling")
                    self.webAction.click_element("third_panel_transfer_park_answer")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_park_call_in_client- Failed in verifying the put on hold calling" + str(
                                              sys.exc_info()))
            elif params["option"] == "no_park":
                Parked_text = self.queryElement.get_text("default_client_pane_timer")
                print("value from text box : ", Parked_text)
                if 'Park' not in Parked_text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_park_call_in_client- successful in verifying the put on hold calling")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_park_call_in_client- Failed in verifying the put on hold calling" + str(
                                              sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_park_call_in_client- Failed to verifying park calling" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_park_call_in_client - failed")

    def Verifying_third_panel_tab(self, **params):
        """
        Author : Surendra
        Verifying_third_panel_tab() - This API will verify third panel info
        parameter: message
        ex: Verifying_third_panel_tab
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Verifying_third_panel_tab - verifying third panl info ")
            if params["entity"] == "thirdpanel":
                self.assertElement.page_should_contain_element("TP_info")
                self.assertElement.page_should_contain_element("third_panel_answer_call")
                self.assertElement.page_should_contain_element("default_people_contects_delete")
            log.mjLog.LogReporter("ManhattanComponent", "info", "Verifying_third_panel_tab - verified required tabs")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "Verifying_third_panel_tab - failed to sent IM" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error Verifying_third_panel_tab - failed")

    def Sorted_list_Lastname_dashboard(self, **params):
        '''
          SortedLastname_dashboard() - sorted a last name
          ex:   user_db1_2 user ,uma shankar
              it should be like this shankar , user
         '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Sorted_Lastname_dashboard - display all person in sorted by last name")
            time.sleep(2)
            self.defaultPanel.invoke_peoplelist()
            self.webAction.click_element("default_name_number_search")
            self.webAction.input_text("default_search_input", params["last_name"])
            time.sleep(2)
            last_name_list = self._browser.elements_finder("search_peoplel_list")
            for i in last_name_list:
                if len(last_name_list) > 10:
                    last_name = i.text.split("\n")[0].rstrip(" ")
                    if last_name.startswith("U"):
                        self.webAction.scroll("peoples_vertical_scroll_bar_id", 0)
                        self.webAction.press_key("default_close_direct_search", "ESCAPE")
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "%s is displaying" % last_name)
                    else:
                        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Not Verified properly")
                else:
                    print("************************************************** length condition is not verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Error while click_user_profile" + str(sys.exc_info()))
            return False

    def delete_user_forwardcall(self, **params):
        """
        Author: Prashanth
        delete the selected user from forward call
        """
        try:
            time.sleep(4)
            list_cross_button = self._browser.elements_finder("preference_account_access_remove_user")
            for del_button in list_cross_button:
                del_button.click()
                time.sleep(3)
            log.mjLog.LogReporter("ManhattanComponent", "info", "delete_user_forwardcall"
                                                                " -" "user selected is deleted from selection")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "delete_user_forwardcall"
                                                                 " - Failed to delete user from selection " + str(
                sys.exc_info()))
            return False

    def place_blind_conf_call(self, **params):
        '''
           Author: Iswarya
           place_blind_conf_call() - To place blind conference call
           ex:place_blind_conf_call user=userC
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "place_blind_conf_call- Clicking on blind conference call button")
            self.peopleGroup.blind_audio_conference(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "place_blind_conf_call- Call blind transfered")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "place_blind_conf_call- Failed to click blind conf call button" + str(sys.exc_info()))
            return False

    def Click_verify_recent_conf_call(self):
        """
        Click_verify_recent_conf_call() - This method verifies the number of user in recent conference call
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Click_verify_recent_conf_call - Start verification on conference call")
            senderList = self._browser.elements_finder("recent_conf_calls")
            print(senderList)
            senderList[0].click()
            time.sleep(3)
            senderList1 = self._browser.elements_finder("recent_conf_calls_list")
            if len(senderList1) == 2:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "Click_verify_recent_conf_call - sucessfully verified confernce call")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "Click_verify_recent_conf_call - Unable to verify confernce call")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "Click_verify_recent_conf_call - Unable to verify confernce call " + str(
                                      sys.exc_info()))
            raise Exception("Click_verify_recent_conf_call - Unable to verify confernce call ")

    def play_unread_voicemails_via_phone(self):
        '''
        Author : Iswarya
        play_unread_voicemails_via_phone
        '''
        try:
            # self.webAction.click_element("vm_all_tab")
            unread_vm = self._browser.elements_finder("vm_unread")
            for vm in unread_vm:
                vm.click()
                break
            else:
                raise AssertionError("Either xpath 'vm_unread' is incorrect or No unheard voicemail is there!")
            time.sleep(2)
            log.mjLog.LogReporter("People_Group", "info", "play_unread_voicemails_via_phone - opened unread voicemail")
            phone_buttons = self._browser.elements_finder("vm_play_through_phone")
            play_buttons = self._browser.elements_finder("vm_play_button")
            time.sleep(2)  # wait for buttons to become clickable
            for ph_button in phone_buttons:
                for play_button in play_buttons:
                    ph_button.click()
                    time.sleep(2)
                    play_button.click()
                    time.sleep(5)
                    if self.queryElement.element_not_displayed("recent_voicemail_pause"):
                        continue
                    else:
                        time.sleep(2)
            log.mjLog.LogReporter("People_Group", "info",
                                  "play_unread_voicemails_via_phone - voicemail played via phone")
        except:
            log.mjLog.LogReporter("People_Group", "error", "play_unread_voicemails_via_phone " + str(sys.exc_info()))
            raise

    def reply_forward_voicemail(self, **params):
        """
        Author: Uttam
        reply_forward_voicemail() - This API forwards voicemail to recipients
        Parameters: recipient and subject
        Ex1: reply_forward_voicemail recipient1=abc subject=fwd
        Ex2: reply_forward_voicemail recipient1=abc recipient2=cgc subject=fwd
        Ex3: reply_forward_voicemail subject=fwd/default recording_device=phone/computer vm_type=all/urgent/private/receipt/none
        """
        try:
            if params["option"] == "reply":
                self.voicemail.reply_voicemail(params)
                log.mjLog.LogReporter("ManhattanComponent", "info", "reply_forward_voicemail - "
                                                                    "Replied with Voicemail")
            else:
                recipientlist = []
                for key in params.keys():
                    if "recipient" in key:
                        recipientlist.append(re.sub("\*", " ", params[key]))
                self.voicemail.forward_voicemail(recipientlist, params)

                log.mjLog.LogReporter("ManhattanComponent", "info", "reply_forward_voicemail - "
                                                                    "Voicemail forwarded")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "reply_forward_voicemail - "
                                                                 "failed to either reply or forward voicemail " + str(
                sys.exc_info()))
            raise

    def select_play_delete_recent_voicemail(self, **params):
        '''
           Author: Manoj modified by Uttam
           select_play_delete_recent_voicemail() - clicks on recent voice mail,plays,delete the recent voice mail
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "select_play_delete_recent_voicemail "
                                                                "- clicks on recent voice mail,plays,delete the recent voice mail")

            self.webAction.click_element("voicemail_all_tab")
            time.sleep(3)
            senderList = self._browser.elements_finder("recent_vm_sender_unread")
            print(senderList)
            print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,3")
            senderList[0].click()
            # for i in senderList:
            # if params["sender"] in i.text:
            # i.click()
            # time.sleep(3)
            self.webAction.click_element("recent_voicemail_play")
            time.sleep(10)
            self.assertElement.page_should_contain_element("recent_VM_reply")
            self.assertElement.page_should_contain_element("recent_VM_forward")
            self.assertElement.page_should_contain_element("recent_VM_deletion")
            print(",,,,,,,,,,,,,,all 3 options hasbeen checked,,,,,,,,,,,,,,4")
            if "option" in params.keys() and params["option"] == "delete":
                self.webAction.click_element("recent_voicemails_delete")

            log.mjLog.LogReporter("ManhattanComponent", "info", "select_play_delete_recent_voicemail -"
                                                                " success in clicking on recent voice mail,plays,delete the recent voice mail")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "select_play_delete_recent_voicemail -"
                                                                 " Failed to clicks on recent voice mail, plays, delete the recent"
                                                                 " voice mail" + str(sys.exc_info()))
            return False

    def delete_voicemails(self, **params):
        """
        Author: Uttam
        delete_voicemails() - This API deletes read or unread VMs
        Parameters: type and sender
        Ex: delete_voicemails type=read/unread sender=UserA
        """
        try:
            if params["type"] == "read":
                self.voicemail.delete_read_vm(params["sender"])
            else:
                self.voicemail.delete_unread_vm(params["sender"])

            log.mjLog.LogReporter("ManhattanComponent", "info", "delete_voicemails - "
                                                                "%s is deleted" % (params["type"]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "delete_voicemails - "
                                                                 "failed to delete voicemail" + str(sys.exc_info()))
            raise

    def restore_voicemail_recent(self, **params):
        '''
           author : kiran
           restore_voicemail_recent():restore the voicemail
        '''
        try:
            self.assertElement.element_should_be_displayed("voicemail_deleted_dropdown")
            self.webAction.click_element("voicemail_deleted_dropdown")
            if params["option"] == "none":
                deList1 = self._browser.elements_finder("sender_name_list")
                if len(deList1) >= 1:
                    print("there is 1 or more deleted vm present")
                else:
                    print(" there is no any deleted vm present.....")
            elif params["option"] == "check":
                deList = self._browser.elements_finder("sender_name_list")
                for i in deList:
                    if params["sender"] in i.text:
                        i.click()
                if params["choice"] == "verify":
                    self.assertElement.element_should_be_displayed("recent_vm_restore")
                    print("restore option showing.......")
                elif params["choice"] == "restore":
                    self.assertElement.element_should_be_displayed("recent_vm_restore")
                    self.webAction.click_element("recent_vm_restore")

            self.webAction.click_element("voicemail_deleted_dropdown")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "contact_card_verify_notification- Failed to dispaly the contact card " + str(
                                      sys.exc_info()))
            return False

    def check_restored_vm(self, **params):
        '''
            author: kiran
        '''
        try:
            senderList = self._browser.elements_finder("recent_vm_sender_unread")
            print(senderList)
            leng = len(senderList) - 1
            for i in range(leng):
                if params["sender"] in senderList[leng].text:
                    print("test case passed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_restored_vm- Failed to dispaly the contact card " + str(sys.exc_info()))
            return False

    def restore_voicemail(self, **params):
        """
        Author: Prashanth
        restore_vm - This API restores the deleted voicemails
        Parameters: sender
        Ex: restore_vm sender=USERTest
        """
        try:
            self.webAction.explicit_wait("vm_deleted_vms")
            # putting timeout of 1 second to prevent stale reference exception
            time.sleep(1)
            self.webAction.click_element("vm_deleted_vms")

            self.webAction.click_element("vm_recent_deleted_voicemail")
            
            self.webAction.click_element("vm_restore")
            time.sleep(2)
            self.assertElement.element_should_not_be_displayed("vm_restore")
            log.mjLog.LogReporter("ManhattanComponent", "info", "restore_voicemail - "
                                  "%s voicemail is restored" % (params["type"]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "restore_voicemail - "
                                  "failed to restore voicemail" + str(sys.exc_info()))
            raise

    def save_unsave_voicemail(self, **params):
        """
        Author: prashanth
        save_unsave_voicemail() - Right click over voicemail & select flag or unflag voice mail
        Parameters: option, vm_to_save and sender
        Ex: save_unsave_voicemail option=save/unsave vm_to_save=heard/unheard sender=abc
        """
        try:
            sender = params["sender"].lstrip("{").rstrip("}")
            if params["option"] == "save":
                self.voicemail.save_vm(sender, params["vm_to_save"])
            else:
                self.voicemail.unsave_vm(sender, params["vm_to_save"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "save_unsave_voicemail - Error " + str(sys.exc_info()))
            return False

    def send_group_vm(self, **params):
        """
        Author: Uttam
        send_group_vm() - To send the group voicemail or cancel
        Parameters: option and subject
        Ex: send_group_vm option=send recording_device=computer/phone subject=Group*Voicemailvm_type=all/urgent/private/receipt/none
        """
        try:
            self.thirdPanel.send_cancel_group_vm(params)
            if params["option"] == "send":
                log.mjLog.LogReporter("ManhattanComponent", "info", "send_group_vm"
                                                                    " - Group VM send")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "send_group_vm"
                                                                    " - Group VM cancelled")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "send_group_vm"
                                                                 " - Failed to send group VM " + str(sys.exc_info()))
            return False

    def verify_hold_consult_in_conf_call(self, **params):
        """
        verify_hold_consult_in_conf_call() - This method clicks on end or hold call button in client pane of the user
        change List: added elif params["option"] == "complete_consult" (UKumar: 15-Dec-2016)
        """
        try:
            log.mjLog.LogReporter("PeopleGroup", "info",
                                  "verify_hold_consult_in_conf_call - Clicked on end call successfully")
            if params["option"] == "on_hold":
                whisperpage_text = self.queryElement.get_text('TP_conf_transfer_time')
                if 'On Hold' in whisperpage_text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_hold_consult_in_conf_call - success in verifying Whisper_page in calling")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_hold_consult_in_conf_call - failed in verifying Whisper_page in calling")
            elif params["option"] == "consulting":
                whisperpage_text = self.queryElement.get_text('Tp_whisper_page')
                if 'Consulting...' in whisperpage_text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_hold_consult_in_conf_call - success in verifying Consulting")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_hold_consult_in_conf_call - Consulting text is not present")
            elif params["option"] == "Merge":
                self.webAction.click_element("TP_conf_transfer_join")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_hold_consult_in_conf_call - Clicked on merge button to complete consult")
            elif params["option"] == "complete_consult":
                self.webAction.click_element("TP_complete_consult_transfer")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_hold_consult_in_conf_call - Clicked on transfer button to complete consult")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "verify_hold_consult_in_conf_call - Failed to click on call button " + str(
                                      sys.exc_info()))
            return False

    def verify_users_in_a_dashboard_in_call(self, **params):
        """
        Author: Manoj
        verify_users_in_a_dashboard_in_call() - To verify park text in user name
        Parameters: option and user
        Ex: verify_users_in_a_dashboard_in_call option=one_user user=abc
            verify_users_in_a_dashboard_in_call option=two_users user1=abc user2=xyz
            verify_users_in_a_dashboard_in_call option=three_users user1=abc user2=xyz user3=lmn
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                " -  Going to verifying dashboard users")
            if params["option"] == "one_user":
                user = self.queryElement.get_text("FP_single_user_in_call")
                if params["user"] in user:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                        " - success in verifying dashboard users")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                        " - user not present in dashboard")
            elif params["option"] == "two_users":
                self.webAction.click_element("default_clicktogglecall") # click on drown arrow to show participants list
                users = self._browser.elements_finder("default_call_users")
                for i in users:
                    self.user1 = params["user1"]
                    self.user2 = params["user2"]
                    if (params["user1"] in i.text) or (params["user2"] in i.text):
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - success in verifying dashboard users")
                    else:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - user not present in dashboard")
                self.webAction.click_element("default_clicktogglecall") # click on drown arrow to hide participants list
            elif params["option"] == "three_users":
                self.webAction.click_element("default_clicktogglecall") # click on drown arrow to show participants list
                users = self._browser.elements_finder("default_call_users")
                for i in users:
                    self.user1 = params["user1"]
                    self.user2 = params["user2"]
                    self.user3 = params["user3"]
                    if params["user1"] or params["user2"] or params["user3"] in i.text:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - success in verifying dashboard users")
                    else:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - user not present in dashboard")
                self.webAction.click_element("default_clicktogglecall") # click on drown arrow to hide participants list
        except:
            try:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                    " -  Going to verifying dashboard users Second Time")
                if params["option"] == "one_user":
                    user = self.queryElement.get_text("FP_single_user_in_call")
                    if params["user"] in user:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - success in verifying dashboard users")
                    else:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - user not present in dashboard")
                elif params["option"] == "two_users":
                    self.webAction.click_element("default_clicktogglecall")
                    users = self._browser.elements_finder("default_call_users")
                    for i in users:
                        self.user1 = params["user1"]
                        self.user2 = params["user2"]
                        if (params["user1"] in i.text) or (params["user2"] in i.text):
                            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                                " - success in verifying dashboard users")
                        else:
                            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                            " - user not present in dashboard")
                    self.webAction.click_element("default_clicktogglecall")
                elif params["option"] == "three_users":
                    self.webAction.click_element("default_clicktogglecall")
                    users = self._browser.elements_finder("default_call_users")
                    for i in users:
                        self.user1 = params["user1"]
                        self.user2 = params["user2"]
                        self.user3 = params["user3"]
                        if params["user1"] or params["user2"] or params["user3"] in i.text:
                            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                                " - success in verifying dashboard users")
                        else:
                            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_in_a_dashboard_in_call"
                                                                                " - user not present in dashboard")
                    self.webAction.click_element("default_clicktogglecall")
            except:
                log.mjLog.LogReporter("ManhattanComponent", "error", "verify_users_in_a_dashboard_in_call"
                                                                     " - Failed to verify dashboard users " + str(
                    sys.exc_info()))
                raise Exception("ManhattanComponent error verify_users_in_a_dashboard_in_call - failed")

    def open_new_event(self):
        '''
           Author: Gautham
           open_new_event() - Create a new event from events tab, opens third panel
                                for creating an event
           ex: open_new_event

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_new_event - Opening event panel")
            if not self.queryElement.element_not_displayed("TP_Close"):
                self.webAction.click_element("TP_Close")
                self.webAction.click_element("event_discard_yes")
            self.event.click_new_event()
            time.sleep(2)
            self.assertElement.element_should_be_displayed("events_third_panel")
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_new_event - Events panel opened successfully ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "open_new_event - Failed to open Events panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_new_event - failed")

    def events_add_meeting_details(self, **params):
        '''
        Author: Gautham
        events_add_meeting_details() - This method set meeting title
        ex: events_add_meeting_details name=test
        change List: added set_meeting_time() method (UKumar:09_Dec-2016)
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", " events_add_meeting_details- Adding meeting details")
            for key in params.keys():
                if "name" in key:
                    self.event.set_meeting_title(params["name"])
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "events_add_meeting_details- Meeting title added successfully")
                elif "date" in key:
                    self.event.set_calendar_date(params["date"])
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "events_add_meeting_details- Date selected successfully")
                elif "time" in key:
                    new_time_entered = self.event.set_meeting_time(params["time"])
                    actual_new_time = self.queryElement.get_value("TP_get_time")
                    # print("entered value",new_time_entered, actual_new_time)
                    # self.assertElement.values_should_be_equal(new_time_entered, actual_new_time)
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "events_add_meeting_details - Time entered successfully")
                elif "replace" in key:
                    self.webAction.click_element("events_time")
                    self.webAction.focus("events_time")
                    self.webAction.input_text_basic("events_meeting_title", "0420")
                elif "duration" in key:
                   self.event.set_event_duration(int(params["duration"]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "events_add_meeting_details"
                                                                 " - Failed to add meeting details" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error events_add_meeting_details - failed")

    def events_select_meeting_type(self, **params):
        '''
           Author: Gautham
           events_select_meeting_type() - Select a meeting type (Collaborative or Custom)
           parameters: option
           ex: events_select_meeting_type option=collaborative
           ex: events_select_meeting_type option=custom

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "events_select_meeting_type- Selecting meeting type")
            if params["option"] == "collaborative":
                self.assertElement.element_should_be_displayed("events_organisers")
                self.assertElement.element_should_be_displayed("events_presenters")
            elif params["option"] == "custom":
                self.webAction.click_element("event_show_participant")
                self.assertElement.element_should_be_displayed("events_organisers")
                self.assertElement.element_should_be_displayed("events_presenters")
                self.webAction.explicit_wait("events_participants")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "events_select_meeting_type- Meeting type is selected successfully")
            else:
                raise AssertionError("Wrong arguments passed !!!")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "events_select_meeting_type- Failed to select meeting type" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error events_select_meeting_type - failed")

    def events_meeting_type_add_user(self, **params):
        '''
           Author: Gautham
           events_meeting_type_add_user() - Add users to organizers or presenters or participants
           parameters: option: organizers or presenters or participants
                       username: 1 user to be added
           ex: events_meeting_type_add_user option=organizers username=userA

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "events_meeting_type_add_user- Adding users to meeting type ")
            if params["option"] == "organizers":
                self.event.add_user_organizers(re.sub("\*", " ", params["username"]))
            elif params["option"] == "presenters":
                for key in params.keys():
                    if "user" in key:
                        self.event.add_user_presenters(re.sub("\*", " ", params[key]))
            elif params["option"] == "participants":
                self.event.add_user_participants(params)
            else:
                raise AssertionError("Wrong arguments passed !!!")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "events_meeting_type_add_user- Users added to meeting type successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "events_meeting_type_add_user- Failed to add users to meeting type" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error events_meeting_type_add_user - failed")
            
    def events_change_meeting_settings(self, **params):
        '''
        Author: Gautham
        events_change_meeting_settings() - Expand or hide meeting settings option
        parameters: option: hide - hide meeting settings option
                    option: show - expand meeting settings option
        ex: events_change_meeting_settings option=hide
        ex: events_change_meeting_settings option=show
        Change list: Added assertion and moved helper APIs from PeopleGroup to Events page (UKumar: 12-April-2017)
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "events_show_meeting_settings"
                                                                " - Changing events meeting settings")
            self.event.toggle_more_settings()
            if params["option"] == "hide":
                self.assertElement.element_should_be_displayed("events_more_settings_arrow_down")
                log.mjLog.LogReporter("ManhattanComponent", "info", "events_show_meeting_settings"
                                                                    " - Meeting Settings are hidden")
            elif params["option"] == "show":
                self.assertElement.element_should_be_displayed("events_more_settings_arrow_up")
                log.mjLog.LogReporter("ManhattanComponent", "info", "events_show_meeting_settings"
                                                                    " - Showing Meeting Settings")
            else:
                raise AssertionError("wrong arguments passed !!")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "events_show_meeting_settings"
                                                                 " - Failed to change Meeting Settings " + str(
                sys.exc_info()))
            return False

    def events_create_invite(self):
        '''
           Author: Gautham
           events_create_invite() - This method clicks on create event invite and
                                    checks if event is created or not
           ex: events_create_invite event=test

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", " events_create_invite- Creating event invite")
            self.event.click_create_event_invite()
            # self.webAction.explicit_wait("events_name_second_panel")
            # self.peopleGroup.check_event_second_panel(params["event"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "events_create_invite- Event created successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "events_create_invite - Failed to create event" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error events_create_invite - failed")

    def create_event(self, **params):
        """
        create_event() - Creates an event if event not found
        Ex: create_event name events_select_meeting_type_option events_meeting_type_add_user_option username1 username2 events_change_meeting_settings_option
            configure_meeting_settings_option join_audio  send_meeting_request_outlook_option meeting_name
        """
        try:
            event_found = get_event(self, params)
            if event_found == "no":
                self.open_new_event()
                self.events_add_meeting_details(**{name: params["name"]})
                self.events_select_meeting_type(**{option : params["events_select_meeting_type_option"]})
                time.sleep(1)
                self.events_meeting_type_add_user(**{option : params["events_meeting_type_add_user_option"], username1: params["username1"], username2: params["username2"]})
                self.events_change_meeting_settings(**{option: params["events_change_meeting_settings_option"]})
                self.configure_meeting_settings(**{option: params["configure_meeting_settings_option"], join_audio: params["join_audio"]})
                self.events_create_invite()
                time.sleep(12)
                self.send_meeting_request_outlook(**{option: params["send_meeting_request_outlook_option"], meeting_name: params["meeting_name"]})
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "create_event - Failed to find any event" + str(sys.exc_info()))
            raise

    def get_event(self, **params):
        """
        Author: UKumar
        get_event() - Returns yes if given event found under Upcoming tab otherwise returns no
        Parameters: event_name
        Ex: get_event event_name
        """
        try:
            event_found = self.event.get_upcoming_event(params["event_name"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "get_event - Event found : %s" % event_found)
            return event_found
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "get_event - Failed to find any event" + str(sys.exc_info()))
            return False
    
    def get_badge_count(self, **params):
        """
        get_badge_count() - Returns yes if given event found under Upcoming tab otherwise returns no
        Parameters: tabName
        Ex: get_badge_count tabName
        """
        try:
            if params["tabName"].lower() == "messages":
                count = self.queryElement.get_value("FP_voicemail_badge_count")
            elif params["tabName"].lower() == "voicemails":
                count = self.queryElement.get_value("FP_message_badge_count")
            log.mjLog.LogReporter("ManhattanComponent", "info", "get_badge_count -  count : %s" % count)
            return count
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "get_badge_count - Failed" + str(sys.exc_info()))
            return False

    def open_event_info(self, **params):
        '''
        Author: Prashanth
        open_event_info() - To open a event under upcoming events
        Change List: added if-else condition for clicking on event name (UKumar: 13-April-2017)

        '''
        try:
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            time.sleep(2)
            if "event_name" in params.keys():
                found = False
                for i in range(4):
                    event_names = self._browser.elements_finder("event_events_name")
                    for name in event_names:
                        if params["event_name"] == name.text:
                            name.click()
                            found = True
                            log.mjLog.LogReporter("ManhattanComponent", "info", "open_event_info - Clicked on event name")
                            break
                    else:
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "open_event_info - event not listed in %s try (ies) " % (i + 1))
                        time.sleep(2)
                    if found:
                        break
                else:
                    raise AssertionError("Meeting not displayed in Upcoming tab!")
            else:
                self.webAction.click_element("people_event_click")

            if "groupchat" in params.keys():
                self.webAction.click_element("first_panel_calls")
                time.sleep(10)
                self.webAction.click_element("first_panel_eventchat")
            elif "info" in params.keys():
                time.sleep(3)
                self.webAction.click_element("TP_EVENT_INFO")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "open_event_info - Clicked on event to show information")
            elif "verify" in params.keys():
                time.sleep(3)
                self.assertElement.page_should_contain_text(params["event"])

            elif "doubleclick" in params.keys():
                time.sleep(3)
                self.webAction.double_click_element("TP_Event_Org")
                self.assertElement.element_should_be_displayed("TP_contact_name")
                name = self.queryElement.get_text("TP_contact_name")
                if name == params["user"]:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "open_event_info - verified the user in contact card")
                else:
                    raise AssertionError("Users contact card not opened")


            elif "verifyevent" in params.keys():
                time.sleep(3)
                self.assertElement.page_should_contain_text(params["event"])
                self.assertElement.page_should_contain_text("Edit Meeting")
                self.assertElement.page_should_contain_text("ORGANIZERS")
                self.assertElement.page_should_contain_text("PRESENTERS")
                self.assertElement.page_should_contain_text(params["organizer"])
                self.assertElement.page_should_contain_text(params["presenter"])
                self.assertElement.page_should_contain_text("PM" or "AM")

                date = self.queryElement.get_value('events_time')
                actual = date.split("")

                ctime = time.strftime("%A %B %Y %d %I")
                if ctime in actual:
                    print("#########verified the current day,year,month,date#############")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  " open_event_info- clicking on event info in second panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_event_info failed")

    def verifying_event_details(self, **params):
        """
        Author: Surendra
        verifying_event_details() - This API checks the presenters and participents check present or not
        Ex:

        """
        try:
            if params["entity"] == "event":
                self.event.verifying_event_details(params)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verifying_event_details - Failed to check presenters/particepents text" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error verifying_event_details - failed")

    def verify_events_page(self):
        '''
           verify_events_page()- This API verifies events page elements
        '''
        try:
            self.assertElement.element_should_be_displayed("events_upcoming_tab")
            self.assertElement.element_should_be_displayed("events_past_tab")
            self.assertElement.element_should_be_displayed("events_new_event_button")
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_events_page - Events page verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_events_page - error while verifying"
                                                                 " events page elements" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_events_page - failed")

    def verify_events_avail_upcoming(self, **params):
        '''
           verify_events_avail_upcoming()- This API verifies events availability under upcoming tab
        '''
        try:
            if params["entity"] == "event_avail":
                # self.assertElement.element_should_not_be_displayed("event_click_modify1")
                userlist = self._browser.elements_finder("event_click_modify")
                if len(userlist) == 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_events_avail_upcoming - no events are avaial")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_events_avail_upcoming - events are avaial")
            elif params["entity"] == "event_verify":
                self.assertElement.element_should_be_displayed("event_click_modify1")
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_events_avail_upcoming -  event is avaial")
            elif params["entity"] == "event_click":
                time.sleep(3)
                self.webAction.click_element("event_click_modify1")
                time.sleep(2)
                self.assertElement.page_should_contain_text(params["event"])
            elif params["entity"] == "event_third":
                userlist = self._browser.elements_finder("events_create_invite")
                if len(userlist) == 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_events_avail_upcoming - third panel is not avaial")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_events_avail_upcoming - third panel avaial")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_events_avail_upcoming - events are avail")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_events_avail_upcoming - error while verifying events page elements" + str(
                                      sys.exc_info()))
            return False

    def chk_event_creation_user(self, **params):
        '''
           Author: surendra
           chk_event_creation_user() - This method checks if event
                                          are present after event creation in second panel of the events under upcoming tab
            Parameters: eventname: name of the user to be checked
           ex: chk_usr_aft_event_creation eventname=event1

        '''
        try:
            self.webAction.explicit_wait("events_edit_meeting")
            self.webAction.click_element("events_edit_meeting")
            if "name" in params.keys():
                self.event.set_meeting_title(params["name"])
                self.event.events_add_meeting_time_details(params)
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "chk_event_creation_user- Meeting title modified successfully")
                self.event.click_create_event_invite()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " chk_event_creation_user- Checking event under upcoming event")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "chk_event_creation_user - Failed to check event in upcoming event" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error chk_event_creation_user failed")

    def verifying_event_users_avail(self, **params):
        """
        Author : Surendra
        verifying_event_users_avail() - This API will verify event user avail
        parameter: message
        ex: verifying_event_users_avail
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verifying_event_users_avail - user availability verification")
            name = re.sub("\*", " ", params["user"])

            count = 0
            if params["user_list"] == "Exo":
                userlist = self._browser.elements_finder("first_panel_verify_sender")
            if params["user_list"] in "Endo":
                userlist = self._browser.elements_finder("first_panel_attandees")

            for user_name in userlist:
                userNameDisplayed = user_name.text
                if '...' in user_name.text:
                    userNameDisplayed = userNameDisplayed[:userNameDisplayed.index("...")]
                if userNameDisplayed in name:
                    count = count + 1
            if count != 0:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verifying_event_users_avail"
                                                                    " - %s is available in event list" % params[
                                            "user"])
            else:
                raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verifying_event_users_avail - "
                                                                 "User is NOT available in event list" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error verifying_event_users_avail failed")

    def share_call_screen(self, **params):
        """
        author:prashanth
        share_call_screen() - This API clicks on the screen share button in call
        change list: added if condition for share_option (UKumar: 26-Dec-2016)
        """
        try:
            if "share" in params.keys():
                self.webAction.click_element("events_share_button")
                if params["share_option"] == "share_full_screen":
                    self.webAction.click_element("event_share_full_screen")
                    time.sleep(12)
                    log.mjLog.LogReporter("PeopleGroup", "info", "share_call_screen - clicked on share full screen")
                elif params["share_option"] == "share_area":
                    self.webAction.click_element("event_share_area")
                    log.mjLog.LogReporter("PeopleGroup", "info", "share_call_screen - clicked on share area")
                else:
                    self.webAction.click_element("event_share_window")
                    log.mjLog.LogReporter("PeopleGroup", "info", "share_call_screen - clicked on share window")
            if "accept" in params.keys():
                self.webAction.click_element("default_accept_share")
                log.mjLog.LogReporter("PeopleGroup", "info",
                                      "share_call_screen - accepted screen share successfully")
        except:
            log.mjLog.LogReporter("PeopleGroup", "error",
                                  "share_call_screen - clicked screen share failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error share_call_screen failed")

    def share_endo_client_screen(self, **params):
        """
        Author: Surendra
        share_endo_client_screen() - This API shares screen while user is in event from endo client
        Parameters: share_option and user_role
        Ex.: share_endo_client_screen click_on_screen_share_again=yes/no share_option=share_full_screen/share_area/share_window
                                      user_role=organizer/presenter/participant
        Extra Info: pass click_on_screen_share_again=yes if you are clicking on share screen button for the second time
        change list: added log messages (UKumar: 23-Dec-2016)
                     added if condition to distinguish the user's role in event (UKumar: 29-Dec-2016)
        """
        try:
            time.sleep(4)
            if params["click_on_screen_share_again"] == "yes":
                self.webAction.click_element("events_share_button")
            else:
                self.event.share_call_screen({"share": "yes", "share_option": params["share_option"], "role": params["user_role"]})

            if params["user_role"] == "organizer" or params["user_role"] == "presenter":
                log.mjLog.LogReporter("ManhattanComponent", "info", "share_endo_client_screen"
                                                                    " - Screen sharing started")
            else:
                self.assertElement.element_should_contain_text("event_approval_text",
                                                               "Waiting for organizer's approval to share screen")
                self.assertElement.element_should_be_displayed("event_wait_for_approval")
                log.mjLog.LogReporter("ManhattanComponent", "info", "share_endo_client_screen"
                                                                    " - waiting for organizer's approval to share screen")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "share_endo_client_screen"
                                                                 " - failed to start screen share " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error share_endo_client_screen failed")

    def permit_share_screen(self, **params):
        """
        Author: UKumar
        permit_share_screen() - This API verifies permission option for screen share and accepts
                                are rejects screen sharing permission
        Parameters: click_on_screen_share, first_name, last_name and accept
        Ex.: permit_share_screen click_on_screen_share=yes/no first_name=abc last_name=xyz accept=yes/no/no_action
        Extra Info: pass click_on_screen_share=yes if you want to click on "share your screen" button also
                    first_name and last_name are the name of participant
                    pass accept=yes for granting permission, no for rejection and no_action for doing nothing
        """
        try:
            if self.queryElement.element_not_displayed("event_accept_permission") or params["click_on_screen_share"] == "yes" :
                self.webAction.click_element("events_share_button")
            name = params["first_name"] + " " + params["last_name"]
            self.assertElement.element_should_be_displayed("event_reject_permission")
            self.assertElement.element_should_be_displayed("event_accept_permission")
            self.assertElement.page_should_contain_text(name + " would like to share their screen.")

            if params["accept"] == "yes":
                self.webAction.click_element("event_accept_permission")
                log.mjLog.LogReporter("ManhattanComponent", "info", "permit_share_screen"
                                                                    " - screen sharing approved")
            elif params["accept"] == "no":
                self.webAction.click_element("event_reject_permission")
                log.mjLog.LogReporter("ManhattanComponent", "info", "permit_share_screen"
                                                                    " - screen sharing permission rejected")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "permit_share_screen"
                                                                    " - Screen sharing options verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "permit_share_screen"
                                                                 " - failed to permit screen share " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error permit_share_screen failed")

    def click_away_verify_share_dialog(self, **params):
        """
        Author: UKumar
        click_away_verify_share_dialog() - This API clicks away from the screen sharing
                        permission dialog and verifies that dialog disappears
        Parameters: user_role
        Ex.: click_away_verify_share_dialog user_role=orgainzer/participant

        """
        try:
            if params["user_role"] == "organizer":
                self.webAction.click_element("second_panel_conf_header")
                # time.sleep(1)
                # self.assertElement.element_should_be_displayed("event_approval_dialog_disappear")
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_away_verify_share_dialog"
                                                                    " - approval dialog disappeared")
            else:
                self.webAction.click_element("second_panel_conf_header")
                # time.sleep(1)
                # self.assertElement.element_should_be_displayed("event_wait_for_approval_dialog_disappear")
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_away_verify_share_dialog"
                                                                    " - waiting for approval dialog disappeared")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_away_verify_share_dialog"
                                                                 " - failed to verify dialog " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_away_verify_share_dialog failed")

    def accept_screen_share(self, **params):
        """
        Author: UKumar
        accept_screen_share(): This API accept sharing either by pressing
            'green join button' in dashboard or by pressing 'View Screen Share'
            button (sharing started after chat) and verifies that sharing is in
            progress or waiting for sharing
        Parameters: join_when and join_how
        Ex: accept_screen_share join_when=before_play/after_play join_how=green_join_button/view_screen_share
        """
        try:
            self.peopleGroup.accept_screen_share(params["join_how"])
            time.sleep(4)  # wait for waiting dialog/screenshare to appear
            if params["join_when"] == "before_play":
                self.assertElement.element_should_be_displayed("TP_waiting_to_share")
                log.mjLog.LogReporter("ManhattanComponent", "info", "accept_screen_share"
                                                                    " - waiting for another user to start sharing")
            else:
                self.assertElement.element_should_be_displayed("TP_shared_window")
                log.mjLog.LogReporter("ManhattanComponent", "info", "accept_screen_share"
                                                                    " - sharing is in progress")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "accept_screen_share"
                                                                 " - failed to accept screen share")
            raise Exception("ManhattanComponent error accept_screen_share failed. waiting dialog/screenshare didn't appear.")

    def verify_screen_share(self, **params):
        """
        Author: UKumar
        verify_screen_share(): This API verifies that user is waiting for share,
            sharing is in progress or sharing has ended
        Parameters: option
        Ex: verify_screen_share option=waiting_to_share/sharing_in_progress/ended_sharing
        """
        try:
            if params["option"] == "waiting_to_share":
                self.assertElement.element_should_be_displayed("TP_waiting_to_share")
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_screen_share"
                                                                    " - waiting for another user to start sharing")
            elif params["option"] == "sharing_in_progress":
                self.webAction.explicit_wait("TP_shared_window")
                self.assertElement.element_should_be_displayed("TP_shared_window")
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_screen_share"
                                                                    " - sharing is in progress")
            else:
                self.assertElement.element_should_be_displayed("TP_ended_sharing")
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_screen_share"
                                                                    " - sharing has been ended")
        except:
            try:
                log.mjLog.LogReporter("ManhattanComponent", "info", "checking second time - verify_screen_share")
                if params["option"] == "waiting_to_share":
                    self.assertElement.element_should_be_displayed("TP_waiting_to_share")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_screen_share"
                                                                        " - waiting for another user to start sharing")
                elif params["option"] == "sharing_in_progress":
                    self.webAction.explicit_wait("TP_shared_window")
                    self.assertElement.element_should_be_displayed("TP_shared_window")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_screen_share"
                                                                        " - sharing is in progress")
                else:
                    self.assertElement.element_should_be_displayed("TP_ended_sharing")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_screen_share"
                                                                        " - sharing has been ended")
            except:
                log.mjLog.LogReporter("ManhattanComponent", "error", "verify_screen_share"
                                                                     " - failed to verify screen share " + str(sys.exc_info()))
                raise Exception("ManhattanComponent error verify_screen_share failed")

    def play_pause_close_presenter(self, **params):
        """
        Author: UKumar
        play_pause_close_presenter(): This API clicks on play, pause or close button
            of Presenter window to start, resume or close the sharing
        Parameters: option
        Ex: play_pause_close_presenter option=play/pause/close/close_dialog
        """
        try:
            winText = autoit.win_get_text("[TITLE:STPresenter]")
            if not "Actively Sharing" in winText.split("\n") and not "Sharing Paused" in winText.split("\n"):
                autoit.control_click("[TITLE:STPresenter]", "[NAME:shareExpandCollapse]")
            if params["option"] == "play":
                autoit.control_click("[TITLE:STPresenter]", "[NAME:SharingStartPauseButton]")
                log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                    " - clicked on play button to start screen share")
            elif params["option"] == "pause":
                autoit.control_click("[TITLE:STPresenter]", "[NAME:SharingStartPauseButton]")
                log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                    " - clicked on pause button to pause screen share")
            elif params["option"] == "close":
                try:
                    autoit.control_click("[TITLE:STPresenter]", "[NAME:SharingStopButton]")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                        " - clicked on stop button to stop screen share")
                except:
                    return False
            else:
                autoit.control_click("[Class:#32770]", "Button1")
                log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                    " - dialog box closed")
        except:
            try:
                log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter - checking second time")
                if params["option"] == "play":
                    autoit.control_click("[TITLE:STPresenter]", "[NAME:SharingStartPauseButton]")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                        " - clicked on play button to start screen share")
                elif params["option"] == "pause":
                    autoit.control_click("[TITLE:STPresenter]", "[NAME:SharingStartPauseButton]")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                        " - clicked on pause button to pause screen share")
                elif params["option"] == "close":
                    try:
                        autoit.control_click("[TITLE:STPresenter]", "[NAME:SharingStopButton]")
                        log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                            " - clicked on stop button to stop screen share")
                    except:
                        return False
                else:
                    autoit.control_click("[Class:#32770]", "Button1")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_close_presenter"
                                                                        " - dialog box closed")
            except:    
                log.mjLog.LogReporter("ManhattanComponent", "error", "play_pause_close_presenter"
                                                                     " - failed to click on play or stop button " + str(sys.exc_info()))
                raise Exception("ManhattanComponent error play_pause_close_presenter failed")


    def join_exo_event(self, **params):
        """
        Author : UKumar
        join_exo_event():To join conference from exo client
        parameters : sender
        Ex: join_exo_event sender=user1
        """
        try:
            participant = re.sub("\*", " ", params["sender"])
            self.event.join_via_exo_client(participant)
            self.assertElement.page_should_contain_text(participant)
            log.mjLog.LogReporter("ManhattanComponent", "info", "join_exo_event - Joined Event")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "join_exo_event - Failed to join event")
            raise Exception("ManhattanComponent error join_exo_event failed")

    def click_on_users_for_chat(self, **params):
        """
        Author : UKumar
        click_on_users_for_chat(): To click on individual user or group
                    for 1-1 IM chat or group chat from exo client
        Parameters: chat_option and participant
        Ex: click_on_users_for_chat chat_option=individual_chat/group_chat participant=user1
        """
        try:
            if params["chat_option"] == "individual_chat":
                username = re.sub("\*", " ", params["participant"])
                participants_list = self._browser.elements_finder("Exo_individual_chat")
                for participant in participants_list:
                    participant.click()
                    participant_name = participant.text.strip()
                    if participant_name == username:
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "click_on_users_for_chat - clicked on %s for 1-1 IM" % username)
                        break
            elif params["chat_option"] == "group_chat":
                self.webAction.click_element("Exo_click_groupchat")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "click_on_users_for_chat - clicked on group chat icon")
            else:
                raise AssertionError("Wrong option!")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_on_users_for_chat - Failed to click on users for chat " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_on_users_for_chat failed")

    def send_im_exo(self, **params):
        """
        Author : UKumar
        send_im_exo(): To send IM from exo client
        Parameters: message
        Ex: send_im_exo message=hello
        """
        try:
            self.webAction.click_element("EXO_panel_chatBox1")
            self.webAction.input_text("EXO_panel_chatBox1", params["message"])
            self.webAction.press_key("EXO_panel_chatBox1", "RETURN")
            self.assertElement.page_should_contain_text(params["message"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "send_im_exo - IM sent")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "send_im_exo - Failed to send IM " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error send_im_exo failed")

    def verify_Exo_IM(self, **params):
        '''
        Author : Prashanth
        verify_Exo_IM():To verify the IM from endo & start chat with endo

        '''
        try:
            if "verify" in params.keys():
                self.assertElement.page_should_contain_text(params["ENDOIM"])

            elif "chat" in params.keys():
                self.webAction.click_element("Exo_click_groupchat")
                self.webAction.click_element("EXO_panel_chatBox1")
                self.webAction.input_text("EXO_panel_chatBox1", params["EXOIM"])
                self.webAction.press_key("EXO_JOIN", "RETURN")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_Exo_IM - verified IM from Endoclient in groupchat")

            elif "clickIM" in params.keys():
                self.webAction.click_element("Exo_individual_chat")
                self.assertElement.page_should_contain_text(params["EXOIM"])
            else:
                raise
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_Exo_IM - Failed to verify IM in Exo" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_Exo_IM failed")

    def clicking_user_sending_IM(self, **params):
        """
        Author : Surendra
        clicking_user_sending_IM() - This API will click on user for im
        parameter: message
        ex: clicking_user_sending_IM
        """
        try:
            if params["user_list"] == "Exo":
                name = re.sub("\*", " ", params["user"])
                userlist = self._browser.elements_finder("first_panel_verify_sender")
                count = 0
                for user_name in userlist:
                    print(user_name.text)
                    print("*************")
                    if user_name.text == name:
                        user_name.click()
                        count = count + 1
                if count != 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "clicking_user_sending_IM"
                                                                        " - Clicked on %s to send IM" % name)
                else:
                    raise AssertionError("User not present")
            if params["user_list"] == "Endo":
                name = re.sub("\*", " ", params["user"])
                userlist = self._browser.elements_finder("first_panel_attandees")
                count = 0
                for user_name in userlist:
                    if user_name.text == name:
                        user_name.click()
                        count = count + 1
                if count != 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "clicking_user_sending_IM"
                                                                        " - Clicked on %s to send IM" % name)
                else:
                    raise AssertionError("User not present")
            if params["user_list"] == "group_chat":
                self.webAction.click_element("default_group_call_icon")
                log.mjLog.LogReporter("ManhattanComponent", "info", "clicking_user_sending_IM"
                                                                    " - Clicked on group chat icon in Endo client to send IM")
            if params["user_list"] == "group_chat_Exo":
                self.webAction.click_element("Exo_click_groupchat")
                log.mjLog.LogReporter("ManhattanComponent", "info", "clicking_user_sending_IM"
                                                                    " - Clicked on group chat icon in EXO client to send IM")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "clicking_user_sending_IM "
                                                                 "- Failed to click on chat icon " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error clicking_user_sending_IM failed")


    def share_exo_client_screen(self, **params):
        """
        author : kiran
        share_exo_client_screen() - This API clicks on one screen sharing options from EXO client based on parameters
        Parameters: share_option and browser_name
        Ex: share_exo_client_screen share_option=share_full_screen/share_area/share_window browser_name=chrome
        Change List: Merged two APIs (share_exo_client_screen) written by Kiran and Surendra
                     Both the APIs were having same name but diffrent functionality (UKumar: 14-April-2017)
        """
        try:
            if self.queryElement.element_not_displayed("event_exo_control_bar"):
                self.webAction.mouse_hover("event_exo_sharing_panel")
            self.webAction.explicit_wait("event_exo_share_button")
            self.webAction.click_element("event_exo_share_button")
            self.event.screen_share_exo(params["share_option"])
            time.sleep(2)
            if params["browser_name"] == "chrome" or params["browser_name"] == "ie":                                         
                time.sleep(3)
                title = str(params["event_name"]) + " - Google Chrome"
                autoit.win_activate(title)          
                autoit.control_send("[TITLE:%s]" %(title), "Chrome_RenderWidgetHostHWND1", "{LEFT}")
                autoit.control_send("[TITLE:%s]" %(title), "Chrome_RenderWidgetHostHWND1", "{ENTER}")
                #autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{ENTER}")
            else:
                time.sleep(2)  # wait for open button to become enabled
                pyautogui.press("enter")
            time.sleep(6)
            self.event.handle_presenter_upgrade_popup()
            if params["share_option"] == "share_window":                
                time.sleep(6)
                #pyautogui.press("right")
                autoit.win_activate("Select an application to share")
                #autoit.control_send("[CLASS:WindowsForms10.Window.8.app.0.1a0e24_r16_ad1]", "WindowsForms10.SysListView32.app.0.1a0e24_r16_ad11", "{RIGHT}")
                autoit.control_send("[TITLE:Select an application to share]",
                                        "[NAME:runningApplistView]", "{RIGHT}")
                log.mjLog.LogReporter("ManhattanComponent", "info", "share_exo_client_screen"
                                                                    " - Clicked on an application window to share")
            log.mjLog.LogReporter("ManhattanComponent", "info", "share_exo_client_screen"
                                                                " - Ready to share " + params["share_option"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "share_exo_client_screen"
                                                                 " - Failed to click on screen share " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error share_exo_client_screen failed")

    def add_or_delete_to_favorite_group(self, **params):
        """
        Author: Gautham modified by Uttam
        add_or_delete_to_favorite_group() - This API is to add or delete a user to default favorite group
        Parameters: peopleName and option
        Ex: add_or_delete_to_favorite_group  peopleName=abcd option=add
        Change List: search_people_or_extension API added and invoke_peoplelist API removed
        """
        try:
            peopleName = re.sub("\*", " ", params["peopleName"])
            self.defaultPanel.search_people_or_extension(peopleName,{})
            time.sleep(3)
            self.peopleGroup.click_favorite_button(peopleName, params["option"])
            if params["option"] == "add":
                log.mjLog.LogReporter("ManhattanComponent", "info", "add_or_delete_to_favorite_group"
                                                                    " - user " + params[
                                          "peopleName"] + " added to Favorites")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "add_or_delete_to_favorite_group"
                                                                    " - user " + params[
                                          "peopleName"] + " deleted from Favorites")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_or_delete_to_favorite_group"
                                  " - unable to add or delete user to Favorites" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error add_or_delete_to_favorite_group failed")

    def change_user_telephony_status(self, **params):
        '''
           Author: Gautham modified by uttam
           change_user_telephony_status() - This method clicks on user status and changes user status
           parameter : status, customStatus, customMessage and option
           ex: change_user_telephony_status status=available
           ex: change_user_telephony_status status=in_a_meeting
           ex: change_user_telephony_status status=out_of_office
           ex: change_user_telephony_status status=do_not_disturb
           ex: change_user_telephony_status status=vacation
           ex: change_user_telephony_status status=custom... customStatus=Busy option=save customMessage=Reading
           extra info: if you want to set blank status message then do not pass customMessage
                       option could be save or cancel
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " change_user_telephony_status- Clicking on the user telephony presence")
            self.defaultPanel.change_user_status(params["status"])
            if params["status"].lower() == "custom...":
                if "customMessage" in params.keys():
                    self.defaultPanel.set_status_variable(params["customStatus"], params["option"], \
                                                          params["customMessage"])
                elif "option" in params.keys():
                    self.defaultPanel.set_status_variable(params["customStatus"], params["option"])
                else:
                    self.defaultPanel.set_status_variable(params["customStatus"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "change_user_telephony_status -"
                                                                " User telephony status changed - PASSED")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "change_user_telephony_status - "
                                                                 "Could not change user telephony status - FAILED" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error change_user_telephony_status failed")

    def check_user_telephony_presence(self, **params):
        '''
           Author: Gautham
           check_user_telephony_presence() - Checks the user telephony presence (status and color) at the manhattan login
           parameter : status, color
           ex: check_user_telephony_presence status=available color=green
           ex: check_user_telephony_presence status=in_a_meeting color=orange
           ex: check_user_telephony_presence status=out_of_office color=red
           ex: check_user_telephony_presence status=do_not_disturb color=red
           ex: check_user_telephony_presence status=vacation color=red

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " check_user_telephony_presence- Checking the user telephony presence")
            self.defaultPanel.check_user_telephony_presence(params["status"], params["color"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_user_telephony_presence- Correct user telephony status - PASSED")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_user_telephony_presence - Incorrect user telephony status - FAILED" + str(
                                      sys.exc_info()))
            return False

    def call_contact_by_doubleclick(self, **params):
        '''
        call_contact_by_doubleclick() - search a contact and call by double clicking over it
        parameters: contactName
        ex1: call_contact_by_doubleclick searchItem=xxxx
        Change List: Added assertion (UKumar: 28-April-2017)
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "call_contact_by_doubleclick"
                                                                " - Searching contact by name ")
            self.defaultPanel.search_people_or_extension(params["searchItem"].replace("*", " "), True)
            log.mjLog.LogReporter("ManhattanComponent", "info", "call_contact_by_doubleclick - contact available")
            time.sleep(2)            
            self.peopleGroup.call_contact_by_double_click(params["searchItem"].replace("*", ""))
            self.webAction.explicit_wait("first_panel_end_call")
            self.assertElement.element_should_be_displayed("first_panel_end_call")
            log.mjLog.LogReporter("ManhattanComponent", "info", "call_contact_by_doubleclick"
                                                                " - double clicked over the contact to make call")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "call_contact_by_doubleclick -"
                                                                 " unable to call contact by double clicking" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error call_contact_by_doubleclick failed")

    def call_contact_by_doubleclick_search_people(self, **params):
        '''
           call_contact_by_doubleclick() - search a contact and call by double clicking over it
           parameters: contactName
           ex1: call_contact_by_doubleclick searchItem=xxxx

        '''
        try:            
            self.defaultPanel.invoke_peoplelist()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "call_contact_by_doubleclick- Searching people by name ")
            # self.peopleGroup.searchpeople_dashboard(params["personname"])
            self.defaultPanel.search_people_or_extension(params["personname"].replace("*", " "))
            self.assertElement._page_contains(params["personname"].replace("*", " "))
            log.mjLog.LogReporter("ManhattanComponent", "info", "call_contact_by_doubleclick- contact avaialble ")
            time.sleep(3)
            self.peopleGroup.call_contact_by_double_click_people(params["personname"].replace("*", " "))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "call_contact_by_doubleclick- double clicked over the contact")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "call_contact_by_doubleclick- unable to call contact by double clicking" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error call_contact_by_doubleclick failed")

    def verify_contact_card(self, **params):
        """
        Author: UKumar
        verify_contact_card() - This API verifies whether contact card is present for a person
        Parameters: option and username
        Ex: verify_contact_card option=present/absent username=abc
        """
        try:
            status = self.queryElement.element_not_displayed("third_panel_user")
            if status and params["option"] == "absent":
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_card - contact"
                                                                    "card of user " + params[
                                          "username"] + " is not present")
            else:
                username = re.sub("\#", " ", params["username"])
                name = self.queryElement.get_text("third_panel_user")
                if name == username and params["option"] == "present":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_card - contact"
                                                                        "card of user " + username + " is present")
                elif name == username and params["option"] == "absent":
                    raise AssertionError("Contact card is present but it should not!")
                elif name != username and params["option"] == "absent":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_card - contact"
                                                                        "card of user " + username + " is not present")
                else:
                    raise AssertionError("Contact card should not be present, but it is!")
            if "image" in params.keys():
                self.assertElement.element_should_be_displayed("people_image")
            if "status" in params.keys() and params["status"] == "yes":
                self.assertElement.element_should_be_displayed("third_panel_statusColor")
                self.assertElement.element_should_be_displayed("TP_im_presence")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_contact_card "
                                                                 "- failed to verify contact card")
            raise Exception("ManhattanComponent error verify_contact_card failed")

    def check_favorite_symbol(self, **params):
        """
        Author: Uttam
        check_favorite_symbol() - This API checks the presence of favorite
                                  symbol for a user in Favorites tab
        Parameters: peopleName
        Ex: check_favorite_symbol status=true/false peopleName=abcd
        """
        try:
            status = "true"
            if "clickpeople" in params.keys():
                self.webAction.click_element("default_people_tab")
                self.webAction.click_element("peoples_favorite_tab")
                status = self.peopleGroup.check_favorite_button(params["peopleName"])
                if status == "true":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol - favorite button"
                                                                        " is present for user " + params["peopleName"])
                elif status == "no user":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol"
                                                                        " - no user is present")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol"
                                                                        " - user is not Favorite")
            elif "noclick" in params.keys():
                # self.webAction.click_element("peoples_favorite_tab")
                status = self.peopleGroup.check_favorite_button(params["peopleName"])
                if status == "true":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol - favorite button"
                                                                        " is present for user " + params["peopleName"])
                elif status == "no user":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol"
                                                                        " - no user is present")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol"
                                                                        " - user is not Favorite")
            else:
                self.webAction.click_element("peoples_favorite_tab")
                status = self.peopleGroup.check_favorite_button(params["peopleName"])
                if status == "true":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol - favorite button"
                                                                        " is present for user " + params["peopleName"])
                elif status == "no user":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol"
                                                                        " - no user is present")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "check_favorite_symbol"
                                                                        " - user is not Favorite")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_favorite_symbol - failed"
                                                                 " to check Favorite symbol " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error check_favorite_symbol failed")

    def check_favorite_symbol_from_search(self, **params):
        """
        Author: UKumar
        check_favorite_symbol_from_search() - This API searches for a user through search bar
                                    in dashboard and verifies that favorite symbol is present
                                    for a user or not
        Parameters: peopleName
        Ex: check_favorite_symbol_from_search peopleName=abcd
        """
        try:
            self.searchItem = re.sub("\*\*", " ", params["peopleName"])
            self.defaultPanel.search_people_or_extension(self.searchItem,{})
            status = True
            status = self.peopleGroup.check_favorite_symbol_from_search(params["peopleName"])
            if status is False:
                raise
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_favorite_symbol_from_search - favorite button"
                                      " is present for " + params["peopleName"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_favorite_symbol_from_search - failed"
                                                                 " to check Favorite symbol " + str(sys.exc_info()))
            return False

    def close_panel(self, **params):
        """
        Author: Gautham modified by Uttam
        close_panel() - close the second or third panel of Manhattan client
        parameters: panel
        ex1: close_panel panel=second
        ex2: close_panel panel=second_search
        ex3: close_panel panel=third
        ex4: close_panel panel=screen_share
        ex5: close_panel panel=groupDraft
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "close_panel- closing the panel...")
            self.peopleGroup.close_panel(params["panel"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "close_panel- closed the panel successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "close_panel- failed to close the panel " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error close_panel failed")

    def make_call_press_enter(self, **params):
        """
        Author: Uttam
        make_call_press_enter - This API makes a call to a user by pressing ENTER
        Parameters: searchItem, pressEnter and username
        Ex: make_call_press_enter searchItem=1 pressEnter=yes username=USER_PSP_02
        Extra Info.: searchItem could be first one or two letters of username
                     or could be the starting digits of extension number
        """
        try:
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")

            self.webAction.input_text("default_search_input", params["searchItem"])
            time.sleep(2)  # wait for search result to appear
            if params["pressEnter"] == "yes":
                self.peopleGroup.call_by_pressing_enter(re.sub("\*", " ", params["username"]))
                self.webAction.explicit_wait("third_panel_end_call")  # time.sleep(3)
                self.assertElement.element_should_be_displayed("third_panel_end_call")
                log.mjLog.LogReporter("ManhattanComponent", "info", "make_call_press_enter -"
                                                                    " call made by pressing ENTER")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "make_call_press_enter - failed"
                                                                 " to make a call " + str(sys.exc_info()))
            raise

    def search_contact_using_DID(self, **params):
        """
        Author: kalyan
        search_contact_using_DID() - This API will search the DID number in the search list
        Parameters: searchItem
        Ex: search_contact_using_DID searchItem=98066839253
        Extra Info: if searchItem=98066839253 you have to add prefix before dailing any did number.You have to search like this only.
        """
        try:            
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            log.mjLog.LogReporter("ManhattanComponent", "debug", "search_contact_using_DID : Clicked on search button")
            self.webAction.input_text("default_search_input", params["searchItem"])
            self.webAction.explicit_wait("third_panel_new_contact")
            self.assertElement.element_should_be_displayed("third_panel_new_contact")
            did = self.queryElement.get_text("third_panel_new_contact")
            print("third panel contact name", did)
            did[1:11]
            print("the did number is ", did[1:11])
            if params["searchItem"][1:11] == did[1:11]:
                print("contact is matched and will get the number in the contact card")
            print("************************called***********************")
            time.sleep(2)
            self.assertElement.element_should_be_displayed("third_panel_answer_call")
            log.mjLog.LogReporter("ManhattanComponent", "info", "search_contact_using_DID- contact is searched")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "search_contact_using_DID- contact is not found" + str(sys.exc_info()))
            return False
            
    def thirdpanel_call_record(self, **params):
        """
        Author: Manoj
        thirdpanel_call_record() - This API will sgo and clicka the record button
        Ex: thirdpanel_call_record option=start_recording/stop_recording
        """
        try:
            self.webAction.click_element("FP_first_call_on_dashboard")
            time.sleep(2)
            if params["option"] == "start_recording":
                self.assertElement.element_should_be_enabled("TP_call_record_off")
                self.webAction.click_element("TP_call_record_off")
                self.webAction.explicit_wait("TP_call_record_on")
                self.assertElement.page_should_contain_element("TP_call_record_on")
                log.mjLog.LogReporter("ManhattanComponent","info","thirdpanel_call_record - recording started")
            else:
                self.webAction.click_element("TP_call_record_on")
                self.webAction.explicit_wait("TP_call_record_off")
                self.assertElement.page_should_contain_element("TP_call_record_off")
                log.mjLog.LogReporter("ManhattanComponent","info","thirdpanel_call_record - recording stopped")
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","thirdpanel_call_record -"
                                    " failed to click on record button "+str(sys.exc_info()))
            raise
            
    def verify_conferencecall_users_ends_the_call(self, **params):
        """
        click_down_arrow_conferencecall_ends_the_call() - This method clicks the down arrow of conference call and ends any of the call which is added in the call
        author : kiran
        parameters : user1, option
        EX. : verify_conferencecall_users_ends_the_call user1=auser user2=user2 option=verify
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent","info","verify_conferencecall_users_ends_the_call"
                    " - going to check the conference call and end any of call from the call list")
            userlist = []
            for key in params.keys():
                if "user" in key:                       
                    userlist.append(params[key])
            if params["option"] == "verify":
                self.defaultPanel.verify_conference_call_users(userlist)
            else:
                self.defaultPanel.end_any_call_from_conferenceCall(userlist)                                                  
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","verify_conferencecall_users_ends_the_call"
                    " - Failed to click on call button "+str(sys.exc_info()))
            return False
            
    def click_call_contact_from_recent_history(self, **params):
        '''
           click_call_contact_from_recent_history() - search a contact and call by double clicking over it
           parameters: contactName
           ex1: click_call_contact_from_recent_history searchItem=xxxx
        
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent","info","click_call_contact_from_recent_history- Invoke recent history list ")
            self.assertElement._page_contains(params["searchItem"])
            log.mjLog.LogReporter("ManhattanComponent","info","click_call_contact_from_recent_history- contact avaialble ")
            time.sleep(3)
            peopleList=self._browser.elements_finder("Recent_outgoing_call")
            
            for i in peopleList:
                i.click()
                break
            log.mjLog.LogReporter("ManhattanComponent","info","click_call_contact_from_recent_history- double clicked over the contact")
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","click_call_contact_from_recent_history- unable to call contact in recent list by double clicking"+str(sys.exc_info()))
            return False

    def click_first_entry_from_recent_tab(self, **params):
        '''
            click_first_entry_from_recent_tab() -search a  contact and open contact card
            ex1: click_first_entry_from_recent_tab searchItem=xxxx
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent","info","click_first_entry_from_recent_tab- Invoke recent history list ")
            if not params["searchItem"]:
                self.assertElement._page_contains(params["searchItem"])
                self.webAction.input_text("recent_search_textbox", params["searchItem"])
                time.sleep(1)
            self.webAction.click_element("recent_all_tab_first_item")
            time.sleep(2)
            log.mjLog.LogReporter("ManhattanComponent","info","click_first_entry_from_recent_tab- contact avaialble and clicked ")
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","click_first_entry_from_recent_tab- unable to click first entry in recent tab. "+str(sys.exc_info()))
            return False

    def click_filter_message(self, **params):
        '''
           Author: prashanth
           click_filter_message() - Filter the message from thirdpanel  close im chat
           ex: click_filter_message filter=message

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_filter_message- Message")
            
            if params["filter"].lower() ==  "messages":
                self.webAction.click_element('third_panel_messages')
            elif params["filter"].lower() ==  "calls":
                self.webAction.click_element('third_panel_calls')
            elif params["filter"].lower() ==  "messages":
                self.webAction.click_element('third_panel_messagefilter')
            else :
                self.webAction.click_element('third_panel_voicemail')

            if "close" in params.keys():
                self.webAction.click_element("third_panel_minimize")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_filter_message - Failed to change filter " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_filter_message failed")

    def send_IM(self, **params):
        """
        send_IM() - This API sends IM from one user to another
        parameter: message
        ex: send_IM message="hello"
        """
        try:
            self.message.send_IM(params["message"])
            #self.assertElement.page_should_contain_text(params["message"])---commented due to defect ENG-521694- Endo: First IM is disappearing from the contact card
            log.mjLog.LogReporter("ManhattanComponent", "info", "send_IM - message sent successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "send_IM - failed to sent IM")
            raise Exception("ManhattanComponent error send_IM failed")

    def received_IMA(self, **params):
        """
        Author: Uttam
        received_IMA() - This API checks that IM is received or not
        Parameters: status and message
        Ex: received_IMA status=true message=hello
        Extra Info: if status=true then it will check for "IM is received"
                         otherwise it will check for "IM is not received"
        """
        try:
            if params["status"].lower() == "true":
                #time.sleep(2)
                self.assertElement.page_should_contain_text(params["message"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "received_IMA - IM received")
            else:
                self.assertElement.page_should_not_contain_text(params["message"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "received_IMA - IM not received")

            if "initial" in params.keys():
                self.assertElement.page_should_contain_text(params["initial"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "received_IMA - Initials of user name verified")
        except:
            try:
                log.mjLog.LogReporter("ManhattanComponent", "info", "received_IMA - checking second time")
                autoit.win_activate("Mitel Connect")
                self.assertElement.page_should_contain_text(params["message"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "received_IMA - IM received")
            except:    
                log.mjLog.LogReporter("ManhattanComponent", "error", "received_IMA - failed to"
                                                                     " receive IM " + str(sys.exc_info()))
                raise Exception("ManhattanComponent error received_IMA failed")

    def received_IMB(self, **params):
        """
        Author: Upendra,modified by prashanth
        received_IMB() - This API checks that IM is received or not & also the initials of the sender
        Parameters: status and message
        Ex: received_IMB status=true message=hello
        Extra Info: if status=true then it will check for "IM is received"
                         otherwise it will check for "IM is not received"
                    If second panel(Messages) is not opened already then use
                     invoke_dashborad_tab API before using this API
        """
        try:
            if params["status"].lower() == "true":
                self.message.verify_im_received(re.sub("\*", " ", params["message"]))
                log.mjLog.LogReporter("ManhattanComponent", "info", "received_IMB - IM received")
            else:
                # not yet implemented
                pass
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "received_IMB - failed to"
                                                                 " receive IM " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error received_IMB failed")

    def Im_send_differnt_scenerios(self, **params):
        """
           Im_send_differnt_scenerios()- This API sends different types of im's
           Author:Manoj
           Parameters : Im_send_differnt_scenerios option = Special_characters.........
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "Im_send_differnt_scenerios "
                                                                "- Going to send different types of IMs")
            if params["option"] == "Special_characters":
                special_string = "aakash"
                encoded_string = special_string.encode("cp1252")
                im_to_send = encoded_string.decode("cp1252")
            elif params["option"] == "Different_characters":
                different_string = "dowHWE720983$%^7LKSA'PEOLDSPWAO"
                encoded_string = different_string.encode("cp1252")
                im_to_send = encoded_string.decode("cp1252")
            elif params["option"] == "Quotedstring":
                im_to_send = '"' + 'Shoretel' + '"'
            elif params["option"] == "without_quotedstring":
                im_to_send = "shoretel"
            elif params["option"] == "Hyperlink":
                im_to_send = "https://www.google.co.in"
            else:
                raise AssertionError("Invalid argument!")

            self.webAction.click_element("third_panel_chatBox")
            self.webAction.input_text("third_panel_chatBox", im_to_send)
            self.webAction.press_key("third_panel_chatBox", "RETURN")
            log.mjLog.LogReporter("ManhattanComponent", "info", "Im_send_differnt_scenerios - IM %s sent" % im_to_send)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Im_send_differnt_scenerios"
                                                                 " - unable to send IM " + str(sys.exc_info()))
            return False

    def Im_verify_differnt_scenerios(self, **params):
        """
           Im_verify_differnt_scenerios()- This API sends different types of im's
           Author:Manoj
           Parameters : Im_verify_differnt_scenerios option = Special_characters       .........
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "Im_verify_differnt_scenerios"
                                                                " - verifying different types of IMs")
            if params["option"] == "Special_characters":
                special_string = "aakash"
                encoded_string = special_string.encode("cp1252")
                im_to_verify = encoded_string.decode("cp1252")
            elif params["option"] == "Different_characters":
                different_string = "dowHWE720983$%^7LKSA'PEOLDSPWAO"
                encoded_string = different_string.encode("cp1252")
                im_to_verify = encoded_string.decode("cp1252")
            elif params["option"] == "Quotedstring":
                im_to_verify = '"' + 'Shoretel' + '"'
            elif params["option"] == "without_quotedstring":
                im_to_verify = "shoretel"
            elif params["option"] == "Hyperlink":
                im_to_verify = "https://www.google.co.in"
            else:
                raise AssertionError("Invalid argument!")

            messages = self._browser.elements_finder("second_panel_Im_users")
            for message in messages:
                if im_to_verify in message.text:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "Im_verify_differnt_scenerios -"
                                                                        " IM %s verified" % im_to_verify)
                    break
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Im_verify_differnt_scenerios -"
                                                                 " unable to verify IM " + str(sys.exc_info()))
            return False

    def click_filter_IM(self, **params):
        '''
           Author: prashanth
           click_filter_IM() - This method clicks on the filter icon & types a letter & verifies the IM
            Parameters: IM: name of the IM to be checked
           ex: click_filter_IM eventname=event1

        '''
        try:
            self.webAction.click_element("default_IM_filter")
            time.sleep(1)
            self.webAction.click_element("default_IM_filtertext")
            self.webAction.input_text("default_IM_filtertext", params["IM"])
            time.sleep(3)
            self.webAction.press_key("default_IM_filtertext", "RETURN")
            time.sleep(3)
            self.assertElement.page_should_contain_text(params["message"])
            log.mjLog.LogReporter("ManhattanComponent", "info", " click_filter_IM - Filtered IM verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_filter_IM - Failed to filter and verify IM " + str(sys.exc_info()))
            return False

    def verify_im_chat_time(self):
        """
        Author : Manoj
        verify_im_chat_time() - This API will verify the time in chatpanel
        ex: verify_im_chat_time content=message Split=Yes
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_im_chat_time - going to check the time in chatpanela ")
            chat_list = self._browser.elements_finder("TP_chat_list")
            print(chat_list)
            if 'am' or 'pm' in self.queryElement.element_displayed("TP_chat_time"):
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_im_chat_time - time in chat panel is verified properly" + str(
                                          sys.exc_info()))
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_im_chat_time - time in chat panel is noty verified properly" + str(
                                          sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_im_chat_time - failed to verify time in chat panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_im_chat_time failed")

    def verify_im_first_chat_time(self):
        """
        Author : Manoj
        verify_im_first_chat_time() - This API will verify the time in chatpanel
        ex: verify_im_first_chat_time
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_im_first_chat_time - going to check the time in chat panel")
            first_chat_list = self._browser.elements_finder("TP_chat_list_first")
            if 'am' or 'pm' in first_chat_list[0]:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_im_first_chat_time - time in chat panel is verified properly")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_im_first_chat_time - time in chat panel is not verified properly")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_im_first_chat_time"
                                                                 " - failed to verify time in chat panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_im_first_chat_time failed")


    def verify_im_textarea(self, **params):
        """
        Author : Manoj
        verify_im_textarea() - This API will verify the text area in Im Panel
        parameter: message
        ex: verify_im_textarea content=message Split=Yes
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_im_textarea - going to click verify_im_textarea ")
            content1 = params["content1"]
            self.webAction.click_element("third_panel_chatBox")
            time.sleep(5)
            content = self.queryElement.get_element_attribute("third_panel_chatBox", "placeholder")
            print("content is <<<<-------------->>>:", content)
            if "Split" in params.keys():
                split_name = content1.split("*")
                content1 = " ".join(split_name)
                print("@@@@@@@@@@@@@@@@@@@@@  content1 @@@@@@@@@@@", content1)
            if content in content1:
                rgb = self._browser.element_finder("third_panel_chatBox").value_of_css_property("background-color")
                print("@@@@@@@@@@@@@@@@@@@@@  rgb @@@@@@@@@@@", rgb)
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                if "#d9d9d9" in hex_color:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_im_textarea"
                                                                        " - color is grey")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_im_textarea"
                                                                        " - color is not grey")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_im_textarea"
                                                                    " - content are not equal " + str(sys.exc_info()))
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_im_textarea - Text area not verified properly")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_im_textarea - failed to verify test area" + str(sys.exc_info()))
            return False

    def verify_im_textarea_hint_not_present(self, **params):
        """
        Author : Manoj
        verify_im_textarea_hint_not_present() - This API will verify the text area in Im Panel
        parameter: message
        ex: verify_im_textarea_hint_not_present IM=hi option = enter or clear or Null
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_im_textarea_hint_not_present - going to click verify_im_textarea ")
            IM = params["IM"]
            self.webAction.click_element("third_panel_chatBox")
            time.sleep(5)
            content = self.queryElement.get_element_attribute("third_panel_chatBox", "placeholder")
            if content is not None:
                self.webAction.input_text("third_panel_chatBox", IM)
                if content is None:
                    self.webAction.click_element("third_panel_chatBox")
                elif params['option'] == 'enter':
                    self.webAction.press_key("third_panel_chatBox", "RETURN")
                    time.sleep(5)
                elif params['option'] == 'clear':
                    self.webAction.clear_input_text("third_panel_chatBox")
                    time.sleep(5)
                elif params['option'] == 'Null':
                    self.webAction.press_key("third_panel_chatBox", "NULL")
            if content is not None:
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "verify_im_textarea_hint_not_present - veried test area" + str(sys.exc_info()))
            else:
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "verify_im_textarea_hint_not_present - failed to verify test area" + str(
                                          sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_im_textarea_hint_not_present - failed to verify test area" + str(
                                      sys.exc_info()))
            return False
            
            
    def verify_im_textarea_check_sent_text(self, **params):
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                    "verify_im_textarea_check_sent_text - going to click verify_im_textarea ")
                                  
            ActionChains(self._browser.get_current_browser()).send_keys("Mitel").perform()
            time.sleep(2)
            content = self.queryElement.get_text('third_panel_chatBox')
        
            if not content:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_im_textarea_check_sent_text"
                                                                        " - Nothing is present in IM text area")
            else:  
                raise Exception("ManhattanComponent error verify_im_textarea_check_sent_text failed")
        except:
            raise Exception("ManhattanComponent error verify_im_textarea_check_sent_text failed")  
        

    def chat_add_participants(self, **params):
        """
        Author : Manoj
        chat_add_participants() - This API will add another user to group chat
        parameter: message
        ex: chat_add_participants personname="hello"
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "chat_add_participants - message sent successfully")
            self.personname = params["personname"]
            self.webAction.click_element("TP_chat_add_participants")
            time.sleep(3)
            self.webAction.input_text("TP_chat_add_participants_input", params["personname"])
            time.sleep(3)
            self.webAction.click_element("TP_chat_add_participants_user")
            time.sleep(3)
            self.webAction.click_element("TP_chat_add_participants_add")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "chat_add_participants - message sent successfully" + str(sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "chat_add_participants - failed to sent IM" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error chat_add_participants failed")

    def add_contact_conversation(self, **params):
        """
        Author: Prashanth
        add_contact_conversation() - This API help in joining a contact to conversation
        parameters: name: Name of the contact

        ex: add_contact_conversation name=PUser
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "add_contact_conversation- Adding contact to  Conversation ")
            # self.webAction.input_text("TP_add_contact",params["name"])
            if "name" in params.keys():
                self.peopleGroup.add_contact_conversation(params["name"], params["checkname"])
            else:
                raise AssertionError("Wrong arguments passed !!!")
                # log.mjLog.LogReporter("ManhattanComponent","info","join_conference- able to join conference successfully")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "join_conference - Failed to join Conference")
            raise

    def verify_open_chat_entry(self, **params):
        """
        Author: UKUmar
        verify_open_chat_entry() - Verifies that a read chat entry is present in Messages tab and clicks on it
                                    participant name in chat
        Parameters: sender_name
        Ex: verify_open_chat_entry sender_name=abc if it is a 1-1 chat
            verify_open_chat_entry sender_name1=abc sender_name2=def if it is a group chat
        """
        try:
            self.message.verify_open_chat_entry(params)
            self.webAction.explicit_wait("third_panel_chatBox")
            self.assertElement.element_should_be_displayed("third_panel_chatBox")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " verify_open_chat_entry - chat entry verified and opened")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_open_chat_entry - Error " + str(sys.exc_info()))
            raise

    def verifying_group_chat_IM_users(self, **params):
        """
        Author : Surendra
        verifying_group_chat_IM_users() - This API will verify for attendes
        parameter: message
        ex: verifying_group_chat_IM_users
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verifying_group_chat_IM_users - user avaialability verification ")
            name = re.sub("\*", " ", params["user"])
            if params["user_list"] == "Exo":
                # userlist = self._browser.elements_finder("Exo_group_chat_users")
                user_data = self.queryElement.get_text("Exo_group_chat_users")

                List = user_data.split()
                print(List)
                if len(List) == 3:
                    print("this is if *************")
                    if name in List:
                        print("********if********")
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "verifying_group_chat_IM_users - User is avial in event list")
                    else:
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "verifying_group_chat_IM_users - User is avial in event list")
            elif params["user_list"] == "Endo":
                userlist = self._browser.elements_finder("first_panel_attandees")
                print(userlist)
                count = 0
                for user_name in userlist:
                    if user_name.text == name:
                        count = count + 1
                if count != 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "clicking_user_sending_IM - User is avial in event list")
                else:
                    raise AssertionError("User not present")

            elif params["user_list"] == "Endo_Im":
                userlist = self._browser.elements_finder("first_panel_conversation_item")
                print("length : ", len(userlist))
                count = 0
                for user_name in userlist:
                    print("*******")
                    print("from client ", user_name.text.split("\n")[0])
                    print("from testcase ", params["user"])
                    # user1=user_name.text
                    # List=user1.split()
                    if user_name.text.split("\n")[0] == name:
                        count = count + 1
                        break
                if count != 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verifying_group_chat_IM_users - User is avial in event list")
                else:
                    raise AssertionError("User not present")

            elif params["user_list"] == "Endo_Im1":
                userlist = self._browser.elements_finder("first_panel_conversation_item1")
                print(userlist)
                count = 0
                for user_name in userlist:
                    print("*******")
                    print(user_name.text)
                    userslist = []
                    user1 = user_name.text
                    List = user1.split()
                    if name in List:
                        count = count + 1
                        break
                if count != 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verifying_group_chat_IM_users - User is avial in event list")
                else:
                    raise AssertionError("User not present")

            elif params["user_list"] == "Endo_Group":
                userlist = self._browser.elements_finder("verify_people_group_chat")
                print(userlist)
                count = 0
                for user_name in userlist:
                    print("*******")
                    print(user_name.text)
                    print("*******************")
                    if user_name.text == name:
                        count = count + 1
                if count != 0:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verifying_group_chat_IM_users - User is avial in event list")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "error",
                                          "verifying_group_chat_IM_users - User is avial in event list")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verifying_group_chat_IM_users - user is replaced with group chat pane")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verifying_group_chat_IM_users - User is NOT avial in event list" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error verifying_group_chat_IM_users failed")

    def verifying_default_user_presence(self, **params):
        """
        Author : Surendra
        verifying_chat_IM_pane() - This API will verify IM pane
        parameter: message
        ex: verifying_chat_IM_pane
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verifying_chat_IM_pane - Exo user pane avaialability verification ")
            if params["user_list"] == "default_user":
                self.assertElement.page_should_contain_element("default_own_name")
            elif params["user_list"] == "single_chat":
                self.assertElement.page_should_contain_element("Exo_verify_single_chat")
            elif params["user_list"] == "verify_call":
                self.assertElement.page_should_contain_element("default_client_pane_user")
            else:
                raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verifying_chat_IM_pane - Exo pane is NOT avial in event list" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verifying_chat_IM_pane failed")

    def verifying_chat_IM_pane(self, **params):
        """
        Author : Surendra
        verifying_chat_IM_pane() - This API will verify IM pane
        parameter: message
        ex: verifying_chat_IM_pane
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verifying_chat_IM_pane - Exo user pane avaialability verification ")
            if params["user_list"] == "Exo_Group":
                user1 = re.sub("\*", " ", params["user1"])
                user2 = re.sub("\*", " ", params["user2"])
                user3 = re.sub("\*", " ", params["user3"])
                self.assertElement.page_should_contain_element("Exo_verify_group_initials1")
                userList = self.queryElement.get_text("Exo_verify_group_initials1")
                print("user list is " + userList)
                self.assertElement.page_should_contain_text("3 participants")
                print("##########All participants verified%%%%%%%%%%%%%%%")
                if user1 and user2 and user3 in userList:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verifying_chat_IM_pane - User is avial in event list")
                else:
                    print("user not in list")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verifying_chat_IM_pane - User is not in list")
            elif params["user_list"] == "single_chat":
                self.assertElement.page_should_contain_element("Exo_verify_single_chat")
            else:
                raise AssertionError("User not present")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verifying_chat_IM_pane - Exo pane is NOT avial in event list" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verifying_chat_IM_pane failed")

    def verifying_sending_IM_user_intial_right(self, **params):
        """
        Author : Surendra
        verifying_sending_IM_user_intial_right() - This API will verify for right sidetials for IM
        parameter: message
        ex: clicking_user_sending_IM
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verifying_sending_IM_user_intial_right - user avaialability verification ")
            if params["user_list"] == "Exo":
                # userlist = self._browser.elements_finder("Exo_group_chat_users")
                self.assertElement.page_should_contain_text(params["user"])
                # user_data = self.queryElement.get_text("Exo_chat_initial")
                # print("***************")
                # print(user_data)
                # if user_data in params["user"]:
                # log.mjLog.LogReporter("ManhattanComponent","info","verifying_sending_IM_user_intial_right - User is avial in event list")
                # else:
                # log.mjLog.LogReporter("ManhattanComponent","error","verifying_sending_IM_user_intial_right - User is avial in event list")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verifying_sending_IM_user_intial_right - user is replaced with group chat pane")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verifying_sending_IM_user_intial_right - User is NOT avial in event list" + str(
                                      sys.exc_info()))
            return False

    def play_pause_read_vms(self, **params):
        """
        Author : UKumar
        play_pause_read_vms() - This API plays or pauses
            the Voicemail which is marked as read either in Recent tab or in Third Panel
        Parameters: panel, option, vmNumber, playingDevice
        Ex1: play_pause_read_vms panel=recent/third option=play vmNumber=1, playingDevice=phone/computer
        EX2: play_pause_read_vms option=pause
        Extra Info.: vmNumber represents which vm to play
        """
        try:
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params['option'] == 'play':
                if params['panel'] == "recent":
                    read_vm = self._browser.elements_finder("recent_vm_read")
                else:
                    read_vm = self._browser.elements_finder("TP_read_vm")
                read_vm[int(params["vmNumber"]) - 1].click()
                if params["playingDevice"] == "phone":
                    self.webAction.click_element("recent_voicemail_play_through_phone")
                else:
                    self.webAction.click_element("recent_voicemail_play_through_computer")
                time.sleep(3)
                self.webAction.click_element("recent_voicemail_play")
                time.sleep(0.5)
                self.assertElement.element_should_be_displayed("recent_voicemail_pause")
                log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_read_vms"
                                                                    " - voicemail played")
            else:
                self.webAction.click_element("recent_voicemail_pause")
                self.assertElement.element_should_be_displayed("recent_voicemail_play")
                log.mjLog.LogReporter("ManhattanComponent", "info", "play_pause_read_vms"
                                                                    "- voicemail paused")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "play_pause_read_vms"
                                                                 "- error : " + str(sys.exc_info()))
            raise

    def verify_vm_comp_info(self, **params):
        """
        Author: Prashanth
        verify_voicemail_info() - To verify the voicemail history(recipient) in third panel
        Parameters: recipient
        Ex: verify_vm_comp_info forwarded=no sender=A recipient=ABC
        """
        try:
            self.thirdPanel.verify_vm_comp_info(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_vm_comp_info"
                                                                " - voicemail played through computer")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_vm_comp_info"
                                                                 " - Failed to verify computer-telephone")
            return False

    def verify_vm_type_indicator(self, **params):
        """
        Author: UKumar
        verify_vm_type_indicator() - To verify whether VM type (Urgent, Private etc.) are present
        Parameters: option and subject(optional)
        Ex: verify_vm_type_indicator option=urgent subject=ab*ok
        Extra Info.: pass option=all if you want to verify urgent and private both
        """
        try:
            vm_type_dict = {"urgent": "Recent_vm_indicate_urgent",
                            "private": "Recent_vm_indicate_private"
                            }
            if params["option"] == "all":
                self.assertElement.element_should_be_displayed("Recent_vm_indicate_urgent")
                self.assertElement.element_should_be_displayed("Recent_vm_indicate_private")
            else:
                self.assertElement.element_should_be_displayed(vm_type_dict[params["option"].lower()])
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_vm_type_indicator - indicator is present")
            if "subject" in params.keys():
                sub = re.sub("\*", " ", params["subject"])
                self.webAction.click_element("vm_unread")
                self.assertElement.page_should_contain_text(sub)
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_vm_type_indicator - subject is set")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_vm_type_indicator"
                                                                 " - failed to verify indicator " + str(sys.exc_info()))
            return False

    def add_new_label(self, **params):
        """
        Author: Ankit modified by prashanth
        add_new_label() - To add a new label and number under profile panel
        Parameters: label, number, activationType, no_of_rings
        Ex: add_new_label label=Label1 number=4084057489 activationType=1/2 no_of_rings=3
        """
        try:
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.add_new_label(**params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_new_label - new label added - PASS")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "add_new_label - unable to add new label - FAIL " + str(sys.exc_info()))
            return False

    def edit_modify_label(self, **params):
        """
        Author: UKumar
        edit_modify_label() - To edit and modify number added in add_new_label API
        Parameters: label_to_edit, new_label new_number, activationType, no_of_rings
        Ex: edit_modify_label label_to_edit=1/2, new_label=Label2 new_number=4084057485 activationType=1/2 no_of_rings=3
        """
        try:
            
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.edit_modify_label(**params)
            log.mjLog.LogReporter("ManhattanComponent","info","edit_modify_label - label modified - PASS")
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","edit_modify_label - failed to modify label "+str(sys.exc_info()))
            return False

    def remove_label(self, **params):
        """
        Author: UKumar
        remove_label() - To remove the label, number configured under profile panel
        Parameters: label_to_remove
        Ex: remove_label label_to_remove=1/2 label_name=abc
        """
        try:
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.remove_label(params["label_to_remove"])
            self.assertElement.element_should_not_contain_text("people_click_external", params["label_name"])
            log.mjLog.LogReporter("ManhattanComponent","info","remove_label - label removed")
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","remove_label - failed to remove label "+str(sys.exc_info()))
            return False

    def press_up_down_arrow(self, **params):
        '''
           press_up_down_arrow() - presses arrow_down or arrow_up
           parameters: arrow_option
           Ex1: press_up_down_arrow arrow_option=up/down
           Ex2: press_up_down_arrow arrow_option=up/down position=settings_window
           change list: added if condition for settings window and added parameter position(UKumar: 01-Aug-2016)
        '''
        try:
            if "position" in params.keys() and "position" == "settings_window":
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
                self.peopleGroup.press_up_down_arrow(params["arrow_option"])
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            else:
                self.peopleGroup.press_up_down_arrow(params["arrow_option"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "press_up_down_arrow"
                                                                " - %s arrow key pressed" % params["arrow_option"])

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "press_up_down_arrow"
                                                                 " - unable to press arrow option" + str(
                sys.exc_info()))
            return False

    def verify_route_slip(self, **params):
        """
        Author: Uttam
        verify_route_slip() - To verify the routing slip
            information during ongoingcall and after the call
        Parameters: when, entity, caller, receiver and callerExtn
        Ex: verify_route_slip when=afterCall entity=Calls caller=A receiver=B callerExtn=123
        Extra Info. : pass when=ongoingCall for verification during call
                      pass when=afterCall for verification after call
        """
        try:
            self.thirdPanel.select_routeslip_entity(params["entity"])
            time.sleep(20)
            if params["entity"] == "Calls":
                self.thirdPanel.verify_call_route_slip(params)

            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_route_slip"
                                                                " - routing slip verified")
            if params["verifySupportInfo"] == "yes":
                self.thirdPanel.verify_support_info()
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_route_slip"
                                                                    " - support info verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_route_slip"
                                                                 " - Failed to verify routing slip")
            return False

    def open_dialpad(self):
        """
        Author: Upendra
        Description: open the dial-pad on the default panel
        """
        try:
            self.defaultPanel.open_dialpad()
            self.assertElement.element_should_be_displayed("FP_dialpad")
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_dialpad - PASSED")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "open_dialpad - FAILED")
            return False

    def verify_dialpad(self):
        '''
        Author: Upendra
        Description: open the dial-pad on the default panel
        '''
        try:
            self.defaultPanel.verify_dialpad()
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_dialpad - PASSED")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_dialpad - FAILED")
            return False

    def click_dialpad_numbers(self, **params):
        """
        Author: Upendra
        Description: Dial the number from dial-pad
        parameters: eg: dial=one
        """
        try:
            self.defaultPanel.click_dialpad_numbers(params["dial"])
            time.sleep(2)
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_dialpad_numbers - PASSED")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_dialpad_numbers - FAILED")
            return False

    def close_dialpad_search(self):
        """
        Author: Upendra
        close_dialpad_search() - close the dial-pad search
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "close_dialpad_search - closing the dial-pad search...")
            self.webAction.click_element("Dialpad_close")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "close_dialpad_search - closed the dial-pad search successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "close_dialpad_search - failed to close the dial-pad search " + str(sys.exc_info()))
            return False

    def click_pin(self):
        '''
           Author: Prashanth
           click_pin() - To click on the pin in second panel and check it is pinned
           change list: added if else condition (UKumar: 1-Sep-2016)

        '''
        try:
            value = self.queryElement.element_not_displayed("default_pinned")
            if value:
                self.webAction.click_element("default_pin")
                self.assertElement.page_should_contain_element("default_pinned")
                log.mjLog.LogReporter("ManhattanComponent", "info", " click_pin"
                                                                    " - Clicked on pin button")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", " click_pin"
                                                                    " - pin button is already clicked")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", " click_pin "
                                                                 "- failed to click on pin button " + str(
                sys.exc_info()))
            return False

    def check_pinned(self):
        '''
           Author: Prashanth
           click_pin() - To click on the pin in second panel and check it is pinned

        '''
        try:
            # self.webAction.click_element("default_pin")
            self.assertElement.page_should_contain_element("default_pinned")


        except:
            log.mjLog.LogReporter("ManhattanComponent", "info", " check_pinned- Checking pinned" + str(sys.exc_info()))
            return False

    def click_pinned(self):
        '''
           Author: Prashanth
           click_pinned() - To click on the pinned in second panel and check it is unpinned


        '''
        try:
            self.webAction.click_element("default_pinned")
            self.assertElement.page_should_contain_element("default_pin")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " click_pinned- Clicking on pinned" + str(sys.exc_info()))
            return False

    def open_own_user_detail(self):
        """
        Author :Yogesh
        open_own_user_detail() : This api clicks on own nam ein dashboard to open details panel
        parameter : No Parameter
        """

        try:
            self.peopleGroup.open_own_user_detail()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "open_own_user_detail : successfully opened details panel")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "open_own_user_detail - Failed to open details panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_own_user_detail failed")

    def open_own_user_preferences(self):
        """
        Author: Gautham
        open_own_user_preferences() - open_own_user_preferences
        parameters:
        ex: open_own_user_preferences
        """
        try:
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            time.sleep(2)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.assertElement.element_should_be_displayed("preferences_telephony")
            self.assertElement.element_should_be_displayed("preferences_account")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "open_own_user_preferences - preferences window opened - PASS")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "open_own_user_preferences - unable to open preferences window"
                                  " - FAIL " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_own_user_preferences failed")

    def join_my_event(self, **params):
        '''
            Author : Prashanth
           join_my_event() - Clicks on my conference bridge,verifies & then clicks on join my event
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "join_my_event- clicking on conference bridge")
            self.webAction.click_element("default_own_name")
            time.sleep(2)
            self.webAction.click_element("second_panel_conferencebridge")
            time.sleep(1)
            self.assertElement.page_should_contain_text("My Conference")
            self.assertElement.page_should_contain_text("Extension")
            # self.assertElement.page_should_contain_text(params["Extension"])
            self.assertElement.page_should_contain_text("Number")
            # self.assertElement.page_should_contain_text("Host Code")
            self.assertElement.page_should_contain_text("Participant Code")
            self.assertElement.page_should_contain_text("Link")
            self.webAction.click_element("second_panel_joinmyevent")
            log.mjLog.LogReporter("ManhattanComponent", "info", "join_my_event : Clicked on join my event")
            time.sleep(20)
            self.webAction.click_element("first_panel_conferenceevent")
            self.webAction.press_key("call_external_number", "RETURN")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "call_external_number - Failed to call external number" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error call_external_number failed")

    def verify_second_panel(self, **params):
        """
        Author: UKumar
        verify_second_panel() - Verifies that second panel, either People tab or Recent tab or Events tab is opened or not
        Parameters: panelName and option
        Example: verify_second_panel panelName=people/recent/event option=present/absent
        """
        try:
            if params["panelName"].lower() == "people":
                self.peopleGroup.verify_people_panel(params["option"])
                log.mjLog.LogReporter("ManhattanComponent", "info", " verify_second_panel"
                                                                    " - second panel People verified")
            elif params["panelName"].lower() == "recent":
                self.recent.verify_recent_panel(params["option"])
                log.mjLog.LogReporter("ManhattanComponent", "info", " verify_second_panel"
                                                                    " - second panel Recent verified")
            else:
                self.event.verify_events_panel(params["option"])
                log.mjLog.LogReporter("ManhattanComponent", "info", " verify_second_panel"
                                                                    " - second panel Events verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info", " verify_second_panel -"
                                                                "failed to verify second panel " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_second_panel failed")

    def verify_third_panel(self, **params):
        """
        Author: UKumar
        verify_third_panel() - Verifies that third panel is opened or closed
        Parameters: option
        Example: verify_third_panel option=present/absent
        """
        try:
            status = self.queryElement.element_not_displayed("third_panel_minimize")
            if status and params["option"] == "absent":
                log.mjLog.LogReporter("ManhattanComponent", "info", " verify_third_panel"
                                                                    " - Third panel is closed")
            elif not status and params["option"] == "present":
                log.mjLog.LogReporter("ManhattanComponent", "info", " verify_third_panel"
                                                                    " - Third panel is opened")
            else:
                raise AssertionError("Failed to verify")

            if "verify" in params.keys():
                self.assertElement.element_should_be_displayed("peoples_panel_customer_name")
                self.assertElement.element_should_be_displayed("third_panel_messagefilter")
                self.webAction.click_element("third_panel_messagefilter")
                people_options = self._browser.elements_finder("third_panel_messagefiltergroup")
                print("**********The Value of Filter is **********  ", people_options)
                for option in people_options:
                    print("filter:")
                    people_check = option.text
                    Actual = ['Everything', 'Calls', 'Voicemails', 'Messages']
                    print("option:" + people_check)
                    if people_check in Actual:
                        print("The options are correct & verified")
                    else:
                        print("The options are not correct")


        except:
            log.mjLog.LogReporter("ManhattanComponent", "info", " verify_third_panel -"
                                                                "failed to verify third panel " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_third_panel failed")

    def click_filter_under_greeny_button(self, **params):
        """
        click_filter_under_greeny_button() - clicking option on beside dropdown green telephony buuton
        click_filter_under_greeny_button
        surendra
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_filter_under_greeny_button-  Checking alret when avaial option in conatct card")
            self.webAction.click_element("TP_close_conatct_green_tele")
            time.sleep(2)
            self.webAction.click_element("TP_close_contact_alert")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_filter_under_greeny_button- Failed to verify calls" + str(sys.exc_info()))
            return False

    def click_voicemail_ok(self, **params):

        try:
            self.webAction.click_element("default_OK")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " click_voicemail_ok- Pressing Ok Button for voicemail" + str(sys.exc_info()))
            return False

    def verify_user_notifications(self, **params):
        """
        Author : Surendra
        verify_user_notifications() - verifying user notificationis avial or not
        Parameters: user
        Ex: verify_user_notifications user=abc
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_user_notifications -  verifying user notification availability")
            self.webAction.explicit_wait("default_VM_user_name")
            user_name = self.queryElement.get_text("default_VM_user_name")
            if params["user"] in user_name:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_user_notifications -  User is available")
            else:
                raise AssertionError("User is not available")
            user_text = self.queryElement.get_text("default_VM_label")

            if ":" in user_text:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_user_notifications"
                                                                    " -  time HH:MM is available")
            else:
                raise AssertionError("HH:MM format is not available")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_user_notifications - Failed to verify notification " + str(sys.exc_info()))
            return False

    def verify_user_notifications_click(self, **params):
        """
        Author: surendra
        verify_user_notifications_click() - clicking option on beside dropdown green telephony buuton
        verify_user_notifications_click
        """
        try:
            self.webAction.click_element("default_VM_user_name")
            time.sleep(3)
            USER = self.queryElement.get_text("first_panle_user_verification")
            List = USER.split()
            if params["user"] in List:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_user_notifications_click"
                                                                    " -  User is available")
            else:
                raise AssertionError("User is not available")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_user_notifications_click"
                                                        " - Failed to click on notification " + str(sys.exc_info()))
            return False

    def verify_contact_listing(self):
        """
        Author: UKumar
        verify_contact_listing() - Clicks on search bar and verifies that contacts are listed
        EX: verify_contact_listing
        """
        try:
            self.webAction.click_element("default_name_number_search")
            self.webAction.explicit_wait("default_search_input")
            contact_list = self._browser.elements_finder("people_search")
            if len(contact_list) >= 4:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_listing - Contacts are listed")
            else:
                raise AssertionError("Contacts are not listed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_contact_listing"
                                                                 " - failed to verify contact listing " + str(
                sys.exc_info()))
            return False

    def display_group_list(self, **params):
        '''
           Display all contacts groups
           Change List: params[groupName] is changed to params (UKumar: 23-June-2016)
        '''
        try:
            log.mjLog.LogReporter("display_group_list", "info", "display_group_list - Entered")
            self.peopleGroup.group_tab()
            self.peopleGroup.display_grouplist(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "display_group_list - Group list displayed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "display_group_list - Unable to display group list" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error display_group_list failed")

# Added from old file as part of cleanup and integration of 133 CI cases with Sanity"""

    def check_presence_in_third_panel(self, **params):
        """
        Author: Uttam
        check_presence_in_third_panel() - This API checks the presence status and
                                          color of a user in third panel
        Parameters: personName and status
        Ex: check_presence_in_third_panel personName=abc status=Busy
        change list: removed both if condition and added code for searching of user(UKumar: 11-Aug-2016)
        """
        try:
            itemObject = self.defaultPanel.search_people_or_extension(params["personName"])
            itemObject.click()
            self.thirdPanel.check_presence_status_third_panel(params["status"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_presence_in_third_panel "
                                                                "- expected status matches with actual")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_presence_in_third_panel "
                                                                 "- expected status does not match with actual")
            raise Exception("ManhattanComponent error check_presence_in_third_panel failed")

    def add_participants_for_park_call(self, **params):
        """
        add_participants_for_park_call() - This API will add participants for park calling
        parameter: add_participants_for_park_call
        ex: add_participants_for_park_call option=park
        change list: removed sys.exc_info() from info log messages (UKumar: 16-Jan-2017)
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "add_participants_for_park_call-  Going to add participants for park calling")
            self.peopleGroup.park_transfer_call(params["user"])

            if params["option"].lower() == "park":
                self.webAction.explicit_wait("third_panel_transfer_park_option1")
                self.webAction.click_element('third_panel_transfer_park_option1')
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                    "add_participants_for_park_call-  able to click the park option")

            elif params["option"].lower() == "park_intercom":
                self.webAction.explicit_wait("third_panel_transfer_park_option3")
                self.webAction.click_element('third_panel_transfer_park_option3')
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                        "add_participants_for_park_call-  able to click the park&intercom option")

            elif params["option"].lower() == "park_page":
                self.webAction.explicit_wait("third_panel_transfer_park_option2")
                self.webAction.click_element('third_panel_transfer_park_option2')
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                    "add_participants_for_park_call-  able to click the park & page option")

            elif params["option"].lower() == "disable_park_intercom":
                self.assertElement.page_should_contain_element("TP_park_intercom_disable")

            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "add_participants_for_park_call-  participants for park calling added successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "add_participants_for_park_call - failed to add Paticipants for parkcalling" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error add_participants_for_park_call failed")

    def verify_park_call(self):
        """
        Author: Manoj
        verify_call_note() - To verify_park_call(
        Ex: verify_park_call
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_park_call-  Going to verifying park calling")
            time.sleep(5)
            self.webAction.click_element('first_panel_default_call')
            time.sleep(3)
            Hold_text = self.queryElement.get_text("default_client_pane_timer")
            print("value from text box : ", Hold_text)
            if 'put you ON HOLD' in Hold_text:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_park_call- successful in verifying the put on hold calling")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_park_call- Failed in verifying the put on hold calling" + str(
                                          sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_park_call- Failed to verifying park calling" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_park_call failed")

    def verify_click_user_dashboard(self, **params):
        """
        author : Manoj
        verify_click_user_dashboard() - this API verifies the contact name in call entry in dashboard and clciks on it
        ex1: verify_click_user_dashboard contact=abc
        """
        try:
            calllist = self._browser.elements_finder("default_OutG_CallName")
            for i in calllist:
                if params["contact"] in i.text.strip():
                    i.click()
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_click_user_dashboard"
                                          " - user verified in call entry in dashboard and clicked on call entry")
                    break
                else:
                    raise AssertionError("User %s not present in call entry" % params["contact"])
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_click_user_dashboard- failed to verify user in call entry " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_click_user_dashboard failed")

    def click_barge_call_in_client(self, **params):
        """
        Author: Manoj
        click_barge_call_in_client() - To Barge-In in a call
        Ex: click_barge_call_in_client
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_barge_call_in_client -  Going to Barge In")
            self.webAction.click_element('Tp_call_dropdown')
            time.sleep(2)
            if params["option"] == "enable":
                barge_in = False
                Enable_list = self._browser.elements_finder("Tp_call_dropdown_container")
                for extension in Enable_list:
                    if extension.text == 'Barge In':
                        extension.click()
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "click_barge_call_in_client - Clicked on Barge In")
                        barge_in = True
                        break
                #if barge_in:
                    #self.webAction.explicit_wait("third_panel_end_call")
                #    time.sleep(4)
                #    self.assertElement.element_should_be_displayed("third_panel_end_call")
                #    log.mjLog.LogReporter("ManhattanComponent", "info", "click_barge_call_in_client - Barge In successful")
                #else:
                #    raise AssertionError("Failed to Barge In")
            elif params["option"] == "disable":
                disable_list = self._browser.elements_finder("Tp_call_dropdown_container_disable_list")
                time.sleep(5)
                for extension in disable_list:
                    if 'Barge In' in extension.text:
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "click_barge_call_in_client- success in verifying barge in calling")
                    else:
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "click_barge_call_in_client- success in verifying barge in calling")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "click_barge_call_in_client- Failed in verifing barge in calling" + str(
                                          sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_barge_call_in_client- Failed to verifying park calling" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_barge_call_in_client failed")

    def verify_barge_call_in_client(self, **params):
        """
        Author: Manoj
        verify_barge_call_in_client() - To verify park text in user name
        Ex: verify_barge_call_in_client option = 'two_call_list'
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_barge_call_in_client-  Going to verifying park calling")
            if params["option"] == 'two_call_list':
                two_call_list = self._browser.elements_finder("first_panel_default_call")
                if len(two_call_list) == 2:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_barge_call_in_client- verifying barge in calling")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_barge_call_in_client- Failed in verifying barge in calling")
            elif params["option"] == 'one_call_list':
                one_call_list = self._browser.elements_finder("default_call_users")
                if len(one_call_list) == 2:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_barge_call_in_client- verifying barge in calling")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "verify_barge_call_in_client- Failed in verifying barge in calling")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_barge_call_in_client- Failed in verifying barge in calling")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_barge_call_in_client- Failed to verifying park calling" + str(sys.exc_info()))
            return False

    def verify_bargein_call(self, **params):
        """
        Author: Manoj
        verify_bargein_call() - To verify barge call status
        Parameters: callNote
        Ex: verify_bargein_call
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_bargein_call-  Going to verifying park calling")
            time.sleep(5)
            self.webAction.click_element('first_panel_default_call')
            time.sleep(3)
            Hold_text = self.queryElement.get_text("default_client_pane_timer")
            print("value from text box : ", Hold_text)
            if 'put you ON HOLD' in Hold_text:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_bargein_call- successful in verifying the put on hold calling")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_bargein_call- Failed in verifying the put on hold calling")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_bargein_call- Failed to verifying park calling " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_bargein_call failed")

    def verify_silent_moniter_mute_unmute(self, **params):
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_silent_moniter_mute_unmute-  Going to verifying park calling")
            if params["option"] == "mute":
                self.peopleGroup.mute_unmute_call()
                self.assertElement.page_should_contain_element("Tp_unmute")
            elif params["option"] == "unmute":
                time.sleep(3)
                self.webAction.click_element("Tp_unmute")
                self.assertElement.page_should_contain_element("third_panel_mute")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "verify_silent_moniter_mute_unmute- Failed to verifying silent monitoring calling" + str(
                                          sys.exc_info()))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_silent_moniter_mute_unmute- successful in verifying the silent monitoring calling" + str(
                                      sys.exc_info()))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_silent_moniter_mute_unmute- Failed to verifying silent monitoring calling" + str(
                                      sys.exc_info()))
            return False

    def check_user_mute_in_transfer(self, **params):
        '''
           Author: Manoj
           check_user_mute_in_transfer() - Check if a perticular attribute is available in third panel of user info
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_user_mute_in_transfer- Checking for the attribute in user info panel ")
            if params["check"] == "positive":
                self.assertElement._is_element_present("third_panel_mute")
            elif params["check"] == "negative":
                self.webAction.click_element("third_panel_mute")
                self.assertElement._is_element_present("Tp_unmute")
            else:
                raise AssertionError("wrong arguments passed !!")

            if "completetransfer" in params.keys():
                self.webAction.click_element("default_client_pane_completetransfer")
                time.sleep(3)
                print("###################Clicked on complete transfer%%%%%%%%%%%%%%%%%%%%%")
            else:
                print("No complete transfer to be done")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_user_mute_in_transfer- Attribute check is successfully completed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_user_mute_in_transfer- Attribute check failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error check_user_mute_in_transfer failed")

    def end_hold_call_from_client_pane(self, **params):
        '''
           Author: Gautham
           end_hold_call_from_client_pane() - Checks if hold and end button is visible in client pane of the user
                                              after mouse hover on the user in client pane and end or hold the
                                              call
           parameters: option: end: to click on end button in client pane
                       option: hold: to click on hold button in client pane
           ex: end_hold_call_from_client_pane option=hold

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "end_hold_call_from_client_pane- Verifying client pane")
            self.webAction.mouse_hover("default_client_pane_user1")
            if params["option"] == "hold":
                self.assertElement.element_should_be_displayed("default_client_pane_end_button")
                self.assertElement.element_should_be_displayed("default_client_pane_hold_button")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "end_hold_call_from_client_pane- hold and end button is visible after mouse hover")
            elif params["option"] == "end":
                # self.assertElement.element_should_be_displayed("default_client_pane_end_button")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "end_hold_call_from_client_pane- end button is visible after mouse hover")               
            self.peopleGroup.end_hold_from_client_pane(params["option"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "end_hold_call_from_client_pane- Button clicked successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "end_hold_call_from_client_pane- Failed to click button in client pane" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error end_hold_call_from_client_pane failed")

    def add_canned_message_whitespaces(self, **params):
        """
        Author: Upendra
        add_canned_message_whitespaces() - To create a canned message with max length
        parameters: message
        ex:  add_canned_message_whitespaces message=hi*how*r*u  with white spaces
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " add_canned_message_whitespaces- To add a canned message with white spaces")
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            time.sleep(2)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            message = re.sub("\*", " ", params["message"])

            self.setting.add_canned_message_whitespaces(message)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_canned_message_whitespaces"
                                                                " - Added a canned message with white spaces")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_canned_message_whitespaces"
                                                                 " - unable to add a canned message with white spaces" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error add_canned_message_whitespaces failed")

    def add_canned_message_without_option(self, **params):
        """
        Author: Upendra
        add_canned_message_without_option() - To create a canned message
        parameters: message
        ex:  add_canned_message_without_option message=hi*how*r*u  with white spaces
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " add_canned_message_without_option- To add a canned message with white spaces")
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            time.sleep(2)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            message = re.sub("\*", " ", params["message"])
            for x in range(0, 20):
                message = message + str(int(x))
                self.setting.add_canned_message_without_option(message)
            # self.peopleGroup.add_canned_message_without_option(message)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "add_canned_message_without_option - Added a canned message ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "add_canned_message_without_option - unable to add a canned message" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error add_canned_message_without_option failed")

    def Click_send_any_cannedresponse_incall(self):
        """
        Author: Manoj
        Click_send_any_cannedresponse_incall() - This API will click and sends the canned response while call in progress
        Ex: Click_send_any_cannedresponse_incall
        Extra Info: This API will click and sends the canned response while call in progress
        """
        try:
            log.mjLog.LogReporter(
                "Click_send_any_cannedresponse_incall() - This API will click and sends the canned response while call in progress")
            self.webAction.click_element("default_call_canned_resonse")
            time.sleep(3)
            list = self._browser.elements_finder("default_call_canned_resonse_list")
            noOfmsgs = 0
            for msg in list:
                noOfmsgs = noOfmsgs + 1
                can_message = msg.text
                print(can_message)
            if len(list) > 5:
                print("The length of list is : ", len(list))
                list[3].click()
            else:
                list[0].click()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Click_send_any_cannedresponse_incall - clicked and send response")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Click_send_any_cannedresponse_incall - failed to"
                                                                 " send canned response " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error Click_send_any_cannedresponse_incall failed")

    def verify_default_call_panel_click_vm(self):
        '''
            Author: Manoj
            verify_default_call_panel_click_vm() ---This api is to verify the defalut voice mail tab
            Ex: verify_default_call_panel_click_vm
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " verify_default_call_panel_click_vm- To verify dash board")
            time.sleep(2)
            self.assertElement.page_should_contain_text("Voice Mail")
            time.sleep(2)
            # self.webAction.click_element("default_IM_vm_notification")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_default_call_panel_click_vm- verifying the defalut voice mail tab")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_default_call_panel_click_vm- Failed to  verify the defalut voice mail tab" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error verify_default_call_panel_click_vm failed")

    def check_status_of_call_inStack(self, **params):
        """
        Author: kiran
        check_status_of_call_inStack() - this API checks the position of calls in dashboard stack and verify the call position
        Parameter: callName, verify
        Ex: check_status_of_call_inStack callName=user1 verify=firstCall/secondCall/thirdCall/fourthCall
        """
        try:
            if params["verify"] == "firstCall":
                dashBCall = self._browser.element_finder("people_TopCall_first")
            elif params["verify"] == "secondCall":
                dashBCall = self._browser.element_finder("people_TopCall_second")
            elif params["verify"] == "thirdCall":
                dashBCall = self._browser.element_finder("people_TopCall_third")
            elif params["verify"] == "fourthCall":
                dashBCall = self._browser.element_finder("people_TopCall_fourth")
            else:
                return False
                # dashBCall contains text as call name/hold/unhold/timer... so we are spliting it and compairing by call name
            print(dashBCall.text, params["callName"].replace("*", " "))
            if (params["callName"].replace("*", " ")) in dashBCall.text:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "top of call stack is matching with callname which is passed")
            else:
                raise AssertionError("call name is not matching with call name which is passed")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_status_of_call_inStack - failed"
                                                                 " to perform expected operation " + str(
                sys.exc_info()))
            return False

    def end_call(self, **params):
        '''
           end_call() - ends call in default panel
           ex1: end_call

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "end_call - to end a call in default panel")
            self.defaultPanel.end_call()
            log.mjLog.LogReporter("ManhattanComponent", "info", "end_call- call ended successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "end_call - unable to end call from default panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error end_call failed")

    def check_uncheck_routing_slip(self, **params):
        '''
           Author: Kiran
           check_uncheck_routing_slip() - To check/uncheck close_contact_card
           parameters: option
           ex: check_uncheck_routing_slip option=check/uncheck/checked/unchecked

        '''
        try:
            if "click" in params.keys():
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_uncheck_routing_slip - To check/uncheck close contact card")
                self.peopleGroup.open_own_user_detail()
                self.peopleGroup.open_own_user_preferences()
                time.sleep(2)
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
                self.webAction.explicit_wait("preferences_telephony")
                self.webAction.click_element("preferences_telephony")
                time.sleep(2)
                self.setting.check_uncheck_routing_slip(params)
                self.webAction.click_element("preferences_close_window")
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_uncheck_routing_slip- checked/unchecked close contact card")
            else:
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
                self.setting.check_uncheck_routing_slip(params)
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_uncheck_routing_slip- checked/unchecked close contact card")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_uncheck_routing_slip"
                                  " - unable to check/uncheck routing slip" + str(sys.exc_info()))
            return False

    def click_verify_routing_slip(self, **params):
        """
        Author: kiran
        click_verify_routing_slip() - To verify the routing slip
            information during ongoingcall and after the call
        Parameters: when, entity, caller, receiver and callerExtn
        Ex: click_verify_routing_slip verify/show/hide caller=im1
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_verify_routing_slip"
                                                                " - going to check routing slip")
            if "is_present" in params.keys():
                self.defaultPanel.click_verify_routing_slip_present(params)
            if "hide" in params.keys() and params["hide"] != "":
                self.defaultPanel.click_verify_routing_slip_hide(params)
            if "show" in params.keys() and params["show"] != "":
                self.defaultPanel.click_verify_routing_slip_show(params)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_verify_routing_slip"
                                                                 " - Failed to verify routing slip" + str(
                sys.exc_info()))
            return False

    def telephony_presence_status_with_contactlist(self, **params):
        '''
         author: Yogesh modified by Uttam
         presence_status_with_conactlist():verify selected group contacts list status with contacts
         parameters: groupName
         ex: select group  groupName=Bingo
        '''
        try:
            self.peopleGroup.group_select(params["groupName"])
            # self.webAction.click_element("third_panel_edit_group")
            # time.sleep(10)
            self.peopleGroup.telephony_third_panel_chm_status(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "telephony_presence_status_with_contactlist"
                                                                "    - contact is present with its expected status")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "telephony_presence_status_with_contactlist"
                                                                 " - list is empty " + str(sys.exc_info()))
            return False

    def click_mute_button(self, **params):
        '''
           Author: Iswarya
           click_mute_button() - To click mute button during call

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_mute_button- to be clicked")
            self.peopleGroup.click_mute_button(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_mute_button- clicked")
        except:
            try:
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_mute_button- checking second time")
                self.peopleGroup.click_mute_button(params)
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_mute_button- clicked")
            except:    
                log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "click_mute_button- Failed to click mute button" + str(sys.exc_info()))
                raise Exception("ManhattanComponent error click_mute_button failed")

    def presence_color_active(self, **params):
        '''
            Author : Prashanth
           presence_color_active() - Checks the color of the call & IM in dashboard by unholding call & connecting to another call
           parameter = color


        '''
        try:
            # new step
            if "clickcall" in params.keys():
                self.webAction.mouse_hover("default_client_pane_call1")
                print("###########moseover done##############")
                time.sleep(5)
                self.webAction.click_element("default_client_pane_hold_button")
                self.webAction.mouse_hover("default_client_pane_call2")
                print("###########moseover done##############")
                time.sleep(5)
                self.webAction.click_element("default_client_pane_unhold_button2")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on call successfully")

            if "clickcall2" in params.keys():
                self.webAction.mouse_hover("default_client_pane_call2")
                print("###########moseover done##############")
                time.sleep(5)
                self.webAction.click_element("default_client_pane_hold_button")
                self.webAction.mouse_hover("default_client_pane_call1")
                print("###########moseover done##############")
                time.sleep(5)
                self.webAction.click_element("default_client_pane_unhold_button1")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on call successfully")

            if "clickIM" in params.keys():
                self.webAction.click_element("default_IM")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on call successfully")

            if "clickarrow" in params.keys():
                self.webAction.click_element("default_clicktogglecall")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on downarrow successfully")
                time.sleep(5)
                rgb = self._browser.element_finder("default_callList").value_of_css_property("background-color")
                print("rgb : ", rgb)
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print("hex_color : ", hex_color)
                # item=self.queryElement._get_text("default_people_status")
                if "#FFFFFF" in hex_color:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "bubble_color----- and colour is White")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "call------ color  not found ")
                self.webAction.click_element("default_clicktogglecallclose")

            if "clickgroupIM" in params.keys():
                self.webAction.click_element("default_clickgroupIM")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on groupchat successfully")
                time.sleep(5)
                rgb = self._browser.element_finder("default_clickgroupIM").value_of_css_property("background-color")
                print("rgb : ", rgb)
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print("hex_color : ", hex_color)
                # item=self.queryElement._get_text("default_people_status")
                if "#d9d9d9" in hex_color:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "groupIM----- and colour is Grey")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "groupIM------ color  not found ")

            if "clickIMarrow" in params.keys():
                self.webAction.click_element("default_clicktogglecall")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on downarrow successfully")
                time.sleep(5)
                rgb = self._browser.element_finder("default_groupIM_users").value_of_css_property("background-color")
                print("rgb : ", rgb)
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print("hex_color : ", hex_color)
                # item=self.queryElement._get_text("default_people_status")
                if "#d9d9d9" in hex_color:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "GroupIM----- and colour is grey")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "call users------ color  not found ")

                self.webAction.click_element("default_clicktogglecallclose")

            if "clickIndgroupIM" in params.keys():
                self.webAction.click_element("default_clickINDIM")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "presence_color_active - Clicked on groupchat successfully")
                time.sleep(5)
                rgb = self._browser.element_finder("default_clickINDIM").value_of_css_property("background-color")
                print("rgb : ", rgb)
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print("hex_color : ", hex_color)
                # item=self.queryElement._get_text("default_people_status")
                if "#d9d9d9" in hex_color:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "groupIM----- and colour is Grey")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "groupIM------ color  not found ")

            if "verifygroupIM" in params.keys():
                log.mjLog.LogReporter("ManhattanComponent", "info", "presence_color_active - verifying group IM color")
                time.sleep(5)
                rgb = self._browser.element_finder("default_clickgroupIM").value_of_css_property("background-color")
                print("rgb : ", rgb)
                r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                hex_color = '#%02x%02x%02x' % (r, g, b)
                print("hex_color : ", hex_color)
                # item=self.queryElement._get_text("default_people_status")
                if "#FFFFFF" in hex_color:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "groupIM----- and colour is White")
                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "groupIM------ color  not found ")

            if "verifycolor" in params.keys():

                if "orange" in params.keys():
                    rgb = self._browser.element_finder("default_client_pane_color1").value_of_css_property(
                        "background-color")
                    print("rgb : ", rgb)
                    r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                    hex_color = '#%02x%02x%02x' % (r, g, b)
                    print("hex_color : ", hex_color)
                    # item=self.queryElement._get_text("default_people_status")
                    if "#ffd500" in hex_color:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "bubble_color----- and colour is Orange")

                elif "white" in params.keys():
                    rgb = self._browser.element_finder("default_client_pane_color2").value_of_css_property(
                        "background-color")
                    print("rgb : ", rgb)
                    r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                    hex_color = '#%02x%02x%02x' % (r, g, b)
                    print("hex_color : ", hex_color)
                    # item=self.queryElement._get_text("default_people_status")
                    if "#FFFFFF" in hex_color:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "bubble_color----- and colour is White")


                elif "grey" in params.keys():
                    rgb = self._browser.element_finder("default_client_pane_color3").value_of_css_property(
                        "background-color")
                    print("rgb : ", rgb)
                    r, g, b = map(int, re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+).*', rgb).groups())
                    hex_color = '#%02x%02x%02x' % (r, g, b)
                    print("hex_color : ", hex_color)
                    # item=self.queryElement._get_text("default_people_status")
                    if "#d9d9d9" in hex_color:
                        log.mjLog.LogReporter("ManhattanComponent", "info", "bubble_color----- and colour is grey")

                else:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "bubble_color------ color  not found ")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "bubble_color " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error bubble_color failed")

    def verify_Call_behaviour_items(self):
        """
        Author: Manoj
        verify_Call_behaviour_items() - This API checks the call
        Ex: verify_Call_behaviour_items
        """
        try:
            log.mjLog.LogReporter(
                "verify_Call_behaviour_items() - This API checks that dashboard call and verifies items in call")
            time.sleep(3)
            self.assertElement.element_should_be_displayed("default_client_pane_timer")
            self.assertElement.element_should_be_displayed("third_panel_hold_call123")
            self.assertElement.element_should_be_displayed("third_panel_end_call")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_Call_behaviour_items - able to verify all items in call")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_Call_behaviour_items - failed to"
                                                                 " receive IM " + str(sys.exc_info()))
            
            raise Exception("ManhattanComponent error verify_Call_behaviour_items failed")

    def verify_hold_user_dashboard(self, **params):
        """
        Author: UKumar
        verify_hold_user_dashboard() - This API verifies that callee's name and On Hold text is present in caller's dashboard
        Parameters: name and option
        Ex: verify_hold_user_dashboard name=uttam option=on_hold/put_you_on_hold
        """
        try:
            status = self.queryElement.element_not_displayed("default_onhold_timer")
            if status:
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_hold_user_dashboard"
                                                                    " - no call on hold indication")
            else:
                name = re.sub("\*", " ", params["name"])
                callee_name = self.queryElement.get_text("default_callee_name")
                if name == params["name"]:
                    if params["option"] == "on_hold":
                        self.assertElement.page_should_contain_element("default_onhold_timer")
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_hold_user_dashboard"
                                                                            " - Call is on hold for " + name + " and On Hold text is present")
                    else:
                        self.assertElement.page_should_contain_element("default_putyouonhold_timer")
                        log.mjLog.LogReporter("ManhattanComponent", "info", "verify_hold_user_dashboard"
                                                                            " - Call is on hold for " + name + " and put you On Hold text is present")
                else:
                    raise AssertionError("Call is not on hold")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_hold_user_dashboard - failed to"
                                                                 " verify call on hold " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_hold_user_dashboard failed")

    def blind_audio_conference_call(self, **params):
        """
        Author: Manoj
        blind_audio_conference_call() - This method clicks on conference and adds a third user to conference
        """
        try:
            self.user = params["user"]
            self.webAction.explicit_wait("third_panel_conf")
            self.webAction.click_element("third_panel_conf")
            self.webAction.explicit_wait("third_panel_conference_text")
            self.webAction.input_text("third_panel_conference_text", params["user"])
            self.webAction.explicit_wait("TP_chat_add_participants_user")
            self.webAction.click_element("TP_chat_add_participants_user")

            time.sleep(2)

            if params["option"] == "conference":
                self.webAction.explicit_wait("third_panel_blind_conf_click")
                self.webAction.click_element("third_panel_blind_conf_click")
                log.mjLog.LogReporter("PeopleGroup", "info", "blind_audio_conference_call"
                                                             " - user added to conference successfully")
            elif params["option"] == "Consult":
                self.webAction.explicit_wait("third_panel_blind_cons_click")
                self.webAction.click_element("third_panel_blind_cons_click")
                log.mjLog.LogReporter("PeopleGroup", "info", "blind_audio_conference_call"
                                                             " - user added to consult conference successfully")
            elif params["option"] == "Intercom":
                self.webAction.explicit_wait("TP_conf_intercom")
                self.webAction.click_element("TP_conf_intercom")
                log.mjLog.LogReporter("PeopleGroup", "info", "blind_audio_conference_call"
                                                             " - user added to Intercom conference successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", " blind_audio_conference_call"
                                                                 " - failed to add user to conference " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error blind_audio_conference_call failed")

    def click_merge_call(self, **params):
        '''
           click_merge_call() - merge a call
           parameters: contactName
           ex1: click_merge_call option=Merge_hold merge=yes

        '''
        try:
            time.sleep(1)
            if params["option"] == "merge":
                self.webAction.click_element("people_merge_call")
                time.sleep(2)
                self.assertElement.element_should_not_be_displayed("people_merge_call")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "click_merge_call - Merge button pressed to complete conference")
            if params["option"] == "Merge_hold":
                if "merge" in params.keys():
                    self.webAction.click_element("Dashboard_call_merge")
                    #self.webAction.click_element("Dashboard_call_merge_destination")
                    time.sleep(2)
                    self.webAction.click_element("FP_call_block")
                self.webAction.explicit_wait("third_panel_hold_call123")
                self.webAction.click_element("third_panel_hold_call123")
                text = self.queryElement.get_text("third_panel_transfer_park_held")
                if "On Hold" in text:
                    log.mjLog.LogReporter("ManhattanComponent", "info",
                                          "click_merge_call - 'On Hold' verified")
                self.webAction.click_element("third_panel_unhold_call")
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_merge_call- Merge and Hold-Unhold is completed")
            if params["option"] == "end_call":
                self.webAction.click_element("Dashboard_call_merge_toggle")
                Merged_end_list = self._browser.elements_finder("Dashboard_call_merge_end")
                Merged_end_list[0].click()
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_merge_call- double clicked over the contact")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_merge_call- Failed to Merge the call " + str(
                                      sys.exc_info()))
            return False

    def Click_send_cannedresponse_incall(self, **params):
        """
        Author: Manoj
        Click_send_cannedresponse_incall() - This API will click and sends the canned response while call in progress
        Parameters: status and message
        Ex: Click_send_cannedresponse_incall
        Extra Info: This API will click and sends the canned response while call in progress
        """
        try:
            log.mjLog.LogReporter(
                "Click_send_cannedresponse_incall() - This API will click and sends the canned response while call in progress")
            self.defaultPanel.ongoingcall_send_canned_response(params["response"])
            time.sleep(3)
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "Click_send_cannedresponse_incall - clicked and send response")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Click_send_cannedresponse_incall - failed to"
                                                                 " send canned response " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error Click_send_cannedresponse_incall failed")

    def click_verify_received_IMB(self, **params):
        """
        Author: Manoj
        click_verify_received_IMB() - This API checks that IM is received or not
        Parameters: status and message
        Ex: click_verify_received_IMB status=true message=hello
        Extra Info: if status=true then it will check for "IM is received"
                         otherwise it will check for "IM is not received"
        change list : added first statement to click on notification (UKumar: 9-Jan-2017)
        """
        try:
            self.webAction.click_element("first_panel_im_in_response_call")
            time.sleep(2)  # wait for IMs to load
            if params["status"].lower() == "true":
                self.assertElement.page_should_contain_text(params["message"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_verify_received_IMB - IM received")
            else:
                self.assertElement.page_should_not_contain_text(params["message"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "click_verify_received_IMB - IM did not receive")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_verify_received_IMB - failed to"
                                                                 " receive IM " + str(sys.exc_info()))
            return False

    def search_people_contact_remove_fav(self, **params):
        """
        Author : surendra
        search_people_contact_remove_fav() - search people by giving searchItem as name or number
        Parameters: searchItem
        Ex2 : search_people_contact_remove_fav searchItem=123 option=add
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "search_people_contact_remove_fav - Searching people by name ")
            self.searchItem = re.sub("\*\*", " ", params["searchItem"])
            self.defaultPanel.search_people_or_extension(self.searchItem)
            time.sleep(2)
            self.webAction.mouse_hover("peoples_favorite_on")
            self.webAction.click_element("peoples_favorite_on")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "search_people_contact_remove_fav - Searching people by name"
                                  " failed" + str(sys.exc_info()))
            return False

    def verify_preferences_call_routing_page(self):
        '''
           Author: Iswarya
           verify_preferences_call_routing_page() - To verify elements in call routing tab in own preferences
           ex:  verify_preferences_call_routing_page

        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " verify_preferences_call_routing_page- To verify call routing tab elements in preferences")
            time.sleep(1)
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            time.sleep(2)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            # self.webAction.explicit_wait("preferences_call_routing")
            self.setting.click_preference_call_routing()
            self.setting.verify_preferences_call_routing()
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_preferences_call_routing_page-elements verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_preferences_call_routing_page - unable to verify elements" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error verify_preferences_call_routing_page failed")

    def verify_preferences_power_routing_tab(self):
        '''
           Author: Iswarya
           verify_preferences_power_routing_tab() - To verify elements in power routing tab in own preferences
           ex:  verify_preferences_power_routing_tab

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " verify_preferences_power_routing_tab - To verify power routing tab elements in preferences")
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            time.sleep(3)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.setting.click_preference_call_routing()
            self.setting.verify_preferences_power_routing()
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_preferences_power_routing_tab - elements verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_preferences_power_routing_tab - unable to verify elements" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error verify_preferences_call_routing_page failed")

    def create_new_power_rule(self, **params):
        '''
           Author: Gautham
           create_new_power_rule() - To create a new power rule
           ex: create_new_power_rule ruleName=test

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            time.sleep(2)
            log.mjLog.LogReporter("ManhattanComponent", "info", " create_new_power_rule- creating a new power rule")
            self.setting.click_create_new_power_rule()
            self.webAction.explicit_wait("preferences_power_routing_rule")
            self.setting.enter_rule_name(params["ruleName"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "create_new_power_rule-New rule name entered successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "create_new_power_rule - Failed to enter a new rule name" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error create_new_power_rule failed")

    def click_on_my_availabilty(self):
        '''
           Author: Gautham
           click_on_my_availabilty() - To click on my availabilty
           ex: click_on_my_availabilty

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", " click_on_my_availabilty- clicking on my availabilty")
            self.setting.click_my_availabilty()
            self.webAction.explicit_wait("preferences_power_routing_availability_remove_button")
            self.assertElement.element_should_be_displayed("preferences_power_routing_available")
            self.assertElement.element_should_be_displayed("preferences_power_routing_inameeting")
            self.assertElement.element_should_be_displayed("preferences_power_routing_outofoffice")
            self.assertElement.element_should_be_displayed("preferences_power_routing_vacation")
            self.assertElement.element_should_be_displayed("preferences_power_routing_variable")
            self.assertElement.element_should_be_displayed("preferences_power_routing_dnd")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_on_my_availabilty-my availabilty opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_on_my_availabilty - Failed to open my availabilty" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_on_my_availabilty failed")

    def click_on_the_phone(self):
        '''
           Author: Gautham
           click_on_the_phone() - To click on (on the phone) option
           ex: click_on_the_phone

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", " click_on_the_phone- clicking on (on the phone)")
            self.setting.click_on_the_phone()
            self.webAction.explicit_wait("preferences_on_phone_remove_button")
            self.assertElement.page_should_contain_text("m on the phone")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_on_the_phone- (on the phone) opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_on_the_phone - Failed to open (on the phone)" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_on_the_phone failed")

    def click_on_number_matches(self):
        '''
           Author: Gautham
           click_on_number_matches() - To click on number matches
           ex: click_on_number_matches
               click_on_number_matches OR=yes -  this will also verify if OR is present between two number matches

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", " click_on_number_matches- clicking on number matches")
            self.setting.click_number_matches()
            if "OR" in params.keys():
                self.assertElement.page_should_contain_text("OR")
            # self.webAction.explicit_wait("preferences_number_matches_remove_button")
            # self.assertElement.element_should_be_displayed("preferences_number_matches_remove_button")
            self.webAction.explicit_wait("preference_number_matches_remove_1")
            self.assertElement.element_should_be_displayed("preference_number_matches_remove_1")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_on_number_matches-number matches opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_on_number_matches - Failed to open number matches" + str(sys.exc_info()))
            return False

    def add_number_matches(self, **params):
        '''
           Author: Gautham modified by Uttam
           add_number_matches() - To Add number details on number matches
           parameters: option=0 : The number is
                       option=1 : The number is any internal number
                       option=2 : The number is an internal extension starting with
                       option=3 : The number is an external number starting with
                       option=4 : The number is off system ext
                       option=5 : The number is private
                       option=6 : The number is out of area/unknown
                       text=10505 : extension number
           ex: add_number_matches option=0 text=10505
           change list: added regular expression in place of split(UKumar: 26-July-2016)
        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " add_number_matches- Adding number details on number matches")
            self.text = ""
            if "text" in params.keys():
                print("Inside the text block")
                self.text = re.sub("\*", " ", params["text"])
            self.firstName = ""
            self.lastName = ""
            self.number = ""
            if "firstName" in params.keys():
                self.firstName = params["firstName"]
            if "lastName" in params.keys():
                self.lastName = params["lastName"]
            self.name = self.firstName + " " + self.lastName
            if "number" in params.keys():
                self.number = params["number"]
            self.setting.add_number_matches(params["option"], self.name, self.number, self.text)
            # else:
            # print("Inside the else no text block")
            # self.peopleGroup.add_number_matches(params["option"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_number_matches - "
                                                                "Number details added successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_number_matches - "
                                                                 "Failed to add number details" + str(sys.exc_info()))
            return False

    def click_forward_call_button(self):
        '''
           Author: Gautham
           click_forward_call_button() - This method clicks on forward call button
           ex: click_forward_call_button

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " click_forward_call_button- clicking on forward call button")
            self.setting.click_forward_call_button()
            self.webAction.explicit_wait("preferences_submit_create_rule1")
            self.assertElement.element_should_be_displayed("preferences_submit_create_rule1")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_forward_call_button- forward call buttons opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_forward_call_button - Failed to open forward call button" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error click_forward_call_button failed")

    def configure_forward_call(self, **params):
        """
        Author: Uttam
        configure_forward_call() - This API selects on of the two radiobuttons
                                   presents inside "Forward Cal to" tab and
                                   enters values also
        Parameters: radio, optionOrText and ringtone=salsa(optional) firstName1=user(optional) firstName2=user1(optional) type =external(optional) type=name(optional) nameToAdd=user/external number(optional)
        Ex: configure_forward_call radio=dropdown optionOrText=Voicemail
        Extra Info.: pass radio=dropdown optionOrText=1 for Voicemail
                     pass radio=dropdown optionOrText=2 for Auto FindMe,
                     pass radio=dropdown optionOrText=3 for Announced FindMe
                     pass radio=dropdown optionOrText=4 for play ringtone ringtone=salsa
                     pass radio=text optionOrText="any text" to select textbox
                     and enter any valuue
        """
        try:
            forwordCallDict = {"1": "my voicemail", "2": "auto FindMe", "3": "announced FindMe", "4": "play ringtone"}
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            if params["radio"] == "dropdown":
                if "ringtone" in params.keys():
                    self.setting.choose_forward_call(forwordCallDict[params["optionOrText"]], \
                                                     params["ringtone"])
                else:
                    self.setting.choose_forward_call(forwordCallDict[params["optionOrText"]])
                log.mjLog.LogReporter("ManhattanComponent", "info", "configure_forward_call"
                                                                    " - " + forwordCallDict[
                                          params["optionOrText"]] + " is selected")
            else:
                self.setting.add_user_forward_callto(params)

                log.mjLog.LogReporter("ManhattanComponent", "info", "configure_forward_call "
                                                                    "- " + params[
                                          "optionOrText"] + " number is entered")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "configure_forward_call"
                                                                 " - Failed to enter values " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error configure_forward_call failed")

    def configure_my_availabilty(self, **params):
        '''
           Author: Gautham
           configure_my_availabilty() - To configure my availabilty option
           ex1: configure_my_availabilty text=available
           ex2: configure_my_availabilty text=inameeting
           ex3: configure_my_availabilty text=outofoffice
           ex4: configure_my_availabilty text=vacation
           ex5: configure_my_availabilty text=variable
           ex6: configure_my_availabilty text=dnd

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " configure_my_availabilty- Adding my availabilty details")
            self.setting.add_my_availabilty(params["text"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "configure_my_availabilty-my availabilty details added successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "configure_my_availabilty - Failed to add my availabilty details" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error configure_my_availabilty failed")

    def create_rule_check_error(self, **params):
        """
        Author: Uttam
        create_rule_check_error() - This API clicks on create rule button
                            and checks if there is any error, if no error
                            is there then it will create the rule
        Parameters: ruleName and tabName (tabName is name of area under
                                        which you want to check error)
        Ex: create_rule_check_error ruleName=Rule1 tabName=timeisDay
            tabName=timeisDay
            tabname=timeisTime
            tabName=my_availability
            tabName=noCondition
            tabName=forward_call_to
            tabName=number_matches
            tabName=ruleName
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.webAction.click_element("preferences_submit_create_rule1")
            time.sleep(1)
            status = self.queryElement.text_present(params["ruleName"])
            if status is False:
                self.setting.check_rule_error(params["tabName"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "create_rule_check_error"
                                                                    " - error occurred during creation of rule")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "create_rule_check_error"
                                                                    " - " + params[
                                          "ruleName"] + " created successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "create_rule_check_error -"
                                                                 " Failed to create the rule")
            raise Exception("ManhattanComponent error create_rule_check_error failed")

    def edit_rule(self, **params):
        '''
           Author: Gautham
           edit_rule() - To click on edit rule option on call power routing
           ex: edit_rule ruleName=test

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", " edit_rule- editing rule")
            self.setting.click_on_edit_rule(params["ruleName"])
            log.mjLog.LogReporter("ManhattanComponent", "info", " edit_rule- clicked on edit rule name editing rule")
            self.webAction.explicit_wait("preferences_edit_save_rule")
            self.assertElement.element_should_be_displayed("preferences_edit_save_rule")
            log.mjLog.LogReporter("ManhattanComponent", "info", "edit_rule- edit rule opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "edit_rule - Failed to open edit rule" + str(sys.exc_info()))
            return False

    def edit_rule_check_error(self, **params):
        """
        Author: Uttam
        edit_rule_check_error() - This API clicks on save rule button and
                            checks if there is any error, if no error is
                            there then it will create the rule
        Parameters: ruleName and tabName (tabName is name of part under
                                        which you want to check error)
        Ex: edit_rule_check_error ruleName=Rule1 tabName=timeisDay
            tabName=timeisDay
            tabname=timeisTime
            tabName=my_availability
            tabName=noCondition
            tabName=forward_call_to
            tabName=ruleName
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.webAction.click_element("preferences_edit_save_rule")
            time.sleep(1)
            status = self.queryElement.text_present(params["ruleName"])
            if status is False:
                self.setting.check_rule_error(params["tabName"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "edit_rule_check_error"
                                                                    " - error occurred during saving the rule")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info", "edit_rule_check_error"
                                                                    " - " + params["ruleName"] + " saved successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "edit_rule_check_error -"
                                                                 " Failed to edit the rule")
            return False

    def save_rule(self, **params):
        '''
           Author: Gautham
           save_rule() - Save rule and check if rule saved
           ex: save_rule ruleName=test

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", " save_rule- Saving rule")
            self.setting.save_rule()
            self.assertElement.page_should_contain_text(params["ruleName"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "save_rule- Rule saved successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "save_rule - save rule Failed" + str(sys.exc_info()))
            return False

    def remove_rule_option(self, **params):
        '''
           Author: Gautham
           remove_rule_option() - This method removes an option from the rule
           ex: remove_rule_option option=number_matches
               remove_rule_option option=dialed_number
               remove_rule_option option=my_availability
               remove_rule_option option=on_the_phone
               remove_rule_option option=time_is
        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", " remove_rule_option- Removing an option")
            xp = self.setting.remove_rule_option(params["option"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "remove_rule_option- option removed successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "remove_rule_option - Failed to remove option" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error remove_rule_option failed")

    def to_check_incoming_IM_voiceMail(self, **params):
        '''
           Author: Gautham
           to_check_incoming_IM_voiceMail() - To check if IM or voicemail notification is selected or unselected
           Parameters: option=im: for Incoming IM
                       option=voiceMail: for Incoming Voicemail
                       check=positive: to check if the option is selected
                       check=negative: to check if the option is unselected
           ex: to_check_incoming_IM_voiceMail option=im check=positive
           '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "to_check_incoming_IM_voiceMail - Checking popup notification check box")
            if params["option"] == "im":
                self.setting.check_incoming_IM(params["check"])
            elif params["option"] == "voiceMail":
                self.setting.check_incoming_voiceMail(params["check"])
            else:
                raise AssertionError("Wrong arguments passed !!")
            log.mjLog.LogReporter("ManhattanComponent", "info", "to_check_incoming_IM_voiceMail- PASS")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "to_check_incoming_IM_voiceMail - FAIL" + str(sys.exc_info()))
            return False

    def open_notifications_tab(self):
        '''
           Author: Gautham
           open_notifications_tab() - To open notifications tab in preferences window
           ex: open_notifications_tab
           '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_notifications_tab - Opening notifications tab")
            self.setting.click_notifications_tab()
            self.webAction.explicit_wait("preferences_notifications_popup")
            self.assertElement.element_should_be_displayed("preferences_notifications_popup")
            self.assertElement.element_should_be_displayed("preferences_notifications_sounds")
            self.assertElement.element_should_be_displayed("preferences_notifications_voicemail")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "open_notifications_tab- Notifications tab opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "open_notifications_tab - Failed to open notifications tab" + str(sys.exc_info()))
            return False

    def open_preferences_notifications_popup(self):
        '''
           Author: Gautham
           open_preferences_notifications_popup() - This method opens popup tab under notifications in preferences window
           ex: open_preferences_notifications_popup
        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " open_preferences_notifications_popup- Opening popup tab")
            self.setting.click_notifications_popup()
            self.webAction.explicit_wait("preferences_notifications_incoming_voicemail")
            self.assertElement.element_should_be_displayed("preferences_notifications_incoming_voicemail")
            self.assertElement.element_should_be_displayed("preferences_notifications_incoming_im")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "open_preferences_notifications_popup- Popup tab opened successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "open_preferences_notifications_popup - Failed to open Popup tab" + str(
                                      sys.exc_info()))
            return False

    def check_uncheck_popup_option(self, **params):
        '''
           Author: Gautham
           check_uncheck_popup_option() - This method select or unselect incoming IM or ncoming Voicemail
                                          option under popup in Notifications tab
           Parameters: option=im: for Incoming IM
                       option=voiceMail: for Incoming Voicemail
                       check=true: to select the option
                       check=false: to unselect the option
           ex: check_uncheck_popup_option option=im check=true
           ex: check_uncheck_popup_option option=im check=false
           change list: added if "notification_time" in params.keys(): (UKumar: 27-July-2016)
        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " check_uncheck_popup_option- select or unselect the option")
            if params["option"] == "im":
                self.setting.check_uncheck_incoming_IM(params["check"])
                if "notification_time" in params.keys():
                    self.webAction.select_from_dropdown_using_text("preferences_notifications_im_dropdown",
                                                                   params["notification_time"])
                    pass
            elif params["option"] == "voiceMail":
                self.setting.check_uncheck_incoming_voiceMail(params["check"])
            else:
                raise AssertionError("Wrong arguments passed !!")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_uncheck_popup_option- option selected or unselected successfully")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))

            if "close" in params.keys():
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
                self.webAction.click_element("TP_close")
                self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "check_uncheck_popup_option - Failed to select or unselect the option" + str(
                                      sys.exc_info()))
            return False

    def verify_preferences_basic_routing_change_panels(self, **params):
        '''
           Author: Manoj
           verify_preferences_basic_routing_rules_change_panels() - To verify the change button near basic routing rule redirects to corresponding page
           option=simulring/inc_call/findme/vm_greeting/interacting_greeting1/interacting_greeting2
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " verify_preferences_basic_routing_rules_change_panels- Verifying rules change button panels in basic routing tab under call routing")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.setting.verify_preferences_basic_routing_change_panels(params["option"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_preferences_basic_routing_rules_change_panels-basic routing rules change button for given rule is been verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_preferences_basic_routing_rules_change_panels - Failed to verify basic routing rules change button panels" + str(
                                      sys.exc_info()))
            return False

    def interacting_with_greeting_allow_VM(self, **params):
        '''
           Author: Gautham
           interacting_with_greeting_allow_VM() - To check if 'callers can leave a voice mail' option is selected or not
                                                at Interacting with Greeting page under Basic routing
           parameters: allow=yes: API pass if 'callers can leave a voice mail' option is selected
                       allow=no: API pass if 'callers will not be able to leave a voice mail' option is selected
           ex: interacting_with_greeting_allow_VM allow=yes

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "interacting_with_greeting_allow_VM- Checking if callers can leave VM or not")
            if params["allow"] == "yes":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "interacting_with_greeting_allow_VM- --callers can leave a voice mail-- option is selected")
            elif params["allow"] == "no":
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "interacting_with_greeting_allow_VM- --callers will not be able to leave a voice mail-- option is selected")
            else:
                raise AssertionError("error checking option")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "interacting_with_greeting_allow_VM- Wrong voice mail option selected under Interacting with greeting page" + str(
                                      sys.exc_info()))
            return False

    def verify_findme_panel_number(self, **params):

        """
        Author : Vishwas
        verify_findme_panel_number() - This method verifies the Home or Work or
        any other number specified is present in a particular page.
        Params: number1 and number2
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            time.sleep(2)
            message_1 = params["number1"]
            print(message_1)
            split_msg = message_1.split("*")
            message_1 = " ".join(split_msg)

            message_2 = params["number2"]
            print(message_2)
            split_msg = message_2.split("*")
            message_2 = " ".join(split_msg)
            if (self.assertElement._is_text_present(message_1) or self.assertElement._is_text_present(message_2)):
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_findme_panel_number - verified basic routing configuration page elements and Number found")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_findme_panel_number - verified basic routing configuration page elements and number not present")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_findme_panel_number - error while verifying numbers in FindMe page " + str(
                                      sys.exc_info()))
            return False

    def close_preferences_window(self):
        '''
           Author: Gautham
           close_preferences_window() - To close preferences window
           ex: close_preferences_window

        '''
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " close_preferences_window- closing preferences window")
            self.setting.close_preferences_window()
            time.sleep(2)
            windows_count = self.webAction.window_handles_count()
            if windows_count == 2:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "close_preferences_window- preferences window closed successfully")
            else:
                raise
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "close_preferences_window - Failed to close preferences window" + str(
                                      sys.exc_info()))
            raise Exception("ManhattanComponent error close_preferences_window failed")

    def add_or_remove_select_number_in_findme_panel(self, **params):
        """
        Author: Indresh
        add_or_remove_select_number_in_findme_panel() - adds find me numbers in Findme panel
        params: labelName, number
        """
        try:
            self.setting.add_or_remove_select_number_in_findme_panel(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_or_remove_select_number_in_findme_panel"
                                                                " - clicked on selected number")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_or_remove_select_number_in_findme_panel"
                                                                 " - failed to click on selected number " + str(
                sys.exc_info()))
            raise

    def check_ring_my_findme_numbers(self):
        """
        Author: Indresh
        check_ring_my_findme_numbers() - checks Ring my FindMe numbers sequentially before playing my voicemail
        """
        try:
            self.webAction.click_element("pref_ring_my_findme_numbers")
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_ring_my_findme_numbers"
                                                                " - clicked on Ring my FindMe numbers sequentially before playing my voicemail")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_ring_my_findme_numbers"
                                                                 " - failed to click on Ring my FindMe numbers sequentially before playing my voicemail" + str(
                sys.exc_info()))
            raise

    def save_call_routing_setting(self):
        """
        Author: Indresh
        save_call_routing_setting() - checks Ring my FindMe numbers sequentially before playing my voicemail
        """
        try:
            self.webAction.click_element("pref_save_call_routing_settings")
            log.mjLog.LogReporter("ManhattanComponent", "info", "save_call_routing_setting"
                                                                " - clicked on Ring my FindMe numbers sequentially before playing my voicemail")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "save_call_routing_setting"
                                                                 " - failed to click on Ring my FindMe numbers sequentially before playing my voicemail" + str(
                sys.exc_info()))
            raise

    def verify_recent_counter_badge(self, **params):
        """
        verify_recent_counter_badge() - verifies recent counter badge number
        Parameters: badgeNo tab
        Ex: verify_recent_counter_badge badgeNo=1 tab=voicemail/messages/recent
        """
        try:
            self.defaultPanel.verify_recent_counter_badge(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_recent_counter_badge"
                                                                " - badge count verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_recent_counter_badge"
                                                                 " - failed to verify badge count " + str(
                sys.exc_info()))
            raise

            # ####################################################################################"""

    def cleanup(self, **params):
        """
        Author: UKumar
        cleanup() - To clear the setings made by test cases
        """
        try:
            self.webAction.click_element("default_people_tab")
            time.sleep(1)
            value = self.queryElement.element_not_displayed("default_pin")
            if value:
                self.webAction.click_element("default_pinned")
                self.assertElement.page_should_contain_element("default_pin")
                log.mjLog.LogReporter("ManhattanComponent", "info", " cleanup"
                                                                    " - Clicked on pinned button")
            bigA_Selected = self.queryElement.element_not_displayed("peoples_bigA_selected")
            if bigA_Selected:
                self.webAction.click_element("peoples_bigA")
                log.mjLog.LogReporter("ManhattanComponent", "info", " cleanup"
                                                                    " - bigA view selected")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", " cleanup "
                                                                 "- failed to do cleanup " + str(sys.exc_info()))
            return False


# Added for Sanity Automation by UKumar

    def invoke_dashboard_tab(self, **params):
        '''
        Author: Vijay Ravi
        invoke_dashboard_tab - To Open any of the tabs on the Dashboard Ex: Voicemail / IM / WG/ Events
        parameters: option
        ex: invoke_dashboard_tab option=people/recent/voicemail/messages/event
        '''
        try:
            if params["option"].lower() == "people":
                self.defaultPanel.invoke_peoplelist()
                log.mjLog.LogReporter("ManhattanComponent", "info", "invoke_dashboard_tab"
                                                                    " - People tab opened successfully")
            elif params["option"].lower() == "recent":
                self.defaultPanel.invoke_recent_tab()
                log.mjLog.LogReporter("ManhattanComponent", "info", "invoke_dashboard_tab"
                                                                    " - Recent tab opened successfully")
            elif params["option"].lower() == "voicemail":
                self.defaultPanel.invoke_voicemails_tab()
                log.mjLog.LogReporter("ManhattanComponent", "info", "invoke_dashboard_tab"
                                                                    " - Voicemail tab opened successfully")
            elif params["option"].lower() == "messages":
                return self.defaultPanel.invoke_messages_tab()
                log.mjLog.LogReporter("ManhattanComponent", "info", "invoke_dashboard_tab"
                                                                    " - Messages tab opened successfully")
            elif params["option"].lower() == "workgroups":
                self.defaultPanel.invoke_workgroups_tab()
                log.mjLog.LogReporter("ManhattanComponent", "info", "invoke_dashboard_tab"
                                                                    " - Workgroups tab opened successfully")
            else:                
                self.defaultPanel.invoke_events_tab()
                log.mjLog.LogReporter("ManhattanComponent", "info", "open_events_tab- Events tab opened successfully")
                if "exchange_username" in params.keys():
                    exchange_credentials_required = self.queryElement.element_not_displayed("event_exchange_username")
                    if not exchange_credentials_required:
                        self.event.enter_exchange_credentials(params["exchange_username"], params["exchange_password"])
                        log.mjLog.LogReporter("ManhattanComponent", "info", "open_events_tab"
                                                                            " - Exchange credentials submitted.")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "invoke_dashboard_tab -"
                                                                 " Failed to open a tab in the Dashboard " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error invoke_dashboard_tab failed")

    def select_tab(self, **params):
        """
        Author: Vijay Ravi
        select_tab  - This API selects a tab in the specified panel.
        parameters: tab name panel name
        ex: select_tab tabName=all panelName=voicemail
        """
        try:
            if params["tabName"] == "all":
                if params["panelName"] == "voicemail":
                    self.webAction.click_element("voicemail_all_tab")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "select_tab - Clicked on All tab under Voicemail tab")

                elif params["panelName"] == "recent":
                    self.webAction.click_element("recent_all_tab")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "select_tab - Clicked on All tab under Recent tab")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "select_tab -"
                                                                 " failed to select " + params["tabName"] + " tab.")
            raise Exception("ManhattanComponent error select_tab failed")

    def upgrade_client(self, **params):
        """
        Author: UKumar
        upgrade_client() - To upgrade connect client
        Parameters: username and password
        Ex: upgrade_client username=ukumar password=hello
        """
        try:
            self.common_func.login(params['username'], params['password'], params['server_address'])
            self.webAction.explicit_wait("default_panel_upgrade_button")
            self.webAction.click_element("default_panel_upgrade_button")
            log.mjLog.LogReporter("ManhattanComponent", "info", "upgrade_client - Clicked on upgrade button")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", " upgrade_client "
                                                                 "- failed to click on upgrade button " + str(
                sys.exc_info()))
            raise

    def install_client(self, **params):
        """
        Author: UKumar
        install_client() - To interact with installer of connect client (For Upgrade)
        Parameters: installation_folder
        Ex: install_client installation_folder=C:\Client
        Extra Info: installation_folder parameter is optional, if you would not pass,
                    the client will be installed in C:\\NodeWebKit\\
        """
        try:
            install_folder = "C:\\NodeWebKit\\"
            if "installation_folder" in params.keys():
                install_folder = params['installation_folder']
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - waiting for installer window")
            # whnld = autoit.win_wait("ShoreTel Connect - InstallShield Wizard", 15)
            whnld = autoit.win_wait("[CLASS:MsiDialogCloseClass]", 20)
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - installer window appeared")
            autoit.win_activate("[CLASS:MsiDialogCloseClass]")

            # is_enabled = autoit.control_command("[CLASS:MsiDialogCloseClass]", "Button1", "IsEnabled")
            is_next_enabled = autoit.control_command("[CLASS:MsiDialogCloseClass]", "&Next >", "IsEnabled")
            while (is_next_enabled != "1"):
                is_next_enabled = autoit.control_command("[CLASS:MsiDialogCloseClass]", "&Next >", "IsEnabled")
                time.sleep(5)

            # Click on Next button
            ##autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button1")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "&Next >")
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - clicked on next button")

            # Accept license agreement and click Next
            time.sleep(2)
            ##autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button3")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "I &accept the terms in the license agreement")
            time.sleep(1)
            ##autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button5")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "&Next >")
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - accepted license agreement"
                                                                " and clicked on next button")

            # Change installation folder and Click on Next
            time.sleep(2)
            ##autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button3")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "&Change...")  # Click on Change
            time.sleep(1)
            autoit.control_send("[CLASS:MsiDialogCloseClass]", "RichEdit20W1", install_folder)  # give folder name
            time.sleep(1)
            ##autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button1")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "OK")  # Click on OK
            time.sleep(1)
            # autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button1")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "&Next >")
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - installation folder"
                                                                " changed and clicked on next button")

            # Click on Install
            time.sleep(1)
            ##autoit.control_click("[CLASS: MsiDialogCloseClass]", "Button1")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "&Install")
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - clicked on install button")

            # Wait for installation to finish
            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - waiting for install to finish")
            time.sleep(100)
            is_finish_enabled = autoit.control_command("[CLASS:MsiDialogCloseClass]", "&Finish", "IsEnabled")
            #log.mjLog.LogReporter("ManhattanComponent","info", "install_client - finish button found %s" type(is_finish_enabled))

            while is_finish_enabled != "1":
                is_finish_enabled = autoit.control_command("[CLASS:MsiDialogCloseClass]", "&Finish", "IsEnabled")
                log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - state " + is_finish_enabled)
                time.sleep(10)

            # Click on Finish button
            autoit.win_activate("ShoreTel Connect - InstallShield Wizard")
            autoit.control_click("[CLASS:MsiDialogCloseClass]", "&Finish")

            log.mjLog.LogReporter("ManhattanComponent", "info", "install_client - clicked on Finish button")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "install_client "
                                                                 "- failed to interact with installer " + str(
                sys.exc_info()))
            return False

    def send_meeting_request_outlook(self, **params):
        """
        Author: UKumar
        send_meeting_request_outlook() - This API sends the meeting request from the outlook
        Parameters: option and meeting_name
        Ex: send_meeting_request_outlook option=cancel_meeting_invite
            send_meeting_request_outlook option=send_meeting_invite meeting_name=test
        """
        try:
            if params["option"] == "send_meeting_invite":
                self.event.send_meeting_request_for_invite()
                #time.sleep(5)  # waiting for event to appear in Upcoming tab
                self.event.verify_event_appeared(params["meeting_name"])
                # self.assertElement.page_should_contain_text(params["meeting_name"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "send_meeting_request_outlook - event created")
            else:
                self.event.send_meeting_request_for_cancel()
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "send_meeting_request_outlook - Failed to create event")
            raise Exception("ManhattanComponent error send_meeting_request_outlook failed")

    def click_first_ongoing_event(self):
        """
        click_first_ongoing_event() - This API click on first ongoing event from the dashboard panel
        Ex: click_first_ongoing_event 
        """
        try:
            time.sleep(2)
            self.webAction.click_element("FP_first_ongoing_event")            
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_first_ongoing_event - clicked on first ongoing event")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_first_ongoing_event - not able to click on first ongoing event")
            raise Exception("ManhattanComponent error click_first_ongoing_event failed")

    def cancel_event(self):
        """
        cancel_event() - This API click on given event in events tab and then click on cancel
        Ex: cancel_event
        """
        try:
            self.webAction.click_element("TP_event_cancel")
            time.sleep(3)  # wait for playing screen to appear (Explicit wait not working here)
            self.webAction.click_element("TP_event_cancel_yes")
            log.mjLog.LogReporter("ManhattanComponent", "info", "cancel_event - canceled the event")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "cancel_event - not able to delete the event")
            raise Exception("ManhattanComponent error cancel_event failed")

    def record_conference(self, **params):
        """
        Author: UKumar
        record_conference() - This API records the conference
        Parameters: option
        Ex: record_conference option=start_recording/stop_recording
        """
        try:
            if params["option"] == "start_recording":
                self.webAction.click_element("event_start_recording")
                if not self.queryElement.element_not_displayed("event_recording_notification"):
                    self.webAction.click_element("event_recording_notification")
                self.assertElement.element_should_be_displayed("event_stop_recording")
                log.mjLog.LogReporter("ManhattanComponent", "info", "record_conference - conference recording started.")
            else:
                self.webAction.click_element("event_stop_recording")
                self.assertElement.element_should_be_displayed("event_start_recording")
                log.mjLog.LogReporter("ManhattanComponent", "info", "record_conference - conference recording stopped.")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "record_conference - Failed to record conference")
            raise Exception("ManhattanComponent error record_conference failed")

    def play_download_delete_recording(self, **params):
        """
        Author: UKumar
        play_download_delete_recording() - This API plays recording through client, downloads
                            recording and deletes recording according to the parameters passed
        Parameters: option and download_file_path
        Ex: play_download_delete_recording option=play
            play_download_delete_recording option=download download_file_path=C:\\download\\recording.zip
            play_download_delete_recording option=delete
        """
        try:
            time.sleep(1)
            self.webAction.click_element("event_recording_arrow")
            recording_options = self._browser.elements_finder("event_recording_options")

            if params["option"] == "play":
                self.event.play_recording_through_client(recording_options[0])
                time.sleep(3)  # wait for playing screen to appear
                self.assertElement.element_should_be_displayed("event_recording_playing_screen")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "play_download_delete_recording - recording started palying.")
            elif params["option"] == "download":
                download_path = "C:\\Recordings\\recording.zip"
                if "download_file_path" in params.keys():
                    download_path = params["download_file_path"]
                self.event.download_recording(recording_options[1], download_path)
                time.sleep(4)
                client_utils.unzip_recording(download_path)
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "play_download_delete_recording - recording downloaded.")
            else:
                # not yet implemented
                # self.event.delete_recording(recording_options[3])
                # log.mjLog.LogReporter("ManhattanComponent", "info", "play_download_delete_recording - recording deleted.")
                pass
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "play_download_delete_recording"
                                                                 " - Failed to either play or download or delete conference!")
            raise Exception("ManhattanComponent error play_download_delete_recording failed")

    def configure_meeting_settings(self, **params):
        """
        Author: UKumar
        configure_meeting_settings() - This API plays recording through client, downloads
                            recording and deletes recording according to the parameters passed
        Parameters: option and download_file_path
        Ex: configure_meeting_settings option=dial_out_to_participants join_audio=press_one/automatic
        """
        try:
            if params["option"] == "dial_out_to_participants":
                self.event.set_dial_out_participant(params["join_audio"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "configure_meeting_settings"
                                                                    " - dial out to participants setting done.")
            else:
                # not yet implemented
                pass
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "configure_meeting_settings"
                                                                 " - Failed to configure meeting settings!")
            raise Exception("ManhattanComponent error configure_meeting_settings failed")

    def open_conference_panel(self, **params):
        """
        Author: UKumar
        open_conference_panel() - This API click on meeting entry in dashboard
                to open conference panel to chat, share or for call me options
        Parameters: event_name
        Ex: open_conference_panel event_name=example_event
        """
        try:
            entries = self._browser.elements_finder("default_event_entry")
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_conference_panel - %s" % entries[0].text)
            if params["event_name"] in entries[0].text:
                entries[0].click()
            time.sleep(2)
            self.assertElement.element_should_be_displayed("third_panel_share")
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_conference_panel"
                                                                " - conference panel opened.")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "open_conference_panel"
                                                                 " - Failed to open conference panel! " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error open_conference_panel failed")

    def close_conference_entry(self, **params):
        """
        Author: UKumar
        close_conference_entry() - This API removes the conference entry from dashboard
        Parameters: option
        Ex: close_conference_entry option=organizer/participant/presenter
        Extra Info: first use this api to remove entry from organizer's dashboard
                    after that use it for participants or presenters
        """
        try:
            if not self.queryElement.element_not_displayed("event_leave_goodbye_conf"):
                self.webAction.click_element("event_leave_goodbye_conf")
                time.sleep(1)
            conferenceEntries = self._browser.elements_finder("event_conference_entry")
            conferenceEntryCloseButtons =  self._browser.elements_finder("event_close_conf_dashboard")
            for conferenceEntry, conferenceEntryCloseButton in zip(conferenceEntries, conferenceEntryCloseButtons):
                ActionChains(self._browser.get_current_browser()).move_to_element(conferenceEntry).perform()
                time.sleep(0.5)
                conferenceEntryCloseButton.click()
                time.sleep(1)

                if  params["option"].lower() == "organizer" and not self.queryElement.element_not_displayed("event_leave_end_conf"):
                    self.webAction.click_element("event_leave_end_conf")

                if  params["option"].lower() != "organizer" and not self.queryElement.element_not_displayed("event_leave_conf_yes"):
                    self.webAction.click_element("event_leave_conf_yes")

            if not self.queryElement.element_not_displayed("event_leave_goodbye_conf"):
                self.webAction.click_element("event_leave_goodbye_conf")

            log.mjLog.LogReporter("ManhattanComponent", "info", "close_conference_entry"
                                                                " - conference entry removed.")
        except:
            if "retry" not in params:
                params["retry"] = 1
                self.close_conference_entry(params)
            else:
                log.mjLog.LogReporter("ManhattanComponent", "error", "close_conference_entry"
                                                                    " - Failed to conference entry removed!")
                raise Exception("ManhattanComponent error close_conference_entry failed")

    def join_event_by_callme(self, **params):
        """
        Author: UKumar
        join_event_by_callme() - This API dials an internal extension or
                    external number to join conference through call me feature
                    either from endo client or from Exo client
        Parameters: option and number
        Ex: join_event_by_callme option=end/exo number=123
        """
        try:
            if params["option"] == "endo":
                self.event.callme_from_endo(params["number"])
            else:
                self.event.callme_from_exo(params["number"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "join_event_by_callme"
                                                                " - joined event using Call Me button.")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "join_event_by_callme"
                                                                 " - Failed to join by Call Me feature!")
            raise Exception("ManhattanComponent error join_event_by_callme failed")

    # Sprint 4
    def initiate_search_and_close(self, **params):
        """
        Author: UKumar
        initiate_search_and_close() - This API initiates search by typing in
                    dialer box and presses ESCAPE to close the search results
        Parameters: search_item
        Ex: initiate_search_and_close search_item=mnh
        """
        try:
            self.defaultPanel.initiate_verify_search(params["search_item"])
            self.defaultPanel.close_verify_search()
            log.mjLog.LogReporter("ManhattanComponent", "info", "initiate_search_and_close"
                                                                " - verified search operation successfull")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "initiate_search_and_close"
                                                                 " - Failed to verify search operation!")
            return False

    def scroll_search_results_use_keyboard(self, **params):
        """
        Author: UKumar
        scroll_search_results_use_keyboard() - This API scrolls through search results using up or down arrow key
        Parameters: search_item, scroll_option
        Ex: scroll_search_results_use_keyboard search_item=mnh scroll_option=up/down
        """
        try:
            if params["scroll_option"] == "down":
                self.peopleGroup.scroll_down_use_keyboard(params["search_item"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "scroll_search_results_use_keyboard"
                                                                    " - scrolled successfully using keyboard")
            else:
                # Not yet implemented
                pass
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "scroll_search_results_use_keyboard"
                                                                 " - Failed to verify search operation!")
            return False

    def show_contact_info_right_click(self, **params):
        """
        Author: UKumar
        show_contact_info_right_click() - This API right clicks on searched contact
                    and clicks on any of the options identified by parameter option to
                    show or hide the information
        Parameters: option, contact_info and info_to_verify
        Ex: show_contact_info_right_click option=show contact_info=phone_number info_to_verify=148
            show_contact_info_right_click option=show contact_info=dept_name info_to_verify=Sales
            show_contact_info_right_click option=show contact_info=company_name info_to_verify=ShoreTel
            show_contact_info_right_click option=hide contact_info=phone_number
        """
        try:
            if params["option"].lower() == "show":
                if params["contact_info"] == "phone_number":
                    self.peopleGroup.show_verify_phone_number(params["info_to_verify"])
                    log.mjLog.LogReporter("ManhattanComponent", "info", "show_contact_info_right_click"
                                                                        " - Toggle Phone Number, completed")
                elif params["contact_info"] == "dept_name":
                    self.peopleGroup.show_verify_dept_name(params["info_to_verify"])
                    log.mjLog.LogReporter("ManhattanComponent", "info", "show_contact_info_right_click"
                                                                        " - Toggle department name, completed")
                elif params["contact_info"] == "company_name":
                    self.peopleGroup.show_verify_comp_name(params["info_to_verify"])
                    log.mjLog.LogReporter("ManhattanComponent", "info", "show_contact_info_right_click"
                                                                        " - Toggle company name, completed")
                else:
                    # can be extended for other options
                    pass
            else:
                self.peopleGroup.hide_contact_info(params["contact_info"])
                log.mjLog.LogReporter("ManhattanComponent", "info", "show_contact_info_right_click - Contact info is not visible")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "show_contact_info_right_click"
                                                                 " - Failed to Click on searched results options!")
            raise

    def call_by_click_number_searched_contact(self):
        """
        Author : UKumar
        call_by_click_number_searched_contact() - To place a call to searched contact
                by single clicking on phone number revealed via right click
        Parameters: no parameter
        Ex: call_by_click_number_searched_contact
        """
        try:
            self.webAction.click_element("people_right_click_number")
            self.assertElement.element_should_be_displayed("third_panel_end_call")
            log.mjLog.LogReporter("ManhattanClient", "info", "call_by_click_number_searched_contact"
                                                             " - call placed by clicking on number")
        except:
            log.mjLog.LogReporter("ManhattanClient", "error", "call_by_click_number_searched_contact"
                                                              " - Failed to place call by clicking on number")
            return False

    def open_outlook_tab(self):
        """
        Author : UKumar
        open_outlook_tab() - To open Outlook tab in Settings window
        Parameters: no parameters
        Ex: open_outlook_tab
        """
        try:
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            time.sleep(5)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.assertElement.element_should_be_displayed("preferences_outlook")
            self.webAction.click_element("preferences_outlook")
            log.mjLog.LogReporter("ManhattanClient", "info", "open_outlook_tab - Outlook tab opened")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanClient", "error", "open_outlook_tab - Failed to open Outlook tab "+str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_outlook_tab failed")

    def configure_outlook_tab(self, **params):
        """
        Author : UKumar
        configure_outlook_tab() - To configure various options present on outlook tab
        Parameters: option
        Ex: configure_outlook_tab option=contacts donot_open_outlook=check/uncheck
            configure_outlook_tab option=calendar
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            if params["option"].lower() == "calendar":
                # not yet implemented
                pass
            else:
                self.setting.configure_outlook_options(params)
                log.mjLog.LogReporter("ManhattanClient", "info", "configure_outlook_tab"
                                                                 " - options under contacts are configured")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanClient", "error", "configure_outlook_tab"
                                                              " - Failed to configure Outlook tab")
            raise Exception("ManhattanComponent error configure_outlook_tab failed")

    def check_uncheck_close_contact_card(self, **params):
        '''
           Author: Prashanth
           check_uncheck_close_contact_card() - To check/uncheck close_contact_card
           parameters: option
           ex: check_uncheck_close_contact_card option=check/uncheck/checked/unchecked
        '''
        try:
            if "click" in params.keys():
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "check_uncheck_close_contact_card - To check/uncheck close contact card")
                self.peopleGroup.open_own_user_detail()
                self.peopleGroup.open_own_user_preferences()
            time.sleep(3)  # wait for Settings window to appear
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.setting.check_uncheck_close_contact_card(params)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "check_uncheck_close_contact_card - checked/unchecked close contact card")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_uncheck_close_contact_card"
                                  " - unable to check/uncheck close contact card" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error check_uncheck_close_contact_card failed")

    def configure_sounds_tab(self, **params):
        """
        author:uttam
        configure_sounds_tab() - This API perofrms various action on the entities
                                    under preferences->Notifications->Sounds
        parameters: radio
        ex: configure_sounds_tab radio=off
            configure_sounds_tab radio=on eventName=1 for "new voicemail"
            configure_sounds_tab radio=on eventName=2 for "call from an internal number"
            configure_sounds_tab radio=on eventName=3 for "call from an external number"
            configure_sounds_tab radio=on eventName=4 for "new IM message initiating a new conversation"
        change list: added st3 statement(UKumar: 28-July-2016)
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            if params["radio"] == "off":
                self.webAction.click_element("preferences_notif_sounds_OFF")
                st1 = self.queryElement.element_enabled("preferences_notif_sounds_remSound")
                st2 = self.queryElement.element_enabled("preferences_notif_sounds_addSound")
                st3 = self.queryElement.element_enabled("preferences_notif_sounds_play")
                if not st1 and not st2 and not st3:
                    log.mjLog.LogReporter("ManhattanComponent", "info", "configure_sounds_tab"
                                                                        " - Audio Alert is OFF")
            else:
                self.webAction.click_element("preferences_notif_sounds_ON")
                self.assertElement.element_should_be_selected("preferences_notif_sounds_ON")
                self.setting.set_Forevent_sounds(params["eventName"])
                if "alert" in params.keys():
                    self.setting.configure_alert_sound(params)
                    log.mjLog.LogReporter("ManhattanComponent", "info", "configure_sounds_tab - "
                                                                        "alert configured")
                else:
                    self.assertElement.element_should_be_selected("preferences_notif_sounds_PA_radio")
                    log.mjLog.LogReporter("ManhattanComponent", "info", "configure_sounds_tab - "
                                                                        "Event and Play alert is selected")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "configure_sounds_tab - "
                                                                 "Failed to configure Sounds tab " + str(
                sys.exc_info()))
            return False

    def click_entity_notify(self, **params):
        """
        author:uttam
        click_entity_notify() - This API opens preferences->Notifications tab, checks
                             for the present tabs and clicks on the tab identified by
                             tabName and verifies the elements present under that tab
        parameters: tabName
        click_entity_notify tabName=Voicemail
        """
        try:
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            time.sleep(3)  # explicit_wait is not working
            # self.webAction.explicit_wait("preferences_notifications")
            self.webAction.click_element("preferences_notifications")
            self.assertElement.element_should_be_displayed("preferences_notifications_voicemail")
            self.assertElement.element_should_be_displayed("preferences_notifications_sounds")
            self.assertElement.element_should_be_displayed("preferences_notifications_popup")
            if "tabName" in params.keys():
                self.setting.verify_entity_notify(params["tabName"])

            log.mjLog.LogReporter("ManhattanComponent", "info", "click_entity_notify -"
                                                                " Notifications tab clicked")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_entity_notify -"
                                                                 " Failed to click Notifications tab")
            return False

    def add_user_to_blocked_list(self, **params):
        """
        add_user_to_blocked_list() - This API adds a user identified by
                                    username to a blocked list of another user
        parameters: username
        ex: add_user_to_blocked_list username1=User_DB1_01
        extra info.: if you want to pass one user then write username1=abd
                     for two users pass username1=abd username2=xyz
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            contactlist = []
            for key in params.keys():
                if "username" in key:
                    contactlist.append(params[key])
            self.setting.add_user_to_blocked_list(contactlist)
            # self.assertElement.element_should_contain_text("preferences_IM_BlockNotif_contact", params["username"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "add_user_to_blocked_list"
                                                                " - User added to blocked list")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "add_user_to_blocked_list"
                                                                 " - Failed to add user to blocked list")
            return False

    def open_IM_panel(self, **params):
        """
        open_IM_panel() - This APIs Opens preferences->IM panel
        parameters: no parameter
        ex: open_IM_panel
        """
        try:
            self.peopleGroup.open_own_user_detail()
            self.peopleGroup.open_own_user_preferences()
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            time.sleep(3)
            self.webAction.click_element("preferences_im")
            self.assertElement.element_should_be_displayed("preferences_IM_BlockNotif")
            log.mjLog.LogReporter("ManhattanComponent", "info", "open_IM_panel - IM panel opened")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "open_IM_panel - Failed to open"
                                                                 " IM panel" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_IM_panel failed")

    def click_block_notify_IM(self, **params):
        """
        click_block_notify_IM() - This API clicks on "Block Notifications" tab under IM
        parameters: no parameter
        ex: click_block_notify_IM
        """
        try:
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.webAction.click_element("preferences_IM_BlockNotif")
            self.assertElement.element_should_be_displayed("preferences_IM_BlockNotif_IMChat_label")
            self.assertElement.element_should_be_displayed("preferences_IM_BlockNotif_GrpChat_label")
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_block_notify_IM - Block Notification"
                                                                " tab clicked")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "click_block_notify_IM - Failed to Block"
                                                                 " Notification tab " + str(sys.exc_info()))
            return False

    def delete_draft(self, **params):
        """
        Author : UKumar
        delete_draft() - To delete the draft for group, contact and event
        Parameters: option
        Ex: delete_draft option=contact/group/event entity_name=abc
        """
        try:
            if params["option"] == "contact":
                # not yet implemented
                pass
            elif params["option"] == "group":
                # not yet implemented
                pass
            else:
                self.defaultPanel.delete_event_draft()
                self.assertElement.page_should_not_contain_text(params["entity_name"])
                log.mjLog.LogReporter("ManhattanClient", "info", "delete_draft"
                                                                 " - Event draft deleted")
        except:
            log.mjLog.LogReporter("ManhattanClient", "error", "delete_draft"
                                                              " - Failed to delete draft")
            return False
            
# By Prashanth
    def select_phone_type(self, **params):
        """
        Author: Prashanth
        select_phone_type(): This API selects the softphone or deskphone option for a user
        parameters: phone_type
        EX: select_phone_type phone_type=soft_phone/desk_phone
        """
        try:
            self.peopleGroup.open_own_user_detail()
            if params["phone_type"].lower() == "soft_phone":
                self.peopleGroup.select_soft_phone(params)
                log.mjLog.LogReporter("ManhattanComponent", "info", "select_phone_type - Softphone selected")
            else:
                self.peopleGroup.select_desk_phone(params)
                log.mjLog.LogReporter("ManhattanComponent", "info", "select_phone_type - Deskphone selected")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "select_phone_type - FAILED" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error select_phone_type failed")

    def check_badge_count(self, **params):
        """
        Author: Vijay Ravi
        check_badge_count() : This API checks for badge count in the dashboard
        Parameter: tab
        Ex1: check_badge_count tab=voicemail
        Ex2: check_badge_count tab=recent
        """
        try:
            time.sleep(3)
            if params["tab"] == "messages":
                self.webAction.explicit_wait("first_panel_messages_badge_no")
            elif params["tab"] == "voicemail":
                self.webAction.explicit_wait("first_panel_voicemail_badge_no")
            elif params["tab"] == "recent":
                self.webAction.explicit_wait("first_panel_recent_badge_no")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_badge_count"
                                                                 " - Failed to check VM badge count " + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error check_badge_count failed")

    def open_contact_card(self, **params):
        """
        Author: UKumar
        open_contact_card() - Opens contact card of a user either by clicking on it from Favorites or from any Group
            or by clicking on an entry in Recent
        Parameters: option, name
        Ex: open_contact_card option=favorites/groups name=abc
            open_contact_card option=recent
        Extra info: before using this API for recent use invoke_dashboard_tab API
        """
        try:
            if params["option"] == "favorites":
                name = params["name"].lstrip("{").rstrip("}")
                self.webAction.click_element("peoples_favorite_tab")
                self.peopleGroup.open_contact_from_favourites(name)
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "open_contact_card - clicked on a user under Favorite to open contact card")
            elif params["option"] == "groups":
                name = params["name"].lstrip("{").rstrip("}")
                self.webAction.click_element("peoples_group")
                contact_list = self._browser.elements_finder("peoples_search_name_group")
                for user in contact_list:
                    if user.text.strip() == name:
                        user.click()
                        log.mjLog.LogReporter("ManhattanComponent", "info",
                                              "open_contact_card - clicked on a user under Groups to open contact card")
                        break
            else:
                recent_entries = self._browser.elements_finder("recent_history_name")
                time.sleep(1)
                recent_entries[0].click()
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "open_contact_card - clicked on a Recent entry to open contact card")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "open_contact_card - Failed to click on user " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error open_contact_card failed")

    def verify_dial_button_dropdown(self, **params):
        '''
           Author: prashanth
           verify_dial_button_dropdown() - Click on dropdown near dial button & verify the multiple numbers appearing
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_dial_button_dropdown- clicking on dropdown dial button")
            self.webAction.click_element("people_options")
            time.sleep(3)
            #self.assertElement.page_should_contain_text("mobile")
            self.assertElement.page_should_contain_text("home")
            #self.assertElement.page_should_contain_text(params["mobile"])
            #self.assertElement.page_should_contain_text(params["home"])
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_dial_button_dropdown- clicking on first favourite ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_dial_button_dropdown- Failed to click" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_dial_button_dropdown failed")

    def click_first_result_in_directory(self):
        """
        click_first_result_in_directory() - This API will click on directory &then open the contact card of first user
        parameter: message
        ex: click_first_result_in_directory
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_first_result_in_directory - going to click verify_im_textarea")
            self.webAction.click_element("default_name_number_search")
            time.sleep(1)
            self.webAction.explicit_wait("default_search_input")
            firstname = self.queryElement.get_text("FP_directory_firstname")

            contactlist = self._browser.elements_finder("people_search")
            contactlist[0].click()
            return firstname
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_first_result_in_directory - failed to verify test area" + str(sys.exc_info()))
            return False

    def verify_route_slip_third_panel(self, **params):
        """
        verify_route_slip_third_panel() - This API will click on first item on recent history
        ex: verify_route_slip_third_panel    caller=807564321
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_first_result_in_recent - going to click first item in recent all tab")
            self.webAction.explicit_wait("recent_all_tab_first_item")
            self.webAction.click_element("recent_all_tab_first_item")
            self.webAction.explicit_wait("TP_first_recent_entry")
            self.webAction.click_element("TP_first_recent_entry")
            time.sleep(1)
            self.assertElement.element_should_contain_text("TP_first_recent_entry_routing_slip_origin", (str("+91 ") + params["caller"][1:]))
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_first_result_in_search - failed to verify test area" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_route_slip_third_panel failed")

    def click_first_visible_result_in_search(self):
        """
        click_first_result_in_search() - This API will click on directory &then open the contact card of first user
        parameter: message
        ex: click_first_visible_result_in_search
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_first_visible_result_in_search - going to click on first visible contact")
            self.webAction.click_element("First_visible_contact")
            time.sleep(1)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_first_visible_result_in_search - failed to verify test area" + str(sys.exc_info()))
            return False

    def event_joineeinfo(self, **params):
        '''
           Author: Prashanth
           event_joineeinfo() - To click on the info button & verify the attendees of the event
        '''
        try:
            self.webAction.explicit_wait("event_info")
            self.webAction.click_element("event_info")
            # self.assertElement.page_should_contain_element("event_availability")
            self.assertElement.page_should_contain_element("event_attendee_name")
            name = re.sub("\*", " ", params["name"])
            self.assertElement.page_should_contain_text(name)

        except:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  " event_joineeinfo- failed to verify attendee" + str(sys.exc_info()))
            return False

    def create_meeting_outlook(self, **params):
        """
        Author: prashanth
        create_meeting_outlook() - Creating a meeting/event via Outlook
        Parameters: meeting_name, recipient1 and recipient2
        Ex: create_meeting_outlook meeting_name=anyName recipient1=xyz@qa.shoretel.com recipient2=abc@qa.shoretel.com
        """
        try:
            from datetime import datetime
            from datetime import timedelta
            import win32com.client

            oOutlook = win32com.client.Dispatch("Outlook.Application")
            appt = oOutlook.CreateItem(1)  # 1 - olAppointmentItem
            appt.MeetingStatus = 1  # 1 - olMeeting; Changing the appointment to meeting
            # only after changing the meeting status recipients can be added
            now = datetime.now()
            plus2 = timedelta(seconds=30)
            start = now + plus2
            start_time = start.strftime('%Y-%m-%d %H:%M:%S')
            appt.Start = start_time
            appt.Subject = params["meeting_name"]
            appt.Duration = 30
            appt.Location = 'Office - Room 132A'

            appt.Recipients.Add(params["recipient1"])
            appt.Recipients.Add(params["recipient2"])

            appt.Save()
            appt.Send()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "create_meeting_outlook - Meeting request sent to outlook")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "create_meeting_outlook - Failed to create meeting through outlook" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error create_meeting_outlook failed")

    def call_contact_from_recent_history(self, **params):
        """
        call_contact_from_recent_history() - For making a call either by double clicking on a Recent entry
                or by clicking on a number in recent history
        parameters: option and contact_name
        ex1: call_contact_from_recent_history option=double_click_on_entry/click_on_number contact_name=abc

        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "call_contact_from_recent_history- Invoke recent history list ")
            if params["option"] == "double_click_on_entry":
                self.recent.call_double_click_recent_entry(params["contact_name"])
            else:
                if "contact_name" in params:
                    self.recent.call_click_number_recent_entry(params["contact_name"])
                else:                    
                    self.recent.call_click_number_recent_entry()
            self.webAction.explicit_wait("default_call_end_button")
            self.assertElement.element_should_be_displayed("default_call_end_button")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "call_contact_from_recent_history- call placed from recent entry")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "call_contact_from_recent_history"
                                                                 " - Failed to make call from recent entry" + str(sys.exc_info()))
            return False

    def tab_away(self):
        """
        Author: prashanth
        tab_away() : This api does alt tab on exo client
        """
        try:
            #autoit.win_activate(title)          
            #autoit.send("[CLASS:Chrome_WidgetWin_1]" , "Chrome_RenderWidgetHostHWND1", "!{TAB}")
            #autoit.send("[TITLE:%s]" %(title), "Chrome_RenderWidgetHostHWND1", "{ENTER}")
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            #pyautogui.press('tab')
            #pyautogui.press('tab')
            pyautogui.keyUp('alt')
            log.mjLog.LogReporter("ManhattanComponent", "info", "tab_away - successfully completed the tab away ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "tab_away - Failed to do tab away" + str(sys.exc_info()))
            return False

    def remove_conversation(self, **params):
        """
        Author: Vijay Ravi
        remove_conversation() - This API removes the required IM conversation
        Parameters: search_im_entry_by, message and username
        Ex: remove_conversation search_im_entry_by=im message=hello
            remove_conversation search_im_entry_by=username username1=abc username2=def
        """
        try:
            self.message.remove_im_conversation(params)
            log.mjLog.LogReporter("ManhattanComponent", "info", "remove_conversation - removed conversation")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "remove_conversation - failed to"
                                                        " remove conversation" + str(sys.exc_info()))
            return False

    def mark_im_as_read(self, **params):
        """
        Author: Vijay Ravi
        mark_im_as_read() - This API marks the required IM conversation as read
        Parameters: message
        Ex: mark_im_as_read message=hello
        """
        try:
            self.message.mark_as_read_im_conversation(re.sub("\*", " ", params["message"]))
            log.mjLog.LogReporter("ManhattanComponent", "info", "mark_im_as_read - marked conversation as read")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "mark_im_as_read - failed to"
                                                         " mark conversation as read" + str(sys.exc_info()))
            return False

    def check_first_recent_call_type(self, **params):
        """
        check_first_recent_call_type - This API checks the first recent call is conference call or not
        Ex: option=conference
        """       
        try:
            if params["option"] == "conference":
                self.assertElement.element_should_contain_text("recent_all_tab_first_item", "Conference call")

            log.mjLog.LogReporter("ManhattanComponent", "info", "check_first_recent_call_type - call type verified")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_first_recent_call_type - failed to check first recent call type")
            raise Exception("ManhattanComponent error check_first_recent_call_type failed")

    def cleanup_canned_msgs(self):
        '''
           Author : Aakash           
           Ex : cleanup_canned_msgs        
        '''
        try:
            i=2
            log.mjLog.LogReporter("ManhattanComponent","info","cleanup_canned_msgs- Open the People tab and unmark number of users")           
            self.peopleGroup.open_own_user_detail()
            time.sleep(1)
            self.peopleGroup.open_own_user_preferences()
            time.sleep(1)
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['SETTINGS_WINDOW_NUMBER']))
            self.webAction.click_element("preferences_im")
            time.sleep(1)
            removecannedmsg = self._browser.elements_finder("canned_response_list")
            #removecannedmsg1 = removecannedmsg[2:]
            for i in range(0, (len(removecannedmsg)-2)):                 
                try:            
                    removecannedmsg[2].click()                   
                    self.webAction.click_element("delete_selected_canned_msg")
                    time.sleep(2)                    
                    #i+=1;
                    removecannedmsg = self._browser.elements_finder("canned_response_list")                     
                except:                   
                    return 
            #self.webAction.click_element("preferences_close_window")
            self.webAction.switch_to_window(int(confMgr.getConfigMap()['DEFAULT_WINDOW_NUMBER']))            
            self.webAction.click_element("peoples_second_panel_minimized_button")
            #self.webAction.click_element("default_own_name")
            time.sleep(2)
            
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","cleanup_canned_msgs- Failed to open People tab"+str(sys.exc_info()))
            raise Exception("ManhattanComponent error cleanup_canned_msgs failed")

    def cleanup_voicemails(self):
        '''
           Author : Aakash
           parameters : no parameter specified
           Ex : cleanup_voicemails
        
        '''
        try:
            i = 0
            log.mjLog.LogReporter("ManhattanComponent", "info","cleanup_voicemails- Open the People tab and unmark number of users")
            self.webAction.click_element("default_voicemail_tab")
            self.webAction.click_element("vm_all_tab")
            remove_vms = self._browser.elements_finder("vm_unread")
            for i in range(0, (len(remove_vms) - 6)):
                try:
                    remove_vms[i].click()
                    self.webAction.click_element("delete_vm")
                    time.sleep(1)
                    i += 1
                except:
                    self.webAction.click_element("default_voicemail_tab")
                    return

            self.webAction.click_element("default_voicemail_tab")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error","cleanup_voicemails- Failed to open People tab" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error cleanup_voicemails failed")
        
    def cleanup_favorites(self):
        '''
           Author : Aakash
           cleanup_favorites() - Open the people tab by default favorite contacts will shown, then unmark the favorite icon
           parameters : no parameter specified
           Ex : cleanup_favorites
        
        '''
        try:
            i=0
            log.mjLog.LogReporter("ManhattanComponent","info","cleanup_favorites- Open the People tab and unmark number of users")           
            self.webAction.click_element("default_people_tab")
            self.webAction.click_element("peoples_favorite_tab")           
            removefavoritelist = self._browser.elements_finder("peoples_favorite_list")            
            while(1):              
                try:            
                    removefavoritelist[i].click()
                    time.sleep(2)                   
                    i+=1;   
                except:
                    self.webAction.click_element("default_people_tab")
                    return                   
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","cleanup_favorites- Failed to open People tab"+str(sys.exc_info()))
            raise Exception("ManhattanComponent error cleanup_favorites failed")
        
    
    def cleanup_groups(self):
        '''
           Author : Aakash
           cleanup_groups() - Open the people tab then click on groups, groups will shown, then delete the groups
           parameters : no parameter specified
           Ex : cleanup_groups
        
        '''
        try:
            i=0
            log.mjLog.LogReporter("ManhattanComponent","info","cleanup_groups- Open the People tab and unmark number of users")           
            self.webAction.click_element("default_people_tab")
            self.webAction.click_element("peoples_group")           
            removegrouplist = self._browser.elements_finder("group_arrow")            
            while(1):              
                try:            
                    removegrouplist[i].click()
                    self.webAction.click_element("third_panel_edit_group")
                    self.webAction.click_element("TP_delete_group")
                    self.webAction.explicit_wait("peoples_group_delete_popup")
                    self.webAction.click_element("TP_detele_confirm")
                    time.sleep(2)                   
                    i+=1;   
                except:
                    self.webAction.click_element("default_people_tab")
                    #time.sleep(2)
                    return                   
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","cleanup_groups- Failed to open People tab"+str(sys.exc_info()))
            raise Exception("ManhattanComponent error cleanup_groups failed")

    def create_new_contact(self, **params):
        '''
           Author : bparihar
           create_new_contact() - Check weather a user with extetion exist or not if yes, then delete that user first and then open the create contact section, fill all the entries and save
           parameters : 
                    pos: position of the number
                    phType: phone type to be selected(Mobile,Home,Office,Fax,Assistant)
                    num: number to be added
                    first_name, middle_name, last_name, company, department, business, mobile,
                    pager, home_number, fax, email, IM, title, address, city, state, zip, country, cancel
           Ex : create_new_contact add_contact_number pos=1 phType=Mobile num=9977667766 first_name=CUSER_273051 last_name=CLast email=cclast@shoretel.com\
            department=test company=shoretel component_id=$componentId1
        
        '''
        try:
            self.delete_contact(**params)
            self.go_to_new_contact()
            self.add_contact_number(**params)
            self.add_contact_details(**params)
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","create_new_contact- Failed to create new contact "+str(sys.exc_info()))
            raise Exception("ManhattanComponent error create_new_contact failed")

    def verify_log_files_creation(self):
        '''
        Author: Indresh
        Checks whether log folder exists or not
        '''
        try:
            if platform.system() == "Windows":
                logFolder = Path(os.getenv('LOCALAPPDATA') + "\Mitel\Logs")
                if not logFolder.is_dir():
                    raise Exception(log.mjLog.LogReporter("ManhattanComponent","error","Log folder does not exist"))
        except:
            raise
            
            
    def click_first_user(self):
        """
        Author : Prashanth
        click_first_user() - This API will click on directory &then open the contact card of first user
        parameter: message
        ex: click_first_user
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_first_user - going to click verify_im_textarea")
            self.webAction.click_element("default_name_number_search")
            time.sleep(1)
            self.webAction.explicit_wait("default_search_input")
            firstname = self.queryElement.get_text("FP_directory_firstname")
 
            contactlist = self._browser.elements_finder("people_search")
            time.sleep(1)
            contactlist[0].click()
            return firstname
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_first_user - failed to verify test area" + str(sys.exc_info()))
            raise
            
    def search_member_group(self, **params):
        '''
           Author : HariPrakash
           cleanup_groups() - seraches a member in the group tab
           parameters : username
           
        
        '''
        try:
            if (params["option"]=="inputuser"):
                self.webAction.input_text("search_group_input", params["user"])
            elif(params["option"]=="clear"):
                self.webAction.clear_input_text("search_group_input")
                self.webAction.click_element("search_group_input")
           
        except:
            log.mjLog.LogReporter("ManhattanComponent","error","search_member_group "+str(sys.exc_info()))
            raise Exception("ManhattanComponent search_member_group failed to find the groups")

    def open_compact_view_in_group(self, **params):
        '''
           click on the add new button which is on the bottom of the page
        '''
        try:
            if (params["option"]=="compact"):
                autoit.win_activate("Mitel Connect")
                self.webAction.click_element("change_view_group_list")
                time.sleep(3)
                self.webAction.click_element("compact_view")            
                log.mjLog.LogReporter("PeopleGroup","info","open_compact_view_in_group")
            elif(params["option"]=="list"):
                autoit.win_activate("Mitel Connect")             
                self.webAction.click_element("change_view_group_grid")
                time.sleep(3)
                self.webAction.click_element("list_view")   
                log.mjLog.LogReporter("PeopleGroup","info","open_compact_view_in_group")                
            
        except:
            log.mjLog.LogReporter("PeopleGroup","error","open_compact_view_in_group -Error while opening the view"+str(sys.exc_info()))
            raise
    def search_people_withfirstname_clickUser(self, **params):
        """
        Author : Poornima
        search_people_withfirstname_clickUser() - search people by first name,then clicks on a particular username by searching in the list
        Parameters: searchItem
        Ex1: search_people_withfirstname_clickUser=user1
        Ex2 : search_people_withfirstname_clickUser=123
        Extra Info. : If your searchItem has spaces then pass it like first**second
        """
        try:          
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                    "search_people_withfirstname_clickUser - Searching people by name ")
                                                                                                                   
            itemObject = self.defaultPanel.search_people_by_firstname(params["searchItem"], False)
 
            searchItem1 = params["lastName"]
            for i in itemObject:
                if searchItem1 in i.text.strip():                                               
                    i.click()
                    time.sleep(5)
                    log.mjLog.LogReporter("ManhattanComponent", "info", "search_people_withfirstname_clickUser"                                                                                                                                                       " - Click on Particular User in the list displayed by first name")                                                                        
                    break
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "search_people_withfirstname_clickUser - Searching people by name"
                                                                 " failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error search_people_withfirstname_clickUser - failed")


    def verify_external_assignment(self):    
        try:
            
            log.mjLog.LogReporter("verify_Call_behaviour_items() - This API checks that dashboard call and verifies items in call")
            time.sleep(3)
            self.queryElement.element_not_displayed("default_client_pane_timer")
            if not self.queryElement.element_not_displayed("FP_Recieve_Button"):
                raise
            self.queryElement.element_not_displayed("third_panel_end_call")
            log.mjLog.LogReporter("ManhattanComponent", "info","verify_Call_behaviour_items - able to verify all items in call")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_Call_behaviour_items - failed to" " receive IM " + str(sys.exc_info()))
                
            raise Exception("ManhattanComponent error verify_Call_behaviour_items failed")
    
    def verify_info_calls_messages_vmtab(self):
        """
        Author: Vijayvenkatesh
        verify_info_calls_messages_vmtab - To verify on third panel verify_info_calls_messages_vmtab
        Parameters: no parameter
        """
        try:
            self.assertElement.element_should_be_displayed("third_panel_info")
            self.assertElement.element_should_be_displayed("third_panel_messages")
            self.assertElement.element_should_be_displayed("third_panel_calls")
            self.assertElement.element_should_be_displayed("third_panel_voicemail")
            log.mjLog.LogReporter("ThirdPanel", "info", " Succesuffy verifed info_calls_messages_vmtab")
        except:
            log.mjLog.LogReporter("ThirdPanel", "error", "verify_info_calls_messages_vmtab"
                                                                 " - failed to verify on third panel verify_info_calls_messages_vmtab")
            raise

    def verify_avatar(self, **params):
        """
        Author: Vijayvenkatesh
        verify_avatar - To verify avatar on third panel 
        Parameters: no parameter
        """
        try:
            fname=re.match( r'(.).*',params["fname"])
            lname=re.match( r'(.).*',params["lname"])
            uname=fname.group(1)+lname.group(1)
            con = self.queryElement.get_text("third_panel_avatar")
            con = con.lower()
            print con
            print uname
            if con.lower() == uname.lower():
			    log.mjLog.LogReporter("ManhattanComponent", "info", " Successfully verifed avatar")
            else:
                log.mjLog.LogReporter("ManhattanComponent", "error", "verify_avatar"
                                                                 " - failed to verify on third panel verify_avatar")
                raise
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_avatar"
                                                                 " - failed to verify on third panel verify_avatar")
            raise

    def mouse_hover_phone_type(self, **params):
        """
        Author: Junaid
        mouse_hover_phone_type - verifying the text weather it is softphone or deskphone releated text 
        Parameters: phone_type = deskphone
        """
        try:
            if params["phone_type"] == "deskphone":
                self.webAction.mouse_hover("text_join_via_deskphone")
                hover_text = self.queryElement.get_element_attribute("text_join_via_deskphone", "title")
                self.assertElement.values_should_be_equal(hover_text, "Dial me in via my deskphone")
                log.mjLog.LogReporter("Events", "info", "mouse_hover_phone_type"
                                                        " - display hover text as  Call me at my deskphone")
            elif params["phone_type"] == "softphone":
                self.webAction.mouse_hover("text_join_on_softphone")				
                hover_text = self.queryElement.get_element_attribute("text_join_on_softphone", "title")
                self.assertElement.values_should_be_equal(hover_text, "Call me on my softphone")
                log.mjLog.LogReporter("Events", "info", "mouse_hover_phone_type"
                                                        " - display hover text as  Call me on my softphone")
            else:
                self.webAction.mouse_hover("text_join_on_external_number")
                hover_text = self.queryElement.get_element_attribute("text_join_on_external_number", "title")
                text_contained = "Dial me in via External"
                self.assertElement.element_should_contain_text("text_join_on_external_number", text_contained)
                log.mjLog.LogReporter("Events", "info", "mouse_hover_phone_type"
                                                        " - display hover text as Dial me in via External ")
        except:
            log.mjLog.LogReporter("Events", "error", "mouse_hover_phone_type - failed"
                                                     " to display the hovering phone type " + str(sys.exc_info()))
            raise

    def click_Dropdown_send_Intercom(self, **params):
        """
        Author: Uday
        click_Dropdown_send_Intercom() - clicking drop down option in third panel and clicks on send Intercom
        click_Dropdown_send_Intercom
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_Dropdown_send_Intercom-  Checking alret when avaial option in conatct card")
            self.webAction.click_element("Third_panel_additional_option")
            if params["check"] == "Intercom":
                self.webAction.click_element("TP_Contactcard_More_Dropdown_Intercom")

                
        except:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "click_Dropdown_send_Intercom- Failed to verify calls" + str(sys.exc_info()))
            raise

    def play_unread_voicemails_via_computer_speaker(self, **params):
        '''
        Author : Uday
        play_unread_voicemails_via_computer_speaker
        '''
        try:
            unread_vm = self._browser.elements_finder("vm_unread")
            for vm in unread_vm:
                vm.click()
                break
            else:
                raise AssertionError("Either xpath 'vm_unread' is incorrect or No unheard voicemail is there!")
            self.webAction.explicit_wait("vm_play_through_computer")
            computer_buttons = self._browser.elements_finder("vm_play_through_computer")
            play_buttons = self._browser.elements_finder("vm_play_button")
            for cum_button in computer_buttons:
                for play_button in play_buttons:
                    cum_button.click()
                    time.sleep(2)
                    play_button.click()
                    time.sleep(5)
                    if self.queryElement.element_not_displayed("recent_voicemail_pause"):
                        continue
            log.mjLog.LogReporter("People_Group", "info",
                                  "play_unread_voicemails_via_computer_speaker - voicemail played via computer speaker")
        except:
            log.mjLog.LogReporter("People_Group", "error", "play_unread_voicemails_via_computer_speaker " + str(sys.exc_info()))
            return False

    def people_sort_icon(self):
        """
        Author: Haritha
        people_sort_icon - Clicks on "last contact" from people sort Icon 
        Parameters: 
        """
        try:
            log.mjLog.LogReporter("people_sort_icon - This API clicks on Last contact from sort tab in favorite")
 
            self.webAction.click_element("people_sort")
 
            time.sleep(2) 
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{ENTER}")
        
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "people_sort_icon - failed to" " click on Last contact from sort tab in favorite " + str(sys.exc_info()))
                
            raise Exception("ManhattanComponent error people_sort_icon failed")
    def verify_user_sorted_lastcontact(self, **params):
        """
        Author: Haritha
        verify_user_sorted_lastcontact - verifying the contact is in first position after selecting "last contact" 
        Parameters: 
        """
        try:
            userintop = self._browser.elements_finder("people_filter_lastcontact")
            console("Line 1 executed")
            if params["peopleName"] in userintop[1].text:
                console("Line 2 executed")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "verify_user_sorted_lastcontact - Passed to verify user who contacted last")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", 
                     "verify_user_sorted_lastcontact - error while verifying a user who contacted last" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error people_sort_icon failed")

    def Primary_phone_assignment(self, **params):
        """
        Author: Uday
        Primary_phone_assignment: It will clicks on External assignment radio button and will pass parameters
        EX: Parameters: name: Uday , number: DID
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "Primary_phone_assignment - going to click and verify")
            self.webAction.click_element("FP_External_Assignment")
            time.sleep(2)
            self.webAction.click_element("FP_External_Label_Assignment")
            self.webAction.input_text("FP_External_Label_Assignment",params["name"])
            self.webAction.click_element("FP_External_Number_Assignment")
            self.webAction.input_text("FP_External_Number_Assignment",params["number"])
            self.webAction.click_element("FP_External_Assignment_Add")
            log.mjLog.LogReporter("ManhattanComponent", "info", "Primary_phone_assignment - After click and verification")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Primary_phone_assignment - failed to" " click and verify " + str(sys.exc_info()))
                
            raise Exception("ManhattanComponent error Primary_phone_assignment failed")

    def Join_external_conference(self, **params):
        """
        Author: Uday
        Join_external_conference: It will verifies and enters the Extension/DID number and clicks on call me button
        EX: Parameters: number: DID
        """
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "Join_external_conference - verifies the green telephony button")
            self.assertElement.page_should_contain_element("event_join_via_deskphone")
            self.webAction.explicit_wait("TP_Call_Me")            
            self.webAction.click_element("TP_Call_Me")
            self.webAction.click_element("TP_call_Me_Number")
            self.webAction.input_text("TP_call_Me_Number",params["number"])
            self.webAction.click_element("TP_Call_Me_Button")
            log.mjLog.LogReporter("ManhattanComponent", "info", "Join_external_conference - After filling check the text box")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Join_external_conference - failed to" " join the external number " + str(sys.exc_info()))
                
            raise Exception("ManhattanComponent error Join_external_conference failed")

    def search_list_IM_presence_people_extension(self, **params):
        """
        Author: Sameera
        search_list_IM_presence_people_extension - Searching Users list with first name 
        Parameters: params["searchItem"] = UserName 
        """        
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "search_people_or_extension - Searching people by name ")
            search_item = re.sub("\*\*", " ", params["searchItem"])
            self.defaultPanel.search_list_people_or_extension(search_item)
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                      "search_people_extension - Searching people by name"
                                      " failed" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error search_people_extension - failed")
			

    def verify_Im_presence_Avatar_from_SearchList(self, **params):
        """
        Author: Sameera
        verify_Im_presence_Avatar_from_SearchList - verifying IM presence AVAtar from searchList 
        """
        try:
            list = self._browser.elements_finder("IM_Presence_Avatar")
            if len(list) == 2:
                print("Im presence of user is present")
                log.mjLog.LogReporter("ManhattanComponent", "info",
                				"verify_Im_presence_Avatar_from_SearchList - Im presence for the users Searching people by name")
                list[0].click()
                self.webAction.explicit_wait("IM_Contact_Card_Avatar_Presence")
                self.webAction.mouse_hover("IM_Contact_Card_Avatar_Presence")
            else:
                raise Exception("IM_presence_verification is failed for  search_people_extension1 - failed")
            list = self._browser.elements_finder("IM_NOT_Presence_Avatar")
            if len(list) == 2:
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "verify_Im_presence_Avatar_from_SearchList - Im absence for the users Searching people by name")
                list[1].click()
                self.webAction.explicit_wait("IM_Contact_Card_Avatar_Not_Presence")
                self.webAction.mouse_hover("IM_Contact_Card_Avatar_Not_Presence")
				
            else:
                 raise Exception("IM_presence_verification is failed for  search_people_extension2 - failed")
        except:
			raise Exception("IM_presence_verification is failed for  search_people_extension3 - failed")

    def mouse_hover_canned_im(self, **params):
        """
        Author: Sameera
        mouse_hover_canned_im - verifying the hover is happening or not on saved IM 
        Parameters: check = "positive"
        """
        try:
			if params["check"] == "positive":
			    self.webAction.mouse_hover("IM_Hover_cannedIM")
			elif params["option"] == "negative":
			   self.webAction.click_element("IM_Hover_cannedIM")
			   self.webAction.mouse_hover("IM_Hover_savedIM")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "verify_Canned_IM - failed to" " receive IM " + str(sys.exc_info()))

            raise Exception("ManhattanComponent error verify_Canned_IM failed")

    def verify_contact_card_on_call(self, **params):
        """
        Author: Anirban(This is a slight modification of verify_contact_card)
        verify_contact_card() - This API verifies whether contact card is present for a person
        Parameters: option and username
        Ex: verify_contact_card option=present/absent username=abc
        """
        try:
            status = self.queryElement.element_not_displayed("third_panel_user")
            if status and params["option"] == "absent":
                log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_card - contact"
                                                                    "card of user " + params[
                                          "username"] + " is not present")
            else:
                username = re.sub("\#", " ", params["username"])
                name = self.queryElement.get_text("third_panel_user")
                if name in username and params["option"] == "present":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_card - contact"
                                                                        "card of user " + username + " is present")
                elif name in username and params["option"] == "absent":
                    raise AssertionError("Contact card is present but it should not!")
                elif name != username and params["option"] == "absent":
                    log.mjLog.LogReporter("ManhattanComponent", "info", "verify_contact_card - contact"
                                                                        "card of user " + username + " is not present")
                else:
                    raise AssertionError("Contact card should not be present, but it is!")
            if "image" in params.keys():
                self.assertElement.element_should_be_displayed("people_image")
            if "status" in params.keys() and params["status"] == "yes":
                self.assertElement.element_should_be_displayed("third_panel_statusColor")
                self.assertElement.element_should_be_displayed("TP_im_presence")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_contact_card"
                                                         " failed to verify contact card " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_contact_card failed")

			
    def click_vm_forward(self,**params):
        '''
        Author : Haritha
        clicks on forward in second panel of voicemail
        '''
        try:
            log.mjLog.LogReporter("reply", "info", "click_vm_forward - successful"
                                                         "clicking on forward button successful " + str(sys.exc_info()))
            self.webAction.click_element("vm_forward_button")
            if params["subject"] != "default":
                self.webAction.input_text("vm_subject_field", params["subject"])
        except:
            log.mjLog.LogReporter("Voicemails", "error", "forward_voicemail - error"
                                                         " while clicking on forward button " + str(sys.exc_info()))
            raise

    def add_contact_vm_conversation_second_panel(self,**params):
        '''
        Author : Haritha
        Add contact in the 'To Field' for voicemail in the secomd panel
        parameters: Username
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", 
                                "add_contact_vm_conversation_second_panel Adding contact to  vm Conversation in second panel" + str(sys.exc_info()))
            self.webAction.click_element("recent_vm_forward_to")
            time.sleep(2)
            self.webAction.input_text("recent_vm_forward_to", params["name"])
            self.webAction.explicit_wait("people_grp_drop_drown_contact_name")
            self.webAction.click_element("people_grp_drop_drown_contact_name")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", 
                          "add_contact_vm_conversation_second_panel - Failed to join vm Converstaion in second panel" + str(sys.exc_info()))
            raise
	

    def record_vm_reply_second_panel(self,**params):
        '''
        Author : Haritha
        Record the voicemail from second panel
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "record_vm_reply_second_panel- record and reply voicemail successful ")

            if params["recording_device"] == "computer":
                self.webAction.click_element("vm_play_through_computer")
                self.webAction.click_element("vm_start_record_button")
                self.webAction.explicit_wait("vm_stop_record_button")
                self.webAction.click_element("vm_stop_record_button")
                self.webAction.explicit_wait("vm_cancel_button")
                self.assertElement.element_should_be_displayed("vm_cancel_button")
                self.assertElement.element_should_be_displayed("vm_send_button")
                self.webAction.click_element("vm_send_button")
                log.mjLog.LogReporter("ManhattanComponent", "info", "record_vm_reply_second_panel"
                                                " - Clicked on Send button" + str(sys.exc_info()))
            else:
                self.webAction.click_element("vm_play_through_phone")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "record_vm_reply_second_panel- error"
                                                         " record and reply voicemail fails " + str(sys.exc_info()))
            raise

    def verify_users_telephony_presence(self, **params):
        '''
        Author : Rahul
        check_userGroup_telephony_presence() - This API will verify the telephony presense status and color both of a
                                                user in a group in the Third Pannel
        parameter: color: Flick_orange; status: Available[On The Phone]

        '''
        try:
            self.thirdPanel.check_presence_status_third_panel(params["status"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_telephony_presence "
                                                                "- expected status and color matches with actual")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_users_telephony_presence- error"
                                                         " - expected status and color does not match with actual " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_users_telephony_presence failed")

    def verify_users_availabilty_status(self, **params):
        '''
        Author : Rahul
        check_users_availabilty_status - This API will verify only status of users in Third Pannel
        parameter: status: Available [Ringing]
        '''
        try:
            self.thirdPanel.check_availability_status_third_panel(params["status"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "verify_users_availabilty_status "
                                                                "- expected status matches with actual")

        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "verify_users_availabilty_status- error"
                                                         " - expected status does not match with actual " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error verify_users_availabilty_status failed")

    def click_always_on_top(self):
        try:

            autoit.win_activate("Mitel Connect")
            self.webAction.click_element("FP_Click_Connect")
            time.sleep(2)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(5)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(5)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(5)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(5)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{DOWN}")
            time.sleep(5)
            autoit.control_send("[CLASS:Chrome_WidgetWin_1]", "Chrome_RenderWidgetHostHWND1", "{ENTER}")
            time.sleep(5)
            log.mjLog.LogReporter("ManhattanComponent", "info", "click_always_on_top - check on always on top")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_always_on_top -Error while click on always on top" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_always_on_top failed")

    def open_notepad(self):
        try:
            autoit.run("C:\\WINDOWS\\system32\\notepad.exe")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_always_on_top -Error while click on always on top" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_always_on_top failed")

    def close_notepad_new(self):
        try:
            autoit.win_activate("[CLASS:#32770]")
            autoit.win_close("[CLASS:Notepad]")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "click_always_on_top -Error while click on always on top" + str(sys.exc_info()))
            raise Exception("ManhattanComponent error click_always_on_top failed")

    def get_conference_dial_in(self):
        '''
        Author : Ashappa
        get_conference_dial_in():To get the conference extension

        '''
        try:
            conf_number = self.queryElement.get_text("TP_conference_dial_in")
            dial_in = conf_number.split()[3]
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "conference code for dial in is " + dial_in)
            access_code = self.queryElement.get_text("TP_access_code")
            access_code = re.sub("\-", "", access_code)
            access_code = re.sub("Organizer code: ", "", access_code)
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "access code for conference is : " + access_code)
            for i in range(0, len(dial_in)):
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "dialled number " + dial_in[i])
                self.defaultPanel.click_dialpad_numbers(dial_in[i])
            time.sleep(1)
            ActionChains(self._browser.get_current_browser()).send_keys(Keys.ENTER).perform()
            time.sleep(20)
            for j in range(0, len(access_code)):
                log.mjLog.LogReporter("ManhattanComponent", "info",
                                      "dialled number " + access_code[j])
                self.defaultPanel.click_dialpad_numbers(access_code[j])
            time.sleep(1)
            ActionChains(self._browser.get_current_browser()).send_keys(Keys.ENTER).perform()
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                  "get_conference_dial_in - dialed the access code successfully")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error",
                                  "get_conference_dial_in - failed to dial the access code " + str(sys.exc_info()))
            return False
 	
    def check_incoming_call_verify_CannedIMarrow(self):
        '''
           Author: Sameera
           check_incoming_call_verify_cannedIMarrow() - To check whether Canned IM arrow is displayed while incoming call in manhattan client
           Parameter: No parameter
           Ex: check_incoming_call_verify_cannedIMarrow
        '''
        try:
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_incoming_call"
                                                                " - Verfying cannedIMarrow incoming call")
            self.assertElement.element_should_be_displayed("IM_Hover_cannedIM")
            log.mjLog.LogReporter("ManhattanComponent", "info", "check_incoming_call"
                                                                " - CannedIM is visible")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "check_incoming_call"
                                                                 " - Failed to check incoming call notification1" + str(
                sys.exc_info()))
            raise Exception("ManhattanComponent error check_incoming_call - Failed to chack incoming call notification22")

    def Click_verify_any_cannedresponse_incall(self):
        """
        Author: Sameera
        Click_verify_any_cannedresponse_incall() - This API will click and verifys the saved canned response and the textbox to write new canned IM.
        Ex: Click_verify_any_cannedresponse_incall
        Extra Info: This API will click and verifys the saved canned response and the text box for the writing the new canned IM.
        """
        try:
            log.mjLog.LogReporter(
                "Click_send_any_cannedresponse_incall() - This API will click and sends the canned response while call in progress")
            self.webAction.click_element("default_call_canned_resonse")
            self.webAction.mouse_hover("IM_Text_Respond_with_heading")
            self.webAction.mouse_hover("IM_Verify_Saved_Canned_IMs")
            time.sleep(3)
            self.webAction.mouse_hover("IM_Verify_Text_Box_Write_NewIM")
            self.webAction.explicit_wait("default_call_canned_resonse")
            self.webAction.click_element("default_call_canned_resonse")
            log.mjLog.LogReporter("ManhattanComponent", "info",
                                    "Click_verify_any_cannedresponse_incall - clicked and verified the canned  response")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "Click_verify_any_cannedresponse_incall - failed to"
                                                                 " verify the canned response " + str(sys.exc_info()))
            raise Exception("ManhattanComponent error Click_verify_any_cannedresponse_incall failed")

    def send_client_log(self):
        """
        Vijayvenkatesh 
        send_client_log() - This API sends Cient log from one user to another
        Ex: send_client_log
        """
        file_dir="C:\Users\Public\Documents"
        try:
            self.webAction.click_element("FP_default_connect_menu")
            time.sleep(10)
            autoit.control_send("[TITLE:Mitel Connect]", "", "{DOWN}")
            autoit.control_send("[TITLE:Mitel Connect]", "", "{DOWN}")
            autoit.control_send("[TITLE:Mitel Connect]", "", "{DOWN}")
            autoit.control_send("[TITLE:Mitel Connect]", "", "{DOWN}")
            autoit.control_send("[TITLE:Mitel Connect]", "", "{DOWN}")
            autoit.control_send("[TITLE:Mitel Connect]", "", "{DOWN}")
            autoit.control_send("[TITLE:Mitel Connect]", "", "{ENTER}")
            time.sleep(2)
            autoit.win_wait_active("[TITLE:Mitel Support Assistant]",20)
            autoit.win_activate("[TITLE:Mitel Support Assistant]")
            autoit.control_send("[TITLE:Mitel Support Assistant]", "", "{ENTER}")
            autoit.control_send("[TITLE:Mitel Support Assistant]", "", "{TAB 2}")
            autoit.control_send("[TITLE:Mitel Support Assistant]", "", "{ENTER}")
            time.sleep(2)
            autoit.control_click("[TITLE:Mitel Support Assistant]", "[NAME:radioButton2]")
            autoit.control_send("[TITLE:Mitel Support Assistant]", "", "{TAB 2}")
            autoit.control_send("[TITLE:Mitel Support Assistant]", "", "{ENTER}")

            time.sleep(2)
            autoit.win_wait_active("[TITLE:Client Log Files - Message (Plain Text) ]", 20)
            autoit.send("+{TAB 1}")
            autoit.send("{ENTER}")
            time.sleep(2)
            autoit.send("!s")
            time.sleep(2)
            autoit.control_set_text("[TITLE:Save As]","[CLASS:ComboBox; INSTANCE:1]","C:\Users\Public\Documents")
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            autoit.send("+{TAB 1}")
            autoit.send("+{TAB 1}")
            autoit.send("+{TAB 1}")
            autoit.send("+{TAB 1}")
            autoit.send("{ENTER}")
            time.sleep(10)
            autoit.win_close("[TITLE:Client Log Files - Message (Plain Text) ]")
            time.sleep(5)
            autoit.control_send("[TITLE:Mitel Support Assistant]", "", "{ENTER}")
            log.mjLog.LogReporter("ManhattanComponent", "info", "send_client_log"
                                                                " - clicked on About Mitel Connect Menu")
            log.mjLog.LogReporter("ManhattanComponent", "info", "send_client_log - Unzipping the Log file and verify date ")
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "send_client_log - failed to"
                                                                 " not able to unzipping the Log file and verify date " + str(sys.exc_info()))		 
            raise
			
    def unzip_log_file(self, **params):
        """
        Vijayvenkatesh 
        send_client_log() - This API sends Cient log from one user to another
        Parameters: extension = 3333
        Ex: send_client_log
        """
        try: 		
            self.peopleGroup.unzip_file(params["extension"])
            log.mjLog.LogReporter("ManhattanComponent", "info", "unzip_log_file - Unzipping the Log file and verify date ") 
        except:
            log.mjLog.LogReporter("ManhattanComponent", "error", "unzip_log_file - failed to"
                                                                 " not able to unzipping the Log file and verify date " + str(sys.exc_info()))
            raise		
    
	
if __name__ == "__main__":
    params = {"component_type": "ManhattanComponent", "port": "4444", "aut": "connect_client", "browserName": "chrome"}
    manhattan = ManhattanComponent(params)
    # manhattan.launch_url({"URL": r"C:\Users\mnhauto5\Desktop\Backup\recording\ClickMeToPlay.html"})
    manhattan.client_login({"username": "mnhauto9", "password": "changeme"})
    manhattan.search_people_extension({"searchItem": "mnh**auto10"})
    # manhattan.check_user_detail_attribute({"option":"call", "check":"positive"})
    #manhattan.place_end_call({"option": "start"})
