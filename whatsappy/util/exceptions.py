class InvalidEventException(Exception):
    """Exception raised when an invalid event is passed to the event handler."""
    ...

class NotSelectedException(Exception):
    """Exception raised when a user tries to use a feature that requires a selected chat, but no chat is selected."""
    ...