from datetime import datetime
from dataclasses import dataclass, field

from selenium.webdriver.remote.webelement import WebElement

from .. import whatsapp
from ..chat import Conversation

@dataclass(init=False)
class Message:
    """Utility class for messages. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead."""

    _element: WebElement = field(repr=False)
    _whatsapp: whatsapp.Whatsapp = field(repr=False)
    author: str = None
    content: str = None
    timestamp: datetime = None
    chat: Conversation = None
    is_forwarded: bool = None
    is_reply: bool = None
    
    def __init__(self, _whatsapp: whatsapp.Whatsapp, _element: WebElement = None) -> None:
        self._whatsapp = _whatsapp
        self._element = _element

        # TODO: Parse the message element and set the properties accordingly.
    
    @property
    def is_starred(self) -> bool:
        """Returns whether the message is starred."""

        raise NotImplementedError("This method is not implemented yet.")
    
    @property
    def is_deleted(self) -> bool:
        """Returns whether the message is deleted."""

        raise NotImplementedError("This method is not implemented yet.")
