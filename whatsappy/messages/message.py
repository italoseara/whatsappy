from __future__ import annotations

import datefinder
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from ..util import *
from .. import chat
from .. import whatsapp

@dataclass(init=False)
class Message:
    """Utility class for messages. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead.

    #### Properties
        * author (str): The author of the message.
        * content (str): The content of the message.
        * timestamp (datetime): The timestamp of the message.
        * chat (Any): The chat the message was sent in.
        * attatchments (List[Any]): The attatchments of the message.
        * is_forwarded (bool): Whether the message is forwarded.
        * is_reply (bool): Whether the message is a reply.
    """

    _element: WebElement = field(repr=False)
    _whatsapp: whatsapp.Whatsapp = field(repr=False)
    
    chat: chat.Chat | chat.Group = None
    author: str = None
    content: str = None
    timestamp: datetime = None
    attatchments: List[Any] = None
    is_forwarded: bool = False
    is_reply: bool = False
    
    def __init__(self, _whatsapp: whatsapp.Whatsapp, _element: WebElement, chat: chat.Chat | chat.Group) -> None:
        self._whatsapp = _whatsapp
        self._element = _element
        self.chat = chat

        # TODO: Add support for attatchments.

        self.author = _element.find_element(By.CSS_SELECTOR, Selectors.MESSAGE_AUTHOR).get_attribute("aria-label")[:-1]

        if content := find_element_if_exists(_element, By.CSS_SELECTOR, Selectors.MESSAGE_CONTENT):
            self.content = message_to_text(content)

        if info := find_element_if_exists(_element, By.CSS_SELECTOR, Selectors.MESSAGE_INFO):
            self.timestamp = list(datefinder.find_dates(info.text))[0]
        else:
            self.timestamp = list(datefinder.find_dates(_element.find_element(By.CSS_SELECTOR, Selectors.MESSAGE_META).text))[0]
            self.timestamp = self.timestamp.replace(year=1900, month=1, day=1)

        self.is_forwarded = element_exists(_element, By.CSS_SELECTOR, Selectors.MESSAGE_FORWARDED)
        self.is_reply = element_exists(_element, By.CSS_SELECTOR, Selectors.MESSAGE_QUOTE)

