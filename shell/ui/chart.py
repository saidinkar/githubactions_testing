import os
import time


class Chart:

    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    CHART_BUTTON = "(//*[local-name()='g'] / * [local-name()='path' and @class='highcharts-button-symbol'])[{}]"

    DOWNLOAD_OPTION = "//li[contains(text(),'{}')]"
    COMPARISON_SUMMARY = "//mat-card[2]/mat-card-content[1]/div[2]"
    SUBMIT_SLEEP = 5
    CHART = "// *[local-name() = 'g'] / *[local - name() = 'path' and class ='highcharts-button-symbol']"

    def __init__(self, driver, parent=None):
        self.driver = driver

    def comparison_summary_chart(self):
        self.driver.click("html")
        self.driver.scroll_top()
        self.driver.find(self.COMPARISON_SUMMARY)
        self.driver.click(self.COMPARISON_SUMMARY)
        self.driver.wait_for_disappear(self.LOADER, timeout=120)

    def download_chart(self, index, option):
        if not (self.driver.is_visible(self.CHART_BUTTON.format(index))):
            try:
                self.driver.click("html")
                self.driver.scroll_down()
                self.driver.find(self.CHART_BUTTON.format(index))
            except:
                self.driver.click("html")
                self.driver.scroll_down()
                self.driver.find(self.CHART_BUTTON.format(index))
        else:
            self.driver.find(self.CHART_BUTTON.format(index))

        self.driver.click(self.CHART_BUTTON.format(index))
        self.driver.click(self.DOWNLOAD_OPTION.format(option))
        self.wait_file_download()

    def wait_file_download(self):
        def method():
            time.sleep(self.SUBMIT_SLEEP)
        self.driver.wait_until(method, timeout=120)
