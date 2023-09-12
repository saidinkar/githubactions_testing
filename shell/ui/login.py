"""
Login Module
"""

from ...base.exceptions.element import ElementNotVisibleException


class Login(object):

    EMAIL = "//input[@formcontrolname='username']"
    PASSWORD = "//input[@formcontrolname='password']"

    SUBMIT = "//button"

    ERROR = "//form/div[@class='alert alert-danger']"
    INPUT_ERROR_USERNAME = "//label[./input[@formcontrolname='username']]/span"
    INPUT_ERROR_PASSWORD = "//label[./input[@formcontrolname='password']]/span"
    LOADER = "//div[@class='ngx-overlay loading-foreground']/div[@class='ngx-foreground-spinner center-center']"

    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        self.driver.find(self.EMAIL)
        self.driver.input(self.EMAIL, email)
        self.driver.input(self.PASSWORD, password)
        self.driver.click(self.SUBMIT)
        self.driver.wait_for_disappear(self.LOADER, timeout=90)
        self.check_error_messages()

    def check_error_messages(self):
        try:
            input_error = self.driver.find_all(self.INPUT_ERROR_USERNAME)
            if len(input_error) != 0:
                error_msg = self.driver.text(self.INPUT_ERROR_USERNAME)
                raise Exception(error_msg)
        except ElementNotVisibleException:
            if self.driver.is_visible(self.INPUT_ERROR_PASSWORD):
                error_msg = self.driver.text(self.INPUT_ERROR_PASSWORD)
                raise Exception(error_msg)

        try:
            error = self.driver.find_all(self.ERROR)
            if len(error) != 0:
                error_msg = self.driver.text(self.ERROR)
                raise Exception(error_msg)
        except ElementNotVisibleException:
            if self.driver.is_visible(self.ERROR):
                error_msg = self.driver.text(self.ERROR)
                raise Exception(error_msg)
