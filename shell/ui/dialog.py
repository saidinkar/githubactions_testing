import time

from ..web_elements.radio import RadioCbu


class AbstractDialog:
    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    DIALOG = "//mat-dialog-container"
    CONTENT = DIALOG + "/mat-dialog-content"
    LABEl = CONTENT + "/mat-button-toggle-group/mat-button-toggle[@value='{}']/button"
    FOOTER = DIALOG + "/mat-dialog-actions"
    PRIMARY = "/button[2]"
    OK = "/button"
    CANCEL = "/button/span[text()='Cancel']"
    GRID_OK = "//button/span[contains(text(),'Ok')]"
    GRID_EYE_BUTTON = "//mat-dialog-content/div/div[./div[contains(text(),'{}')]]/div/div[mat-icon]/mat-icon"
    CONTINUE = "//button[@type='submit']"
    SUBMIT_SLEEP = 5

    def __init__(self, driver):
        self.driver = driver
        self.driver.find(self.DIALOG)

    def download_report(self, **kwargs):
        if "report_format" not in kwargs:
            raise Exception
        else:
            self.driver.click(self.LABEl.format(kwargs['report_format']))
            self.primary()
            self.driver.wait_for_disappear(self.LOADER, timeout=240)

        self.driver.wait_for_disappear(self.DIALOG)
        self.driver.wait_for_disappear(self.LOADER, timeout=280)
        self.wait_report_download()

    def wait_report_download(self):
        def method():
            time.sleep(self.SUBMIT_SLEEP)
        self.driver.wait_until(method, timeout=120)

    def primary(self):
        self.driver.click(self.FOOTER + self.PRIMARY)

    def ok(self):
        self.driver.click(self.FOOTER + self.OK)

    def cancel(self):
        self.driver.click(self.FOOTER + self.CANCEL)
        self.driver.wait_for_disappear(self.DIALOG, timeout=5)
    
    def wait_dialog_disappear(self, timeout=120):
        self.driver.wait_for_disappear(self.DIALOG, timeout=timeout)

    def grid_label_click(self, label_name):
        if self.driver.text(self.GRID_EYE_BUTTON.format(label_name)) == 'visibility':
            self.driver.click(self.GRID_EYE_BUTTON.format(label_name))
            if self.driver.text(self.GRID_EYE_BUTTON.format(label_name)) == 'visibility_off':
                self.driver.click(self.GRID_OK)
            else:
                raise Exception("Column is Visible need to change it into invisible state")
        else:
            raise Exception("Column is already in invisible state")

    def cbu_level(self, value):
        RadioCbu(self.driver, self.CONTENT).input(value)
        self.driver.click(self.CONTINUE)
