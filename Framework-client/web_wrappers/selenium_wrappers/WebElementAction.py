"""
Description: WebElementAction module contains methods to perform action on web applications
"""

__author__ = "Vinay HA"


# Selenium Modules
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


#Python modules
import sys
import os
import time
import inspect
# STAF modules

from log import log
import datetime
from time import gmtime, strftime


class WebElementAction:
    '''
    Methods to perform web operations are implemented in this class
    '''
    def __init__(self, browser):
        self._browser = browser

    def click_element(self, locator, replace_dict=None, value=None):
        """Click element identified by `locator`.
        replace_dict: For dynamically changing the xpath
        value: If you have multiple elements identified by locator and you want to click on a
               particular element where some text is written, then pass value=text_on_element,
               it will match value with text written on the element and click on that.
        """
        if value:
            self.elements = self._elements_finder(locator, replace_dict)
            if self.elements:
                for i in self.elements:
                    match_text = i.text.strip()
                    if "\n" in match_text:
                        match_text = map(str.strip, match_text.split("\n"))
                    if value in match_text:
                        i.click()
                        log.mjLog.LogReporter("WebUIOperation", "debug", "Click operation \
                                                      successful- %s" % (locator))
                        break
        else:
            self.element = self._element_finder(locator, replace_dict)
            if self.element:
                self.element.click()
                log.mjLog.LogReporter("WebUIOperation", "debug", "Click operation \
                                         successful- %s" % (locator))

    def input_text(self,locator, Text):
        """Types the given `text` into text field identified by `locator`.

        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.clear()
            self.element.send_keys(Text)
            log.mjLog.LogReporter("WebUIOperation","debug","Input_text operation \
                                    successful- %s" %(locator))
            
    def submit_form(self, locator):
        """Submits a form identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.submit()

    def clear_input_text(self,locator):
        """
        clear the given text field identified by `locator`.
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.clear()
            log.mjLog.LogReporter("WebUIOperation","debug","clear_input_text operation \
                                     successful- %s" %(locator))

    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`.
        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            self.element.click()
            log.mjLog.LogReporter("WebUIOperation","debug","select_checkbox operation \
                                    successful- %s" %(locator))

    def unselect_checkbox(self, locator):
        """Un-selects checkbox identified by `locator`.

        Does nothing if checkbox is already un-selected. Key attributes for
        checkboxes are `id` and `name`.
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            self.element.click()
            log.mjLog.LogReporter("WebUIOperation","debug","unselect_checkbox operation \
                                    successful- %s" %(locator))

    def select_radio_button(self, locator):
        """Sets selection of radio button .

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        """
        self.element = self._element_finder(locator)
        if not self.element.is_selected():
            self.element.click()
            log.mjLog.LogReporter("WebUIOperation","debug","unselect_checkbox operation \
                                    successful- %s" %(locator))
    
    def execute_javascript(self, script_name):
        '''
          execute java script
        '''
        self._browser.get_current_browser().execute_script(script_name)
            
    def choose_file(self, locator, file_path):
        """Inputs the `file_path` into file input field found by `locator`.

        This keyword is most often used to input files into upload forms.
        The file specified with `file_path` must be available on the same host 
        where the Selenium is running.

        """
        if not os.path.isfile(file_path):
            log.mjLog.LogReporter("WebUIOperation","debug","choose_file - File '%s' does not exist on the \
                                    local file system" % file_path)
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(file_path)
            log.mjLog.LogReporter("WebUIOperation","debug","choose_file - File '%s' selected" % file_path)

    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        """
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).double_click(self.element).perform()
            log.mjLog.LogReporter("WebUIOperation","debug","double_click_element operation \
                                     successful- %s" %(locator))                
      
    def drag_and_drop(self, source, target):
        """Drags element identified with `source` which is a locator.

        Element can be moved on top of another element with `target`
        argument.

        `target` is a locator of the element where the dragged object is
        dropped.
        """
        self.source_ele = self._element_finder(source)
        self.target_ele = self._element_finder(target)
        
        if self.source_ele and self.target_ele:
            ActionChains(self._browser.get_current_browser()).drag_and_drop(self.source_ele, self.target_ele).perform()
            log.mjLog.LogReporter("WebUIOperation","debug","drag_and_drop operation \
                                    successful: %s -> %s" %(source, target))
                                    
    def drag_and_move(self, source, target):
        """Drags element identified with `source` which is a locator.
        Element can be moved on top of another element with `target`
        argument.
        `target` is a locator of the element where the dragged object is
        dropped.
        """
        self.source_ele = self._element_finder(source)
        self.target_ele = self._element_finder(target)
        
        if self.source_ele and self.target_ele:
          
            ActionChains(self._browser.get_current_browser()).click_and_hold(self.source_ele).move_to_element(self.target_ele).perform()

    def right_click(self, locator):
        '''Right Click on element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        '''
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).context_click(self.element).perform()
            log.mjLog.LogReporter("WebUIOperation", "debug", "right_click operation \
                                     successful- %s" % (locator))

    def explicit_wait(self, element, waittime=20, replace_dict=None, ec='visibility_of_element_located', msg=None, msg_to_verify=None):
        """
        explicit_wait() is used to wait until element is displayed & enabled
        element: the web element
        waittime: max time to wait
        replace_dict: to replace variables in the value in map file. Refer _map_converter function in browser.py for more info
        ec: expected condition to wait on
        msg: msg to be validated irrespective of the element e.g. title_is or title_contains
        msg_to_verify: msg to be validated on a web element e.g. text_to_be_present_in_element

        e.g.
        For a map file entry as below
        comp_name==span#xpath#//*[@id="companyName"]

        some example calls to this function could be
        r = self.action_ele.explicit_wait("comp_name")
        r = self.action_ele.explicit_wait("comp_name",ec="title_contains",msg="Account") # "comp_name" i.e. element is not required
        in this call but it is required as it is a mandatory argument. It is this way to make this function backward compatible
        r = self.action_ele.explicit_wait("comp_name", ec="text_to_be_present_in_element", msg_to_verify="M5Portal Company")
        """
        self.elementAttr = self._browser._map_converter(element, replace_dict)
        wait = WebDriverWait(self._browser.get_current_browser(), waittime)
        result = None
        condition = getattr(EC, ec)
        locator = getattr(By, self.elementAttr['BY_TYPE'].upper())
        if msg:
            result = wait.until(condition(msg))
        elif msg is None and msg_to_verify is None:
            result = wait.until(condition((locator, self.elementAttr["BY_VALUE"])))
        elif msg_to_verify:
            result = wait.until(condition((locator, self.elementAttr["BY_VALUE"]), msg_to_verify))

        return result

    def focus(self, locator):
        """Sets focus to element identified by `locator`."""
        
        self.element = self._element_finder(locator)
        self._current_browser().execute_script("arguments[0].focus();", self.element)
        log.mjLog.LogReporter("WebUIOperation","debug","focus operation successful: %s" %(locator))
        
    def alert_action(self, Cancel= False):
        """Dismisses currently shown alert dialog and returns it's message.

        By default, this keyword chooses 'OK' option from the dialog. If
        'Cancel' needs to be chosen, set keyword ` Cancel = True'
        """
        self.text = self._alert(Cancel)
        log.mjLog.LogReporter("WebUIOperation","debug","alert_action successful:Text => %s" %(self.text))
        return self.text
        
    def press_key(self, locator, key):
        """Simulates user pressing key on element identified by `locator`.

        `key` is a single character.

        Examples:
        press_key ("GoogleSearch", "BACKSPACE")
        """
        if len(key) < 1:
            log.mjLog.LogReporter("WebUIOperation","error","press_key - Key value \
                                    not present  - %s" %(key))
            return None
        keydict = self._map_ascii_key_code_to_key(key)
        #if len(key) > 1:
        #    raise ValueError("Key value '%s' is invalid.", key)
        self.element = self._element_finder(locator)
        #select it
        if self.element:
            self.element.send_keys(keydict)
            log.mjLog.LogReporter("WebUIOperation","debug","press_key - Key %s sent \
                                    successfully " %(key))
    
    def mouse_hover(self, locator):
        '''Mouse hover on element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`
        '''
        self.element = self._element_finder(locator)
        if self.element:
            ActionChains(self._browser.get_current_browser()).move_to_element(self.element).perform()
            log.mjLog.LogReporter("WebUIOperation","debug","mouse_hover operation \
                                     successful- %s" %(locator))
    def switch_to_frame(self,frameno):
        '''
          switch to frame('frameno') 
        '''
        self.framelist=self._browser.elements_finder("UCB_Frame")
        self.browserdriver=self._browser.get_current_browser()
        self.browserdriver.switch_to_frame(self.framelist[frameno])

    def select_from_dropdown_using_text(self,locator,itemtext):
        ''' Selecting item from dropdownlist by using the option itemtext
        
        '''
        selectionlist=self._element_finder(locator)
        for option in selectionlist.find_elements_by_tag_name('option'):
            if option.text.strip() == itemtext :
                option.click()
                log.mjLog.LogReporter("WebUIOperation","debug","select_form_dropdown using text \
                                    successful- %s" %(itemtext))

    def select_from_dropdown_using_index(self,locator,itemindex):
        ''' Selecting item from dropdownlist by using the option itemindex
        
        '''
        selectionlist=self._element_finder(locator)
        sel = Select(selectionlist)
        for option in selectionlist.find_elements_by_tag_name('option'):
            if option.get_attribute("index") == str(itemindex):
                #self._setSelected(option)
                sel.select_by_index(itemindex)
                log.mjLog.LogReporter("WebUIOperation","debug","select_form_dropdown using index \
                                    successful- %s" %(itemindex))

    def select_list_item_using_text(self,locator,itemtext):
        '''
           select item from list by using itemtext
        '''
        # below change is to take care of new dropdown implementation
        selectlist=self._browser.elements_finder(locator)
        for item in selectlist:
            if item.text==itemtext:
                item.click()
                log.mjLog.LogReporter("WebUIOperation","debug","select_list_item form list \
                                    successful- %s" %(itemtext))
                break

    def select_list_item_using_index(self,locator,itemindex):
        '''
         select item from list by using itemindex
        '''
        selectlist=self._element_finder(locator)
        for item in selectlist:
            if item[index]==itemindex:
                item[index].click()
                log.mjLog.LogReporter("WebUIOperation","debug","select_list_item form list \
                                    successful- %s" %(itemindex))
    
    def switch_to_window(self,window):
        '''
          switch to window('window') 
        '''
        self.browserdriver = self._browser.get_current_browser()
        self.window_list = self.browserdriver.window_handles
        self.browserdriver.switch_to_window(self.window_list[window])
    
    
    def scroll(self, locator, position=1000):
        '''Scrolls from top to desired position at bottom
           locator is the id or class of scroll bar not exactly xpath
           position is the value of the place till where you want to scroll
           pass position=0 for scrolling from bottom to top
        '''
        self.xpath = self._browser._map_converter(locator)["BY_VALUE"]
        self.type = self._browser._map_converter(locator)["ELEMENT_TYPE"]
        if self.type == "id" :
            scriptName = "$(document).ready(function(){$('#"+self.xpath+"').scrollTop("+str(position)+");});"
            self._browser.get_current_browser().execute_script(scriptName)
        else:
            scriptName = "$(document).ready(function(){$('."+self.xpath+"').scrollTop("+str(position)+");});"
            self._browser.get_current_browser().execute_script(scriptName)
    
    def input_text_basic(self, locator, text):
        """sets the given 'text' into the field identified by 'locator'
           extra info: This method performs operation on HTML element called time
           Eg: if you want to set time then pass the time parameter in form of 'hhmm'
        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(text)
            log.mjLog.LogReporter("WebUIOperation","debug","input_text_basic operation successful- %s" %(locator))

    def window_handles_count(self):
        '''
          Get window handles count 
        '''
        self.browserdriver=self._browser.get_current_browser()
        self.window_list = self.browserdriver.window_handles
        return len(self.window_list)

    def check_checkbox(self, locator):
        """Checks if checkbox identified by `locator` is selected or unselected
        """
        self.element = self._element_finder(locator)
        if self.element.is_selected():
            log.mjLog.LogReporter("WebUIOperation","debug","check_checkbox operation successful- %s" %(locator))
            return True
        else:
            return False

    def clear_input_text_new(self,locator):
        """
        clear the given text field identified by `locator`.
        clear_input_text() does not work if text is right aligned,this new api works.

        """
        self.element = self._element_finder(locator)
        if self.element:
            self.element.send_keys(Keys.CONTROL + "a")
            self.element.send_keys(Keys.DELETE)
            log.mjLog.LogReporter("WebUIOperation","debug","clear_input_text operation \
                                         successful- %s" %(locator))

    def maximize_browser_window(self):
        """Maximizes the currently opened browser window
        """
        self._current_browser().maximize_window()
        log.mjLog.LogReporter("WebUIOperation","debug","maximize_browser_window - operation successfull")
        
    def minimize_browser_window(self):
        """minimizes the currently opened browser window
        """
        self._current_browser().set_window_position(-2000, 0)
        log.mjLog.LogReporter("WebUIOperation","debug","minimize_browser_window - operation successfull")


    def takeScreenshot(self, funcName, location=None):
        """
        Method to save screen shot to a given path with the function name
        :param funcName: Function name
        :param location: is an optional parameter.If present, the provided location will be used for saving the screen shot
        :return: None
        """
        # trying to figure out the report location
        if location is None:
            for frame in inspect.stack():
                if "page" in frame[1] and "Component" in frame[1]:
                    feature_file = frame[1]
                    location = feature_file.split("page")[0]
                    break
                elif "lib" in frame[1] and "Component" in frame[1]:
                    feature_file = frame[1]
                    location = feature_file.split("lib")[0]
                    break
            else:
                # falling back to framework location
                location = os.path.dirname(os.path.dirname(__file__))
        path = location+"\\reports\\report_"+str(datetime.datetime.now().date())+os.sep
        try:
            if not os.path.exists(path):
                print("Report path not found.Creating...")
                os.makedirs(path)
            name = path+funcName+str(datetime.datetime.now().time()).replace(":","_")+".png"
            print(name)
            self._browser.get_screenshot_as_file(name)
        except Exception, e:
            print(e)

# Private method
    def _element_finder(self, locator, replace_dict=None):
        '''
        _element_finder() - Method to invoke element_finder from browser class
        '''
        return self._browser.element_finder(locator, replace_dict)

    def _elements_finder(self, locator, replace_dict=None):
        '''
        _elements_finder() - Method to invoke elements_finder from browser class
        '''
        return self._browser.elements_finder(locator, replace_dict)
    
    def _map_ascii_key_code_to_key(self, key_code):
        map = {
            "NULL": Keys.NULL,
            "BACKSPACE": Keys.BACK_SPACE,
            "TAB": Keys.TAB,
            "RETURN": Keys.RETURN,
            "ENTER": Keys.ENTER,
            "CANCEL": Keys.CANCEL,
            "ESCAPE": Keys.ESCAPE,
            "SPACE": Keys.SPACE,
            "MULTIPLY": Keys.MULTIPLY,
            "ADD": Keys.ADD,
            "SUBTRACT": Keys.SUBTRACT,
            "DECIMAL": Keys.DECIMAL,
            "DIVIDE": Keys.DIVIDE,
            "SEMICOLON": Keys.SEMICOLON,
            "EQUALS": Keys.EQUALS,
            "SHIFT": Keys.SHIFT,
            "ARROW_UP": Keys.ARROW_UP,
            "ARROW_DOWN": Keys.ARROW_DOWN,
            "ARROW_LEFT": Keys.ARROW_LEFT,
            "ARROW_RIGHT": Keys.ARROW_RIGHT,
            "INSERT": Keys.INSERT,
            "DELETE": Keys.DELETE,
            "END": Keys.END,
            "HOME": Keys.HOME,
            "F12": Keys.F12,
            "ALT": Keys.ALT

        }
        key = map.get(key_code)
        if key is None:
            log.mjLog.LogReporter("WebUIOperation","info","Key not present, returning same string - %s" %(key_code))
            key = chr(key_code)
        return key

    def _alert(self, Cancel=False):
        alert = None
        try:
            
            alert = self._browser.get_current_browser().switch_to_alert()
            text = ' '.join(alert.text.splitlines()) # collapse new lines chars
            if Cancel: alert.dismiss()
            else: alert.accept()
            return text
        except WebDriverException:
            log.mjLog.LogReporter("WebUIOperation","info","Alert not present" )
            return None

    def _current_browser(self):
        return self._browser.get_current_browser()
                
    def _get_list_item_using_text(self, locator, itemtext):
        selectlist=self._element_finder(locator)
        print(selectlist)
        for item in selectlist:
            print(item.text)
            if item.text==itemtext:
                return item
            
    def _get_parent_obj(self, obj):
        return obj.find_element_by_xpath('..')
                


if __name__ == "__main__":
    params = {"name" : "Vinay"}
    myBrowser = Browser(params)
    myBrowser.go_to("http://google.com")
    Webaction = WebElementAction(myBrowser)
    Webaction.input_text("SearchButton","Vinay")
    Webaction.submit_form("SearchButton")
    #Webaction.press_key("SearchButton","ENTER")
    time.sleep(3)
    myBrowser.quit()
    
