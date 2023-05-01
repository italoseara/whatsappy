from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Any
from multimethod import multimethod

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
    
    def send(self, 
             message: str = None, 
             attatchments: List[Any] = None, 
             type: Literal["auto", "audio", "contact", "document", "image", "sticker", "video"] = "auto"
        ) -> None:
        """Sends a message to the chat.

        Args:
            message (str, optional): The message to send. Defaults to None.
            attatchments (List[Any], optional): The attatchments to send. Defaults to None.
            type (Literal["auto", "audio", "contact", "document", "image", "sticker", "video"], optional): The type of the attatchments. Defaults to "auto". "auto" will automatically detect the type, but it cannot detect contacts and stickers.
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
