from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .. import whatsapp
from ..util import *

@dataclass(init=False)
class Conversation:
    """Utility class for chats and groups. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead."""
    
    _whatsapp: whatsapp.Whatsapp = field(repr=False)

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        self._whatsapp = _whatsapp

    @property
    def starred_messages(self) -> List[str]:
        """Returns a list of starred messages in the chat."""

        raise NotImplementedError("This method is not implemented yet.")
    
    def send(self, message: str = "", attatchments: List[str] = []) -> None:
        """Sends a message to the chat.

        Args:
            message (str): The message to send.
            attatchments (List[str], optional): A list of paths to attatchments to send. Defaults to [].
        """

        if not message and not attatchments:
            raise ValueError("You must provide a message or attatchments to send.")
        
        input_chat = self._whatsapp.driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_INPUT)
        input_chat.click() # Focus the input

        for line in message.split("\n"):
            input_chat.send_keys(line)
            send_shortcut(self._whatsapp.driver, Keys.SHIFT, Keys.ENTER)            

        input_chat.send_keys(Keys.ENTER)

    def send_contacts(self, contacts: List[str]) -> None:
        """Sends contacts to the chat.

        Args:
            contacts (List[str]): A list of numbers or names to send.
        """

        raise NotImplementedError("This method is not implemented yet.")
    
    def send_sticker(self, sticker: str) -> None:
        """Sends a sticker to the chat.

        Args:
            sticker (str): The path of the image to send.
        """

        raise NotImplementedError("This method is not implemented yet.")

    def mute(self, time: Literal["8 hours", "1 week", "Always"]) -> None:
        """Mutes the chat notifications.

        Args:
            time (Literal["8 hours", "1 week", "Always"]): The time to mute the chat for.
        """

        raise NotImplementedError("This method is not implemented yet.")

    def unmute(self) -> None:
        """Unmutes the chat notifications."""

        raise NotImplementedError("This method is not implemented yet.")

    def archive(self) -> None:
        """Archives the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def block(self) -> None:
        """Blocks the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def unblock(self) -> None:
        """Unblocks the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def delete(self) -> None:
        """Deletes the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def pin(self) -> None:
        """Pins the chat."""

        raise NotImplementedError("This method is not implemented yet.")
