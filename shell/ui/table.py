import random
import time

from retrying import retry
from .dialog import AbstractDialog
from selenium.webdriver import ActionChains
from ..web_elements.checkbox import CheckBoxValue, CheckBoxSelect
from ...base.utilities.pydash_ext import maybe_to_tuple
from ...base.exceptions import GenericException
from selenium.webdriver.common.keys import Keys


class Table:
    TABLE = "//table"
    BASE = "table"
    HEAD = TABLE + "/div"
    SEARCH = "//input[@type='search']"
    ROW = TABLE+"/tbody/tr"

    HEADER = TABLE+"/thead/tr/th"
    TABLE_HEADER = "/div/div/span[contains(text(),'{}')]"
    SORT_VALUE = HEADER + "[." + TABLE_HEADER + "]"

    HOME_SEARCH = "//input[@type='text']"
    SEARCH_VALUE = "//b[contains(text(),'{}')]"
    BY_ID = "[./td[text()='{}']]"
    KEBAB_IN_ROW = "/td/button"
    NAV_IN_ROW = "./td[2]/div/ice-link/a"
    CHECKBOX_IN_ROW = "td>ice-table-checkbox>div.chkbox-box"
    fields = {}
    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    PAGE_ARROW = "//mat-select"
    PER_PAGE = "//mat-option/span[text()=' {} ']"
    FILTER_ICON = "//div/span/i[contains(@class,'fa-sliders')]"
    SELECT_FILTER = "//span[contains(text(), '{}')]"
    APPLY_FILTER = "//mat-sidenav//span[contains(text(),'Apply Filter')]"     # updated Apply filter
    RESET_FILTER = "//span[contains(text(),'Reset')]"
    TABLE_DATA = ROW + "/td[contains(text(),'{}')]"
    CONFIGURE_GRID = "//app-common-table/div[2]//span[3]/i[1]"

    ACTION_MENU = "//div[contains(@id,'mat-menu-panel')]/div/div"

    SORT = "//table/thead/tr/th[./div/div/span[contains(text(),'Test Names')]]"

    def __init__(self, driver, parent=None):
        self.parent = parent
        self.driver = driver
        try:
            self.driver.scroll_into_view(self.BASE)
        except:
            self.driver.click("html")
            self.driver.scroll_down(self.BASE)
        self.driver.find(self.BASE)


    def _wait_for_loading(self):
        def method():
            big_loader = self.driver.find_all(self.LOADER, timeout=180)
            if len(big_loader) != 0:
                raise Exception("Whole Page still loading...")
            else:
                return True

        return self.driver.wait_until(method)

    def _stat_row(self, row, detail=True):
        if detail is False:
            return {
                "id": self.driver.text(self.fields["name"], web_element=row)
            }
        profile = {}

        for key, field_value in self.fields.items():
            self.driver.scroll_into_view(row)
            try:
                value = self.driver.find_all(field_value, web_element=row)
            except:
                value = ''
            if len(value) != 0:
                value = self.driver.text(field_value, web_element=row)
                if value == "":
                    value = " "
                elif value == "-":
                    value = " "
            else:
                value = " "
            profile[key] = value
        return profile

    def list(self, detail=False):
        content = self._wait_for_loading()
        if not content:
            return ()
        res = []
        while True:
            try:
                rows = self.driver.find_elements_by_xpath(self.ROW)
            except:
                self.driver.scroll_into_view(self.ROW)
                rows = self.driver.find_elements_by_xpath(self.ROW)
            for item in rows:
                res.append(self._stat_row(item, detail))
            break
        self.driver.click("html")
        self.driver.scroll_top()
        return tuple(res)

    def _xpath_row_by_id(self, id_):
        return self.ROW + self.BY_ID.format(id_)

    def _find_row(self, id_):
        ele = self.driver.find(self.BASE)
        content = self._wait_for_loading()
        if not content:
            raise Exception("empty table")

        while True:
            row_xpath = self._xpath_row_by_id(id_)
            res = self.driver.find_all(row_xpath)
            if len(res) > 1:
                raise Exception("Find two items with the same id: ", row_xpath)
            if len(res) == 1:
                return res[0]
            if not self.paginator().try_next_page():
                raise Exception("Cannot find row with id: ", row_xpath)

    def stat(self, id_):
        row = self._find_row(id_)
        return self._stat_row(row, detail=True)

    def nav(self, id_):
        row = self._find_row(id_)
        self.driver.click(self.NAV_IN_ROW, web_element=row)

    @retry(stop_max_attempt_number=3)
    def open_menu(self, id_, method="kebab"):
        row = self._find_row(id_)
        # Sometimes the kebab menu on dropdown does not work. 
        # scrolling to view and having a delay to overcome the issue
        self.driver.scroll_into_view(row)
        time.sleep(1)
        if method == "kebab":
            self.driver.click(self.KEBAB_IN_ROW, web_element=row)
        else:
            raise GenericException({
                "message": "Invalid param for method. Only `kebab`, `right` and `table` are allowed.",
                "param": method
            })

    def _select_single(self, id_):
        row = self._find_row(id_)
        status = "ui-state-active" in self.driver.find(self.CHECKBOX_IN_ROW, web_element=row).get_attribute("class")
        if status is False:
            self.driver.click(self.CHECKBOX_IN_ROW, web_element=row)

    def select(self, id_):
        for item in maybe_to_tuple(id_):
            self._select_single(item)

    def select_all(self):
        content = self._wait_for_loading()
        if not content:
            raise Exception("empty table")
        self._wait_for_content_load()
        self.driver.click(self.SELECT_ALL)

    def selected_count(self):
        count_info = self.driver.text(self.SELECT_COUNT)
        return int(count_info.split(" ")[0])

    def show_selected(self):
        self.driver.click(self.SHOW_SELECTED)

    def click_table_header(self, column_name):
        self.driver.click(self.SORT_VALUE.format(column_name))
        sort_order = self.driver.find(self.SORT_VALUE.format(column_name)).get_attribute("aria-sort")
        self.driver.wait_for_disappear(self.LOADER, timeout=180)
        return sort_order

    def table_scroll(self):
        a = ActionChains(self.driver)
        table_area = self.driver.find("//mat-card/mat-card-content/app-common-table/perfect-scrollbar")
        a.move_to_element(table_area).click().perform()
        a.key_down(Keys.CONTROL).send_keys(Keys.HOME).key_up(Keys.CONTROL).perform()

    def search(self, query):
        try:
            self.driver.input(self.SEARCH, query)
        except:
            self.driver.click("html")
            self.driver.scroll_top()
            self.driver.input(self.SEARCH, query)
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click("html")
        self.driver.scroll_down()

    def dashboard_search(self, query):
        self.driver.input(self.HOME_SEARCH, query)
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.SEARCH_VALUE.format(query))
        self.driver.wait_for_disappear(self.LOADER, timeout=120)

    def control_table_checkbox(self):
        CheckBoxSelect(self.driver).control_checkbox()

    def item_per_page(self, item):
        self.driver.click(self.PAGE_ARROW)
        self.driver.click(self.PER_PAGE.format(item))
        self.driver.wait_for_disappear(self.LOADER, timeout=120)

    def filter_(self, filter_, option=None):
        self.driver.wait_for_disappear(self.LOADER, timeout=240)
        self.driver.click("html")
        self.driver.scroll_top()
        self.driver.click(self.FILTER_ICON)
        self.driver.click(self.SELECT_FILTER.format(filter_))
        filter_options = CheckBoxSelect(self.driver).select_option(option)
        self.driver.click(self.APPLY_FILTER)
        self.driver.wait_for_disappear(self.LOADER, timeout=200)
        return filter_options

    def action(self):
        res = []
        value = self.driver.find_all(self.ACTION_MENU)
        for item in value:
            res.append(item.text)
        return res

    def configure_grid(self, query):
        self.driver.click(self.CONFIGURE_GRID)
        AbstractDialog(self.driver).grid_label_click(query)
        self.driver.wait_for_disappear(self.LOADER, timeout=60)


class TableAllTests(Table):
    fields = {
        "Test Names": "//td[contains(@class,'test_name')]",
        "Test Window": "//td[contains(@class,'test_window')]/span",
        "Details": "//td[contains(@class,'details')]/span",
        "Created At": "//td[contains(@class,'Created')]",
        "Test Type": "//td[contains(@class,'test_type')])",
        "Last Modified At": "//td[contains(@class,'Modified')]",
        "Status": "//td[contains(@class,'status')]/span"
    }



class TestMeasurementTable(Table):
    BASE = "//table"
    fields = {
        "Test Store Customer Number": "//td[contains(@class,'teststoreid')]",
        "Test Store Pre Period Avg/Week (£)": "//td[contains(@class,'testgrppreavg')]",
        "Test Store Post Period Avg/Week (£)": "//td[contains(@class,'testgrppostavg')]",
        "Test Store Pre Vs Post Lift (%)": "//td[contains(@class,'testprepost')]",
        "Test Store Post period Estimated Avg/Week (£)": "//td[contains(@class,'testgroup_postEstimated')]",
        "Test Store Customer Group": "//td[contains(@class,'banner')]",
        "Test Store Customer Chain": "//td[contains(@class,'testStoreCustomerChain')]",
        "Control Store Customer Number": "//td[contains(@class,'cntrlstreid')]",
        "Control Store Pre Period Avg/Week (£)": "//td[contains(@class,'cntrlgrppreavg')]",
        "Control Store Post Period Avg/Week (£)": "//td[contains(@class,'cntrlgrppostavg')]",
        "Control Store Pre Vs Post Lift (%)": "//td[contains(@class,'cntrlprepost')]",
        "Control Store Customer Group": "//td[contains(@class,'cntrlbanner')]",
        "Control Store Customer Chain": "//td[contains(@class,'controlStoreCustomerChain')]",
        "Test vs Control Lift %": "//td[contains(@class,'testvscntrl')]",
        "Incremental RSV": "//td[contains(@class,'incremantal_rsv')]",
        "Outlier": "//td[contains(@class,'outlier_format')]",
    }


class TableSelectStores(Table):
    fields = {
        "Customer Number": "//td[contains(@class,'column-store_no')]",
        "Customer Group": "//td[contains(@class,'column-banner ')]",
        "Territory ID": "//td[contains(@class,'column-Territory')]",
        "Store Number": "//td[contains(@class,'column-store_segment')]",
        }


class TableStoresCorrelation(Table):

    fields = {
        "Customer Number": "//td[contains(@class,'column-store_no')]",
        "Outlet Address": "//td[contains(@class,'column-Street')]",
        "Similarity value to population": "//td[contains(@class,'column-similarity_value')]",
        "Sales correlation": "//td[contains(@class,'column-sales_corelation')]",
        }


class TableControlStores(Table):
    CONFIGURE_GRID = "//app-common-table/div[2]//i"
    fields = {
        "Customer Number": "//td[contains(@class,'test_storeno')]",
        "Customer Group": "//td[contains(@class,'control_mapped')]",
        "Control Store Id": "//td[contains(@class,'similar_value')]",
        "Customer Chain": "//td[contains(@class ,'test_storedetails')]",
        "control_customer group": "//td[contains(@class,'corr_value')]",
        "control_customer chain": "//td[contains(@class,'store_segment')]",
        "Sales Correlation": "//td[contains(@class,'correlation')]",
        "Similarity Value": "//td[contains(@class,'others')]",
        "Similarity CBU level": "//td[contains(@class,'similarCBUvalue')]",
        "Difference": "//td[contains(@class,'difference')]",
    }
