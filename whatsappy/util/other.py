import re
from dataclasses import dataclass
from threading import Thread, Event

class MyThread(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self) -> None:
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

@dataclass
class UnreadChat:
    """An unread chat.

    Properties:
        chat (str): The chat of the unread chat.
        count (int): The count of the unread chat.
        last_message (str): The last message of the unread chat.
    """

    chat: str
    count: int
    last_message: str

phone_number_regex = re.compile(r'\+?\d{1,3}[-.\s]?\d{1,14}[-.\s]?\d{1,14}[-.\s]?\d{1,14}')