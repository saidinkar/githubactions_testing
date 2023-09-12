

class Logout:
    DROPDOWN = "//div/span[text()='Admin']"
    LOGOUT = "// span[text() = 'Logout']"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    def __init__(self, driver):
        self.driver = driver
        self.driver.wait_for_disappear(self.LOADER, timeout=90)
        self.driver.find(self.DROPDOWN)

    def logout(self):
        self.driver.click(self.DROPDOWN)
        self.driver.click(self.LOGOUT)
        self.driver.wait_for_disappear(self.LOADER, timeout=90)
