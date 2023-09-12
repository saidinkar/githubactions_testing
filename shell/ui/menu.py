
from ...base.exceptions import GenericException

GLOBAL_MENU_BASE = "//div[contains(@class,'mat-menu-content')]"
MENU_ITEM_BY_LABEL = "/div[text()='{}']"
GLOBAL_MENU_ITEM_BY_LABEL = GLOBAL_MENU_BASE + MENU_ITEM_BY_LABEL


def select_menu_item_by_label(driver, xpath: str, label: str, parent=None):
    try:
        driver.click(xpath, web_element=parent)
    except Exception as excp:
        raise GenericException({
            "message": "Menu Item not found",
            "item": label,
            "xpath": xpath
        }) from excp


class AbstractMenu:
    BASE = None

    def __init__(self, driver, parent=None):
        self.driver = driver
        self.parent = parent
        if parent is not None:
            if isinstance(parent, str):
                parent = self.driver.find(parent)
        self.driver.find(self.BASE, web_element=parent)

    def select(self, label):
        raise NotImplementedError("Not implemented yet")


class KebabMenu(AbstractMenu):
    BASE = GLOBAL_MENU_BASE

    def select(self, label):
        select_menu_item_by_label(self.driver, GLOBAL_MENU_ITEM_BY_LABEL.format(label), label, parent=self.parent)


class Menu:

    def __init__(self, driver, method="kebab", parent=None):
        self.driver = driver

        if method == "kebab":
            self.menu = KebabMenu(self.driver)
        else:
            raise GenericException({
                "message": "Invalid param for method. Only `kebab`, `right` and `table` are allowed.",
                "param": method
            })

    def select(self, label):
        self.menu.select(label)
