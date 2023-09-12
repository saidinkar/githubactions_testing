
from .abstract import Abstract
import time


class CheckBoxList(Abstract):
    SELECTOR = "mat-checkbox"

    def __init__(self, driver, parent):
        Abstract.__init__(self, driver, parent)

    def input(self):
        locator = self.BASE
        self.driver.click(locator)


class CheckBoxValue(Abstract):
    SELECTOR = "mat-checkbox"
    SELECT_BY_ID = "/label[./span[contains(text(),'{}')]]/span/input"

    def __init__(self, driver, parent):
        Abstract.__init__(self, driver, parent)

    def input(self, value):
        check = self.driver.find(self.BASE).get_attribute('class')
        if 'checked' in check :
            self.driver.find(self.BASE + self.SELECT_BY_ID.format(value))
            self.driver.click(self.BASE+self.SELECT_BY_ID.format(value))
        else:
            return self


class CheckBox(Abstract):
    SELECTOR = "input"
    CHECK_BOX_OPTION = "[1]"
    CHECK_BOX_VALUE = "[2]"
    ERROR = "//p/span"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    def input(self, value):
        locator = self.BASE + self.CHECK_BOX_OPTION
        self.driver.click(locator)
        self.driver.input(self.BASE+self.CHECK_BOX_VALUE, value, web_element=self.web_element)
        self.driver.wait_for_disappear(self.LOADER, timeout=200)


class CheckBoxSelect:
    FILTER_OPTIONS = "//mat-accordion/mat-expansion-panel[2]/div/div/mat-panel-description/mat-checkbox"
    FILTER_OPTIONS_1 = "//mat-panel-description[./mat-checkbox]//span[contains(text(),'{}')]"
    ROW = "//table/tbody/tr"
    TABLE_CHECKBOX = ROW + "/td/mat-checkbox//label"

    def __init__(self, driver):
        self.driver = driver

    def select_option(self, option):
        if option is None:
            if self.driver.is_visible(self.FILTER_OPTIONS):
                filter_options = self.driver.find(self.FILTER_OPTIONS)
                self.driver.click(self.FILTER_OPTIONS)
            else:
                filter_options = None
            return filter_options.text

        else:
            time.sleep(5)
            if self.driver.is_visible(self.FILTER_OPTIONS_1.format(option)):
                filter_options = self.driver.find(self.FILTER_OPTIONS_1.format(option))
                self.driver.click(self.FILTER_OPTIONS_1.format(option))
            else:
                filter_options = None
            return filter_options.text

    def control_checkbox(self):
        self.driver.click(self.TABLE_CHECKBOX)