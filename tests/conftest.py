import datetime
from allure_commons.types import AttachmentType
import os
from ..tests.settings import TARGET_DIR, emailID, encryptedPasscode, SCREENSHOTS_DIR, BROWSER_LOGS_DIR,url,browser
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from ..src.pom.pages.openpowerbi_page import OpenPowerBIPage
from ..src.pom.pages.samplepowerbi_page import SummaryReportPage
from ..utilities.encryption import decode
import json


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=browser)
    parser.addoption("--url", action="store", default=url)


@pytest.fixture(scope="session")
def get_browser(request):
    browser = request.config.getoption("--browser")
    return browser


@pytest.fixture(scope="function")
def get_driver(request, get_browser):
    global driver
    if get_browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path='D:\PyTest-Automation-Framework-master\chromedriver_win32\chromedriver.exe')
        driver.get(url)
        driver.maximize_window()
    elif get_browser == "firefox":
        driver = webdriver.Firefox(GeckoDriverManager().install())
    elif get_browser == "headless":
        chrome_options = Options()
        #chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    else:
        print("Driver not supported")
    driver.implicitly_wait(10)
    # Add in here each page from the POM in order to initialize the driver for each one.

    request.cls.OpenPowerBI=OpenPowerBIPage(driver)
    request.cls.summaryReport = SummaryReportPage(driver)
    #driver(settings.url)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def shell(request,get_browser):  # pylint: disable=redefined-outer-name
    global driver
    global driver
    if get_browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
    elif get_browser == "firefox":
        driver = webdriver.Firefox(GeckoDriverManager().install())
    elif get_browser == "headless":
        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    else:
        print("Driver not supported")
    driver.implicitly_wait(10)
    # Add in here each page from the POM in order to initialize the driver for each one.

    yield driver


    shell = OpenPowerBIPage({
            "temp": TARGET_DIR,
            "headless": "false"

    })
    try:
        shell.power_BI_login(emailID, decode(encryptedPasscode))
        yield shell
    except Exception as e:
        currentDT = datetime.datetime.now()
        shell.driver.get_screenshot_as_file(
            os.path.join(SCREENSHOTS_DIR, "connect_fail_{}.png".format(str(currentDT).replace(" ", "_")))
        )
        shell.quit()
        raise e

    try:
        shell.quit()
    except Exception as E:
        print(E)
        print("Warning: Shell close fail.")


def pytest_exception_interact(node, call, report): # pylint:disable=duplicate-argument-name, unused-argument
    # set a report attribute for failed call
    setattr(node, "rep_fail", True)


def get_file_name(request):
    class_type = request.cls
    file_name = request.module.__name__
    if class_type is not None:
        file_name = file_name + "." + class_type.__name__.lower()
    return file_name + "." + request.node.name
