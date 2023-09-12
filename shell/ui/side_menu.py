from ...base.exceptions import GenericException
from ..web_elements.dropdown import DropDown


class SideMenuOption:

    DASHBOARD = "Dashboard"
    CREATE_NEW_TEST = "Create New Test"
    ANALYSE_TEST_IMPACT = "Analyse Test Impact"


class SideMenu:
    MENU = "//mat-nav-list"
    CATEGORY = MENU + "/a/span[@class='mat-list-item-content']/div/span"
    ITEM_BY_LABEL = MENU + "/a[@title='{}']"
    MARS_WRIGLEY = MENU + "/mat-list-item/span/mat-icon"
    CHECK = "//div[@class='sidebar_border_active']"
    COUNTRY_DROPDOWN = "//mat-list-item/span/ngx-select/div/div/div/span/span"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    COUNTRY_DROPDOWN_LIST = "//ngx-select-choices/ul/li/a"
    DROPDOWN_COUNTRY_NAME = COUNTRY_DROPDOWN_LIST + "/span[contains(text(),'{}')]"

    def __init__(self, driver):
        self.driver = driver
        self.driver.find(self.MENU)
        self.driver.wait_for_disappear(self.LOADER, timeout=240)


    def select_option(self, target):
        option_locator = self.ITEM_BY_LABEL.format(target)
        option = self.driver.find_all(option_locator)
        if len(option) == 0:
            raise GenericException({
                "message": "item not found",
                "item": target
            })
        option_class = self.driver.find(option_locator).get_attribute("class")
        if "active-menuitem-routerlink" not in option_class:
            try:
                self.driver.click(option_locator)
            except:
                self.driver.scroll_into_view(option_locator)
                self.driver.click(option_locator)
            self.driver.wait_for_disappear(self.LOADER, timeout=120)

    def list_category(self):
        categories = self.driver.find_all(self.CATEGORY)
        res = []
        for item in categories:
            res.append(item.text)
        return tuple(res)

    def switch_collapse(self, switch):
        check_ = self.driver.find_all(self.CHECK)
        if switch is "expand":
            if len(check_) == 0:
                self.driver.click(self.MARS_WRIGLEY)
                if len(self.driver.find_all(self.CHECK)) != 0:
                    return "expand"
            return "expand"
        elif switch is "collapse":
            if len(check_) != 0:
                self.driver.click(self.MARS_WRIGLEY)
                if len(self.driver.find_all(self.CHECK)) == 0:
                    return "collapse"
            return "collapse"

    def county_dropdown(self, country):
        self.driver.click(self.COUNTRY_DROPDOWN)
        country_list = self.driver.find_all(self.COUNTRY_DROPDOWN_LIST)
        for i in country_list:
            if country == i.text:
                self.driver.click(self.DROPDOWN_COUNTRY_NAME.format(country))
        country = self.driver.find(self.COUNTRY_DROPDOWN).text
        return country

