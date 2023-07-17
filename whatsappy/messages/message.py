from __future__ import annotations

import datefinder
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, List, Literal

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
        * chat (Chat | Group): The chat the message was sent in.
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
        container = _element.find_element(By.CSS_SELECTOR, Selectors.MESSAGE_CONTAINER)

        self.author = container.find_element(By.CSS_SELECTOR, Selectors.MESSAGE_AUTHOR).get_attribute("aria-label")[:-1]

        if content := find_element_if_exists(container, By.CSS_SELECTOR, Selectors.MESSAGE_CONTENT):
            self.content = emoji_to_text(content)

        if info := find_element_if_exists(container, By.CSS_SELECTOR, Selectors.MESSAGE_INFO):
            dates = list(datefinder.find_dates(info.text))
            self.timestamp = dates[0] if dates else datetime(1900, 1, 1, 0, 0)
        else:
            self.timestamp = list(datefinder.find_dates(container.find_element(By.CSS_SELECTOR, Selectors.MESSAGE_META).text))[0]
            self.timestamp = self.timestamp.replace(year=1900, month=1, day=1)

        self.is_forwarded = element_exists(container, By.CSS_SELECTOR, Selectors.MESSAGE_FORWARDED)
        self.is_reply = element_exists(container, By.CSS_SELECTOR, Selectors.MESSAGE_QUOTE)

    def __str__(self) -> str:
        return f"{self.author}: {self.content}"

    def reply(self,
              message: str = None,
              attatchments: List[str] = None,
              type: Literal["auto", "document", "midia", "contact"] = "auto"
        ) -> None:
        """Replies to the message.

        #### Arguments
            * message (str, optional): The message to send. Defaults to None.
            * attatchments (List[Any], optional): The attatchments to send. Defaults to None.
            * type (Literal["auto", "document", "midia", "contact"], optional): The type of the attatchments. Defaults to "auto".
            If the type is specified, all the attatchments must be of the same type.
        """

        action = ActionChains(self._whatsapp.driver)
        action.double_click(self._element).perform()

        self.chat.send(message, attatchments, type)

    def delete(self) -> None:
        """Deletes the message."""

        raise NotImplementedError("This method is not implemented yet.")

    def forward(self, chats: List[str]) -> None:
        """Forwards the message to the specified chats.

        #### Arguments
            * chats (List[str]): The chats to forward the message to.
        """

        raise NotImplementedError("This method is not implemented yet.")

    def react(self, emoji: str) -> None:
        """Reacts to the message with the specified emoji.

        #### Arguments
            * emoji (str): The emoji to react with.
        """

        raise NotImplementedError("This method is not implemented yet.")