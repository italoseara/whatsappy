from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal

from .. import whatsapp

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
    
    def send(self, message: str, attatchments: List[str] = []) -> None:
        """Sends a message to the chat.

        Args:
            message (str): The message to send.
            attatchments (List[str], optional): A list of paths to attatchments to send. Defaults to [].
        """

        raise NotImplementedError("This method is not implemented yet.")

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

    def delete(self) -> None:
        """Deletes the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def pin(self) -> None:
        """Pins the chat."""

        raise NotImplementedError("This method is not implemented yet.")
