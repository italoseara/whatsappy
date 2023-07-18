class InvalidEventException(Exception):
    """Exception raised when an invalid event is passed to the event handler."""
    ...

class NotSelectedException(Exception):
    """Exception raised when a user tries to use a feature that requires a selected chat, but no chat is selected."""
    ...

class MaxPinnedChatsException(Exception):
    """Exception raised when a user tries to pin a chat, but the maximum number of pinned chats has been reached."""
    ...

class ContactNotFoundException(Exception):
    """Exception raised when a user tries to open a chat with a contact that doesn't exist."""
    ...

class UserNotFoundException(Exception):
    """Exception raised when a user tries to perform an action on a user that doesn't exist."""
    ...

class UserAlreadyAdminException(Exception):
    """Exception raised when a user tries to promote a user to admin, but the user is already an admin."""
    ...

class UserNotAdminException(Exception):
    """Exception raised when a user tries to demote a user from admin, but the user is not an admin."""
    ...