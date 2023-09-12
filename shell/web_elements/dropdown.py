from .abstract import Abstract
from ...base.exceptions.control import ValueNotFoundException




class DropDown(Abstract):
    SELECTOR = "ngx-select"
    CONTENT = "/div/div/div"
    LABEL = CONTENT + "/span/span"
    TRIGGER = CONTENT + "/span[@class='ngx-select__toggle-buttons']"

    PANEL = "//div/ul"
    PANEL_APPEND = CONTENT + "/div[contains(@class, 'ui-dropdown-panel')]/div/ul"
    OPTION_BY_TEXT = "/li[./a/span[contains(text(), '{}')]]"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    SEARCH = "//input[@type='text']"


    def __init__(self, driver, parent):
        Abstract.__init__(self, driver, parent)
        self.driver.wait_for_disappear(self.LOADER, timeout=60)

    def select_by_value(self, value):
        label = self.driver.text(self.BASE + self.LABEL)
        if value is None:
            value = "Select Dropdown"
        if label != value:
            self.driver.find(self.BASE + self.TRIGGER)
            self.driver.click(self.BASE + self.TRIGGER)
            self.driver.find(self.BASE + self.PANEL)
            dialog_value = self.driver.find_all(self.PANEL + self.OPTION_BY_TEXT.format(value))
            if len(dialog_value) == 0:
                raise ValueNotFoundException(self.BASE, value)
            self.driver.click(self.PANEL + self.OPTION_BY_TEXT.format(value))
            self.driver.wait_for_disappear(self.LOADER, timeout=60)



class MultiSelectDropDown(DropDown):
    SELECTOR = "ngx-select"
    CONTENT = "/div/div"
    FORM_FIX = "/form"
    LABEL = CONTENT + "/span/span"
    TRIGGER = CONTENT + "/span[@class='ngx-select__toggle-buttons']"
    ACTIVE = "[contains(text(),'{}')]"
    NO_DATA_AVAILABLE = "/li/h5"
    SEARCH_PANEL = "//div/div/ul[1]"
    PANEL = "//div/div/ul[2]"
    PANEL_ALL = "//div/div/ul[1]/li[./div[text()='{}']]"
    PANEL_APPEND = CONTENT + "/div[contains(@class, 'ui-dropdown-panel')]/div/ul"
    OPTION_BY_TEXT = "/li[./div[text()='{}']]"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    SEARCH = "//input[@type='text']"


    def select_by_value(self, value):
        label = self.driver.text(self.BASE + self.LABEL)
        if value is None:
            value = "---Select---"
        if label != value:
            self.driver.find(self.BASE)
            self.driver.click(self.BASE)
            if len(self.driver.find_all(self.BASE + self.PANEL + self.NO_DATA_AVAILABLE)) == 1:
                no_data_available = self.driver.text(self.BASE + self.PANEL + self.NO_DATA_AVAILABLE)
                raise ValueNotFoundException(value, no_data_available)
            if value == "Select All" or value == "UnSelect All":
                self.driver.click(self.BASE + self.PANEL_ALL.format(value))
            else:
                self.driver.find(self.BASE + self.PANEL)
                for i in range(len(value)):
                    if self.driver.is_visible(self.BASE + self.PANEL):
                        element = self.driver.find(self.BASE + self.SEARCH_PANEL + self.SEARCH)
                        element.send_keys(value[i])
                    dialog_value = self.driver.find_all(self.PANEL + self.OPTION_BY_TEXT.format(value[i]))
                    if len(dialog_value) == 0:
                        raise ValueNotFoundException(value, "Value not Present")
                    active = self.driver.find_all(self.BASE + self.LABEL + self.ACTIVE.format(value[i]))
                    if len(active) == 0:
                        self.driver.click(self.PANEL + self.OPTION_BY_TEXT.format(value[i]))
                        self.driver.find(self.BASE + self.SEARCH_PANEL + self.SEARCH).clear()




