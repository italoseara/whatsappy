class WhatsappyError(Exception):
    """The base exception type for the errors specific for this library."""


class LoginError(WhatsappyError):
    """Raised when there is an error when trying to login."""


class BadPathError(WhatsappyError):
    """Raised when there is an invalid path."""


class PermissionError(WhatsappyError):
    """Raised when the user does not have permission."""


class InvalidActionError(WhatsappyError):
    """Raised when the user tries to do an invalid action."""