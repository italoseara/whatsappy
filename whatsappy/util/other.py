import re
import mimetypes
from threading import Thread, Event

class MyThread(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self) -> None:
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

def get_attachment_type(attachment: str) -> str:
    if "." not in attachment:
        return "contact"
    
    mime = mimetypes.guess_type(attachment)[0]

    if mime is None:
        return "document"

    match mime.split("/")[0]:
        case "image" | "video" | "audio":
            return "midia"
        case _:
            return "document"

phone_number_regex = re.compile(r'\+?\d{1,3}[-.\s]?\d{1,14}[-.\s]?\d{1,14}[-.\s]?\d{1,14}')