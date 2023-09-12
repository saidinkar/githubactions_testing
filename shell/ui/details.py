
class Top:
    ADMIN = "//mat-card/div"
    INFO = ADMIN + "[contains(@class,'admin_dash_text')]"

    TEST_SUMMARY = "//div[@id='test_status']/mat-card/div[2]/div/div"
    TEST_IMPACT = "//div[@class='test_impact']/span"
    LIST_IMPACT = "//div/perfect-scrollbar/div/div/div/div"
    NOTIFICATION_BELL = "//div/i[@class='far fa-bell fa-stack']"
    MARK_ALL = "//u[text()='Mark all as read']"
    CLICK_NOTIFICATION = "//div[@ id='notify']/button"
    NOTIFICATION_VALUE = "//span[contains(text(),'Notifications')]"
    NO_NOTIFICATION_TEXT = "//span[contains(text(),'No Notification found')]"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    def __init__(self, driver):
        self.driver = driver

    def admin_message(self):
        admin = self.driver.find(self.ADMIN).text
        info = self.driver.find(self.INFO).text
        return admin, info

    def summary(self):
        summary = self.driver.find_all(self.TEST_SUMMARY)
        res = []
        for item in summary:
            value = item.text
            res.append(value)
        return res

    def impact(self):
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.TEST_IMPACT)
        self.driver.click(self.LIST_IMPACT)

    def click_notification(self):
        self.driver.click(self.NOTIFICATION_BELL)
        notify = self.driver.find(self.NOTIFICATION_VALUE).text
        if "(0)" not in notify:
            self.driver.click(self.CLICK_NOTIFICATION)
        else:
            print(self.driver.find(self.NO_NOTIFICATION_TEXT).text)

    def mark_as_all_read(self):
        self.driver.click(self.NOTIFICATION_BELL)
        notify = self.driver.find(self.NOTIFICATION_VALUE).text
        if "(0)" not in notify:
            self.driver.click(self.MARK_ALL)
        else:
            print("Mark as All is not found")


class History:
    SELECTOR = "//app-history"
    HISTORY = SELECTOR + "/perfect-scrollbar/div/div/div/div"
    CANCEL = SELECTOR + "/div[./span[text()='History of Test']]/span/i"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    def __init__(self, driver):
        self.driver = driver
        self.driver.wait_for_disappear(self.LOADER, timeout=90)

    def history(self):
        info = self.driver.find_all(self.HISTORY)
        res = []
        for item in info:
            value = item.text
            res.append(value)
        self.driver.click(self.CANCEL)
        return res


class Getting_started:
    HOW_TO_RUN = "//mat-expansion-panel-header[@id='mat-expansion-panel-header-0']"
    HOW_TO_RUN_DESC = HOW_TO_RUN + "/ancestor::mat-expansion-panel//p"
    WHAT_TO_KNOW = "//mat-expansion-panel-header[@id='mat-expansion-panel-header-1']"
    WHAT_TO_KNOW_DESC = WHAT_TO_KNOW + "/ancestor::mat-expansion-panel//p"
    IDEAL_DURATION = "//mat-expansion-panel-header[@id='mat-expansion-panel-header-2']"
    IDEAL_DURATION_DESC = IDEAL_DURATION + "/ancestor::mat-expansion-panel//p"
    INITIATED_TEST = "//mat-expansion-panel-header[@id='mat-expansion-panel-header-3']"
    INITIATED_TEST_DESC = INITIATED_TEST + "/ancestor::mat-expansion-panel//p"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"

    def __init__(self, driver):
        self.driver = driver

    def how_to_run(self):
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.HOW_TO_RUN)
        return self.driver.find(self.HOW_TO_RUN_DESC).text

    def what_to_know(self):
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.WHAT_TO_KNOW)
        return self.driver.find(self.WHAT_TO_KNOW_DESC).text

    def ideal_duration(self):
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.IDEAL_DURATION)
        return self.driver.find(self.IDEAL_DURATION_DESC).text

    def initiated_test(self):
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.INITIATED_TEST)
        return self.driver.find(self.INITIATED_TEST_DESC).text
