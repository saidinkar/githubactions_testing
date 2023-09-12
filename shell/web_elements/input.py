from .abstract import Abstract


class Input(Abstract):

    SELECTOR = "input"

    def input(self, value):
        self.driver.input(self.BASE, value, web_element=self.web_element)
        return self

    def get_value(self):
        return self.driver.find(self.BASE, web_element=self.web_element).get_attribute("value")
