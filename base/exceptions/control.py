from ..exceptions import GenericException


class ValueNotFoundException(GenericException):
    """ This exception is raised when the control does not have a specific value
    """
    def __init__(self, locator, value):

        super().__init__({
            "message": f"{value} not found in control {locator}",
            "locator": locator,
            "value": value
        })


class ControlNotFoundException(GenericException):
    """ This exception when a specific control not found
    """
    def __init__(self, key):

        super().__init__({
            "message": f"'{key}' not found ",
            "key": key
        })


class ValidationException(GenericException):
    """ This exception is raised there is validation error on the form field
    """
    def __init__(self, key, error_messages):

        super().__init__({
            "message": f"Validation Error Key: {key}, error: {error_messages}",
            "key": key,
            "error_messages": error_messages
        })
