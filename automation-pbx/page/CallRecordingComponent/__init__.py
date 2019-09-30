from CommonFunctionality import CommonFunctionality
from CallRecording import CallRecording


class CallRecordingPage(object):
    """Module for all the Call Recording"""

    def __init__(self, browser):
        self.common_func = CommonFunctionality(browser)
        self.call_recording = CallRecording(browser)
        
        
