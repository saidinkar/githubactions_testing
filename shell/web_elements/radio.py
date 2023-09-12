from .abstract import Abstract



class Radio(Abstract):

    SELECTOR = "mat-radio-group"

    OPTION_BY_VALUE = "/mat-radio-button[./label/span[text()='{}']]"

    def __init__(self, driver, parent):
        Abstract.__init__(self, driver, parent)

    def input(self, value):
        self.driver.scroll_into_view(self.BASE + self.OPTION_BY_VALUE.format(value))
        status = self.driver.find(self.BASE + self.OPTION_BY_VALUE.format(value)).get_attribute("value")
        if int(status) == 1:
            raise Exception(value, "Radio is enabled")
        else:
            self.driver.click(self.BASE + self.OPTION_BY_VALUE.format(value))



class RadioOption(Radio):

    OPTION_BY_VALUE = "/mat-radio-button[./label/span/span[contains(text(),'{}')]]"


class RadioCbu(Radio):

    OPTION_BY_VALUE = "//mat-radio-button[@value='{}']"








