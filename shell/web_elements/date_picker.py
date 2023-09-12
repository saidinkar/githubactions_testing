from .abstract import Abstract


class DatePicker(Abstract):
    SELECTOR = "input"
    SELECTOR_ = "//bs-daterangepicker-container"

    WRAPPER = SELECTOR_ + "/div/div/div/div"
    DAYS_WRAPPER = WRAPPER + "/bs-days-calendar-view"
    HEAD = "/bs-calendar-layout/div/bs-datepicker-navigation-view"
    BODY = "/bs-calendar-layout/div/table/tbody/tr/td/span[text()='{}']"

    MONTHS_WRAPPER = WRAPPER + "/bs-month-calendar-view"
    YEAR_WRAPPER = WRAPPER + "/bs-years-calendar-view"

    PREVIOUS = "/button[@class='previous']"
    NEXT = "/button[@class='next']"
    MONTH = "/button[@class='current ng-star-inserted']"
    YEAR = "/button[@class='current']"

    def input(self, date):

        self.driver.click(self.BASE)

        for i in range(0, 2):
            num = i+1
            day, month, year = date[i].split("-")
            CAL = self.DAYS_WRAPPER + "[{}]".format(num) + self.HEAD

            if year != self.driver.find(CAL + self.YEAR).text:
                self.driver.click(CAL + self.YEAR)
                self.driver.click(self.YEAR_WRAPPER + self.BODY.format(year))
                self.driver.click(self.MONTHS_WRAPPER + self.BODY.format(month))

            if month != self.driver.find(CAL + self.MONTH).text:
                self.driver.click(CAL + self.MONTH)
                self.driver.click(self.MONTHS_WRAPPER + self.BODY.format(month))

            self.driver.click(self.DAYS_WRAPPER + "[{}]".format(num) + self.BODY.format(day))

        return self
