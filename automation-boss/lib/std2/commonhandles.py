import stafenv

from web_wrappers.selenium_wrappers import LocalBrowser
from web_wrappers import selenium_wrappers as base


class CommonHandles(object):
    def __init__(self, browser):
        # self._browser = LocalBrowser._BROWSER
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
