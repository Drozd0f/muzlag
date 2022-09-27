class InputValueError(Exception):
    """Exception raised for errors in the input value.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message='Input value is not valid'):
        self.message = message
        super().init(self.message)
