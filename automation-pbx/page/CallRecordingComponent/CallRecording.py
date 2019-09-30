"""Call-Recording application Module
   File: CallRecording.py
   Author: Gopal
"""
import os
import sys
import re
import datetime
import inspect
import datetime as dt
import time
from time import gmtime, strftime
from datetime import timedelta
from pytz import timezone
from datetime import datetime
from distutils.util import strtobool
from collections import defaultdict
import string
import pdb
from bs4 import BeautifulSoup
import pandas as pd
#For console logs while executing ROBOT scripts
from robot.api.logger import console
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))


import web_wrappers.selenium_wrappers as base
import inspect
__author__ = "Gopal"

class CallRecording(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def call_duration(self,starttime,endtime):
        """Get the duration of pick-up and disconnect call .
        """
        try:
            FMT = "%I:%M:%S %p"
            tdelta = datetime.strptime(endtime, FMT) - datetime.strptime(starttime, FMT)
            print "duration %s" %tdelta
            return tdelta
        except Exception as e:
            print e
            raise AssertionError("Call duration time not correct" )

    def time_format_custom_search(self,curr_time):
        try:
            cur_time = curr_time.split()
            curr_time = cur_time[1]
            return curr_time
        except:
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Time format not support custom search  ")

    def time_format_correction(self,curr_time):
        """Get time format same as recorded in tele server .
        """
        try:
            cur_time = curr_time.split()
            curr_time = cur_time[1] + ' ' + cur_time[2]
            print curr_time
            index = 0
            if curr_time[index] == '0':
                phone_time = curr_time[1:]
                return phone_time
            return curr_time
        except Exception as e:
            print e
            print "Function Name :%s " % (inspect.stack()[0][3])
            raise AssertionError("Time not in Eastern time format ")

    def  date_format_correction(self,curtime):
        """Get date format same as recorded into tele server .
        """
        try:
            cur_time = curtime.split()
            print cur_time
            curr_date = cur_time[0]
            print curr_date
            index = 0
            if curr_date[index] == '0':
                phone_date = curr_date[1:]
                index_pos= phone_date.index('0')
                if index_pos == 2:
                    print "index postion %d" % index_pos
                    begin = phone_date[:index_pos]
                    end = phone_date[index_pos + 1:]
                    format_date = begin + end
                    print format_date
                    return format_date
                else:
                    return phone_date
            else:
                index_pos = curr_date.index('0')
                if index_pos == 3:
                    print "index postion %d" % index_pos
                    begin = curr_date[:index_pos]
                    end = curr_date[index_pos + 1:]
                    format_date = begin + end
                    print format_date
                    return format_date
            return curr_date
        except:
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Time not in US/Eastern time format ")

    def call_recording_data_validation(self,**params):

        #import  pdb;
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        try:
            st = self.time_format_correction(params["starttime"])
            et = self.time_format_correction(params["endtime"])
            call_date = self.date_format_correction(params["starttime"])
            st = dt.datetime.strptime(st, "%I:%M:%S %p")
            et = dt.datetime.strptime(et, "%I:%M:%S %p")
            call_date = dt.datetime.strptime(call_date, "%m/%d/%Y")
            call_type = None
            time.sleep(3)
            if params["call_type"] == "inbound":
                call_type = "in"
            elif params["call_type"] == "outbound":
                call_type="out"
            #self.action_ele.explicit_wait("recent_call_1")
            #self.action_ele.click_element("recent_call_1")
            #time.sleep(3)
            self.capture_call_recording_data()
            print "Debug: Call data  validation"
            df1 = pd.read_csv("callrecording.csv", usecols=['Date', 'Starttime', 'Endtime', 'Direction', 'CLID', 'DialedNumber'], nrows=1)              #Read first line
            df = pd.read_csv("callrecording.csv", usecols=['Date', 'Starttime', 'Endtime', 'Direction', 'CLID', 'DialedNumber'],skiprows=[1], nrows=1)    #Read 2nd line
            if params["option"] == "did_call" or params["option"] == "recent_call" or params["option"] == "trans" or params["option"] == "call_hold" or params["option"] == "call_parked" :
                self.validate_data(df1, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
            elif params["option"] == "conf":
                if params["record_mode"] == "alwayson" and call_type == "in":
                    self.validate_data(df1, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                elif params["record_mode"] == "ondemand" and call_type=="in":
                    #self.validate_data(df1, call_date, st, et, params["to_calle"], params["extn"], call_type)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                elif params["record_mode"] == "alwayson" and call_type=="out":
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                elif params["record_mode"] == "ondemand" and call_type=="out":
                    #self.validate_data(df1, call_date, st, et, params["from_calle"], params["extn"] , "in")
                    self.validate_data(df1,  call_date, st, et, params["from_calle"], params["to_calle"] , call_type, flag=1)
            elif params["option"] == "sm":
                if params["record_mode"] == "alwayson" and call_type == "in":
                    #self.validate_data(df1, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                elif params["record_mode"] == "ondemand" and call_type=="in":
                    #self.validate_data(df1, call_date, st, et, params["to_calle"], params["extn"], call_type)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
            elif params["option"] == "sc":
                if params["record_mode"] == "alwayson" and call_type == "in":
                    #self.validate_data(df1, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                elif params["record_mode"] == "ondemand" and call_type=="in":
                    #self.validate_data(df1, call_date, st, et, params["to_calle"], params["extn"], call_type)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
            elif params["option"] == "bargein":
                if params["record_mode"] == "alwayson" and call_type == "in":
                    #self.validate_data(df1, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
                elif params["record_mode"] == "ondemand" and call_type=="in":
                    #self.validate_data(df1, call_date, st, et, params["to_calle"], params["extn"], call_type)
                    self.validate_data(df, call_date, st, et, params["from_calle"], params["to_calle"], call_type, flag=1)
            elif params["option"] == "call_pickup":
                self.validate_data(df1, call_date, st, et, params["from_calle"], params["to_calle"], call_type,flag=1)
            elif params["option"] == "extn_call":
                starttime = str(df1['Starttime'].values[0])
                starttime = dt.datetime.strptime(starttime, "%I:%M:%S %p")
                endtime = str(df1['Endtime'].values[0])
                endtime = dt.datetime.strptime(endtime, "%I:%M:%S %p")
                if starttime <= st and endtime >= et:
                    raise AssertionError("Extension call:Something is wrong,please check Manually")
                else:
                    print "Extension call:Call Recording not happening ,because it's not trunk call"

        except:
            raise AssertionError("Validation Failed", str(sys.exc_info()))

    def validate_data(self,df, call_date, starttime, endtime, from_num, out_num, call_type,flag=0):
        """Validated recorded call data  .
        params@ startime: call start time (call pick-up time)
                endtime: call disconnect time
                callduration: total duration of call
                flag: set values based on types of calls

        """


        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            dial_date = df['Date'].values[0]
            dial_date=dt.datetime.strptime(dial_date, "%m/%d/%Y")
            call_direction = df['Direction'].values[0]
            clid = str(df['CLID'].values[0])
            dialnum = str(df['DialedNumber'].values[0])
            if dial_date == call_date:
                print "Call Date Validated"
            else:
                raise AssertionError("Call Date Validation failed")
            clid = re.sub(r'[\W_]+', '', clid)
            if len(clid) > 11:
                clid = clid[1:]
                if clid == from_num:
                    print "CLID check passed"
                else:
                    raise AssertionError("CLID check error")
            if call_direction.lower() == call_type.lower():
                print "Call type Validated"
            else:
                raise AssertionError("Call type Validation failed")
            if flag == 1:
                st = str(df['Starttime'].values[0])
                st = dt.datetime.strptime(st, "%I:%M:%S %p")
                et = str(df['Endtime'].values[0])
                et = dt.datetime.strptime(et, "%I:%M:%S %p")
                if starttime <= st:
                    print "Time Validation passed"
                else:
					raise AssertionError("Time Validation failed")
        except Exception as e:
            raise AssertionError("Validation failed", str(sys.exc_info()))

    def validate_data_custom_search(self,var, **params):

        try:
            print "Validate data Custom Search"
            sttime = self.time_format_correction(params["starttime"])
            edtime = self.time_format_correction(params["endtime"])
            call_date = self.date_format_correction(params["starttime"])

            sttime = dt.datetime.strptime(sttime, "%I:%M:%S %p")
            edtime = dt.datetime.strptime(edtime, "%I:%M:%S %p")
            call_date = dt.datetime.strptime(call_date, "%m/%d/%Y")

            time.sleep(1)
            self.capture_call_recording_data()
            time.sleep(5)

            df = pd.read_csv("callrecording.csv",usecols=['Date', 'Starttime', 'Endtime','RecDuration' ,'UserFirst', 'UserLast', 'Direction', 'CLID', 'DialedNumber'],nrows=1)  # Read first line
            dial_date = df['Date'].values[0]
            dial_date = dt.datetime.strptime(dial_date, "%m/%d/%Y")
            call_direction = df['Direction'].values[0]
            clid = str(df['CLID'].values[0])
            record_dur = str(df['RecDuration'].values[0])
            dialnum = str(df['DialedNumber'].values[0])

            firstname = str(df['UserFirst'].values[0])
            lastname = str(df['UserLast'].values[0])
            username = firstname + ' ' + lastname

            # custom search data Validation part
            if params["option"] == "custom_extn":

                if dialnum == var:
                    print "Extension Number Matched"
                else:
                    raise AssertionError("Extension couldn't matched")
            elif params["option"] == "custom_did":
                clid = re.sub(r'[\W_]+', '', clid)  #Prints only Alphanum -Removes any + sign in number)
                if len(clid) > 11:
                    clid = clid[1:]
                if clid == var:
                    print "Did Number Matched"
                else:
                    raise AssertionError("Did couldn't Matched")
            elif params["option"] == "custom_DN":
                if dialnum == var:
                    print "Dailed Number Matched"
                else:
                    raise AssertionError("DN couldn't matched")
            elif params["option"] == "custom_date":
                if dial_date == call_date:
                    print "CS: Date Matched"
                else:
                    raise AssertionError("Date couldn't Matched")
            elif params["option"] == "custom_dur":
                    if record_dur:
                        print "CS: Call Recorded"
                    else:
                        raise AssertionError("CS Data validation; Call Not Recorded")
            elif params["option"] == "custom_user":
                if username == var:
                    print "CS: User Name Matched"
                else:
                    raise AssertionError("CS Data validation; User Name Couldn,t Matched")
            elif params["option"] == "custom_call_time":
                if var == 1:
                    st = df['Starttime'].values[0]
                    st = dt.datetime.strptime(st, "%I:%M:%S %p")
                    et = df['Endtime'].values[0]
                    et = dt.datetime.strptime(et, "%I:%M:%S %p")
                    if sttime <= st and edtime >= et:
                        print "Time Validation passed"
                    else:
                        raise AssertionError("Time Validation failed")
            else:
                raise AssertionError("Custom Search : Not Matched None of custom search")
        except Exception as e:
            print e
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise Exception("Custom Search : Call Recording Data Validation",str(sys.exc_info()))

    def get_page_source(self):
        """
        Get page source
        :return:
        """
        try:
            time.sleep(5)
            return self._browser.get_current_page_source()
        except Exception as e:
            print e


    def capture_call_recording_data(self):
        """Captured call recorded data from tele server .

        """
        try:
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()

            time.sleep(8)
            self.load_recent_calls()
            self.action_ele.explicit_wait("table_list")
            var=self.get_page_source()
            soup = BeautifulSoup(var, "html.parser")
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            #Collects all Hidden data in soup
            hidden_data = soup.findAll(style="display: none;")
            try:
                for i in hidden_data:
                    i.decompose()    #Decompose will permenantly delete from soup
            except:
                pass

            #Scrapes the table values
            table = soup.find('table', class_="k-selectable")
            #Iterates for columns and rows
            for tr in table.find_all('tr'):
                for td in tr.find_all('td'):
                    try:
                        if td['style'] == "display:none":
                            td.decompose()            # Decomposes if any hidden data
                    except:
                        print "None"
            # Collects Headers list

            headers = soup.find_all(class_="k-header k-filterable")
            my_list = []
            for i in headers:
                if i.text == "Start Time":
                    my_list.append("Starttime")
                elif i.text == "End Time":
                    my_list.append("Endtime")
                else:
                    my_list.append(str(i.text))
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            #Creates pandas object using table html data
            df = pd.read_html(str(table), header=None)
            #Merges table and headers and writes to csv
            df[0].to_csv("callrecording.csv", sep=',', encoding='utf-8', index=False, header=my_list)
        except:
            raise Exception("Unable to capture call recording data", str(sys.exc_info()))

    """def capture_call_recording_data(self):
        Captured call recorded data from tele server .

        try:
            time.sleep(5)
            self.load_recent_calls()
            time.sleep(8)
            for i in range(5):
                try:
                    self.action_ele.explicit_wait("table_list")
                    var=self.get_page_source()
                    soup = BeautifulSoup(var, "html.parser")
                    table = soup.find('table', class_="k-selectable")
                    headers = soup.find_all('th', class_="k-header k-filterable")
                    my_list = []
                    temp = ['ArchiveID', 'Sorting', 'TenantID']
                    for i in headers:
                        if i.text not in temp:
                            my_list.append(str(i.text))
                    df = pd.read_html(str(table), header=None)
                    df[0].to_csv("callrecording.csv", sep=',', encoding='utf-8', index=False, header=my_list)
                    break
                except:
                    time.sleep(7)
        except Exception as e:
            print e
            raise Exception("Unable to capture call recording data", str(sys.exc_info()))"""

    def get_time_now(self):


        """Get time format same as recorded in tele server .
        """
        try:

            fmt = "%m/%d/%Y %I:%M:%S %p"
            now_time = datetime.now(timezone('US/Pacific'))
            time_now = now_time.strftime(fmt)
            print "Current time %s" %time_now
            return time_now
        except:
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise Exception("Unable to capture current time",str(sys.exc_info()))

    def load_recent_calls(self):
        """
        This function is used for click on recent calls button for loaded recent call data in teleserver
        """
        try:
            time.sleep(2)
            self.action_ele.explicit_wait("recent_call")
            self.action_ele.click_element("recent_call")
        except Exception as e:
            print e
            raise e

    def select_custom_search(self):
        """
        This Function is used for click on Custom Search button
        """
        try:
            self.action_ele.explicit_wait("custom_search")
            time.sleep(30)
            self.action_ele.click_element("custom_search")
            time.sleep(2)
        except Exception as e:
            print e
            raise e

    def select_option_tenant(self,t_name):
        """
        Description:This function is used for select Tenant in teleserver
        Params: Passed tenant name to be selected
        Return: None
        """
        try:
            for i in range(5):
                try:
                    self.action_ele.explicit_wait("tenant_menu")
                    self.action_ele.click_element("tenant_menu")
                    self.element = self.action_ele._element_finder("tenant_options")
                    option_list = self.element.find_elements_by_tag_name('li')
                    print("##########,list is :", option_list)
                    if len(option_list) > 0:
                        break
                except:
                    time.sleep(12)
            else:
                raise Exception("Element not found")
            for item in option_list:
                print("##########text is $$$$$$$$$$$", item.text)
                if item.text == t_name:
                    print("##########text is $$$$$$$$$$$", item.text)
                    item.click()
                    time.sleep(7)
                    self.action_ele.explicit_wait("tenant_menu",40)
                    option = self.action_ele.explicit_wait("tenant_menu").text
                    option = option.splitlines()[0]
                    if option == t_name:
                        print("option selected")
        except Exception as e:
            print e
            raise AssertionError("not able to select tenant", str(sys.exc_info()))

    def call_recording_custom_search_extension(self,extNum,**params):
        """
                Description:This function is used for search extension number in call recording data using custom search
                Params: extension number and custom option
                Return: None
        """
        try:
            print "Debug:call recording custom search extension"
            self.select_custom_search()
            time.sleep(2)
            self.action_ele.explicit_wait("extension_select")
            self.action_ele.input_text('extension_select', extNum)
            time.sleep(2)
            self.action_ele.explicit_wait("select_ok")
            self.action_ele.click_element("select_ok")
            time.sleep(2)

            self.validate_data_custom_search(extNum,**params)

        except Exception as e:
            print e
            raise AssertionError("Couldn't search extension in call recording ")

    def call_recording_custom_search_CLID(self,did,**params):
        """
        Description:This function is used for search did number in call recording data using custom search
        Params: did number and custom option
        Return: None
                """
        try:
            print "Debug:call recording custom search CLID"
            self.select_custom_search()

            sip_did = str('+') + str(did)
            self.action_ele.explicit_wait("CLID_select")
            self.action_ele.input_text('CLID_select', sip_did)
            time.sleep(2)
            self.action_ele.explicit_wait("select_ok")
            self.action_ele.click_element("select_ok")
            time.sleep(2)
            self.validate_data_custom_search(did, **params)
        except Exception as e:
            print e
            raise AssertionError("Couldn't search CLID in call recording")

    def call_recording_custom_search_Dialed_Number(self,dialNumber,**params):
        """
        Description:This function is used for search Dial number in call recording data using custom search
        Params: Dial number and custom option
        Return: None
                """
        try:
            print "Debug:call recording custom search Dialed Number"
            print "####################################################"
            self.select_custom_search()
            t = self._browser.element_finder("DN_select")
            date_option_list = t.find_elements_by_tag_name('a')
            for el in date_option_list:
                if el.text == 'Dialed Number':
                    el.click()
                    print("Dailed Number option selected")
                    break

            time.sleep(2)
            self.action_ele.explicit_wait("dnis_option")
            self.action_ele.input_text('dnis_option', dialNumber)

            time.sleep(2)
            self.action_ele.explicit_wait("cs_ok")
            self.action_ele.click_element("cs_ok")
            time.sleep(2)
            self.validate_data_custom_search(dialNumber, **params)
        except Exception as e:
            print e
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Couldn't search Dailed Number in call recording")

    def call_recording_custom_search_Date(self,**params):
        """
        Description:This function is used for search current date in call recording data using custom search
        Params: current date and custom option
        Return: None
        """
        try:
            print "Debug:call recording custom search Date"
            print "####################################################"
            d = self.date_format_correction(params["starttime"])
            self.select_custom_search()

            time.sleep(2)
            self.action_ele.explicit_wait("select_date_menu")
            self.action_ele.click_element("select_date_menu")
            time.sleep(1)

            t = self._browser.element_finder("date_option")
            date_option_list = t.find_elements_by_tag_name('a')
            for el in date_option_list:
                if el.text == 'Current Day':
                    el.click()
                    print("current day option selected")
                    break

            time.sleep(2)
            self.action_ele.explicit_wait("cs_ok")
            self.action_ele.click_element("cs_ok")
            time.sleep(2)
            self.validate_data_custom_search(d, **params)
        except Exception as e:
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Couldn't search Date in call recording" + str(e))

    def call_recording_custom_search_Recording_Duration(self,extn,**params):
        """
        Description:This function is used for search Call duration in call recording data using custom search
        Params: extension number  and call start and end time and custom option
        Return: None
        """
        try:
            print "Debug:call recording custom search Recording Duration"
            self.select_custom_search()
            MinTime = 0
            MaxTime = 8
            time.sleep(2)
            self.action_ele.explicit_wait("recording_duration_st")
            self.action_ele.input_text('recording_duration_st', MinTime)

            time.sleep(2)
            self.action_ele.explicit_wait("recording_duration_et")
            self.action_ele.input_text('recording_duration_et', MaxTime)

            time.sleep(2)
            self.action_ele.explicit_wait("cs_ok")
            self.action_ele.click_element("cs_ok")

            time.sleep(2)
            self.validate_data_custom_search(None, **params)

        except Exception as e:
            print e
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Couldn't search call duration")

    def call_recording_custom_search_StartTime_and_EndTime(self,extn,**params):
        #import pdb;
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        """
        Description:This function is used for search Call start and end time in call recording data using custom search
        Params: extension number  and call start and end time and custom option
        Return: None
        """
        try:
            custom_st = self.time_format_custom_search(params["starttime"])
            custom_et = self.time_format_custom_search(params["endtime"])
            time.sleep(2)
            self.select_custom_search()

            time.sleep(2)
            self.action_ele.explicit_wait("select_start_time")
            self.action_ele.input_text('select_start_time', custom_st)

            time.sleep(1)
            self.action_ele.press_key("select_start_time", "ENTER")
            time.sleep(1)
            self.action_ele.explicit_wait("select_end_time")
            self.action_ele.input_text('select_end_time', custom_et)
            time.sleep(1)
            self.action_ele.press_key("select_end_time", "ENTER")
            print "####################################################"

            time.sleep(2)
            self.action_ele.explicit_wait("cs_ok")
            self.action_ele.click_element("cs_ok")

            time.sleep(2)
            flag = 1
            self.validate_data_custom_search(flag, **params)
        except Exception as e:
            print e
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Couldn't search StartTime and EndTime")

    def call_recording_custom_search_Users(self, firstname, lastname, **params ):
        """
        Description:This function is used for search user name in call recording data using custom search
        Params: user name and custom option
        Return: None
        """
        try:
            self.select_custom_search()
            time.sleep(2)
            self.action_ele.explicit_wait("user_select")
            self.action_ele.click_element("user_select")
            flag = 0
            self.action_ele.explicit_wait("user_data_table")
            user_list = self._browser.elements_finder("user_data_table")
            print user_list
            for ur in user_list:
                for r in ur.find_elements_by_tag_name("tr"):
                    if firstname in r.get_attribute('innerHTML') and lastname in r.get_attribute('innerHTML'):
                        r.click()
                        print "Sucessfully Finded Selected User"
                        flag = 1
                        break
            if flag == 0:
                raise AssertionError("Users: Not present in select tenant")

            time.sleep(2)
            self.action_ele.explicit_wait("add_user_arrow")
            self.action_ele.click_element("add_user_arrow")

            time.sleep(2)
            self.action_ele.explicit_wait("cs_ok")
            self.action_ele.click_element("cs_ok")

            time.sleep(2)
            usr_name = firstname + ' ' + lastname
            self.validate_data_custom_search(usr_name, **params)

        except Exception as e:
            print e
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Couldn't search selected users")

    def cr_play_logoff(self):
        try:
            for i in range(5):
                try:
                    self.action_ele.explicit_wait("user_account")
                    self.action_ele.click_element("user_account")
                    self.action_ele.explicit_wait("log_off")
                    self.action_ele.click_element("log_off")
                    time.sleep(2)
                    self.action_ele.explicit_wait("yes_log_off")
                    self.action_ele.click_element("yes_log_off")
                    break
                except:
                    time.sleep(5)
            else:
                raise Exception("Element not found")
        except Exception as e:
            print e
            raise AssertionError("not clicking on log-off button")

    def cr_play_boss_logoff(self):
        try:
            time.sleep(1)
            self.action_ele.switch_to_window(0)
            time.sleep(2)
            self.action_ele.switch_to_window(1)
            time.sleep(30)

            self.action_ele.explicit_wait("user_account_boss")
            self.action_ele.click_element("user_account_boss")
            time.sleep(1)
            self.action_ele.explicit_wait("log_off")
            self.action_ele.click_element("log_off")
            time.sleep(1)
            self.action_ele.explicit_wait("yes_log_off")
            self.action_ele.click_element("yes_log_off")
            time.sleep(1)
            self.action_ele.switch_to_window(0)
            time.sleep(5)
            self.action_ele.explicit_wait("boss_log_off")
            self.action_ele.click_element("boss_log_off")
            time.sleep(1)
            self.action_ele.explicit_wait("yes_boss")
            self.action_ele.click_element("yes_boss")

        except Exception as e:
            print e
            print "Debug: Function Name :%s" % (inspect.stack()[0][3])
            raise AssertionError("Call Recording log-in Failed OR not clicking on BOSS log-off button")


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
