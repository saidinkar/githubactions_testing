from ...base.exceptions.element import ElementNotFoundException
from ...base.exceptions.element import ElementNotVisibleException


class Abstract:
    
    SELECTOR = ""

    def __init__(self, driver, parent, web_element=None):
        self.driver = driver
        self.web_element = web_element
        if parent.endswith("/"):
            parent = parent[:-1]
        if parent.split("/")[-1].startswith(self.SELECTOR):
            self.BASE = parent
        if parent.split("/")[-1].startswith("md-radio-group") or parent.split("/")[-1].startswith("md-checkbox"):
            self.BASE = parent
        elif self.SELECTOR == "mat-radio-group":
            self.BASE = parent + "/div/" + self.SELECTOR
        else:
            self.BASE = parent + "/" + self.SELECTOR

        base = self.driver.find_all(self.BASE, web_element=web_element)
        if len(base) == 0:
            raise ElementNotFoundException(self.BASE)
