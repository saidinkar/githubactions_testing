"""
Selenium Webdriver Proxy
"""
import time
import re
import platform

import os

import jsonschema

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from ..utilities import pydash_ext as _ext
from . import util
from ...base.exceptions.element import ElementNotAppearException, ElementNotVisibleException

OS_BASE = platform.system()


class SeleniumProxy:
    """
    This is wrapper class with web driver in it.
    It supports a convenient setup of a web driver of default configs.
    Also, it provides certain apis.

    Attributes:
        config(dict):
    """
    def __init__(self, config):

        config_schema = {
            "type": "object",
            "properties": {
                "timeout": {
                    "type": "number"
                },
                "interval": {
                    "type": "number"
                },
                "temp": {
                    "type": "string"
                },
                "headless": {
                    "type": "boolean"
                },
                "remote": {
                    "type": "string"
                },
                "browser": {
                    "type": "string"
                }
            },
            "required": [
                "temp",
                "headless"
            ],
            "additionalProperties": False
        }
        jsonschema.validate(_ext.clean(config), config_schema)
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if config.get("remote") is not None and re.match(regex, config["remote"]) is None:
            raise Exception("invalid remote url: ", config["remote"])

        self.__headless = config["headless"]
        self.__timeout = config.get("timeout") or 20
        self.__interval = config.get("interval") or 0.1
        self.__temp = config["temp"]
        self.__remote = config.get("remote")
        self.__browser = config.get("browser", "chrome")
        self.__downloads = os.path.join(self.__temp, "downloads")
        # self.__screenshots = os.path.join(self.__temp, "screenshots")
        self.__driver_path = None
        self.driver = None
        self.create_browser()
        # self.driver.set_window_size(1500, 1080)

    def __getattr__(self, item):
        if self.driver is None:
            raise Exception("Driver not init.")

        method = getattr(self.driver, item, None)
        return method

    def create_browser(self):
        if self.__browser == 'chrome':
            self.create_chrome()
        else:
            raise Exception(f"Unknown Browser - {self.__browser}")

    def create_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--whitelisted-ips')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1440, 900")
        if self.__headless is True:
            options.headless = True
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.default_directory": self.__downloads
        })

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

        if self.__remote is None:
            self.__driver_path = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(
                **_ext.clean({
                    "executable_path": self.__driver_path,
                    "options": options,
                    "desired_capabilities": capabilities
                })
            )
        else:
            self.driver = webdriver.Remote(
                desired_capabilities=capabilities,
                options=options,
                command_executor=self.__remote
            )
        # enable download in headless mode
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.__downloads}}
        self.driver.execute("send_command", params)

    def _get_locator(self, locator, web_element):
        driver = self.driver
        if web_element is not None:
            driver = web_element
            if isinstance(locator, str) and locator.startswith("/"):
                locator = "." + locator
        locator = util.to_tuple(locator)
        return driver, locator

    def find(self, target, web_element=None, timeout=None, interval=None, visible=True):
        """
        Check the validity of the locator, and use formatting on locator with solve values, if there is any.
        Wait and return an element from locator.

        Args:
            target(dict || list || tuple): Locator.
            timeout(integer): Wait time in secs.
            interval(float): Poll frequency in secs.
            web_element(WebElement): The parent web element to find in with.
            visible:

        Returns:
            WebElement:
        """
        handler, locator = self._get_locator(target, web_element)

        def method():
            element = handler.find_element(*locator)
            if visible is True and not element.is_displayed():
                raise ElementNotVisibleException(locator)
            return element

        return self.wait_until(method, timeout or self.__timeout, interval or self.__interval)

    def text(self, target, web_element=None, timeout=None, interval=None):

        handler, locator = self._get_locator(target, web_element)

        def method():
            element = handler.find_element(*locator)
            if not element.is_displayed():
                raise ElementNotVisibleException(locator)
            return element.text

        return self.wait_until(method, timeout or self.__timeout, interval or self.__interval)

    def find_all(self, locator, timeout=None, gap=None, web_element=None, visible=True):
        """
        Return all elements from locator, it will wait if parameter has condition.

        Args:
            locator(dict || list || tuple): Locator.
            timeout(integer): Wait time in secs.
            gap(float): Poll frequency in secs.
            web_element(WebElement): The parent web element to find in with.
            visible:

        Returns:
            WebElement:
        """
        handler, locator = self._get_locator(locator, web_element)

        def method():
            elements = handler.find_elements(*locator)
            if visible is True:
                for ele in elements:
                    if not ele.is_displayed():
                        raise ElementNotVisibleException(locator)
            return elements

        return self.wait_until(method, timeout or self.__timeout, gap or self.__interval)

    def click(self, locator, timeout=None, interval=None, web_element=None):
        """
        Wait to find the element from locator and click.

        Args:
            locator(dict || list || tuple || WebElement): Web element or a locator.
            timeout(integer): Wait time in secs.
            interval(float): Poll frequency in secs.
            web_element(WebElement): The parent web element to find in with.

        Returns:
            SeleniumProxy: self
        """
        handler, locator = self._get_locator(locator, web_element)
            
        def method():
            if isinstance(locator, WebElement):
                element = locator
            else:
                element = handler.find_element(*locator)
            element.click()

        self.wait_until(method, timeout=timeout, interval=interval)
        return self

    def right_click(self, locator, timeout=None, interval=None, web_element=None):
        """
        Wait to find the element from locator and click.

        Args:
            locator(dict || list || tuple || WebElement): Web element or a locator.
            timeout(integer): Wait time in secs.
            interval(float): Poll frequency in secs.
            web_element(WebElement): The parent web element to find in with.

        Returns:
            SeleniumProxy: self
        """
        handler, locator = self._get_locator(locator, web_element)

        def method():
            if isinstance(locator, WebElement):
                element = locator
            else:
                element = handler.find_element(*locator)

            ActionChains(self.driver).context_click(element).perform()

        self.wait_until(method, timeout=timeout, interval=interval)
        return self

    def input(self, locator, value, web_element=None, timeout=None, interval=None):
        """
        Wait to find the element from locator and input.

        Args:
            locator(dict || list || tuple || WebElement): Web element or a locator.
            value(str): The string to input.
            timeout(integer): Wait time in secs.
            interval(float): Poll frequency in secs.
            web_element(WebElement): The parent web element to find in with.

        Returns:
            SeleniumProxy: self
        """
        if value is None:
            return self

        handler, locator = self._get_locator(locator, web_element)

        def method():
            ele = handler.find_element(*locator)
            ele.clear()
            if value == "":
                # TODO while clearing empty values there was an error in updating empty,temporarily setting it to dummy
                #  string "1" and resetting to over come the issue
                # Need  to find a permanent fix
                ele.send_keys("1")
                if OS_BASE == 'Darwin':
                    ele.send_keys(Keys.COMMAND, 'a')
                else:
                    ele.send_keys(Keys.CONTROL, 'a')
                ele.send_keys(Keys.DELETE)
                # ele.clear()
            else:
                ele.send_keys(value)
        self.wait_until(method, timeout, interval)

        return self

    def get_attribute(self, target, attribute=None, web_element=None, timeout=None, interval=None, visible=True):
        if isinstance(target, (tuple, list)):
            attribute = target[1]
            target = target[0]
        handler, locator = self._get_locator(target, web_element)

        def method():
            element = handler.find_element(*locator)
            if visible is True and not element.is_displayed():
                raise ElementNotVisibleException(locator)
            return element.get_attribute(attribute)

        return self.wait_until(method, timeout or self.__timeout, interval or self.__interval)

    def is_visible(self, target, web_element=None, timeout=None, interval=None):
        if isinstance(target, WebElement):
            ele = target
        else:
            ele = self.find(target, web_element=web_element, timeout=timeout, interval=interval, visible=False)

        return ele.is_displayed() and ele.size["width"] > 0 and ele.size["height"] > 0

    def wait_until(self, method, timeout=None, interval=None):
        end_time = time.time() + (timeout or self.__timeout)
        error = None
        while True:
            try:
                return method()
            except Exception as e:  # pylint: disable=broad-except
                error = e
            time.sleep(interval or self.__interval)
            if time.time() > end_time:
                break
        raise error

    def hover(self, target, timeout=None, interval=None, web_element=None):
        handler, locator = self._get_locator(target, web_element)

        def method():
            if isinstance(locator, WebElement):
                element = locator
            else:
                element = handler.find_element(*util.to_tuple(target))

            ActionChains(handler).move_to_element(element).perform()

        self.wait_until(method, timeout=timeout, interval=interval)
        return self

    def quit(self):
        self.driver.quit()

    def scroll_down(self, web_element=None):
        """
        Scroll down the page to bottom.

        Return:
            self
        """
        # if web_element is None:
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # else:
        #     self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", web_element)
        # return self

        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        return self

    def scroll_top(self):
        ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
        time.sleep(2)
        return self

    def scroll_into_view(self, inner, outer=None, offset=0):
        if not isinstance(inner, WebElement):
            inner = self.find(inner)
        if outer is None:
            self.driver.execute_script("return arguments[0].scrollIntoView(true);", inner)
            return self

        top = outer.location["y"] + 2
        target = inner.location["y"]

        self.driver.execute_script("arguments[0].scrollTop = %s" % (target - top + offset), outer)
        return self

    def select_by_value(self, target, option, timeout=None, web_element=None):
        Select(self.find(target, web_element=web_element, timeout=timeout, visible=False)).select_by_value(option)
        return self

    def wait_for_disappear(self, locator, timeout=None, handler=None):
        handler, locator = self._get_locator(locator, handler)

        def method():
            elements = handler.find_elements(*util.to_tuple(locator))
            if len(elements) != 0:
                raise ElementNotAppearException(locator)

        self.wait_until(method, timeout=timeout)
        return self

    def switch_to_frame(self, frame):
        self.driver.switch_to.frame(self.find(frame))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

