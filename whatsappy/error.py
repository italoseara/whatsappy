class WhatsappyError(Exception):
    """The base exception type for the errors specific for this library."""

class LoginError(WhatsappyError):
    """Describes an error on the login process."""

class BadPathError(WhatsappyError):
    """Describes an invalid path."""
