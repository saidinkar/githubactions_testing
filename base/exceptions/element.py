from ..exceptions import GenericException


class ElementNotFoundException(GenericException):
    """ This exception is raised when the expected element is not found
    """

    def __init__(self, locator):

        super().__init__({
            "message": f"Element not found - {locator}",
            "locator": locator
        })


class ElementNotVisibleException(GenericException):
    """ This exception is raised when the expected element is not visible
    """

    def __init__(self, locator):

        super().__init__({
            "message": f"Element not visible - {locator}",
            "locator": locator
        })


class ElementNotAppearException(GenericException):
    """ This exception is raised when the expected element does not appear
    """

    def __init__(self, locator):

        super().__init__({
            "message": f"Element does not appear - {locator}",
            "locator": locator
        })
