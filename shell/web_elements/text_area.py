from .abstract import Abstract


class TextArea(Abstract):

    SELECTOR = "textarea"

    def __init__(self, driver, parent):
        Abstract.__init__(self, driver, parent)

    def input(self, value):
        self.driver.input(self.BASE, value)
