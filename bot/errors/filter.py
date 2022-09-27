class FilterStrLenError(Exception):
    """Exception raised for errors in the input value.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message='Input lenght of srting is too long'):
        self.message = message
        super().init(self.message)
