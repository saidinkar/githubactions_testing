import sys


class Alert:

    BASE = "//div[@id='toast-container']"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    def __init__(self, driver):
        self.driver = driver
        self.driver.find(self.BASE)

    def success(self, message):
        try:
            # self.driver.find(self.CLOSE.format(message))
            # self.driver.click(self.CLOSE.format(message))
            self.driver.wait_for_disappear(self.LOADER)
        except Exception as e:
            sys.stderr.write(str(e))

