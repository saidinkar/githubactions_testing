class GenericException(Exception):
    """ A generic Exception for all Test Exception
    """
    def __init__(self, error_obj):
        self.error_obj = error_obj
        super().__init__(error_obj["message"])


class TAEditFormException(GenericException):
    """ This exception is raised there is validation error on the edit form
    """
    def __init__(self, error_message):

        super().__init__({
            "message": error_message,
        })