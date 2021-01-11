class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class PresentationParsingError(Exception):
    """Raised when presentation parser cannot parse url"""
    pass


class PresentationNotFound(Exception):
    """Raised when presentation parser not found any slide"""
    def __init__(self, msg="Presentation parser cannot find any slide"):
        super(PresentationNotFound, self).__init__(msg)
