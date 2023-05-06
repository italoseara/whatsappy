from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from .. import whatsapp
from ..util import *
from ..chat import Chat, Group

@dataclass(init=False)
class UnreadMessage:
    """An unread chat. Should not be initialized directly, use `whatsappy.Whatsapp.unread_messages` instead.

    #### Properties
        * name (str): The name of the unread chat.
        * count (int): The count of the unread chat.
        * message (str): The last message of the unread chat.
    """

    _whatsapp: whatsapp.Whatsapp = field(repr=False)
    _element: WebElement = field(repr=False)
    
    name: str
    count: int
    message: str

    def __init__(self, _whatsapp: whatsapp.Whatsapp, _element: WebElement) -> None:
        self._whatsapp = _whatsapp
        self._element = _element

        self.name = _element.find_element(By.CSS_SELECTOR, Selectors.UNREAD_TITLE).get_attribute("title")
        self.count = int(_element.find_element(By.CSS_SELECTOR, Selectors.UNREAD_BADGE).text) or 1

        try:
            self.message = _element.find_element(By.CSS_SELECTOR, Selectors.UNREAD_LAST_MESSAGE).get_attribute("title")
            self.message = self.message[1:-1]
        except NoSuchElementException:
            self.message = None

    def reply(self, 
              message: str, 
              attatchments: List[str] = None, 
              type: Literal["auto", "document", "midia", "contact"] = "auto"
        ) -> Chat | Group:
        """Reply to the unread chat.

        #### Arguments
            * message (str): The message to reply with.
            * attatchments (List[str], optional): The attatchments to reply with. Defaults to None.
            * type (Literal["auto", "document", "midia", "contact"], optional): The type of the attatchments. Defaults to "auto".

        #### Returns
            * Chat | Group: The chat or group that the message was sent to.
        """

        chat = self._whatsapp.open(self.name)
        chat.send(message, attatchments, type)

        return chat