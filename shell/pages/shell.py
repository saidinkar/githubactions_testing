
from ...base.selenium_proxy import SeleniumProxy
from ..ui.login import Login
from ..ui.logout import Logout
from .dashboard import Dashboard
from ...base.utilities.read_write_excel import ReadFromExcel
from .analyse_test_impact import AnalyseTestImpact
from ...base.exceptions import GenericException
import time


class TestShell:
    def __init__(self, config):
        self.driver = SeleniumProxy(config)
        self.__path = None
        self.__runner = None
        self.__system = None
        self.driver = SeleniumProxy(config)
        self.__user = None
        self.__pwd = None
        self.__last_table = None

    def connect(self, login, system, user, pwd):
        def method():
            self.driver.get(login)
            self.driver.find("//app-root", timeout=30)
            if self.driver.title == "502 Bad Gateway":
                raise Exception("Bad Gateway")

        self.driver.wait_until(method)
        self.driver.maximize_window()
        Login(self.driver).login(user, pwd)
        if self.driver.current_url != system:
            raise Exception("Home Page not found")
        self.__path = ()
        self.__runner = Dashboard(self.driver)
        self.__system = system

    def logout(self):
        Logout(self.driver).logout()

    def refresh(self):
        # retry refresh 3 times before failing
        # Some times white sceen appears due to server error while loading js resources
        # rerun will not help so trying browser refresh
        for _ in range(3):
            time.sleep(1)
            self.driver.refresh()
            self.driver.wait_for_disappear("//div[@class='ngx-overlay loading-foreground']", timeout=90)
            app_loaded = self.driver.find_all("//app-root", timeout=60)
            if len(app_loaded) > 0:
                break
            time.sleep(30)
        else:
            raise Exception("Failed to load app")

    def quit(self):
        self.driver.quit()

    def reset(self):
        """
            Click home and go to the home page.
        Returns:
            return the shell itself.

        """
        for _ in range(3):
            self.driver.get(self.__system)
            app_loaded = self.driver.find_all("//app-root", timeout=30)
            if len(app_loaded) > 0:
                break
            time.sleep(30)
        else:
            raise Exception("Failed to load app")
        self.driver.get(self.__system)
        self.__path = ()
        self.__runner = Dashboard(self.driver)
        return self

    def __getattr__(self, item):
        if self.__runner is None:
            raise Exception("Runner not init.")

        method = getattr(self.__runner, item, None)
        if not callable(method):
            raise GenericException({
                "message": "Invalid API in Shell.",
                "api": item
            })

        return method

    def navigate(self, target):
        self.__runner = Dashboard(self.driver).go(target.lower())

    def getdata(self, testdatapath):
        return ReadFromExcel.readFromExcel(testdatapath)
