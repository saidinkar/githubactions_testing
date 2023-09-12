import os
import time
import allure
from selenium import webdriver as web
from selenium.webdriver.common.by import By
from ....src.pom.pages.base_page import BasePageElement
from selenium.webdriver.chrome import webdriver as sm
from ....utilities.CustomLogging import getLogger

log = getLogger()


class OpenPowerBIPage(BasePageElement):
    """Base page class that is initialized on every page object class."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    emailID = '//*[@name="loginfmt"]'
    submitBtn = '//*[@id="idSIButton9"]'
    passwd = '//*[@name="passwd"]'
    extraPopup = '//*[@id="KmsiCheckboxField"]'
    newemail = '//*[@id="email"]'
    newemailsubmit = '//*[@id="submitBtn"]'

    def power_BI_login(self, emailID, password):
        time.sleep(10)
        if len(self.find_elements_by_locator(By.XPATH,self.emailID))>0:
            log.info("Login into power bi using id")
            with allure.step("Login into power bi using id"):
                self.send_keys(By.XPATH, self.emailID, emailID)
                self.click_by_locator(By.XPATH, self.submitBtn)

        else:
            log.info("Login into power bi using id")
            with allure.step("Login into power bi using id"):
                self.send_keys(By.XPATH, self.newemail, emailID)
                self.click_by_locator(By.XPATH, self.newemailsubmit)

        time.sleep(5)
        log.info("Login into power bi using encrypted password")
        with allure.step("Login into power bi using encrypted password"):
            self.send_keys(By.XPATH, self.passwd, password)
            self.click_by_locator(By.XPATH, self.submitBtn)
        time.sleep(5)
        log.info("Clicked the extra pop up in login screen")
        with allure.step("Clicked the extra pop up in login screen"):
            if len(self.find_elements_by_locator(By.XPATH, self.extraPopup)) > 0:
                self.click_by_locator(By.XPATH, self.submitBtn)

    def test(self, emailID):
        time.sleep(10)
        self.find_element_by_locator(By.XPATH, self.emailID)
